"""
This module contains auxiliary functions used in the whole app.
"""

def value(digit):
    """
    This function computes and returns the value of a digit (from a character to an integer).
    The digit is sure to be a correct one.
    :param digit: A character corresponding a digit in a certain base
    :return: The numeric value of the digit
    """
    if digit.isdigit():
        return ord(digit) - ord('0')
    else:
        return ord(digit) - ord('A') + 10 # If it's not a digit, then it sure is a digit in base 16


def char(digit):
    """
    This function computes and returns the character of a digit (from a value to a character).
    The digit is sure to be a correct one.
    :param digit: A value corresponding to a digit in a certain base
    :return: The character of the digit
    """
    if digit < 10:
        return chr(digit + ord('0'))
    else:
        return chr(digit + ord('A') - 10) # If it exceeds 9, then it sure is in base 16


def valid_base(p):
    """
    This functions verifies and returns if a base is valid.
    For this, the base must be one of: {2,3,4,5,6,7,8,9,16}
    :param p: The base
    :return: True if the base is valid, False otherwise
    """
    try:
        p = int(p)
    except ValueError:
        return False
    if p < 2: return False
    if 10 < p < 16: return False
    if p > 16: return False
    return True


def valid_number(p, number, digits_16):
    """
    This functions verifies and returns if a number in a certain base is valid.
    For this, it must be formed only with digits and those digits must be within the bound of the base.
    :param p: The base of the number
    :param number: The number
    :param digits_16: The digits of base 16 (as an auxiliary tool for verifying in case [p] is 16)
    :return: True if the number is valid, False otherwise
    """
    for digit in number:
        if (p <= 10 and ord(digit) - ord('0') >= p) or (p == 16 and not digits_16.count(digit)):
            return False
    return True


def greater_number(n1, n2):
    """
    This function verifies and returns which number is greater between two numbers [n1] and [n2].
    The number with the most digits is the bigger one.
    In case of equality, the digits are compared one by one from left to right until one is bigger.
    In case still of equality, the numbers are equal (but since we need one to be bigger, we will consider
    the first one to be that one).
    :param n1: The first number
    :param n2: The second number
    :return: 1 if the first number is bigger or equal than the second one, 2 otherwise
    """
    if len(n1) > len(n2):
        return 1
    if len(n2) > len(n1):
        return 2
    for i in range(0, len(n1)):
        if value(n1[i]) > value(n2[i]):
            return 1
        if value(n2[i]) > value(n1[i]):
            return 2
    return 1


def remove_leading_zeros(number):
    """
    This functions removes the leading zeros of a number.
    The number is given as a string.
    For this, we parse the string and remove a zero everytime we find it, until there are no more leading zeros.
    If the number is or becomes zero, we stop (since we need to have at least a digit in the number).
    :param number: The number (in string format)
    :return: The number without any leading zeros (in string format)
    """
    while len(number) > 1 and number[0] == '0':
        number = number[1:]
    return number
