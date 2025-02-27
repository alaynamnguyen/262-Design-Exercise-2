# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: Chat.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'Chat.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nChat.proto\x12\x04\x63hat\"(\n\x14LoginUsernameRequest\x12\x10\n\x08username\x18\x01 \x01(\t\">\n\x15LoginUsernameResponse\x12\x13\n\x0buser_exists\x18\x01 \x01(\x08\x12\x10\n\x08username\x18\x02 \x01(\t\":\n\x14LoginPasswordRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"5\n\x15LoginPasswordResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0b\n\x03uid\x18\x02 \x01(\t\"#\n\x14\x44\x65leteAccountRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\"(\n\x15\x44\x65leteAccountResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\'\n\x13ListAccountsRequest\x12\x10\n\x08wildcard\x18\x01 \x01(\t\"(\n\x14ListAccountsResponse\x12\x10\n\x08\x61\x63\x63ounts\x18\x01 \x03(\t\"`\n\x12SendMessageRequest\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x19\n\x11receiver_username\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\"&\n\x13SendMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"!\n\x12GetMessagesRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\"#\n\x13GetMessagesResponse\x12\x0c\n\x04mids\x18\x01 \x03(\t\" \n\x11GetMessageRequest\x12\x0b\n\x03mid\x18\x01 \x01(\t\"\xaa\x01\n\x12GetMessageResponse\x12\x12\n\nsender_uid\x18\x01 \x01(\t\x12\x14\n\x0creceiver_uid\x18\x02 \x01(\t\x12\x17\n\x0fsender_username\x18\x03 \x01(\t\x12\x19\n\x11receiver_username\x18\x04 \x01(\t\x12\x0c\n\x04text\x18\x05 \x01(\t\x12\x11\n\ttimestamp\x18\x06 \x01(\t\x12\x15\n\rreceiver_read\x18\x07 \x01(\x08\"%\n\x16MarkMessageReadRequest\x12\x0b\n\x03mid\x18\x01 \x01(\t\"*\n\x17MarkMessageReadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"2\n\x15\x44\x65leteMessagesRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x0c\n\x04mids\x18\x02 \x03(\t\")\n\x16\x44\x65leteMessagesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xed\x05\n\x0b\x43hatService\x12H\n\rLoginUsername\x12\x1a.chat.LoginUsernameRequest\x1a\x1b.chat.LoginUsernameResponse\x12H\n\rLoginPassword\x12\x1a.chat.LoginPasswordRequest\x1a\x1b.chat.LoginPasswordResponse\x12H\n\rDeleteAccount\x12\x1a.chat.DeleteAccountRequest\x1a\x1b.chat.DeleteAccountResponse\x12\x45\n\x0cListAccounts\x12\x19.chat.ListAccountsRequest\x1a\x1a.chat.ListAccountsResponse\x12\x42\n\x0bSendMessage\x12\x18.chat.SendMessageRequest\x1a\x19.chat.SendMessageResponse\x12\x46\n\x0fGetSentMessages\x12\x18.chat.GetMessagesRequest\x1a\x19.chat.GetMessagesResponse\x12J\n\x13GetReceivedMessages\x12\x18.chat.GetMessagesRequest\x1a\x19.chat.GetMessagesResponse\x12\x44\n\x0fGetMessageByMid\x12\x17.chat.GetMessageRequest\x1a\x18.chat.GetMessageResponse\x12N\n\x0fMarkMessageRead\x12\x1c.chat.MarkMessageReadRequest\x1a\x1d.chat.MarkMessageReadResponse\x12K\n\x0e\x44\x65leteMessages\x12\x1b.chat.DeleteMessagesRequest\x1a\x1c.chat.DeleteMessagesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Chat_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGINUSERNAMEREQUEST']._serialized_start=20
  _globals['_LOGINUSERNAMEREQUEST']._serialized_end=60
  _globals['_LOGINUSERNAMERESPONSE']._serialized_start=62
  _globals['_LOGINUSERNAMERESPONSE']._serialized_end=124
  _globals['_LOGINPASSWORDREQUEST']._serialized_start=126
  _globals['_LOGINPASSWORDREQUEST']._serialized_end=184
  _globals['_LOGINPASSWORDRESPONSE']._serialized_start=186
  _globals['_LOGINPASSWORDRESPONSE']._serialized_end=239
  _globals['_DELETEACCOUNTREQUEST']._serialized_start=241
  _globals['_DELETEACCOUNTREQUEST']._serialized_end=276
  _globals['_DELETEACCOUNTRESPONSE']._serialized_start=278
  _globals['_DELETEACCOUNTRESPONSE']._serialized_end=318
  _globals['_LISTACCOUNTSREQUEST']._serialized_start=320
  _globals['_LISTACCOUNTSREQUEST']._serialized_end=359
  _globals['_LISTACCOUNTSRESPONSE']._serialized_start=361
  _globals['_LISTACCOUNTSRESPONSE']._serialized_end=401
  _globals['_SENDMESSAGEREQUEST']._serialized_start=403
  _globals['_SENDMESSAGEREQUEST']._serialized_end=499
  _globals['_SENDMESSAGERESPONSE']._serialized_start=501
  _globals['_SENDMESSAGERESPONSE']._serialized_end=539
  _globals['_GETMESSAGESREQUEST']._serialized_start=541
  _globals['_GETMESSAGESREQUEST']._serialized_end=574
  _globals['_GETMESSAGESRESPONSE']._serialized_start=576
  _globals['_GETMESSAGESRESPONSE']._serialized_end=611
  _globals['_GETMESSAGEREQUEST']._serialized_start=613
  _globals['_GETMESSAGEREQUEST']._serialized_end=645
  _globals['_GETMESSAGERESPONSE']._serialized_start=648
  _globals['_GETMESSAGERESPONSE']._serialized_end=818
  _globals['_MARKMESSAGEREADREQUEST']._serialized_start=820
  _globals['_MARKMESSAGEREADREQUEST']._serialized_end=857
  _globals['_MARKMESSAGEREADRESPONSE']._serialized_start=859
  _globals['_MARKMESSAGEREADRESPONSE']._serialized_end=901
  _globals['_DELETEMESSAGESREQUEST']._serialized_start=903
  _globals['_DELETEMESSAGESREQUEST']._serialized_end=953
  _globals['_DELETEMESSAGESRESPONSE']._serialized_start=955
  _globals['_DELETEMESSAGESRESPONSE']._serialized_end=996
  _globals['_CHATSERVICE']._serialized_start=999
  _globals['_CHATSERVICE']._serialized_end=1748
# @@protoc_insertion_point(module_scope)
