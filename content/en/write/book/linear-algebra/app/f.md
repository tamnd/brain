---
title: "Appendix F. Numerical Computation"
---

# Appendix F. Numerical Computation

Linear algebra has an exact theory and a numerical practice. The exact theory treats numbers as exact objects. The numerical practice works with finite representations on a computer.

This distinction matters. A matrix identity may be true in exact arithmetic, while its computed version may contain rounding error. Numerical computation studies how to obtain useful answers despite finite precision, limited memory, and finite time.

Most modern numerical computing uses floating-point arithmetic. Floating-point systems represent real numbers with a finite number of digits and an exponent, similar to scientific notation. The IEEE 754 standard defines common formats, rounding behavior, infinities, and special values such as NaN.

## F.1 Exact Arithmetic and Floating-Point Arithmetic

In exact arithmetic, the expression

$$
\frac{1}{3}+\frac{1}{3}+\frac{1}{3}
$$

equals

$$
1.
$$

On a computer using finite decimal or binary representation, the number \(1/3\) usually cannot be represented exactly. The stored value is rounded. After arithmetic operations, additional rounding may occur.

Floating-point arithmetic represents numbers in the form

$$
\pm m \times \beta^e,
$$

where \(m\) is the significand, \(\beta\) is the base, and \(e\) is the exponent. In most hardware arithmetic, the base is \(2\). Floating-point numbers can represent very small and very large quantities, but only finitely many values are representable.

Thus numerical computation replaces exact real arithmetic by approximate arithmetic.

## F.2 Rounding

When an exact real number cannot be represented in a floating-point system, it is rounded to a nearby representable number.

If \(x\) is a real number, let

$$
\operatorname{fl}(x)
$$

denote the floating-point number obtained by rounding \(x\).

For a basic operation \(\circ\), such as addition or multiplication, one often models floating-point arithmetic as

$$
\operatorname{fl}(a \circ b) =
(a \circ b)(1+\delta),
$$

where

$$
|\delta| \leq u.
$$

The number \(u\) is called the unit roundoff. It measures the relative size of one rounding error.

This model is not a complete description of every floating-point situation, but it is useful for analyzing many algorithms.

## F.3 Absolute Error and Relative Error

Let \(x\) be the exact value and let \(\widehat{x}\) be a computed approximation.

The absolute error is

$$
|x-\widehat{x}|.
$$

The relative error is

$$
\frac{|x-\widehat{x}|}{|x|}
$$

when \(x\neq 0\).

Absolute error measures error in the original units. Relative error measures error compared with the size of the true value.

For example, an error of \(10^{-3}\) is small when approximating \(1000\), but large when approximating \(10^{-5}\). Relative error captures this distinction.

## F.4 Significant Digits

A computed value has many correct significant digits when its relative error is small.

Roughly, if

$$
\frac{|x-\widehat{x}|}{|x|}\approx 10^{-k},
$$

then \(\widehat{x}\) has about \(k\) correct decimal digits.

For example, if

$$
x=3.14159265
$$

and

$$
\widehat{x}=3.1416,
$$

then the approximation has several correct leading digits.

Significant digits are a practical way to describe numerical quality, but error bounds are more precise.

## F.5 Cancellation

Cancellation occurs when two nearly equal numbers are subtracted.

For example,

$$
1.000001 - 1.000000 = 0.000001.
$$

If the inputs have already been rounded, their leading digits cancel, and the remaining result may contain few accurate digits.

Cancellation is dangerous when the result is small relative to the operands. It often appears in formulas that subtract nearly equal quantities.

### Example

The expression

$$
\sqrt{x+1}-\sqrt{x}
$$

suffers cancellation when \(x\) is large. A more stable form is obtained by multiplying by the conjugate:

$$
\sqrt{x+1}-\sqrt{x} =
\frac{1}{\sqrt{x+1}+\sqrt{x}}.
$$

Both expressions are algebraically equal in exact arithmetic, but the second is usually better numerically for large \(x\).

## F.6 Conditioning

Conditioning is a property of a problem, not of an algorithm.

A problem is well-conditioned if small changes in the input cause small changes in the output. It is ill-conditioned if small input changes can cause large output changes.

For a scalar function \(f\), the relative condition number at \(x\) is often measured by

$$
\kappa(x) =
\left|
\frac{x f'(x)}{f(x)}
\right|,
$$

when the expression is defined.

A large condition number means the problem is sensitive. Even a perfect algorithm cannot recover information that has been lost through input uncertainty.

In linear systems, conditioning is measured by the condition number of the matrix.

## F.7 Matrix Condition Number

For an invertible matrix \(A\), the condition number with respect to a matrix norm is

$$
\kappa(A)=\|A\|\,\|A^{-1}\|.
$$

If \(\kappa(A)\) is close to \(1\), the system

$$
Ax=b
$$

is well-conditioned. If \(\kappa(A)\) is large, small perturbations in \(A\) or \(b\) may cause large changes in the solution \(x\).

The condition number explains why some linear systems are difficult to solve accurately. The difficulty comes from the geometry of the problem itself.

## F.8 Stability

Stability is a property of an algorithm.

An algorithm is stable if it does not greatly amplify rounding errors. An unstable algorithm may give poor answers even for well-conditioned problems.

It is useful to separate two questions.

| Question | Concept |
|---|---|
| Is the problem sensitive to input changes? | Conditioning |
| Does the algorithm control rounding error? | Stability |

A well-conditioned problem solved by a stable algorithm usually gives an accurate answer. An ill-conditioned problem may give inaccurate answers even when the algorithm is stable.

## F.9 Forward Error and Backward Error

Forward error compares the computed answer with the exact answer.

If \(x\) is the exact solution and \(\widehat{x}\) is the computed solution, the forward error is

$$
\|x-\widehat{x}\|.
$$

Backward error asks a different question: for what nearby problem is the computed answer exact?

For a linear system, if

$$
A\widehat{x}\neq b,
$$

then backward error measures how much \(A\) or \(b\) must be changed so that \(\widehat{x}\) becomes an exact solution.

A backward stable algorithm produces the exact solution to a nearby problem. This is a strong and useful guarantee.

## F.10 Residuals

For a computed solution \(\widehat{x}\) to

$$
Ax=b,
$$

the residual is

$$
r=b-A\widehat{x}.
$$

If \(r=0\), then \(\widehat{x}\) solves the system exactly.

A small residual means

$$
A\widehat{x}
$$

is close to \(b\). However, a small residual does not always imply a small error in \(\widehat{x}\). If \(A\) is ill-conditioned, a small residual may still correspond to a large solution error.

Residuals are easy to compute and widely used as stopping criteria in iterative methods.

## F.11 Norms in Numerical Computation

Norms measure the size of vectors and matrices.

Common vector norms include:

| Norm | Formula |
|---|---|
| \(1\)-norm | \(\|x\|_1=\sum_i |x_i|\) |
| \(2\)-norm | \(\|x\|_2=\sqrt{\sum_i |x_i|^2}\) |
| \(\infty\)-norm | \(\|x\|_\infty=\max_i |x_i|\) |

Common matrix norms include:

| Norm | Meaning |
|---|---|
| \(1\)-norm | Maximum absolute column sum |
| \(\infty\)-norm | Maximum absolute row sum |
| \(2\)-norm | Largest singular value |
| Frobenius norm | Square root of sum of squared entries |

Norms are used to measure error, residuals, perturbations, and convergence.

## F.12 Machine Epsilon

Machine epsilon is commonly used to describe floating-point precision. Informally, it is the distance from \(1\) to the next larger representable floating-point number in a given format.

For IEEE double precision, machine epsilon is approximately

$$
2.22\times 10^{-16}.
$$

For IEEE single precision, it is approximately

$$
1.19\times 10^{-7}.
$$

Unit roundoff is often half of machine epsilon when rounding to nearest is used. Authors sometimes use the terms differently, so one should check the convention in a given text.

## F.13 Overflow, Underflow, and NaN

Floating-point systems have finite range.

Overflow occurs when a result is too large to represent. Underflow occurs when a result is too small in magnitude to represent normally.

IEEE-style floating-point arithmetic also includes special values:

| Value | Meaning |
|---|---|
| \(+\infty\) | Positive overflow or exact infinite result |
| \(-\infty\) | Negative overflow or exact infinite result |
| NaN | Not a Number |
| Signed zero | Distinguishes \(+0\) and \(-0\) |
| Subnormal numbers | Very small numbers with reduced precision |

These values are part of practical numerical computation. They allow many operations to continue after exceptional events, but they also require care.

## F.14 Scaling

Scaling changes the magnitude of a problem without changing its essential mathematical content.

For example, a linear system may be difficult to solve numerically if one row contains entries near \(10^{12}\) and another row contains entries near \(10^{-12}\). Row or column scaling can reduce the range of magnitudes.

Scaling is used to reduce overflow, underflow, and loss of precision. It is also used before computing norms, factorizations, and eigenvalues.

Good numerical software often applies scaling internally.

## F.15 Pivoting

Gaussian elimination may fail or become inaccurate if it divides by a small pivot.

Partial pivoting swaps rows so that a larger pivot is used. In each column, the algorithm selects an entry of large magnitude below or at the current pivot position and swaps that row into place.

Pivoting improves numerical stability. It also avoids division by zero when a nonzero pivot can be found by row exchange.

In exact arithmetic, row exchanges may seem like bookkeeping. In floating-point arithmetic, they are a stability mechanism.

## F.16 Dense and Sparse Computation

A dense matrix stores most of its entries explicitly. A sparse matrix has many zero entries and stores only the nonzero structure.

Dense algorithms are appropriate when most entries are nonzero. Sparse algorithms are appropriate when the matrix has few nonzero entries relative to its size.

| Matrix type | Storage | Typical algorithms |
|---|---|---|
| Dense | All entries | LU, QR, SVD |
| Sparse | Nonzero entries and indices | Sparse LU, iterative methods, Krylov methods |

Sparse computation is essential for large graphs, finite element methods, optimization, and scientific simulations.

## F.17 Direct and Iterative Methods

A direct method solves a problem by a finite sequence of algebraic operations. Gaussian elimination, LU decomposition, QR decomposition, and Cholesky decomposition are direct methods.

An iterative method starts from an initial approximation and improves it repeatedly. Jacobi, Gauss-Seidel, conjugate gradient, GMRES, and power iteration are iterative methods.

| Method class | Strength | Limitation |
|---|---|---|
| Direct | Predictable, accurate for moderate size | Can require large memory |
| Iterative | Scales to large sparse problems | Needs convergence control |

The choice depends on matrix size, sparsity, conditioning, and required accuracy.

## F.18 Complexity

Computational complexity estimates the cost of an algorithm.

For dense \(n\times n\) matrices, classical matrix multiplication costs

$$
O(n^3)
$$

arithmetic operations.

Gaussian elimination also costs

$$
O(n^3)
$$

operations for dense square systems.

Matrix-vector multiplication with a dense \(n\times n\) matrix costs

$$
O(n^2).
$$

If the matrix is sparse with \(m\) nonzero entries, matrix-vector multiplication costs approximately

$$
O(m).
$$

These estimates describe scaling behavior. Actual runtime also depends on memory access, cache behavior, parallelism, and hardware.

## F.19 Memory and Data Movement

Modern numerical computation is often limited by memory movement rather than arithmetic.

A processor can perform many arithmetic operations per second, but moving data between memory hierarchy levels can be expensive. Efficient algorithms use blocking, cache-aware layouts, and batched operations to reuse data.

For example, matrix multiplication can be organized so that blocks of matrices remain in fast cache while many arithmetic operations are performed on them. This is one reason high-quality numerical libraries can be much faster than straightforward code.

## F.20 Reproducibility

Floating-point arithmetic is not always reproducible across platforms or execution orders.

Addition is associative in exact arithmetic:

$$
(a+b)+c=a+(b+c).
$$

In floating-point arithmetic, this identity may fail because rounding occurs after each operation.

Parallel computations often sum terms in different orders. This can produce slightly different results.

Reproducible numerical computation requires controlled rounding, deterministic reduction order, fixed libraries, or compensated algorithms.

## F.21 Compensated Summation

Ordinary summation can accumulate rounding error. Compensated summation keeps an additional correction term.

The Kahan summation algorithm is a common example. It improves the accuracy of summing many floating-point numbers by tracking small errors lost during addition.

Compensated techniques are useful when many numbers of different magnitudes are added. They do not make arithmetic exact, but they often reduce error substantially.

## F.22 Numerical Software

Numerical linear algebra is usually implemented through specialized libraries.

Common examples include BLAS, LAPACK, SuiteSparse, ARPACK, and vendor-optimized libraries. These libraries encode decades of work on algorithms, memory layout, stability, and hardware performance.

For most serious numerical work, one should use tested numerical libraries rather than writing basic matrix algorithms from scratch.

The reason is not only speed. Correct numerical behavior depends on pivoting, scaling, blocking, tolerance selection, and error handling.

## F.23 Tolerances

Because computed values are approximate, numerical algorithms often compare quantities to a tolerance.

Instead of testing

$$
x=0,
$$

one may test

$$
|x| \leq \tau,
$$

where \(\tau\) is a chosen tolerance.

A good tolerance depends on the scale of the problem. Absolute tolerances alone may fail when values are very large or very small. Relative tolerances account for magnitude.

A common pattern is

$$
|x-\widehat{x}|
\leq
\tau_{\mathrm{abs}}
+
\tau_{\mathrm{rel}} |x|.
$$

This combines absolute and relative error control.

## F.24 Summary

Numerical computation studies how mathematical procedures behave when implemented with finite precision and finite resources.

The main ideas are:

| Concept | Meaning |
|---|---|
| Floating-point arithmetic | Finite approximation to real arithmetic |
| Rounding | Replacement by nearby representable values |
| Absolute error | Error measured in original units |
| Relative error | Error measured relative to the exact value |
| Cancellation | Loss of significant digits in subtraction |
| Conditioning | Sensitivity of the mathematical problem |
| Stability | Error behavior of the algorithm |
| Residual | Failure of a computed solution to satisfy the equation |
| Pivoting | Row exchange for stable elimination |
| Scaling | Magnitude adjustment for numerical reliability |
| Sparse computation | Exploiting zero structure |
| Tolerance | Practical replacement for exact comparison |

Exact linear algebra explains what should be true. Numerical linear algebra explains what can be computed reliably. Both viewpoints are necessary for using linear algebra in scientific computing, data analysis, engineering, and large-scale simulation.