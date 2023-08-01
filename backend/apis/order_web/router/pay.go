package router

import (
	"apis/order_web/api/pay"

	"github.com/gin-gonic/gin"
)

func InitPayRouter(Router *gin.RouterGroup) {
	PayRouter := Router.Group("pay")
	{
		PayRouter.POST("alipay/notify", pay.Notify)
	}
}
