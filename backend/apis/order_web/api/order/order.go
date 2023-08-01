package order

import (
	"apis/order_web/api"
	"apis/order_web/forms"
	"apis/order_web/global"
	"apis/order_web/models"
	"apis/order_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/smartwalle/alipay/v3"
	"go.uber.org/zap"
)

func generate_alipay_url(orderSn string, total float32) (string, error) {
	client, err := alipay.New(global.ServerConfig.AlipayInfo.AppId, global.ServerConfig.AlipayInfo.PrivateKey, false)
	if err != nil {
		zap.S().Errorw("alipay.New failed", "msg", err.Error())
		return "", err
	}

	err = client.LoadAliPayPublicKey(global.ServerConfig.AlipayInfo.AliPublicKey)
	if err != nil {
		zap.S().Errorw("client.LoadAliPayPublicKey failed", "msg", err.Error())
		return "", err
	}

	p := alipay.TradePagePay{}
	p.NotifyURL = global.ServerConfig.AlipayInfo.NotifyUrl
	p.ReturnURL = global.ServerConfig.AlipayInfo.ReturnUrl
	p.Subject = "pygo-" + orderSn
	p.OutTradeNo = orderSn
	p.TotalAmount = strconv.FormatFloat(float64(total), 'f', 2, 64)
	p.ProductCode = "FAST_INSTANT_TRADE_PAY"

	url, err := client.TradePagePay(p)
	if err != nil {
		zap.S().Errorw("client.TradePagePay failed", "msg", err.Error())
		return "", err
	}

	return url.String(), nil
}

func List(c *gin.Context) {
	userId, _ := c.Get("userId")
	claims := c.MustGet("claims").(*models.CustomClaims)

	request := &proto.OrderFilterRequest{}
	if claims.AuthorityId == 1 {
		// 普通用户, 只能查看自己的订单
		request.UserId = int32(userId.(uint))
	}

	pages := c.DefaultQuery("p", "0")
	pagesInt, _ := strconv.Atoi(pages)
	request.Pages = int32(pagesInt)

	perNums := c.DefaultQuery("pnum", "10")
	perNumsInt, _ := strconv.Atoi(perNums)
	request.PagePerNums = int32(perNumsInt)

	rsp, err := global.OrderSrvClient.OrderList(context.WithValue(context.Background(), "ginContext", c), request)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap := gin.H{
		"total": rsp.Total,
	}
	orderList := make([]interface{}, 0)
	for _, item := range rsp.Data {
		tmp := map[string]interface{}{
			"id":       item.Id,
			"status":   item.Status,
			"pay_type": item.PayType,
			"user":     item.UserId,
			"message":  item.Message,
			"address":  item.Address,
			"name":     item.Name,
			"mobile":   item.Mobile,
			"order_sn": item.OrderSn,
			"add_time": item.AddTime,
		}
		orderList = append(orderList, tmp)
	}
	reMap["data"] = orderList
	c.JSON(http.StatusOK, reMap)
}

func New(c *gin.Context) {
	orderForm := forms.OrderCreateForm{}
	if err := c.ShouldBindJSON(&orderForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}
	userId, _ := c.Get("userId")
	rsp, err := global.OrderSrvClient.CreateOrder(context.WithValue(context.Background(), "ginContext", c), &proto.OrderRequest{
		UserId:  int32(userId.(uint)),
		Name:    orderForm.Name,
		Mobile:  orderForm.Mobile,
		Message: orderForm.Message,
		Address: orderForm.Address,
	})
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.CreateOrder failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	// 生成支付宝的支付链接
	url, err := generate_alipay_url(rsp.OrderSn, rsp.Total)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id":         rsp.Id,
		"alipay_url": url,
	})
}

func Detail(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")

	request := &proto.OrderRequest{
		Id: int32(id),
	}
	claims := c.MustGet("claims").(*models.CustomClaims)
	if claims.AuthorityId == 1 {
		// 普通用户, 只能查看自己的订单
		request.UserId = int32(userId.(uint))
	}

	rsp, err := global.OrderSrvClient.OrderDetail(context.WithValue(context.Background(), "ginContext", c), request)
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.OrderDetail failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	goodsList := make([]interface{}, 0)
	for _, item := range rsp.Data {
		goodsList = append(goodsList, gin.H{
			"id":    item.GoodsId,
			"name":  item.GoodsName,
			"image": item.GoodsImage,
			"price": item.GoodsPrice,
			"nums":  item.GoodsNums,
		})
	}
	reMap := gin.H{
		"id":       rsp.OrderInfo.Id,
		"status":   rsp.OrderInfo.Status,
		"user":     rsp.OrderInfo.UserId,
		"message":  rsp.OrderInfo.Message,
		"address":  rsp.OrderInfo.Address,
		"total":    rsp.OrderInfo.Total,
		"name":     rsp.OrderInfo.Name,
		"mobile":   rsp.OrderInfo.Mobile,
		"pay_type": rsp.OrderInfo.PayType,
		"order_sn": rsp.OrderInfo.OrderSn,
	}
	reMap["goods"] = goodsList

	// 生成支付宝的支付链接
	url, err := generate_alipay_url(rsp.OrderInfo.OrderSn, rsp.OrderInfo.Total)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap["alipay_url"] = url
	c.JSON(http.StatusOK, reMap)
}
