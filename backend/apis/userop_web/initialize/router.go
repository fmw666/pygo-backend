package initialize

import (
	"apis/userop_web/middlewares"
	"apis/userop_web/router"
	"net/http"

	"github.com/gin-gonic/gin"
)

func Routers() *gin.Engine {
	Router := gin.Default()
	// health check
	Router.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"code":    http.StatusOK,
			"message": "ok",
		})
	})

	// CORS
	Router.Use(middlewares.Cors())

	ApiGroup := Router.Group("/v1")
	router.InitAddressRouter(ApiGroup)
	router.InitMessageRouter(ApiGroup)
	router.InitUserFavoriteRouter(ApiGroup)

	return Router
}
