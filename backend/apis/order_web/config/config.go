package config

type GoodsSrvConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type OrderSrvConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type InventorySrvConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
}

type JWTConfig struct {
	SigningKey string `mapstructure:"key" json:"key" yaml:"key"`
}

type ConsulConfig struct {
	Host string `mapstructure:"host" json:"host" yaml:"host"`
	Port int    `mapstructure:"port" json:"port" yaml:"port"`
}

type JaegerConfig struct {
	Name string `mapstructure:"name" json:"name" yaml:"name"`
	Host string `mapstructure:"host" json:"host" yaml:"host"`
	Port int    `mapstructure:"port" json:"port" yaml:"port"`
}

type AlipayConfig struct {
	AppId        string `mapstructure:"app_id" json:"app_id" yaml:"app_id"`
	PrivateKey   string `mapstructure:"private_key" json:"private_key" yaml:"private_key"`
	AliPublicKey string `mapstructure:"ali_public_key" json:"ali_public_key" yaml:"ali_public_key"`
	NotifyUrl    string `mapstructure:"notify_url" json:"notify_url" yaml:"notify_url"`
	ReturnUrl    string `mapstructure:"return_url" json:"return_url" yaml:"return_url"`
}

type ServerConfig struct {
	Name             string             `mapstructure:"name" json:"name" yaml:"name"`
	Host             string             `mapstructure:"host" json:"host" yaml:"host"`
	Port             int                `mapstructure:"port" json:"port" yaml:"port"`
	Tags             []string           `mapstructure:"tags" json:"tags" yaml:"tags"`
	Debug            string             `mapstructure:"debug" json:"debug" yaml:"debug"`
	GoodsSrvInfo     GoodsSrvConfig     `mapstructure:"goods_srv" json:"goods_srv" yaml:"goods_srv"`
	OrderSrvInfo     OrderSrvConfig     `mapstructure:"order_srv" json:"order_srv" yaml:"order_srv"`
	InventorySrvInfo InventorySrvConfig `mapstructure:"inventory_srv" json:"inventory_srv" yaml:"inventory_srv"`
	JWTInfo          JWTConfig          `mapstructure:"jwt" json:"jwt" yaml:"jwt"`
	ConsulInfo       ConsulConfig       `mapstructure:"consul" json:"consul" yaml:"consul"`
	JaegerInfo       JaegerConfig       `mapstructure:"jaeger" json:"jaeger" yaml:"jaeger"`
	AlipayInfo       AlipayConfig       `mapstructure:"alipay" json:"alipay" yaml:"alipay"`
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
