import grpc
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from userop_srv.model.models import UserFavorite
from userop_srv.proto import userfavorite_pb2, userfavorite_pb2_grpc


class UserFavoriteServicer(userfavorite_pb2_grpc.UserFavoriteServicer):

    @logger.catch
    def GetUserFavoriteList(
        self,
        request: userfavorite_pb2.UserFavoriteRequest,
        context: grpc.ServicerContext
    ) -> userfavorite_pb2.UserFavoriteListResponse:
        """
        获取收藏列表
        :param request: UserFavoriteRequest
        :param context: grpc.ServicerContext
        :return: UserFavoriteListResponse
        """
        rsp = userfavorite_pb2.UserFavoriteListResponse()
        favorites = UserFavorite.select()
        if request.userId:
            favorites = favorites.where(UserFavorite.user == request.userId)
        if request.goodsId:
            favorites = favorites.where(UserFavorite.goods == request.goodsId)

        rsp.total = favorites.count()
        for favorite in favorites:
            favorite_rsp = userfavorite_pb2.UserFavoriteResponse()

            favorite_rsp.userId = favorite.user
            favorite_rsp.goodsId = favorite.goods

            rsp.data.append(favorite_rsp)

        return rsp

    @logger.catch
    def GetUserFavoriteDetail(
        self,
        request: userfavorite_pb2.UserFavoriteRequest,
        context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        """
        获取收藏详情
        :param request: UserFavoriteRequest
        :param context: grpc.ServicerContext
        :return: Empty
        """
        try:
            _ = UserFavorite.get(
                UserFavorite.user == request.userId,
                UserFavorite.goods == request.goodsId)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("favorite not found")
            return empty_pb2.Empty()

    @logger.catch
    def CreateUserFavorite(
        self,
        request: userfavorite_pb2.UserFavoriteRequest,
        context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        """
        创建收藏
        :param request: UserFavoriteRequest
        :param context: grpc.ServicerContext
        :return: Empty
        """
        favorite = UserFavorite(
            user=request.userId,
            goods=request.goodsId
        )
        favorite.save(force_insert=True)

        return empty_pb2.Empty()

    @logger.catch
    def DeleteUserFavorite(
        self,
        request: userfavorite_pb2.UserFavoriteRequest,
        context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        """
        删除收藏
        :param request: UserFavoriteRequest
        :param context: grpc.ServicerContext
        :return: Empty
        """
        try:
            favorite = UserFavorite.get(
                UserFavorite.user == request.userId,
                UserFavorite.goods == request.goodsId)
            favorite.delete_instance(permanently=True)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("favorite not found")
            return empty_pb2.Empty()
