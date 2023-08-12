from datetime import datetime

from userop_srv.settings import settings

from peewee import (Model, DateTimeField, BooleanField, IntegerField,
                    CharField, TextField, CompositeKey)


class BaseModel(Model):
    """基础模型"""

    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")

    def save(self, *args, **kwargs):
        if self._pk is not None:
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently: bool = False) -> int:
        """
        :param permanently: True: 真实删除; False: 逻辑删除
        :return: 执行操作的行数
        """
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently: bool = False,
                        recursive: bool = ..., delete_nullable: bool = ...):
        """
        :param permanently: True: 真实删除; False: 逻辑删除
        :param recursive:
        :param delete_nullable:
        :return: 执行操作的行数
        """
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            return self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(is_deleted=False)

    class Meta:
        database = settings.DB


class LeaveMessage(BaseModel):
    """
    用户留言表
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购"),
        (6, "其他"),
    )
    user = IntegerField(verbose_name="用户ID")
    message_type = IntegerField(choices=MESSAGE_CHOICES, default=1,
                                verbose_name="留言类型",
                                help_text=(u"留言类型：1(留言),2(投诉),"
                                           u"3(询问),4(售后),5(求购),6(其他)"))
    subject = CharField(max_length=100, default="", verbose_name="主题")
    message = TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = CharField(max_length=200, default="", verbose_name="上传的文件",
                     help_text="上传的文件")


class Address(BaseModel):
    """
    用户收货地址
    """
    user = IntegerField(verbose_name="用户ID")
    province = CharField(max_length=100, default="", verbose_name="省份")
    city = CharField(max_length=100, default="", verbose_name="城市")
    district = CharField(max_length=100, default="", verbose_name="区域")
    address = CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = CharField(max_length=100, default="", verbose_name="签收人")
    signer_mobile = CharField(max_length=11, default="", verbose_name="电话")


class UserFavorite(BaseModel):
    """
    用户收藏表
    """
    user = IntegerField(verbose_name="用户ID")
    goods = IntegerField(verbose_name="商品ID")

    class Meta:
        primary_key = CompositeKey("user", "goods")


def init() -> None:
    settings.DB.create_tables([LeaveMessage, Address, UserFavorite])


if __name__ == "__main__":
    init()
