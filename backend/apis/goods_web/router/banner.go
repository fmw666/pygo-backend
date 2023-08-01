package router

import (
	"apis/goods_web/middlewares"

	"apis/goods_web/api/banner"

	"github.com/gin-gonic/gin"
)

func InitBannerRouter(Router *gin.RouterGroup) {
	BannerRouter := Router.Group("banners").Use(middlewares.Trace())
	{
		BannerRouter.GET("", banner.List)
		BannerRouter.POST("", middlewares.JWTAuth(), middlewares.IsAdminAuth(), banner.New)
		BannerRouter.DELETE("/:id", middlewares.JWTAuth(), middlewares.IsAdminAuth(), banner.Delete)
		BannerRouter.PUT("/:id", middlewares.JWTAuth(), middlewares.IsAdminAuth(), banner.Update)
	}
}
