import unittest
from io import StringIO
from contextlib import redirect_stdout

import solver


class TestComputorV1Mandatory(unittest.TestCase):
    def run_case(self, equation: str) -> str:
        buffer = StringIO()
        with redirect_stdout(buffer):
            solver.run(equation)
        return buffer.getvalue()

    def test_degree_0_any_real_solution(self):
        out = self.run_case("6 * X^0 = 6 * X^0")
        self.assertIn("Reduced form:", out)
        self.assertIn("Polynomial degree: 0", out)
        self.assertIn("Any real number is a solution.", out)

    def test_degree_0_no_solution(self):
        out = self.run_case("6 * X^0 = 7 * X^0")
        self.assertIn("Polynomial degree: 0", out)
        self.assertIn("No solution.", out)

    def test_degree_1_solution(self):
        out = self.run_case("5 * X^0 + 4 * X^1 = 4 * X^0")
        self.assertIn("Reduced form:", out)
        self.assertIn("Polynomial degree: 1", out)
        self.assertIn("The solution is:", out)
        self.assertIn("-0.25", out)

    def test_degree_2_positive_discriminant(self):
        out = self.run_case("5 * X^0 + 4 * X^1 - 9 * X^2 = 1 * X^0")
        self.assertIn("Reduced form:", out)
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is strictly positive", out)

    def test_degree_2_zero_discriminant(self):
        out = self.run_case("1 * X^0 + 2 * X^1 + 1 * X^2 = 0")
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is zero", out)
        self.assertIn("-1.0", out)

    def test_degree_2_negative_discriminant(self):
        out = self.run_case("1 * X^0 + 2 * X^1 + 5 * X^2 = 0")
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is strictly negative", out)
        self.assertIn("i", out)

    def test_degree_greater_than_2(self):
        out = self.run_case("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
        self.assertIn("Polynomial degree: 3", out)
        self.assertIn("I can't solve.", out)
    
    def test_linear_no_x_term(self):
        out = self.run_case("5 * X^0 = 2 * X^0")
        self.assertIn("Polynomial degree: 0", out)
        self.assertIn("No solution.", out)

    def test_quadratic_two_real_solutions(self):
        out = self.run_case("1 * X^2 - 3 * X^1 + 2 * X^0 = 0")
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is strictly positive", out)
        self.assertIn("2.0", out)
        self.assertIn("1.0", out)

    def test_zero_polynomial(self):
        out = self.run_case("0 * X^0 = 0")
        self.assertIn("Reduced form:", out)
        self.assertIn("Polynomial degree: 0", out)
        self.assertIn("Any real number is a solution.", out)

    def test_linear_negative_solution(self):
        out = self.run_case("2 * X^1 = 6 * X^0")
        self.assertIn("Polynomial degree: 1", out)
        self.assertIn("The solution is:", out)
        self.assertIn("3", out)
        
    def test_quadratic_one_real_solution(self):
        out = self.run_case("1 * X^2 - 2 * X^1 + 1 * X^0 = 0")
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is zero", out)
        self.assertIn("1.0", out)

    def test_quadratic_negative_discriminant_contains_complex(self):
        out = self.run_case("1 * X^2 + 0 * X^1 + 1 * X^0 = 0")
        self.assertIn("Polynomial degree: 2", out)
        self.assertIn("Discriminant is strictly negative", out)
        self.assertIn("i", out)

    def test_degree_three_rejected(self):
        out = self.run_case("1 * X^3 + 2 * X^2 + 3 * X^1 + 4 * X^0 = 0")
        self.assertIn("Polynomial degree: 3", out)
        self.assertIn("I can't solve.", out)

    def test_mixed_terms_reduce_correctly(self):
        out = self.run_case("3 * X^2 + 2 * X^1 - 5 * X^2 + 7 * X^0 = 1 * X^0")
        self.assertIn("Reduced form:", out)
        self.assertIn("Polynomial degree:", out)


if __name__ == "__main__":
    unittest.main()