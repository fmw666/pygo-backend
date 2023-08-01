package main

import (
	"apis/order_web/global"
	"apis/order_web/initialize"
	"apis/order_web/utils"
	"apis/order_web/utils/register/consul"
	myvalidator "apis/order_web/validator"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/gin-gonic/gin/binding"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	uuid "github.com/satori/go.uuid"
	"go.uber.org/zap"
)

func main() {
	// 0. set debug mode
	os.Setenv(global.Debug, "true")

	// 1. init logger
	initialize.InitLogger()

	// 2. init config
	initialize.InitConfig()

	// 3. init routers
	Router := initialize.Routers()

	// 4. init translator
	if err := initialize.InitTrans("zh"); err != nil {
		zap.S().Panic("An error occurred while setting up translations", err)
	}

	// 5. init grpc client
	initialize.InitSrvConn()

	// 6. init validator
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		_ = v.RegisterValidation("mobile", myvalidator.ValidateMobile)
		_ = v.RegisterTranslation("mobile", global.Trans, func(ut ut.Translator) error {
			return ut.Add("mobile", "{0} 非法的手机号", true)
		}, func(ut ut.Translator, fe validator.FieldError) string {
			t, _ := ut.T("mobile", fe.Field())
			return t
		})
	}

	// if debug mode, use a default port. otherwise, use a random port
	debug := os.Getenv(global.Debug) == "true"
	if !debug {
		port, err := utils.GetFreePort()
		if err == nil {
			global.ServerConfig.Port = port
		}
	}

	// 7. register service to consul
	registerClient := consul.NewRegistryClient(global.ServerConfig.ConsulInfo.Host, global.ServerConfig.ConsulInfo.Port)
	serviceId := uuid.NewV4().String()
	err := registerClient.Register(global.ServerConfig.Host, global.ServerConfig.Port, global.ServerConfig.Name, global.ServerConfig.Tags, serviceId)
	if err != nil {
		zap.S().Panic("An error occurred while registering service to consul", err)
	}

	zap.S().Debugf("Start to listening the incoming requests on http address: %d", global.ServerConfig.Port)
	go func() {
		if err := Router.Run(fmt.Sprintf(":%d", global.ServerConfig.Port)); err != nil {
			zap.S().Panic("An error occurred while starting the http server", err)
		}
	}()

	// 8. graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	if err = registerClient.DeRegister(serviceId); err != nil {
		zap.S().Panic("An error occurred while deregistering service from consul", err)
	}
}
