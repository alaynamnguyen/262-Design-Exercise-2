import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.client_login import (
    check_username, login_user, create_account, cli_login
)
from utils import hash_password

# ---------------- FIXTURES ---------------- #

@pytest.fixture
def mock_socket():
    """
    Fixture to provide a mock socket object.
    """
    return Mock()

@pytest.fixture
def sample_response():
    """
    Fixture for a sample successful login response.
    """
    return {"login_success": True, "uid": "user123", "unread_messages": ["msg1", "msg2"]}

# ---------------- TESTS FOR check_username() ---------------- #

@patch("controller.client_login.build_and_send_task")
def test_check_username_exists(mock_build_and_send, mock_socket):
    """
    Test if check_username() correctly identifies an existing user.
    """
    mock_build_and_send.return_value = {"user_exists": True}
    
    result = check_username(mock_socket, "Alice", use_wire_protocol=False)

    mock_build_and_send.assert_called_once_with(mock_socket, "login-username", username="Alice", use_wire_protocol=False)
    assert result is True

@patch("controller.client_login.build_and_send_task")
def test_check_username_not_exists(mock_build_and_send, mock_socket):
    """
    Test if check_username() correctly identifies a non-existent user.
    """
    mock_build_and_send.return_value = {"user_exists": False}

    result = check_username(mock_socket, "NonExistentUser", use_wire_protocol=False)

    mock_build_and_send.assert_called_once_with(mock_socket, "login-username", username="NonExistentUser", use_wire_protocol=False)
    assert result is False

# ---------------- TESTS FOR login_user() ---------------- #

@patch("controller.client_login.build_and_send_task")
@patch("utils.hash_password", return_value="hashed_password123")
def test_login_user_failure(mock_hash_password, mock_build_and_send, mock_socket):
    """
    Test if login_user() correctly handles failed authentication.
    """
    mock_build_and_send.return_value = {"login_success": False}

    response = login_user(mock_socket, "Alice", "wrongpassword", use_wire_protocol=False)

    assert response == {"login_success": False}

# ---------------- TESTS FOR create_account() ---------------- #

@patch("controller.client_login.build_and_send_task")
@patch("utils.hash_password", return_value="hashed_password123")
def test_create_account_success(mock_hash_password, mock_build_and_send, mock_socket, sample_response):
    """
    Test if create_account() correctly creates a new user account.
    """
    mock_build_and_send.return_value = sample_response

    response = create_account(mock_socket, "NewUser", "newpass", use_wire_protocol=False)

    assert response == sample_response

@patch("controller.client_login.build_and_send_task")
@patch("utils.hash_password", return_value="hashed_password123")
def test_create_account_failure(mock_hash_password, mock_build_and_send, mock_socket):
    """
    Test if create_account() correctly handles failed account creation.
    """
    mock_build_and_send.return_value = {"login_success": False}

    response = create_account(mock_socket, "NewUser", "weakpass", use_wire_protocol=False)

    assert response == {"login_success": False}

# ---------------- TEST FOR cli_login() ---------------- #

@patch("builtins.input", side_effect=["Alice", "secure123"])  # Simulate user input
@patch("controller.client_login.check_username", return_value=True)
@patch("controller.client_login.login_user", return_value={"login_success": True, "uid": "user123", "unread_messages": []})
def test_cli_login_existing_user(mock_login_user, mock_check_username, mock_input, mock_socket):
    """
    Test if cli_login() successfully logs in an existing user.
    """
    uid = cli_login(mock_socket)

    mock_check_username.assert_called_once_with(mock_socket, "Alice")
    mock_login_user.assert_called_once_with(mock_socket, "Alice", "secure123")
    assert uid == "user123"

@patch("builtins.input", side_effect=["NewUser", "newpassword"])  # Simulate user input
@patch("controller.client_login.check_username", return_value=False)
@patch("controller.client_login.create_account", return_value={"login_success": True, "uid": "user123"})
def test_cli_login_new_user(mock_create_account, mock_check_username, mock_input, mock_socket):
    """
    Test if cli_login() successfully creates a new user.
    """
    uid = cli_login(mock_socket)

    mock_check_username.assert_called_once_with(mock_socket, "NewUser")
    mock_create_account.assert_called_once_with(mock_socket, "NewUser", "newpassword")
    assert uid == "user123"
