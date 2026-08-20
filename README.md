<div align="center">

# ⚡ ComputorV1

### A polynomial equation solver — built from scratch, no math libraries.

[![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![School](https://img.shields.io/badge/School-42-000000?style=for-the-badge)](https://42.fr)
[![Grade](https://img.shields.io/badge/Grade-100%2F100-brightgreen?style=for-the-badge)]()

</div>

---

## 📖 About

**ComputorV1** is a 42 school project that reimplements polynomial equation solving **from the ground up** — no `math` library, no `cmath`, no shortcuts. It parses, reduces, and solves polynomial equations of degree 0, 1, and 2, complete with discriminant analysis and complex number support.

> *"The first in a series that aims to make you rekindle with maths."*

---

## 🧮 How It Works

The solver operates in three distinct phases:

```
Input equation  →  Parse  →  Reduce  →  Solve  →  Output
```

| Phase | Description |
|-------|-------------|
| **Parse** | Splits the equation on `=`, tokenizes each side into `coefficient * X^power` terms |
| **Reduce** | Moves all terms to the left-hand side and sums like powers |
| **Solve** | Dispatches to the appropriate solver based on the polynomial degree |

---

## ✨ Features

- ✅ **Degree 0** — detects trivial identities and contradictions
- ✅ **Degree 1** — solves linear equations `ax + b = 0`
- ✅ **Degree 2** — solves quadratic equations using the discriminant (Δ)
  - Δ > 0 → two real solutions
  - Δ = 0 → one repeated real solution
  - Δ < 0 → two complex conjugate solutions (displayed as fractions when possible)
- ✅ **Degree > 2** — gracefully refuses with a clear message
- ✅ **Custom square root** — implemented via Newton-Raphson iteration (no `math.sqrt`)
- ✅ **Fraction simplification** — uses GCD to display complex solutions as exact fractions
- ✅ **Robust parsing** — handles negative coefficients, constants, and malformed input

---

## 🚀 Usage

```bash
python3 computor.py "<equation>"
```

The equation must follow the format `a * X^p + ... = b * X^q + ...`

> **Note:** The solver is case-insensitive — `X` and `x` are both accepted.

---

## 🎯 Examples

### Degree 0 — No solution
```bash
$ python3 computor.py "6 * X^0 = 7 * X^0"
Reduced form: -1 * X^0 = 0
Polynomial degree: 0
No solution.
```

### Degree 0 — Infinite solutions
```bash
$ python3 computor.py "6 * X^0 = 6 * X^0"
Reduced form: 0 * X^0 = 0
Polynomial degree: 0
Any real number is a solution.
```

### Degree 1 — Linear
```bash
$ python3 computor.py "5 * X^0 + 4 * X^1 = 4 * X^0"
Reduced form: 1 * X^0 + 4 * X^1 = 0
Polynomial degree: 1
The solution is:
-0.25
```

### Degree 2 — Two real solutions (Δ > 0)
```bash
$ python3 computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
0.905239
-0.475131
```

### Degree 2 — One repeated solution (Δ = 0)
```bash
$ python3 computor.py "1 * X^0 + 2 * X^1 + 1 * X^2 = 0"
Reduced form: 1 * X^0 + 2 * X^1 + 1 * X^2 = 0
Polynomial degree: 2
Discriminant is zero, the solution is:
-1.0
```

### Degree 2 — Complex solutions (Δ < 0)
```bash
$ python3 computor.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
Reduced form: 1 * X^0 + 2 * X^1 + 5 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly negative, the two complex solutions are:
-1/5 + 2/5i
-1/5 - 2/5i
```

### Degree > 2 — Unsolvable
```bash
$ python3 computor.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
Reduced form: 5 * X^0 - 6 * X^1 - 5.6 * X^3 = 0
Polynomial degree: 3
The polynomial degree is strictly greater than 2, I can't solve.
```

---

## 🧪 Testing

A test suite is included covering all edge cases:

```bash
python3 -m pytest test.py -v
```

| Test Category | Cases |
|---|---|
| Degree 0 | identity, contradiction, zero polynomial |
| Degree 1 | positive solution, negative solution |
| Degree 2 | Δ > 0, Δ = 0, Δ < 0 (real & complex) |
| Degree > 2 | rejection |
| Parsing | multi-term reduction, mixed sides |

---

## 📐 Math Reference

### Quadratic Formula

For `ax² + bx + c = 0`:

```
         -b ± √Δ
x = ───────────────
           2a

where  Δ = b² - 4ac
```

| Discriminant | Nature of roots |
|---|---|
| Δ > 0 | Two distinct real roots |
| Δ = 0 | One repeated real root |
| Δ < 0 | Two complex conjugate roots |

### Square Root (Newton-Raphson)

The custom `my_sqrt(n)` function approximates √n iteratively:

```
x_{n+1} = (x_n + n / x_n) / 2
```

Converges to machine precision in ~100 iterations.

---

## 📁 Project Structure

```
computorv1/
├── computor.py     # Main solver — parse, reduce, solve
├── test.py         # Unit test suite (unittest)
└── subject/
    └── Computorv1.pdf  # Original project subject
```

---

## ⚙️ Implementation Details

| Function | Role |
|---|---|
| `parse_equation()` | Splits on `=`, delegates each side |
| `parse_side()` | Tokenizes terms, handles negatives & constants |
| `reduce()` | Subtracts right-side coefficients from left |
| `get_degree()` | Finds the highest non-zero power |
| `print_reduced()` | Formats and prints the reduced form |
| `solve()` | Dispatcher — calls degree-specific solver |
| `solve_degree0()` | Handles trivial cases |
| `solve_degree1()` | `x = -c / b` |
| `solve_degree2()` | Discriminant method + GCD simplification |
| `my_sqrt()` | Newton-Raphson square root |
| `gcd()` | Euclidean algorithm for fraction reduction |

---

<div align="center">

Made with 🧠 as part of the **42 school** curriculum

</div>
