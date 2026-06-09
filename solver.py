import sys


class PolynomialSolver:

    def __init__(self, equation_string):
        self.equation_string = equation_string
        self.coeffs = {}

    def run(self):
        try:
            left, right = self._parse_equation()
            self.coeffs = self._reduce(left, right)
            self._solve()
        except Exception as e:
            self._error(e)

    def _parse_equation(self):
        if "=" not in self.equation_string:
            self._error("equation should have = sign")
        left_str, right_str = self.equation_string.split("=", 1)
        return self._parse_side(left_str), self._parse_side(right_str)

    def _parse_side(self, side_str):
        side_str = side_str.strip()
        if side_str == "0":
            return [(0.0, 0)]
        terms = []
        side_str = side_str.replace(" - ", " + -")
        for part in side_str.split(" + "):
            piece = part.strip()
            if piece == "0":
                continue
            terms.append(self._parse_term(piece))
        return terms

    @staticmethod
    def _parse_term(term):
        coeff_str, x_str = term.split(" * ")
        coeff = float(coeff_str)
        power = int(x_str.split("^")[1])
        return coeff, power

    def _reduce(self, left, right):
        coeffs = {}
        for coeff, power in left:
            coeffs[power] = coeffs.get(power, 0) + coeff
        for coeff, power in right:
            coeffs[power] = coeffs.get(power, 0) - coeff
        return coeffs


    def _solve(self):
        self._print_reduced()
        degree = self._degree()
        print(f"Polynomial degree: {degree}")
        if degree > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
        elif degree == 2:
            self._solve_degree2()
        elif degree == 1:
            self._solve_degree1()
        else:
            self._solve_degree0()


    def _solve_degree0(self):
        if self.coeffs.get(0, 0) == 0:
            print("Any real number is a solution.")
        else:
            print("No solution.")

    def _solve_degree1(self):
        b = self.coeffs.get(1, 0)
        c = self.coeffs.get(0, 0)
        print("The solution is:")
        print(-c / b)

    def _solve_degree2(self):
        a = self.coeffs.get(2, 0)
        b = self.coeffs.get(1, 0)
        c = self.coeffs.get(0, 0)
        delta = b * b - 4 * a * c

        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sqrt_d = delta ** 0.5
            print(round((-b + sqrt_d) / (2 * a), 6))
            print(round((-b - sqrt_d) / (2 * a), 6))
        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            print(round(-b / (2 * a), 6))
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")
            sqrt_d = (-delta) ** 0.5
            real = round(-b / (2 * a), 6)
            imag = round(sqrt_d / (2 * a), 6)
            print(f"{real} + {imag}i")
            print(f"{real} - {imag}i")



    def _degree(self):
        return max(
            (p for p, c in self.coeffs.items() if c != 0),
            default=0,
        )

    def _print_reduced(self):
        terms = []
        for power in sorted(self.coeffs):
            c = self.coeffs[power]
            if not terms:
                terms.append(f"{self._fmt(c)} * X^{power}")
            elif c < 0:
                terms.append(f"- {self._fmt(abs(c))} * X^{power}")
            else:
                terms.append(f"+ {self._fmt(c)} * X^{power}")
        print("Reduced form: " + " ".join(terms) + " = 0")

    @staticmethod
    def _fmt(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        if isinstance(value, int):
            return str(value)
        return str(round(value, 6)).rstrip("0").rstrip(".")

    @staticmethod
    def _error(msg):
        sep = "-" * 20
        print(f"{sep}\nError:  {msg}\n{sep}")
        sys.exit(1)




if __name__ == "__main__":
    equation = sys.argv[1] if len(sys.argv) == 2 else input("insert the equation: ")
    PolynomialSolver(equation).run()