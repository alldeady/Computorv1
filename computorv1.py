import sys

NUMS = '1234567890'
SYM = '*/-+^=xX.'
VERBOSE = True

def check_dot(fl):
    s = str(fl) + '\0'
    i = 0
    if '.' not in s:
        return False
    while i < len(s):
        if s[i] == '.' and s[i + 1] == '0' and s[i + 2] == '\0':
            return False
        i += 1
    return True

def expression(string: str):
    expr, after_equal = ''.join(i for i in string if i in NUMS+SYM).upper().split("=")

    if VERBOSE == True:
        print("\033[34mUntil '=':\n\033[0m" + "\033[31m" + expr + "\033[0m")
        print("\033[34mAfter '=':\n\033[0m" + "\033[31m" + after_equal + "\033[0m")

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


def core(string):
    string = expression(string) + '\0'
    lr = []
    dic = {}
    if VERBOSE == True:
        LOG = 'Summ of members: \n'
        print("\033[34mOne side expression: \033[31m\n" + string + " = 0\033[0m")

    i = 0
    while i < len(string):
        sr = ''
        j = i
        while string[j] != '\0' and string[j] not in '+-':
            sr += string[j]
            j += 1
        if sr != '':
            lr.append(sr)
        if string[j] in "+-":
            lr.append(string[j])
            j += 1
        i = j
        if string[j] == '\0':
            break

    if VERBOSE:
        print("\033[34mDecomposition: ")
        print("\033[31m", end='')
        print(lr)
        print("\033[0m", end='')

    lp = []
    next_minus = False
    for val in lr:
        i = 0
        while i < len(val):
            power = ''
            if val[i] == '-':
                next_minus = True
                i += 1
                continue
            if val[i] == 'X':
                check = i
                val += '\0'
                if val[i + 1] != '\0':
                    i += 2
                    while val[i] != '\0':
                        power += val[i]
                        i += 1
                else:
                    power = '1'
                val = val[:check-1]
                if val == 'X':
                    val = '1'
            else:
                power = '0'
            i += 1
        if val != '-' and next_minus == True:
            val = float(val) * -1
            next_minus = False
        if val != '-' and val != '+':
            if int(power) in dic:
                if VERBOSE:
                    LOG += "\033[32msum: " + str(dic[int(power)]) +" + "+ str(val) + ", power - '" + power + "'" + '\033[0m || '
                dic[int(power)] += float(val)
            else:
                dic.update({int(power): float(val)})
                if VERBOSE:
                    LOG += "\033[33mcreate: " + str(val) + ", power - '" + power + "'" + '\033[0m || '
            lp.append(val)

    if VERBOSE:
        print("\033[34mSecond decomposition: \033[31m")
        print(lp)
        print("\033[34m" + LOG)
        print("\033[34mSummed members key=power, value=value: \033[31m")
        print(dic)
        print("\033[0m")

    reduced_form = 'Reduced form: '
    keys_dic = sorted(dic.keys(), reverse=True)
    for key in keys_dic:
        if dic[key] != 0.0:
            if keys_dic[0] != key:
                reduced_form += " + "
            if key == 0:
                reduced_form += str(dic[key])
            elif key == 1:
                reduced_form += str(dic[key]) + "*x"
            else:
                reduced_form += str(dic[key]) + f"*x^{key}"
        else:
            dic.pop(key)
    reduced_form += ' = 0'
    print(reduced_form)

    if 1 not in dic or 0 not in dic:
        print("Expression is not polynomial equation.")
        return
    for k in keys_dic:
        if k > 2:
            print(f"Polynomial degree: {k}\nThe polynomial degree is strictly greater than 2, I can't solve.")
            return
    if 2 not in dic:
        print ("Polynomial degree: 1\nThe solution is:")
        x = -dic[0] / dic[1]
        if VERBOSE and check_dot(x):
            fraction = x.as_integer_ratio()
            print(f"\033[34mIn irreducible fraction x = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
        print("x = %.6g" % x)
    else:
        print("Polynomial degree: 2")
        discr = dic[1]**2 - 4*dic[2]*dic[0]
        print("Discriminant = %.9g" % discr, end='. ')
        if VERBOSE and check_dot(discr):
            fraction = discr.as_integer_ratio()
            print(f"\n\033[34mIn irreducible fraction Discriminant = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
        if discr > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            x1 = (-dic[1] + discr**(1/2)) / (2 * dic[2])
            if VERBOSE and check_dot(x1):
                fraction = x1.as_integer_ratio()
                print(f"\033[34mIn irreducible fraction x1 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
            x2 = (-dic[1] - discr**(1/2)) / (2 * dic[2])
            if VERBOSE and check_dot(x2):
                fraction = x2.as_integer_ratio()
                print(f"\033[34mIn irreducible fraction x2 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
            print("x1 = %.9g \nx2 = %.9g" % (x1, x2))
        elif discr == 0:
            print("Discriminant is 0, the one solutions are:")
            x = -dic[1] / (2 * dic[2])
            if VERBOSE and check_dot(x):
                fraction = x.as_integer_ratio()
                print(f"\033[34mIn irreducible fraction x2 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
            print("x = %.9g" % x)
        else:
            print("Discriminant is strictly negative, no solutions.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        core(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-v":
        VERBOSE = False
        core(sys.argv[2])
    else:
        print("Wrong number of arguments.")
