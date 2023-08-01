package global

import (
	"apis/user_web/config"
	"apis/user_web/proto"

	ut "github.com/go-playground/universal-translator"
)

var (
	Debug        string               = "PYGO_DEBUG"
	ServerConfig *config.ServerConfig = &config.ServerConfig{}
	NacosConfig  *config.NacosConfig  = &config.NacosConfig{}
	Trans        ut.Translator

	UserSrvClient proto.UserClient
)
