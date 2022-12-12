"""
This module contains the user interface, containing the menu and the options of the app,
data validation, and prints the results.
For all the functions, any occurrences of the following phrases define the following:
".upper()" - is used for simplicity - in case a number is in base 16 we convert its digits that are from
the set {a,b,c,d,e,f,g} to the corresponding uppercase letter {A,B,C,D,E,F,G}
"remove_leading_zeros" - we remove the leading zeros of a certain number
"""

import operations
import conversions
from functions import valid_number
from functions import valid_base
from functions import remove_leading_zeros

def personal_data():
    # This function prints the author's data for identification
    print("Name: Ignat Alex-Matei")
    print("Group: 914")


def command():
    print("Please choose an option:")
    print("1. Arithmetic operation")
    print("2. Conversion")
    print("3. Exit the application")
    cmd = input("Enter your option: ")
    try:
        cmd = int(cmd)
    except ValueError:
        raise Exception("Invalid option, please try again.")
    return cmd


def addition_and_subtraction_ui(cmd, digits_16):
    p = input("Enter the base: ")
    if not valid_base(p):
        raise Exception("The base is not valid, please try again.")
    p = int(p)
    n1 = input("Enter the first number: ")
    n1 = remove_leading_zeros(n1).upper()
    if not valid_number(p, n1, digits_16):
        raise Exception("The number is not valid in the selected base, please try again.")
    n2 = input("Enter the second number: ")
    n2 = remove_leading_zeros(n2).upper()
    if not valid_number(p, n2, digits_16):
        raise Exception("The number is not valid in the selected base, please try again.")
    if cmd == 1:
        print("The result is:", operations.addition(p, n1, n2))
    else:
        print("The result is:", operations.subtraction(p, n1, n2))


def multiplication_and_division_ui(cmd, digits_16):
    p = input("Enter the base: ")
    if not valid_base(p):
        raise Exception("The base is not valid, please try again.")
    p = int(p)
    n = input("Enter the number: ")
    n = remove_leading_zeros(n).upper()
    if not valid_number(p, n, digits_16):
        raise Exception("The number is not valid in the selected base, please try again.")
    d = input("Enter the digit: ")
    d = remove_leading_zeros(d).upper()
    if len(d) != 1 or not valid_number(p, d, digits_16):
        raise Exception("The digit is not valid in the selected base, please try again.")
    if cmd == 3:
        print("The result is:", operations.multiplication(p, n, d))
    else:
        if int(d) == 0:
            raise Exception("The digit for division cannot be zero, please try again.")
        print("The result is:", operations.division(p, n, d))


def arithmetic_op(digits_16):
    arithmetic_options = {1: addition_and_subtraction_ui,
                          2: addition_and_subtraction_ui,
                          3: multiplication_and_division_ui,
                          4: multiplication_and_division_ui}
    print("1. Addition of two numbers")
    print("2. Subtraction of two numbers")
    print("3. Multiplication by a digit")
    print("4. Division by a digit")
    try:
        cmd = int(input("Enter your option: "))
    except ValueError:
        raise Exception("Invalid option, please try again.")
    try:
        arithmetic_options[cmd](cmd, digits_16)
    except KeyError:
        raise Exception("Invalid option, please try again.")
    except Exception as e:
        raise e

def successive_divisions_ui(digits_16):
    source_base = input("Enter the source base: ")
    if not valid_base(source_base):
        raise Exception("Source base not valid, please try again.")
    destination_base = input("Enter the destination base: ")
    if not valid_base(destination_base):
        raise Exception("Destination base not valid, please try again.")
    source_base, destination_base = int(source_base), int(destination_base)
    if source_base <= destination_base:
        raise Exception("This method is recommended when the source base > destination base, "
                        "please choose another method.")
    number = input("Enter the number in the source base: ")
    number = remove_leading_zeros(number).upper()
    if not valid_number(source_base, number, digits_16):
        raise Exception("Number not valid in the selected source base, please try again.")
    print("The number in base", destination_base, "is:",
          conversions.successive_divisions(source_base, destination_base, number))


def substitution_method_ui(digits_16):
    source_base = input("Enter the source base: ")
    if not valid_base(source_base):
        raise Exception("Source base not valid, please try again.")
    destination_base = input("Enter the destination base: ")
    if not valid_base(destination_base):
        raise Exception("Destination base not valid, please try again.")
    source_base, destination_base = int(source_base), int(destination_base)
    if source_base >= destination_base:
        raise Exception("This method is recommended when the source base < destination base, "
                        "please choose another method.")
    number = input("Enter the number in the source base: ")
    number = remove_leading_zeros(number).upper()
    if not valid_number(source_base, number, digits_16):
        raise Exception("Number not valid in the selected source base, please try again.")
    print("The number in base", destination_base, "is:",
          conversions.substitution_method(source_base, destination_base, number))


def intermediate_base_ui(digits_16):
    source_base = input("Enter the source base: ")
    if not valid_base(source_base):
        raise Exception("Source base not valid, please try again.")
    destination_base = input("Enter the destination base: ")
    if not valid_base(destination_base):
        raise Exception("Destination base not valid, please try again.")
    source_base, destination_base = int(source_base), int(destination_base)
    number = input("Enter the number in the source base: ")
    number = remove_leading_zeros(number).upper()
    if not valid_number(source_base, number, digits_16):
        raise Exception("Number not valid in the selected source base, please try again.")
    print("The number in base", destination_base, "is:",
          conversions.intermediate_base(source_base, destination_base, number))


def rapid_conversions_ui(digits_16):
    correct_bases = (2, 4, 8, 16)
    source_base = input("Enter the source base: ")
    if not valid_base(source_base):
        raise Exception("Source base not valid, please try again.")
    destination_base = input("Enter the destination base: ")
    if not valid_base(destination_base):
        raise Exception("Destination base not valid, please try again.")
    source_base, destination_base = int(source_base), int(destination_base)
    if not correct_bases.count(source_base) or not correct_bases.count(destination_base):
        raise Exception("For rapid conversions, the bases should be powers of 2 (2,4,8,16), "
                        "please try another method.")
    number = input("Enter the number in the source base: ")
    number = remove_leading_zeros(number).upper()
    if not valid_number(source_base, number, digits_16):
        raise Exception("Number not valid in the selected source base, please try again.")
    print("The number in base", destination_base, "is:",
          conversions.rapid_conversions(source_base, destination_base, number))


def conversion(digits_16):
    conversion_options = {1: successive_divisions_ui,
                          2: substitution_method_ui,
                          3: intermediate_base_ui,
                          4: rapid_conversions_ui}
    print("1. Using successive divisions (source base > destination base)")
    print("2. Using substitution method (destination bases < source base)")
    print("3. Using base 10 as an intermediate base")
    print("4. Using rapid conversions (for bases: 2,4,8,16)")
    try:
        cmd = int(input("Enter your option: "))
    except ValueError:
        raise Exception("Invalid option, please try again.")
    try:
        conversion_options[cmd](digits_16)
    except KeyError:
        raise Exception("Invalid option, please try again.")
    except Exception as e:
        raise e


def exit_app(digits_16):
    raise SystemError("exit")


def menu():
    personal_data()
    print("Welcome to the app!")
    digits_16 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F')
    options = {1: arithmetic_op,
               2: conversion,
               3: exit_app}
    while True:
        try:
            options[command()](digits_16)
        except KeyError:
            print("Invalid option, please try again.")
        except SystemError:
            return
        except Exception as e:
            print(e)
