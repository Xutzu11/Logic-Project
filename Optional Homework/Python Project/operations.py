"""
This module contains the operations parts, functions that do arithmetic operations in a certain
base with positive integers.
"""

from functions import value
from functions import char
from functions import greater_number
from functions import remove_leading_zeros


def addition(p, n1, n2):
    """
    This functions performs the addition between two positive integers [n1] and [n2]
    in a certain base [p], and returns the result.
    For this, the addition is performed from right to left:
    1. The two digits are added together (the digit for a number with no more digits is considered zero),
    and also add the carry (if it exists) from the previous addition.
    2. The modulo base [p] is kept as the digit for that position, and we also take into account
    the carry for the next digit addition.
    :param p: The base of the numbers
    :param n1: The first number
    :param n2: The second number
    :return: The result from adding the two numbers
    """
    result = ""
    n1 = n1[::-1]  # Reverse the numbers so that we can do addition from right to left
    n2 = n2[::-1]
    max_length = max(len(n1), len(n2))
    carry = 0
    for i in range(0, max_length):
        if i < len(n1):
            digit_1 = n1[i]
        else:
            digit_1 = '0'  # If a number has no more digits, we consider it to have leading zeros (as many as we need)
        if i < len(n2):
            digit_2 = n2[i]
        else:
            digit_2 = '0'
        partial_result = value(digit_1) + value(digit_2) + carry  # The current addition
        remainder = partial_result % p  # We keep the current digit
        carry = partial_result >= p  # We also take into account the carry (which cannot exceed 1)
        result += char(remainder)
    if carry:
        result += '1'  # At the end, we may still have a carry, which we need to add to the number
    result = result[::-1]  # We reverse the result (since we built it from right to left)
    return result


def subtraction(p, n1, n2):
    """
    This function performs the subtraction between two numbers [n1] and [n2] in a certain base [p],
    and returns the result.
    For this, we perform the subtraction that is easier to do, subtracting the smaller number
    from the bigger number. If the order is reversed, we add a minus sign at the result.
    The subtraction is performed from right to left:
    1. The digits are subtracted one from the other (if the second number has no more digits,
    we consider it to be zero), and also subtract the carry (if it exists) from the previous subtraction.
    2. If it is positive, we have our current digit. If not, we add the base (being a carry from the
    next subtraction) and now we have our digit (the negative number cannot exceed the base, so after
    adding the base we are sure to have something not negative).
    :param p: The base of the numbers
    :param n1: The first number
    :param n2: The second number
    :return: The result of the subtraction
    """
    neg = 0
    if greater_number(n1, n2) == 2:  # If the second number is bigger, we swap them
        n1, n2 = n2, n1
        neg = 1  # The final result will be negative
    result = ""
    n1 = n1[::-1]  # We reverse the numbers, since we parse from right to left
    n2 = n2[::-1]
    carry = 0
    for i in range(0, len(n1)):
        digit_1 = n1[i]
        if i < len(n2):
            digit_2 = n2[i]
        else:
            digit_2 = '0'  # If there are no more digits, we consider that digit to be zero
        partial_result = value(digit_1) - value(digit_2) - carry
        carry = 0
        if partial_result < 0:
            carry = 1  # The carry will be 1 if we need to borrow
            partial_result += p
        result += char(partial_result)
    result = result[::-1]
    result = remove_leading_zeros(result)  # We may have leading zeros, which we remove
    if neg:
        result = "-" + result
    return result


def multiplication(p, n, d):
    """
    This function performs the multiplication between a number [n] and a digit [d] in a certain base
    [p], and return the result.
    For this, the number is parsed from right to left:
    1. We perform the multiplication between the digit of the number [n], and our digit [d], also adding
    (if it exists) a carry from the last multiplication.
    2. If the number has one digit in base [p], that will be our current digit.
    If not, the second digit will be the current one, and the first one will be kept as a carry
    (the partial result cannot exceed two digits in base [p]).
    :param p: The base of the numbers
    :param n: The number (one of the factors)
    :param d: The digit (one of the factors)
    :return: The result of the multiplication
    """
    result = ""
    n = n[::-1]
    carry = 0
    for i in range(0, len(n)):
        digit = n[i]
        partial_result = value(d) * value(digit) + carry
        result += char((partial_result % p))
        carry = int(partial_result / p)  # The first digit of the partial result in base [p] (which can also be zero)
    if carry:
        result += char(carry)  # We may still have a carry at the end, which we add to the result
    result = result[::-1]  # We reverse the result, since we parsed it from right to left
    return result


def division(p, n, d):
    """
    This function performs the division between a number [n] and a digit [d], in a base [p], and
    return the result.
    For this, the number is parsed from left to right:
    1. We find the current digit of the result, being the quotient of the current dividend and the
    digit (in the base [p]).
    2. The following dividend will be as it is done in a manual division, we keep the modulo of
    the dividend and the digit, and we "lower" a next digit of the number, or simply:
    the modulo is multiplied by the base, and we just add the next digit.
    3. After we "lowered" all the digits, we create the fractional part, by doing the same
    algorithm but by lowering fractionally zeros.
    :param p: The base of the numbers
    :param n: The number (dividend)
    :param d: The digit (divisor)
    :return: The result (quotient) of the division
    """
    result = ""
    dividend = 0
    for i in range(0, len(n)):
        digit = n[i]
        dividend = dividend * p + value(digit)  # The value of the dividend is kept in base 10
        result += char(int(dividend / value(d)))  # By the division rules, we will always have a valid
        # digit, so we just transform it - the base doesn't matter since it won't exceed the base [p]
        dividend %= value(d)
    result = remove_leading_zeros(result) + '.'
    for i in range(10):  # We consider 10 fractional digits to be enough
        dividend *= p  # A zero is "lowered", so we can just multiply the dividend with the base
        result += char(int(dividend / value(d)))
        dividend %= value(d)
    result = remove_leading_zeros(result[::-1])
    if result[0] == '.':  # We may not have a fractional part, so we remove the point
        result = result[1:]
    result = result[::-1]
    return result
