from datetime import datetime

from peewee import (Model, DateTimeField, BooleanField, IntegerField,
                    CharField)

from inventory_srv.settings import settings


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
        :return: 执行受影响的行数
        """
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(self, permanently: bool = False, recursive: bool = ...,
                        delete_nullable: bool = ...):
        """
        :param permanently: True: 真实删除; False: 逻辑删除
        :param recursive: 是否递归删除
        :param delete_nullable: 是否删除可空字段
        :return: 执行受影响的行数
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


class Inventory(BaseModel):
    """
    库存表
    """
    goods = IntegerField(unique=True, verbose_name="商品ID")
    stocks = IntegerField(default=0, verbose_name="库存数量")
    # 分布式锁 -- 乐观锁
    version = IntegerField(default=0, verbose_name="版本号")

    def __str__(self):
        return f"{self.goods}: {self.stocks}"


class InventoryHistory(BaseModel):
    """
    库存变更历史表
    """
    order_sn = CharField(max_length=64, unique=True, verbose_name="订单号")
    order_inv_detail = CharField(max_length=200, verbose_name="订单库存详情")
    status = IntegerField(choices=((1, "已扣减"), (2, "已归还")), default=1,
                          verbose_name="状态")


def init() -> None:
    """初始化表和数据"""
    settings.DB.create_tables([Inventory, InventoryHistory])

    # 设置初始化值
    for i in range(421, 848):
        inv = Inventory.select().where(Inventory.goods == i).first()
        if inv:
            inv.stocks = 100
            inv.save()
        else:
            inv = Inventory(goods=i, stocks=100)
            inv.save(force_insert=True)


if __name__ == "__main__":
    init()
