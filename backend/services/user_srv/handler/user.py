import time
from datetime import date
from passlib.hash import pbkdf2_sha256

import grpc
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from user_srv.model.models import User
from user_srv.proto import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):

    def convert_user_to_rsp(self, user: User) -> user_pb2.UserInfoResponse:
        """
        将 user 对象转换为 UserInfoResponse 对象
        :param user: user 对象
        :return: UserInfoResponse 对象
        """
        user_info_rsp = user_pb2.UserInfoResponse()

        user_info_rsp.id = user.id
        user_info_rsp.mobile = user.mobile
        user_info_rsp.role = user.role
        user_info_rsp.password = user.password

        if user.nick_name:
            user_info_rsp.nickName = user.nick_name
        if user.gender:
            user_info_rsp.gender = user.gender
        if user.birthday:
            user_info_rsp.birthDay = int(
                time.mktime(user.birthday.timetuple())
            )

        return user_info_rsp

    @logger.catch
    def GetUserList(
        self, request: user_pb2.PageInfo, context: grpc.ServicerContext
    ) -> user_pb2.UserListResponse:
        """
        获取用户列表
        :param request: PageInfo
        :param context: grpc.ServicerContext
        :return: UserListResponse
        """
        rsp = user_pb2.UserListResponse()

        users = User.select()
        rsp.total = users.count()

        start = 0
        per_page_nums = 10
        if request.pSize:
            per_page_nums = request.pSize
        if request.pn:
            start = (request.pn - 1) * per_page_nums

        users = users.limit(per_page_nums).offset(start)

        for user in users:
            rsp.data.append(self.convert_user_to_rsp(user))

        return rsp

    @logger.catch
    def GetUserById(
        self, request: user_pb2.IdRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserInfoResponse:
        """
        通过 id 获取用户信息
        :param request: IdRequest
        :param context: grpc.ServicerContext
        :return: UserInfoResponse
        """
        try:
            user = User.get(User.id == request.id)
            return self.convert_user_to_rsp(user)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("user not found")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByMobile(
        self, request: user_pb2.MobileRequest, context: grpc.ServicerContext
    ) -> user_pb2.UserInfoResponse:
        """
        通过手机号获取用户信息
        :param request: MobileRequest
        :param context: grpc.ServicerContext
        :return: UserInfoResponse
        """
        try:
            user = User.get(User.mobile == request.mobile)
            return self.convert_user_to_rsp(user)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("user not found")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CreateUser(
        self, request: user_pb2.CreateUserInfo, context: grpc.ServicerContext
    ) -> user_pb2.UserInfoResponse:
        """
        创建用户
        :param request: CreateUserInfo
        :param context: grpc.ServicerContext
        :return: UserInfoResponse
        """
        try:
            User.get(User.mobile == request.mobile)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("user already exists")
            return user_pb2.UserInfoResponse()
        except DoesNotExist:
            pass

        user = User()
        user.nick_name = request.nickName
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.password)
        user.save()

        return self.convert_user_to_rsp(user)

    @logger.catch
    def UpdateUser(
        self, request: user_pb2.UpdateUserInfo, context: grpc.ServicerContext
    ) -> user_pb2.UserInfoResponse:
        """
        更新用户信息
        :param request: UpdateUserInfo
        :param context: grpc.ServicerContext
        :return: UserInfoResponse
        """
        try:
            user = User.get(User.id == request.id)
            user.nick_name = request.nickName
            user.gender = request.gender
            user.birthday = date.fromtimestamp(request.birthDay)
            user.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("user not found")
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CheckPassword(
        self,
        request: user_pb2.PasswordCheckInfo,
        context: grpc.ServicerContext
    ) -> user_pb2.CheckPasswordResponse:
        """
        检查密码
        :param request: PasswordCheckInfo
        :param context: grpc.ServicerContext
        :return: CheckPasswordResponse
        """
        return user_pb2.CheckPasswordResponse(
            success=pbkdf2_sha256.verify(request.password,
                                         request.encryptedPassword))
