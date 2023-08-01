package initialize

import (
	"apis/goods_web/global"
	"apis/goods_web/proto"
	"apis/goods_web/utils/otgrpc"
	"fmt"

	_ "github.com/mbobakov/grpc-consul-resolver"
	"github.com/opentracing/opentracing-go"
	"go.uber.org/zap"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func InitSrvConn() {
	consulInfo := global.ServerConfig.ConsulInfo
	goodsConn, err := grpc.Dial(
		fmt.Sprintf("consul://%s:%d/%s?wait=14s", consulInfo.Host, consulInfo.Port, global.ServerConfig.GoodsSrvInfo.Name),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy": "round_robin"}`),
		grpc.WithUnaryInterceptor(otgrpc.OpenTracingClientInterceptor(opentracing.GlobalTracer())),
	)
	if err != nil {
		zap.S().Fatalf("[InitSrvConn] grpc.Dial failed", "msg", err.Error())
	}

	global.GoodsSrvClient = proto.NewGoodsClient(goodsConn)
	global.CategorySrvClient = proto.NewCategoryClient(goodsConn)
	global.BannerSrvClient = proto.NewBannerClient(goodsConn)
	global.BrandSrvClient = proto.NewBrandClient(goodsConn)
}
