package forms

type BrandForm struct {
	Name string `form:"name" json:"name" binding:"required,min=3,max=100"`
	Logo string `form:"logo" json:"logo" binding:"required"`
}

type CategoryBrandForm struct {
	CategoryId int32 `form:"category_id" json:"category_id" binding:"required"`
	BrandId    int32 `form:"brand_id" json:"brand_id" binding:"required"`
}
