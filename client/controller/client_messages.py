from .communication import build_and_send_task

def delete_messages(sock, mids):
    print("Calling delete_messages")

    response = build_and_send_task(sock, "delete-messages", mids=mids)

    if response["success"]:
        print("Messages successfully deleted:", mids)
        # TODO: update UI to remove the deleted messages
        return
    else:
        print("Failed to delete messages.")
        return # UI does not change