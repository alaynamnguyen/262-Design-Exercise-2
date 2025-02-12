import pytest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.communication import build_and_send_task

# ---------------- TESTS FOR build_and_send_task() ---------------- #

@patch("controller.communication.send_request")
@patch("controller.communication.receive_response")
def test_build_and_send_task_success(mock_receive_response, mock_send_request):
    """
    Test if build_and_send_task() successfully sends a task and receives a response.
    """
    mock_socket = Mock()
    mock_receive_response.return_value = {"success": True, "task": "test-task"}

    task = "test-task"
    use_wire_protocol = False
    additional_data = {"key1": "value1", "key2": "value2"}

    response = build_and_send_task(mock_socket, task, use_wire_protocol, **additional_data)

    expected_message = {"task": task, "key1": "value1", "key2": "value2"}

    # Check if send_request was called with the correct message
    mock_send_request.assert_called_once_with(mock_socket, expected_message, use_wire_protocol)

    # Check if receive_response was called once
    mock_receive_response.assert_called_once_with(mock_socket, use_wire_protocol)

    assert response == {"success": True, "task": "test-task"}  # Ensuring correct response

@patch("controller.communication.send_request")
@patch("controller.communication.receive_response")
def test_build_and_send_task_failure(mock_receive_response, mock_send_request):
    """
    Test if build_and_send_task() handles server failure response correctly.
    """
    mock_socket = Mock()
    mock_receive_response.return_value = {"success": False, "error": "Task failed"}

    task = "test-task"
    use_wire_protocol = False

    response = build_and_send_task(mock_socket, task, use_wire_protocol)

    expected_message = {"task": task}

    # Check if send_request was called with the correct message
    mock_send_request.assert_called_once_with(mock_socket, expected_message, use_wire_protocol)

    # Check if receive_response was called once
    mock_receive_response.assert_called_once_with(mock_socket, use_wire_protocol)

    assert response == {"success": False, "error": "Task failed"}  # Ensuring correct error handling
