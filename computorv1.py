import sys

VERBOSE = True
NUMS = '1234567890'
SYM = '*/-+^=xX.'

def nodd(a, b, c):
    tmp_b = b

    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    nod_1 = a + b
    b = tmp_b
    while b != 0 and c != 0:
        if b > c:
            b %= c
        else:
            c %= b
    nod_2 = b + c
    if nod_1 == nod_2:
        return [True, nod_1]
    else:
        return [False]

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
    try:
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

        minus = False
        for val in lr:
            i = 0
            while i < len(val):
                power = ''
                if val[i] == '-':
                    minus = True
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
            if val != '-' and minus == True:
                val = float(val) * -1
                minus = False
            if val != '-' and val != '+':
                if int(power) in dic:
                    if VERBOSE:
                        LOG += "\033[32msum: " + str(dic[int(power)]) +" + "+ str(val) + ", power - '" + power + "'" + '\033[0m || '
                    dic[int(power)] += float(val)
                else:
                    dic.update({int(power): float(val)})
                    if VERBOSE:
                        LOG += "\033[33mcreate: " + str(val) + ", power - '" + power + "'" + '\033[0m || '

        if VERBOSE:
            print("\033[34m" + LOG)
            print("\033[34mSummed members key=power, value=value: \033[31m")
            print(dic)
            print("\033[0m")

        reduced_form = 'Reduced form: '
        keys_dic = sorted(dic.keys(), reverse=True)
        for key in keys_dic:
            minus = False
            if dic[key] != 0.0:
                if keys_dic[0] != key:
                    if dic[key] < 0.0:
                        reduced_form += " - "
                        minus = True
                    else:
                        reduced_form += " + "
                if key == 0:
                    reduced_form += str(dic[key] if minus == False else dic[key] * -1)
                elif key == 1:
                    reduced_form += str(dic[key] if minus == False else dic[key] * -1) + "*x"
                else:
                    reduced_form += str(dic[key] if minus == False else dic[key] * -1) + f"*x^{key}"

        print(reduced_form + ' = 0')
        print(dic)
        for k in keys_dic:
            if k > 2:
                raise Exception(f"Polynomial degree: {k}\nThe polynomial degree is strictly greater than 2, I can't solve.")
        if 1 not in dic:
            dic.update({1: 0.0})
        if 0 not in dic:
            dic.update({0: 0.0})
        if 2 in dic and dic[2] == 0.0:
            dic.pop(2)
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
            print("Discriminant = %.6g" % discr, end='. ')
            if VERBOSE and check_dot(discr):
                fraction = discr.as_integer_ratio()
                print(f"\n\033[34mIn irreducible fraction Discriminant = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
            if discr > 0:
                print("Discriminant is strictly positive, the two solutions are:")
                x1 = (-dic[1] + discr**0.5) / (2 * dic[2])
                if VERBOSE and check_dot(x1):
                    fraction = x1.as_integer_ratio()
                    print(f"\033[34mIn irreducible fraction x1 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
                x2 = (-dic[1] - discr**0.5) / (2 * dic[2])
                if VERBOSE and check_dot(x2):
                    fraction = x2.as_integer_ratio()
                    print(f"\033[34mIn irreducible fraction x2 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
                print("x1 = %.6g \nx2 = %.6g" % (x1, x2))
            elif discr == 0:
                print("Discriminant is 0, the one solutions are:")
                x = -dic[1] / (2 * dic[2])
                if VERBOSE and check_dot(x):
                    fraction = x.as_integer_ratio()
                    print(f"\033[34mIn irreducible fraction x2 = \033[31m{fraction[0]}/{fraction[1]}\033[0m")
                print("x = %.6g" % x)
            else:
                print("Discriminant is strictly negative, complex solutions are:")
                nod = [False]
                com_discr = (discr*-1)**0.5
                denominator = 2*dic[2]
                if check_dot(-dic[1]) == False and check_dot(com_discr) == False and check_dot(denominator) == False:
                    nod = nodd(-dic[1], com_discr, denominator)
                if nod[0] == True:
                    if denominator/nod[1] == 1:
                        print("x1,2 = %.6g \u00B1 %.6gi" % (-dic[1]/nod[1], com_discr/nod[1]))
                    else:
                        print("x1,2 = (%.6g \u00B1 %.6gi)/%.6g" % (-dic[1]/nod[1], com_discr/nod[1], denominator/nod[1]))
                else:
                    print("x1,2 = (%.6g \u00B1 %.6gi)/%.6g" % (-dic[1], com_discr, denominator))

    except Exception as e:
        print(e, end='. ')
        print("Input Error")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        core(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-v":
        VERBOSE = True
        core(sys.argv[2])
    else:
        print("Wrong number of arguments.")


