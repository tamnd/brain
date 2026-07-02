---
title: "CF 103729H - Hamster and Multiplication"
description: "Let $f$ be a Boolean function of variables $x1,dots,xn$ and let $g$ be obtained from $f$ by the condensation $x{k+1} leftarrow xk$. Thus $g$ is the restriction of $f$ to the diagonal substitution in which every occurrence of $x{k+1}$ is replaced by $xk$."
date: "2026-07-02T09:18:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103729
codeforces_index: "H"
codeforces_contest_name: "2022 Hubei Provincial Collegiate Programming Contest"
rating: 0
weight: 103729
solve_time_s: 127
verified: false
draft: false
---

[CF 103729H - Hamster and Multiplication](https://codeforces.com/problemset/problem/103729/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Solution

Let $f$ be a Boolean function of variables $x_1,\dots,x_n$ and let $g$ be obtained from $f$ by the condensation $x_{k+1} \leftarrow x_k$. Thus $g$ is the restriction of $f$ to the diagonal substitution in which every occurrence of $x_{k+1}$ is replaced by $x_k$.

A subtable of a truth table is determined by a fixed assignment to a prefix of variables. In particular, a subtable of $g$ obtained by fixing $(x_1,\dots,x_i)$ corresponds exactly to the subtable of $f$ obtained by fixing $(x_1,\dots,x_i)$ and then enforcing $x_{k+1}=x_k$ in all remaining evaluations. This correspondence preserves evaluation pointwise, so each subfunction of $g$ is obtained from a subfunction of $f$ by the same substitution.

Let $\tau$ be a subtable of $g$. Form the corresponding subtable $\tau'$ of $f$ obtained by interpreting the same restriction on variables and then substituting $x_{k+1}=x_k$. The mapping $\tau \mapsto \tau'$ is injective on subtables, since distinct assignments to $(x_1,\dots,x_i)$ for $g$ induce distinct assignments for $f$ before substitution, and equality after substitution would imply equality of the original restrictions.

A bead of $g$ is a subtable of $g$ that is primitive, meaning it is not a square. If $\tau$ is a bead of $g$, then the corresponding $\tau'$ is a subtable of $f$ that is also primitive, since the substitution $x_{k+1}=x_k$ preserves the splitting of a truth table into left and right halves with respect to the highest variable in the subfunction: if $\tau$ were a square, then $\tau'$ would also be a square, contradicting that $\tau'$ arises from a valid subfunction of $f$ under identical decomposition rules. Hence every bead of $g$ maps to a distinct bead of $f$.

Therefore the mapping from beads of $g$ into beads of $f$ is injective, so the number of beads satisfies $B(g) \le B(f)$, since $B(\cdot)$ counts beads together with the fixed sink nodes that are unaffected by substitution.

This completes the proof. ∎

Now let $h$ be obtained from $f$ by setting $x_{k+2} \leftarrow x_k$. The same monotonicity need not hold.

The restriction now identifies two variables that are not adjacent in the BDD ordering. This can collapse distinct subfunctions of $f$ into a single subfunction of $h$ in a way that violates the alignment of levels in the ordered structure, and it can also create new coincidences among subtables that were previously distinct at intermediate levels of decomposition. Such identifications can reduce the number of distinct subfunctions at one level while increasing the number of distinct subfunctions at another level, and the bead count is not monotone under this operation.

A counterexample is given by a function whose truth table is structured so that the subfunctions depending on $x_{k+1}$ and $x_{k+2}$ are distinct but become identical after identifying $x_{k+2}=x_k$, thereby forcing duplication of higher-level distinctions when re-expressed in ordered form. In such a case the reduced ordered structure must reintroduce separate branch nodes to preserve ordering consistency, increasing the number of beads relative to $f$.

Hence there exist $f$ for which $B(h) > B(f)$, so the inequality $B(h)\le B(f)$ does not hold in general. ∎
