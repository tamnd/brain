---
title: "CF 2013B - Battle for Survive"
description: "We are given a collection of fighters, each with a positive rating. The process repeatedly merges two alive fighters, where the fighter with the smaller index is removed and the fighter with the larger index absorbs the smaller one’s rating with subtraction."
date: "2026-06-15T04:29:11+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2013
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 973 (Div. 2)"
rating: 900
weight: 2013
solve_time_s: 53
verified: false
draft: false
---

[CF 2013B - Battle for Survive](https://codeforces.com/problemset/problem/2013/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of fighters, each with a positive rating. The process repeatedly merges two alive fighters, where the fighter with the smaller index is removed and the fighter with the larger index absorbs the smaller one’s rating with subtraction. After all operations, only one fighter remains, and its final rating depends on the sequence of eliminations.

The key freedom is that at every step we may choose any pair of remaining fighters with indices $i < j$, and decide that $i$ is eliminated while $j$ becomes $a_j - a_i$. Since indices never change, the structure of who can eliminate whom is fixed, but the order is fully controlled.

The goal is to maximize the final remaining rating.

The constraints are strong: up to $2 \cdot 10^5$ total fighters across all test cases. Any solution that tries to simulate all possible elimination sequences or even anything quadratic per test case will fail immediately. This pushes us toward an $O(n)$ or $O(n \log n)$ greedy or invariant-based argument.

A subtle difficulty is that subtraction makes the process non-monotone. Even though all initial values are positive, intermediate values can become negative, and a naive greedy choice like “always merge smallest into largest” can easily fail if applied without understanding the global structure.

A small example where intuition can mislead is:

Input:

```
3
1 100 101
```

If we always merge small into large greedily, we might do $1 \to 100$, giving $99$, then $99 \to 101$, giving $2$. But a different ordering can yield a different intermediate evolution. This shows the process is not locally obvious.

We must reason globally about how many times each value effectively gets subtracted from the final survivor.

## Approaches

A brute-force approach would simulate all possible sequences of merges. At each step we pick an ordered pair $i < j$, apply the operation, and recurse on the remaining set. The branching factor is large: roughly $O(n^2)$ choices per step, and there are $n-1$ steps, so the total number of states explodes combinatorially. Even with memoization, the state includes the entire multiset of values with structure, which is far too large.

The key observation is that the operation always preserves a single linear structure: every eliminated fighter contributes its value exactly once, with a negative sign, to exactly one survivor chain. Each fighter’s value is subtracted exactly once, but the identity of the final survivor determines whether it is subtracted from something that eventually contributes to the answer or not.

Reframing the process, every fighter except the last contributes its value negatively exactly once to some later survivor. The only thing we control is which fighter becomes the final survivor and how many times it absorbs others indirectly. The structure collapses into a greedy ordering problem: we want to maximize the final value, which turns out to depend only on the largest element and the sum of all others except one optimally chosen element.

The correct invariant is that we can always arrange the process so that all elements except the maximum are eventually subtracted into it in an order that does not change the final value beyond a simple linear expression. The optimal strategy becomes selecting one element to be the final survivor, and arranging all others to be absorbed in a way that minimizes damage.

The optimal choice turns out to be making the largest element the final survivor, while ensuring all other elements contribute in a way that effectively alternates signs through the process. This yields a final answer that simplifies to:

$$\max(a) - \sum(\text{others except one adjusted contribution})$$

which resolves to a closed form depending on parity of $n$. A more direct derivation shows the final answer is:

$$\sum a_i - 2 \cdot \min(a)$$

when $n = 2$, and more generally reduces to taking the total sum minus the smallest element.

The clean way to see it is: every merge reduces total sum by twice the eliminated element, except the last survivor never gets eliminated. Thus we want to minimize the total “lost” contribution, which is achieved by leaving the largest element un-subtracted and eliminating all others.

This yields the final insight: the answer is the sum of all elements minus twice the minimum contribution that is forced to be “wasted” by the structure, which simplifies to a direct formula depending on selecting the best survivor.

The optimal solution is therefore linear per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Greedy / Invariant Reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all fighter ratings in the array. This represents the total mass of values that will be redistributed through eliminations.
2. Identify the maximum element. This is the most natural candidate for the final survivor, because it loses the least relative value when absorbing others.
3. Identify the minimum element. This value is the most harmful if it remains too late in the process, since it can be subtracted repeatedly in unfavorable ways.
4. Return the expression $\text{sum} - 2 \cdot \text{min}$.

The reason this form appears is that in any optimal sequence, all elements except one can be arranged so that their net contribution is subtracted exactly once from the system, while the smallest element can be made to contribute twice in terms of effective loss if not handled carefully. The optimal construction ensures only the unavoidable minimum loss remains.

### Why it works

The process can be viewed as repeatedly combining two values into one adjusted accumulator. Each operation removes one element and injects its value negatively into another. Over the full process, exactly $n-1$ elements are removed, and each removal contributes its value once with a negative sign into the final survivor’s chain.

The only degree of fr
