---
title: "Appendix D. Polynomial Algebra"
---

# Appendix D. Polynomial Algebra

Polynomials appear throughout linear algebra. Determinants, characteristic polynomials, minimal polynomials, eigenvalues, matrix factorizations, and canonical forms all depend on polynomial algebra.

This appendix develops the basic algebraic properties of polynomials needed later in the book.

## D.1 Polynomials

Let \(F\) be a field. In this book, \(F\) is usually either

$$
\mathbb{R}
\quad \text{or} \quad
\mathbb{C}.
$$

A polynomial in one variable \(x\) over \(F\) is an expression of the form

$$
p(x) =
a_0+a_1x+a_2x^2+\cdots+a_nx^n,
$$

where

$$
a_0,a_1,\ldots,a_n \in F.
$$

The numbers \(a_i\) are called coefficients.

The largest exponent with nonzero coefficient is called the degree of the polynomial. If

$$
a_n \neq 0,
$$

then

$$
\deg(p)=n.
$$

For example,

$$
p(x)=3x^4-2x+7
$$

has degree \(4\).

The zero polynomial is the polynomial whose coefficients are all zero. Its degree is usually left undefined.

The set of all polynomials over \(F\) is denoted by

$$
F[x].
$$

## D.2 Equality of Polynomials

Two polynomials are equal if and only if their corresponding coefficients are equal.

Thus

$$
a_0+a_1x+\cdots+a_nx^n =
b_0+b_1x+\cdots+b_nx^n
$$

if and only if

$$
a_i=b_i
$$

for all \(i\).

For example,

$$
x^2+2x+1
\neq
x^2+1.
$$

Even if two polynomials happen to take the same value at some inputs, they are equal only when all coefficients match.

## D.3 Polynomial Addition

Polynomials are added coefficientwise.

If

$$
p(x)=a_0+a_1x+\cdots+a_nx^n
$$

and

$$
q(x)=b_0+b_1x+\cdots+b_nx^n,
$$

then

$$
p(x)+q(x) =
(a_0+b_0)+(a_1+b_1)x+\cdots+(a_n+b_n)x^n.
$$

Example:

$$
(2x^2+3x+1)+(x^2-5) =
3x^2+3x-4.
$$

Polynomial addition satisfies the same algebraic laws as vector addition.

## D.4 Polynomial Multiplication

Polynomial multiplication uses distributivity.

For example,

$$
(x+2)(x+3) =
x^2+3x+2x+6 =
x^2+5x+6.
$$

In general,

$$
\left(
\sum_{i=0}^m a_ix^i
\right)
\left(
\sum_{j=0}^n b_jx^j
\right) =
\sum_{k=0}^{m+n}
\left(
\sum_{i+j=k} a_ib_j
\right)x^k.
$$

The degree of a product satisfies

$$
\deg(pq)=\deg(p)+\deg(q)
$$

whenever neither polynomial is zero.

## D.5 Powers of Polynomials

If \(p(x)\) is a polynomial and \(k\) is a nonnegative integer, then

$$
p(x)^k
$$

means repeated multiplication:

$$
p(x)^k =
\underbrace{
p(x)p(x)\cdots p(x)
}_{k\text{ times}}.
$$

For example,

$$
(x+1)^2=x^2+2x+1,
$$

and

$$
(x+1)^3=x^3+3x^2+3x+1.
$$

The binomial theorem states that

$$
(x+y)^n =
\sum_{k=0}^n
\binom{n}{k}
x^{n-k}y^k.
$$

This identity appears in expansions and combinatorial arguments.

## D.6 Evaluation of Polynomials

If \(p(x)\in F[x]\) and \(a\in F\), then one may evaluate \(p\) at \(a\):

$$
p(a).
$$

For example, if

$$
p(x)=x^2-3x+2,
$$

then

$$
p(1)=1-3+2=0.
$$

A number \(a\) is called a root or zero of \(p\) if

$$
p(a)=0.
$$

Roots are central in eigenvalue theory because eigenvalues are roots of characteristic polynomials.

## D.7 Factor Theorem

The factor theorem states:

> A number \(a\) is a root of \(p(x)\) if and only if
>
> \[
> (x-a)
> \]
>
> divides \(p(x)\).

Thus,

$$
p(a)=0
\iff
p(x)=(x-a)q(x)
$$

for some polynomial \(q(x)\).

### Example

Let

$$
p(x)=x^2-5x+6.
$$

Since

$$
p(2)=4-10+6=0,
$$

the factor theorem implies

$$
x^2-5x+6=(x-2)(x-3).
$$

The factor theorem is fundamental in polynomial factorization.

## D.8 Polynomial Division

Given polynomials \(p(x)\) and \(d(x)\neq 0\), there exist unique polynomials \(q(x)\) and \(r(x)\) such that

$$
p(x)=d(x)q(x)+r(x),
$$

where either

$$
r(x)=0
$$

or

$$
\deg(r)<\deg(d).
$$

This is the polynomial division algorithm.

### Example

Divide

$$
x^3-1
$$

by

$$
x-1.
$$

The quotient is

$$
x^2+x+1,
$$

because

$$
x^3-1=(x-1)(x^2+x+1).
$$

Polynomial division is analogous to integer division.

## D.9 Greatest Common Divisors

A polynomial \(d(x)\) is a common divisor of \(p(x)\) and \(q(x)\) if

$$
d(x)\mid p(x)
$$

and

$$
d(x)\mid q(x).
$$

The greatest common divisor, denoted

$$
\gcd(p,q),
$$

is the common divisor of largest degree, usually chosen to be monic.

A polynomial is monic if its leading coefficient equals \(1\).

### Example

For

$$
p(x)=x^2-1
$$

and

$$
q(x)=x^2-2x+1,
$$

we have

$$
p(x)=(x-1)(x+1),
$$

$$
q(x)=(x-1)^2.
$$

Thus

$$
\gcd(p,q)=x-1.
$$

Greatest common divisors are important in minimal polynomial theory.

## D.10 Irreducible Polynomials

A nonconstant polynomial is irreducible over \(F\) if it cannot be factored into lower-degree polynomials over \(F\).

### Examples over \(\mathbb{R}\)

| Polynomial | Reducible? |
|---|---|
| \(x^2-1\) | Yes |
| \(x^2+1\) | No |
| \(x^2+4x+4\) | Yes |

Indeed,

$$
x^2-1=(x-1)(x+1),
$$

and

$$
x^2+4x+4=(x+2)^2.
$$

But

$$
x^2+1
$$

has no real roots, so it cannot factor into linear real polynomials.

### Over \(\mathbb{C}\)

The polynomial

$$
x^2+1
$$

factors as

$$
(x-i)(x+i).
$$

Thus irreducibility depends on the field.

## D.11 Fundamental Theorem of Algebra

The fundamental theorem of algebra states:

> Every nonconstant polynomial with complex coefficients has at least one complex root.

Equivalently, every polynomial of degree \(n\geq 1\) over \(\mathbb{C}\) factors completely into linear factors:

$$
p(x) =
a(x-\lambda_1)\cdots(x-\lambda_n).
$$

For example,

$$
x^2+1=(x-i)(x+i).
$$

This theorem is one reason why complex vector spaces have a cleaner spectral theory than real vector spaces. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Fundamental_theorem_of_algebra?utm_source=chatgpt.com))

## D.12 Multiplicity of Roots

Suppose

$$
p(x)=(x-a)^k q(x),
$$

where

$$
q(a)\neq 0.
$$

Then \(a\) is called a root of multiplicity \(k\).

### Example

The polynomial

$$
(x-2)^3(x+1)
$$

has:

| Root | Multiplicity |
|---|---|
| \(2\) | \(3\) |
| \(-1\) | \(1\) |

Repeated roots play an important role in Jordan canonical form and minimal polynomials.

## D.13 Polynomial Functions and Formal Polynomials

A polynomial may be viewed in two ways.

| Viewpoint | Meaning |
|---|---|
| Polynomial function | A rule \(x\mapsto p(x)\) |
| Formal polynomial | A symbolic algebraic object |

In elementary settings, these viewpoints are often identified. However, algebraically they are distinct.

For example, in finite fields different formal polynomials may define the same function.

In linear algebra, the formal viewpoint is important because one substitutes matrices into polynomials.

## D.14 Polynomials of Matrices

If

$$
p(x)=a_0+a_1x+\cdots+a_nx^n
$$

and \(A\) is a square matrix, then define

$$
p(A) =
a_0I+a_1A+\cdots+a_nA^n.
$$

For example, if

$$
p(x)=x^2-3x+2,
$$

then

$$
p(A)=A^2-3A+2I.
$$

This construction is fundamental in matrix theory.

Characteristic polynomials, minimal polynomials, matrix exponentials, and spectral decompositions all use polynomial expressions in matrices.

## D.15 Characteristic Polynomials

If \(A\) is an \(n\times n\) matrix, its characteristic polynomial is

$$
p_A(\lambda)=\det(\lambda I-A).
$$

The roots of this polynomial are the eigenvalues of \(A\).

### Example

Let

$$
A=
\begin{bmatrix}
2 & 0 \\
0 & 3
\end{bmatrix}.
$$

Then

$$
\lambda I-A =
\begin{bmatrix}
\lambda-2 & 0 \\
0 & \lambda-3
\end{bmatrix}.
$$

Thus

$$
p_A(\lambda) =
(\lambda-2)(\lambda-3).
$$

The eigenvalues are

$$
2
\quad \text{and} \quad
3.
$$

Characteristic polynomials connect linear algebra with polynomial algebra.

## D.16 Minimal Polynomials

The minimal polynomial of a matrix \(A\) is the monic polynomial of smallest degree satisfying

$$
m(A)=0.
$$

For example, if

$$
A=
\begin{bmatrix}
2 & 0 \\
0 & 3
\end{bmatrix},
$$

then

$$
(A-2I)(A-3I)=0.
$$

Thus one possible annihilating polynomial is

$$
(x-2)(x-3).
$$

In fact this is the minimal polynomial.

The minimal polynomial divides every polynomial that annihilates \(A\), including the characteristic polynomial.

## D.17 Polynomial Roots and Eigenvalues

The equation

$$
p_A(\lambda)=0
$$

determines the eigenvalues of \(A\).

Thus many matrix problems reduce to polynomial problems.

### Example

Consider

$$
A=
\begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}.
$$

Its characteristic polynomial is

$$
\lambda^2+1.
$$

The roots are

$$
\lambda=i,
\qquad
\lambda=-i.
$$

Therefore \(A\) has no real eigenvalues but has two complex eigenvalues.

This example shows why complex numbers naturally arise in linear algebra.

## D.18 Algebraic and Geometric Multiplicity

If \(\lambda\) is a root of the characteristic polynomial, its multiplicity as a root is called its algebraic multiplicity.

The dimension of the eigenspace associated with \(\lambda\) is called its geometric multiplicity.

These quantities satisfy

$$
1
\leq
\text{geometric multiplicity}
\leq
\text{algebraic multiplicity}.
$$

Equality for every eigenvalue characterizes diagonalizable matrices.

## D.19 Companion Matrices

Every monic polynomial

$$
p(x)=x^n+a_{n-1}x^{n-1}+\cdots+a_1x+a_0
$$

has an associated companion matrix:

$$
C=
\begin{bmatrix}
0 & 0 & \cdots & 0 & -a_0 \\
1 & 0 & \cdots & 0 & -a_1 \\
0 & 1 & \cdots & 0 & -a_2 \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \cdots & 1 & -a_{n-1}
\end{bmatrix}.
$$

The characteristic polynomial of \(C\) is exactly \(p(x)\).

Companion matrices are used in canonical forms and linear recurrence relations.

## D.20 Polynomial Interpolation

Suppose distinct numbers

$$
x_1,\ldots,x_n
$$

and values

$$
y_1,\ldots,y_n
$$

are given.

There exists a unique polynomial of degree at most \(n-1\) satisfying

$$
p(x_i)=y_i
$$

for all \(i\).

This is polynomial interpolation.

Interpolation connects linear algebra with approximation theory because the coefficients of \(p(x)\) satisfy a linear system.

The associated matrix is the Vandermonde matrix:

$$
V=
\begin{bmatrix}
1 & x_1 & x_1^2 & \cdots & x_1^{n-1} \\
1 & x_2 & x_2^2 & \cdots & x_2^{n-1} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_n & x_n^2 & \cdots & x_n^{n-1}
\end{bmatrix}.
$$

## D.21 Polynomial Identities

Several polynomial identities appear repeatedly in linear algebra.

### Difference of squares

### Sum of geometric series

$$
1+x+x^2+\cdots+x^n =
\frac{x^{n+1}-1}{x-1},
\qquad
x\neq 1.
$$

### Binomial expansion

(x+y)^n=\sum_{k=0}^{n}\binom{n}{k}x^{n-k}y^k

These identities simplify determinant computations, matrix powers, and algebraic manipulations.

## D.22 Summary

Polynomial algebra provides the algebraic framework for much of linear algebra.

Key ideas include:

| Concept | Meaning |
|---|---|
| Polynomial | Finite algebraic expression in powers of \(x\) |
| Degree | Largest nonzero exponent |
| Root | Value where \(p(a)=0\) |
| Factor theorem | Roots correspond to linear factors |
| Irreducibility | Cannot factor further |
| Characteristic polynomial | Determines eigenvalues |
| Minimal polynomial | Smallest annihilating polynomial |
| Multiplicity | Repeated root structure |

Polynomials connect algebraic equations with matrix theory. Many questions about matrices reduce to questions about polynomial factorization, roots, and divisibility.