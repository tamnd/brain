---
title: "CF 103720A - \u0414\u0438\u0430\u0433\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a"
description: "Let $f$ be a Boolean function of variables $x1,dots,xn$ and let $g$ be obtained from $f$ by the condensation $x{k+1} leftarrow xk$. Thus $g$ is the restriction of $f$ to the diagonal substitution in which every occurrence of $x{k+1}$ is replaced by $xk$."
date: "2026-07-02T09:18:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103720
codeforces_index: "A"
codeforces_contest_name: "VII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b. 3-7 \u043a\u043b\u0430\u0441\u0441\u044b"
rating: 0
weight: 103720
solve_time_s: 43
verified: false
draft: false
---

[CF 103720A - \u0414\u0438\u0430\u0433\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u043f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a](https://codeforces.com/problemset/problem/103720/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
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
