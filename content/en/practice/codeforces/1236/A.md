---
title: "CF 1236A - Stones"
description: "We are given three piles of stones with sizes $a$, $b$, and $c$. Alice starts with zero collected stones and repeatedly performs operations that move stones from these piles into her collection. There are two possible moves."
date: "2026-06-13T19:20:21+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1236
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 593 (Div. 2)"
rating: 800
weight: 1236
solve_time_s: 535
verified: false
draft: false
---

[CF 1236A - Stones](https://codeforces.com/problemset/problem/1236/A)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 8m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given three piles of stones with sizes $a$, $b$, and $c$. Alice starts with zero collected stones and repeatedly performs operations that move stones from these piles into her collection.

There are two possible moves. The first move consumes one stone from pile one and two stones from pile two, and in exchange Alice gains all three removed stones. The second move consumes one stone from pile two and two stones from pile three, again yielding three stones total. The process stops when no operation can be performed.

The goal is to maximize the total number of stones Alice can collect.

The constraints are small: each pile size is at most 100 and there are at most 100 test cases. This immediately rules out any need for complex data structures or optimization techniques. Even a simulation over all states would be feasible in principle, but the structure of the operations suggests a much simpler greedy reasoning.

A subtle edge case appears when one pile is abundant but cannot be fully exploited because of a bottleneck in the previous pile. For example, if $a = 0$, $b = 1$, $c = 100$, no operation can use the third pile at all, so the answer is 0 despite a large supply in $c$. Similarly, if $b$ is small, it limits both operations, and naive attempts that focus only on pairing $b$ with $c$ or $a$ independently will overcount.

Another failure mode comes from greedily exhausting one operation without considering its impact on enabling the other. Since both operations consume from $b$, the order matters if handled incorrectly.

## Approaches

A brute-force strategy would treat each state as a triple $(a,b,c)$ and recursively try both operations whenever possible. Each move reduces the total number of stones in the system, so the state space is finite. However, even though the constraints are small, this approach is unnecessary because the structure has a strong monotonic property: every operation always consumes stones from higher-index piles in a fixed direction, and never restores resources.

The key observation is that pile $b$ is the only shared resource between the two operations. It acts as a bridge: the first operation consumes $b$ heavily (2 units), while the second consumes it lightly (1 unit). This creates a natural dependency chain from $c \rightarrow b \rightarrow a$.

Instead of simulating choices, we can think in terms of how many times we use each operation. Let $x$ be the number of times we apply the second operation (using $b,c$), and $y$ be the number of times we apply the first operation (using $a,b$). The constraints become:

$c \ge 2x$, $b \ge x + 2y$, $a \ge y$.

Each operation always yields exactly 3 stones, so maximizing collected stones is equivalent to maximizing $3(x+y)$, or simply maximizing $x+y$.

To maximize the number of operations, we want to prioritize the operation that consumes fewer bottleneck resources first. The second operation is strictly more efficient in terms of consuming $b$ per stone gained from $c$, so we should perform it as many times as possible before using $b$ for the first operation.

Once the second operation is exhausted, we greedily use the first operation with whatever remains.

This greedy ordering is sufficient because once $b$ is reduced, it cannot be recovered, and delaying the second operation would only reduce the number of possible uses of $c$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search) | $O(3^{a+b+c})$ worst-case exponential | $O(a+b+c)$ recursion | Too slow |
| Greedy with ordering | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We compute the answer independently for each test case.

1. First determine how many times the second operation can be applied. This is limited by pile $c$, since each use requires two stones from $c$. So we compute $x = \min(b, c // 2)$ only in terms of feasibility, but we must also consider that each use consumes one unit of $b$, so $x = \min(b, c // 2)$. This step prioritizes using $c$ before it becomes unusable.
2. After performing $x$ second operations, update the remaining resources: $b := b - x$ and $c := c - 2x$. The remaining value of $c$ is irrelevant for further operations.
3. Now compute how many times the first operation can be applied using remaining $a$ and $b$. Each use consumes one $a$ and two $b$, so $y = \min(a, b // 2)$.
4. The final answer is $3(x + y)$, since each operation contributes exactly three stones to Alice’s collection.

### Why it works

The core invariant is that pile $c$ is only useful through the second operation, and once the second operation is no longer possible, $c$ becomes irrelevant. Similarly, pile $a$ is only consumed by the first operation and never influences any other choice.

The only coupling occurs through $b$, which is shared. Because the second operation uses strictly fewer units of $b$ per unit of progress in the system (it unlocks consumption of $c$ without needing $a$), it is always optimal to prioritize it. Any reordering that delays second-operation usage can only reduce the maximum possible consumption of $c$, while never increasing access to $a$. Therefore, the greedy split between the two operations is optimal.

## Python Solution

```
PythonRun
```

The solution directly applies the greedy split described earlier. The only subtle point is that we must update $b$ after using the second operation before computing the first operation, since both compete for the same resource.

A common mistake is computing both $x$ and $y$ independently from the original $b$, which overcounts usage of pile $b$.

## Worked Examples

### Example 1

Input:

```

```

We track the process:

| Step | a | b | c | x (second ops) | b after | y (first ops) | total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| initial | 3 | 4 | 5 | 0 | 4 | 0 | 0 |
| apply second ops | 3 | 4 | 5 | 2 | 2 | 0 | 6 |
| apply first ops | 3 | 2 | 1 | 2 | 2 | 1 | 9 |

We first apply the second operation twice, consuming most of $c$ while carefully spending $b$. After that, only a small portion of $b$ remains, which allows one application of the first operation. The final result is 9.

### Example 2

Input:

```

```

| Step | a | b | c | x | b after | y | total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| initial | 1 | 0 | 5 | 0 | 0 | 0 | 0 |

No second operation is possible because $b = 0$, and no first operation is possible either. The answer is 0. This shows that large $c$ is useless if the intermediate bottleneck $b$ is missing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case is processed with a constant number of arithmetic operations |
| Space | $O(1)$ | Only a fixed number of variables are used |

The constraints allow up to 100 test cases with small values, so a constant-time per test solution is easily sufficient.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | 0 | all piles empty |
| 0 3 10 | 6 | only second operation chain |
| 5 10 0 | 15 | only first operation chain |
| 3 6 6 | 15 | mixed dependency between both operations |

## Edge Cases

When $a = 0$, the first operation is impossible regardless of how much remains in $b$ or $c$. The algorithm handles this because $y = \min(a, b // 2)$ immediately becomes zero, preventing any invalid usage.

When $b < 2$, both operations are severely restricted. The second operation may still run once if $c \ge 2$, but after subtracting $b$, the first operation cannot proceed. The greedy update of $b$ ensures no overuse occurs.

When $c$ is large but $b$ is small, the algorithm prioritizes converting $c$ into usable intermediate value first. Once $b$ is exhausted, no further use of $c$ is possible, which matches the real constraint structure.
