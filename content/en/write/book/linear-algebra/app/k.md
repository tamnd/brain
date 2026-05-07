---
title: "Appendix K. Symbol Index"
---

# Appendix K. Symbol Index

This appendix lists common symbols used in the book. A symbol may have several meanings in different contexts. When ambiguity is possible, the surrounding definition controls the meaning.

## K.1 Number Systems and Fields

| Symbol | Meaning |
|---|---|
| \(\mathbb{N}\) | Natural numbers |
| \(\mathbb{Z}\) | Integers |
| \(\mathbb{Q}\) | Rational numbers |
| \(\mathbb{R}\) | Real numbers |
| \(\mathbb{C}\) | Complex numbers |
| \(F\) | A field of scalars |
| \(0\) | Zero scalar, zero vector, or zero matrix |
| \(1\) | Multiplicative identity in a field |

## K.2 Sets and Logic

| Symbol | Meaning |
|---|---|
| \(x\in A\) | \(x\) is an element of \(A\) |
| \(x\notin A\) | \(x\) is not an element of \(A\) |
| \(A\subseteq B\) | \(A\) is a subset of \(B\) |
| \(A\cup B\) | Union |
| \(A\cap B\) | Intersection |
| \(A\setminus B\) | Set difference |
| \(\varnothing\) | Empty set |
| \(A\times B\) | Cartesian product |
| \(\forall\) | For all |
| \(\exists\) | There exists |
| \(\exists!\) | There exists exactly one |
| \(\implies\) | Implies |
| \(\iff\) | If and only if |

## K.3 Functions and Maps

| Symbol | Meaning |
|---|---|
| \(f:A\to B\) | Function from \(A\) to \(B\) |
| \(x\mapsto f(x)\) | Mapping rule |
| \(f(S)\) | Image of a set \(S\) |
| \(f^{-1}(T)\) | Preimage of a set \(T\) |
| \(f\circ g\) | Composition of functions |
| \(\operatorname{dom}(f)\) | Domain of \(f\) |
| \(\operatorname{im}(f)\) | Image of \(f\) |

## K.4 Vectors and Vector Spaces

| Symbol | Meaning |
|---|---|
| \(V,W,U\) | Vector spaces or subspaces |
| \(v,u,w,x,y,z\) | Vectors or scalar variables |
| \(F^n\) | \(n\)-dimensional coordinate space over \(F\) |
| \(\mathbb{R}^n\) | Real coordinate space |
| \(\mathbb{C}^n\) | Complex coordinate space |
| \(v_i\) | \(i\)-th component of \(v\) |
| \(e_i\) | \(i\)-th standard basis vector |
| \(\operatorname{span}(S)\) | Span of \(S\) |
| \(\dim(V)\) | Dimension of \(V\) |
| \([v]_{\mathcal B}\) | Coordinate vector of \(v\) in basis \(\mathcal B\) |

## K.5 Matrices

| Symbol | Meaning |
|---|---|
| \(A,B,C\) | Matrices or linear transformations |
| \(F^{m\times n}\) | Set of \(m\times n\) matrices over \(F\) |
| \(a_{ij}\) | Entry of \(A\) in row \(i\), column \(j\) |
| \(A^T\) | Transpose of \(A\) |
| \(A^*\) | Conjugate transpose of \(A\) |
| \(A^{-1}\) | Inverse of \(A\) |
| \(I\), \(I_n\) | Identity matrix |
| \(\operatorname{diag}(d_1,\ldots,d_n)\) | Diagonal matrix |
| \(\operatorname{tr}(A)\) | Trace of \(A\) |
| \(\det(A)\) | Determinant of \(A\) |
| \(\operatorname{rank}(A)\) | Rank of \(A\) |

Matrix notation commonly uses two subscripts for entries, with the first index giving the row and the second index giving the column. Matrix multiplication may be viewed entrywise, columnwise, or as composition of linear maps.

## K.6 Linear Transformations

| Symbol | Meaning |
|---|---|
| \(T:V\to W\) | Linear transformation from \(V\) to \(W\) |
| \(\ker(T)\) | Kernel of \(T\) |
| \(\operatorname{im}(T)\) | Image of \(T\) |
| \(\operatorname{rank}(T)\) | Dimension of image |
| \(\operatorname{nullity}(T)\) | Dimension of kernel |
| \(T^{-1}\) | Inverse transformation, when it exists |
| \([T]_{\mathcal B}^{\mathcal C}\) | Matrix of \(T\) from basis \(\mathcal B\) to basis \(\mathcal C\) |

## K.7 Inner Products, Norms, and Orthogonality

| Symbol | Meaning |
|---|---|
| \(\langle u,v\rangle\) | Inner product |
| \(u\cdot v\) | Dot product |
| \(\|v\|\) | Norm of \(v\) |
| \(\|v\|_1\) | Sum of absolute component values |
| \(\|v\|_2\) | Euclidean norm |
| \(\|v\|_\infty\) | Maximum absolute component value |
| \(\|A\|_F\) | Frobenius norm |
| \(u\perp v\) | \(u\) is orthogonal to \(v\) |
| \(W^\perp\) | Orthogonal complement of \(W\) |
| \(\operatorname{proj}_W(v)\) | Projection of \(v\) onto \(W\) |

## K.8 Eigenvalues and Spectral Notation

| Symbol | Meaning |
|---|---|
| \(\lambda,\mu\) | Eigenvalues or scalar parameters |
| \(Av=\lambda v\) | Eigenvalue equation |
| \(E_\lambda\) | Eigenspace for \(\lambda\) |
| \(p_A(\lambda)\) | Characteristic polynomial of \(A\) |
| \(\chi_A(\lambda)\) | Alternative notation for characteristic polynomial |
| \(m_A(\lambda)\) | Minimal polynomial of \(A\) |
| \(\rho(A)\) | Spectral radius of \(A\) |
| \(\Lambda\) | Diagonal matrix of eigenvalues |

Eigenvectors are nonzero vectors whose direction is preserved by a linear transformation, up to scalar multiplication. Eigenvalues are the corresponding scalars.

## K.9 Matrix Factorizations

| Symbol | Meaning |
|---|---|
| \(A=LU\) | LU factorization |
| \(A=PLU\) | LU factorization with permutation |
| \(A=QR\) | QR factorization |
| \(A=LL^T\) | Cholesky factorization, real case |
| \(A=LL^*\) | Cholesky factorization, complex case |
| \(A=U\Sigma V^*\) | Singular value decomposition |
| \(A=PDP^{-1}\) | Diagonalization |
| \(A=QTQ^*\) | Schur decomposition |
| \(\Sigma\) | Diagonal matrix of singular values |

## K.10 Polynomial Notation

| Symbol | Meaning |
|---|---|
| \(F[x]\) | Polynomials in \(x\) with coefficients in \(F\) |
| \(p(x),q(x)\) | Polynomials |
| \(\deg(p)\) | Degree of \(p\) |
| \(p(A)\) | Polynomial evaluated at matrix \(A\) |
| \((x-\lambda)\mid p(x)\) | \(x-\lambda\) divides \(p(x)\) |
| \(\gcd(p,q)\) | Greatest common divisor of polynomials |
| \(\lambda\) | Root of a polynomial or eigenvalue |

## K.11 Determinants and Permutations

| Symbol | Meaning |
|---|---|
| \(S_n\) | Symmetric group on \(n\) elements |
| \(\sigma\) | Permutation |
| \(\operatorname{sgn}(\sigma)\) | Sign of a permutation |
| \(\varepsilon_{ijk}\) | Levi-Civita symbol |
| \(\delta_{ij}\) | Kronecker delta |
| \(M_{ij}\) | Minor of entry \(a_{ij}\) |
| \(C_{ij}\) | Cofactor of entry \(a_{ij}\) |
| \(\operatorname{adj}(A)\) | Adjugate of \(A\) |

## K.12 Numerical Computation

| Symbol | Meaning |
|---|---|
| \(\widehat{x}\) | Computed approximation to \(x\) |
| \(r=b-A\widehat{x}\) | Residual |
| \(\epsilon\) | Small error or tolerance |
| \(u\) | Unit roundoff |
| \(\kappa(A)\) | Condition number of \(A\) |
| \(\operatorname{fl}(x)\) | Floating-point representation of \(x\) |
| \(O(\cdot)\) | Big-O asymptotic bound |
| \(\tau\) | Numerical tolerance |

## K.13 Calculus and Optimization

| Symbol | Meaning |
|---|---|
| \(f'(x)\) | Derivative of \(f\) |
| \(\frac{\partial f}{\partial x_i}\) | Partial derivative |
| \(\nabla f(x)\) | Gradient |
| \(\nabla^2 f(x)\) | Hessian |
| \(J_F(x)\) | Jacobian matrix |
| \(\arg\min_x f(x)\) | Value of \(x\) minimizing \(f\) |
| \(\min_x f(x)\) | Minimum value of \(f\) |
| \(\|Ax-b\|^2\) | Least squares objective |

## K.14 Common Greek Symbols

| Symbol | Common use |
|---|---|
| \(\alpha,\beta,\gamma\) | Scalars or coefficients |
| \(\delta\) | Perturbation or Kronecker delta |
| \(\epsilon\) | Small positive number or error |
| \(\theta,\phi\) | Angles |
| \(\lambda,\mu\) | Eigenvalues |
| \(\sigma_i\) | Singular values |
| \(\Sigma\) | Singular value matrix |
| \(\Lambda\) | Eigenvalue matrix |

## K.15 Summary

This symbol index is a reference for notation, not a replacement for definitions. Symbols in linear algebra are compact because they often describe high-dimensional objects. A single expression such as

$$
A=U\Sigma V^*
$$

contains several layers of meaning: a matrix factorization, orthonormal coordinate systems, singular values, rank information, and geometric scaling.

When reading a formula, first identify the type of each object. Determine whether each symbol denotes a scalar, vector, matrix, set, space, function, or operator. Once the types are clear, the meaning of the expression usually becomes much simpler.