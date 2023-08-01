package config

type GoodsSrvConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type UserOpSrvConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type JWTConfig struct {
	SigningKey string `mapstructure:"key" json:"key" yaml:"key"`
}

type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host" yaml:"host"`
	Port int    `mapstructure:"port" json:"port" yaml:"port"`
}

type ServerConfig struct {
	Name          string          `mapstructure:"name" json:"name" yaml:"name"`
	Host          string          `mapstructure:"host" json:"host" yaml:"host"`
	Port          int             `mapstructure:"port" json:"port" yaml:"port"`
	Tags          []string        `mapstructure:"tags" json:"tags" yaml:"tags"`
	Debug         string          `mapstructure:"debug" json:"debug" yaml:"debug"`
	GoodsSrvInfo  GoodsSrvConfig  `mapstructure:"goods_srv" json:"goods_srv" yaml:"goods_srv"`
	UserOpSrvInfo UserOpSrvConfig `mapstructure:"userop_srv" json:"userop_srv" yaml:"userop_srv"`
	JWTInfo       JWTConfig       `mapstructure:"jwt" json:"jwt" yaml:"jwt"`
	ConsulInfo    ConsulConfig    `mapstructure:"consul" json:"consul" yaml:"consul"`
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
