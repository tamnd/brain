---
title: "Appendix B. Proof Techniques"
---

# Appendix B. Proof Techniques

Mathematics depends on proof. A proof is a logical argument that establishes the truth of a statement from definitions, assumptions, and previously proved results.

Linear algebra contains computational procedures, but it is also a theoretical subject. Many important statements must be proved rather than merely observed from examples. A computation may suggest a pattern, but a proof explains why the pattern always holds.

This appendix presents the proof methods used throughout the book.

## B.1 Statements and Definitions

A mathematical statement is a sentence that is either true or false.

For example,

$$
2+3=5
$$

is a true statement, while

$$
2+3=6
$$

is false.

Definitions introduce precise meanings for mathematical terms. A definition does not require proof. Instead, it establishes terminology.

For example:

> A square matrix \(A\) is invertible if there exists a matrix \(B\) such that
>
> \[
> AB = BA = I.
> \]

Once this definition is accepted, one may prove theorems about invertible matrices.

A theorem is a statement proved from definitions and previously known results.

A lemma is a theorem mainly used to prove another theorem.

A corollary is a result that follows quickly from a theorem.

## B.2 Structure of a Proof

A proof should proceed in a clear sequence of steps.

A typical proof contains:

| Part | Purpose |
|---|---|
| Assumptions | State what is given |
| Goal | State what must be shown |
| Argument | Use definitions and known facts |
| Conclusion | State that the goal has been proved |

For example:

> Let \(u,v,w\) be vectors in a vector space \(V\). Prove that
>
> \[
> u+(v+w) = (u+v)+w.
> \]

Proof:

Vector addition in a vector space satisfies the associative law by definition. Therefore,

$$
u+(v+w) = (u+v)+w.
$$

Hence the statement holds.

This proof is short because associativity is already part of the definition of a vector space.

## B.3 Direct Proof

A direct proof begins with assumptions and proceeds logically to the desired conclusion.

### Example

Prove that the sum of two odd integers is even.

Proof:

Let \(a\) and \(b\) be odd integers. Then there exist integers \(m\) and \(n\) such that

$$
a = 2m+1,
\qquad
b = 2n+1.
$$

Therefore,

$$
a+b =
(2m+1)+(2n+1) =
2(m+n+1).
$$

Since \(m+n+1\) is an integer, \(a+b\) is even.

Thus the sum of two odd integers is even.

The proof succeeds because it begins with the definition of odd integers and manipulates the resulting expressions.

## B.4 Proof by Contrapositive

An implication

$$
P \implies Q
$$

is logically equivalent to its contrapositive

$$
\neg Q \implies \neg P.
$$

Sometimes the contrapositive is easier to prove than the original statement.

### Example

Prove:

> If a real number \(x\) satisfies \(x^2 \neq 0\), then \(x \neq 0\).

Instead of proving this directly, prove the contrapositive.

Contrapositive:

> If \(x=0\), then \(x^2=0\).

Proof:

If \(x=0\), then

$$
x^2 = 0^2 = 0.
$$

Therefore the contrapositive holds, so the original statement holds.

In linear algebra, contraposition often appears in proofs about injectivity, independence, and invertibility.

## B.5 Proof by Contradiction

Proof by contradiction assumes the statement is false and derives an impossibility.

The contradiction shows that the assumption of falsity cannot hold.

### Example

Prove:

> There is no rational number whose square equals \(2\).

Proof:

Assume, for contradiction, that

$$
\sqrt{2} = \frac{p}{q}
$$

for integers \(p\) and \(q\) with no common factor.

Squaring gives

$$
2 = \frac{p^2}{q^2},
$$

so

$$
p^2 = 2q^2.
$$

Thus \(p^2\) is even, which implies \(p\) is even. Write

$$
p = 2k.
$$

Then

$$
4k^2 = 2q^2,
$$

so

$$
q^2 = 2k^2.
$$

Thus \(q^2\) is even, so \(q\) is even.

Hence both \(p\) and \(q\) are even, contradicting the assumption that they have no common factor.

Therefore \(\sqrt{2}\) is irrational.

Contradiction proofs are common in dimension arguments and existence theorems.

## B.6 Proof by Cases

A proof by cases divides a problem into separate possibilities and proves the statement in each case.

### Example

Prove that for every integer \(n\),

$$
n(n+1)
$$

is even.

Proof:

Every integer is either even or odd.

Case 1: \(n\) is even.

Then

$$
n = 2k
$$

for some integer \(k\). Therefore,

$$
n(n+1) =
2k(n+1),
$$

which is even.

Case 2: \(n\) is odd.

Then

$$
n = 2k+1
$$

for some integer \(k\). Therefore,

$$
n+1 = 2k+2 = 2(k+1),
$$

which is even. Hence,

$$
n(n+1)
$$

is even.

Since both cases give the same conclusion, the statement holds for all integers \(n\).

## B.7 Existence Proofs

An existence proof shows that at least one object satisfies a given property.

There are two common forms.

| Type | Method |
|---|---|
| Constructive | Explicitly build the object |
| Nonconstructive | Prove existence indirectly |

### Constructive Example

Prove that there exists a real number whose square is \(9\).

Proof:

The number \(3\) satisfies

$$
3^2 = 9.
$$

Therefore such a number exists.

### Nonconstructive Example

Suppose a theorem proves that every polynomial of odd degree has a real root. Such a proof may establish existence without giving an explicit formula for the root.

Linear algebra often uses constructive existence proofs. For example, Gaussian elimination explicitly constructs solutions to systems of equations.

## B.8 Uniqueness Proofs

A uniqueness proof shows that only one object satisfies a property.

The usual method is:

1. Assume two objects satisfy the property.
2. Show they must be equal.

### Example

Prove that the zero vector in a vector space is unique.

Proof:

Suppose \(0\) and \(0'\) are both zero vectors.

Since \(0\) is a zero vector,

$$
0 + 0' = 0'.
$$

Since \(0'\) is a zero vector,

$$
0 + 0' = 0.
$$

Therefore,

$$
0 = 0'.
$$

Hence the zero vector is unique.

Uniqueness arguments appear frequently in decompositions, coordinate systems, and bases.

## B.9 Proof by Induction

Mathematical induction proves statements indexed by the natural numbers.

To prove a statement \(P(n)\) for all integers \(n \geq 1\), one proves:

1. Base case: \(P(1)\).
2. Inductive step: \(P(k) \implies P(k+1)\).

### Example

Prove:

$$
1+2+\cdots+n =
\frac{n(n+1)}{2}.
$$

Base case:

For \(n=1\),

$$
1 = \frac{1(2)}{2}.
$$

Thus the statement holds for \(n=1\).

Inductive step:

Assume

$$
1+2+\cdots+k =
\frac{k(k+1)}{2}.
$$

Then

$$
1+2+\cdots+k+(k+1) =
\frac{k(k+1)}{2} + (k+1).
$$

Factor:

$$= \frac{k(k+1)+2(k+1)}{2} = \frac{(k+1)(k+2)}{2}.$$

Thus the formula holds for \(k+1\).

Therefore, by induction, the formula holds for all \(n \geq 1\).

Induction is important in linear algebra for proofs involving matrix powers, recursive algorithms, and determinant formulas.

## B.10 Counterexamples

A universal statement

$$
\forall x,\ P(x)
$$

is disproved by finding a single counterexample.

### Example

Consider the statement:

> Every square matrix is invertible.

This is false.

Counterexample:

$$
A =
\begin{bmatrix}
1 & 2 \\
2 & 4
\end{bmatrix}.
$$

The second row is a multiple of the first row, so

$$
\det(A)=0.
$$

Therefore \(A\) is not invertible.

One counterexample is enough to disprove a universal claim.

## B.11 Necessary and Sufficient Conditions

Suppose \(P\) and \(Q\) are statements.

If

$$
P \implies Q,
$$

then \(Q\) is necessary for \(P\), and \(P\) is sufficient for \(Q\).

For example:

> If a matrix is invertible, then its determinant is nonzero.

Thus:

| Statement | Role |
|---|---|
| Invertible | Sufficient |
| Nonzero determinant | Necessary |

If both implications hold,

$$
P \iff Q,
$$

then each condition is both necessary and sufficient for the other.

Many major theorems in linear algebra consist of equivalent conditions.

For example, for an \(n \times n\) matrix \(A\), the following are equivalent:

| Condition |
|---|
| \(A\) is invertible |
| \(\det(A)\neq0\) |
| The columns of \(A\) are linearly independent |
| The equation \(Ax=b\) has a unique solution for every \(b\) |

Such equivalence theorems are central to the subject.

## B.12 Forward and Backward Reasoning

In problem solving, one may reason forward from assumptions or backward from the desired conclusion.

### Forward reasoning

Start from what is known and derive consequences.

### Backward reasoning

Ask what conditions would guarantee the desired conclusion.

### Example

Suppose we want to prove

$$
A^2 = I
$$

for a matrix \(A\).

Backward reasoning suggests checking whether multiplying \(A\) by itself simplifies naturally. One may then inspect the structure of \(A\) or compute directly.

In practice, good proofs often combine both directions.

## B.13 Equality Proofs

To prove two sets are equal, prove mutual inclusion:

$$
A=B
$$

means:

$$
A \subseteq B
\quad \text{and} \quad
B \subseteq A.
$$

### Example

Prove:

$$
A \cap (B \cup C) =
(A \cap B)\cup(A \cap C).
$$

Proof:

First show

$$
A \cap (B \cup C)
\subseteq
(A \cap B)\cup(A \cap C).
$$

Let

$$
x \in A \cap (B \cup C).
$$

Then

$$
x \in A
$$

and

$$
x \in B \cup C.
$$

Thus \(x\in B\) or \(x\in C\).

If \(x\in B\), then

$$
x \in A\cap B.
$$

If \(x\in C\), then

$$
x \in A\cap C.
$$

Hence

$$
x \in (A\cap B)\cup(A\cap C).
$$

Now prove the reverse inclusion similarly.

Therefore the sets are equal.

Set equality arguments appear frequently in subspace proofs.

## B.14 Proofs in Linear Algebra

Linear algebra proofs usually involve:

| Object | Typical method |
|---|---|
| Vector spaces | Verify axioms |
| Subspaces | Check closure properties |
| Linear independence | Analyze linear combinations |
| Spanning sets | Construct representations |
| Linear maps | Verify linearity |
| Bases | Combine spanning and independence |
| Matrix identities | Use algebraic manipulation |
| Eigenvalues | Analyze characteristic equations |

### Example: Subspace Proof

Prove that the set

$$
W = \left\{
\begin{bmatrix}
x \\
y \\
0
\end{bmatrix}
: x,y \in \mathbb{R}
\right\}
$$

is a subspace of \(\mathbb{R}^3\).

Proof:

The zero vector belongs to \(W\):

$$
\begin{bmatrix}
0 \\
0 \\
0
\end{bmatrix}
\in W.
$$

Let

$$
u=
\begin{bmatrix}
x_1 \\
y_1 \\
0
\end{bmatrix},
\qquad
v=
\begin{bmatrix}
x_2 \\
y_2 \\
0
\end{bmatrix}
\in W.
$$

Then

$$
u+v =
\begin{bmatrix}
x_1+x_2 \\
y_1+y_2 \\
0
\end{bmatrix}
\in W.
$$

Now let \(c \in \mathbb{R}\). Then

$$
cu =
\begin{bmatrix}
cx_1 \\
cy_1 \\
0
\end{bmatrix}
\in W.
$$

Therefore \(W\) is closed under addition and scalar multiplication. Hence \(W\) is a subspace.

## B.15 Common Errors in Proofs

Several mistakes occur frequently.

### Assuming what must be proved

A proof cannot begin by assuming the conclusion.

### Checking only examples

Examples may illustrate a statement, but they do not prove universal truth.

### Using undefined notation

Every symbol should have a clear meaning.

### Ignoring quantifiers

Statements involving “for all” and “there exists” require careful interpretation.

### Confusing implication and equivalence

Proving

$$
P \implies Q
$$

does not prove

$$
Q \implies P.
$$

## B.16 Reading Proofs

Reading proofs is a skill that develops gradually.

A good strategy is:

1. Identify the assumptions.
2. Identify the conclusion.
3. Locate the main idea.
4. Check each logical step.
5. Determine which definitions are used.

In linear algebra, many proofs become easier once the relevant definitions are written explicitly.

For example, when proving linear independence, begin with the definition:

$$
c_1v_1 + \cdots + c_nv_n = 0.
$$

When proving injectivity of a linear map, begin with

$$
T(u)=T(v).
$$

The definition often determines the entire structure of the proof.

## B.17 Writing Proofs

Good proofs are precise, organized, and economical.

Useful guidelines include:

| Guideline | Purpose |
|---|---|
| State assumptions clearly | Establish context |
| Use complete sentences | Improve readability |
| Introduce notation carefully | Prevent ambiguity |
| Explain key transitions | Clarify logic |
| Avoid unnecessary detail | Maintain focus |
| End with the conclusion | Signal completion |

A proof is both a logical argument and a mathematical explanation. It should convince the reader that the statement is true and explain why it is true.

## B.18 Summary

Proof techniques are tools for establishing mathematical truth.

| Method | Main idea |
|---|---|
| Direct proof | Deduce conclusion from assumptions |
| Contrapositive | Prove equivalent reverse implication |
| Contradiction | Derive impossibility |
| Cases | Separate possibilities |
| Induction | Extend from one integer to the next |
| Existence proof | Show an object exists |
| Uniqueness proof | Show only one object exists |
| Counterexample | Disprove universal statement |

Linear algebra uses these methods constantly. Computational skill alone is not enough. The subject also requires logical structure, precise definitions, and rigorous argument.