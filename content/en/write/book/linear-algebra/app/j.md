---
title: "Appendix J. Common Identities and Formulas"
---

# Appendix J. Common Identities and Formulas

This appendix collects frequently used identities from linear algebra, matrix algebra, vector calculus, and numerical computation. The goal is reference rather than proof. Most formulas are proved earlier in the text.

## J.1 Algebraic Identities

### Difference of Squares

$$
a^2-b^2=(a-b)(a+b).
$$

### Binomial Expansion

$$
(x+y)^n =
\sum_{k=0}^n
\binom{n}{k}
x^{n-k}y^k.
$$

### Geometric Series

For \(x\neq 1\),

$$
1+x+x^2+\cdots+x^n =
\frac{x^{n+1}-1}{x-1}.
$$

If

$$
|x|<1,
$$

then the infinite series converges:

$$
\sum_{k=0}^{\infty}x^k =
\frac{1}{1-x}.
$$

### Quadratic Formula

For

$$
ax^2+bx+c=0,
\qquad
a\neq 0,
$$

the solutions are

$$
x =
\frac{-b\pm\sqrt{b^2-4ac}}{2a}.
$$

## J.2 Complex Number Identities

For

$$
z=a+bi,
$$

the conjugate is

$$
\overline{z}=a-bi.
$$

### Modulus

$$
|z| =
\sqrt{a^2+b^2}.
$$

### Product with Conjugate

$$
z\overline{z} =
|z|^2.
$$

### Reciprocal

If \(z\neq 0\),

$$
z^{-1} =
\frac{\overline{z}}{|z|^2}.
$$

### Euler Formula

$$
e^{i\theta} =
\cos\theta+i\sin\theta.
$$

### Polar Multiplication

$$
(re^{i\theta})(se^{i\phi}) =
rs\,e^{i(\theta+\phi)}.
$$

## J.3 Vector Identities

### Dot Product

For

$$
x,y\in\mathbb{R}^n,
$$

$$
x\cdot y =
x^Ty =
\sum_{i=1}^n x_i y_i.
$$

### Euclidean Norm

$$
\|x\|_2 =
\sqrt{x^Tx}.
$$

### Distance Formula

$$
d(x,y) =
\|x-y\|.
$$

### Cauchy-Schwarz Inequality

$$
|\langle x,y\rangle|
\leq
\|x\|\,\|y\|.
$$

### Triangle Inequality

$$
\|x+y\|
\leq
\|x\|+\|y\|.
$$

### Parallelogram Identity

$$
\|x+y\|^2+\|x-y\|^2 =
2\|x\|^2+2\|y\|^2.
$$

## J.4 Matrix Addition and Multiplication

### Matrix Addition

If \(A,B\in F^{m\times n}\),

$$
(A+B)_{ij} =
a_{ij}+b_{ij}.
$$

### Matrix Multiplication

If

$$
A\in F^{m\times n},
\qquad
B\in F^{n\times p},
$$

then

$$
(AB)_{ij} =
\sum_{k=1}^n a_{ik}b_{kj}.
$$

### Associativity

$$
A(BC)=(AB)C.
$$

### Distributivity

$$
A(B+C)=AB+AC.
$$

$$
(A+B)C=AC+BC.
$$

### Scalar Compatibility

$$
(cA)B =
A(cB) =
c(AB).
$$

### Noncommutativity

In general,

$$
AB\neq BA.
$$

## J.5 Transpose Identities

### Transpose of Sum

$$
(A+B)^T =
A^T+B^T.
$$

### Transpose of Product

$$
(AB)^T =
B^TA^T.
$$

### Double Transpose

$$
(A^T)^T=A.
$$

### Inverse of Transpose

$$
(A^T)^{-1} =
(A^{-1})^T.
$$

when \(A\) is invertible.

## J.6 Conjugate Transpose Identities

### Conjugate Transpose of Product

$$
(AB)^* =
B^*A^*.
$$

### Double Conjugate Transpose

$$
(A^*)^*=A.
$$

### Inverse Relation

$$
(A^*)^{-1} =
(A^{-1})^*.
$$

for invertible \(A\).

## J.7 Determinant Identities

### Determinant of Product

$$
\det(AB) =
\det(A)\det(B).
$$

### Determinant of Transpose

$$
\det(A^T)=\det(A).
$$

### Determinant of Inverse

$$
\det(A^{-1}) =
\frac{1}{\det(A)}.
$$

### Determinant of Triangular Matrix

For triangular \(A\),

$$
\det(A) =
\prod_{i=1}^n a_{ii}.
$$

### Invertibility Criterion

$$
A \text{ invertible}
\iff
\det(A)\neq 0.
$$

## J.8 Trace Identities

### Definition

$$
\operatorname{tr}(A) =
\sum_{i=1}^n a_{ii}.
$$

### Linearity

$$
\operatorname{tr}(A+B) =
\operatorname{tr}(A)
+
\operatorname{tr}(B).
$$

### Scalar Multiplication

$$
\operatorname{tr}(cA) =
c\,\operatorname{tr}(A).
$$

### Cyclic Property

$$
\operatorname{tr}(AB) =
\operatorname{tr}(BA).
$$

More generally,

$$
\operatorname{tr}(ABC) =
\operatorname{tr}(BCA) =
\operatorname{tr}(CAB).
$$

## J.9 Inverse Identities

### Inverse of Product

$$
(AB)^{-1} =
B^{-1}A^{-1}.
$$

### Identity Inverse

$$
I^{-1}=I.
$$

### Inverse of Diagonal Matrix

If

$$
D=\operatorname{diag}(d_1,\ldots,d_n),
$$

with all \(d_i\neq 0\), then

$$
D^{-1} =
\operatorname{diag}
\left(
\frac{1}{d_1},
\ldots,
\frac{1}{d_n}
\right).
$$

## J.10 Rank Identities

### Rank Bound

If

$$
A\in F^{m\times n},
$$

then

$$
\operatorname{rank}(A)
\leq
\min(m,n).
$$

### Rank-Nullity Theorem

For a linear map

$$
T:V\to W,
$$

$$
\dim(V) =
\operatorname{rank}(T)
+
\operatorname{nullity}(T).
$$

### Rank of Product

$$
\operatorname{rank}(AB)
\leq
\min(
\operatorname{rank}(A),
\operatorname{rank}(B)
).
$$

## J.11 Orthogonality Identities

### Orthogonal Matrix

$$
Q^TQ=I.
$$

### Unitary Matrix

$$
U^*U=I.
$$

### Norm Preservation

If \(Q\) is orthogonal,

$$
\|Qx\|_2 =
\|x\|_2.
$$

### Orthogonal Projection

If \(P\) is an orthogonal projection,

$$
P^2=P,
\qquad
P^T=P.
$$

## J.12 Eigenvalue Identities

### Eigenvalue Equation

$$
Av=\lambda v.
$$

### Characteristic Polynomial

$$
p_A(\lambda) =
\det(\lambda I-A).
$$

### Sum of Eigenvalues

The sum of eigenvalues equals the trace:

$$
\sum_i \lambda_i =
\operatorname{tr}(A).
$$

### Product of Eigenvalues

The product of eigenvalues equals the determinant:

$$
\prod_i \lambda_i =
\det(A).
$$

### Similarity Invariance

If

$$
B=P^{-1}AP,
$$

then \(A\) and \(B\) have the same eigenvalues.

## J.13 Diagonalization Identities

If

$$
A=PDP^{-1},
$$

then

$$
A^k =
PD^kP^{-1}.
$$

If

$$
D=
\operatorname{diag}(\lambda_1,\ldots,\lambda_n),
$$

then

$$
D^k =
\operatorname{diag}
(\lambda_1^k,\ldots,\lambda_n^k).
$$

## J.14 Singular Value Decomposition

If

$$
A=U\Sigma V^*,
$$

then:

| Property | Formula |
|---|---|
| \(U\) unitary | \(U^*U=I\) |
| \(V\) unitary | \(V^*V=I\) |
| Singular values | Diagonal entries of \(\Sigma\) |
| Eigenvalues of \(A^*A\) | \(\sigma_i^2\) |

### Frobenius Norm from Singular Values

$$
\|A\|_F^2 =
\sum_i \sigma_i^2.
$$

### Spectral Norm

$$
\|A\|_2 =
\sigma_{\max}(A).
$$

## J.15 Least Squares Formulas

For the least squares problem

$$
\min_x \|Ax-b\|_2^2,
$$

the normal equations are

$$
A^TAx=A^Tb.
$$

If the columns of \(A\) are linearly independent, then

$$
x =
(A^TA)^{-1}A^Tb.
$$

### Projection Matrix

The orthogonal projection onto the column space of \(A\) is

$$
P =
A(A^TA)^{-1}A^T.
$$

## J.16 Calculus Identities

### Derivative of Power

$$
\frac{d}{dx}x^n =
nx^{n-1}.
$$

### Product Rule

$$
(fg)' =
f'g+fg'.
$$

### Chain Rule

$$
(f\circ g)' =
(f'\circ g)g'.
$$

### Gradient of Quadratic Form

If

$$
f(x)=x^TAx,
$$

then

$$
\nabla f(x) =
(A+A^T)x.
$$

If \(A\) is symmetric,

$$
\nabla f(x)=2Ax.
$$

### Hessian of Quadratic Form

If \(A\) is symmetric,

$$
\nabla^2(x^TAx)=2A.
$$

## J.17 Matrix Calculus Identities

### Derivative of Linear Form

$$
\nabla_x(c^Tx)=c.
$$

### Derivative of Norm Squared

$$
\nabla_x \|x\|_2^2 =
2x.
$$

### Derivative of Least Squares Objective

If

$$
f(x)=\|Ax-b\|_2^2,
$$

then

$$
\nabla f(x) =
2A^T(Ax-b).
$$

## J.18 Numerical Computation Identities

### Residual

For approximate solution \(\widehat{x}\),

$$
r=b-A\widehat{x}.
$$

### Relative Error

$$
\frac{\|x-\widehat{x}\|}{\|x\|}.
$$

### Condition Number

$$
\kappa(A) =
\|A\|\,\|A^{-1}\|.
$$

### Floating-Point Model

$$
\operatorname{fl}(a\circ b) =
(a\circ b)(1+\delta),
\qquad
|\delta|\leq u.
$$

## J.19 Probability and Statistics Identities

### Mean

For data points \(x_1,\ldots,x_n\),

$$
\mu =
\frac{1}{n}
\sum_{i=1}^n x_i.
$$

### Variance

$$
\operatorname{Var}(x) =
\frac{1}{n}
\sum_{i=1}^n (x_i-\mu)^2.
$$

### Covariance Matrix

For centered vectors \(x_i\),

$$
C =
\frac{1}{n}
\sum_{i=1}^n x_ix_i^T.
$$

Covariance matrices are symmetric and positive semidefinite.

## J.20 Fourier and Orthogonality Identities

### Fourier Coefficient

$$
c_k =
\langle f,\phi_k\rangle.
$$

### Orthogonality Relation

$$
\langle \phi_i,\phi_j\rangle =
0,
\qquad
i\neq j.
$$

### Parseval Identity

$$
\|f\|^2 =
\sum_k |c_k|^2.
$$

## J.21 Common Matrix Factorizations

| Factorization | Form |
|---|---|
| LU decomposition | \(A=LU\) |
| QR decomposition | \(A=QR\) |
| Cholesky decomposition | \(A=LL^T\) |
| Eigenvalue decomposition | \(A=PDP^{-1}\) |
| Singular value decomposition | \(A=U\Sigma V^*\) |
| Schur decomposition | \(A=QTQ^*\) |

## J.22 Summary

The identities in this appendix appear repeatedly throughout linear algebra, numerical computation, optimization, statistics, and applied mathematics.

Several themes recur:

| Theme | Representative identity |
|---|---|
| Structure preservation | \((AB)^T=B^TA^T\) |
| Geometry | \(\langle x,y\rangle=x^Ty\) |
| Invertibility | \(\det(A)\neq 0\iff A^{-1}\text{ exists}\) |
| Orthogonality | \(Q^TQ=I\) |
| Spectral structure | \(Av=\lambda v\) |
| Optimization | \(A^TAx=A^Tb\) |
| Numerical analysis | \(\kappa(A)=\|A\|\|A^{-1}\|\) |

These formulas form the computational and theoretical vocabulary of linear algebra.