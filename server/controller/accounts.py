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
        A list of all accounts.
    """
    accounts = [user.username for user in users_dict.values()]
    if wildcard:
        print("Wildcard:", wildcard, "Accounts:", accounts)
        accounts = fnmatch.filter(accounts, wildcard)
    return accounts