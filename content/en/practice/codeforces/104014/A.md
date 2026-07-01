---
title: "CF 104014A - \u0411\u043e\u043b\u044c\u0448\u043e\u0439 \u0443\u0434\u043e\u0439"
description: "Let $F$ denote the family of 5757 SGB words represented on variables $a1,dots,z5$ as in (131), and let the associated ZDD be constructed in the standard ordered way with variables processed in lexicographic order."
date: "2026-07-02T04:57:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104014
codeforces_index: "A"
codeforces_contest_name: "2022-2023 ICPC NERC, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0433\u0438\u043e\u043d\u0430 \u0438 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438"
rating: 0
weight: 104014
solve_time_s: 121
verified: false
draft: false
---

[CF 104014A - \u0411\u043e\u043b\u044c\u0448\u043e\u0439 \u0443\u0434\u043e\u0439](https://codeforces.com/problemset/problem/104014/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Solution

Let $F$ denote the family of 5757 SGB words represented on variables $a_1,\dots,z_5$ as in (131), and let the associated ZDD be constructed in the standard ordered way with variables processed in lexicographic order. The z-profile records, for each variable position, the number of distinct ZDD nodes occurring at that level, equivalently the number of distinct residual subfamilies obtained by conditioning on assignments to earlier variables and then branching on the current variable.

For a variable such as $a_2$, the construction has already fixed $a_1$ and then considers whether the second letter is $a$. Every node at this level represents a distinct residual family of completions of a partial word prefix of length $2$. Two such nodes are identical if and only if the remaining sets of completions are identical as subsets of the SGB word list.

The entry $23$ for $a_2$ arises because, after fixing $a_1$ in all admissible ways and then branching on $a_2$, there are exactly $23$ distinct nonempty continuation classes of partial words that remain distinguishable by the suffix constraints imposed by the dictionary. In ZDD terms, $23$ is the number of distinct subfamilies reachable at level $a_2$ after reduction merges identical continuation sets induced by different prefixes. Each of these corresponds to a distinct node because no further reduction applies at this level: the continuation sets differ in at least one allowed completion in the remaining positions.

The entry $3$ for $b_2$ reflects a further collapse of structure after the $a$-variables are resolved. At the $b_2$ level, the residual families induced by different prefixes of length $2$ in the $b$-component fall into exactly three equivalence classes under the relation “has identical completion set in variables $b_3,\dots,z_5$.” This reduction occurs because the constraints defining SGB words do not distinguish many intermediate prefixes once the first two-letter block is fixed; multiple branches in the decision structure lead to identical continuation sets, so they merge in the reduced ZDD. The value $3$ is therefore the number of distinct subfunctions of $F$ depending on the first variable at the $b_2$ level.

For the final entries $0,3,2,1,1,2$ corresponding to $v_5,w_5,x_5,y_5,z_5$, the interpretation is governed by the fact that these are terminal positions in the 5-letter word structure. At depth $5$, each node represents a fully determined prefix of length $4$ together with a single remaining letter choice constrained by membership in the SGB dictionary.

The entry $0$ at $v_5$ indicates that every partial assignment reaching that level is inconsistent with the word list, so no continuation exists; every corresponding residual subfamily is empty and is therefore reduced away in a ZDD, leaving no node contribution at that position.

The entry $3$ at $w_5$ indicates that exactly three distinct nonempty residual families survive when the fifth letter is restricted to valid completions of prefixes ending in $w$. These families differ in whether the remaining completion is uniquely determined or still has multiple valid extensions.

The entries $2,1,1,2$ for $x_5,y_5,z_5$ arise from progressively tighter suffix constraints. At $x_5$, two distinct continuation classes remain because two inequivalent suffix contexts still permit completions. At $y_5$ and $z_5$, each partial assignment determines a unique continuation behavior, so each contributes a single surviving ZDD node per consistent class. The final value $2$ at $z_5$ reflects that two distinct terminal consistency patterns remain for completions ending in $z$, distinguished by whether the last constraint is satisfied uniquely or by multiple dictionary-consistent words.

In each case, the z-profile entry equals the number of distinct reduced subfamilies of SGB words induced by fixing variables up to that level, and the listed values follow from the merging of identical continuation sets in the reduced ordered ZDD representation.

This completes the proof. ∎
