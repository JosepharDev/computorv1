import sys


def run(equation_line):
    try:
        left, right = parse_equation(equation_line)
        coeffs = reduce(left, right)
        solve(coeffs)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

def reduce(left, right):
    coeffs = {}
    for power, coeff in left.items():
        coeffs[power] = coeffs.get(power, 0) + coeff
        
    for power, coeff in right.items():
        coeffs[power] = coeffs.get(power, 0) - coeff
        

    return coeffs

def parse_equation(equation_string):
    if "=" not in equation_string:
        print("equation should have = sign")
        sys.exit(1)
        
    left_str, right_str = equation_string.split("=", 1)
    return parse_side(left_str), parse_side(right_str)


def parse_side(side_str):
    side_str = side_str.replace(" ", "").upper()
    terms = {}
    
    side_str = side_str.replace("-", "+-")
    raw_terms = side_str.split("+")
    
    for term in raw_terms:
        if term == "":
            continue
            
        if "*X^" not in term:
            try:
                coeff = float(term)
                power = 0
            except ValueError:
                print(f"Error: Invalid format in term '{term}'. Expected a * X^p or a constant.")
                sys.exit(1)
        else:
            parts = term.split('*X^')
            coeff = float(parts[0])
            power = int(parts[1])
            
        terms[power] = terms.get(power, 0) + coeff
        
    return terms

def get_degree(coeffs):
    degree = 0
    for power, coeff in coeffs.items():
        if coeff != 0 and power > degree:
            degree = power
    return degree


def print_reduced(coeffs):
    terms = []
    for power in sorted(coeffs.keys()):
        coeff = round(coeffs[power], 6)
        
        if coeff != 0:
            if coeff.is_integer():
                coeff = int(coeff)
            terms.append(f"{coeff} * X^{power}")
            
    if not terms:
        print("Reduced form: 0 * X^0 = 0")
    else:
        equation_str = " + ".join(terms)
        equation_str = equation_str.replace("+ -", "- ")
        print(f"Reduced form: {equation_str} = 0")

def gcd(a, b):
    a = abs(int(a))
    b = abs(int(b))
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return a

def my_sqrt(n):
    if n == 0:
        return 0.0
        
    guess = n / 2.0
    precision = 0.00001
    for _ in range(100):
        new_guess = (guess + (n / guess)) / 2.0
        
        if abs(guess - new_guess) < precision:
            return new_guess
            
        guess = new_guess
        
    return guess
        
def solve(coeffs):
    print_reduced(coeffs)
    degree = get_degree(coeffs)
    print(f"Polynomial degree: {degree}")
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    elif degree == 2:
        solve_degree2(coeffs)
    elif degree == 1:
        solve_degree1(coeffs)
    else:
        solve_degree0(coeffs)


def solve_degree0(coeffs):
    if coeffs.get(0, 0) == 0:
        print("Any real number is a solution.")
    else:
        print("No solution.")

def solve_degree1(coeffs):
    b = coeffs.get(1, 0)
    c = coeffs.get(0, 0)
    print("The solution is:")
    print(-c / b)

def solve_degree2(coeffs):
    a = coeffs.get(2, 0)
    b = coeffs.get(1, 0)
    c = coeffs.get(0, 0)
    delta = b * b - 4 * a * c

    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        sqrt_d = my_sqrt(delta)
        print(round((-b + sqrt_d) / (2 * a), 6))
        print(round((-b - sqrt_d) / (2 * a), 6))
        
    elif delta == 0:
        print("Discriminant is zero, the solution is:")
        print(round(-b / (2 * a), 6))
        
    else:
        print("Discriminant is strictly negative, the two complex solutions are:")
        sqrt_d = my_sqrt(-delta)
        
        r_num = round(-b, 6)
        i_num = round(sqrt_d, 6)
        denom = round(2 * a, 6)
        
        if r_num.is_integer() and i_num.is_integer() and denom.is_integer():
            g_real = gcd(r_num, denom)
            g_imag = gcd(i_num, denom)
            
            real_frac = f"{int(r_num)//g_real}/{int(denom)//g_real}"
            imag_frac = f"{int(i_num)//g_imag}/{int(denom)//g_imag}"
            
            print(f"{real_frac} + {imag_frac}i")
            print(f"{real_frac} - {imag_frac}i")
        else:
            real = round(-b / (2 * a), 6)
            imag = round(sqrt_d / (2 * a), 6)
            print(f"{real} + {imag}i")
            print(f"{real} - {imag}i")



if __name__ == "__main__":
    equation = sys.argv[1] if len(sys.argv) == 2 else input("insert the equation: ")
    run(equation)