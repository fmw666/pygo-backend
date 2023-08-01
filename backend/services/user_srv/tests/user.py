import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

import time

import grpc

from user_srv.proto import user_pb2, user_pb2_grpc


class UserTest:
    def __init__(self) -> None:
        # try to connect to the server
        channel = grpc.insecure_channel("localhost:50051")
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        rsp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfo(pn=2, pSize=2))
        print(rsp.total)
        for user in rsp.data:
            print(user.nickName, user.mobile, user.birthDay)
    
    def get_user_by_id(self, id):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(id=id))
        print(rsp.mobile, rsp.nickName, rsp.birthDay)
    
    def get_user_by_mobile(self, mobile):
        rsp: user_pb2.UserInfoResponse = self.stub.GetUserByMobile(user_pb2.MobileRequest(mobile=mobile))
        print(rsp.mobile, rsp.nickName, rsp.birthDay)
    
    def create_user(self, nick_name, mobile, password):
        rsp: user_pb2.UserInfoResponse = self.stub.CreateUser(user_pb2.CreateUserInfo(
            nickName=nick_name,
            mobile=mobile,
            password=password,
        ))
        print(rsp.id)
    
    def update_user(self, id, nick_name, gender, birthday):
        self.stub.UpdateUser(user_pb2.UpdateUserInfo(
            id=id,
            nickName=nick_name,
            gender=gender,
            birthDay=birthday,
        ))
        # check on database


if __name__ == "__main__":
    user_test = UserTest()
    # user_test.user_list()
    # user_test.get_user_by_id(211)
    # user_test.get_user_by_mobile("13800000001")
    # user_test.create_user("test", "19800000001", "123456")
    user_test.update_user(2, "test222", "female", int(time.mktime(time.strptime("1990-01-01", "%Y-%m-%d"))))
