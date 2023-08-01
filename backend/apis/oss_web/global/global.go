package global

import (
	"apis/oss_web/config"

	ut "github.com/go-playground/universal-translator"
)

var (
	Debug string = "PYGO_DEBUG"
	Trans ut.Translator

	ServerConfig *config.ServerConfig = &config.ServerConfig{}

	NacosConfig *config.NacosConfig = &config.NacosConfig{}
)
