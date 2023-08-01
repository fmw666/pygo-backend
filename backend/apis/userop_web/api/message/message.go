package message

import (
	"apis/userop_web/api"
	"apis/userop_web/forms"
	"apis/userop_web/global"
	"apis/userop_web/models"
	"apis/userop_web/proto"
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

func List(c *gin.Context) {
	request := &proto.MessageRequest{}

	userId, _ := c.Get("userId")
	claims := c.MustGet("claims").(*models.CustomClaims)
	if claims.AuthorityId == 1 {
		request.UserId = int32(userId.(uint))
	}
	rsp, err := global.MessageClient.MessageList(context.Background(), request)
	if err != nil {
		zap.S().Errorw("[List] 查询消息列表失败")
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	reMap := gin.H{
		"total": rsp.Total,
	}
	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		result = append(result, gin.H{
			"id":          value.Id,
			"user_id":     value.UserId,
			"messageType": value.MessageType,
			"subject":     value.Subject,
			"message":     value.Message,
			"file":        value.File,
		})
	}
	reMap["data"] = result

	c.JSON(http.StatusOK, reMap)
}

func New(c *gin.Context) {
	userId, _ := c.Get("userId")

	messageForm := forms.MessageForm{}
	if err := c.ShouldBindJSON(&messageForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	rsp, err := global.MessageClient.CreateMessage(context.Background(), &proto.MessageRequest{
		UserId:      int32(userId.(uint)),
		MessageType: messageForm.MessageType,
		Subject:     messageForm.Subject,
		Message:     messageForm.Message,
		File:        messageForm.File,
	})
	if err != nil {
		zap.S().Errorw("[New] 新建消息失败")
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id": rsp.Id,
	})
}
