package router

import (
	"apis/order_web/api/shop_cart"
	"apis/order_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitShopCartRouter(Router *gin.RouterGroup) {
	ShopCartRouter := Router.Group("shopcarts").Use(middlewares.JWTAuth())
	{
		ShopCartRouter.GET("", shop_cart.List)
		ShopCartRouter.DELETE("/:id", shop_cart.Delete)
		ShopCartRouter.POST("", shop_cart.New)
		ShopCartRouter.PATCH("/:id", shop_cart.Update)
	}
}
