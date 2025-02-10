from .communication import build_and_send_task

def delete_messages(sock, mids):
    print("Calling delete_messages")
    response = build_and_send_task(sock, "delete-messages", mids=mids)

    if response["success"]:
        deleted_mids = response["deleted-mids"]
        print("Messages successfully deleted:", deleted_mids)
        # TODO: update UI to remove the deleted messages
        return
    else:
        print("Failed to delete messages.")
        return # UI does not change
    
def mark_message_read(sock, mid):
    print("Calling mark_message_read")
    response = build_and_send_task(sock, "mark-message-read", mid=mid)

    if response["success"]:
        print("Message marked as read.")