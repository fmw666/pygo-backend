apt install wget
wget https://dl.google.com/go/go1.18.3.linux-amd64.tar.gz
tar zxvf go1.18.3.linux-amd64.tar.gz -C /usr/local

sed -i '$a export PATH=$PATH:/usr/local/go/bin' ~/.bashrc
sed -i '$a export GOROOT=/usr/local/go' ~/.bashrc
sed -i '$a export GOPATH=$GOROOT/gowork' ~/.bashrc
sed -i '$a export GOBIN=$GOROOT/bin' ~/.bashrc
source ~/.bashrc
