package banner

import (
	"apis/goods_web/api"
	"apis/goods_web/forms"
	"apis/goods_web/global"
	"apis/goods_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/golang/protobuf/ptypes/empty"
)

func List(c *gin.Context) {
	rsp, err := global.BannerSrvClient.BannerList(context.Background(), &empty.Empty{})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		result = append(result, map[string]interface{}{
			"id":    value.Id,
			"image": value.Image,
			"index": value.Index,
			"url":   value.Url,
		})
	}

	c.JSON(http.StatusOK, result)
}

func New(c *gin.Context) {
	bannerForm := forms.BannerForm{}
	if err := c.ShouldBindJSON(&bannerForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	rsp, err := global.BannerSrvClient.CreateBanner(context.Background(), &proto.BannerRequest{
		Image: bannerForm.Image,
		Index: bannerForm.Index,
		Url:   bannerForm.Url,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, map[string]interface{}{
		"id":    rsp.Id,
		"index": rsp.Index,
		"image": rsp.Image,
		"url":   rsp.Url,
	})
}

func Delete(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		c.Status(http.StatusBadRequest)
		return
	}

	_, err = global.BannerSrvClient.DeleteBanner(context.Background(), &proto.BannerRequest{
		Id: int32(idInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func Update(c *gin.Context) {
	bannerForm := forms.BannerForm{}
	if err := c.ShouldBindJSON(&bannerForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		c.Status(http.StatusBadRequest)
		return
	}

	_, err = global.BannerSrvClient.UpdateBanner(context.Background(), &proto.BannerRequest{
		Id:    int32(idInt),
		Image: bannerForm.Image,
		Index: bannerForm.Index,
		Url:   bannerForm.Url,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}
