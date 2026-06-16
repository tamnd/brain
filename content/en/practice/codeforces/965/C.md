---
title: "CF 965C - Greedy Arkady"
description: "We are given a linear stream of $n$ candies and a fixed number of people $k$. A single parameter $x$ determines how the candies are distributed: candies are processed in consecutive blocks of size $x$."
date: "2026-06-17T01:37:58+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 965
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 476 (Div. 2) [Thanks, Telegram!]"
rating: 2000
weight: 965
solve_time_s: 38
verified: false
draft: false
---

[CF 965C - Greedy Arkady](https://codeforces.com/problemset/problem/965/C)

**Rating:** 2000  
**Tags:** math  
**Solve time:** 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a linear stream of $n$ candies and a fixed number of people $k$. A single parameter $x$ determines how the candies are distributed: candies are processed in consecutive blocks of size $x$. Each block is assigned to one person in cyclic order, starting from Arkady (person 1), then person 2, and so on until person $k$, then repeating from person 1 again.

Any leftover candies fewer than $x$ at the end are discarded. Thus, only full blocks matter.

Arkady’s total gain depends entirely on how many full blocks are assigned to him, since each such block gives him exactly $x$ candies. If he receives $t$ blocks, his total is $t \cdot x$.

The choice of $x$ is constrained in two ways. First, $x \le M$, so each batch is not too large. Second, no person can receive more than $D$ batches in total. Since blocks are distributed cyclically, each person receives either $\lfloor B/k \rfloor$ or $\lceil B/k \rceil$ blocks depending on position, where $B = \lfloor n/x \rfloor$.

The goal is to choose $x$ that respects both constraints while maximizing Arkady’s total candies.

The constraints are extremely large: $n$ can reach $10^{18}$, so any solution that iterates over candies or simulates distribution is impossible. The key computational challenge is reasoning about divisors and block counts efficiently, in logarithmic or square-root style complexity.

A subtle edge case arises when small values of $x$ produce too many total blocks, causing some person to exceed $D$. For example, if $n$ is large and $x = 1$, then $B = n$, and each person receives roughly $n/k$ blocks, which can easily exceed $D$. Even though $x$ is small and seems beneficial, it is invalid.

Another edge case is when $x$ is large, close to $M$ or $n$. Then $B$ is small, possibly $0$ or $1$, and Arkady may receive very few blocks even though constraints are satisfied. The optimal solution often lies in a middle range.

Finally, boundary cases occur when $n < k\cdot x$, leading to $B < k$, where only the first few people receive blocks and Arkady may benefit disproportionately.

## Approaches

A direct approach is to try every possible $x$ from $1$ to $M$. For each $x$, compute $B = \lfloor n/x \rfloor$, simulate how many blocks each person receives, check whether any person exceeds $D$, and if valid compute Arkady’s gain. This is correct because it directly mirrors the process described in the problem.

However, this approach is far too slow. $M$ can be as large as $10^{18}$, and even computing $B$ for each $x$ leads to an infeasible $O(Mk)$ or $O(M)$ process. The bottleneck is not arithmetic but iteration over an enormous domain.

The key observation is that the number of full blocks $B = \lfloor n/x \rfloor$ changes only when $x$ crosses divisors of $n$. More importantly, for fixed $B$, all values of $x$ in an interval produce the same $B$, and therefore the same feasibility condition and Arkady score. This turns the problem into reasoning over ranges of $x$ grouped by constant quotient $n/x$.

We then invert the viewpoint: instead of choosing $x$, we choose $B$, the number of full blocks. Since $B = \lfloor n/x \rfloor$, valid $x$ lie in the interval $(n/(B+1), n/B]$. For each such $B$, we can test whether there exists an $x \le M$ in this interval that also satisfies the per-person constraint. Once $B$ is fixed, Arkady’s gain becomes maximizing $x \cdot t$, where $t$ is the number of times he appears in the cycle among $B$ blocks.

This reduces the problem to checking only $O(\sqrt{n})$ candidate ranges of $B$, because the quotient structure of $n/x$ has only that many distinct values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $x$ | $O(Mk)$ | $O(1)$ | Too slow |
| Quotient grouping over $B = \lfloor n/x \rfloor$ | $O(\sqrt{n})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that for a fixed $x$, the total number of full batches is $B = \lfloor n/x \rfloor$. This determines all distributions.
2. For each possible $B$, derive the range of $x$ that produces it. That range is $x \in [\lfloor n/(B+1) \rfloor + 1, \lfloor n/B \rfloor]$. This converts the problem from iterating over $x$ to iterating over $B$.
3. Iterate over all distinct values of $B$ by jumping using the standard quotient trick. Starting from $x = 1$, compute $B = n // x$, and jump $x$ to the end of this segment.
4. For each segment, compute whether there exists at least one $x \le M$ in the segment. If not, skip it entirely since it is infeasible.
5. For a valid segment, determine how many blocks Arkady receives. In $B$ total blocks distributed cyclically among $k$ people, Arkady gets either $\lfloor B/k \rfloor$ or $\lceil B/k \rceil$ blocks depending on remainder. Since Arkady is first, he receives $\lceil B/k \rceil$.
6. To maximize Arkady’s total candies, we want the largest feasible $x$ in the segment, since gain is proportional to $x$. Therefore choo
