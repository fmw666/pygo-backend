# 本地开发

> 本篇基于 windows 系统

ipconfig 查找局域网适配器 ipv4 地址

docker 服务均可通过该地址访问

虚拟机也通过该地址访问到 docker 服务

---

我虚拟机中启动 python 环境，我的虚拟机 ip 为 192.168.200.129

我的 docker 和本机环境 ip 都是 192.168.200.1

服务都是启用在当前宿主机环境，服务启用 ip 应该和宿主机 ip 一致

consul 要对 虚拟机 ip 访问进行健康检查，因此 虚拟机应该关闭防火墙：`systemctl stop firewalld`


### proto 文件生成

```py
pip install grpcio
pip install grpcio-tools==1.43.0

python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I . *.proto

# change user_pb2_grpc.py
# from . import user_pb2 as user__pb2
```

```go
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

protoc --go_out=. --go-grpc_out=. ./*.proto
```

### `scripts/utils/init_config.py`

1. 读取 `config.ini` 配置文件信息：
    + 修改 nacosfiles 中的 host、mysql、redis、consul、rocketmq、jaeger、ali_sms、alipay、oss 配置信息.
1. 读取 `config.ini` 中 **Nacos** 信息：
    + 修改 services/**/config.json 中的 nacos 配置信息.
    + 修改 apis/**/config.yaml 中的 nacos 配置信息.
1. 读取 `config.ini` 中 **Jenkins** 信息：
    + 修改 jenkinscfg 下配置文件信息.
    + 修改 services/**/Jenkinsfile 中的 git、remote server 配置信息.

### `scripts/utils/init_nacos.py`

1. 删除所有 id 相同的命名空间，创建新的命名空间.
1. 向各命名空间中导入 nacosfiles 下的配置文件.

### `scripts/utils/init_mysql.py`

1. 通过 pymysql 连接 mysql，并创建数据库.
1. 通过运行 `python backend/services/xxx_srv/model/models.py` 来创建表和初始化表记录.
    1. 读取 `backend/services/xxx_srv/settings/settings.py` 中的 nacos 配置信息.
    1. 通过 nacos 配置信息获取 nacos 管理台中的数据库配置信息.（需保证 --init_nacos 已正确执行）

### `scripts/utils/init_jenkins.py`

1. 创建文件夹，若存在同名文件夹则报错退出.
1. 安装 jenkins 插件：`Localization: Chinese (Simplified)`, `SSH Credentials`, `Publish Over SSH`, `Pipeline`, `Git`.
1. 读取 jenkinscfg 下凭证配置文件信息，在文件夹下创建 jenkins 凭证.
1. 读取 jenkinscfg 下配置文件信息，在文件夹下创建 jenkins 任务.
