---
title: "CF 1538G - Gift Set"
description: "We have two piles of candies. One pile contains x red candies and the other contains y blue candies. Each gift set must use exactly a + b candies. There are two possible compositions: - a red and b blue - b red and a blue The two types are symmetric."
date: "2026-06-10T14:54:09+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 2100
weight: 1538
solve_time_s: 54
verified: false
draft: false
---

[CF 1538G - Gift Set](https://codeforces.com/problemset/problem/1538/G)

**Rating:** 2100  
**Tags:** binary search, greedy, math, ternary search  
**Solve time:** 54s  
**Verified:** no  

## Solution
## Problem Understanding

We have two piles of candies. One pile contains `x` red candies and the other contains `y` blue candies.

Each gift set must use exactly `a + b` candies. There are two possible compositions:

- `a` red and `b` blue
- `b` red and `a` blue

The two types are symmetric. For every set we are free to choose either orientation. A candy can be used at most once.

The task is to compute the largest number of gift sets that can be formed.

The constraints are the main clue. All values can be as large as `10^9`, and there are up to `10^4` test cases. Any algorithm that tries to simulate gift sets one by one is impossible. Even a single test case might have an answer close to `10^9`.

A solution around `O(log 10^9)` per test case is perfectly fine because `10^4 × 30 ≈ 3 × 10^5` operations. Anything linear in the answer is ruled out.

Several edge cases are easy to miss.

Consider:

```
x = 1, y = 1, a = 2, b = 2
```

Each set needs four candies total, but only two candies exist. The answer is:

```
0
```

A naive check based only on balancing colors might incorrectly think one set is possible.

Now consider:

```
x = 1000000000
y = 1
a = 1
b = 1000000000
```

One set is possible by taking `1` red and `1000000000` blue, or vice versa. Since blue candies are scarce, only one set can be made. The correct answer is:

```
1
```

Any formula that only looks at total candy count would incorrectly predict a much larger answer.

Another subtle case occurs when `a = b`.

```
x = 10
y = 12
a = b = 3
```

Every set consumes exactly three red and three blue candies. There is no freedom in orientation anymore. The answer becomes:

```
min(10 // 3, 12 // 3) = 3
```

A general solution must still handle this degenerate situation correctly.

## Approaches

A brute-force strategy would be to guess how many sets use the first orientation and how many use the second orientation.

Suppose we want to create `k` total sets. Let `t` of them be `(a red, b blue)` and `k - t` be `(b red, a blue)`.

The total red consumption becomes:

```
t·a + (k - t)·b
```

and the total blue consumption becomes:

```
t·b + (k - t)·a
```

We could try every possible value of `t` and check feasibility. This is correct because every arrangement corresponds to some choice of `t`.

The problem is that `k` itself can be close to `10^9`. Even checking all values of `t` for a single candidate answer is far too expensive.

The key observation is that the answer is monotonic.

If it is possible to create `k` gift sets, then it is also possible to create any smaller number of gift sets. We can simply discard some sets.

Monotonicity immediately suggests binary search on the answer.

Now the problem becomes:

> Given a candidate value `k`, can we determine whether `k` gift sets are possible?

Let `t` again denote the number of sets of the first orientation.

The resource constraints are:

```
t·a + (k - t)·b ≤ x
t·b + (k - t)·a ≤ y
```

After rearranging:

```
t(a - b) ≤ x - kb
t(a - b) ≥ ka - y
```

These inequalities describe an interval of valid values for `t`.

Instead of searching for `t`, we only need to know whether this interval contains an integer.

That turns feasibility checking into a constant-time arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) per feasibility check | O(1) | Too slow |
| Optimal | O(log(min(x,y))) | O(1) | Accepted |

## Algorithm Walkthrough

1. If `a < b`, swap them. This guarantees `a - b ≥ 0`, which simplifies the inequalities.
2. Binary search the answer `k`.
3. For a fixed `k`, determine wheth
