package pay

import (
	"apis/order_web/api"
	"apis/order_web/global"
	"apis/order_web/proto"
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/smartwalle/alipay/v3"
	"go.uber.org/zap"
)

func Notify(c *gin.Context) {
	client, err := alipay.New(global.ServerConfig.AlipayInfo.AppId, global.ServerConfig.AlipayInfo.PrivateKey, false)
	if err != nil {
		zap.S().Errorw("alipay.New failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	err = client.LoadAliPayPublicKey(global.ServerConfig.AlipayInfo.AliPublicKey)
	if err != nil {
		zap.S().Errorw("client.LoadAliPayPublicKey failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	noti, err := client.GetTradeNotification(c.Request)
	if err != nil {
		zap.S().Errorw("client.GetTradeNotification failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	_, err = global.OrderSrvClient.UpdateOrderStatus(context.Background(), &proto.OrderStatusRequest{
		OrderSn: noti.OutTradeNo,
		Status:  string(noti.TradeStatus),
	})
	if err != nil {
		zap.S().Errorw("UpdateOrderStatus failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "success",
	})
}
