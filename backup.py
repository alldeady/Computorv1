import sys

NUMS = '1234567890'
SYM = '*/-+^=xX.'
VERBOSE = True

def print_red(element):
    print("\033[31m", end='')
    print(element, end='')
    print("\033[0m")

def under_equal(string: str):
    expr, after_equal = ''.join(i for i in string if i in NUMS+SYM).lower().split("=")

    if VERBOSE == True:
        print_red("Until '=': " + expr)
        print_red("After '=': " + after_equal)

    if after_equal[0] != '0':
        after_equal+='\0'
        i = 0
        if after_equal[i] in NUMS:
            expr += '-'
        while i < len(after_equal):
            if after_equal[i] == '+':
                expr += '-'
                i += 1
                continue
            elif after_equal[i] == '-':
                expr += '+'
                i += 1
                continue
            elif after_equal[i] == '\0':
                break
            else:
                expr += after_equal[i]
            if after_equal[i] in NUMS and after_equal[i - 1] != '^':
                if after_equal[i+1] == '\0':
                    break
                while after_equal[i + 1] in NUMS:
                    i += 1
                    expr += after_equal[i]
            i += 1
    return expr


def core(string: str):
    expr = under_equal(string) + '\0'
    if VERBOSE == True:
        LOG = 'Members: \n'
        print_red("Expression: " + expr + " = 0")
    abc_expr = {}
    i = 0
    while i < len(expr):
        if expr[i] == 'x':
            number_str = ''
            if expr[i + 1] == '^':
                j = i + 2
                power = ''
                while j < len(expr) and expr[j] in NUMS:
                    power += expr[j]
                    j += 1
            j = i-2
            while j >= 0 and expr[j] in NUMS+'.-*/':
                number_str += expr[j]
                if expr[j] == '-':
                    break
                j -= 1
            if int(power) in abc_expr:
                if VERBOSE == True:
                    LOG += "\033[32msum: " + str(abc_expr[int(power)]) +" + "+ number_str[::-1] + " power - '" + power + "'" + '\033[0m || '
                abc_expr[int(power)] += float(number_str[::-1])
            else:
                abc_expr.update({int(power): float(number_str[::-1])})
                if VERBOSE == True:
                    LOG += "\033[33mcreate: " + number_str[::-1] + " power - '" + power + "'" + '\033[0m || '
            i += 2
        i += 1

    if VERBOSE == True:
        print_red(LOG)
        print_red("Expression members, key=power, value=value:):")
        print_red(abc_expr)

    reduced_form = 'Reduced form: '
    keys_dic = sorted(abc_expr.keys(), reverse=True)
    for key in keys_dic:
        if abc_expr[key] != 0.0:
            if keys_dic[0] != key:
                reduced_form += " + "
            reduced_form += str(abc_expr[key]) + f"*X^{key}"
        else:
            abc_expr.pop(key)
    reduced_form += ' = 0'
    print(reduced_form)

    if 1 not in abc_expr or 0 not in abc_expr:
        print("Expression is not polynomial equation.")
        return
    for k in keys_dic:
        if k > 2:
            print(f"Polynomial degree: {k}\nThe polynomial degree is strictly greater than 2, I can't solve.")
            return
    if 2 not in abc_expr:
        print ("Polynomial degree: 1\nThe solution is:")
        print("x = %.6g" % (-abc_expr[0] / abc_expr[1]))
    else:
        print("Polynomial degree: 2")
        discr = abc_expr[1] ** 2 - 4 * abc_expr[2] * abc_expr[0]
        print("Discriminant = %.9g" % discr, end='. ')
        if discr > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            x1 = (-abc_expr[1] + discr**(1/2)) / (2 * abc_expr[2])
            x2 = (-abc_expr[1] - discr**(1/2)) / (2 * abc_expr[2])
            print("x1 = %.9g \nx2 = %.9g" % (x1, x2))
        elif discr == 0:
            print("Discriminant is 0, the one solutions are:")
            x = -abc_expr[1] / (2 * abc_expr[2])
            print("x = %.9g" % x)
        else:
            print("Discriminant is strictly negative, no solutions.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        core(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-v":
        VERBOSE = True
        core(sys.argv[2])
    else:
        print("Wrong number of arguments.")
