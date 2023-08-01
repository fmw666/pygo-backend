package forms

type UserFavoriteForm struct {
	GoodsId int32 `form:"goods" json:"goods" binding:"required"`
}
