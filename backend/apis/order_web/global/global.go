package global

import (
	"apis/order_web/config"
	"apis/order_web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	Debug        string               = "PYGO_DEBUG"
	ServerConfig *config.ServerConfig = &config.ServerConfig{}
	NacosConfig  *config.NacosConfig  = &config.NacosConfig{}
	Trans        ut.Translator

	GoodsSrvClient     proto.GoodsClient
	OrderSrvClient     proto.OrderClient
	InventorySrvClient proto.InventoryClient
)
