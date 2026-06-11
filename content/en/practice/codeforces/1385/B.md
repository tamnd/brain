---
title: "CF 1385B - Restore the Permutation by Merger"
description: "We are given an array of length $2n$. This array was created by taking a permutation $p$ of the numbers $1$ through $n$, making a second copy of the same permutation, and interleaving the two copies while preserving the relative order inside each copy."
date: "2026-06-11T10:42:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1385
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 656 (Div. 3)"
rating: 800
weight: 1385
solve_time_s: 175
verified: false
draft: false
---

[CF 1385B - Restore the Permutation by Merger](https://codeforces.com/problemset/problem/1385/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length $2n$. This array was created by taking a permutation $p$ of the numbers $1$ through $n$, making a second copy of the same permutation, and interleaving the two copies while preserving the relative order inside each copy.

Every value from $1$ to $n$ appears exactly twice in the final array. Our task is to reconstruct the original permutation.

The crucial detail is that the answer is guaranteed to exist and is guaranteed to be unique.

The constraints are very small. Each test case has $n \le 50$, so the input array contains at most 100 numbers. Even an $O(n^2)$ solution would run comfortably within the limit. The challenge is not performance, it is recognizing the structure created by merging two identical permutations.

A common mistake is to try to reconstruct the merge process itself. That is unnecessary and can easily become complicated. The guarantee that both copies are the same permutation gives a much simpler observation.

Consider the input

```
1 3 1 4 3 4 2 2
```

The correct answer is

```
1 3 4 2
```

A careless approach might try to pair occurrences together and infer where each copy came from. None of that information is needed. The first time each number appears already reveals the permutation.

Another edge case occurs when the two copies are completely separated:

```
1 2 3 1 2 3
```

The answer is still

```
1 2 3
```

A solution that expects the two occurrences of each value to be adjacent would fail.

## Approaches

A brute-force idea is to try all possible permutations of length $n$, simulate all valid merges of two copies, and check which one produces the given array. This is correct because it directly follows the definition of the problem. Unfortunately, there are $n!$ permutations, which becomes enormous even for modest values of $n$.

The structure of the merge makes a much simpler solution possible.

Take any value $x$ in the original permutation. Since both copies preserve their internal order, the first occurrence of $x$ in the merged array must appear exactly when $x$ first becomes available from either copy. Before that point, $x$ has never appeared.

Because the original permutation contains every number exactly once, the sequence of first appearances in the merged array is exactly the original permutation itself.

For example:

```
2 3 2 4 1 3 4 1
```

Reading from left to right, the first appearances are:

```
2, 3, 4, 1
```

which is the answer.

The problem reduces to collecting numbers in the order
