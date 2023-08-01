package router

import (
	"apis/goods_web/api/brand"
	"apis/goods_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitBrandRouter(Router *gin.RouterGroup) {
	BrandRouter := Router.Group("brands").Use(middlewares.Trace())
	{
		BrandRouter.GET("", brand.BrandList)
		BrandRouter.POST("", brand.NewBrand)
		BrandRouter.PUT("/:id", brand.UpdateBrand)
		BrandRouter.DELETE("/:id", brand.DeleteBrand)
	}

	CategoryBrandRouter := Router.Group("categorybrands").Use(middlewares.Trace())
	{
		CategoryBrandRouter.GET("", brand.CategoryBrandList)
		CategoryBrandRouter.POST("", brand.NewCategoryBrand)
		CategoryBrandRouter.PUT("/:id", brand.UpdateCategoryBrand)
		CategoryBrandRouter.DELETE("/:id", brand.DeleteCategoryBrand)
		CategoryBrandRouter.GET("/:id", brand.GetCategoryBrandList)
	}
}
