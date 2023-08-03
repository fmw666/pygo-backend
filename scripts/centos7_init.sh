# 安装 wget 工具
sudo yum install wget

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

# 编辑 ~/.bashrc 文件
sudo yum install vim
sed -i '$a VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3' ~/.bashrc
sed -i '$a export WORKON_HOME=$HOME/.virtualenvs' ~/.bashrc
sed -i '$a source /usr/local/bin/virtualenvwrapper.sh' ~/.bashrc
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

# 关闭防火墙
systemctl stop firewalld.service
systemctl disable firewalld.service

# 创建代码目录
mkdir -p /docker/python
chmod -R 777 /docker/python
mkdir -p /docker/golang
chmod -R 777 /docker/golang
