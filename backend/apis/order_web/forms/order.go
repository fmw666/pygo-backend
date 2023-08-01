package forms

type OrderCreateForm struct {
	Address string `json:"address" binding:"required"`
	Name    string `json:"name" binding:"required"`
	Mobile  string `json:"mobile" binding:"required"`
	Message string `json:"message" binding:"required"`
}
