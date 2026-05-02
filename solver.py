import sys

def print_error(err_msg):
    print("-"*20)
    print(f"Error:  {err_msg}")
    print("-"*20)
    exit(1)

def print_reduced(coeffs):
    terms = []
    for power in sorted(coeffs.keys()):
        c = coeffs[power]
        terms.append(f"{c} * X^{power}")
    print("Reduced form: " + " + ".join(terms) + " = 0")

def get_degree(coeffs):
    degree = 0
    for power, coeff in coeffs.items():
        if coeff != 0 and power > degree:
            degree = power
    return degree

def my_sqrt(n):
    if n < 0:
        print("Cannot sqrt a negative number here")
        exit(1)
    if n == 0:
        return 0.0
    guess = n / 2.0
    for _ in range(1000):
        better = (guess + n / guess) / 2.0
        if abs(better - guess) < 1e-10:
            break
        guess = better
    return guess

def parse_term(term):
    p = term.split(" * ")
    print(p, term)
    coeff = float(p[0])
    power = int(p[1].split('^')[1])
    return coeff, power
    

def parse_side(side_str):
    terms = []
    side_str = side_str.replace(" - ", " + -")
    parts  = side_str.split(" + ")
    for p in parts:
        coeff, power = parse_term(p.strip())
        terms.append((coeff, power))
    return terms


def parse_equation(equation_string):
    if "=" not in equation_string:
        print_error("equation should have = sign")
    sides = equation_string.split("=")
    left = parse_side(sides[0])
    right = parse_side(sides[1])
    return left, right

def reduce_equation(left, right):
    coeffs = {}
    
    for coeff, power in left:
        coeffs[power] = coeffs.get(power,0) + coeff
    
    for coeff, power in right:
        coeffs[power] = coeffs.get(power, 0) - coeff
    return coeffs

def solve_degree0(coeffs):
    c = coeffs.get(0, 0)
    if c == 0:
        print("Any real number is a solution.")
    else:
        print("No solution.")

def solve_degree1(coeffs):
    b = coeffs.get(1, 0)   # coefficient of X^1
    c = coeffs.get(0, 0)   # coefficient of X^0

    # X = -c / b
    solution = -c / b
    print("The solution is:")
    print(solution)

def gcd(a, b):
    a, b = abs(a), abs(b)
    while b: a, b = b, a % b
    return a

def solve_degree2(coeffs):
    a = coeffs.get(2, 0)
    b = coeffs.get(1, 0)
    c = coeffs.get(0, 0)

    delta = b*b - 4*a*c       # Δ = b² - 4ac

    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        sqrt_d = my_sqrt(delta)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        print(round(x1, 6))
        print(round(x2, 6))

    elif delta == 0:
        print("Discriminant is zero, the solution is:")
        x = -b / (2 * a)
        print(round(x, 6))

    else:                          # delta < 0 → complex!
        print("Discriminant is strictly negative, the two complex solutions are:")
        sqrt_d = my_sqrt(-delta)   # √|Δ|
        real_part = -b / (2*a)
        imag_part = sqrt_d / (2*a)
        # Show as fractions: numerator/denominator
        denom = 2 * int(a)
        r_num = int(-b)
        i_num = int(sqrt_d)
        g1 = gcd(r_num, denom); g2 = gcd(i_num, denom)
        print(f"{r_num//g1}/{denom//g1} + {i_num//g2}i/{denom//g2}")
        print(f"{r_num//g1}/{denom//g1} - {i_num//g2}i/{denom//g2}")

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

def main(equation):
    try:
        left, right = parse_equation(equation)
        coeffs = reduce_equation(left, right)
        solve(coeffs)
    except Exception as e:
        print_error(e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        equation = sys.argv[1]
    else:
        equation = input("insert the equation: ")
    main(equation)