import math

from utilites import *


def doOperation(x1, x2, operation, stack1):
    if operation == "+":
        stack1.append(x1 + x2)
    elif operation == '*':
        stack1.append(x1 * x2)
    elif operation == '/':
        stack1.append(x2 / x1)
    elif operation == '-':
        stack1.append(x2 - x1)
    elif operation == '^':
        try:
            stack1.append(x2 ** x1)
        except OverflowError:
            print(f'{x2}^{x1}')
    elif operation == 'u-':
        stack1.append(-x1)
    elif operation == 'sin':
        stack1.append(math.sin(x1))
    elif operation == 'cos':
        stack1.append(math.cos(x1))
    elif operation == 'tan':
        stack1.append(math.tan(x1))
    elif operation == 'ctg':
        stack1.append(math.cos(x1) / math.sin(x1))
    elif operation == 'log2':
        stack1.append(math.log2(abs(x1)))
    elif operation == 'log':
        base = float(x1.split(',')[0])
        x = float(x1.split(',')[1])
        stack1.append(math.log(abs(x), abs(base)))


def count_equation(equation):
    # change string to list
    if type(equation) != list:
        equation = list(equation)

    # parse
    stack1 = []
    stack2 = []
    now = ""
    for i in range(len(equation)):
        n = equation[i]
        if now in op.keys():
            if now != 'log' or equation[i] != '2':
                stack2.append(now)
                now = ''
        if n not in op.keys() or (i > 0 and n == '-' and equation[i-1] == 'e'):
            now += n
        else:
            if now.isdigit() or (len(now) > 1 and now[1:].isdigit()):
                stack1.append(int(now))
            elif isfloat(now) or (len(now) > 1 and isfloat(now[1:])):
                stack1.append(float(now))
            elif ',' in now:
                stack1.append(now)
            now = ''
            if len(stack2) > 0:
                while len(stack2) > 0 and op[n] <= op[stack2[-1]] < op['(']:
                    if stack2[-1] in unary_op:
                        doOperation(stack1.pop(-1), None, stack2[-1], stack1)
                    elif len(stack1) > 1:
                        doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                    stack2.pop(-1)
            if n == ')':
                while stack2[-1] != '(':
                    if stack2[-1] in unary_op:
                        doOperation(stack1.pop(-1), None, stack2[-1], stack1)
                    elif len(stack1) > 1:
                        doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                    stack2.pop(-1)
                stack2.pop(-1)
            elif n == '|':
                if i > 0 and equation[i-1] not in binary_op:
                    while stack2[-1] != '|':
                        if stack2[-1] in unary_op:
                            doOperation(stack1.pop(-1), None, stack2[-1], stack1)
                        elif len(stack1) > 1:
                            doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                        stack2.pop(-1)
                    stack2.pop(-1)
                    stack1[-1] = abs(stack1[-1])
                else:
                    stack2.append(n)
            else:
                if n == '-' and (i == 0 or equation[i-1] in op.keys()):
                    stack2.append('u-')
                else:
                    stack2.append(n)
    if now.isdigit() or (len(now) > 1 and now[1:].isdigit()):
        stack1.append(int(now))
    elif isfloat(now) or (len(now) > 1 and isfloat(now[1:])):
        stack1.append(float(now))
    elif ',' in now:
        stack1.append(now)
    if now in op.keys():
        stack2.append(now)
    while len(stack2) > 0 and len(stack1) > 0:
        if stack2[-1] in unary_op:
            doOperation(stack1.pop(-1), None, stack2[-1], stack1)
        elif len(stack1) > 1:
            doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
        stack2.pop(-1)
    return stack1[0]


def get_monomials(equation):
    monomials = []
    monomial = ''
    operation = ''
    for s in equation:
        if s == '+' or s == '-':
            if operation == '':
                monomials.append([monomial, '+'])
            else:
                monomials.append([monomial, operation])
            operation = s
            monomial = ''
        else:
            monomial += s
    if operation == '':
        operation = '+'
    monomials.append([monomial, operation])
    return monomials


if __name__ == "__main__":
    print(count_equation('log2(5)'))
