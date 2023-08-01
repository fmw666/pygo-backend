# 快速启动

> 本篇基于 windows 系统

## 1. 安装

### 1.1. 安装 docker

### 1.2. 安装 docker-compose

### 1.3. 安装 git

### 1.4. 安装 python

### 1.5. 下载虚拟机，并安装 centos7

## 2. 初始化

### 2.1. 启动 docker

### 2.2. 编辑 docker 配置文件

```bash
```

### 2.3. 运行脚本

```bash
docker-compose up -d
```

### 2.4. 初始化 nacos 配置

```bash
cd scripts
python main.py --init_nacos
```

## 自动化部署

jenkins 中安装插件：pipeline、SSH Credentials Plugin、git、Publish Over SSH

添加 git 凭证，命名为 

### 部署 backend/apis

### 部署 backend/services

