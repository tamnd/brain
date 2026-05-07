---
title: "Appendix C. Real and Complex Numbers"
---

# Appendix C. Real and Complex Numbers

Linear algebra is usually developed over a field of scalars. The two most common scalar fields are the real numbers \(\mathbb{R}\) and the complex numbers \(\mathbb{C}\). A real vector space allows real scalar multiplication. A complex vector space allows complex scalar multiplication. This distinction affects eigenvalues, inner products, matrix factorizations, and spectral theory.

## C.1 The Real Numbers

The real numbers form the number system used for ordinary measurement. They include integers, rational numbers, and irrational numbers.

$$
\mathbb{Z} \subseteq \mathbb{Q} \subseteq \mathbb{R}.
$$

A real number may be positive, negative, or zero. It can be placed on the real line. Addition and multiplication of real numbers satisfy the usual algebraic laws:

| Law | Formula |
|---|---|
| Associativity of addition | \((a+b)+c=a+(b+c)\) |
| Commutativity of addition | \(a+b=b+a\) |
| Additive identity | \(a+0=a\) |
| Additive inverse | \(a+(-a)=0\) |
| Associativity of multiplication | \((ab)c=a(bc)\) |
| Commutativity of multiplication | \(ab=ba\) |
| Multiplicative identity | \(a\cdot 1=a\) |
| Multiplicative inverse | \(a\neq 0 \implies a^{-1}\text{ exists}\) |
| Distributivity | \(a(b+c)=ab+ac\) |

These laws make \(\mathbb{R}\) a field. A field is a scalar system in which addition, subtraction, multiplication, and division by nonzero elements are possible.

## C.2 Order on the Real Numbers

The real numbers are ordered. For real numbers \(a\) and \(b\), one may write

$$
a < b,
\qquad
a \leq b,
\qquad
a > b,
\qquad
a \geq b.
$$

The order is compatible with addition:

$$
a \leq b \implies a+c \leq b+c.
$$

It is also compatible with multiplication by nonnegative numbers:

$$
a \leq b,\ c \geq 0 \implies ac \leq bc.
$$

If \(c < 0\), the inequality reverses:

$$
a \leq b,\ c < 0 \implies ac \geq bc.
$$

Order is important in topics such as length, norm, positivity, optimization, and positive definite matrices. Complex numbers do not have an order compatible with field operations in the same way.

## C.3 Absolute Value

The absolute value of a real number \(x\) is

$$
|x| =
\begin{cases}
x, & x \geq 0, \\
-x, & x < 0.
\end{cases}
$$

It measures distance from zero on the real line.

For example,

$$
|5|=5,
\qquad
|-5|=5.
$$

The absolute value satisfies:

| Property | Formula |
|---|---|
| Nonnegativity | \(|x|\geq 0\) |
| Definiteness | \(|x|=0 \iff x=0\) |
| Multiplicativity | \(|xy|=|x||y|\) |
| Triangle inequality | \(|x+y|\leq |x|+|y|\) |

The triangle inequality is the one-dimensional prototype of norm inequalities in vector spaces.

## C.4 Distance on the Real Line

The distance between two real numbers \(a\) and \(b\) is

$$
|a-b|.
$$

For example, the distance between \(3\) and \(-2\) is

$$
|3-(-2)| = |5| = 5.
$$

This formula generalizes to Euclidean distance in \(\mathbb{R}^n\). If

$$
x=(x_1,\ldots,x_n),
\qquad
y=(y_1,\ldots,y_n),
$$

then the Euclidean distance is

$$
\sqrt{(x_1-y_1)^2+\cdots+(x_n-y_n)^2}.
$$

Thus the absolute value is the first example of a norm.

## C.5 Square Roots and Positivity

For every nonnegative real number \(a\), there exists a unique nonnegative real number \(\sqrt{a}\) such that

$$
(\sqrt{a})^2=a.
$$

For example,

$$
\sqrt{9}=3.
$$

The equation

$$
x^2=a
$$

has two real solutions when \(a>0\):

$$
x=\sqrt{a}
\quad \text{and} \quad
x=-\sqrt{a}.
$$

It has one real solution when \(a=0\), and no real solution when \(a<0\).

The failure of the equation

$$
x^2=-1
$$

to have a real solution leads to the complex numbers.

## C.6 The Complex Numbers

The complex numbers extend the real numbers by adjoining a new number \(i\), called the imaginary unit, satisfying

$$
i^2=-1.
$$

Every complex number has the form

$$
z=a+bi,
$$

where \(a,b\in\mathbb{R}\). The number \(a\) is the real part of \(z\), and \(b\) is the imaginary part of \(z\). The set of all complex numbers is denoted by \(\mathbb{C}\).

We write

$$
\operatorname{Re}(z)=a,
\qquad
\operatorname{Im}(z)=b.
$$

For example, if

$$
z=3-4i,
$$

then

$$
\operatorname{Re}(z)=3,
\qquad
\operatorname{Im}(z)=-4.
$$

A real number is a complex number with imaginary part zero:

$$
a = a+0i.
$$

Thus

$$
\mathbb{R} \subseteq \mathbb{C}.
$$

## C.7 Addition and Multiplication in \(\mathbb{C}\)

Complex numbers are added componentwise:

$$
(a+bi)+(c+di)=(a+c)+(b+d)i.
$$

For example,

$$
(2+3i)+(5-i)=7+2i.
$$

Multiplication is defined by the distributive law and the relation \(i^2=-1\):

$$
(a+bi)(c+di) =
ac+adi+bci+bd i^2.
$$

Since \(i^2=-1\),

$$
(a+bi)(c+di) =
(ac-bd)+(ad+bc)i.
$$

For example,

$$
(2+3i)(4-i) =
8-2i+12i-3i^2 =
11+10i.
$$

The complex numbers form a field. Addition, subtraction, multiplication, and division by nonzero complex numbers are all defined.

## C.8 Complex Conjugation

The complex conjugate of

$$
z=a+bi
$$

is

$$
\overline{z}=a-bi.
$$

Conjugation changes the sign of the imaginary part and leaves the real part unchanged.

For example,

$$
\overline{3+5i}=3-5i.
$$

Important identities include:

| Identity | Formula |
|---|---|
| Conjugate of a sum | \(\overline{z+w}=\overline{z}+\overline{w}\) |
| Conjugate of a product | \(\overline{zw}=\overline{z}\,\overline{w}\) |
| Double conjugation | \(\overline{\overline{z}}=z\) |
| Real criterion | \(z\in\mathbb{R}\iff z=\overline{z}\) |

Conjugation is essential in complex inner product spaces. It appears in Hermitian matrices, unitary matrices, and the complex spectral theorem.

## C.9 Modulus of a Complex Number

The modulus of

$$
z=a+bi
$$

is

$$
|z|=\sqrt{a^2+b^2}.
$$

Geometrically, this is the distance from the origin to the point \((a,b)\) in the complex plane.

The modulus satisfies

$$
|z| \geq 0,
$$

$$
|z|=0 \iff z=0,
$$

$$
|zw|=|z||w|,
$$

and

$$
|z+w|\leq |z|+|w|.
$$

The product of a complex number with its conjugate is real and nonnegative:

$$
z\overline{z}=|z|^2.
$$

Indeed, if \(z=a+bi\), then

$$
z\overline{z} =
(a+bi)(a-bi) =
a^2+b^2.
$$

This identity is used to divide by complex numbers.

## C.10 Division in \(\mathbb{C}\)

If \(z\neq 0\), then

$$
z^{-1}=\frac{\overline{z}}{|z|^2}.
$$

For

$$
z=a+bi,
$$

this gives

$$
\frac{1}{a+bi} =
\frac{a-bi}{a^2+b^2}.
$$

For example,

$$
\frac{1}{2+3i} =
\frac{2-3i}{2^2+3^2} =
\frac{2}{13}-\frac{3}{13}i.
$$

Thus division by a nonzero complex number reduces to multiplication by its conjugate divided by its squared modulus.

## C.11 The Complex Plane

A complex number

$$
z=a+bi
$$

can be represented by the point \((a,b)\) in the plane. The horizontal axis is the real axis, and the vertical axis is the imaginary axis.

This identifies \(\mathbb{C}\) with \(\mathbb{R}^2\) as a real vector space:

$$
a+bi \leftrightarrow (a,b).
$$

However, \(\mathbb{C}\) has more structure than \(\mathbb{R}^2\), because complex numbers can be multiplied.

Multiplication by \(i\) sends

$$
a+bi
$$

to

$$
i(a+bi)=ai+b i^2=-b+ai.
$$

In coordinate form,

$$
(a,b) \mapsto (-b,a).
$$

This is rotation by \(90^\circ\) counterclockwise.

Thus complex multiplication has a geometric interpretation: it combines scaling and rotation.

## C.12 Polar Form

A nonzero complex number can be written in polar form:

$$
z=r(\cos\theta+i\sin\theta),
$$

where

$$
r=|z|
$$

and \(\theta\) is an argument of \(z\).

The number \(r\) is the distance from the origin. The angle \(\theta\) is measured from the positive real axis.

If

$$
z=a+bi,
$$

then

$$
a=r\cos\theta,
\qquad
b=r\sin\theta.
$$

Polar form is useful because multiplication becomes simple:

$$
r(\cos\theta+i\sin\theta)\,s(\cos\phi+i\sin\phi) =
rs(\cos(\theta+\phi)+i\sin(\theta+\phi)).
$$

Thus multiplying complex numbers multiplies their moduli and adds their arguments.

## C.13 Euler's Formula

Euler's formula states that

$$
e^{i\theta}=\cos\theta+i\sin\theta.
$$

Using this notation, polar form becomes

$$
z=re^{i\theta}.
$$

Multiplication is then

$$
(re^{i\theta})(se^{i\phi})=rs e^{i(\theta+\phi)}.
$$

Euler's formula connects algebra, geometry, and analysis. In linear algebra, it appears in rotations, complex eigenvalues, Fourier analysis, unitary matrices, and matrix exponentials.

## C.14 Real and Complex Vector Spaces

A real vector space uses scalars from \(\mathbb{R}\). A complex vector space uses scalars from \(\mathbb{C}\).

For example, \(\mathbb{R}^n\) is a real vector space. Its vectors have real components, and scalar multiplication uses real numbers.

The space \(\mathbb{C}^n\) is a complex vector space. Its vectors have complex components, and scalar multiplication uses complex numbers.

Every complex vector space can also be viewed as a real vector space by restricting scalars from \(\mathbb{C}\) to \(\mathbb{R}\). For example, \(\mathbb{C}\) has dimension \(1\) over \(\mathbb{C}\), but dimension \(2\) over \(\mathbb{R}\).

Indeed,

$$
\mathbb{C} = \{a+bi : a,b\in\mathbb{R}\}.
$$

As a real vector space, a basis is

$$
\{1,i\}.
$$

As a complex vector space, a basis is

$$
\{1\}.
$$

The scalar field affects dimension.

## C.15 Real Matrices and Complex Matrices

A real matrix has entries in \(\mathbb{R}\). A complex matrix has entries in \(\mathbb{C}\).

A real matrix may still have complex eigenvalues. For example,

$$
A=
\begin{bmatrix}
0 & -1 \\
1 & 0
\end{bmatrix}
$$

represents rotation by \(90^\circ\) in \(\mathbb{R}^2\). Its characteristic polynomial is

$$
\lambda^2+1.
$$

This polynomial has no real roots. Over \(\mathbb{C}\), it has roots

$$
\lambda=i
\quad \text{and} \quad
\lambda=-i.
$$

Thus complex numbers are needed for a complete eigenvalue theory. The fundamental theorem of algebra states that every nonconstant polynomial with complex coefficients has a complex root, so polynomial equations behave more completely over \(\mathbb{C}\) than over \(\mathbb{R}\).

## C.16 Conjugate Transpose

For a complex matrix \(A\), the transpose alone is usually not the correct analogue of the real transpose. Instead one uses the conjugate transpose.

If

$$
A=(a_{ij}),
$$

then the conjugate transpose of \(A\) is denoted by

$$
A^*
$$

and is defined by

$$
(A^*)_{ij}=\overline{a_{ji}}.
$$

Thus \(A^*\) is obtained by transposing \(A\) and conjugating each entry.

For example, if

$$
A=
\begin{bmatrix}
1+i & 2 \\
3i & 4-i
\end{bmatrix},
$$

then

$$
A^* =
\begin{bmatrix}
1-i & -3i \\
2 & 4+i
\end{bmatrix}.
$$

The conjugate transpose is central in complex inner product spaces.

## C.17 Real and Complex Inner Products

On \(\mathbb{R}^n\), the standard inner product is

$$
x \cdot y = x_1y_1+\cdots+x_ny_n.
$$

On \(\mathbb{C}^n\), the standard inner product usually includes complex conjugation:

$$
\langle x,y\rangle =
\overline{x_1}y_1+\cdots+\overline{x_n}y_n.
$$

Some authors place the conjugate on the second variable instead. This book uses the convention above unless otherwise stated.

The conjugate is needed so that

$$
\langle x,x\rangle
$$

is real and nonnegative.

Indeed, if

$$
x=(x_1,\ldots,x_n),
$$

then

$$
\langle x,x\rangle =
|x_1|^2+\cdots+|x_n|^2.
$$

This quantity is zero only when \(x=0\).

## C.18 Hermitian and Unitary Matrices

A complex square matrix \(A\) is Hermitian if

$$
A^*=A.
$$

Hermitian matrices are the complex analogue of real symmetric matrices. Their eigenvalues are real, and they have strong orthogonality properties.

A complex square matrix \(U\) is unitary if

$$
U^*U=UU^*=I.
$$

Unitary matrices are the complex analogue of real orthogonal matrices. They preserve inner products and norms.

In real linear algebra, the corresponding conditions are

$$
A^T=A
$$

for symmetric matrices and

$$
Q^TQ=QQ^T=I
$$

for orthogonal matrices.

## C.19 Choosing the Scalar Field

The choice between \(\mathbb{R}\) and \(\mathbb{C}\) depends on the problem.

| Use \(\mathbb{R}\) when | Use \(\mathbb{C}\) when |
|---|---|
| Quantities are naturally real-valued | Eigenvalues may be complex |
| Geometry takes place in real space | Rotations and oscillations are central |
| Order and positivity matter directly | Polynomial factorization is important |
| Optimization uses real variables | Fourier methods are used |
| Symmetric matrices are enough | Hermitian and unitary structure appears |

Many real problems are temporarily extended to \(\mathbb{C}\) because the complex setting gives cleaner algebra. After solving the complex problem, one may return to the real interpretation.

## C.20 Summary

The real numbers provide order, distance, positivity, and the usual scalar system for geometry and computation. The complex numbers extend the real numbers by introducing \(i\), where \(i^2=-1\). Every complex number has the form \(a+bi\), and complex arithmetic follows from ordinary algebra together with this defining relation.

For linear algebra, the main points are:

| Concept | Real case | Complex case |
|---|---|---|
| Scalar field | \(\mathbb{R}\) | \(\mathbb{C}\) |
| Standard space | \(\mathbb{R}^n\) | \(\mathbb{C}^n\) |
| Transpose analogue | \(A^T\) | \(A^*\) |
| Symmetric analogue | Symmetric matrix | Hermitian matrix |
| Orthogonal analogue | Orthogonal matrix | Unitary matrix |
| Eigenvalue theory | May require complex roots | Algebraically complete |

Real and complex numbers are both fundamental. Real numbers support geometry and measurement. Complex numbers complete the algebraic picture and make spectral theory more natural.