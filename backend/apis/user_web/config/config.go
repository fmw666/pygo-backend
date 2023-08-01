package config

type UserSrvConfig struct {
	Host string `mapstructure:"host" json:"host" yaml:"host"`
	Port int    `mapstructure:"port" json:"port" yaml:"port"`
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type JWTConfig struct {
	SigningKey string `mapstructure:"key" json:"key" yaml:"key"`
}

type AliSmsConfig struct {
	ApiKey     string `mapstructure:"key" json:"key" yaml:"key"`
	ApiSecrect string `mapstructure:"secrect" json:"secrect" yaml:"secrect"`
}

type RedisConfig struct {
	Host   string `mapstructure:"host" json:"host" yaml:"host"`
	Port   int    `mapstructure:"port" json:"port" yaml:"port"`
	Expire int    `mapstructure:"expire" json:"expire" yaml:"expire"`
}

type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host" yaml:"host"`
	Port int    `mapstructure:"port" json:"port" yaml:"port"`
}

type ServerConfig struct {
	Name        string        `mapstructure:"name" json:"name" yaml:"name"`
	Host        string        `mapstructure:"host" json:"host" yaml:"host"`
	Port        int           `mapstructure:"port" json:"port" yaml:"port"`
	Tags        []string      `mapstructure:"tags" json:"tags" yaml:"tags"`
	Debug       string        `mapstructure:"debug" json:"debug" yaml:"debug"`
	UserSrvInfo UserSrvConfig `mapstructure:"user_srv" json:"user_srv" yaml:"user_srv"`
	JWTInfo     JWTConfig     `mapstructure:"jwt" json:"jwt" yaml:"jwt"`
	AliSmsInfo  AliSmsConfig  `mapstructure:"ali_sms" json:"ali_sms" yaml:"ali_sms"`
	RedisInfo   RedisConfig   `mapstructure:"redis" json:"redis" yaml:"redis"`
	ConsulInfo  ConsulConfig  `mapstructure:"consul" json:"consul" yaml:"consul"`
}

type NacosConfig struct {
	Host      string `mapstructure:"host" json:"host" yaml:"host"`
	Port      uint64 `mapstructure:"port" json:"port" yaml:"port"`
	Namespace string `mapstructure:"namespace" json:"namespace" yaml:"namespace"`
	User      string `mapstructure:"user" json:"user" yaml:"user"`
	Password  string `mapstructure:"password" json:"password" yaml:"password"`
	DataId    string `mapstructure:"data_id" json:"data_id" yaml:"data_id"`
	Group     string `mapstructure:"group" json:"group" yaml:"group"`
}
