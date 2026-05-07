---
title: "Appendix E. Calculus Review"
---

# Appendix E. Calculus Review

Linear algebra can be developed without much calculus, but many applications use both subjects together. Differential equations, optimization, least squares, matrix exponentials, Fourier analysis, numerical methods, and machine learning all rely on calculus ideas.

This appendix reviews the calculus needed later in the book. The purpose is not to replace a calculus course. It is to collect the definitions and formulas that occur most often in linear algebra applications.

## E.1 Functions of One Variable

A function of one real variable assigns a real number \(f(x)\) to each input \(x\) in its domain.

$$
f : D \to \mathbb{R},
\qquad
x \mapsto f(x).
$$

For example,

$$
f(x)=x^2+3x-1
$$

defines a function on all real numbers.

The graph of \(f\) is the set of points

$$
\{(x,f(x)) : x \in D\}.
$$

A function may be studied locally, near a single point, or globally, over its whole domain. Calculus studies how functions change, how they accumulate area, and how they can be approximated by simpler functions.

## E.2 Limits

The limit

$$
\lim_{x\to a} f(x)=L
$$

means that \(f(x)\) becomes arbitrarily close to \(L\) when \(x\) is sufficiently close to \(a\), with \(x\neq a\).

Limits describe local behavior. They do not depend only on the value \(f(a)\). A function may have a limit at \(a\) even if \(f(a)\) is undefined.

For example,

$$
f(x)=\frac{x^2-1}{x-1}
$$

is undefined at \(x=1\), but for \(x\neq 1\),

$$
\frac{x^2-1}{x-1} =
\frac{(x-1)(x+1)}{x-1} =
x+1.
$$

Thus

$$
\lim_{x\to 1}\frac{x^2-1}{x-1}=2.
$$

Limits are used to define derivatives, continuity, integrals, and infinite series.

## E.3 Continuity

A function \(f\) is continuous at \(a\) if

$$
\lim_{x\to a} f(x)=f(a).
$$

This condition includes three requirements:

| Requirement | Meaning |
|---|---|
| \(f(a)\) exists | The function is defined at \(a\) |
| \(\lim_{x\to a}f(x)\) exists | Nearby values approach one number |
| The two are equal | The function has no jump or hole at \(a\) |

A function is continuous on an interval if it is continuous at every point of that interval.

Polynomials are continuous everywhere. Rational functions are continuous wherever their denominators are nonzero.

Continuity matters in linear algebra because many matrix-valued expressions depend continuously on their entries. Determinants, matrix products, eigenvalue approximations, and norms are all studied using continuity.

## E.4 Derivatives

The derivative of \(f\) at \(a\) is

$$
f'(a) =
\lim_{h\to 0}
\frac{f(a+h)-f(a)}{h},
$$

when this limit exists.

The derivative measures the instantaneous rate of change of \(f\) at \(a\). Geometrically, it is the slope of the tangent line to the graph of \(f\) at \(a\).

For example, if

$$
f(x)=x^2,
$$

then

$$
f'(a) =
\lim_{h\to 0}
\frac{(a+h)^2-a^2}{h}.
$$

Expanding,

$$
(a+h)^2-a^2 =
2ah+h^2.
$$

Thus

$$
\frac{(a+h)^2-a^2}{h} =
2a+h.
$$

Taking the limit gives

$$
f'(a)=2a.
$$

Therefore,

$$
\frac{d}{dx}x^2=2x.
$$

## E.5 Basic Differentiation Rules

The following rules are used throughout applied linear algebra.

| Rule | Formula |
|---|---|
| Constant rule | \(\frac{d}{dx}c=0\) |
| Power rule | \(\frac{d}{dx}x^n=nx^{n-1}\) |
| Constant multiple rule | \(\frac{d}{dx}(cf)=cf'\) |
| Sum rule | \(\frac{d}{dx}(f+g)=f'+g'\) |
| Product rule | \(\frac{d}{dx}(fg)=f'g+fg'\) |
| Quotient rule | \(\frac{d}{dx}\left(\frac{f}{g}\right)=\frac{f'g-fg'}{g^2}\) |
| Chain rule | \(\frac{d}{dx}f(g(x))=f'(g(x))g'(x)\) |

### Example

Let

$$
f(x)=(x^2+1)^5.
$$

By the chain rule,

$$
f'(x) =
5(x^2+1)^4(2x) =
10x(x^2+1)^4.
$$

The chain rule is especially important in optimization and machine learning, where functions are often built as compositions of simpler maps.

## E.6 Higher Derivatives

The second derivative is the derivative of the derivative:

$$
f''(x)=\frac{d}{dx}f'(x).
$$

More generally, the \(k\)-th derivative is denoted by

$$
f^{(k)}(x).
$$

If

$$
f(x)=x^4,
$$

then

$$
f'(x)=4x^3,
$$

$$
f''(x)=12x^2,
$$

$$
f^{(3)}(x)=24x,
$$

and

$$
f^{(4)}(x)=24.
$$

The first derivative measures slope. The second derivative measures curvature. Higher derivatives appear in Taylor polynomials and error estimates.

## E.7 Critical Points and Optimization

A critical point of a differentiable function \(f\) is a point \(a\) where

$$
f'(a)=0.
$$

At such a point, the tangent line is horizontal. Local maxima and local minima often occur at critical points.

If \(f\) is twice differentiable, then the second derivative test gives a useful classification:

| Condition | Conclusion |
|---|---|
| \(f'(a)=0\), \(f''(a)>0\) | Local minimum |
| \(f'(a)=0\), \(f''(a)<0\) | Local maximum |
| \(f'(a)=0\), \(f''(a)=0\) | Test inconclusive |

### Example

Let

$$
f(x)=x^2-4x+7.
$$

Then

$$
f'(x)=2x-4.
$$

Set

$$
2x-4=0.
$$

Thus

$$
x=2.
$$

Since

$$
f''(x)=2>0,
$$

the function has a local minimum at \(x=2\). The minimum value is

$$
f(2)=4-8+7=3.
$$

Optimization in higher dimensions generalizes this idea using gradients and Hessian matrices.

## E.8 Integrals

The definite integral

$$
\int_a^b f(x)\,dx
$$

measures signed accumulation of \(f\) over the interval \([a,b]\). Geometrically, it measures signed area under the graph.

An antiderivative of \(f\) is a function \(F\) such that

$$
F'(x)=f(x).
$$

The indefinite integral is written

$$
\int f(x)\,dx = F(x)+C,
$$

where \(C\) is an arbitrary constant.

### Example

Since

$$
\frac{d}{dx}x^3=3x^2,
$$

we have

$$
\int 3x^2\,dx=x^3+C.
$$

Integrals appear in continuous least squares, Fourier coefficients, inner products of functions, probability, and differential equations.

## E.9 Fundamental Theorem of Calculus

The fundamental theorem of calculus connects derivatives and integrals.

If \(f\) is continuous on \([a,b]\) and \(F\) is an antiderivative of \(f\), then

$$
\int_a^b f(x)\,dx =
F(b)-F(a).
$$

For example,

$$
\int_0^1 2x\,dx =
[x^2]_0^1 =
1^2-0^2 =
1.
$$

This theorem turns many integral problems into antiderivative problems. In linear algebra applications, it justifies many formulas involving continuous inner products and energy norms.

## E.10 Basic Integration Rules

| Rule | Formula |
|---|---|
| Constant multiple | \(\int cf(x)\,dx=c\int f(x)\,dx\) |
| Sum rule | \(\int(f+g)\,dx=\int f\,dx+\int g\,dx\) |
| Power rule | \(\int x^n\,dx=\frac{x^{n+1}}{n+1}+C,\ n\neq -1\) |
| Reciprocal rule | \(\int \frac{1}{x}\,dx=\ln |x|+C\) |
| Exponential rule | \(\int e^x\,dx=e^x+C\) |
| Sine rule | \(\int \sin x\,dx=-\cos x+C\) |
| Cosine rule | \(\int \cos x\,dx=\sin x+C\) |

### Example

$$
\int (3x^2-4x+1)\,dx =
x^3-2x^2+x+C.
$$

Integration rules are used less often than differentiation rules in basic linear algebra, but they become essential when vector spaces of functions are studied.

## E.11 Integration by Parts

Integration by parts follows from the product rule. If \(u\) and \(v\) are differentiable functions, then

$$
\int u\,dv =
uv-\int v\,du.
$$

Equivalently,

$$
\int_a^b u(x)v'(x)\,dx =
[u(x)v(x)]_a^b -
\int_a^b u'(x)v(x)\,dx.
$$

This identity is important in differential equations, Fourier analysis, and weak formulations of linear systems.

### Example

Compute

$$
\int x e^x\,dx.
$$

Let

$$
u=x,
\qquad
dv=e^x\,dx.
$$

Then

$$
du=dx,
\qquad
v=e^x.
$$

Therefore,

$$
\int x e^x\,dx =
xe^x-\int e^x\,dx =
xe^x-e^x+C.
$$

## E.12 Functions of Several Variables

A function of several variables has the form

$$
f:\mathbb{R}^n\to\mathbb{R}.
$$

For example,

$$
f(x,y)=x^2+xy+y^2
$$

is a function from \(\mathbb{R}^2\) to \(\mathbb{R}\).

In vector notation, we often write

$$
f(x)
$$

where

$$
x=
\begin{bmatrix}
x_1 \\
\vdots \\
x_n
\end{bmatrix}.
$$

Such functions occur constantly in optimization. A common example is the least squares objective

$$
f(x)=\|Ax-b\|^2.
$$

This is a scalar-valued function of a vector variable.

## E.13 Partial Derivatives

The partial derivative of \(f(x_1,\ldots,x_n)\) with respect to \(x_i\) measures how \(f\) changes when \(x_i\) varies and all other variables are held fixed.

It is denoted by

$$
\frac{\partial f}{\partial x_i}.
$$

### Example

Let

$$
f(x,y)=x^2y+3y^2.
$$

Then

$$
\frac{\partial f}{\partial x} =
2xy,
$$

because \(y\) is treated as constant.

Also,

$$
\frac{\partial f}{\partial y} =
x^2+6y.
$$

Partial derivatives are the building blocks of gradients, Jacobians, and Hessians.

## E.14 Gradient

For a differentiable function

$$
f:\mathbb{R}^n\to\mathbb{R},
$$

the gradient is the vector of partial derivatives:

$$
\nabla f(x) =
\begin{bmatrix}
\frac{\partial f}{\partial x_1}(x) \\
\frac{\partial f}{\partial x_2}(x) \\
\vdots \\
\frac{\partial f}{\partial x_n}(x)
\end{bmatrix}.
$$

The gradient points in the direction of steepest increase of the function.

### Example

Let

$$
f(x,y)=x^2+xy+y^2.
$$

Then

$$
\nabla f(x,y) =
\begin{bmatrix}
2x+y \\
x+2y
\end{bmatrix}.
$$

For optimization, critical points satisfy

$$
\nabla f(x)=0.
$$

In least squares, setting a gradient equal to zero leads to the normal equations.

## E.15 Hessian Matrix

The Hessian matrix of a twice differentiable function

$$
f:\mathbb{R}^n\to\mathbb{R}
$$

is the matrix of second partial derivatives:

$$
H_f(x) =
\begin{bmatrix}
\frac{\partial^2 f}{\partial x_1^2} &
\frac{\partial^2 f}{\partial x_1\partial x_2} &
\cdots &
\frac{\partial^2 f}{\partial x_1\partial x_n}
\\
\frac{\partial^2 f}{\partial x_2\partial x_1} &
\frac{\partial^2 f}{\partial x_2^2} &
\cdots &
\frac{\partial^2 f}{\partial x_2\partial x_n}
\\
\vdots & \vdots & \ddots & \vdots
\\
\frac{\partial^2 f}{\partial x_n\partial x_1} &
\frac{\partial^2 f}{\partial x_n\partial x_2} &
\cdots &
\frac{\partial^2 f}{\partial x_n^2}
\end{bmatrix}.
$$

The Hessian describes local curvature.

### Example

For

$$
f(x,y)=x^2+xy+y^2,
$$

we have

$$
H_f(x,y) =
\begin{bmatrix}
2 & 1 \\
1 & 2
\end{bmatrix}.
$$

This matrix is constant because \(f\) is a quadratic function.

Quadratic functions are central in linear algebra because their gradients are linear functions and their Hessians are constant matrices.

## E.16 Directional Derivatives

Let

$$
f:\mathbb{R}^n\to\mathbb{R}
$$

be differentiable, and let \(u\in\mathbb{R}^n\). The directional derivative of \(f\) at \(x\) in the direction \(u\) is

$$
D_u f(x) =
\lim_{t\to 0}
\frac{f(x+tu)-f(x)}{t}.
$$

If \(u\) is a unit vector, then \(D_u f(x)\) measures the rate of change of \(f\) per unit distance in the direction \(u\).

For differentiable functions,

$$
D_u f(x)=\nabla f(x)\cdot u.
$$

Thus the gradient contains all directional derivative information.

## E.17 Jacobian Matrix

For a differentiable vector-valued function

$$
F:\mathbb{R}^n\to\mathbb{R}^m,
$$

where

$$
F(x)=
\begin{bmatrix}
F_1(x) \\
\vdots \\
F_m(x)
\end{bmatrix},
$$

the Jacobian matrix is

$$
J_F(x) =
\begin{bmatrix}
\frac{\partial F_1}{\partial x_1} &
\cdots &
\frac{\partial F_1}{\partial x_n}
\\
\vdots & \ddots & \vdots
\\
\frac{\partial F_m}{\partial x_1} &
\cdots &
\frac{\partial F_m}{\partial x_n}
\end{bmatrix}.
$$

The Jacobian is the best linear approximation to \(F\) near \(x\).

For a linear map

$$
F(x)=Ax,
$$

the Jacobian is simply

$$
J_F(x)=A.
$$

Thus matrices appear naturally as derivatives of vector-valued functions.

## E.18 Taylor Polynomials

Taylor polynomials approximate a differentiable function near a point by a polynomial. For a function \(f\) with sufficiently many derivatives, the Taylor polynomial of degree \(n\) about \(a\) is

$$
T_n(x) =
f(a)+f'(a)(x-a)+\frac{f''(a)}{2!}(x-a)^2+\cdots+
\frac{f^{(n)}(a)}{n!}(x-a)^n.
$$

The corresponding Taylor series is

$$
\sum_{k=0}^{\infty}
\frac{f^{(k)}(a)}{k!}(x-a)^k.
$$

When \(a=0\), it is called a Maclaurin series.

Taylor expansions are used to approximate nonlinear functions by linear or quadratic functions. This is the bridge from nonlinear problems back to linear algebra.

For small \(h\),

$$
f(a+h)
\approx
f(a)+f'(a)h.
$$

This is the first-order, or linear, approximation.

For a function of several variables,

$$
f(x+h)
\approx
f(x)+\nabla f(x)^T h.
$$

The right-hand side is affine in \(h\). Its linear part is determined by the gradient.

## E.19 Common Taylor Series

The following Taylor series are frequently used:

| Function | Series near \(0\) |
|---|---|
| \(e^x\) | \(\sum_{k=0}^{\infty}\frac{x^k}{k!}\) |
| \(\sin x\) | \(\sum_{k=0}^{\infty}(-1)^k\frac{x^{2k+1}}{(2k+1)!}\) |
| \(\cos x\) | \(\sum_{k=0}^{\infty}(-1)^k\frac{x^{2k}}{(2k)!}\) |
| \(\frac{1}{1-x}\) | \(\sum_{k=0}^{\infty}x^k,\ |x|<1\) |
| \(\ln(1+x)\) | \(\sum_{k=1}^{\infty}(-1)^{k+1}\frac{x^k}{k},\ |x|<1\) |

These expansions are used in matrix functions. For example, the matrix exponential is defined by replacing \(x\) with a square matrix \(A\):

$$
e^A =
I+A+\frac{A^2}{2!}+\frac{A^3}{3!}+\cdots.
$$

## E.20 Differential Equations

A differential equation is an equation involving an unknown function and its derivatives.

A first-order linear differential equation may have the form

$$
x'(t)=ax(t).
$$

Its solution is

$$
x(t)=Ce^{at}.
$$

For systems, one obtains

$$
x'(t)=Ax(t),
$$

where \(A\) is a matrix and \(x(t)\) is a vector-valued function.

The solution is expressed using the matrix exponential:

$$
x(t)=e^{tA}x(0).
$$

Thus linear algebra gives the natural language for systems of differential equations.

## E.21 Inner Products of Functions

Calculus allows vector space ideas to be applied to functions.

For continuous functions on \([a,b]\), define

$$
\langle f,g\rangle =
\int_a^b f(x)g(x)\,dx.
$$

This is an inner product on a suitable function space.

The corresponding norm is

$$
\|f\| =
\sqrt{
\int_a^b f(x)^2\,dx
}.
$$

Orthogonality means

$$
\int_a^b f(x)g(x)\,dx=0.
$$

This idea leads to Fourier series, orthogonal polynomials, projection methods, and continuous least squares.

## E.22 Summary

Calculus studies change, accumulation, approximation, and motion. Linear algebra studies vectors, matrices, spaces, and linear transformations. The two subjects meet whenever a problem is approximated, optimized, discretized, or written as a system.

Key ideas from this appendix include:

| Concept | Role in linear algebra |
|---|---|
| Derivative | Local rate of change |
| Gradient | Vector of first derivatives |
| Hessian | Matrix of second derivatives |
| Jacobian | Matrix of a derivative |
| Integral | Continuous accumulation |
| Taylor polynomial | Linear and quadratic approximation |
| Differential equation | Dynamics expressed by matrices |
| Function inner product | Geometry of function spaces |

The most important connection is this: the derivative of a sufficiently smooth function is a linear approximation. That is why matrices occur throughout calculus-based applications.