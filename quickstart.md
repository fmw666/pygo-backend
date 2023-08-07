# 快速启动

> 本篇基于 windows 系统，本篇中出现的 `127.0.0.1` 替换为本机 docker ip 地址即可.

## 1. 前期准备

- [x] 安装 git
    + 提交代码到 git 仓库，用于 jenkins 自动化部署
- [x] 安装 docker、docker-compose
    + 基于 docker 部署 mysql、redis、consul、nacos、jaeger、rabbitmq、kong、jenkins
    + jenkins 容器用于构建 backend 中后端服务
- [x] 安装 python3.8+
    + 用于本地初始化（nacos）配置
    + 用于本地测试服务器连接
- [x] 下载虚拟机，并安装 centos7
    + 用于部署运行 backend 中后端服务

## 2. Docker 部署

- [x] 编辑 `.env` 文件，设置环境变量
- [x] 如果需要）编辑 `docker-compose.yml` 文件，设置容器配置
- [x] 运行脚本 `docker-compose up -d`

## 3. 本地初始化

***注：***

+ 为方便本地测试运行，该项目中各服务均使用 **同一数据库**.
+ 如果要配置多个数据库：
    1. 请勿运行 `scripts/main.py --init_mysql` 脚本
    1. 在 nacos 管理台中修改各服务 `xxx-srv.json` 配置的 mysql 信息.
+ 如果不用配置多个数据库，可以运行 `scripts/main.py --init` 直接初始化所有配置.
+ 分别执行命令时，需要 **严格按照以下顺序运行**.

- [x] 修改 `scripts/config.ini` 配置文件
- [x] 测试连接：`python scripts/main.py --test_connect`（未初始化 jenkins 管理台会失败）
- [x] 初始化 config 配置：`python scripts/main.py --init_config`
- [x] 初始化 nacos 配置：`python scripts/main.py --init_nacos`
- [x] 初始化 mysql 数据库：`python scripts/main.py --init_mysql`
- [x] 进入 jenkins web 管理台，初始化 jenkins.
- [x] 进入 jenkins web 管理台，创建用户：`root/123456`（同 config.ini 中用户信息），并生成 token 记录在 config.ini 中.
- [x] 进入 jenkins 管理台，添加 SSH Sever：<http://127.0.0.1:9080/manage/configure>
- [x] 初始化 jenkins 配置：`python scripts/main.py --init_jenkins`

## 4. 配置服务器

+ *构建服务器（Jenkins）将 go 语言项目在本地编译成二进制文件，再传输到部署服务器（CentOS7）*
+ *构建服务器（Jenkins）将 python 语言项目直接源文件打包传输到部署服务器（CentOS7）*
+ *因此，**部署服务器（CentOS7）只需要配置好 python 项目运行环境.***

### 4.1. 配置 *构建* 服务器

- [x] 进入 jenkins 容器：`docker exec -it jenkins bash`
- [x] 在容器中运行 `scripts/jenkins_init.sh` 脚本，安装 go 语言环境.

### 4.2. 配置 *部署* 服务器

- [x] 启用虚拟机中 centos7 系统（[虚拟机中安装 centos7 - csdn](https://blog.csdn.net/hjp2020/article/details/106156642)）
- [x] 在虚拟机中运行 `scripts/centos7_init.sh` 脚本，初始化服务器环境.

## 5. 本地测试

> 注：地址、端口、账号密码，均在 `.env` 文件中由用户自定义配置，此处仅为默认.

- [x] mysql：本地连接检查数据库是否初始化成功
- [x] nacos：浏览器访问 `http://127.0.0.1:8848/nacos`
- [x] consul：浏览器访问 `http://127.0.0.1:8500`
- [x] rabbitmq：浏览器访问 `http://127.0.0.1:15672`，账号密码：`guest/guest`
- [x] jaeger：浏览器访问 `http://127.0.0.1:16686`
- [x] konga：浏览器访问 `http://127.0.0.1:1337`
- [x] jenkins：浏览器访问 `http://127.0.0.1:9080`，账号密码：`root/123456`

## 6. 自动化部署

- [x] 进入 jenkins web 管理台：`http://127.0.0.1:9080/job/pygo_backend/`
- [x] 安装插件：pipeline、SSH Credentials Plugin、git、Publish Over SSH
- [x] 将 `backend/apis` 提交到 git 仓库
- [x] 将 `backend/services` 提交到 git 仓库
- [x] 在 jenkins 管理台中构建任务.
- [x] 在 consul 管理台中查看服务是否注册成功.
