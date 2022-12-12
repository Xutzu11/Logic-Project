"""
This module contains the conversions parts, functions that do conversions of natural numbers
between certain bases.
"""

from functions import value
from functions import char
from functions import remove_leading_zeros
from operations import addition
from operations import multiplication
from math import pow
from math import log2


def successive_divisions(b, h, n):
    """
    This function converts a number [n] from base [b] to base [h] by using successive divisions.
    This method is primarily used for conversions with a source base greater than a destination base.
    For this, we perform a division between the number [n] and the base [h], in the base [b].
    The remainder will be a digit in the result (but in reverse order), and on the quotient we perform
    the same algorithm (until the quotient becomes zero).
    :param b: The source base
    :param h: The destination base
    :param n: The number (initially in the source base)
    :return: The converted number in base [h]
    """
    result = ""
    while n != "0":
        partial_result, remainder, dividend = 0, 0, ""
        for i in range(0, len(n)):
            digit = n[i]
            partial_result = partial_result * b + value(digit)  # We "lower" the next digit
            dividend += char(int(partial_result / h))
            partial_result %= h  # As in division, this will be in the result
        remainder = partial_result
        result += char(remainder)
        n = remove_leading_zeros(dividend)  # The quotient kept for the next operations, with leading zeros removed
    result = result[::-1]
    return result


def substitution_method(b, h, n):
    """
    This function converts a number [n] from base [b] to base [h], using the substitution method.
    This method is primarily used for conversions with a destination base greater than a source base.
    For this, the digits are converted into base [h] (since [h] > [b], the digits remain the same).
    Then, each digit is multiplied by a corresponding power of the source base, but in the destination base.
    All of these multiplications are added together, making the result.
    :param b: The source base
    :param h: The destination base
    :param n: The number (initially in the source base)
    :return: The converted number in base [h]
    """
    n = n[::-1]
    power = "1"  # The initial power is [b] at power 0, which is equal to 1.
    result = multiplication(h, n[0], power)
    for i in range(1, len(n)):
        power = multiplication(h, power, char(b))  # We create the next power, by multiplying the current one with [b]
        digit = n[i]
        partial_result = multiplication(h, power, digit)  # We create the partial result, by multiplying the power
        # with the digit
        result = addition(h, result, partial_result)  # We add the partial result to the whole result
    return result


def intermediate_base(b, h, n):
    """
    This function converts a number [n] from a base [b] to a base [h], using base 10 as an intermediate
    base.
    For this, the number is first converted into base 10, by simply computing it:
    1. We parse the digits from right to left.
    2. Every digit is multiplied with a power of [b] (corresponding to the index of the digit), and
    is added to the converted number.
    For converting the number from base 10 to base [h], we compute it the following way:
    1. The modulo of the number and the base [h] will be a current digit.
    2. We only keep the quotient, and we repeat.
    The digits will be reversed in the result.
    :param b: The source base
    :param h: The destination base
    :param n: The number (initially in the source base)
    :return: The converted number in base [h]
    """
    base_10_number = 0
    result = ""
    if b == 10:
        base_10_number = int(n)
    else:
        n = n[::-1]
        for i in range(0, len(n)):
            digit = n[i]
            base_10_number += value(digit) * int(pow(b, i))  # We add the digit multiplied with the corresponding power
    if h == 10:
        return base_10_number
    while base_10_number != 0:
        result += char(base_10_number % h)  # The modulo will be a digit in the result
        base_10_number = int(base_10_number / h)  # We keep the quotient to continue finding the result's digits
    result = result[::-1]
    return result


def convert_to_2(b, n):
    """
    This function converts a number [n] from a base [b] to base 2, using rapid conversions. For this,
    the source base [b] must be a power of 2 (since we won't convert a number already in base 2,
    [b] must be from the set {4,8,16}).
    Suppose we write the base [b] as b = 2^x.
    Then, we replace every digit of the number with [x] digits in base 2, by computing the corresponding
    3-digit number.
    :param b: The source base (from {4,8,16})
    :param n: The number (initially in the source base)
    :return: The converted number in base 2
    """
    result = ""
    for i in range(0, len(n)):
        partial_result = ""
        digit = value(n[i])
        for j in range(int(log2(b))):  # The digit will be transformed in x (log base 2 of b) digits
            partial_result = char(digit % 2) + partial_result
            digit = int(digit / 2)
        result += partial_result  # The digit is replaced with the newly created x-digit number
    return remove_leading_zeros(result)


def convert_from_2(h, n):
    """
    This function converts a number [n] from base 2 to base [h], using rapid conversions. For this, the
    destination base must be a power of 2 (since we won't convert a number that is in base 2 into the same base,
    [h] must be from the set {4,8,16}).
    Suppose we write the base [h] as 2^x.
    Then, we will make groups of [x] digits (from right to left), and every [x] digits will be converted into
    one digit, that will replace on the same position those [x] digits in the final result.
    Since we may not have a multiple of [x] as a number of digits, we add as many leading zeros as we need.
    :param h: The destination base (from {4,8,16})
    :param n: The number (initially in base 2)
    :return: The converted number in base [h]
    """
    result = ""
    n = n[::-1]
    while len(n) % int(log2(h)):
        n += '0'  # We add leading zeros so that we can make groups of [x] digits
    for i in range(0, len(n), int(log2(h))):
        partial_result = 0
        for j in range(0, int(log2(h))):
            digit = n[i + j]
            partial_result += int(pow(2, j)) * value(digit)  # We create the base 10 number corresponding to the
            # x-digit number
        result += char(partial_result)  # We add the digit corresponding to the base 10 number to the result
    result = result[::-1]  # Since it's parsed from right to left, we reverse it
    return result


def rapid_conversions(b, h, n):
    """
    This function converts a number [n] from a base [b] to a base [h] using rapid conversions. For this,
    the bases must be powers of 2 (so [b] and [h] must be from the set {2,4,8,16}).
    First, the number is converted from base [b] to base 2 (if necessary), then from base 2 into base [h]
    (if necessary), creating the final result.
    :param b: The source base (from {2,4,8,16})
    :param h: The destination base (from {2,4,8,16})
    :param n: The number (initially in the source base)
    :return: The converted number in base [h]
    """
    if b != 2:
        result = convert_to_2(b, n)  # We only converted to base 2 if it's not already converted
    else:
        result = n
    if n != 2:
        result = convert_from_2(h, result)  # We only convert it to base 2 if it's not already converted
    return result
