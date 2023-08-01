from peewee import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    """
    用户表
    """
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男"),
    )

    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员"),
    )

    mobile = CharField(max_length=11, verbose_name="手机号码", index=True, unique=True)
    password = CharField(max_length=255, verbose_name="密码")
    nick_name = CharField(max_length=255, verbose_name="昵称", null=True)
    head_url = CharField(max_length=255, verbose_name="头像", null=True)
    birthday = DateField(verbose_name="生日", null=True)
    address = CharField(max_length=255, verbose_name="地址", null=True)
    desc = TextField(verbose_name="个人描述", null=True)
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="角色")


if __name__ == "__main__":
    settings.DB.create_tables([User])
    from passlib.hash import pbkdf2_sha256
    # for i in range(10):
    #     user = User()
    #     user.nick_name = f"bob{i}"
    #     user.mobile = f"1380000000{i}"
    #     user.password = pbkdf2_sha256.hash("123456")
    #     user.save(
    # )
    for user in User.select():
        print(pbkdf2_sha256.verify("123456", user.password))
