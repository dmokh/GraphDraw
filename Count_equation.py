from utilites import *


def count_equation(String_x):
    i = 0
    while i < len(String_x):
        if String_x[i] == '-' and (i == 0 or String_x[i - 1] in op.keys()):
            if i + 1 < len(String_x) and String_x[i + 1][0] != '-':
                String_x[i + 1] = "-" + String_x[i + 1]
                String_x.pop(i)
                i = max(0, i - 2)
            elif i + 1 < len(String_x):
                String_x.pop(i)
                i = max(0, i - 2)
        i += 1
    stack1 = []
    stack2 = []
    now = ""
    i = 0
    while i < len(String_x):
        n = String_x[i]
        if n not in op.keys():
            if n != ' ':
                now += n
        elif n != ' ':
            if now.isdigit() or (len(now) > 1 and now[1:].isdigit()):
                stack1.append(int(now))
            elif isfloat(now) or (len(now) > 1 and isfloat(now[1:])):
                stack1.append(float(now))
            now = ""
            if len(stack2) > 0:
                while len(stack2) > 0 and op[n] <= op[stack2[-1]] and op[n] != 3 and op[stack2[-1]] != 3:
                    x1 = stack1.pop(-1)
                    x2 = stack1.pop(-1)
                    if stack2[-1] == "+":
                        stack1.append(x1 + x2)
                    elif stack2[-1] == '*':
                        stack1.append(x1 * x2)
                    elif stack2[-1] == '/':
                        stack1.append(x2 / x1)
                    elif stack2[-1] == '-':
                        stack1.append(x2 - x1)
                    elif stack2[-1] == '^':
                        stack1.append(x2**x1)
                    stack2.pop(-1)
            if n == ')':
                while stack2[-1] != '(':
                    x1 = stack1.pop(-1)
                    x2 = stack1.pop(-1)
                    if stack2[-1] == "+":
                        stack1.append(x1 + x2)
                    elif stack2[-1] == '*':
                        stack1.append(x1 * x2)
                    elif stack2[-1] == '/':
                        stack1.append(x2 / x1)
                    elif stack2[-1] == '-':
                        stack1.append(x2 - x1)
                    elif stack2[-1] == '^':
                        stack1.append(x2 ** x1)
                    stack2.pop(-1)
                stack2.pop(-1)
            else:
                stack2.append(n)
        i += 1
    if now.isdigit():
        stack1.append(int(now))
    elif isfloat(now):
        stack1.append(float(now))
    if now in op.keys():
        stack2.append(now)
    while len(stack2) > 0 and len(stack1) > 1:
        now = ""
        x1 = stack1.pop(-1)
        x2 = stack1.pop(-1)
        if stack2[-1] == "+":
            stack1.append(x1 + x2)
        elif stack2[-1] == '*':
            stack1.append(x1 * x2)
        elif stack2[-1] == '/':
            stack1.append(x2 / x1)
        elif stack2[-1] == '-':
            stack1.append(x2 - x1)
        elif stack2[-1] == '^':
            stack1.append(x2 ** x1)
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
