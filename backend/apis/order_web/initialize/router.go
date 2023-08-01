package initialize

import (
	"apis/order_web/middlewares"
	"apis/order_web/router"
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
	router.InitOrderRouter(ApiGroup)
	router.InitShopCartRouter(ApiGroup)
	router.InitPayRouter(ApiGroup)

	return Router
}
