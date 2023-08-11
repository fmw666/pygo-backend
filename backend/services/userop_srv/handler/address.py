import grpc
from loguru import logger
from peewee import DoesNotExist
from google.protobuf import empty_pb2

from userop_srv.model.models import Address
from userop_srv.proto import address_pb2, address_pb2_grpc


class AddressServicer(address_pb2_grpc.AddressServicer):
    @logger.catch
    def GetAddressList(self, request: address_pb2.AddressRequest, context):
        rsp = address_pb2.AddressListResponse()
        addresses = Address.select()

        if request.userId:
            addresses = addresses.where(Address.user == request.userId)

        rsp.total = addresses.count()
        for addr in addresses:
            rsp.data.append(address_pb2.AddressResponse(
                id=addr.id,
                userId=addr.user,
                province=addr.province,
                city=addr.city,
                district=addr.district,
                address=addr.address,
                signerName=addr.signer_name,
                signerMobile=addr.signer_mobile,
            ))

        return rsp

    @logger.catch
    def CreateAddress(self, request: address_pb2.AddressRequest, context):
        address = Address(
            user=request.userId,
            province=request.province,
            city=request.city,
            district=request.district,
            address=request.address,
            signer_name=request.signerName,
            signer_mobile=request.signerMobile
        )
        address.save()

        return address_pb2.AddressResponse(
            id=address.id,
            userId=address.user,
            province=address.province,
            city=address.city,
            district=address.district,
            address=address.address,
            signerName=address.signer_name,
            signerMobile=address.signer_mobile
        )

    @logger.catch
    def UpdateAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(Address.id == request.id)
            if request.province:
                address.province = request.province
            if request.city:
                address.city = request.city
            if request.district:
                address.district = request.district
            if request.address:
                address.address = request.address
            if request.signerName:
                address.signer_name = request.signerName
            if request.signerMobile:
                address.signer_mobile = request.signerMobile
            address.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Address with id %s not found!" % request.id)
            return empty_pb2.Empty()

    @logger.catch
    def DeleteAddress(self, request: address_pb2.AddressRequest, context):
        try:
            address = Address.get(Address.id == request.id)
            address.delete_instance()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Address with id %s not found!" % request.id)
            return empty_pb2.Empty()
