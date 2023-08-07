import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime

from peewee import *
from playhouse.mysql_ext import JSONField

from goods_srv.settings import settings


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")

    def save(self, *args, **kwargs):
        if self._pk is not None:
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)
    
    @classmethod
    def delete(cls, permanently: bool = False):
        """
        permanently: True: 真实删除; False: 逻辑删除
        """
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently: bool = False, recursive: bool = ..., delete_nullable: bool = ...):
        """
        permanently: True: 真实删除; False: 逻辑删除
        """
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            return self.save()
    
    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)

    class Meta:
        database = settings.DB


class Category(BaseModel):
    name = CharField(max_length=30, verbose_name="类别名称")
    parent_category = ForeignKeyField("self", null=True, verbose_name="父类别")
    level = IntegerField(default=1, verbose_name="类别级别")
    is_tab = BooleanField(default=False, verbose_name="是否导航")

    class Meta:
        table_name = "category"
        verbose_name = "类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Brands(BaseModel):
    """
    品牌表
    """
    name = CharField(max_length=30, index=True, unique=True, verbose_name="品牌名称")
    logo = CharField(max_length=200, null=True, default="", verbose_name="品牌logo")


class Goods(BaseModel):
    """
    商品表
    """
    category = ForeignKeyField(Category, on_delete="CASCADE", verbose_name="类别")
    brand = ForeignKeyField(Brands, on_delete="CASCADE", verbose_name="品牌")
    on_sale = BooleanField(default=True, verbose_name="是否上架")
    goods_sn = CharField(max_length=50, index=True, unique=True, verbose_name="商品唯一货号")
    name = CharField(max_length=100, verbose_name="商品名称")
    click_num = IntegerField(default=0, verbose_name="点击数")
    sold_num = IntegerField(default=0, verbose_name="商品销售量")
    fav_num = IntegerField(default=0, verbose_name="收藏数")
    market_price = FloatField(default=0, verbose_name="市场价格")
    shop_price = FloatField(default=0, verbose_name="本店价格")
    goods_brief = TextField(verbose_name="商品简短描述")
    ship_free = BooleanField(default=True, verbose_name="是否承担运费")
    desc_images = JSONField(verbose_name="商品描述图片")
    goods_front_image = CharField(max_length=200, null=True, default="", verbose_name="封面图")
    is_new = BooleanField(default=False, verbose_name="是否新品")
    is_hot = BooleanField(default=False, verbose_name="是否热销")


class GoodsCategoryBrand(BaseModel):
    """
    商品类别品牌
    """
    id = AutoField(primary_key=True, verbose_name="ID")
    category = ForeignKeyField(Category, verbose_name="类别")
    brand = ForeignKeyField(Brands, verbose_name="品牌")

    class Meta:
        indexes = (
            (("category", "brand"), True),
        )


class Banner(BaseModel):
    """
    轮播图
    """
    image = CharField(max_length=200, default="", verbose_name="轮播图")
    url = CharField(max_length=200, default="", verbose_name="访问地址")
    index = IntegerField(default=0, verbose_name="轮播图顺序")


if __name__ == "__main__":
    settings.DB.create_tables([Category, Brands, Goods, GoodsCategoryBrand, Banner])
    
    # list all sql files and execute
    sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
    for filename in os.listdir(sql_path):
        if not filename.endswith(".sql"):
            continue
        with open(os.path.join(sql_path, filename), "r", encoding="utf-8") as f:
            sql_statements = f.read().split(";")    
            for sql in sql_statements:
                if sql.strip():
                    settings.DB.execute_sql(sql)
        