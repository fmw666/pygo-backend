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
