from peewee import (Model, CharField, DateField, TextField, IntegerField)

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

    mobile = CharField(max_length=11, index=True, unique=True,
                       verbose_name="手机号码")
    password = CharField(max_length=255, verbose_name="密码")
    nick_name = CharField(max_length=255, verbose_name="昵称", null=True)
    head_url = CharField(max_length=255, verbose_name="头像", null=True)
    birthday = DateField(verbose_name="生日", null=True)
    address = CharField(max_length=255, verbose_name="地址", null=True)
    desc = TextField(verbose_name="个人描述", null=True)
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True,
                       verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="角色")


def init() -> None:
    settings.DB.create_tables([User])

    from passlib.hash import pbkdf2_sha256
    for i in range(10):
        # select by mobile, if not exists, create
        user, created = User.get_or_create(mobile=f"1380000000{i}")
        if created:
            user.nick_name = f"bob{i}"
            user.password = pbkdf2_sha256.hash("123456")
            user.save()


if __name__ == "__main__":
    init()
