# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from . import userfavorite_pb2 as userfavorite__pb2


class UserFavoriteStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUserFavoriteList = channel.unary_unary(
                '/UserFavorite/GetUserFavoriteList',
                request_serializer=userfavorite__pb2.UserFavoriteRequest.SerializeToString,
                response_deserializer=userfavorite__pb2.UserFavoriteListResponse.FromString,
                )
        self.GetUserFavoriteDetail = channel.unary_unary(
                '/UserFavorite/GetUserFavoriteDetail',
                request_serializer=userfavorite__pb2.UserFavoriteRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.CreateUserFavorite = channel.unary_unary(
                '/UserFavorite/CreateUserFavorite',
                request_serializer=userfavorite__pb2.UserFavoriteRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.DeleteUserFavorite = channel.unary_unary(
                '/UserFavorite/DeleteUserFavorite',
                request_serializer=userfavorite__pb2.UserFavoriteRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class UserFavoriteServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUserFavoriteList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserFavoriteDetail(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateUserFavorite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteUserFavorite(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserFavoriteServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUserFavoriteList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserFavoriteList,
                    request_deserializer=userfavorite__pb2.UserFavoriteRequest.FromString,
                    response_serializer=userfavorite__pb2.UserFavoriteListResponse.SerializeToString,
            ),
            'GetUserFavoriteDetail': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserFavoriteDetail,
                    request_deserializer=userfavorite__pb2.UserFavoriteRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CreateUserFavorite': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateUserFavorite,
                    request_deserializer=userfavorite__pb2.UserFavoriteRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'DeleteUserFavorite': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteUserFavorite,
                    request_deserializer=userfavorite__pb2.UserFavoriteRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'UserFavorite', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class UserFavorite(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUserFavoriteList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserFavorite/GetUserFavoriteList',
            userfavorite__pb2.UserFavoriteRequest.SerializeToString,
            userfavorite__pb2.UserFavoriteListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUserFavoriteDetail(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserFavorite/GetUserFavoriteDetail',
            userfavorite__pb2.UserFavoriteRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateUserFavorite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserFavorite/CreateUserFavorite',
            userfavorite__pb2.UserFavoriteRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteUserFavorite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/UserFavorite/DeleteUserFavorite',
            userfavorite__pb2.UserFavoriteRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
