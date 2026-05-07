---
title: "Appendix A. Set Theory and Logic"
---

# Appendix A. Set Theory and Logic

Linear algebra uses a small amount of set theory and logic. The main ideas are sets, elements, functions, relations, quantifiers, and proof. These notions give precise meaning to statements such as “let \(V\) be a vector space,” “for every vector \(v \in V\),” and “there exists a unique solution.”

This appendix gives only the background needed for the rest of the book. It uses informal set theory, in the usual style of undergraduate mathematics.

## A.1 Sets

A set is a collection of objects. The objects in a set are called its elements.

If \(x\) is an element of a set \(A\), we write

$$
x \in A.
$$

If \(x\) is not an element of \(A\), we write

$$
x \notin A.
$$

For example, if

$$
A = \{1,2,3\},
$$

then

$$
2 \in A,
\qquad
5 \notin A.
$$

Sets are determined by their elements. The order in which the elements are written does not matter, and repeated entries do not change the set:

$$
\{1,2,3\} = \{3,2,1\} = \{1,1,2,3\}.
$$

This is different from a vector, where order and repetition do matter. For example,

$$
(1,2) \neq (2,1).
$$

## A.2 Common Sets of Numbers

The following sets occur throughout linear algebra.

| Symbol | Meaning |
|---|---|
| \(\mathbb{N}\) | Natural numbers |
| \(\mathbb{Z}\) | Integers |
| \(\mathbb{Q}\) | Rational numbers |
| \(\mathbb{R}\) | Real numbers |
| \(\mathbb{C}\) | Complex numbers |

Different authors use different conventions for \(\mathbb{N}\). Some include \(0\), while others begin with \(1\). When this distinction matters, it will be stated explicitly.

Linear algebra usually takes scalars from a field. The most common fields are

$$
\mathbb{R}
\quad \text{and} \quad
\mathbb{C}.
$$

Thus many vector spaces in this book are real vector spaces or complex vector spaces.

## A.3 Subsets

A set \(A\) is a subset of a set \(B\) if every element of \(A\) is also an element of \(B\). We write

$$
A \subseteq B.
$$

This means

$$
x \in A \implies x \in B.
$$

For example,

$$
\{1,2\} \subseteq \{1,2,3\}.
$$

If \(A \subseteq B\) and \(A \neq B\), then \(A\) is a proper subset of \(B\). Some authors write this as

$$
A \subset B.
$$

Because notation varies, this book uses \(\subseteq\) when equality is allowed.

## A.4 The Empty Set

The empty set is the set with no elements. It is denoted by

$$
\varnothing.
$$

The empty set is a subset of every set:

$$
\varnothing \subseteq A.
$$

This statement is true because there is no element of \(\varnothing\) that violates the condition for being in \(A\).

The empty set should not be confused with the set containing the empty set:

$$
\varnothing \neq \{\varnothing\}.
$$

The first set has no elements. The second set has one element, namely \(\varnothing\).

## A.5 Set Operations

Given two sets \(A\) and \(B\), their union is the set of elements that belong to at least one of them:

$$
A \cup B = \{x : x \in A \text{ or } x \in B\}.
$$

Their intersection is the set of elements that belong to both:

$$
A \cap B = \{x : x \in A \text{ and } x \in B\}.
$$

Their difference is the set of elements in \(A\) but not in \(B\):

$$
A \setminus B = \{x : x \in A \text{ and } x \notin B\}.
$$

For example, if

$$
A = \{1,2,3\},
\qquad
B = \{3,4,5\},
$$

then

$$
A \cup B = \{1,2,3,4,5\},
$$

$$
A \cap B = \{3\},
$$

and

$$
A \setminus B = \{1,2\}.
$$

Two sets are disjoint if their intersection is empty:

$$
A \cap B = \varnothing.
$$

## A.6 Cartesian Products

The Cartesian product of two sets \(A\) and \(B\) is the set of all ordered pairs \((a,b)\), where \(a \in A\) and \(b \in B\):

$$
A \times B = \{(a,b) : a \in A,\ b \in B\}.
$$

For example, if

$$
A = \{1,2\},
\qquad
B = \{x,y\},
$$

then

$$
A \times B =
\{(1,x),(1,y),(2,x),(2,y)\}.
$$

The order matters. In general,

$$
A \times B \neq B \times A.
$$

The set \(\mathbb{R}^2\) is the Cartesian product

$$
\mathbb{R} \times \mathbb{R}.
$$

Its elements are ordered pairs

$$
(x,y).
$$

Similarly,

$$
\mathbb{R}^n
$$

is the set of all ordered \(n\)-tuples of real numbers.

## A.7 Tuples

An ordered \(n\)-tuple is a finite ordered list

$$
(a_1,a_2,\ldots,a_n).
$$

The entries may repeat, and their order matters. Thus

$$
(1,2,1)
$$

is a valid tuple, and

$$
(1,2) \neq (2,1).
$$

Vectors in \(\mathbb{R}^n\) are often represented as tuples or as column arrays. The tuple

$$
(x_1,\ldots,x_n)
$$

and the column vector

$$
\begin{bmatrix}
x_1 \\
\vdots \\
x_n
\end{bmatrix}
$$

contain the same data, but the column form is better suited to matrix multiplication.

## A.8 Functions

A function from a set \(A\) to a set \(B\) assigns to each element of \(A\) exactly one element of \(B\). We write

$$
f : A \to B.
$$

The set \(A\) is called the domain. The set \(B\) is called the codomain.

If \(a \in A\), then \(f(a)\) denotes the value of the function at \(a\).

For example,

$$
f : \mathbb{R} \to \mathbb{R},
\qquad
f(x) = x^2
$$

defines a function from the real numbers to the real numbers.

A function must assign exactly one output to each input. A rule that assigns two different outputs to the same input is not a function.

## A.9 Image and Preimage

Let

$$
f : A \to B
$$

be a function.

The image of a subset \(S \subseteq A\) is

$$
f(S) = \{f(s) : s \in S\}.
$$

The image of the whole domain is

$$
f(A) = \{f(a) : a \in A\}.
$$

This is also called the range of \(f\).

If \(T \subseteq B\), then the preimage of \(T\) is

$$
f^{-1}(T) = \{a \in A : f(a) \in T\}.
$$

The notation \(f^{-1}(T)\) does not require \(f\) to have an inverse function. It means all inputs whose outputs lie in \(T\).

In linear algebra, if

$$
T : V \to W
$$

is a linear map, then the image of \(T\) is

$$
\operatorname{im}(T) = \{T(v) : v \in V\}.
$$

The kernel of \(T\) is the preimage of \(\{0\}\):

$$
\ker(T) = T^{-1}(\{0\}).
$$

## A.10 Injective, Surjective, and Bijective Functions

A function

$$
f : A \to B
$$

is injective if different inputs always have different outputs. Equivalently,

$$
f(a_1) = f(a_2) \implies a_1 = a_2.
$$

An injective function is also called one-to-one.

The function is surjective if every element of the codomain is hit by the function. That is,

$$
\forall b \in B,\ \exists a \in A \text{ such that } f(a)=b.
$$

A surjective function is also called onto.

The function is bijective if it is both injective and surjective. A bijective function gives an exact pairing between the elements of \(A\) and the elements of \(B\).

Bijective functions have inverse functions. If \(f : A \to B\) is bijective, then there exists a function

$$
f^{-1} : B \to A
$$

such that

$$
f^{-1}(f(a)) = a
$$

for all \(a \in A\), and

$$
f(f^{-1}(b)) = b
$$

for all \(b \in B\).

In linear algebra, an invertible linear transformation is a bijective linear transformation.

## A.11 Relations

A relation from \(A\) to \(B\) is a subset of the Cartesian product \(A \times B\).

If \(R \subseteq A \times B\), then \((a,b) \in R\) means that \(a\) is related to \(b\).

A relation on a set \(A\) is a subset of

$$
A \times A.
$$

Important examples include equality, order relations, and equivalence relations.

A relation \(\sim\) on \(A\) is an equivalence relation if it satisfies three properties.

| Property | Meaning |
|---|---|
| Reflexive | \(a \sim a\) |
| Symmetric | \(a \sim b \implies b \sim a\) |
| Transitive | \(a \sim b\) and \(b \sim c \implies a \sim c\) |

Equivalence relations divide a set into equivalence classes. In linear algebra, quotient spaces are built from equivalence classes of vectors.

## A.12 Quantifiers

Mathematical statements often use quantifiers.

The universal quantifier means “for all”:

$$
\forall.
$$

The existential quantifier means “there exists”:

$$
\exists.
$$

For example,

$$
\forall x \in \mathbb{R},\ x^2 \geq 0
$$

means that every real number has a nonnegative square.

The statement

$$
\exists x \in \mathbb{R} \text{ such that } x^2 = 4
$$

means that at least one real number has square \(4\).

There is also a uniqueness quantifier:

$$
\exists!
$$

The statement

$$
\exists! x \in A \text{ such that } P(x)
$$

means that there exists exactly one element \(x\) in \(A\) for which the property \(P(x)\) holds.

## A.13 Implication and Equivalence

An implication has the form

$$
P \implies Q.
$$

It means that if \(P\) is true, then \(Q\) is true.

The converse is

$$
Q \implies P.
$$

The converse of a true statement may be false.

For example, if a square matrix is invertible, then its columns are linearly independent. The converse is also true in this case, but this must be proved separately.

Two statements \(P\) and \(Q\) are equivalent if each implies the other:

$$
P \iff Q.
$$

This means

$$
P \implies Q
$$

and

$$
Q \implies P.
$$

In mathematics, the phrase “if and only if” means logical equivalence.

## A.14 Negation

The negation of a statement \(P\) is written

$$
\neg P.
$$

It means that \(P\) is false.

Negating quantified statements requires care.

The negation of

$$
\forall x \in A,\ P(x)
$$

is

$$
\exists x \in A \text{ such that } \neg P(x).
$$

The negation of

$$
\exists x \in A \text{ such that } P(x)
$$

is

$$
\forall x \in A,\ \neg P(x).
$$

For example, the negation of

$$
\forall x \in \mathbb{R},\ x > 0
$$

is

$$
\exists x \in \mathbb{R} \text{ such that } x \leq 0.
$$

## A.15 Proof by Direct Argument

A direct proof begins with assumptions and uses definitions, known facts, and algebraic manipulation to reach the desired conclusion.

For example, suppose \(a\) and \(b\) are even integers. Then there exist integers \(m\) and \(n\) such that

$$
a = 2m,
\qquad
b = 2n.
$$

Then

$$
a+b = 2m + 2n = 2(m+n).
$$

Since \(m+n\) is an integer, \(a+b\) is even.

This proof uses only the definition of evenness and elementary algebra.

## A.16 Proof by Contrapositive

The contrapositive of

$$
P \implies Q
$$

is

$$
\neg Q \implies \neg P.
$$

An implication and its contrapositive are logically equivalent.

To prove \(P \implies Q\), it is often easier to prove the contrapositive.

For example, to prove that if \(n^2\) is even, then \(n\) is even, one may prove the contrapositive: if \(n\) is odd, then \(n^2\) is odd.

If \(n\) is odd, then

$$
n = 2k+1
$$

for some integer \(k\). Thus

$$
n^2 = (2k+1)^2 = 4k^2 + 4k + 1 = 2(2k^2+2k) + 1.
$$

Therefore \(n^2\) is odd. Hence, by contrapositive reasoning, if \(n^2\) is even, then \(n\) is even.

## A.17 Proof by Contradiction

In proof by contradiction, one assumes that the desired conclusion is false and derives an impossibility.

For example, to prove that \(\sqrt{2}\) is irrational, assume that

$$
\sqrt{2} = \frac{p}{q}
$$

where \(p\) and \(q\) are integers with no common factor and \(q \neq 0\). Then

$$
2 = \frac{p^2}{q^2},
$$

so

$$
p^2 = 2q^2.
$$

Thus \(p^2\) is even, so \(p\) is even. Write \(p=2k\). Then

$$
4k^2 = 2q^2,
$$

so

$$
q^2 = 2k^2.
$$

Thus \(q^2\) is even, so \(q\) is even. Hence both \(p\) and \(q\) are even, contradicting the assumption that they have no common factor.

Therefore \(\sqrt{2}\) is irrational.

## A.18 Existence and Uniqueness

Many theorems in linear algebra have two parts: existence and uniqueness.

An existence proof shows that at least one object satisfies a property.

A uniqueness proof shows that no two distinct objects satisfy that property.

For example, to prove that the zero vector is unique, suppose \(0\) and \(0'\) are both zero vectors in a vector space \(V\). By definition,

$$
0 + 0' = 0'
$$

because \(0\) is a zero vector. Also,

$$
0 + 0' = 0
$$

because \(0'\) is a zero vector. Therefore,

$$
0 = 0'.
$$

Thus the zero vector is unique.

## A.19 Indexed Families

An indexed family is a collection of objects labeled by elements of an index set.

For example,

$$
(v_i)_{i \in I}
$$

denotes a family of vectors indexed by the set \(I\).

If \(I = \{1,2,\ldots,n\}\), then the family is finite:

$$
v_1, v_2, \ldots, v_n.
$$

Linear combinations are usually built from finite indexed families:

$$
\sum_{i=1}^{n} c_i v_i.
$$

The summation notation means

$$
c_1v_1 + c_2v_2 + \cdots + c_nv_n.
$$

Indexed notation is compact and becomes essential when working with matrices, bases, coordinates, and finite-dimensional spaces.

## A.20 Mathematical Induction

Mathematical induction is a proof method for statements indexed by natural numbers.

To prove that a statement \(P(n)\) holds for all \(n \geq n_0\), prove two things.

| Step | Purpose |
|---|---|
| Base case | Prove \(P(n_0)\) |
| Induction step | Prove \(P(k) \implies P(k+1)\) |

For example, prove that

$$
1 + 2 + \cdots + n = \frac{n(n+1)}{2}
$$

for all \(n \geq 1\).

For \(n=1\),

$$
1 = \frac{1(1+1)}{2}.
$$

So the base case holds.

Assume the formula holds for \(n=k\):

$$
1 + 2 + \cdots + k = \frac{k(k+1)}{2}.
$$

Then

$$
1 + 2 + \cdots + k + (k+1) =
\frac{k(k+1)}{2} + (k+1).
$$

Factor:

$$
\frac{k(k+1)}{2} + (k+1) =
\frac{k(k+1)+2(k+1)}{2} =
\frac{(k+1)(k+2)}{2}.
$$

This is the desired formula for \(k+1\). Therefore, by induction,

$$
1 + 2 + \cdots + n = \frac{n(n+1)}{2}
$$

for all \(n \geq 1\).

## A.21 Partitions

A partition of a set \(A\) is a collection of nonempty subsets of \(A\) such that each element of \(A\) belongs to exactly one subset in the collection.

For example,

$$
\{\{1,3\},\{2,4\}\}
$$

is a partition of

$$
\{1,2,3,4\}.
$$

The blocks of a partition are disjoint and their union is the whole set.

Equivalence relations and partitions describe the same structure. Every equivalence relation determines a partition into equivalence classes, and every partition determines an equivalence relation.

This idea appears when constructing quotient vector spaces.

## A.22 Finite and Infinite Sets

A set is finite if its elements can be counted by a natural number. A set with \(n\) elements has cardinality \(n\), written

$$
|A| = n.
$$

A set is infinite if it is not finite.

For example,

$$
\{1,2,3\}
$$

is finite, while

$$
\mathbb{N}
$$

is infinite.

The set \(\mathbb{R}^n\) is infinite for every positive integer \(n\). A finite-dimensional vector space can still contain infinitely many vectors. The word finite-dimensional refers to the size of a basis, not to the number of vectors in the space.

## A.23 Countability

An infinite set is countable if its elements can be listed in a sequence

$$
a_1, a_2, a_3, \ldots.
$$

The integers \(\mathbb{Z}\) and rational numbers \(\mathbb{Q}\) are countable. The real numbers \(\mathbb{R}\) are uncountable.

Most linear algebra in this book does not depend on advanced cardinality arguments. Still, the distinction between finite, countable, and uncountable sets helps clarify the difference between finite-dimensional and infinite-dimensional spaces.

## A.24 Logical Form of Common Linear Algebra Statements

Many statements in linear algebra have a simple logical form.

For example, the statement “\(S\) spans \(V\)” means

$$
\forall v \in V,\ \exists c_1,\ldots,c_n \in F
$$

such that

$$
v = c_1s_1 + \cdots + c_ns_n.
$$

The statement “\(S\) is linearly independent” means

$$
c_1s_1 + \cdots + c_ns_n = 0
\implies
c_1 = \cdots = c_n = 0.
$$

The statement “\(T\) is injective” means

$$
T(u)=T(v) \implies u=v.
$$

Equivalently, for a linear transformation,

$$
\ker(T)=\{0\}.
$$

Writing definitions in logical form helps prevent ambiguity. It also makes proofs more systematic.

## A.25 Summary

Set theory supplies the language of elements, subsets, functions, products, relations, and indexed families. Logic supplies the language of quantifiers, implication, equivalence, negation, and proof.

Linear algebra uses these tools constantly. A vector space is a set with operations. A subspace is a subset closed under those operations. A linear transformation is a function preserving those operations. A basis is a set of vectors satisfying spanning and independence conditions.

The main purpose of this appendix is not to develop set theory for its own sake. It is to make the statements and proofs of linear algebra precise.