# import pytest
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from controller.messages import (
#     send_message, delete_messages, mark_message_read,
#     get_message_by_mid, get_sent_messages_id, get_received_messages_id
# )
# from model.user import User
# from model.message import Message
# from unittest.mock import Mock

# import unittest
# import grpc
# from concurrent import futures
# import server_proto  # Import the gRPC server implementation
# import chat_pb2
# import chat_pb2_grpc

# class ServerProtoTests(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         """Set up a test gRPC server before running tests."""
#         cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
#         chat_pb2_grpc.add_ChatServiceServicer_to_server(server_proto.ChatService(), cls.server)
#         cls.port = "[::]:50052"  # Test on different port to avoid conflicts
#         cls.server.add_insecure_port(cls.port)
#         cls.server.start()

#         # Create a gRPC channel & stub for testing
#         cls.channel = grpc.insecure_channel(cls.port)
#         cls.stub = chat_pb2_grpc.ChatServiceStub(cls.channel)

#     @classmethod
#     def tearDownClass(cls):
#         """Stop the test server after all tests."""
#         cls.server.stop(None)

#     ## ----------- TEST LOGINUSERNAME ----------- ##
#     def test_login_username_existing(self):
#         """Test if username lookup works for an existing user."""
#         request = chat_pb2.LoginUsernameRequest(username="alice")
#         response = self.stub.LoginUsername(request)
#         self.assertTrue(response.user_exists)
#         self.assertEqual(response.username, "alice")

#     def test_login_username_not_existing(self):
#         """Test username lookup for a non-existent user."""
#         request = chat_pb2.LoginUsernameRequest(username="unknown_user")
#         response = self.stub.LoginUsername(request)
#         self.assertFalse(response.user_exists)
#         self.assertEqual(response.username, "unknown_user")

#     ## ----------- TEST LOGINPASSWORD ----------- ##
#     def test_login_password_correct(self):
#         """Test login with correct username and password."""
#         request = chat_pb2.LoginPasswordRequest(username="alice", password="valid_password")
#         response = self.stub.LoginPassword(request)
#         self.assertTrue(response.success)
#         self.assertNotEqual(response.uid, "")

#     def test_login_password_wrong(self):
#         """Test login with correct username but wrong password."""
#         request = chat_pb2.LoginPasswordRequest(username="alice", password="wrong_password")
#         response = self.stub.LoginPassword(request)
#         self.assertFalse(response.success)

#     def test_login_password_new_user(self):
#         """Test login with a new username (account should be created)."""
#         request = chat_pb2.LoginPasswordRequest(username="new_user", password="new_password")
#         response = self.stub.LoginPassword(request)
#         self.assertTrue(response.success)
#         self.assertNotEqual(response.uid, "")

#     ## ----------- TEST DELETE ACCOUNT ----------- ##
#     def test_delete_account_valid(self):
#         """Test deleting an existing user account."""
#         request = chat_pb2.DeleteAccountRequest(uid="existing_uid")
#         response = self.stub.DeleteAccount(request)
#         self.assertTrue(response.success)

#     def test_delete_account_invalid(self):
#         """Test deleting a non-existent user account."""
#         request = chat_pb2.DeleteAccountRequest(uid="invalid_uid")
#         response = self.stub.DeleteAccount(request)
#         self.assertFalse(response.success)

#     ## ----------- TEST GET RECEIVED MESSAGES ----------- ##
#     def test_get_received_messages_valid(self):
#         """Test retrieving received messages for an existing user."""
#         request = chat_pb2.GetMessagesRequest(uid="alice_uid")
#         response = self.stub.GetReceivedMessages(request)
#         self.assertIsInstance(response.mids, list)

#     def test_get_received_messages_no_messages(self):
#         """Test retrieving messages for a user with no received messages."""
#         request = chat_pb2.GetMessagesRequest(uid="bob_uid")
#         response = self.stub.GetReceivedMessages(request)
#         self.assertEqual(len(response.mids), 0)

#     ## ----------- TEST SEND MESSAGE ----------- ##
#     def test_send_message_valid(self):
#         """Test sending a message from one user to another."""
#         request = chat_pb2.SendMessageRequest(
#             sender="alice",
#             receiver_username="bob",
#             text="Hello, Bob!",
#             timestamp="2025-02-24 14:00:00"
#         )
#         response = self.stub.SendMessage(request)
#         self.assertTrue(response.success)

#     def test_send_message_invalid_sender(self):
#         """Test sending a message from a non-existent sender."""
#         request = chat_pb2.SendMessageRequest(
#             sender="invalid_user",
#             receiver_username="bob",
#             text="This should fail",
#             timestamp="2025-02-24 14:01:00"
#         )
#         response = self.stub.SendMessage(request)
#         self.assertFalse(response.success)

# if __name__ == '__main__':
#     unittest.main()
