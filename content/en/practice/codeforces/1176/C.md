---
title: "CF 1176C - Lose it!"
description: "We are given a sequence whose elements are restricted to the six numbers 4, 8, 15, 16, 23, 42. We may delete some elements, and after the deletions the remaining elements must be splittable into several subsequences, each equal to 4 → 8 → 15 → 16 → 23 → 42 with the order inside…"
date: "2026-06-12T01:44:24+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1176
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 565 (Div. 3)"
rating: 1300
weight: 1176
solve_time_s: 51
verified: false
draft: false
---

[CF 1176C - Lose it!](https://codeforces.com/problemset/problem/1176/C)

**Rating:** 1300  
**Tags:** dp, greedy, implementation  
**Solve time:** 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence whose elements are restricted to the six numbers `4, 8, 15, 16, 23, 42`. We may delete some elements, and after the deletions the remaining elements must be splittable into several subsequences, each equal to

`4 → 8 → 15 → 16 → 23 → 42`

with the order inside each subsequence preserved.

The task is to remove as few elements as possible. Equivalently, we want to keep as many elements as possible while arranging them into complete chains of length six.

The array length can reach `5 × 10^5`, which immediately rules out any algorithm that tries many combinations or repeatedly scans large portions of the array. Quadratic algorithms would require roughly `2.5 × 10^11` operations, which is far beyond what fits into two seconds. Linear or near-linear solutions are required.

Several situations are easy to mishandle.

Consider

```
6
4 8 15 16 42 23
```

The correct answer is

```
2
```

because the order inside a chain must be exactly `4,8,15,16,23,42`. Even though all six values are present, `42` appears before `23`, so both numbers must be discarded.

Another tricky case is

```
7
4 8 15 16 23 42 4
```

The answer is

```
1
```

The first six elements form one complete chain, while the final `4` cannot be completed. A solution that only checks whether each number appears the same number of times would incorrectly keep all seven elements.

A third example is

```
8
8 15 16 23 42 4 8 15
```

The answer is

```
8
```

The first five elements cannot start a chain because no preceding `4` exists. The last three elements are also incomplete. Every element must be removed. A careless implementation that starts chains from any value would produce a wrong answer.

## Approaches

A brute-force viewpoint is to decide which elements belong to which chain. For every occurrence we could try assigning it to one of many partial sequences and search over all possibilities. Such a method is correct because every valid answer corresponds to some assignment, but the number of possibilities grows exponentially. With `n = 500000`, this approach is completely infeasible.

The structure of the required sequence provides a much simpler idea. Every number has exactly one predecessor:

| Value | Must come after |
| --- | --- |
| 4 | start |
| 8 | 4 |
| 15 | 8 |
| 16 | 15 |
| 23 | 16 |
| 42 | 23 |

While scanning the array from left to right, we only need to know how many unfinished chains currently end at each stage.

Suppose we encounter a `15`. It can only be useful if there is an unfinished chain ending at `8`. In that case we extend one such chain and move it to the next stage. Otherwise this `15` can never participate in any valid sequence and must eventually be deleted.

The brute-force works because it explores all possible ways to build chains, but fails because the number of assignments explodes. The observation that each value has exactly one allowed predecessor reduces the problem to maintaining counts of partial chains, giving a linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create the required order

```
4 → 8 → 15 → 16 → 23 → 42
```

and map each value to its position in this order.
2. Maintain an array `cnt[0...5]`, where `cnt[i]` represents how many unfinished chains currently end at stage `i`.

For example, `cnt[2]` counts chains that have reached `15`.
3. Scan the input from left to right.
4. When the current number is `4`, start a new chain by increasing `cnt[0]`.

Every valid sequence begins with `4`, so every `4` may potentially become useful.
5. For any other number, find its previous stage.

If there exists an unfinished chain at that previous stage, decrease the previous counter and increase the current counter.

This extends one existing chain.
6. If no such chain exists, ignore the number.

Such an element can never belong to a valid sequence because its required predecessor does not exist before it.
7. After processing the whole array, `cnt[5]` equals the number of complete chains.
8. Each complete chain contributes six kept elements, so the number of kept elements is

```
6 × cnt[5]
```
9. The answer is

```
n − 6 × cnt[5]
```

### Why it works

At every moment, `cnt[i]` stores the number of chains whose last accepted value is the `i`-th number of the required sequence. Whenever a new value arrives, the only legal action is to attach it to a chain ending at the immediately preceding stage. If no such chain exists, the value cannot be part of any valid subsequence because all later elements appear after it and cannot serve as predecessors.

Thus every accepted element belongs to some chain that respects the required order, and every complete chain contributes exactly six elements. No valid element is wasted, so the numb
