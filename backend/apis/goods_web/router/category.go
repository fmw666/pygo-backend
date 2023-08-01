package router

import (
	"apis/goods_web/api/category"
	"apis/goods_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitCategoryRouter(Router *gin.RouterGroup) {
	CategoryRouter := Router.Group("categorys").Use(middlewares.Trace())
	{
		CategoryRouter.GET("", category.List)
		CategoryRouter.POST("", category.New)
		CategoryRouter.GET("/:id", category.Detail)
		CategoryRouter.DELETE("/:id", category.Delete)
		CategoryRouter.PUT("/:id", category.Update)
	}
}
