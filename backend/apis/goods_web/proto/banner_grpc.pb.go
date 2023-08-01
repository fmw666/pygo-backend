// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v3.20.1
// source: banner.proto

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
	Banner_BannerList_FullMethodName   = "/Banner/BannerList"
	Banner_CreateBanner_FullMethodName = "/Banner/CreateBanner"
	Banner_DeleteBanner_FullMethodName = "/Banner/DeleteBanner"
	Banner_UpdateBanner_FullMethodName = "/Banner/UpdateBanner"
)

// BannerClient is the client API for Banner service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BannerClient interface {
	// 轮播图接口
	BannerList(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*BannerListResponse, error)
	CreateBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*BannerResponse, error)
	DeleteBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	UpdateBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
}

type bannerClient struct {
	cc grpc.ClientConnInterface
}

func NewBannerClient(cc grpc.ClientConnInterface) BannerClient {
	return &bannerClient{cc}
}

func (c *bannerClient) BannerList(ctx context.Context, in *emptypb.Empty, opts ...grpc.CallOption) (*BannerListResponse, error) {
	out := new(BannerListResponse)
	err := c.cc.Invoke(ctx, Banner_BannerList_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bannerClient) CreateBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*BannerResponse, error) {
	out := new(BannerResponse)
	err := c.cc.Invoke(ctx, Banner_CreateBanner_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bannerClient) DeleteBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Banner_DeleteBanner_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *bannerClient) UpdateBanner(ctx context.Context, in *BannerRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Banner_UpdateBanner_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BannerServer is the server API for Banner service.
// All implementations must embed UnimplementedBannerServer
// for forward compatibility
type BannerServer interface {
	// 轮播图接口
	BannerList(context.Context, *emptypb.Empty) (*BannerListResponse, error)
	CreateBanner(context.Context, *BannerRequest) (*BannerResponse, error)
	DeleteBanner(context.Context, *BannerRequest) (*emptypb.Empty, error)
	UpdateBanner(context.Context, *BannerRequest) (*emptypb.Empty, error)
	mustEmbedUnimplementedBannerServer()
}

// UnimplementedBannerServer must be embedded to have forward compatible implementations.
type UnimplementedBannerServer struct {
}

func (UnimplementedBannerServer) BannerList(context.Context, *emptypb.Empty) (*BannerListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method BannerList not implemented")
}
func (UnimplementedBannerServer) CreateBanner(context.Context, *BannerRequest) (*BannerResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateBanner not implemented")
}
func (UnimplementedBannerServer) DeleteBanner(context.Context, *BannerRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteBanner not implemented")
}
func (UnimplementedBannerServer) UpdateBanner(context.Context, *BannerRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateBanner not implemented")
}
func (UnimplementedBannerServer) mustEmbedUnimplementedBannerServer() {}

// UnsafeBannerServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to BannerServer will
// result in compilation errors.
type UnsafeBannerServer interface {
	mustEmbedUnimplementedBannerServer()
}

func RegisterBannerServer(s grpc.ServiceRegistrar, srv BannerServer) {
	s.RegisterService(&Banner_ServiceDesc, srv)
}

func _Banner_BannerList_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(emptypb.Empty)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BannerServer).BannerList(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Banner_BannerList_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BannerServer).BannerList(ctx, req.(*emptypb.Empty))
	}
	return interceptor(ctx, in, info, handler)
}

func _Banner_CreateBanner_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BannerRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BannerServer).CreateBanner(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Banner_CreateBanner_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BannerServer).CreateBanner(ctx, req.(*BannerRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Banner_DeleteBanner_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BannerRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BannerServer).DeleteBanner(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Banner_DeleteBanner_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BannerServer).DeleteBanner(ctx, req.(*BannerRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Banner_UpdateBanner_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BannerRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BannerServer).UpdateBanner(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Banner_UpdateBanner_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BannerServer).UpdateBanner(ctx, req.(*BannerRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Banner_ServiceDesc is the grpc.ServiceDesc for Banner service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Banner_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Banner",
	HandlerType: (*BannerServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "BannerList",
			Handler:    _Banner_BannerList_Handler,
		},
		{
			MethodName: "CreateBanner",
			Handler:    _Banner_CreateBanner_Handler,
		},
		{
			MethodName: "DeleteBanner",
			Handler:    _Banner_DeleteBanner_Handler,
		},
		{
			MethodName: "UpdateBanner",
			Handler:    _Banner_UpdateBanner_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "banner.proto",
}
