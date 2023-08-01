package initialize

import (
	sentinel "github.com/alibaba/sentinel-golang/api"
	"github.com/alibaba/sentinel-golang/core/flow"
	"go.uber.org/zap"
)

func InitSentinel() {

	err := sentinel.InitDefault()
	if err != nil {
		zap.S().Fatalf("[InitSentinel] sentinel.InitDefault failed", "msg", err.Error())
	}

	// 10s 内最多只能访问 3 次
	_, err = flow.LoadRules([]*flow.Rule{
		{
			Resource:               "goods-list",
			TokenCalculateStrategy: flow.Direct,
			ControlBehavior:        flow.Reject,
			Threshold:              3,
			StatIntervalInMs:       6000,
		},
	})
	if err != nil {
		zap.S().Fatalf("[InitSentinel] sentinel.LoadRules failed", "msg", err.Error())
	}
}
