package userfavorite

import (
	"apis/userop_web/api"
	"apis/userop_web/forms"
	"apis/userop_web/global"
	"apis/userop_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func List(c *gin.Context) {
	userId, _ := c.Get("userId")
	rsp, err := global.UserFavoriteClient.GetUserFavoriteList(context.Background(), &proto.UserFavoriteRequest{
		UserId: int32(userId.(uint)),
	})
	if err != nil {
		zap.S().Errorw("GetUserFavoriteList failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	goodIds := make([]int32, 0)
	for _, value := range rsp.Data {
		goodIds = append(goodIds, value.GoodsId)
	}

	if len(goodIds) == 0 {
		c.JSON(http.StatusOK, gin.H{
			"total": 0,
		})
		return
	}

	// 获取商品信息
	goodsRsp, err := global.GoodsSrvClient.BatchGetGoods(context.Background(), &proto.BatchGoodsIdInfo{
		Id: goodIds,
	})
	if err != nil {
		zap.S().Errorw("BatchGetGoods failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap := gin.H{
		"total": rsp.Total,
	}

	goodsList := make([]interface{}, 0)
	for _, value := range rsp.Data {
		data := gin.H{
			"id": value.GoodsId,
		}

		for _, good := range goodsRsp.Data {
			if value.GoodsId == good.Id {
				data["name"] = good.Name
				data["shop_price"] = good.ShopPrice
			}
		}

		goodsList = append(goodsList, data)
	}

	reMap["data"] = goodsList
	c.JSON(http.StatusOK, reMap)
}

func Detail(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")
	_, err = global.UserFavoriteClient.GetUserFavoriteDetail(context.Background(), &proto.UserFavoriteRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: int32(idInt),
	})
	if err != nil {
		zap.S().Errorw("GetUserFavoriteDetail failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "查询成功",
	})
}

func Delete(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")
	_, err = global.UserFavoriteClient.DeleteUserFavorite(context.Background(), &proto.UserFavoriteRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: int32(idInt),
	})
	if err != nil {
		zap.S().Errorw("DeleteUserFavorite failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "删除成功",
	})
}

func New(c *gin.Context) {
	userFavoriteForm := forms.UserFavoriteForm{}
	if err := c.ShouldBindJSON(&userFavoriteForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")
	_, err := global.UserFavoriteClient.CreateUserFavorite(context.Background(), &proto.UserFavoriteRequest{
		UserId:  int32(userId.(uint)),
		GoodsId: userFavoriteForm.GoodsId,
	})
	if err != nil {
		zap.S().Errorw("CreateUserFavorite failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "收藏成功",
	})
}
