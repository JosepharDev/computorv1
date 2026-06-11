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
        # put left side to the scale
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
    # Standardize the string to uppercase and remove spaces
    side_str = side_str.replace(" ", "").upper()
    terms = {}
    
    # Handle subtraction by replacing '-' with '+-'
    side_str = side_str.replace("-", "+-")
    raw_terms = side_str.split("+")
    
    for term in raw_terms:
        if term == "":
            continue
            
        # Check if the term has the strict "*X^" format
        if "*X^" not in term:
            # FALLBACK: Is it a bare number like the '0' after the '=' sign?
            try:
                coeff = float(term)
                power = 0  # A bare number mathematically has an X^0 power
            except ValueError:
                # If it's not a valid number either, throw the strict error
                print(f"Error: Invalid format in term '{term}'. Expected a * X^p or a constant.")
                sys.exit(1)
        else:
            # If it has the correct format, split and extract
            parts = term.split('*X^')
            coeff = float(parts[0])
            power = int(parts[1])
            
        # Add the parsed term to our dictionary
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
        # --- THE FIX: Round away floating point noise ---
        coeff = round(coeffs[power], 6)
        
        if coeff != 0:
            # If it is a clean integer (e.g., 5.0), convert to int (5)
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
    # We use absolute values because signs don't matter for finding the divisor
    a = abs(int(a))
    b = abs(int(b))
    while b != 0:
        remainder = a % b
        a = b
        b = remainder
    return a

def my_sqrt(n):
    # Edge case 1: Negative numbers don't have real square roots
    if n < 0:
        return -1.0 # Or you can raise an Exception, depending on how you want to handle it
        
    # Edge case 2: The square root of 0 is 0
    if n == 0:
        return 0.0
        
    # Step 1: Start with a reasonable guess (half the number is a safe start)
    guess = n / 2.0
    
    # We loop up to 100 times, though it usually finds the answer in less than 10
    for _ in range(100):
        # Step 2 & 3 & 4: Calculate the average of the guess and (n / guess)
        new_guess = (guess + (n / guess)) / 2.0
        
        # If the new guess is practically identical to the old guess, we found it!
        # We check if the difference is tiny (e.g., less than 0.00001)
        # We don't use `==` because floating-point math can be slightly imprecise
        difference = guess - new_guess
        if difference < 0: # Make sure difference is positive (absolute value)
            difference = -difference
            
        if difference < 0.000001:
            break
            
        # Update the guess for the next loop
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
        
        # --- THE FIX: Round away the floating point noise first! ---
        r_num = round(-b, 6)
        i_num = round(sqrt_d, 6)
        denom = round(2 * a, 6)
        
        # Now the integer check will work perfectly
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