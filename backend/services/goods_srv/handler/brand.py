from goods_srv.model.models import Brands, GoodsCategoryBrand, Category
from goods_srv.proto import brand_pb2, brand_pb2_grpc, category_pb2

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist


class BrandServicer(brand_pb2_grpc.BrandServicer):

    @logger.catch
    def BrandList(self, request: empty_pb2.Empty, context):
        """
        获取所有 brand
        """
        rsp = brand_pb2.BrandListResponse()
        brands = Brands.select()

        rsp.total = brands.count()
        for brand in brands:
            brand_rsp = brand_pb2.BrandInfoResponse()

            brand_rsp.id = brand.id
            brand_rsp.name = brand.name
            brand_rsp.logo = brand.logo

            rsp.data.append(brand_rsp)
        return rsp

    # @logger.catch
    def CreateBrand(self, request: brand_pb2.BrandRequest, context):
        """
        创建 brand
        """
        brands = Brands.select().where(Brands.name == request.name)
        if brands.count() > 0:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("brand already exists")
            return brand_pb2.BrandInfoResponse()

        brand = Brands()

        brand.name = request.name
        brand.logo = request.logo

        brand.save()

        return brand_pb2.BrandInfoResponse(
            id=brand.id,
            name=brand.name,
            logo=brand.logo,
        )

    @logger.catch
    def DeleteBrand(self, request: brand_pb2.BrandRequest, context):
        """
        删除 brand
        """
        try:
            brand = Brands.get(Brands.id == request.id)
            brand.delete_instance()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("brand not found")

        return empty_pb2.Empty()

    @logger.catch
    def UpdateBrand(self, request: brand_pb2.BrandRequest, context):
        """
        更新 brand
        """
        try:
            brand = Brands.get(Brands.id == request.id)
            if request.name:
                brand.name = request.name
            if request.logo:
                brand.logo = request.logo
            brand.save()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("brand not found")

        return empty_pb2.Empty()

    @logger.catch
    def CategoryBrandList(self, request: empty_pb2.Empty(), context):
        """
        获取所有 category_brand
        """
        rsp = brand_pb2.CategoryBrandListResponse()
        category_brands = GoodsCategoryBrand.select()

        # pagination
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = (request.pages - 1) * per_page_nums

        category_brands = category_brands.offset(start).limit(per_page_nums)
        rsp.total = category_brands.count()

        for category_brand in category_brands:
            category_brand_rsp = brand_pb2.CategoryBrandResponse()

            category_brand_rsp.id = category_brand.id

            category_brand_rsp.brand.id = category_brand.brand.id
            category_brand_rsp.brand.name = category_brand.brand.name
            category_brand_rsp.brand.logo = category_brand.brand.logo

            category_brand_rsp.category.id = category_brand.category.id
            category_brand_rsp.category.name = category_brand.category.name
            category_brand_rsp.category.parentCategory = (
                category_brand.category.parent_category_id
            )
            category_brand_rsp.category.level = category_brand.category.level
            category_brand_rsp.category.isTab = category_brand.category.is_tab

            rsp.data.append(category_brand_rsp)

        return rsp

    @logger.catch
    def GetCategoryBrandList(self, request: category_pb2.CategoryInfoRequest,
                             context):
        """
        获取分类下的所有品牌
        """
        rsp = brand_pb2.BrandListResponse()

        try:
            category = Category.get(Category.id == request.id)
            category_brands = GoodsCategoryBrand.select() \
                .where(GoodsCategoryBrand.category == category)

            rsp.total = category_brands.count()
            for category_brand in category_brands:
                brand_rsp = brand_pb2.BrandInfoResponse()

                brand_rsp.id = category_brand.brand.id
                brand_rsp.name = category_brand.brand.name
                brand_rsp.logo = category_brand.brand.logo

                rsp.data.append(brand_rsp)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("category not found")

        return rsp

    @logger.catch
    def CreateCategoryBrand(self, request: brand_pb2.CategoryBrandRequest,
                            context):
        category_brand = GoodsCategoryBrand()

        try:
            category_brand.brand = Brands.get(Brands.id == request.brandId)
            category_brand.category = Category.get(
                Category.id == request.categoryId)
            category_brand.save()

            return brand_pb2.CategoryBrandResponse(
                id=category_brand.id,
                brand=brand_pb2.BrandInfoResponse(
                    id=category_brand.brand.id,
                    name=category_brand.brand.name,
                    logo=category_brand.brand.logo,
                ),
                category=category_pb2.CategoryInfoResponse(
                    id=category_brand.category.id,
                    name=category_brand.category.name,
                    parentCategory=category_brand.category.parent_category_id,
                    level=category_brand.category.level,
                    isTab=category_brand.category.is_tab,
                ),
            )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("brand or category not found")
            return brand_pb2.CategoryBrandResponse()

    @logger.catch
    def DeleteCategoryBrand(self, request: brand_pb2.CategoryBrandRequest,
                            context):
        try:
            category_brand = GoodsCategoryBrand.get(
                GoodsCategoryBrand.id == request.id)
            category_brand.delete_instance()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("category_brand not found")

        return empty_pb2.Empty()

    @logger.catch
    def UpdateCategoryBrand(self, request: brand_pb2.CategoryBrandRequest,
                            context):
        try:
            category_brand = GoodsCategoryBrand.get(
                GoodsCategoryBrand.id == request.id)
            if request.brandId:
                category_brand.brand = Brands.get(Brands.id == request.brandId)
            if request.categoryId:
                category_brand.category = Category.get(
                    Category.id == request.categoryId)
            category_brand.save()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("category_brand not found")

        return empty_pb2.Empty()
