package shop_cart

import (
	"apis/order_web/api"
	"apis/order_web/forms"
	"apis/order_web/global"
	"apis/order_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func List(c *gin.Context) {
	userId, _ := c.Get("userId")
	zap.S().Infof("userId: %v", userId)
	rsp, err := global.OrderSrvClient.CartItemList(context.Background(), &proto.UserInfoRequest{
		Id: int32(userId.(uint)),
	})
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.CartItemList failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	ids := make([]int32, 0)
	for _, item := range rsp.Data {
		ids = append(ids, item.GoodsId)
	}
	if len(ids) == 0 {
		c.JSON(http.StatusOK, gin.H{
			"total": 0,
		})
		return
	}

	// 获取商品详情
	goodsRsp, err := global.GoodsSrvClient.BatchGetGoods(context.Background(), &proto.BatchGoodsIdInfo{
		Id: ids,
	})
	if err != nil {
		zap.S().Errorw("global.GoodsSrvClient.BatchGetGoods failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap := gin.H{
		"total": rsp.Total,
	}
	/*
		{
			"total": 100,
			"data": [
				{
					"id": 1,
					"goods_id": 1,
					"goods_name": "测试商品",
					"goods_image": "http://www.img.com",
					"nums": 10,
					"goods_price": 100,
					"checked": true
				}
			]
		}
	*/
	goodsList := make([]interface{}, 0)
	for _, item := range rsp.Data {
		for _, goods := range goodsRsp.Data {
			if item.GoodsId == goods.Id {
				tmp := map[string]interface{}{
					"id":          item.Id,
					"goods_id":    item.GoodsId,
					"goods_name":  goods.Name,
					"goods_image": goods.GoodsFrontImage,
					"goods_price": goods.ShopPrice,
					"nums":        item.Nums,
					"checked":     item.Checked,
				}

				goodsList = append(goodsList, tmp)
			}
		}
	}
	reMap["data"] = goodsList

	c.JSON(http.StatusOK, reMap)
}

func New(c *gin.Context) {
	itemForm := forms.ShopCartItemForm{}
	if err := c.ShouldBindJSON(&itemForm); err != nil {
		zap.S().Errorw("c.ShouldBindJSON failed", "msg", err.Error())
		api.HandleValidatorError(c, err)
		return
	}

	// 获取商品详情
	_, err := global.GoodsSrvClient.GetGoodsDetail(context.Background(), &proto.GoodInfoRequest{
		Id: itemForm.GoodsId,
	})
	if err != nil {
		zap.S().Errorw("global.GoodsSrvClient.GetGoodsDetail failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	// 获取库存
	invRsp, err := global.InventorySrvClient.InvDetail(context.Background(), &proto.GoodsInvInfo{
		GoodsId: itemForm.GoodsId,
	})
	if err != nil {
		zap.S().Errorw("global.InventorySrvClient.InvDetail failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}
	if invRsp.Num <= itemForm.Nums {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "库存不足",
		})
		return
	}

	userId, _ := c.Get("userId")
	rsp, err := global.OrderSrvClient.CreateCartItem(context.Background(), &proto.CartItemRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: itemForm.GoodsId,
		Nums:    itemForm.Nums,
	})
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.CreateCartItem failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id": rsp.Id,
	})
}

func Detail(c *gin.Context) {

}

func Delete(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "参数错误",
		})
		return
	}

	userId, _ := c.Get("userId")
	_, err = global.OrderSrvClient.DeleteCartItem(context.Background(), &proto.CartItemRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: int32(idInt),
	})
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.DeleteCartItem failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func Update(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "参数错误",
		})
		return
	}

	itemForm := forms.ShopCartItemUpdateForm{}
	if err := c.ShouldBindJSON(&itemForm); err != nil {
		zap.S().Errorw("c.ShouldBindJSON failed", "msg", err.Error())
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")
	request := &proto.CartItemRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: int32(idInt),
		Nums:    itemForm.Nums,
	}
	if itemForm.Checked != nil {
		request.Checked = *itemForm.Checked
	}

	_, err = global.OrderSrvClient.UpdateCartItem(context.Background(), request)
	if err != nil {
		zap.S().Errorw("global.OrderSrvClient.UpdateCartItem failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}
