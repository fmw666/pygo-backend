package router

import (
	"apis/order_web/api/order"
	"apis/order_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitOrderRouter(Router *gin.RouterGroup) {
	OrderRouter := Router.Group("orders").Use(middlewares.JWTAuth()).Use(middlewares.Trace())
	{
		OrderRouter.GET("", order.List)
		OrderRouter.GET("/:id", order.Detail)
		OrderRouter.POST("", order.New)
	}
}
