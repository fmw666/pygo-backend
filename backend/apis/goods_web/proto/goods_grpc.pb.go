// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v3.20.1
// source: goods.proto

package proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

const (
	Goods_GoodsList_FullMethodName      = "/Goods/GoodsList"
	Goods_BatchGetGoods_FullMethodName  = "/Goods/BatchGetGoods"
	Goods_CreateGoods_FullMethodName    = "/Goods/CreateGoods"
	Goods_DeleteGoods_FullMethodName    = "/Goods/DeleteGoods"
	Goods_UpdateGoods_FullMethodName    = "/Goods/UpdateGoods"
	Goods_GetGoodsDetail_FullMethodName = "/Goods/GetGoodsDetail"
)

// GoodsClient is the client API for Goods service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type GoodsClient interface {
	// 商品接口
	GoodsList(ctx context.Context, in *GoodsFilterRequest, opts ...grpc.CallOption) (*GoodsListResponse, error)
	BatchGetGoods(ctx context.Context, in *BatchGoodsIdInfo, opts ...grpc.CallOption) (*GoodsListResponse, error)
	CreateGoods(ctx context.Context, in *CreateGoodsInfo, opts ...grpc.CallOption) (*GoodsInfoResponse, error)
	DeleteGoods(ctx context.Context, in *DeleteGoodsInfo, opts ...grpc.CallOption) (*emptypb.Empty, error)
	UpdateGoods(ctx context.Context, in *CreateGoodsInfo, opts ...grpc.CallOption) (*emptypb.Empty, error)
	GetGoodsDetail(ctx context.Context, in *GoodInfoRequest, opts ...grpc.CallOption) (*GoodsInfoResponse, error)
}

type goodsClient struct {
	cc grpc.ClientConnInterface
}

func NewGoodsClient(cc grpc.ClientConnInterface) GoodsClient {
	return &goodsClient{cc}
}

func (c *goodsClient) GoodsList(ctx context.Context, in *GoodsFilterRequest, opts ...grpc.CallOption) (*GoodsListResponse, error) {
	out := new(GoodsListResponse)
	err := c.cc.Invoke(ctx, Goods_GoodsList_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *goodsClient) BatchGetGoods(ctx context.Context, in *BatchGoodsIdInfo, opts ...grpc.CallOption) (*GoodsListResponse, error) {
	out := new(GoodsListResponse)
	err := c.cc.Invoke(ctx, Goods_BatchGetGoods_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *goodsClient) CreateGoods(ctx context.Context, in *CreateGoodsInfo, opts ...grpc.CallOption) (*GoodsInfoResponse, error) {
	out := new(GoodsInfoResponse)
	err := c.cc.Invoke(ctx, Goods_CreateGoods_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *goodsClient) DeleteGoods(ctx context.Context, in *DeleteGoodsInfo, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Goods_DeleteGoods_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *goodsClient) UpdateGoods(ctx context.Context, in *CreateGoodsInfo, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Goods_UpdateGoods_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *goodsClient) GetGoodsDetail(ctx context.Context, in *GoodInfoRequest, opts ...grpc.CallOption) (*GoodsInfoResponse, error) {
	out := new(GoodsInfoResponse)
	err := c.cc.Invoke(ctx, Goods_GetGoodsDetail_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// GoodsServer is the server API for Goods service.
// All implementations must embed UnimplementedGoodsServer
// for forward compatibility
type GoodsServer interface {
	// 商品接口
	GoodsList(context.Context, *GoodsFilterRequest) (*GoodsListResponse, error)
	BatchGetGoods(context.Context, *BatchGoodsIdInfo) (*GoodsListResponse, error)
	CreateGoods(context.Context, *CreateGoodsInfo) (*GoodsInfoResponse, error)
	DeleteGoods(context.Context, *DeleteGoodsInfo) (*emptypb.Empty, error)
	UpdateGoods(context.Context, *CreateGoodsInfo) (*emptypb.Empty, error)
	GetGoodsDetail(context.Context, *GoodInfoRequest) (*GoodsInfoResponse, error)
	mustEmbedUnimplementedGoodsServer()
}

// UnimplementedGoodsServer must be embedded to have forward compatible implementations.
type UnimplementedGoodsServer struct {
}

func (UnimplementedGoodsServer) GoodsList(context.Context, *GoodsFilterRequest) (*GoodsListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GoodsList not implemented")
}
func (UnimplementedGoodsServer) BatchGetGoods(context.Context, *BatchGoodsIdInfo) (*GoodsListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method BatchGetGoods not implemented")
}
func (UnimplementedGoodsServer) CreateGoods(context.Context, *CreateGoodsInfo) (*GoodsInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateGoods not implemented")
}
func (UnimplementedGoodsServer) DeleteGoods(context.Context, *DeleteGoodsInfo) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteGoods not implemented")
}
func (UnimplementedGoodsServer) UpdateGoods(context.Context, *CreateGoodsInfo) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateGoods not implemented")
}
func (UnimplementedGoodsServer) GetGoodsDetail(context.Context, *GoodInfoRequest) (*GoodsInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetGoodsDetail not implemented")
}
func (UnimplementedGoodsServer) mustEmbedUnimplementedGoodsServer() {}

// UnsafeGoodsServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to GoodsServer will
// result in compilation errors.
type UnsafeGoodsServer interface {
	mustEmbedUnimplementedGoodsServer()
}

func RegisterGoodsServer(s grpc.ServiceRegistrar, srv GoodsServer) {
	s.RegisterService(&Goods_ServiceDesc, srv)
}

func _Goods_GoodsList_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GoodsFilterRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).GoodsList(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_GoodsList_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).GoodsList(ctx, req.(*GoodsFilterRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Goods_BatchGetGoods_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BatchGoodsIdInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).BatchGetGoods(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_BatchGetGoods_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).BatchGetGoods(ctx, req.(*BatchGoodsIdInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _Goods_CreateGoods_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CreateGoodsInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).CreateGoods(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_CreateGoods_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).CreateGoods(ctx, req.(*CreateGoodsInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _Goods_DeleteGoods_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(DeleteGoodsInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).DeleteGoods(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_DeleteGoods_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).DeleteGoods(ctx, req.(*DeleteGoodsInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _Goods_UpdateGoods_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CreateGoodsInfo)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).UpdateGoods(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_UpdateGoods_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).UpdateGoods(ctx, req.(*CreateGoodsInfo))
	}
	return interceptor(ctx, in, info, handler)
}

func _Goods_GetGoodsDetail_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GoodInfoRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(GoodsServer).GetGoodsDetail(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Goods_GetGoodsDetail_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(GoodsServer).GetGoodsDetail(ctx, req.(*GoodInfoRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Goods_ServiceDesc is the grpc.ServiceDesc for Goods service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Goods_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Goods",
	HandlerType: (*GoodsServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GoodsList",
			Handler:    _Goods_GoodsList_Handler,
		},
		{
			MethodName: "BatchGetGoods",
			Handler:    _Goods_BatchGetGoods_Handler,
		},
		{
			MethodName: "CreateGoods",
			Handler:    _Goods_CreateGoods_Handler,
		},
		{
			MethodName: "DeleteGoods",
			Handler:    _Goods_DeleteGoods_Handler,
		},
		{
			MethodName: "UpdateGoods",
			Handler:    _Goods_UpdateGoods_Handler,
		},
		{
			MethodName: "GetGoodsDetail",
			Handler:    _Goods_GetGoodsDetail_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "goods.proto",
}
