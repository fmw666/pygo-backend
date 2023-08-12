from datetime import datetime

from peewee import (Model, DateTimeField, BooleanField, IntegerField,
                    CharField, DecimalField)

from order_srv.settings import settings


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

    def delete_instance(self, permanently: bool = False, recursive: bool = ...,
                        delete_nullable: bool = ...):
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


class ShoppingCart(BaseModel):
    """
    购物车
    """
    user = IntegerField(verbose_name="用户id")
    goods = IntegerField(verbose_name="商品id")
    nums = IntegerField(default=0, verbose_name="购买数量")
    checked = BooleanField(default=True, verbose_name="是否选中")


class OrderInfo(BaseModel):
    """
    订单表
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "支付成功"),
        ("TRADE_CLOSED", "支付关闭"),
        ("WAIT_BUYER_PAY", "等待支付"),
        ("TRADE_FINISHED", "交易结束"),
        ("PAYING", "待支付"),
    )
    PAY_TYPE = (
        ("ALIPAY", "支付宝"),
        ("WEIXIN", "微信"),
    )

    user = IntegerField(verbose_name="用户id")
    order_sn = CharField(max_length=30, null=True, unique=True,
                         verbose_name="订单号")
    pay_type = CharField(choices=PAY_TYPE, default="ALIPAY", max_length=10,
                         verbose_name="支付类型")
    status = CharField(choices=ORDER_STATUS, default="PAYING", max_length=30,
                       verbose_name="订单状态")
    trade_no = CharField(max_length=100, null=True, unique=True,
                         verbose_name="交易号")
    order_mount = DecimalField(max_digits=10, decimal_places=2,
                               verbose_name="订单金额")
    pay_time = DateTimeField(null=True, verbose_name="支付时间")

    address = CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = CharField(max_length=20, default="", verbose_name="签收人")
    signer_mobile = CharField(max_length=11, verbose_name="联系电话")
    leave_message = CharField(max_length=200, default="", verbose_name="留言")


class OrderGoods(BaseModel):
    """
    订单商品表
    """
    order = IntegerField(verbose_name="订单id")
    goods = IntegerField(verbose_name="商品id")
    goods_name = CharField(max_length=100, verbose_name="商品名称")
    goods_image = CharField(max_length=200, verbose_name="商品图片")
    goods_price = DecimalField(max_digits=10, decimal_places=2,
                               verbose_name="商品价格")
    nums = IntegerField(default=0, verbose_name="购买数量")


def init() -> None:
    settings.DB.create_tables([ShoppingCart, OrderInfo, OrderGoods])


if __name__ == "__main__":
    init()
