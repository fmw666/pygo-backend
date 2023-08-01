package category

import (
	"apis/goods_web/api"
	"apis/goods_web/forms"
	"apis/goods_web/global"
	"apis/goods_web/proto"
	"context"
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/golang/protobuf/ptypes/empty"
	"go.uber.org/zap"
)

func List(c *gin.Context) {
	r, err := global.CategorySrvClient.GetAllCategorysList(context.Background(), &empty.Empty{})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	data := make([]interface{}, 0)
	err = json.Unmarshal([]byte(r.JsonData), &data)
	if err != nil {
		zap.S().Errorw("[List] json.Unmarshal failed", "msg", err.Error())
	}
	c.JSON(http.StatusOK, data)
}

func Detail(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		zap.S().Errorw("[Detail] strconv.ParseInt failed", "msg", err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "参数错误",
		})
		return
	}

	reMap := make(map[string]interface{})
	subCategorys := make([]interface{}, 0)
	if r, err := global.CategorySrvClient.GetSubCategory(context.Background(), &proto.CategoryListRequest{
		Id: int32(idInt),
	}); err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	} else {
		for _, value := range r.SubCategorys {
			subCategorys = append(subCategorys, map[string]interface{}{
				"id":              value.Id,
				"name":            value.Name,
				"level":           value.Level,
				"parent_category": value.ParentCategory,
				"is_tab":          value.IsTab,
			})
		}
		reMap["sub_categorys"] = subCategorys
		reMap["id"] = r.Info.Id
		reMap["name"] = r.Info.Name
		reMap["level"] = r.Info.Level
		reMap["parent_category"] = r.Info.ParentCategory
		reMap["is_tab"] = r.Info.IsTab

		c.JSON(http.StatusOK, reMap)
	}
}

func New(c *gin.Context) {
	categoryForm := forms.CategoryForm{}
	if err := c.ShouldBindJSON(&categoryForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	r, err := global.CategorySrvClient.CreateCategory(context.Background(), &proto.CategoryInfoRequest{
		Name:           categoryForm.Name,
		ParentCategory: categoryForm.ParentCategory,
		Level:          categoryForm.Level,
		IsTab:          *categoryForm.IsTab,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	rspMap := map[string]interface{}{
		"id":              r.Id,
		"name":            r.Name,
		"parent_category": r.ParentCategory,
		"level":           r.Level,
		"is_tab":          r.IsTab,
	}

	c.JSON(http.StatusOK, rspMap)
}

func Delete(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		zap.S().Errorw("[Delete] strconv.ParseInt failed", "msg", err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "参数错误",
		})
		return
	}

	// 1. 查询该分类所有的子分类
	// 2. 将所有的分类逻辑删除
	// 3. 将所有分类下的商品逻辑删除
	_, err = global.CategorySrvClient.DeleteCategory(context.Background(), &proto.DeleteCategoryRequest{
		Id: int32(idInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func Update(c *gin.Context) {
	categoryForm := forms.CategoryUpdateForm{}
	if err := c.ShouldBindJSON(&categoryForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		zap.S().Errorw("[Update] strconv.ParseInt failed", "msg", err.Error())
		c.JSON(http.StatusBadRequest, gin.H{
			"msg": "参数错误",
		})
		return
	}

	_, err = global.CategorySrvClient.UpdateCategory(context.Background(), &proto.CategoryInfoRequest{
		Id:   int32(idInt),
		Name: categoryForm.Name,
		IsTab: func() bool {
			if categoryForm.IsTab != nil {
				return *categoryForm.IsTab
			}
			return false
		}(),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}
