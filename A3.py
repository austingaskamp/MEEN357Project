# Davis McMullan
# UIN: 128008620

import numpy
import math
from scipy.optimize import root_scalar


def bisection(functionHandle, lowerBound, upperBound, errorCap=0.05, iterationCeil=100):
    # Initial Values block
    iteration = 0
    error = float(1)
    exitFlag = 1  # Program assumes normal exit until shown otherwise
    try:
        errorCap *= 0.01  # This converts the percent to a decimal
        lowerVal = functionHandle(lowerBound)
        upperVal = functionHandle(upperBound)
    except TypeError:
        if (  # This long conditional checks the validity of all input parameters
                (type(lowerBound) not in (float, int))
                or (type(upperBound) not in (float, int))
                or (type(errorCap) not in (float, int))
                or ((type(iterationCeil) is not int
                     or iterationCeil < 0))
        ):
            exitFlag = -2
            raise ValueError('Parameters not of correct datatype')

    # Input Validation block
    if (type(lowerVal) is not float) or (type(upperVal) is not float):  # Checks that function handle returns a scalar
        exitFlag = -2
        return 'Error', 'Error', 'Error', exitFlag

    if (lowerVal * upperVal) > 0:  # This confirms the bracket contains at least one zero
        exitFlag = -1  # Note: this way of detecting roots does not account for roots that only "touch" 0
        return 'Error', 'Error', 'Error', exitFlag

    if (  # This long conditional is repeated as a check if the value accidentally passed the "try" statement above
            (type(lowerBound) not in (float, int))
            or (type(upperBound) not in (float, int))
            or (type(errorCap) not in (float, int))
            or ((type(iterationCeil) is not int
                 or iterationCeil < 0))
    ):
        exitFlag = -2
        raise ValueError

    # Main Calculation Body
    while (error >= errorCap) and (iteration <= iterationCeil):  # main process loop
        xMid = (lowerBound + upperBound) / 2
        lowerVal = functionHandle(lowerBound)
        midVal = functionHandle(xMid)

        if iteration == iterationCeil:  # This conditional checks if loop is on max iteration
            exitFlag = 0
        else:
            iteration += 1

        if (lowerVal * midVal) < 0:
            upperBound = xMid
        elif (lowerVal * midVal) > 0:
            lowerBound = xMid
        elif (lowerVal * midVal) == 0:
            error = 0.0
            return xMid, error, iteration, exitFlag

        if iteration != 1:
            error = abs((oldVal - xMid) / xMid)

        oldVal = xMid

    return xMid, (error * 100), iteration, exitFlag


def falsepos(functionHandle, lowerBound, upperBound, errorCap=0.05, iterationCeil=100):
    # Initial Values block
    iteration = 0
    error = float(1)
    exitFlag = 1  # Program assumes normal exit until shown otherwise
    try:
        errorCap *= 0.01  # This converts the percent to a decimal
        lowerVal = functionHandle(lowerBound)
        upperVal = functionHandle(upperBound)
    except TypeError:
        if (  # This long conditional checks the validity of all input parameters
                (type(lowerBound) not in (float, int))
                or (type(upperBound) not in (float, int))
                or (type(errorCap) not in (float, int))
                or ((type(iterationCeil) is not int
                     or iterationCeil < 0))
        ):
            exitFlag = -2
            raise ValueError('Parameters not of correct datatype')

    # Input Validation block
    if (type(lowerVal) is not float) or (type(upperVal) is not float):  # Checks that function handle returns a scalar
        exitFlag = -2
        return 'Error', 'Error', 'Error', exitFlag

    if (lowerVal * upperVal) > 0:  # This confirms the bracket contains at least one zero
        exitFlag = -1  # Note: this way of detecting roots does not account for roots that only "touch" 0
        return 'Error', 'Error', 'Error', exitFlag

    if (  # This long conditional is repeated as a check if the value accidentally passed the "try" statement above
            (type(lowerBound) not in (float, int))
            or (type(upperBound) not in (float, int))
            or (type(errorCap) not in (float, int))
            or ((type(iterationCeil) is not int
                 or iterationCeil < 0))
    ):
        exitFlag = -2
        raise ValueError

    # Main Calculation Body
    while (error >= errorCap) and (iteration <= iterationCeil):  # main process loop
        upperVal = functionHandle(upperBound)
        lowerVal = functionHandle(lowerBound)
        xMid = upperBound - ((upperVal * (lowerBound - upperBound)) / (lowerVal - upperVal))
        midVal = functionHandle(xMid)

        if iteration == iterationCeil:  # This conditional checks if loop is on max iteration
            exitFlag = 0
        else:
            iteration += 1

        if (lowerVal * midVal) < 0:
            upperBound = xMid
        elif (lowerVal * midVal) > 0:
            lowerBound = xMid
        elif (lowerVal * midVal) == 0:
            error = 0.0
            return xMid, error, iteration, exitFlag

        if iteration != 1:
            error = abs((oldVal - xMid) / xMid)

        oldVal = xMid

    return xMid, (error * 100), iteration, exitFlag


def secant(functionHandle, rootGuess, errorCap=0.05, iterationCeil=100):
    # Initial Values block
    iteration = 0
    error = float(1)
    exitFlag = 1  # Program assumes normal exit until shown otherwise
    try:
        errorCap *= 0.01  # This converts the percent to a decimal
        old_guess = rootGuess - 1
        y_i = functionHandle(rootGuess)
        y_old = functionHandle(old_guess)
    except TypeError:
        if (  # This long conditional checks the validity of all input parameters
                (type(rootGuess) not in (float, int))
                or (type(errorCap) not in (float, int))
                or ((type(iterationCeil) is not int
                     or iterationCeil < 0))
        ):
            exitFlag = -2
            raise ValueError('Parameters not of correct datatype')

    # Input Validation block
    if (type(y_old) is not float) or (type(y_i) is not float):
        exitFlag = -2
        return 'Error', 'Error', 'Error', exitFlag

    if (type(iterationCeil) is not int) or (iterationCeil < 0):
        raise ValueError('Max iteration error')

    # Main Calculation Body
    while (error >= errorCap) and (iteration <= iterationCeil):  # main process loop
        y_old = functionHandle(old_guess)
        y_i = functionHandle(rootGuess)
        if y_i == y_old:
            error = 0.0
            break
        nextGuess = old_guess - ((y_old * (rootGuess - old_guess)) / (y_i - y_old))

        if iteration == iterationCeil:  # This conditional checks if loop is on max iteration
            exitFlag = 0
        else:
            iteration += 1

        if iteration != 1 and nextGuess != 0.0:
            error = abs((nextGuess - rootGuess) / nextGuess)

        old_guess = rootGuess
        rootGuess = nextGuess

    return rootGuess, (error * 100), iteration, exitFlag


def func_a(x_val):
    y_val = x_val * math.sin(x_val) + 3 * math.cos(x_val) - x_val
    return y_val


def func_b(x_val):
    y_val = x_val * (math.sin(x_val) - x_val * math.cos(x_val))
    return y_val


def func_c(x_val):
    y_val = (1 / 40) * (x_val**3 - 2*x_val**2 + 5*x_val - 25)
    return y_val


def func_fake(x_val):
    return [1, 2]


if __name__ == "__main__":
    ############################################
    # Test code
    root, err, numIter, exitFlag = bisection(func_a, 0, 2, 0.01, 300)
    root1, err1, numIter1, exitFlag1 = bisection(func_a, 0, 1, 0.01, 300)
    root2, err2, numIter2, exitFlag2 = bisection(func_a, 0, 2, 0.01, 3)
    root3, err3, numIter3, exitFlag3 = bisection(func_fake, 0, 1, 0.01, 300)
    # root4, err4, numIter4, exitFlag4 = bisection(func_a, 0, 'dog', 0.01, 300)

    root5, err5, numIter5, exitFlag5 = falsepos(func_a, 0, 2, 0.01, 300)
    root6, err6, numIter6, exitFlag6 = falsepos(func_a, 0, 1, 0.01, 300)
    root7, err7, numIter7, exitFlag7 = falsepos(func_a, 0, 2, 0.01, 3)
    root8, err8, numIter8, exitFlag8 = falsepos(func_fake, 0, 1, 0.01, 300)

    root9, err9, numIter9, exitFlag9 = secant(func_a, 1, 0.01, 100)
    test = root_scalar(func_a, method='secant', x0=0, x1=1)

    #########################################
    # Task 4
    # Function A
    A_root1, A_error1, A_iter1, A_exitFlag1 = falsepos(func_a, -5, -4)
    A_root2, A_error2, A_iter2, A_exitFlag2 = falsepos(func_a, -4, -2)
    A_root3, A_error3, A_iter3, A_exitFlag3 = falsepos(func_a, 0, 2)

    # Function B
    B_root1, B_error1, B_iter1, B_exitFlag1 = bisection(func_b, -5, -4)
    B_root2, B_error2, B_iter2, B_exitFlag2 = secant(func_b, -1)
    B_root3, B_error3, B_iter3, B_exitFlag3 = bisection(func_b, 4, 5)

    # Function C
    C_root1, C_error1, C_iter1, C_exitFlag1 = bisection(func_c, 2, 5)

    print('done')