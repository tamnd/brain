---
title: "CF 1716B - Permutation Chain"
description: "We start from the identity permutation [1, 2, ..., n]. At every step we are allowed to swap any two positions, producing a new permutation. The number of fixed points, meaning positions whose value is equal to the position index, must strictly decrease after every swap."
date: "2026-06-09T19:49:49+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1716
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 133 (Rated for Div. 2)"
rating: 800
weight: 1716
solve_time_s: 39
verified: false
draft: false
---

[CF 1716B - Permutation Chain](https://codeforces.com/problemset/problem/1716/B)

**Rating:** 800  
**Tags:** constructive algorithms, math  
**Solve time:** 39s  
**Verified:** no  

## Solution
## Problem Understanding

We start from the identity permutation `[1, 2, ..., n]`. At every step we are allowed to swap any two positions, producing a new permutation. The number of fixed points, meaning positions whose value is equal to the position index, must strictly decrease after every swap.

The task is not merely to produce a valid chain. We must make the chain as long as possible. For each test case we have to output the number of permutations in the chain and then print every permutation in order.

The constraints are tiny. There are at most 99 test cases and `n ≤ 100`, so even an `O(n²)` construction per test case is easily fast enough. Memory is also negligible because each permutation contains only 100 elements.

A subtle point is that one swap may destroy several fixed points at once. Starting from the identity permutation with `n` fixed points, we want to decrease the number of fixed points as slowly as possible, since each decrease gives us another permutation in the chain.

Consider `n = 2`.

```
1 2
```

The only possible swap gives

```
2 1
```

The number of fixed points changes from 2 to 0, so the chain length is 2. A careless approach might expect one step per fixed point and incorrectly output three permutations.

Another interesting case is `n = 3`.

```
1 2 3
```

Swapping positions 1 and 2 produces

```
2 1 3
```

whose fixedness is 1. Any further swap involving positions 1 and 2 returns one of them to its original place and increases the fixedness. The lon
