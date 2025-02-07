from .communication import build_and_send_task

def list_accounts(sock, wildcard):
    print("Calling list_accounts")
    response = build_and_send_task(sock, "list-accounts", wildcard=wildcard)

    if response["accounts"]:
        print("Accounts:", response["accounts"])
        return