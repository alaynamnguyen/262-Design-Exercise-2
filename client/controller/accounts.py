from .communication import build_and_send_task

def list_accounts(sock, wildcard):
    print("Calling list_accounts")
    response = build_and_send_task(sock, "list-accounts", wildcard=wildcard)

    if response["accounts"]:
        print("Accounts:", response["accounts"])
    
def delete_account(sock, uid):
    print("Calling delete_account")
    confirm = 'Y' == input("Type 'Y' to confirm deletion of your account: ")
    success = False
    if confirm:
        response = build_and_send_task(sock, "delete-account", uid=uid)
        # TODO handle the response here and return to login screen if successful
        print("Response:", response)
        success = response["success"]
    else:
        print("Deletion cancelled.")
    return success