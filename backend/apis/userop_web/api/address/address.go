package address

import (
	"apis/userop_web/api"
	"apis/userop_web/forms"
	"apis/userop_web/global"
	"apis/userop_web/models"
	"apis/userop_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func List(c *gin.Context) {
	request := &proto.AddressRequest{}

	claims := c.MustGet("claims").(*models.CustomClaims)
	if claims.AuthorityId == 1 {
		userId, _ := c.Get("userId")
		request.UserId = int32(userId.(uint))
	}

	rsp, err := global.AddressClient.GetAddressList(context.Background(), request)
	if err != nil {
		zap.S().Errorw("AddressList failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap := gin.H{
		"total": rsp.Total,
	}

	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		result = append(result, gin.H{
			"id":            value.Id,
			"user_id":       value.UserId,
			"province":      value.Province,
			"city":          value.City,
			"district":      value.District,
			"address":       value.Address,
			"signer_name":   value.SignerName,
			"signer_mobile": value.SignerMobile,
		})
	}

	reMap["data"] = result
	c.JSON(http.StatusOK, reMap)
}

func Delete(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	_, err = global.AddressClient.DeleteAddress(context.Background(), &proto.AddressRequest{
		Id: int32(idInt),
	})
	if err != nil {
		zap.S().Errorw("DeleteAddress failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "删除成功",
	})
}

func New(c *gin.Context) {
	addressForm := forms.AddressForm{}
	if err := c.ShouldBindJSON(&addressForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	userId, _ := c.Get("userId")

	rsp, err := global.AddressClient.CreateAddress(context.Background(), &proto.AddressRequest{
		UserId:       int32(userId.(uint)),
		Province:     addressForm.Province,
		City:         addressForm.City,
		District:     addressForm.District,
		Address:      addressForm.Address,
		SignerName:   addressForm.SignerName,
		SignerMobile: addressForm.SignerMobile,
	})
	if err != nil {
		zap.S().Errorw("CreateAddress failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id": rsp.Id,
	})
}

func Update(c *gin.Context) {
	addressForm := forms.AddressForm{}
	if err := c.ShouldBindJSON(&addressForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	_, err = global.AddressClient.UpdateAddress(context.Background(), &proto.AddressRequest{
		Id:           int32(idInt),
		Province:     addressForm.Province,
		City:         addressForm.City,
		District:     addressForm.District,
		Address:      addressForm.Address,
		SignerName:   addressForm.SignerName,
		SignerMobile: addressForm.SignerMobile,
	})
	if err != nil {
		zap.S().Errorw("UpdateAddress failed", "msg", err.Error())
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"msg": "更新成功",
	})
}
