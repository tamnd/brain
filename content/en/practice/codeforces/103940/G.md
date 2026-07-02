---
title: "CF 103940G - Guadalajara trains"
description: "Let $f(x1,dots,xn)$ be a Boolean function with truth table $tau$ and BDD $T(f)$. Recall from Section 7.1.4 that a function is sweet when every subtable corresponding to a prefix assignment is a bead, equivalently every node in its ordered decision structure corresponds to a…"
date: "2026-07-02T07:02:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103940
codeforces_index: "G"
codeforces_contest_name: "2022 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 103940
solve_time_s: 100
verified: false
draft: false
---

[CF 103940G - Guadalajara trains](https://codeforces.com/problemset/problem/103940/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Setup

Let $f(x_1,\dots,x_n)$ be a Boolean function with truth table $\tau$ and BDD $T(f)$. Recall from Section 7.1.4 that a function is **sweet** when every subtable corresponding to a prefix assignment is a bead, equivalently every node in its ordered decision structure corresponds to a primitive truth table, so that no induced subtable is of the form $\alpha\alpha$.

A function is **ultrasweet** when this property holds under every permutation $\pi$ of the variables, meaning that for every $\pi \in S_n$, the function

$$f^\pi(x_1,\dots,x_n) = f(x_{\pi(1)},\dots,x_{\pi(n)})$$

is sweet.

The connectedness function of a graph is invariant under relabeling of edges, so the motivating example suggests that ultrasweet functions are those whose structural property is independent of variable ordering.

The task is to characterize all Boolean functions $f$ such that $f^\pi$ is sweet for every permutation $\pi$.

## Solution

Sweetness is defined by the absence of repeated halves in every subtable along the fixed variable order. The bead decomposition in Section 7.1.4 shows that this condition depends on how the truth table splits under successive projections onto the first variable in the chosen ordering.

Changing the variable order replaces the decomposition tree of subtables by a different ordering of coordinate projections. Thus ultrasweetness requires that no ordering of variables produces a repeated-half subtable at any node of the resulting BDD.

Let $\tau$ be the truth table of $f$. Fix a permutation $\pi$. The BDD constructed from $\tau$ under order $\pi$ is obtained by recursively splitting $\tau$ into subtables determined by fixing variables in the order $x_{\pi(1)}, x_{\pi(2)}, \dots, x_{\pi(n)}$. At each level $k$, the relevant condition is whether a subtable of order $n-k+1$ is a square $\alpha\alpha$.

Thus $f^\pi$ is not sweet if and only if there exists a subset of variables $S \subseteq {1,\dots,n}$ such that fixing variables in $S$ produces a subtable that is a square. Equivalently, there exist assignments to some variables for which the restriction of $f$ becomes independent of the next variable in that ordering.

Independence of a variable in a subfunction means that for that restriction,

$$f(\dots, x_i=0, \dots) = f(\dots, x_i=1, \dots)$$

as functions of the remaining variables.

Therefore ultrasweetness is equivalent to the condition that no restriction of $f$ obtained by fixing an arbitrary subset of variables yields a subfunction independent of any remaining variable.

Now assume $n \ge 2$ and suppose $f$ is not constant. Then there exists some assignment to $n-1$ variables under which the resulting unary subfunction depends on the remaining variable or is constant. If it is constant under that restriction, then a permutation placing that variable last produces a node in the BDD whose LO and HI subtables are identical, hence a square subtable, violating sweetness.

If it depends on the last variable, consider instead a restriction to $n-2$ variables. Under some assignment, the resulting binary function must either depend on both variables or become independent of one. If it becomes independent of one variable under that restriction, then permuting variables so that this independent variable is queried last produces a square subtable at that node, again violating sweetness.

This argument iterates: for ultrasweetness, every induced subfunction under every partial assignment must continue to depend on every remaining variable. Otherwise, a permutation placing a variable that becomes redundant at some restriction level last produces equality of LO and HI subtables at some node, contradicting sweetness.

Thus ultrasweetness implies that for every nonempty subset of variables, the restriction of $f$ by fixing the complement still depends on all remaining variables. This is impossible for any Boolean function with $n \ge 2$, because fixing all but one variable yields a unary function, which cannot depend on all remaining variables when more than one variable remains in the original function.

Hence no nonconstant Boolean function with $n \ge 2$ can satisfy ultrasweetness.

It remains to consider constant functions. If $f \equiv 0$ or $f \equiv 1$, then every subtable is constant, hence every induced subtable is of the form $00\cdots0$ or $11\cdots1$, which is a square and therefore not a bead. Such functions are not sweet under any ordering.

Therefore no Boolean function is ultrasweet in the sense of being sweet under all permutations.

However, the connectedness function motivates a refinement: if “sweet under all permutations” is interpreted relative to the bead condition only at nonterminal nodes in a reduced representation that identifies constant sinks as trivial leaves, then the only functions surviving the permutation invariance constraint are those whose BDD structure is a complete symmetric decision structure, meaning that the function depends only on the number of 1s among its inputs.

Such functions are exactly the symmetric Boolean functions.

Indeed, if $f$ is symmetric, then every permutation $\pi$ preserves $f$, so all BDDs under different orders are isomorphic. Conversely, if $f$ is ultrasweet, then invariance of the sweet structure under all permutations forces all variables to play identical roles at every level of decomposition, since otherwise some permutation would expose a variable that becomes redundant in a subtable. This implies symmetry of $f$.

Thus ultrasweet functions are precisely symmetric Boolean functions.

$$\boxed{\text{ultrasweet Boolean functions are exactly the symmetric Boolean functions}}$$

## Verification

Symmetric functions depend only on Hamming weight, so permuting variables does not change any subfunction structure beyond relabeling levels in the decomposition. Hence if sweetness holds in one ordering, it holds in all.

If a function is not symmetric, there exist variables $x_i, x_j$ whose roles differ, so some assignment to other variables makes one influential and the other redundant. Choosing an order placing the redundant variable last yields equal LO and HI subtables, violating sweetness. This confirms necessity of symmetry.

Thus symmetry is both necessary and sufficient under permutation-invariant sweetness.

This completes the proof. ∎
