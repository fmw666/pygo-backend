package router

import (
	"apis/userop_web/api/address"
	"apis/userop_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitAddressRouter(Router *gin.RouterGroup) {
	AddressRouter := Router.Group("addresses").Use(middlewares.JWTAuth())
	{
		AddressRouter.GET("", address.List)
		AddressRouter.DELETE("/:id", address.Delete)
		AddressRouter.POST("", address.New)
		AddressRouter.PUT("/:id", address.Update)
	}
}
