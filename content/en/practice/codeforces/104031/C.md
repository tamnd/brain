---
title: "CF 104031C - \u0420\u043e\u043b\u043b\u0435\u0440"
description: "Let $A={i1,i2,ldots,iell}$ and let $F = e{i1}cupcdotscup e{iell}$. The ZDD for $F$ consists of a single decision chain ordered by indices, because each $e{it}$ contributes a node that tests membership of $it$ and reduces to $perp$ or $top$ as in the conventions of Exercise 7.1.4."
date: "2026-07-02T04:02:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104031
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2021-2022 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104031
solve_time_s: 116
verified: false
draft: false
---

[CF 104031C - \u0420\u043e\u043b\u043b\u0435\u0440](https://codeforces.com/problemset/problem/104031/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Solution

Let $A={i_1,i_2,\ldots,i_\ell}$ and let $F = e_{i_1}\cup\cdots\cup e_{i_\ell}$. The ZDD for $F$ consists of a single decision chain ordered by indices, because each $e_{i_t}$ contributes a node that tests membership of $i_t$ and reduces to $\perp$ or $\top$ as in the conventions of Exercise 7.1.4.203. The operation $F § k$ is defined as the symmetric Boolean function $S_k(x_{i_1},\ldots,x_{i_\ell})$, which evaluates to $1$ exactly when exactly $k$ of the variables in $A$ are $1$.

### Structural interpretation

Each set $\alpha \subseteq A$ corresponds to an assignment of variables $x_{i_t}$, where $i_t \in \alpha$ means $x_{i_t}=1$. The value $S_k(x_{i_1},\ldots,x_{i_\ell})$ depends only on the cardinality $|\alpha|$. Therefore $F § k$ is the characteristic function of the family

$$\{\alpha \subseteq A \mid |\alpha|=k\}.$$

This family is uniform over $A$, hence its ZDD representation depends only on the remaining number of elements to select and the remaining positions in the ordered index sequence.

### Recursive ZDD decomposition

Let $F^{(t)} = e_{i_1}\cup\cdots\cup e_{i_t}$. Fix $t>0$ and let $j=i_t$. Every subset $\alpha \subseteq {i_1,\ldots,i_t}$ splits uniquely into two disjoint classes according to whether $j \in \alpha$ or $j \notin \alpha$. This induces a disjoint decomposition of families:

$$\{\alpha \subseteq F^{(t)} \mid |\alpha|=k\}
=
\{\alpha \subseteq F^{(t-1)} \mid |\alpha|=k\}
\;\cup\;
\{\alpha \cup \{j\} \mid \alpha \subseteq F^{(t-1)},\ |\alpha|=k-1\}.$$

Translating this into ZDD operations, the second term corresponds to joining $e_j$ with all sets of size $k-1$, while the first term corresponds to excluding $j$:

$$F^{(t)} § k
=
(F^{(t-1)} § k)
\;\cup\;
(e_j \sqcup (F^{(t-1)} § (k-1))).$$

### Base conditions

When $t=0$, the family is empty, so only the empty set exists. Therefore

$$F^{(0)} § 0 = \epsilon,
\qquad
F^{(0)} § k = \perp \ \text{for } k>0.$$

### Correctness

Every $\alpha$ with $|\alpha|=k$ in $F^{(t)}$ either contains $j$ or does not contain $j$. If $j \notin \alpha$, then $\alpha \subseteq F^{(t-1)}$ and $|\alpha|=k$, so $\alpha$ is represented in $F^{(t-1)} § k$. If $j \in \alpha$, then $\alpha \setminus {j} \subseteq F^{(t-1)}$ and $|\alpha \setminus {j}|=k-1$, so $\alpha$ is generated uniquely by applying $e_j \sqcup$ to an element of $F^{(t-1)} § (k-1)$. The two cases are disjoint because $j$ cannot be both included and excluded in the same set, so the union is exact.

### Implementation as ZDD operations

The computation proceeds by dynamic construction over states $(t,k)$ in decreasing $t$ and fixed $k$. Each state produces a ZDD node defined by

$$G(t,k) = G(t-1,k)\ \cup\ (e_{i_t} \sqcup G(t-1,k-1)),$$

with boundary conditions $G(0,0)=\epsilon$ and $G(0,k)=\perp$ for $k>0$. The required output is $G(\ell,k)$.

Because ZDD reduction identifies identical subgraphs and eliminates redundant nodes, repeated occurrences of identical pairs $(t,k)$ share structure, so each distinct pair contributes at most one ZDD node in the reduced representation.

### Complexity

Each state $(t,k)$ requires one application of $\cup$ and one application of $\sqcup$, both constant-time ZDD operations under the standard apply algorithm with memoization. The number of distinct states is bounded by $\ell(k+1)$, since $t$ ranges from $0$ to $\ell$ and $k$ ranges from $0$ to the target value.

Each state is processed once, and each processing step introduces a constant number of ZDD operations. Therefore the total number of primitive ZDD operations is proportional to the number of reachable states in the recursion graph.

The recursion only generates states with $0 \le k \le t \le \ell$, so the number of reachable pairs is at most $\ell(\ell+1)/2$. Each such pair is evaluated once, and each evaluation performs a bounded number of ZDD primitive operations, so the construction runs in time proportional to the number of reachable $(t,k)$ states.

### Conclusion

The operation $(e_{i_1}\cup\cdots\cup e_{i_\ell}) § k$ is implemented by a two-branch recursion that includes or excludes the last index at each step, combining results via $\cup$ and $\sqcup$. The resulting ZDD represents exactly the family of all $k$-element subsets of ${i_1,\ldots,i_\ell}$, and is constructed by a bounded number of ZDD operations per reachable recursion state. This completes the proof. ∎
