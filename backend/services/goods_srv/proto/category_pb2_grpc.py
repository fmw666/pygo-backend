# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import category_pb2 as category__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class CategoryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllCategorysList = channel.unary_unary(
                '/Category/GetAllCategorysList',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=category__pb2.CategoryListResponse.FromString,
                )
        self.GetSubCategory = channel.unary_unary(
                '/Category/GetSubCategory',
                request_serializer=category__pb2.CategoryListRequest.SerializeToString,
                response_deserializer=category__pb2.SubCategoryListResponse.FromString,
                )
        self.CreateCategory = channel.unary_unary(
                '/Category/CreateCategory',
                request_serializer=category__pb2.CategoryInfoRequest.SerializeToString,
                response_deserializer=category__pb2.CategoryInfoResponse.FromString,
                )
        self.DeleteCategory = channel.unary_unary(
                '/Category/DeleteCategory',
                request_serializer=category__pb2.DeleteCategoryRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.UpdateCategory = channel.unary_unary(
                '/Category/UpdateCategory',
                request_serializer=category__pb2.CategoryInfoRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class CategoryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllCategorysList(self, request, context):
        """商品分类接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSubCategory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCategory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteCategory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCategory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CategoryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllCategorysList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllCategorysList,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=category__pb2.CategoryListResponse.SerializeToString,
            ),
            'GetSubCategory': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSubCategory,
                    request_deserializer=category__pb2.CategoryListRequest.FromString,
                    response_serializer=category__pb2.SubCategoryListResponse.SerializeToString,
            ),
            'CreateCategory': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCategory,
                    request_deserializer=category__pb2.CategoryInfoRequest.FromString,
                    response_serializer=category__pb2.CategoryInfoResponse.SerializeToString,
            ),
            'DeleteCategory': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteCategory,
                    request_deserializer=category__pb2.DeleteCategoryRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'UpdateCategory': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateCategory,
                    request_deserializer=category__pb2.CategoryInfoRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Category', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Category(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllCategorysList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Category/GetAllCategorysList',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            category__pb2.CategoryListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSubCategory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Category/GetSubCategory',
            category__pb2.CategoryListRequest.SerializeToString,
            category__pb2.SubCategoryListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateCategory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Category/CreateCategory',
            category__pb2.CategoryInfoRequest.SerializeToString,
            category__pb2.CategoryInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteCategory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Category/DeleteCategory',
            category__pb2.DeleteCategoryRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateCategory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Category/UpdateCategory',
            category__pb2.CategoryInfoRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
