package router

import (
	"apis/userop_web/api/userfavorite"
	"apis/userop_web/middlewares"

	"github.com/gin-gonic/gin"
)

func InitUserFavoriteRouter(Router *gin.RouterGroup) {
	UserFavoriteRouter := Router.Group("userfavorites").Use(middlewares.JWTAuth())
	{
		UserFavoriteRouter.GET("", userfavorite.List)
		UserFavoriteRouter.GET("/:id", userfavorite.Detail)
		UserFavoriteRouter.DELETE("/:id", userfavorite.Delete)
		UserFavoriteRouter.POST("", userfavorite.New)
	}
}
