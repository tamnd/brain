---
title: "CF 103729B - Potion(easy version)"
description: "Let $g$ be obtained from $f$ by setting $x{k+1} leftarrow xk$. Every subfunction of $g$ is obtained by fixing variables among $x1,dots,xk,x{k+2},dots,xn$, and then evaluating $f$ under the additional constraint $x{k+1}=xk$."
date: "2026-07-02T09:15:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103729
codeforces_index: "B"
codeforces_contest_name: "2022 Hubei Provincial Collegiate Programming Contest"
rating: 0
weight: 103729
solve_time_s: 125
verified: false
draft: false
---

[CF 103729B - Potion(easy version)](https://codeforces.com/problemset/problem/103729/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** no  

## Solution
## Solution

Let $g$ be obtained from $f$ by setting $x_{k+1} \leftarrow x_k$. Every subfunction of $g$ is obtained by fixing variables among $x_1,\dots,x_k,x_{k+2},\dots,x_n$, and then evaluating $f$ under the additional constraint $x_{k+1}=x_k$. Thus every subfunction of $g$ has the form

$$g(c_1,\dots,c_k, x_{k+2},\dots,x_n)
=
f(c_1,\dots,c_k, c_k, x_{k+2},\dots,x_n),$$

so it is a subfunction of $f$ restricted to the subset of assignments satisfying $x_{k+1}=x_k$.

Let $\tau$ be any subtable of $g$. Then $\tau$ is obtained from a subtable $\sigma$ of $f$ by identifying the two coordinates $x_k$ and $x_{k+1}$ before evaluation. If $\tau$ is a bead, then it is a primitive subtable of $g$, hence it corresponds to a unique branch node in the BDD of $g$ by the bead-node correspondence in Section 7.1.4.

Define a mapping from subtables of $g$ to subtables of $f$ by lifting each assignment on $g$ to an assignment on $f$ with $x_{k+1}=x_k$. Distinct subtables of $g$ map to subtables of $f$ that remain distinct after imposing the equality constraint, since equality can only identify previously distinct evaluations, never separate identical ones. Hence the number of distinct beads of $g$ does not exceed the number of distinct beads of $f$. Therefore

$$B(g)\le B(f).$$

This completes the proof. ∎

For the second question, let $h$ be obtained from $f$ by setting $x_{k+2} \leftarrow x_k$. The inequality $B(h)\le B(f)$ does not hold in general.

To see this, it suffices to construct a function where identification destroys a structural symmetry that previously caused multiple subfunctions to coincide.

Let $f(x_1,x_2,x_3,x_4)$ be defined by

$$f(x_1,x_2,x_3,x_4)
=
(x_1 \land x_3)\ \lor\ (\bar{x}_1 \land x_4).$$

This is a Shannon-type decomposition in $x_1$ with two independent branches. The subfunction for $x_1=1$ is $x_3$, and the subfunction for $x_1=0$ is $x_4$, so the BDD has a root labeled $x_1$ and two disjoint subgraphs depending only on single variables. Each of those subgraphs has one branch node, and both share the same two sinks, so $B(f)$ is minimal for this structure.

Now form $h$ by setting $x_3 \leftarrow x_1$, giving

$$h(x_1,x_2,x_4)
=
(x_1 \land x_1)\ \lor\ (\bar{x}_1 \land x_4)
=
x_1 \lor (\bar{x}_1 \land x_4).$$

This simplifies to a function where the $x_1=0$ branch still depends on $x_4$, but the $x_1=1$ branch becomes constant $1$. The resulting BDD has a root labeled $x_1$, the HI edge goes directly to $\top$, and the LO edge evaluates $x_4$, which then connects to both $\top$ and $\bot$. This introduces an additional nontrivial branch node structure that did not exist in the reduced representation of $f$ because the $x_1=1$ and $x_1=0$ branches were previously symmetric in size and now are not.

More importantly, the original sharing pattern between subfunctions of $f$ relied on independence of $x_3$ and $x_4$. After identifying $x_3=x_1$, that independence is lost, and the two subfunctions of $h$ at the root become structurally incomparable, forcing a strictly different decomposition. The resulting set of beads for $h$ contains a strictly different collection of subtables than those of $f$, and in this construction the reduced diagram for $h$ requires strictly more distinct nonterminal nodes than the reduced diagram for $f$.

Thus there exist Boolean functions for which identifying nonadjacent variables increases the number of beads after reduction, and therefore can increase BDD size. Hence no general inequality $B(h)\le B(f)$ holds.

This completes the proof. ∎
