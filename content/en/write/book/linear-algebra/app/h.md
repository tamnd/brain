---
title: "Appendix H. Historical Notes"
---

# Appendix H. Historical Notes

Linear algebra grew from several older problems. It did not begin as a single unified theory. Its main ideas came from solving systems of linear equations, studying determinants, developing analytic geometry, formalizing vector spaces, and later building numerical methods for computation.

The modern subject combines these older threads. A matrix can be viewed as a table of coefficients, a linear transformation, a data object, or an operator to be computed with. This layered meaning is the result of a long historical development.

## H.1 Linear Equations in Ancient Mathematics

Systems of linear equations are among the oldest sources of linear algebra.

Ancient mathematical texts contain problems equivalent to solving several unknown quantities from several linear conditions. The Chinese text *The Nine Chapters on the Mathematical Art* contains systematic procedures for linear systems using counting rods. These procedures are close in spirit to elimination methods used today.

The central problem was practical:

$$
\text{given several conditions, find several unknown quantities.}
$$

For example, a problem might involve prices of goods, weights of grain, or amounts of material. The unknowns were not called coordinates or vector components, but the algebraic structure was already present.

The historical origin of linear algebra is therefore computational. Long before vector spaces were defined abstractly, people solved systems of linear equations.

## H.2 Elimination

Elimination is the process of removing unknowns from equations until the system becomes simpler.

For a system such as

$$
\begin{aligned}
a_{11}x_1+a_{12}x_2+\cdots+a_{1n}x_n &= b_1,\\
a_{21}x_1+a_{22}x_2+\cdots+a_{2n}x_n &= b_2,\\
&\vdots\\
a_{m1}x_1+a_{m2}x_2+\cdots+a_{mn}x_n &= b_m,
\end{aligned}
$$

elimination replaces equations by simpler equivalent equations. The modern version is Gaussian elimination.

The name refers to Carl Friedrich Gauss, but elimination methods existed long before Gauss. Gauss used related methods in astronomical and geodetic computations, especially in least squares problems. The later systematic matrix form became a standard part of linear algebra.

The historical lesson is important: many mathematical algorithms are older than the notation used to express them.

## H.3 Determinants

Determinants arose from attempts to solve systems of linear equations.

For a \(2\times 2\) system,

$$
\begin{aligned}
ax+by &= e,\\
cx+dy &= f,
\end{aligned}
$$

the quantity

$$
ad-bc
$$

determines whether the system has a unique solution. This quantity is the determinant of the coefficient matrix

$$
\begin{bmatrix}
a & b\\
c & d
\end{bmatrix}.
$$

For larger systems, similar expressions were developed. Gabriel Cramer published a general determinant formula for solving square systems in 1750. This result is now called Cramer's rule. It expresses each unknown as a quotient of determinants when the coefficient determinant is nonzero.

Determinants were studied before matrices became central objects. In early algebra, determinants were often more important than matrices themselves.

## H.4 Cramer's Rule

Cramer's rule gives an explicit solution formula for a square linear system

$$
Ax=b
$$

when

$$
\det(A)\neq 0.
$$

If \(A_i(b)\) denotes the matrix obtained from \(A\) by replacing the \(i\)-th column by \(b\), then

$$
x_i=
\frac{\det(A_i(b))}{\det(A)}.
$$

This formula is theoretically important because it connects solvability with determinants. It shows that a nonzero determinant guarantees a unique solution.

Computationally, however, Cramer's rule is inefficient for large systems. Gaussian elimination is far better in practice. This distinction between theoretical clarity and computational efficiency appears throughout linear algebra.

## H.5 Analytic Geometry and Coordinates

Another source of linear algebra was analytic geometry.

René Descartes and Pierre de Fermat introduced coordinate methods in the seventeenth century. Geometry could then be studied using algebraic equations. Lines, planes, conic sections, and later higher-dimensional objects could be described by equations.

A line in the plane may be written as

$$
ax+by=c.
$$

A plane in three-dimensional space may be written as

$$
ax+by+cz=d.
$$

Systems of such equations describe intersections of lines, planes, and higher-dimensional affine subspaces.

Coordinates made geometry algebraic. Linear equations became geometric objects. This connection remains one of the central themes of linear algebra.

## H.6 Vectors in Geometry and Physics

The idea of a vector developed from geometry and physics.

A vector was first understood as a directed quantity, such as displacement, velocity, acceleration, or force. Such quantities have both magnitude and direction. They can be added geometrically using the parallelogram rule.

For example, two forces acting on a body may be combined into a resultant force. This physical interpretation made vector addition natural.

Later, vectors were represented by coordinates:

$$
v=
\begin{bmatrix}
v_1\\
v_2\\
v_3
\end{bmatrix}.
$$

This coordinate representation connected geometric vectors with systems of numbers. It also made vectors suitable for algebraic computation.

## H.7 Matrices

Matrices began as rectangular arrays of numbers associated with systems of linear equations. The word “matrix” was introduced by James Joseph Sylvester in the nineteenth century. Arthur Cayley then developed matrix algebra more systematically, including operations such as matrix addition, multiplication, and inversion. Historical accounts often identify the mid-nineteenth century as the period when matrices became objects of study in their own right.

This was a major conceptual shift.

Before matrices, one might focus on the equations or on the determinant. After matrices, the coefficient array itself became an algebraic object:

$$
A=
\begin{bmatrix}
a_{11} & \cdots & a_{1n}\\
\vdots & \ddots & \vdots\\
a_{m1} & \cdots & a_{mn}
\end{bmatrix}.
$$

Matrices could be added, multiplied, inverted, factored, and studied structurally. They became the main symbolic language of finite-dimensional linear algebra.

## H.8 Matrix Multiplication

Matrix multiplication was not invented merely as a rule for arrays. It was designed to represent composition of linear transformations.

If

$$
T(x)=Ax
$$

and

$$
S(x)=Bx,
$$

then applying \(S\) first and \(T\) second gives

$$
T(S(x))=A(Bx)=(AB)x.
$$

Thus the product \(AB\) represents the composite transformation.

This explains why matrix multiplication is associative but usually not commutative:

$$
A(BC)=(AB)C,
$$

but generally

$$
AB\neq BA.
$$

The order of transformations matters. Rotating and then projecting may produce a different result from projecting and then rotating.

## H.9 Vector Spaces

The abstract concept of a vector space came later than systems, determinants, and matrices.

A vector space is a set equipped with vector addition and scalar multiplication satisfying certain axioms. This definition includes many objects beyond arrows and coordinate tuples: polynomials, functions, sequences, matrices, and solutions to differential equations.

The modern abstract definition of vector space is commonly associated with the late nineteenth century, especially the work of Giuseppe Peano in 1888.

This abstraction unified many examples. Once the vector space axioms were stated, the same theorems could be applied in many settings.

For example, the ideas of span, linear independence, basis, and dimension apply to:

| Space | Typical vectors |
|---|---|
| \(\mathbb{R}^n\) | Coordinate columns |
| \(F[x]\) | Polynomials |
| \(C[a,b]\) | Continuous functions |
| \(F^{m\times n}\) | Matrices |
| Solution spaces | Functions satisfying equations |

The abstraction made linear algebra more powerful and more portable.

## H.10 Linear Transformations

As vector spaces became central, linear transformations became equally important.

A linear transformation

$$
T:V\to W
$$

satisfies

$$
T(u+v)=T(u)+T(v)
$$

and

$$
T(cv)=cT(v).
$$

Matrices represent linear transformations after bases are chosen. This viewpoint clarifies the meaning of many matrix operations.

For example:

| Matrix concept | Transformation concept |
|---|---|
| Column space | Image |
| Null space | Kernel |
| Rank | Dimension of image |
| Invertible matrix | Isomorphism |
| Similar matrices | Same map in different bases |

The transformation viewpoint shifted linear algebra from manipulation of arrays to study of structure.

## H.11 Eigenvalues

Eigenvalue ideas developed from problems in geometry, mechanics, differential equations, and quadratic forms.

An eigenvector is a direction preserved by a linear transformation:

$$
Av=\lambda v.
$$

The transformation may stretch or reverse the vector, but it does not move it away from its line.

Eigenvalues occur naturally in:

| Area | Role |
|---|---|
| Differential equations | Growth and oscillation rates |
| Mechanics | Principal axes and vibration modes |
| Geometry | Axes of quadratic forms |
| Markov chains | Long-term behavior |
| Graph theory | Connectivity and expansion |
| Quantum mechanics | Observable values |

Historically, eigenvalue problems were often studied before the modern word “eigenvalue” became standard. The underlying question was usually to find special directions, characteristic roots, or normal modes.

## H.12 Inner Products and Orthogonality

Inner products developed from geometry, trigonometry, mechanics, and analysis.

In Euclidean space, the dot product

$$
u\cdot v
$$

measures length and angle. Orthogonality means

$$
u\cdot v=0.
$$

This idea was later extended to abstract vector spaces and function spaces. For example, functions can be orthogonal under the inner product

$$
\langle f,g\rangle =
\int_a^b f(x)g(x)\,dx.
$$

This extension made linear algebra central to Fourier analysis, approximation theory, and differential equations.

Orthogonality is historically important because it connects algebra with geometry. It also leads to stable computational methods, such as orthogonal projection and QR factorization.

## H.13 Canonical Forms

As matrices became algebraic objects, mathematicians sought standard forms that reveal structure.

A canonical form replaces a matrix by a simpler matrix representing the same essential object under a change of basis.

Examples include:

| Form | Purpose |
|---|---|
| Diagonal form | Reveals independent eigendirections |
| Jordan form | Describes repeated eigenvalue structure |
| Rational canonical form | Works over general fields |
| Schur form | Supports numerical eigenvalue methods |
| Singular value decomposition | Describes geometry of linear maps |

Canonical forms show that classification is a major theme of linear algebra. One asks when two matrices represent the same transformation in different coordinate systems.

## H.14 Numerical Linear Algebra

Numerical linear algebra became especially important with modern digital computers after World War II. Large systems of equations, eigenvalue problems, least squares problems, and matrix factorizations became central to science and engineering. Historical surveys often note renewed interest in matrices after the rise of digital computation.

The numerical viewpoint changed the subject.

Exact formulas were no longer enough. Mathematicians and computer scientists had to ask:

| Question | Numerical issue |
|---|---|
| How many operations are required? | Complexity |
| How much memory is needed? | Storage |
| How does rounding error behave? | Stability |
| How sensitive is the problem? | Conditioning |
| Can sparsity be exploited? | Large-scale computation |

This led to modern algorithms such as stable Gaussian elimination, QR methods, Krylov subspace methods, and singular value algorithms.

## H.15 Linear Algebra in Data and Computation

In the twentieth and twenty-first centuries, linear algebra became a basic language of computation.

Data tables are matrices. Images are arrays. Graphs have adjacency matrices. Text, audio, and video can be embedded into vector spaces. Machine learning models use vectors, matrices, tensors, gradients, projections, and decompositions.

Examples include:

| Application | Linear algebra object |
|---|---|
| Search engines | Eigenvectors, graph matrices |
| Statistics | Covariance matrices |
| Machine learning | Feature vectors and weight matrices |
| Computer graphics | Transformation matrices |
| Signal processing | Fourier bases |
| Scientific computing | Sparse linear systems |
| Optimization | Gradients and Hessians |

The subject now serves both pure mathematics and large-scale computation.

## H.16 A Layered Subject

The history of linear algebra explains why the subject has several viewpoints.

| Historical source | Modern topic |
|---|---|
| Practical equations | Linear systems |
| Elimination procedures | Gaussian elimination |
| Determinant formulas | Invertibility and volume |
| Analytic geometry | Coordinates and subspaces |
| Physical vectors | Vector operations |
| Matrix algebra | Linear transformations |
| Abstract algebra | Vector spaces |
| Mechanics and analysis | Eigenvalues |
| Computation | Numerical linear algebra |
| Data science | High-dimensional methods |

No single origin explains the whole subject. Linear algebra is a synthesis.

## H.17 Summary

Linear algebra began with concrete problems about unknown quantities and systems of equations. Determinants provided formulas for solvability. Analytic geometry connected equations with space. Vectors gave directed quantities an algebra. Matrices became objects of study in the nineteenth century. Vector spaces and linear transformations later unified the theory. Numerical computation and data analysis made the subject indispensable in modern science and engineering.

The historical path moves from computation to structure and then back to computation:

$$
\text{equations}
\to
\text{matrices}
\to
\text{vector spaces}
\to
\text{linear maps}
\to
\text{algorithms and applications}.
$$

This is why linear algebra can be read in several ways. It is a theory of equations, a geometry of space, an algebra of transformations, and a computational method for modern data.