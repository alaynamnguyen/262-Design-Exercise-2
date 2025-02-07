import fnmatch

def list_accounts(accounts_dict: dict, wildcard: str = "*"):
    """
    Lists all accounts in the accounts dictionary.

    Parameters:
    ----------
    accounts_dict : dict
        A dictionary of accounts.

    Returns:
    -------
    list
        A list of all accounts.
    """
    accounts = [account['username'] for account in accounts_dict.values()]
    if wildcard:
        accounts = fnmatch.filter(accounts, wildcard)
    return accounts