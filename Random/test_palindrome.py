"""
Test suite for palindrome.py
TDD: Write tests FIRST, then code.
"""

import pytest
from palindrome import is_palindrome


class TestBasicPalindrome:
    """Task 1: Core palindrome logic"""
    
    def test_basic_palindrome(self):
        """Simple palindrome check"""
        result = is_palindrome("racecar")
        assert result["is_palindrome"] is True
        assert result["cleaned"] == "racecar"
    
    def test_non_palindrome(self):
        """Non-palindrome should return False"""
        result = is_palindrome("hello")
        assert result["is_palindrome"] is False
        assert result["cleaned"] == "hello"
    
    def test_single_char(self):
        """Single character is always a palindrome"""
        result = is_palindrome("a")
        assert result["is_palindrome"] is True


class TestInputCleaning:
    """Task 2: Strip non-alphanumeric characters"""
    
    def test_strip_spaces(self):
        """Remove spaces before checking"""
        result = is_palindrome("race car")
        assert result["is_palindrome"] is True
        assert result["cleaned"] == "racecar"
    
    def test_strip_punctuation(self):
        """Remove punctuation and spaces"""
        result = is_palindrome("A man, a plan, a canal: Panama")
        assert result["is_palindrome"] is False  # Case-sensitive!
        assert "amanaplanacanalpanama" in result["cleaned"]
    
    def test_strip_mixed(self):
        """Remove mixed punctuation and spaces"""
        result = is_palindrome("Madam, I'm Adam")
        assert result["is_palindrome"] is False  # Case-sensitive
        assert result["cleaned"] == "madamimadam"


class TestInvalidInputs:
    """Task 3: Handle edge cases gracefully"""
    
    def test_none_input(self):
        """None should return False, not crash"""
        result = is_palindrome(None)
        assert result["is_palindrome"] is False
        assert result["cleaned"] == ""
    
    def test_empty_string(self):
        """Empty string is technically a palindrome"""
        result = is_palindrome("")
        assert result["is_palindrome"] is True
        assert result["cleaned"] == ""
    
    def test_integer_input(self):
        """Integer should return False gracefully"""
        result = is_palindrome(12345)
        assert result["is_palindrome"] is False
    
    def test_only_special_chars(self):
        """String with only punctuation becomes empty after cleaning"""
        result = is_palindrome("!@#$%")
        assert result["is_palindrome"] is True
        assert result["cleaned"] == ""


class TestOutputFormat:
    """Task 4: Verify dict structure"""
    
    def test_output_is_dict(self):
        """Result must be a dictionary"""
        result = is_palindrome("test")
        assert isinstance(result, dict)
    
    def test_required_keys(self):
        """Result must have correct keys"""
        result = is_palindrome("test")
        assert "is_palindrome" in result
        assert "cleaned" in result
        assert len(result) == 2  # No extra keys
    
    def test_value_types(self):
        """Values must be correct types"""
        result = is_palindrome("test")
        assert isinstance(result["is_palindrome"], bool)
        assert isinstance(result["cleaned"], str)
