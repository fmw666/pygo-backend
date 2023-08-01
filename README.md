## 项目介绍


### 项目结构

```text

├── README.md
├── api
│   ├── goods
│   │   ├── goods.pb.go
│   │   ├── goods.proto
```

## 项目启动

### docker 启动

```bash
docker-compose up -d
```

编辑 scripts/config.ini 文件

运行 scripts/main.py --init_nacos 文件，初始化 nacos 配置

#### 数据库初始化

执行 sql 文件夹下的 sql 文件

### 非 docker 启动

services 层必须基于 Linux 或 Mac 环境

#### centos 中创建 python 开发环境

[虚拟机中安装 centos7 - csdn](https://blog.csdn.net/hjp2020/article/details/106156642)

```bash
# 安装 wget 工具
yum install wget

# 安装 librocketmq
wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.2.0/rocketmq-client-cpp-2.2.0-centos7.x86_64.rpm
sudo rpm -ivh rocketmq-client-cpp-2.2.0-centos7.x86_64.rpm

# 安装系统依赖
sudo yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-c++ libffi-devel python-devel python-devel mariadb-devel

# 安装 python3.8
wget https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tgz
tar -zxvf Python-3.8.6.tgz -C /tmp
cd /tmp/Python-3.8.6
./configure --prefix=/usr/local/
make && make altinstall

# 更改 python3.8 软链接
ln -s /usr/local/bin/python3.8 /usr/bin/python3
ln -s /usr/local/bin/pip3.8 /usr/bin/pip3

# 安装 virtualenvwrapper
sudo yum install python-setuptools python-devel
pip3 install virtualenvwrapper

# 编辑 .bashrc 文件
sudo yum install vim
vim ~/.bashrc
# (添加如下内容)
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
# (退出后执行)
source ~/.bashrc

# 创建虚拟环境
mkvirtualenv -p python3 pygo_srv

# 进入虚拟环境
workon pygo_srv

# 安装 python 依赖
pip install rocketmq-client-python

ln -s /usr/local/lib/librocketmq.so /usr/lib
sudo ldconfig

# 配置防火墙
firewall-cmd --zone=public --add-port=10911/tcp --permanent
firewall-cmd --zone=public --add-port=10912/tcp --permanent
sudo firewall-cmd --reload
```

## 开发手册

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

### 服务注册与发现

consul

### 配置文件中心

nacos

### 服务端口

+ Service 层服务
    - [x] user 服务：端口号随机
    - [x] goods 服务：端口号随机
    - [x] inventory 服务：端口号随机
    - [x] order 服务：端口号随机

+ Web 层服务
    - [x] user 服务：8021
    - [x] goods 服务：8022
    - [x] order 服务：8023
    - [x] userop 服务：8024
    - [x] oss 服务：8029
    - [x] 支付宝 服务：8023（集成在 order 服务中）

+ 前端服务
    - [x] vue 服务：8089

+ 工具服务
    - [x] nacos 服务：8848
    - [x] consul 服务：8500
    - [x] mysql 服务：3306
    - [x] redis 服务：6379
    - [x] jaeger 服务：6831、16686
    - [x] rocketmq console 服务：8080
    - [x] rocketmq namesrv 服务：9876
    - [x] rocketmq broker 服务：10909、10911
    - [x] postgres 服务 (by kong)：5432
    - [x] kong 服务：8000、8001、8443
    - [x] konga 服务：1337

### 文件服务器

aliyun oss

### 内网穿透 工具

Q：什么叫内网穿透？
A：内网穿透是一种将局域网或者数据中心内部服务映射到公网上的技术。

Q：实现原理？
A：


- [x] （选用）NATAPP <https://natapp.cn/>

    + 优点：有免费版
    + 缺点：每次本地启动域名会变，需要在 nacos 中每次修改 oss-web.json 的 callback_url

- [ ] 飞鸽 <https://www.fgnwct.com/>

    + 优点：有免费版
    + 缺点：免费隧道需强制访问验证，一些外网服务不方便做回调

### 支付链接

alipay <https://openhome.alipay.com/develop/sandbox/app>

### MySQL 数据库

用户名：root
密码：123456

### Redis 数据库

端口：6379

### RocketMQ

### 链路追踪

#### gin 中使用

1. 添加中间件 tracing.go

2. 添加 utils\otgrpc\*

3. 在 router 中添加中间件

```go
```

4. 在 grpc 拨号中添加链路追踪

```go
import "xx/xx/utils/otgrpc"

xxConn, err := grpc.Dial(
    fmt.Sprintf("consul://%s:%d/%s?wait=14s", consulInfo.Host, consulInfo.Port, global.ServerConfig.GoodsSrvInfo.Name),
    grpc.WithTransportCredentials(insecure.NewCredentials()),
    grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
    grpc.WithUnaryInterceptor(otgrpc.OpenTracingClientInterceptor(opentracing.GlobalTracer())),
)
```

5. 在 handle 中添加 ctx

```go
global.GoodsSrvClient.GoodsList(context.WithValue(context.Background(), "ginContext", c), request)
```

