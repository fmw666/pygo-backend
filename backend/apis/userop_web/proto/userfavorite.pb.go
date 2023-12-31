// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.31.0
// 	protoc        v3.20.1
// source: userfavorite.proto

package proto

import (
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	emptypb "google.golang.org/protobuf/types/known/emptypb"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type UserFavoriteRequest struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	UserId  int32 `protobuf:"varint,1,opt,name=userId,proto3" json:"userId,omitempty"`
	GoodsId int32 `protobuf:"varint,2,opt,name=goodsId,proto3" json:"goodsId,omitempty"`
}

func (x *UserFavoriteRequest) Reset() {
	*x = UserFavoriteRequest{}
	if protoimpl.UnsafeEnabled {
		mi := &file_userfavorite_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UserFavoriteRequest) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UserFavoriteRequest) ProtoMessage() {}

func (x *UserFavoriteRequest) ProtoReflect() protoreflect.Message {
	mi := &file_userfavorite_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UserFavoriteRequest.ProtoReflect.Descriptor instead.
func (*UserFavoriteRequest) Descriptor() ([]byte, []int) {
	return file_userfavorite_proto_rawDescGZIP(), []int{0}
}

func (x *UserFavoriteRequest) GetUserId() int32 {
	if x != nil {
		return x.UserId
	}
	return 0
}

func (x *UserFavoriteRequest) GetGoodsId() int32 {
	if x != nil {
		return x.GoodsId
	}
	return 0
}

type UserFavoriteResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	UserId  int32 `protobuf:"varint,1,opt,name=userId,proto3" json:"userId,omitempty"`
	GoodsId int32 `protobuf:"varint,2,opt,name=goodsId,proto3" json:"goodsId,omitempty"`
}

func (x *UserFavoriteResponse) Reset() {
	*x = UserFavoriteResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_userfavorite_proto_msgTypes[1]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UserFavoriteResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UserFavoriteResponse) ProtoMessage() {}

func (x *UserFavoriteResponse) ProtoReflect() protoreflect.Message {
	mi := &file_userfavorite_proto_msgTypes[1]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UserFavoriteResponse.ProtoReflect.Descriptor instead.
func (*UserFavoriteResponse) Descriptor() ([]byte, []int) {
	return file_userfavorite_proto_rawDescGZIP(), []int{1}
}

func (x *UserFavoriteResponse) GetUserId() int32 {
	if x != nil {
		return x.UserId
	}
	return 0
}

func (x *UserFavoriteResponse) GetGoodsId() int32 {
	if x != nil {
		return x.GoodsId
	}
	return 0
}

type UserFavoriteListResponse struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	Total int32                   `protobuf:"varint,1,opt,name=total,proto3" json:"total,omitempty"`
	Data  []*UserFavoriteResponse `protobuf:"bytes,2,rep,name=data,proto3" json:"data,omitempty"`
}

func (x *UserFavoriteListResponse) Reset() {
	*x = UserFavoriteListResponse{}
	if protoimpl.UnsafeEnabled {
		mi := &file_userfavorite_proto_msgTypes[2]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *UserFavoriteListResponse) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*UserFavoriteListResponse) ProtoMessage() {}

func (x *UserFavoriteListResponse) ProtoReflect() protoreflect.Message {
	mi := &file_userfavorite_proto_msgTypes[2]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use UserFavoriteListResponse.ProtoReflect.Descriptor instead.
func (*UserFavoriteListResponse) Descriptor() ([]byte, []int) {
	return file_userfavorite_proto_rawDescGZIP(), []int{2}
}

func (x *UserFavoriteListResponse) GetTotal() int32 {
	if x != nil {
		return x.Total
	}
	return 0
}

func (x *UserFavoriteListResponse) GetData() []*UserFavoriteResponse {
	if x != nil {
		return x.Data
	}
	return nil
}

var File_userfavorite_proto protoreflect.FileDescriptor

var file_userfavorite_proto_rawDesc = []byte{
	0x0a, 0x12, 0x75, 0x73, 0x65, 0x72, 0x66, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x2e, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x1a, 0x1b, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2f, 0x70, 0x72, 0x6f,
	0x74, 0x6f, 0x62, 0x75, 0x66, 0x2f, 0x65, 0x6d, 0x70, 0x74, 0x79, 0x2e, 0x70, 0x72, 0x6f, 0x74,
	0x6f, 0x22, 0x47, 0x0a, 0x13, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74,
	0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x12, 0x16, 0x0a, 0x06, 0x75, 0x73, 0x65, 0x72,
	0x49, 0x64, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52, 0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64,
	0x12, 0x18, 0x0a, 0x07, 0x67, 0x6f, 0x6f, 0x64, 0x73, 0x49, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28,
	0x05, 0x52, 0x07, 0x67, 0x6f, 0x6f, 0x64, 0x73, 0x49, 0x64, 0x22, 0x48, 0x0a, 0x14, 0x55, 0x73,
	0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e,
	0x73, 0x65, 0x12, 0x16, 0x0a, 0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64, 0x18, 0x01, 0x20, 0x01,
	0x28, 0x05, 0x52, 0x06, 0x75, 0x73, 0x65, 0x72, 0x49, 0x64, 0x12, 0x18, 0x0a, 0x07, 0x67, 0x6f,
	0x6f, 0x64, 0x73, 0x49, 0x64, 0x18, 0x02, 0x20, 0x01, 0x28, 0x05, 0x52, 0x07, 0x67, 0x6f, 0x6f,
	0x64, 0x73, 0x49, 0x64, 0x22, 0x5b, 0x0a, 0x18, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f,
	0x72, 0x69, 0x74, 0x65, 0x4c, 0x69, 0x73, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65,
	0x12, 0x14, 0x0a, 0x05, 0x74, 0x6f, 0x74, 0x61, 0x6c, 0x18, 0x01, 0x20, 0x01, 0x28, 0x05, 0x52,
	0x05, 0x74, 0x6f, 0x74, 0x61, 0x6c, 0x12, 0x29, 0x0a, 0x04, 0x64, 0x61, 0x74, 0x61, 0x18, 0x02,
	0x20, 0x03, 0x28, 0x0b, 0x32, 0x15, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72,
	0x69, 0x74, 0x65, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x52, 0x04, 0x64, 0x61, 0x74,
	0x61, 0x32, 0xa5, 0x02, 0x0a, 0x0c, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69,
	0x74, 0x65, 0x12, 0x46, 0x0a, 0x13, 0x47, 0x65, 0x74, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76,
	0x6f, 0x72, 0x69, 0x74, 0x65, 0x4c, 0x69, 0x73, 0x74, 0x12, 0x14, 0x2e, 0x55, 0x73, 0x65, 0x72,
	0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a,
	0x19, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x4c, 0x69,
	0x73, 0x74, 0x52, 0x65, 0x73, 0x70, 0x6f, 0x6e, 0x73, 0x65, 0x12, 0x45, 0x0a, 0x15, 0x47, 0x65,
	0x74, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x44, 0x65, 0x74,
	0x61, 0x69, 0x6c, 0x12, 0x14, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69,
	0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x16, 0x2e, 0x67, 0x6f, 0x6f, 0x67,
	0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e, 0x45, 0x6d, 0x70, 0x74,
	0x79, 0x12, 0x42, 0x0a, 0x12, 0x43, 0x72, 0x65, 0x61, 0x74, 0x65, 0x55, 0x73, 0x65, 0x72, 0x46,
	0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x12, 0x14, 0x2e, 0x55, 0x73, 0x65, 0x72, 0x46, 0x61,
	0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73, 0x74, 0x1a, 0x16, 0x2e,
	0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x62, 0x75, 0x66, 0x2e,
	0x45, 0x6d, 0x70, 0x74, 0x79, 0x12, 0x42, 0x0a, 0x12, 0x44, 0x65, 0x6c, 0x65, 0x74, 0x65, 0x55,
	0x73, 0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x12, 0x14, 0x2e, 0x55, 0x73,
	0x65, 0x72, 0x46, 0x61, 0x76, 0x6f, 0x72, 0x69, 0x74, 0x65, 0x52, 0x65, 0x71, 0x75, 0x65, 0x73,
	0x74, 0x1a, 0x16, 0x2e, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f,
	0x62, 0x75, 0x66, 0x2e, 0x45, 0x6d, 0x70, 0x74, 0x79, 0x42, 0x09, 0x5a, 0x07, 0x2e, 0x3b, 0x70,
	0x72, 0x6f, 0x74, 0x6f, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_userfavorite_proto_rawDescOnce sync.Once
	file_userfavorite_proto_rawDescData = file_userfavorite_proto_rawDesc
)

func file_userfavorite_proto_rawDescGZIP() []byte {
	file_userfavorite_proto_rawDescOnce.Do(func() {
		file_userfavorite_proto_rawDescData = protoimpl.X.CompressGZIP(file_userfavorite_proto_rawDescData)
	})
	return file_userfavorite_proto_rawDescData
}

var file_userfavorite_proto_msgTypes = make([]protoimpl.MessageInfo, 3)
var file_userfavorite_proto_goTypes = []interface{}{
	(*UserFavoriteRequest)(nil),      // 0: UserFavoriteRequest
	(*UserFavoriteResponse)(nil),     // 1: UserFavoriteResponse
	(*UserFavoriteListResponse)(nil), // 2: UserFavoriteListResponse
	(*emptypb.Empty)(nil),            // 3: google.protobuf.Empty
}
var file_userfavorite_proto_depIdxs = []int32{
	1, // 0: UserFavoriteListResponse.data:type_name -> UserFavoriteResponse
	0, // 1: UserFavorite.GetUserFavoriteList:input_type -> UserFavoriteRequest
	0, // 2: UserFavorite.GetUserFavoriteDetail:input_type -> UserFavoriteRequest
	0, // 3: UserFavorite.CreateUserFavorite:input_type -> UserFavoriteRequest
	0, // 4: UserFavorite.DeleteUserFavorite:input_type -> UserFavoriteRequest
	2, // 5: UserFavorite.GetUserFavoriteList:output_type -> UserFavoriteListResponse
	3, // 6: UserFavorite.GetUserFavoriteDetail:output_type -> google.protobuf.Empty
	3, // 7: UserFavorite.CreateUserFavorite:output_type -> google.protobuf.Empty
	3, // 8: UserFavorite.DeleteUserFavorite:output_type -> google.protobuf.Empty
	5, // [5:9] is the sub-list for method output_type
	1, // [1:5] is the sub-list for method input_type
	1, // [1:1] is the sub-list for extension type_name
	1, // [1:1] is the sub-list for extension extendee
	0, // [0:1] is the sub-list for field type_name
}

func init() { file_userfavorite_proto_init() }
func file_userfavorite_proto_init() {
	if File_userfavorite_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_userfavorite_proto_msgTypes[0].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UserFavoriteRequest); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_userfavorite_proto_msgTypes[1].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UserFavoriteResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
		file_userfavorite_proto_msgTypes[2].Exporter = func(v interface{}, i int) interface{} {
			switch v := v.(*UserFavoriteListResponse); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_userfavorite_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   3,
			NumExtensions: 0,
			NumServices:   1,
		},
		GoTypes:           file_userfavorite_proto_goTypes,
		DependencyIndexes: file_userfavorite_proto_depIdxs,
		MessageInfos:      file_userfavorite_proto_msgTypes,
	}.Build()
	File_userfavorite_proto = out.File
	file_userfavorite_proto_rawDesc = nil
	file_userfavorite_proto_goTypes = nil
	file_userfavorite_proto_depIdxs = nil
}
