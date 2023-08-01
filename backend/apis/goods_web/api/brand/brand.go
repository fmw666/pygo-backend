package brand

import (
	"apis/goods_web/api"
	"apis/goods_web/forms"
	"apis/goods_web/global"
	"apis/goods_web/proto"
	"context"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func BrandList(c *gin.Context) {
	pn := c.DefaultQuery("pn", "0")
	pnInt, _ := strconv.Atoi(pn)
	pSize := c.DefaultQuery("psize", "0")
	pSizeInt, _ := strconv.Atoi(pSize)

	rsp, err := global.BrandSrvClient.BrandList(context.Background(), &proto.BrandFilterRequest{
		Pages:       int32(pnInt),
		PagePerNums: int32(pSizeInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	result := make([]interface{}, 0)
	reMap := make(map[string]interface{})
	reMap["total"] = rsp.Total
	for _, value := range rsp.Data[pnInt : pnInt*pSizeInt+pSizeInt] {
		result = append(result, map[string]interface{}{
			"id":   value.Id,
			"name": value.Name,
			"logo": value.Logo,
		})
	}

	reMap["data"] = result
	c.JSON(http.StatusOK, reMap)
}

func NewBrand(c *gin.Context) {
	brandForm := forms.BrandForm{}
	if err := c.ShouldBindJSON(&brandForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	rsp, err := global.BrandSrvClient.CreateBrand(context.Background(), &proto.BrandRequest{
		Name: brandForm.Name,
		Logo: brandForm.Logo,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, map[string]interface{}{
		"id":   rsp.Id,
		"name": rsp.Name,
		"logo": rsp.Logo,
	})
}

func UpdateBrand(c *gin.Context) {
	brandForm := forms.BrandForm{}
	if err := c.ShouldBindJSON(&brandForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	_, err = global.BrandSrvClient.UpdateBrand(context.Background(), &proto.BrandRequest{
		Id:   int32(idInt),
		Name: brandForm.Name,
		Logo: brandForm.Logo,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func DeleteBrand(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	_, err = global.BrandSrvClient.DeleteBrand(context.Background(), &proto.BrandRequest{
		Id: int32(idInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func GetCategoryBrandList(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	rsp, err := global.BrandSrvClient.GetCategoryBrandList(context.Background(), &proto.CategoryInfoRequest{
		Id: int32(idInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		result = append(result, map[string]interface{}{
			"id":   value.Id,
			"name": value.Name,
			"logo": value.Logo,
		})
	}

	c.JSON(http.StatusOK, result)
}

func CategoryBrandList(c *gin.Context) {
	rsp, err := global.BrandSrvClient.CategoryBrandList(context.Background(), &proto.CategoryBrandFilterRequest{})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}
	reMap := map[string]interface{}{
		"total": rsp.Total,
	}

	result := make([]interface{}, 0)
	for _, value := range rsp.Data {
		result = append(result, map[string]interface{}{
			"id": value.Id,
			"category": map[string]interface{}{
				"id":   value.Category.Id,
				"name": value.Category.Name,
			},
			"brand": map[string]interface{}{
				"id":   value.Brand.Id,
				"name": value.Brand.Name,
				"logo": value.Brand.Logo,
			},
		})
	}
	reMap["data"] = result

	c.JSON(http.StatusOK, reMap)
}

func NewCategoryBrand(c *gin.Context) {
	categoryBrandForm := forms.CategoryBrandForm{}
	if err := c.ShouldBindJSON(&categoryBrandForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	rsp, err := global.BrandSrvClient.CreateCategoryBrand(context.Background(), &proto.CategoryBrandRequest{
		CategoryId: categoryBrandForm.CategoryId,
		BrandId:    categoryBrandForm.BrandId,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.JSON(http.StatusOK, map[string]interface{}{
		"id": rsp.Id,
	})
}

func UpdateCategoryBrand(c *gin.Context) {
	categoryBrandForm := forms.CategoryBrandForm{}
	if err := c.ShouldBindJSON(&categoryBrandForm); err != nil {
		api.HandleValidatorError(c, err)
		return
	}

	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	_, err = global.BrandSrvClient.UpdateCategoryBrand(context.Background(), &proto.CategoryBrandRequest{
		Id:         int32(idInt),
		CategoryId: categoryBrandForm.CategoryId,
		BrandId:    categoryBrandForm.BrandId,
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}

func DeleteCategoryBrand(c *gin.Context) {
	id := c.Param("id")
	idInt, err := strconv.ParseInt(id, 10, 32)
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	_, err = global.BrandSrvClient.DeleteCategoryBrand(context.Background(), &proto.CategoryBrandRequest{
		Id: int32(idInt),
	})
	if err != nil {
		api.HandleGrpcErrorToHttp(err, c)
		return
	}

	c.Status(http.StatusOK)
}
