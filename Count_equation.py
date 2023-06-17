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
        try:
            stack1.append(math.log2(abs(x1)))
        except ValueError:
            stack1.append(math.log2(abs(x1+1)))
    elif operation == 'log':
        base = float(x1.split(',')[0])
        x = float(x1.split(',')[1])
        stack1.append(math.log(abs(x), abs(base)))
    elif operation == 'abs':
        stack1.append(abs(x1))


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
                        stack2.pop(-1)
                    elif len(stack1) > 1:
                        doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                        stack2.pop(-1)
                    else:
                        break
            if n == ')':
                while stack2[-1] != '(':
                    if stack2[-1] in unary_op:
                        doOperation(stack1.pop(-1), None, stack2[-1], stack1)
                        stack2.pop(-1)
                    elif len(stack1) > 1:
                        doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                        stack2.pop(-1)
                    else:
                        break
                stack2.pop(-1)
            elif n == '|':
                if i > 0 and equation[i-1] not in binary_op:
                    while stack2[-1] != '|':
                        if stack2[-1] in unary_op:
                            doOperation(stack1.pop(-1), None, stack2[-1], stack1)
                            stack2.pop(-1)
                        elif len(stack1) > 1:
                            doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
                            stack2.pop(-1)
                        else:
                            break
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
            stack2.pop(-1)
        elif len(stack1) > 1:
            doOperation(stack1.pop(-1), stack1.pop(-1), stack2[-1], stack1)
            stack2.pop(-1)
        else:
            break
    return stack1[0]


def get_monomials(equation):
    monomials = []
    now = ''
    in_parenthesis = False
    in_bracket = False
    c_br_op = 0
    c_br_cl = 0
    c_par_op = 0
    c_par_cl = 0
    last_op = '+'
    for i in range(len(equation)):
        n = equation[i]
        if n in op.keys() or now in op.keys():
            if ((n == '-' and (i == 0 or equation[i-1] != 'e')) or n == '+') and not in_parenthesis and not in_bracket:
                monomials.append([now, last_op])
                now = ''
                last_op = n
            elif n == '(':
                now += n
                in_parenthesis = True
                c_par_op += 1
            elif n == ')':
                now += n
                c_par_cl += 1
                if c_par_op == c_par_cl:
                    in_parenthesis = False
            elif n == '|':
                now += n
                if i > 0 and equation[i-1] not in binary_op:
                    c_br_cl += 1
                    if c_br_cl == c_br_op:
                        in_bracket = False
                else:
                    c_br_op += 1
                    in_bracket = True
            else:
                now += n
        else:
            now += n
    if now != '':
        monomials.append([now, last_op])
    i = 0
    while any(list(map(lambda x: ('+' in x[0] or '-' in x[0]) and ('(' in x[0] or '|' in x[0]), monomials))):
        if '(' not in monomials[i][0] and '|' not in monomials[i][0]:
            i += 1
            if i == len(monomials):
                i = 0
            continue
        mon = monomials[i][0]
        j = 0
        while j < len(mon) and mon[j] != '|' and mon[j] != '(':
            j += 1
        operation = ''
        now = ''
        for h in range(j):
            if mon[h] == '*' or mon[h] == '/':
                if operation != '':
                    mon += operation + now
                    now = ''
                operation = mon[h]
            else:
                now += mon[h]
        if now != '':
            mon += operation + now
        mon = mon[j:]
        if mon[0] == '(':
            k = 1
            c = 1
            while k < len(mon) and c != 0:
                if mon[k] == '(':
                    c += 1
                elif mon[k] == ')':
                    c -= 1
                k += 1
            k -= 1
        else:
            k = 1
            c = 1
            while k < len(mon) and c != 0:
                if mon[k] == '|':
                    if i > 0 and equation[i - 1] not in binary_op:
                        c -= 1
                    else:
                        c += 1
                k += 1
            k -= 1
        for monomial_from in get_monomials(mon[1:k]):
            if mon[0] == '(':
                monomials.append([monomial_from[0]+mon[k+1:], monomials[i][1]])
            else:
                monomials.append(['|' + monomial_from[0] + mon[k + 1:] + '|', monomials[i][1]])
        monomials.pop(i)
        if i == len(monomials):
            i = 0
    return monomials


if __name__ == "__main__":
    s = '(x^2)*(y+4)'
    print(get_monomials(s))
