package forms

type GoodsForm struct {
	Name        string   `form:"name" json:"name" binding:"required,min=3,max=100"`
	GoodsSn     string   `form:"goods_sn" json:"goods_sn" binding:"required,min=3,max=100"`
	Stocks      int32    `form:"stocks" json:"stocks" binding:"required,min=1"`
	CategoryId  int32    `form:"category_id" json:"category_id" binding:"required"`
	MarketPrice float32  `form:"market_price" json:"market_price" binding:"required"`
	ShopPrice   float32  `form:"shop_price" json:"shop_price" binding:"required"`
	GoodsBrief  string   `form:"goods_brief" json:"goods_brief" binding:"required,min=3,max=100"`
	Images      []string `form:"images" json:"images" binding:"required"`
	DescImages  []string `form:"desc_images" json:"desc_images" binding:"required"`
	GoodsDesc   string   `form:"desc" json:"desc" binding:"required"`
	ShipFree    *bool    `form:"ship_free" json:"ship_free"`
	FrontImage  string   `form:"front_image" json:"front_image" binding:"required"`
	BrandId     int32    `form:"brand_id" json:"brand_id" binding:"required"`
}

type GoodsStatusUpdateForm struct {
	IsNew  *bool `form:"is_new" json:"is_new"`
	IsHot  *bool `form:"is_hot" json:"is_hot"`
	OnSale *bool `form:"on_sale" json:"on_sale"`
}
