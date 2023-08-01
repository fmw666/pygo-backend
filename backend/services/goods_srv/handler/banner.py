from goods_srv.model.models import Banner
from goods_srv.proto import banner_pb2, banner_pb2_grpc

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist


class BannerServicer(banner_pb2_grpc.BannerServicer):

    @logger.catch
    def BannerList(self, request: empty_pb2.Empty, context):
        """
        获取所有 banner
        """
        rsp = banner_pb2.BannerListResponse()
        banners = Banner.select()

        rsp.total = banners.count()
        for banner in banners:
            banner_rsp = banner_pb2.BannerResponse()

            banner_rsp.id = banner.id
            banner_rsp.image = banner.image
            banner_rsp.index = banner.index
            banner_rsp.url = banner.url
            
            rsp.data.append(banner_rsp)
        
        return rsp
    
    @logger.catch
    def CreateBanner(self, request: banner_pb2.BannerRequest, context):
        """
        创建 banner
        """
        banner = Banner()

        banner.image = request.image
        banner.index = request.index
        banner.url = request.url

        banner.save()

        return banner_pb2.BannerResponse(
            id=banner.id,
            image=banner.image,
            index=banner.index,
            url=banner.url,
        )
    
    @logger.catch
    def DeleteBanner(self, request: banner_pb2.BannerRequest, context):
        """
        删除 banner
        """
        try:
            banner = Banner.get(Banner.id == request.id)
            banner.delete_instance()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("banner not found")
            
        return empty_pb2.Empty()

    @logger.catch
    def UpdateBanner(self, request: banner_pb2.BannerRequest, context):
        """
        更新 banner
        """
        try:
            banner = Banner.get(Banner.id == request.id)
            if request.image:
                banner.image = request.image
            if request.index:
                banner.index = request.index
            if request.url:
                banner.url = request.url
            banner.save()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("banner not found")

        return empty_pb2.Empty()
