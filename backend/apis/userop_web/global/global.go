package global

import (
	"apis/userop_web/config"
	"apis/userop_web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	Debug        string               = "PYGO_DEBUG"
	ServerConfig *config.ServerConfig = &config.ServerConfig{}
	NacosConfig  *config.NacosConfig  = &config.NacosConfig{}
	Trans        ut.Translator

	GoodsSrvClient     proto.GoodsClient
	MessageClient      proto.MessageClient
	AddressClient      proto.AddressClient
	UserFavoriteClient proto.UserFavoriteClient
)
