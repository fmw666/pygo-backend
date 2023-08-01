package forms

type SendSmsForm struct {
	Mobile string `form:"mobile" json:"mobile" binding:"required,len=11"`
	// 1: register, 2: login
	Type uint `form:"type" json:"type" binding:"required,oneof=1 2"`
}
