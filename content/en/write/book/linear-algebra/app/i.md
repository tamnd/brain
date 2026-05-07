---
title: "Appendix I. Glossary"
---

# Appendix I. Glossary

This glossary summarizes the main terms used throughout the book. Definitions are stated briefly and emphasize the meaning most relevant to linear algebra.

## A

### Affine Space

A set obtained by translating a vector subspace. An affine space does not necessarily contain the zero vector.

### Algebraic Multiplicity

The multiplicity of an eigenvalue as a root of the characteristic polynomial.

### Alternating Form

A multilinear form that changes sign when two arguments are exchanged and becomes zero when two arguments are equal.

### Augmented Matrix

A matrix formed by appending the right-hand side vector \(b\) to the coefficient matrix \(A\) of a system

$$
Ax=b.
$$

## B

### Backward Error

The size of the perturbation needed to make a computed solution exact for a nearby problem.

### Basis

A linearly independent spanning set for a vector space.

### Bilinear Form

A function

$$
B:V\times V\to F
$$

that is linear in each argument separately.

### Block Matrix

A matrix partitioned into submatrices treated as single units.

## C

### Canonical Form

A standard representative chosen from a class of equivalent matrices or transformations.

### Characteristic Polynomial

The polynomial

$$
p_A(\lambda)=\det(\lambda I-A).
$$

Its roots are the eigenvalues of \(A\).

### Cholesky Decomposition

A factorization

$$
A=LL^T
$$

or

$$
A=LL^*
$$

for positive definite matrices.

### Column Space

The span of the columns of a matrix.

### Companion Matrix

A matrix associated with a monic polynomial whose characteristic polynomial equals that polynomial.

### Complex Conjugate

For

$$
z=a+bi,
$$

the conjugate is

$$
\overline{z}=a-bi.
$$

### Condition Number

A measure of sensitivity of a problem to perturbations in the input.

### Coordinate Vector

The vector of coefficients expressing a vector relative to a chosen basis.

## D

### Determinant

A scalar associated with a square matrix that measures invertibility, signed volume scaling, and orientation change.

### Diagonal Matrix

A matrix whose off-diagonal entries are all zero.

### Diagonalizable Matrix

A matrix similar to a diagonal matrix.

### Dimension

The number of vectors in a basis of a vector space.

### Direct Sum

A decomposition of a vector space into subspaces with trivial intersection.

## E

### Eigenvalue

A scalar \(\lambda\) such that

$$
Av=\lambda v
$$

for some nonzero vector \(v\).

### Eigenvector

A nonzero vector satisfying

$$
Av=\lambda v.
$$

### Eigenspace

The subspace

$$
\ker(A-\lambda I).
$$

### Elementary Matrix

A matrix obtained from the identity matrix by one elementary row operation.

### Elementary Row Operation

One of the operations:

| Operation | Meaning |
|---|---|
| Row swap | Exchange two rows |
| Row scaling | Multiply a row by a nonzero scalar |
| Row replacement | Add a multiple of one row to another |

### Euclidean Norm

The norm

$$
\|x\|_2 =
\sqrt{x_1^2+\cdots+x_n^2}.
$$

## F

### Field

A set with addition, subtraction, multiplication, and division by nonzero elements satisfying the field axioms.

### Forward Error

The difference between a computed solution and the exact solution.

### Frobenius Norm

The matrix norm

$$
\|A\|_F =
\sqrt{
\sum_{i,j}|a_{ij}|^2
}.
$$

## G

### Gaussian Elimination

An algorithm for solving linear systems using elementary row operations.

### Geometric Multiplicity

The dimension of the eigenspace associated with an eigenvalue.

### Gram Matrix

A matrix of inner products:

$$
G_{ij}=\langle v_i,v_j\rangle.
$$

### Gram-Schmidt Process

An algorithm that converts a linearly independent set into an orthonormal set.

## H

### Hermitian Matrix

A complex matrix satisfying

$$
A^*=A.
$$

### Hessenberg Matrix

A nearly triangular matrix used in eigenvalue algorithms.

### Householder Transformation

A reflection used in QR factorization and orthogonalization algorithms.

## I

### Identity Matrix

The square matrix \(I\) with ones on the diagonal and zeros elsewhere.

### Image

The set of outputs of a function or linear transformation.

### Independent Set

A set of vectors whose only linear relation is the trivial relation.

### Inner Product

A function

$$
\langle \cdot,\cdot\rangle
$$

that generalizes dot products and defines lengths and angles.

### Invertible Matrix

A square matrix \(A\) with a matrix \(A^{-1}\) satisfying

$$
AA^{-1}=A^{-1}A=I.
$$

### Isomorphism

A bijective linear transformation.

### Iterative Method

An algorithm that approaches a solution through repeated approximation.

## J

### Jacobian Matrix

The matrix of first partial derivatives of a vector-valued function.

### Jordan Block

A matrix of the form

$$
\begin{bmatrix}
\lambda & 1 & 0 & \cdots & 0\\
0 & \lambda & 1 & \cdots & 0\\
\vdots & \vdots & \vdots & \ddots & \vdots\\
0 & 0 & 0 & \cdots & \lambda
\end{bmatrix}.
$$

### Jordan Canonical Form

A block diagonal matrix built from Jordan blocks and similar to the original matrix.

## K

### Kernel

The set

$$
\ker(T)=\{v:T(v)=0\}.
$$

### Krylov Subspace

A subspace generated by vectors

$$
v,Av,A^2v,\ldots.
$$

## L

### Least Squares Problem

An optimization problem minimizing

$$
\|Ax-b\|^2.
$$

### Linear Combination

An expression of the form

$$
c_1v_1+\cdots+c_nv_n.
$$

### Linear Dependence

A relation among vectors where a nontrivial linear combination equals zero.

### Linear Independence

The condition that only the trivial linear combination equals zero.

### Linear Map

Another term for linear transformation.

### Linear System

A collection of linear equations.

### Linear Transformation

A function preserving vector addition and scalar multiplication.

### LU Decomposition

A factorization

$$
A=LU
$$

with \(L\) lower triangular and \(U\) upper triangular.

## M

### Matrix

A rectangular array of scalars.

### Matrix Exponential

The matrix function

$$
e^A =
I+A+\frac{A^2}{2!}+\cdots.
$$

### Matrix Norm

A function measuring matrix size.

### Minimal Polynomial

The monic polynomial of smallest degree satisfying

$$
m(A)=0.
$$

### Multilinear Map

A function linear in each argument separately.

## N

### Nilpotent Matrix

A matrix \(A\) such that

$$
A^k=0
$$

for some positive integer \(k\).

### Normal Equation

The equation

$$
A^TAx=A^Tb
$$

associated with least squares problems.

### Normal Matrix

A matrix satisfying

$$
A^*A=AA^*.
$$

### Norm

A function measuring vector length or size.

### Null Space

Another term for kernel.

### Numerical Stability

The property that rounding errors do not grow excessively during computation.

## O

### Orthogonal Matrix

A real matrix satisfying

$$
Q^TQ=I.
$$

### Orthogonal Complement

The set of vectors orthogonal to a given set.

### Orthogonal Projection

The closest-point projection onto a subspace.

### Orthogonality

The condition

$$
\langle u,v\rangle=0.
$$

### Orthonormal Basis

A basis consisting of mutually orthogonal unit vectors.

## P

### Partial Pivoting

A row-swapping strategy used in Gaussian elimination for stability.

### Permutation Matrix

A matrix obtained by permuting the rows of the identity matrix.

### Pivot

A leading nonzero entry used during elimination.

### Positive Definite Matrix

A symmetric or Hermitian matrix satisfying

$$
x^TAx>0
$$

or

$$
x^*Ax>0
$$

for all nonzero \(x\).

### Projection

A linear transformation satisfying

$$
P^2=P.
$$

### Pseudoinverse

A generalized inverse, often the Moore-Penrose inverse.

## Q

### QR Decomposition

A factorization

$$
A=QR
$$

with \(Q\) orthogonal or unitary and \(R\) upper triangular.

### Quadratic Form

An expression

$$
x^TAx.
$$

## R

### Rank

The dimension of the image or column space of a matrix.

### Reduced Row Echelon Form

A canonical row-equivalent matrix form satisfying specific pivot conditions.

### Residual

The vector

$$
r=b-A\widehat{x}
$$

for an approximate solution \(\widehat{x}\).

### Row Echelon Form

A triangular-like matrix form obtained during elimination.

### Row Space

The span of the rows of a matrix.

## S

### Scalar

An element of the underlying field.

### Schur Decomposition

A factorization

$$
A=QTQ^*
$$

with \(Q\) unitary and \(T\) upper triangular.

### Singular Matrix

A noninvertible square matrix.

### Singular Value

The square root of an eigenvalue of

$$
A^*A.
$$

### Singular Value Decomposition

A factorization

$$
A=U\Sigma V^*.
$$

### Sparse Matrix

A matrix with many zero entries.

### Span

The set of all linear combinations of a collection of vectors.

### Spectral Radius

The maximum absolute value of the eigenvalues of a matrix.

### Spectral Theorem

A theorem describing diagonalization of symmetric or Hermitian matrices by orthogonal or unitary matrices.

### Subspace

A subset closed under vector addition and scalar multiplication.

### Symmetric Matrix

A real matrix satisfying

$$
A^T=A.
$$

## T

### Tensor Product

A construction combining vector spaces into a larger multilinear structure.

### Trace

The sum of the diagonal entries of a square matrix.

### Transformation Matrix

A matrix representing a linear transformation relative to chosen bases.

### Transpose

The matrix obtained by interchanging rows and columns.

### Triangular Matrix

A matrix with all entries above or below the diagonal equal to zero.

## U

### Unitary Matrix

A complex matrix satisfying

$$
U^*U=I.
$$

### Upper Triangular Matrix

A matrix whose entries below the diagonal are zero.

## V

### Vandermonde Matrix

A matrix of the form

$$
\begin{bmatrix}
1 & x_1 & x_1^2 & \cdots \\
1 & x_2 & x_2^2 & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{bmatrix}.
$$

### Vector

An element of a vector space.

### Vector Space

A set with vector addition and scalar multiplication satisfying the vector space axioms.

## W

### Well-Conditioned Problem

A problem whose solution changes little under small input perturbations.

## Z

### Zero Matrix

A matrix whose entries are all zero.

### Zero Vector

The additive identity element of a vector space.