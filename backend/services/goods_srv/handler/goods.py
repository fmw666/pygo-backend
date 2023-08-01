from goods_srv.model.models import Goods, Category, Brands
from goods_srv.proto import goods_pb2, goods_pb2_grpc

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist


class GoodsServicer(goods_pb2_grpc.GoodsServicer):

    def convert_model_to_message(self, goods):
        info_rsp = goods_pb2.GoodsInfoResponse()
        
        info_rsp.id = goods.id
        info_rsp.categoryId = goods.category_id
        info_rsp.name = goods.name
        info_rsp.goodsSn = goods.goods_sn
        info_rsp.clickNum = goods.click_num
        info_rsp.soldNum = goods.sold_num
        info_rsp.favNum = goods.fav_num
        info_rsp.marketPrice = goods.market_price
        info_rsp.shopPrice = goods.shop_price
        info_rsp.goodsBrief = goods.goods_brief
        info_rsp.shipFree = goods.ship_free
        info_rsp.goodsFrontImage = goods.goods_front_image
        info_rsp.isNew = goods.is_new
        info_rsp.isHot = goods.is_hot
        info_rsp.descImages.extend(goods.desc_images)
        info_rsp.images.extend(goods.desc_images)

        info_rsp.category.id = goods.category.id
        info_rsp.category.name = goods.category.name

        info_rsp.brand.id = goods.brand.id
        info_rsp.brand.name = goods.brand.name
        info_rsp.brand.logo = goods.brand.logo

        return info_rsp
    
    @logger.catch
    def GoodsList(self, request: goods_pb2.GoodsFilterRequest, context):
        """
        商品列表
        """
        rsp = goods_pb2.GoodsListResponse()

        goods = Goods.select()
        if request.keyWords:
            goods = goods.filter(Goods.name.contains(request.keyWords))
        if request.isHot:
            goods = goods.filter(Goods.is_hot==True)
        if request.isNew:
            goods = goods.filter(Goods.is_new==True)
        if request.priceMin:
            goods = goods.filter(Goods.shop_price>=request.priceMin)
        if request.priceMax:
            goods = goods.filter(Goods.shop_price<=request.priceMax)
        if request.brand:
            goods = goods.filter(Goods.brand_id==request.brand)
        if request.topCategory:
            try:
                ids = []
                category = Category.get(Category.id==request.topCategory)
                level = category.level

                if level == 1:
                    c2 = Category.alias()
                    categorys = Category.select().where(Category.parent_category_id.in_(
                        c2.select(c2.id).where(c2.parent_category_id==request.topCategory)
                    ))
                    for c in categorys:
                        ids.append(c.id)
                elif level == 2:
                    categorys = Category.select().where(Category.parent_category_id==request.topCategory)
                elif level == 3:
                    ids.append(request.topCategory)

                goods = goods.where(Goods.category_id.in_(ids))
            except Exception as e:
                pass
        
        # page
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = (request.pages - 1) * per_page_nums
        
        goods = goods.limit(per_page_nums).offset(start)
        rsp.total = goods.count()
        for good in goods:
            rsp.data.append(self.convert_model_to_message(good))
        
        return rsp

    @logger.catch
    def BatchGetGoods(self, request: goods_pb2.GoodsFilterRequest, context):
        """
        批量获取商品
        """
        rsp = goods_pb2.GoodsListResponse()
        goods = Goods.select().where(Goods.id.in_(list(request.id)))

        rsp.total = goods.count()
        for good in goods:
            rsp.data.append(self.convert_model_to_message(good))

        return rsp

    @logger.catch
    def DeleteGoods(self, request: goods_pb2.DeleteGoodsInfo, context):
        """
        删除商品
        """
        try:
            good = Goods.get(Goods.id==request.id)
            good.delete_instance()
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品不存在")
            return empty_pb2.Empty()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return empty_pb2.Empty()

    @logger.catch
    def GetGoodsDetail(self, request: goods_pb2.GoodInfoRequest, context):
        """
        获取商品详情
        """
        try:
            good = Goods.get(Goods.id==request.id)
            good.click_num += 1
            good.save()
            return self.convert_model_to_message(good)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品不存在")
            return goods_pb2.GoodsInfoResponse()

    @logger.catch
    def CreateGoods(self, request: goods_pb2.GoodInfoRequest, context):
        """
        创建商品
        """
        try:
            category = Category.get(Category.id==request.categoryId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品分类不存在")
            return goods_pb2.GoodsInfoResponse()
        
        try:
            brand = Brands.get(Brands.id==request.brandId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌不存在")
            return goods_pb2.GoodsInfoResponse()
        
        goods = Goods()
        goods.category = category
        goods.brand = brand
        goods.name = request.name
        goods.goods_sn = request.goodsSn
        goods.market_price = request.marketPrice
        goods.shop_price = request.shopPrice
        goods.goods_brief = request.goodsBrief
        goods.ship_free = request.shipFree
        goods.desc_images = list(request.descImages)
        goods.goods_front_image = request.goodsFrontImage
        goods.is_new = request.isNew
        goods.is_hot = request.isHot
        goods.on_sale = request.onSale

        goods.save()

        # TODO 此处完善库存的设置 - 分布式事务

        return self.convert_model_to_message(goods)
    
    @logger.catch
    def UpdateGoods(self, request: goods_pb2.GoodInfoRequest, context):
        """
        更新商品
        """
        try:
            category = Category.get(Category.id==request.categoryId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品分类不存在")
            return goods_pb2.GoodsInfoResponse()
        
        try:
            brand = Brands.get(Brands.id==request.brandId)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌不存在")
            return goods_pb2.GoodsInfoResponse()
        
        try:
            goods = Goods.get(Goods.id==request.id)
            goods.category = category
            goods.brand = brand
            goods.name = request.name
            goods.goods_sn = request.goodsSn
            goods.market_price = request.marketPrice
            goods.shop_price = request.shopPrice
            goods.goods_brief = request.goodsBrief
            goods.ship_free = request.shipFree
            goods.desc_images = list(request.descImages)
            goods.goods_front_image = request.goodsFrontImage
            goods.is_new = request.isNew
            goods.is_hot = request.isHot
            goods.on_sale = request.onSale

            goods.save()

            # TODO 此处完善库存的设置 - 分布式事务
            return self.convert_model_to_message(goods)
        except DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品不存在")
            return goods_pb2.GoodsInfoResponse()
