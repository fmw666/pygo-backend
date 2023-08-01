package global

import (
	"apis/goods_web/config"
	"apis/goods_web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	Debug        string               = "PYGO_DEBUG"
	ServerConfig *config.ServerConfig = &config.ServerConfig{}
	NacosConfig  *config.NacosConfig  = &config.NacosConfig{}
	Trans        ut.Translator

	GoodsSrvClient    proto.GoodsClient
	CategorySrvClient proto.CategoryClient
	BannerSrvClient   proto.BannerClient
	BrandSrvClient    proto.BrandClient
)
