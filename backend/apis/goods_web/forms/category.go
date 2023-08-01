package forms

type CategoryForm struct {
	Name           string `form:"name" json:"name" binding:"required,min=3,max=100"`
	ParentCategory int32  `form:"parent" json:"parent" binding:"required"`
	Level          int32  `form:"level" json:"level" binding:"required,oneof=1 2 3"`
	IsTab          *bool  `form:"is_tab" json:"is_tab"`
}

type CategoryUpdateForm struct {
	Name  string `form:"name" json:"name" binding:"required,min=3,max=100"`
	IsTab *bool  `form:"is_tab" json:"is_tab"`
}
