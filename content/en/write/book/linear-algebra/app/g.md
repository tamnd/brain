---
title: "Appendix G. Mathematical Notation"
---

# Appendix G. Mathematical Notation

Mathematics depends on notation. Good notation compresses complex ideas into compact symbolic form. Poor notation obscures structure and makes arguments difficult to follow.

Linear algebra uses notation for vectors, matrices, functions, sets, spaces, mappings, indices, norms, determinants, and many other objects. This appendix summarizes the conventions used throughout the book.

The goal is consistency and clarity rather than maximal generality. Different books may use different conventions, especially for inner products, transpose notation, indexing, and matrix dimensions. When a convention matters, it will be stated explicitly.

## G.1 Variables and Constants

Variables usually represent quantities that may vary. Constants represent fixed quantities.

Common conventions include:

| Symbol type | Typical meaning |
|---|---|
| \(x,y,z\) | Scalars or coordinates |
| \(u,v,w\) | Vectors |
| \(A,B,C\) | Matrices or linear transformations |
| \(V,W,U\) | Vector spaces or subspaces |
| \(i,j,k\) | Indices |
| \(m,n,p\) | Dimensions or sizes |
| \(\lambda,\mu\) | Eigenvalues or scalars |
| \(f,g,h\) | Functions |

These conventions are not absolute, but they help communicate the role of an object before it is formally defined.

## G.2 Equality and Assignment

The symbol

$$ =
$$

means equality.

For example,

$$
x+1=3
$$

states that two expressions represent the same quantity.

The symbol

$$
:=
$$

often means “is defined to be.”

For example,

$$
f(x):=x^2+1
$$

defines the function \(f\).

Some texts use \(=\) for both purposes. This book occasionally uses \(:=\) when the distinction improves clarity.

## G.3 Sets

Sets are usually written with braces:

$$
A=\{1,2,3\}.
$$

Set-builder notation describes sets by properties:

$$
A=\{x\in\mathbb{R}:x>0\}.
$$

This means that \(A\) is the set of positive real numbers.

Common set notation includes:

| Symbol | Meaning |
|---|---|
| \(x\in A\) | \(x\) belongs to \(A\) |
| \(x\notin A\) | \(x\) does not belong to \(A\) |
| \(A\subseteq B\) | \(A\) is a subset of \(B\) |
| \(A\cup B\) | Union |
| \(A\cap B\) | Intersection |
| \(A\setminus B\) | Difference |
| \(\varnothing\) | Empty set |

## G.4 Number Systems

The following symbols denote standard number systems:

| Symbol | Meaning |
|---|---|
| \(\mathbb{N}\) | Natural numbers |
| \(\mathbb{Z}\) | Integers |
| \(\mathbb{Q}\) | Rational numbers |
| \(\mathbb{R}\) | Real numbers |
| \(\mathbb{C}\) | Complex numbers |

The symbol

$$
F
$$

often denotes a general field, usually \(\mathbb{R}\) or \(\mathbb{C}\).

## G.5 Intervals

Intervals are subsets of the real line.

| Notation | Meaning |
|---|---|
| \((a,b)\) | \(a<x<b\) |
| \([a,b]\) | \(a\leq x\leq b\) |
| \((a,b]\) | \(a<x\leq b\) |
| \([a,b)\) | \(a\leq x<b\) |

The symbol

$$
(-\infty,\infty)
$$

denotes the entire real line.

## G.6 Functions

A function from \(A\) to \(B\) is written

$$
f:A\to B.
$$

If \(x\in A\), then

$$
f(x)
$$

denotes the image of \(x\).

Functions may also be written as mappings:

$$
x\mapsto f(x).
$$

For example,

$$
f:\mathbb{R}\to\mathbb{R},
\qquad
x\mapsto x^2.
$$

Common notation includes:

| Symbol | Meaning |
|---|---|
| \(\operatorname{dom}(f)\) | Domain |
| \(\operatorname{im}(f)\) | Image or range |
| \(f^{-1}\) | Inverse function or preimage |
| \(f\circ g\) | Composition |

## G.7 Vectors

Vectors are usually written in lowercase boldface or as column arrays.

Examples:

$$
v=
\begin{bmatrix}
1 \\
2 \\
3
\end{bmatrix}.
$$

The vector space of all \(n\)-component real vectors is denoted by

$$
\mathbb{R}^n.
$$

Similarly,

$$
\mathbb{C}^n
$$

denotes the space of complex vectors.

Vector components are indexed:

$$
v=
\begin{bmatrix}
v_1 \\
v_2 \\
\vdots \\
v_n
\end{bmatrix}.
$$

The \(i\)-th component is written

$$
v_i.
$$

## G.8 Matrices

Matrices are usually denoted by uppercase letters:

$$
A,B,C.
$$

An \(m\times n\) matrix has \(m\) rows and \(n\) columns:

$$
A=
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix}.
$$

The entry in row \(i\), column \(j\) is

$$
a_{ij}.
$$

The set of all \(m\times n\) matrices over \(F\) is often denoted by

$$
F^{m\times n}.
$$

## G.9 Matrix Operations

The transpose of a matrix \(A\) is denoted by

$$
A^T.
$$

The conjugate transpose is denoted by

$$
A^*.
$$

The inverse of an invertible matrix is denoted by

$$
A^{-1}.
$$

The determinant is written

$$
\det(A)
$$

or occasionally

$$
|A|.
$$

The trace is written

$$
\operatorname{tr}(A).
$$

The identity matrix is denoted by

$$
I
$$

or

$$
I_n
$$

when the dimension must be specified.

The zero matrix is denoted by

$$
0.
$$

## G.10 Matrix Dimensions

If

$$
A\in F^{m\times n},
$$

then \(A\) has \(m\) rows and \(n\) columns.

If

$$
x\in F^n,
$$

then the product

$$
Ax
$$

is defined and belongs to \(F^m\).

Dimension compatibility is essential for matrix multiplication.

If

$$
A\in F^{m\times n},
\qquad
B\in F^{n\times p},
$$

then

$$
AB\in F^{m\times p}.
$$

The inner dimensions must match.

## G.11 Subscripts and Superscripts

Subscripts usually denote components or indices:

$$
x_i,
\qquad
a_{ij}.
$$

Superscripts often denote powers:

$$
A^2=AA.
$$

However, superscripts may also denote labels rather than powers. For example,

$$
v^{(k)}
$$

often denotes the \(k\)-th vector in a sequence.

Context determines the meaning.

## G.12 Summation Notation

The summation symbol is

$$
\sum.
$$

For example,

$$
\sum_{i=1}^n x_i =
x_1+x_2+\cdots+x_n.
$$

Double sums are written as

$$
\sum_{i=1}^m\sum_{j=1}^n a_{ij}.
$$

Summation notation is compact and appears throughout matrix algebra.

### Example

Matrix-vector multiplication may be written as

$$
(Ax)_i =
\sum_{j=1}^n a_{ij}x_j.
$$

This means the \(i\)-th component of \(Ax\) is the dot product of the \(i\)-th row of \(A\) with \(x\).

## G.13 Product Notation

The product symbol is

$$
\prod.
$$

For example,

$$
\prod_{k=1}^n a_k =
a_1a_2\cdots a_n.
$$

Factorials are products:

$$
n! =
\prod_{k=1}^n k.
$$

Products appear in determinants, characteristic polynomials, and probability formulas.

## G.14 Greek Letters

Greek letters are widely used in linear algebra.

| Symbol | Common use |
|---|---|
| \(\alpha,\beta,\gamma\) | Scalars |
| \(\lambda,\mu\) | Eigenvalues |
| \(\sigma\) | Singular values |
| \(\theta,\phi\) | Angles |
| \(\epsilon\) | Small quantities or errors |
| \(\delta\) | Perturbations |
| \(\pi\) | Constant \(3.14159\ldots\) |

The notation is conventional rather than mandatory.

## G.15 Logical Symbols

Mathematical statements often use logical notation.

| Symbol | Meaning |
|---|---|
| \(\forall\) | For all |
| \(\exists\) | There exists |
| \(\exists!\) | There exists exactly one |
| \(\implies\) | Implies |
| \(\iff\) | If and only if |
| \(\neg\) | Not |

Example:

$$
\forall x\in\mathbb{R},\ x^2\geq 0.
$$

This means every real number has nonnegative square.

## G.16 Norms

Norms are written using double vertical bars:

$$
\|x\|.
$$

Common vector norms include:

| Norm | Formula |
|---|---|
| \(1\)-norm | \(\|x\|_1=\sum_i |x_i|\) |
| \(2\)-norm | \(\|x\|_2=\sqrt{\sum_i |x_i|^2}\) |
| \(\infty\)-norm | \(\|x\|_\infty=\max_i |x_i|\) |

Matrix norms use the same notation.

The Frobenius norm is

$$
\|A\|_F =
\sqrt{
\sum_{i,j}|a_{ij}|^2
}.
$$

## G.17 Inner Products

Inner products are commonly written as

$$
\langle u,v\rangle.
$$

In \(\mathbb{R}^n\),

$$
\langle u,v\rangle =
u^Tv.
$$

In \(\mathbb{C}^n\),

$$
\langle u,v\rangle =
u^*v.
$$

The induced norm is

$$
\|v\| =
\sqrt{\langle v,v\rangle}.
$$

Orthogonality is written

$$
u\perp v.
$$

This means

$$
\langle u,v\rangle=0.
$$

## G.18 Span and Linear Combination

The span of vectors

$$
v_1,\ldots,v_k
$$

is denoted by

$$
\operatorname{span}\{v_1,\ldots,v_k\}.
$$

It is the set of all linear combinations:

$$
c_1v_1+\cdots+c_kv_k.
$$

Linear independence is usually expressed by:

$$
c_1v_1+\cdots+c_kv_k=0
\implies
c_1=\cdots=c_k=0.
$$

## G.19 Basis and Dimension

A basis of a vector space \(V\) is often denoted by

$$
\mathcal{B}=\{v_1,\ldots,v_n\}.
$$

The dimension of \(V\) is written

$$
\dim(V).
$$

Coordinate vectors relative to a basis \(\mathcal{B}\) are often written

$$
[v]_{\mathcal{B}}.
$$

## G.20 Eigenvalues and Eigenvectors

An eigenvalue of \(A\) is usually denoted by

$$
\lambda.
$$

An eigenvector corresponding to \(\lambda\) satisfies

$$
Av=\lambda v.
$$

The eigenspace corresponding to \(\lambda\) is

$$
E_\lambda =
\ker(A-\lambda I).
$$

The characteristic polynomial is

$$
p_A(\lambda)=\det(\lambda I-A).
$$

## G.21 Special Matrix Classes

Several matrix classes have standard notation.

| Matrix type | Condition |
|---|---|
| Symmetric | \(A^T=A\) |
| Hermitian | \(A^*=A\) |
| Orthogonal | \(A^TA=I\) |
| Unitary | \(A^*A=I\) |
| Diagonal | Off-diagonal entries are zero |
| Upper triangular | Entries below diagonal are zero |
| Lower triangular | Entries above diagonal are zero |

## G.22 Approximation Symbols

Approximation notation is common in numerical work.

| Symbol | Meaning |
|---|---|
| \(\approx\) | Approximately equal |
| \(\sim\) | Asymptotically equivalent or related |
| \(O(n)\) | Order notation |
| \(o(n)\) | Lower-order asymptotic behavior |

For example,

$$
f(n)=O(n^2)
$$

means that \(f(n)\) grows at most proportionally to \(n^2\) for large \(n\).

## G.23 Indexed Families

Indexed families are written using subscripts or superscripts.

Examples:

$$
(v_i)_{i=1}^n,
\qquad
(A_k)_{k\geq 0}.
$$

Infinite sequences may be written as

$$
(x_n)_{n=1}^\infty.
$$

This notation is compact and useful for bases, iterations, and recursive algorithms.

## G.24 Standard Abbreviations

Several abbreviations occur frequently.

| Abbreviation | Meaning |
|---|---|
| iff | If and only if |
| w.r.t. | With respect to |
| i.e. | That is |
| e.g. | For example |
| QED | End of proof |

The symbol

$$
\square
$$

is also commonly used to mark the end of a proof.

## G.25 Reading Mathematical Expressions

Mathematical notation should be read structurally rather than symbol by symbol.

For example,

$$
A^{-1}(B+C)^T
$$

should be read as:

1. Add \(B\) and \(C\).
2. Transpose the result.
3. Multiply by \(A^{-1}\).

Parentheses indicate grouping. Superscripts and subscripts modify nearby symbols. Juxtaposition often denotes multiplication.

Careful reading prevents many algebraic errors.

## G.26 Summary

Mathematical notation is a language for expressing structure compactly.

Linear algebra notation describes:

| Object | Typical notation |
|---|---|
| Scalars | \(x,\lambda,\alpha\) |
| Vectors | \(v,u,w\) |
| Matrices | \(A,B,C\) |
| Vector spaces | \(V,W\) |
| Inner products | \(\langle u,v\rangle\) |
| Norms | \(\|x\|\) |
| Determinants | \(\det(A)\) |
| Eigenvalues | \(\lambda\) |
| Span | \(\operatorname{span}\{\cdot\}\) |
| Dimension | \(\dim(V)\) |

The notation of linear algebra is compact because the subject describes large systems and high-dimensional structures. Clear notation reduces complexity and exposes relationships that would otherwise remain hidden.