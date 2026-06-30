"""
Palindrome checker module.

Returns a dict with:
  - is_palindrome (bool): Whether cleaned string is a palindrome
  - cleaned (str): The input after removing non-alphanumeric characters
"""


def is_palindrome(text):
    """
    Check if input is a palindrome (case-sensitive, after cleaning).
    
    Args:
        text: String to check (or any type - returns False if invalid)
    
    Returns:
        dict: {"is_palindrome": bool, "cleaned": str}
    """
    # Handle invalid inputs
    if not isinstance(text, str):
        return {"is_palindrome": False, "cleaned": ""}
    
    # Clean: keep only alphanumeric characters
    cleaned = "".join(char for char in text if char.isalnum())
    
    # Check if palindrome
    is_pal = cleaned == cleaned[::-1]
    
    return {"is_palindrome": is_pal, "cleaned": cleaned}
