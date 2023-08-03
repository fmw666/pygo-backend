

## 项目启动

参考：[quickstart.md](quickstart.md)

## 开发手册

参考：[develop.md](develop.md)

## 项目介绍


### 项目结构

```text

├── README.md
├── api
│   ├── goods
│   │   ├── goods.pb.go
│   │   ├── goods.proto
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

+ 前端服务（暂无）
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
    - [x] jenkins 服务：9080

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

