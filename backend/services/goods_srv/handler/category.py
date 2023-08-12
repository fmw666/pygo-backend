import json

from goods_srv.model.models import Category
from goods_srv.proto import category_pb2, category_pb2_grpc

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist


class CategoryServicer(category_pb2_grpc.CategoryServicer):

    def category_model_to_dict(self, category: Category) -> dict:
        """
        将 Category 模型转换为 dict
        :param category: Category
        :return: dict
        """
        category_dict = {
            "name": category.name,
            "id": category.id,
            "level": category.level,
            "parent": category.parent_category_id,
            "is_tab": category.is_tab,
        }
        return category_dict

    @logger.catch
    def GetAllCategorysList(
        self, request: empty_pb2.Empty, context: grpc.ServicerContext
    ) -> category_pb2.CategoryListResponse:
        """
        获取所有商品分类
        :param request: empty_pb2.Empty
        :param context: grpc.ServicerContext
        :return: CategoryListResponse
        [{
            "name": "string",
            "id": 0,
            "sub_category": [
                {
                    "name": "string",
                    "id": 0,
                    "sub_category": [
                    ]
                }
            ]
        }, {}, {}, ...]
        """
        level1, level2, level3 = [], [], []
        category_list_rsp = category_pb2.CategoryListResponse()
        category_list_rsp.total = Category.select().count()

        for category in Category.select():
            category_rsp = category_pb2.CategoryInfoResponse()

            category_rsp.id = category.id
            category_rsp.name = category.name
            if category.parent_category_id:
                category_rsp.parentCategory = category.parent_category_id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab

            category_list_rsp.data.append(category_rsp)

            if category.level == 1:
                level1.append(self.category_model_to_dict(category))
            elif category.level == 2:
                level2.append(self.category_model_to_dict(category))
            elif category.level == 3:
                level3.append(self.category_model_to_dict(category))

        for l3 in level3:
            for l2 in level2:
                if l3["parent"] == l2["id"]:
                    l2.setdefault("sub_category", []).append(l3)

        for l2 in level2:
            for l1 in level1:
                if l2["parent"] == l1["id"]:
                    l1.setdefault("sub_category", []).append(l2)

        category_list_rsp.jsonData = json.dumps(level1, ensure_ascii=False)
        return category_list_rsp

    @logger.catch
    def GetSubCategory(
        self,
        request: category_pb2.CategoryListRequest,
        context: grpc.ServicerContext
    ) -> category_pb2.SubCategoryListResponse:
        """
        获取子分类
        :param request: category_pb2.CategoryListRequest
        :param context: grpc.ServicerContext
        :return: category_pb2.SubCategoryListResponse
        """
        category_list_rsp = category_pb2.SubCategoryListResponse()

        try:
            category_info = Category.get(Category.id == request.id)

            category_list_rsp.info.id = category_info.id
            category_list_rsp.info.name = category_info.name
            category_list_rsp.info.level = category_info.level
            category_list_rsp.info.isTab = category_info.is_tab
            if category_info.parent_category:
                category_list_rsp.info.parentCategory = (
                    category_info.parent_category_id
                )
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("分类不存在")
            return category_list_rsp

        categorys = Category.select().where(
            Category.parent_category == request.id)
        category_list_rsp.total = categorys.count()
        for category in categorys:
            category_rsp = category_pb2.CategoryInfoResponse()

            category_rsp.id = category.id
            category_rsp.name = category.name
            if category_info.parent_category:
                category_rsp.parentCategory = category_info.parent_category_id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab

            category_list_rsp.subCategorys.append(category_rsp)

        return category_list_rsp

    @logger.catch
    def CreateCategory(
        self,
        request: category_pb2.CategoryInfoRequest,
        context: grpc.ServicerContext
    ) -> category_pb2.CategoryInfoResponse:
        """
        创建分类
        :param request: category_pb2.CategoryInfoRequest
        :param context: grpc.ServicerContext
        :return: category_pb2.CategoryInfoResponse
        """
        try:
            category = Category()
            category.name = request.name
            if request.level != 1:
                category.parent_category = request.parentCategory
            category.level = request.level
            category.is_tab = request.isTab
            category.save()

            category_rsp = category_pb2.CategoryInfoResponse()
            category_rsp.id = category.id
            category_rsp.name = category.name
            if category.parent_category:
                category_rsp.parentCategory = category.parent_category.id
            category_rsp.level = category.level
            category_rsp.isTab = category.is_tab
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("创建分类失败" + str(e))
            return category_pb2.CategoryInfoResponse()

        return category_rsp

    @logger.catch
    def DeleteCategory(
        self,
        request: category_pb2.DeleteCategoryRequest,
        context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        """
        删除分类
        :param request: category_pb2.DeleteCategoryRequest
        :param context: grpc.ServicerContext
        :return: empty_pb2.Empty
        """
        try:
            category = Category.get(Category.id == request.id)
            category.delete_instance()

            # TODO if delete the goods in the category
            # goods = Goods.select().where(Goods.category == request.id)
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("分类不存在")
            return empty_pb2.Empty()

    @logger.catch
    def UpdateCategory(
        self,
        request: category_pb2.CategoryInfoRequest,
        context: grpc.ServicerContext
    ) -> empty_pb2.Empty:
        """
        更新分类
        :param request: category_pb2.CategoryInfoRequest
        :param context: grpc.ServicerContext
        :return: empty_pb2.Empty
        """
        try:
            category = Category.get(Category.id == request.id)
            if request.name:
                category.name = request.name
            if request.parentCategory:
                category.parent_category = request.parentCategory
            if request.level:
                category.level = request.level
            if request.isTab:
                category.is_tab = request.isTab

            category.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("分类不存在")
            return empty_pb2.Empty()
