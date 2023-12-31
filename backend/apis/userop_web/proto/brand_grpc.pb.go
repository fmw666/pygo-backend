// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.3.0
// - protoc             v3.20.1
// source: brand.proto

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
	Brand_BrandList_FullMethodName            = "/Brand/BrandList"
	Brand_CreateBrand_FullMethodName          = "/Brand/CreateBrand"
	Brand_DeleteBrand_FullMethodName          = "/Brand/DeleteBrand"
	Brand_UpdateBrand_FullMethodName          = "/Brand/UpdateBrand"
	Brand_CategoryBrandList_FullMethodName    = "/Brand/CategoryBrandList"
	Brand_GetCategoryBrandList_FullMethodName = "/Brand/GetCategoryBrandList"
	Brand_CreateCategoryBrand_FullMethodName  = "/Brand/CreateCategoryBrand"
	Brand_DeleteCategoryBrand_FullMethodName  = "/Brand/DeleteCategoryBrand"
	Brand_UpdateCategoryBrand_FullMethodName  = "/Brand/UpdateCategoryBrand"
)

// BrandClient is the client API for Brand service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type BrandClient interface {
	// 品牌接口
	BrandList(ctx context.Context, in *BrandFilterRequest, opts ...grpc.CallOption) (*BrandListResponse, error)
	CreateBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*BrandInfoResponse, error)
	DeleteBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	UpdateBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	CategoryBrandList(ctx context.Context, in *CategoryBrandFilterRequest, opts ...grpc.CallOption) (*CategoryBrandListResponse, error)
	GetCategoryBrandList(ctx context.Context, in *CategoryInfoRequest, opts ...grpc.CallOption) (*BrandListResponse, error)
	CreateCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*CategoryBrandResponse, error)
	DeleteCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
	UpdateCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error)
}

type brandClient struct {
	cc grpc.ClientConnInterface
}

func NewBrandClient(cc grpc.ClientConnInterface) BrandClient {
	return &brandClient{cc}
}

func (c *brandClient) BrandList(ctx context.Context, in *BrandFilterRequest, opts ...grpc.CallOption) (*BrandListResponse, error) {
	out := new(BrandListResponse)
	err := c.cc.Invoke(ctx, Brand_BrandList_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) CreateBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*BrandInfoResponse, error) {
	out := new(BrandInfoResponse)
	err := c.cc.Invoke(ctx, Brand_CreateBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) DeleteBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Brand_DeleteBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) UpdateBrand(ctx context.Context, in *BrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Brand_UpdateBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) CategoryBrandList(ctx context.Context, in *CategoryBrandFilterRequest, opts ...grpc.CallOption) (*CategoryBrandListResponse, error) {
	out := new(CategoryBrandListResponse)
	err := c.cc.Invoke(ctx, Brand_CategoryBrandList_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) GetCategoryBrandList(ctx context.Context, in *CategoryInfoRequest, opts ...grpc.CallOption) (*BrandListResponse, error) {
	out := new(BrandListResponse)
	err := c.cc.Invoke(ctx, Brand_GetCategoryBrandList_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) CreateCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*CategoryBrandResponse, error) {
	out := new(CategoryBrandResponse)
	err := c.cc.Invoke(ctx, Brand_CreateCategoryBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) DeleteCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Brand_DeleteCategoryBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *brandClient) UpdateCategoryBrand(ctx context.Context, in *CategoryBrandRequest, opts ...grpc.CallOption) (*emptypb.Empty, error) {
	out := new(emptypb.Empty)
	err := c.cc.Invoke(ctx, Brand_UpdateCategoryBrand_FullMethodName, in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// BrandServer is the server API for Brand service.
// All implementations must embed UnimplementedBrandServer
// for forward compatibility
type BrandServer interface {
	// 品牌接口
	BrandList(context.Context, *BrandFilterRequest) (*BrandListResponse, error)
	CreateBrand(context.Context, *BrandRequest) (*BrandInfoResponse, error)
	DeleteBrand(context.Context, *BrandRequest) (*emptypb.Empty, error)
	UpdateBrand(context.Context, *BrandRequest) (*emptypb.Empty, error)
	CategoryBrandList(context.Context, *CategoryBrandFilterRequest) (*CategoryBrandListResponse, error)
	GetCategoryBrandList(context.Context, *CategoryInfoRequest) (*BrandListResponse, error)
	CreateCategoryBrand(context.Context, *CategoryBrandRequest) (*CategoryBrandResponse, error)
	DeleteCategoryBrand(context.Context, *CategoryBrandRequest) (*emptypb.Empty, error)
	UpdateCategoryBrand(context.Context, *CategoryBrandRequest) (*emptypb.Empty, error)
	mustEmbedUnimplementedBrandServer()
}

// UnimplementedBrandServer must be embedded to have forward compatible implementations.
type UnimplementedBrandServer struct {
}

func (UnimplementedBrandServer) BrandList(context.Context, *BrandFilterRequest) (*BrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method BrandList not implemented")
}
func (UnimplementedBrandServer) CreateBrand(context.Context, *BrandRequest) (*BrandInfoResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateBrand not implemented")
}
func (UnimplementedBrandServer) DeleteBrand(context.Context, *BrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteBrand not implemented")
}
func (UnimplementedBrandServer) UpdateBrand(context.Context, *BrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateBrand not implemented")
}
func (UnimplementedBrandServer) CategoryBrandList(context.Context, *CategoryBrandFilterRequest) (*CategoryBrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CategoryBrandList not implemented")
}
func (UnimplementedBrandServer) GetCategoryBrandList(context.Context, *CategoryInfoRequest) (*BrandListResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetCategoryBrandList not implemented")
}
func (UnimplementedBrandServer) CreateCategoryBrand(context.Context, *CategoryBrandRequest) (*CategoryBrandResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method CreateCategoryBrand not implemented")
}
func (UnimplementedBrandServer) DeleteCategoryBrand(context.Context, *CategoryBrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method DeleteCategoryBrand not implemented")
}
func (UnimplementedBrandServer) UpdateCategoryBrand(context.Context, *CategoryBrandRequest) (*emptypb.Empty, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateCategoryBrand not implemented")
}
func (UnimplementedBrandServer) mustEmbedUnimplementedBrandServer() {}

// UnsafeBrandServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to BrandServer will
// result in compilation errors.
type UnsafeBrandServer interface {
	mustEmbedUnimplementedBrandServer()
}

func RegisterBrandServer(s grpc.ServiceRegistrar, srv BrandServer) {
	s.RegisterService(&Brand_ServiceDesc, srv)
}

func _Brand_BrandList_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BrandFilterRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).BrandList(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_BrandList_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).BrandList(ctx, req.(*BrandFilterRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_CreateBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).CreateBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_CreateBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).CreateBrand(ctx, req.(*BrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_DeleteBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).DeleteBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_DeleteBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).DeleteBrand(ctx, req.(*BrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_UpdateBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(BrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).UpdateBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_UpdateBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).UpdateBrand(ctx, req.(*BrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_CategoryBrandList_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CategoryBrandFilterRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).CategoryBrandList(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_CategoryBrandList_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).CategoryBrandList(ctx, req.(*CategoryBrandFilterRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_GetCategoryBrandList_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CategoryInfoRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).GetCategoryBrandList(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_GetCategoryBrandList_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).GetCategoryBrandList(ctx, req.(*CategoryInfoRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_CreateCategoryBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CategoryBrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).CreateCategoryBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_CreateCategoryBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).CreateCategoryBrand(ctx, req.(*CategoryBrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_DeleteCategoryBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CategoryBrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).DeleteCategoryBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_DeleteCategoryBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).DeleteCategoryBrand(ctx, req.(*CategoryBrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _Brand_UpdateCategoryBrand_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CategoryBrandRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(BrandServer).UpdateCategoryBrand(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: Brand_UpdateCategoryBrand_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(BrandServer).UpdateCategoryBrand(ctx, req.(*CategoryBrandRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Brand_ServiceDesc is the grpc.ServiceDesc for Brand service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Brand_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "Brand",
	HandlerType: (*BrandServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "BrandList",
			Handler:    _Brand_BrandList_Handler,
		},
		{
			MethodName: "CreateBrand",
			Handler:    _Brand_CreateBrand_Handler,
		},
		{
			MethodName: "DeleteBrand",
			Handler:    _Brand_DeleteBrand_Handler,
		},
		{
			MethodName: "UpdateBrand",
			Handler:    _Brand_UpdateBrand_Handler,
		},
		{
			MethodName: "CategoryBrandList",
			Handler:    _Brand_CategoryBrandList_Handler,
		},
		{
			MethodName: "GetCategoryBrandList",
			Handler:    _Brand_GetCategoryBrandList_Handler,
		},
		{
			MethodName: "CreateCategoryBrand",
			Handler:    _Brand_CreateCategoryBrand_Handler,
		},
		{
			MethodName: "DeleteCategoryBrand",
			Handler:    _Brand_DeleteCategoryBrand_Handler,
		},
		{
			MethodName: "UpdateCategoryBrand",
			Handler:    _Brand_UpdateCategoryBrand_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "brand.proto",
}
