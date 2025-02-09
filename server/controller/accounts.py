import fnmatch

def list_accounts(users_dict: dict, wildcard: str = "*"):
    """
    Lists all accounts in the accounts dictionary.

    Parameters:
    ----------
    users_dict : dict
        A dictionary of accounts.

    Returns:
    -------
    list
        A list of all active accounts.
    """
    accounts = [user.username for user in users_dict.values() if user.active]
    if wildcard:
        print("Wildcard:", wildcard, "Accounts:", accounts)
        accounts = fnmatch.filter(accounts, wildcard)
    return accounts

def delete_account(users_dict: dict, uid: str):
    print("Setting user as inactive in users_dict", uid)
    # Set user as inactive in users_dict
    users_dict[uid].active = False
    print("User statuses now:")
    for user in users_dict.keys():
        print(users_dict[user].username, "-->", users_dict[user].active)
    return True # success