package main

import (
	"apis/goods_web/global"
	"apis/goods_web/initialize"
	"apis/goods_web/utils"
	"apis/goods_web/utils/register/consul"
	"fmt"
	"os"
	"os/signal"
	"syscall"

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

	// 6. init sentinel
	initialize.InitSentinel()

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
