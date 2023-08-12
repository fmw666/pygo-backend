import grpc
from loguru import logger

from userop_srv.model.models import LeaveMessage
from userop_srv.proto import message_pb2, message_pb2_grpc


class MessageServicer(message_pb2_grpc.MessageServicer):

    @logger.catch
    def MessageList(
        self,
        request: message_pb2.MessageRequest,
        context: grpc.ServicerContext
    ) -> message_pb2.MessageListResponse:
        """
        获取留言列表
        :param request: MessageRequest
        :param context: grpc.ServicerContext
        :return: MessageListResponse
        """
        rsp = message_pb2.MessageListResponse()
        messages = LeaveMessage.select()
        if request.userId:
            messages = messages.where(LeaveMessage.user == request.userId)

        rsp.total = messages.count()
        for msg in messages:
            msg_rsp = message_pb2.MessageResponse()

            msg_rsp.id = msg.id
            msg_rsp.userId = msg.user
            msg_rsp.messageType = msg.message_type
            msg_rsp.subject = msg.subject
            msg_rsp.message = msg.message
            msg_rsp.file = msg.file

            rsp.data.append(msg_rsp)

        return rsp

    @logger.catch
    def CreateMessage(
        self,
        request: message_pb2.MessageRequest,
        context: grpc.ServicerContext
    ) -> message_pb2.MessageResponse:
        """
        创建留言
        :param request: MessageRequest
        :param context: grpc.ServicerContext
        :return: MessageResponse
        """
        message = LeaveMessage(
            user=request.userId,
            message_type=request.messageType,
            subject=request.subject,
            message=request.message,
            file=request.file
        )
        message.save()

        return message_pb2.MessageResponse(
            id=message.id,
            messageType=message.message_type,
            subject=message.subject,
            message=message.message,
            file=message.file
        )
