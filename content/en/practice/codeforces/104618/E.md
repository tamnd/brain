---
title: "CF 104618E - Cone Coloring"
description: "We are given a line of $N$ dyes, each with a positive integer beauty value. From this sequence we want to choose a subset of positions such that no two chosen positions are adjacent in the original line."
date: "2026-06-29T17:29:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104618
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 1"
rating: 0
weight: 104618
solve_time_s: 79
verified: true
draft: false
---

[CF 104618E - Cone Coloring](https://codeforces.com/problemset/problem/104618/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of $N$ dyes, each with a positive integer beauty value. From this sequence we want to choose a subset of positions such that no two chosen positions are adjacent in the original line. The score of a choice is the sum of selected beauty values, and we want to maximize this score.

In more familiar terms, this is the maximum-weight independent set on a path graph: each position is a node, edges connect consecutive indices, and we cannot pick adjacent nodes.

The constraint $N \le 10^5$ rules out any exponential subset enumeration. A naive $O(2^N)$ approach is impossible, and even $O(N^2)$ transitions over subarrays would be too slow. We need a linear or near-linear dynamic programming solution.

A subtle edge case comes from small arrays where greedy intuition fails. For example, consider:

Input:

```
3
10 1 10
```

A naive greedy strategy like picking locally optimal elements might pick both 10s if not careful, but they are not adjacent, so that works here. However:

Input:

```
4
8 9 8 9
```

Greedy picking the maximum remaining element repeatedly without state tracking could fail depending on implementation order, while the correct answer is 18 (choose indices 2 and 4).

Another edge case is when $N=1$, where the answer is just the single value, and any DP formulation must correctly initialize base states.

## Approaches

A brute-force solution would try every subset of indices and check whether it contains adjacent pairs. For each subset we compute its sum and track the maximum. There are $2^N$ subsets, and checking each subset costs $O(N)$ if implemented directly, giving $O(N2^N)$ time. Even if we optimize subset checking with bit operations, the exponential number of subsets remains the bottleneck.

The key observation is that decisions are local: at index $i$, we only need to know whether we took $i-1$. If we skip index $i$, the best score up to $i$ is the same as up to $i-1$. If we take index $i$, we must add its value to the best solution up to $i-2$. This creates an optimal substructure where the answer up to $i$ depends only on the previous two states.

This reduces the problem to a simple recurrence, similar to the classic “maximum sum of non-adjacent elements”.

Let $dp[i]$ be the maximum achievable sum using only the first $i$ elements. Then:

$$dp[i] = \max(dp[i-1], dp[i-2] + b_i)$$

This immediately leads to a linear-time DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N2^N)$ | $O(N)$ | Too slow |
| Dynamic Programming | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining only the last two DP states.

1. Initialize two variables to represent the best answers for an empty prefix and a prefix of length one. The empty prefix has value 0, and the first element has value $b_1$.
2. For each position $i$ from 2 to $N$, compute two possibilities: skip the current element, which keeps the previous best, or take the current element, which adds $b_i$ to the best result from two steps back. The larger of these two becomes the new state.
3. After computing the new state, shift the previous states forward so that the “previous” and “two-steps-back” values are always correctly aligned for the next iteration.
4. Continue until all elements are processed. The final answer is the best value at the last position.

The reason this works is that every optimal solution must either include or exclude the last element, and both cases reduce to strictly smaller subproblems that do not overlap in required constraints.

### Why it works

At every index $i$, any valid selection splits into two disjoint classes: those that exclude $i$, which are exactly all valid selections over the first $i-1$ elements, and those that include $i$, which force exclusion of $i-1$ and reduce to valid selections over the first $i-2$ elements. These two cases cover all possibilities and preserve optimal substructure, so taking the maximum preserves global optimality inductively.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
b = list(map(int, input().split()))

if n == 0:
    print(0)
    sys.exit()

if n == 1:
    print(b[0])
    sys.exit()

prev2 = 0
prev1 = b[0]

for i in range(1, n):
    take = prev2 + b[i]
    skip = prev1
    cur = max(skip, take)
    prev2 = prev1
    prev1 = cur

print(prev1)
```

The implementation compresses the DP array into two variables. `prev1` represents $dp[i-1]$, while `prev2` represents $dp[i-2]$. At each step, we compute the recurrence directly.

The base cases handle $N=1$ explicitly so that we do not rely on undefined DP values. The transition order matters: `prev2` must be updated after computing the current state, otherwise we would overwrite the value needed for the next iteration.

## Worked Examples

### Example 1

Input:

```
5
5 10 9 10 7
```

| i | b[i] | skip (dp[i-1]) | take (dp[i-2]+b[i]) | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 5 | 5 |
| 1 | 10 | 5 | 10 | 10 |
| 2 | 9 | 10 | 14 | 14 |
| 3 | 10 | 14 | 20 | 20 |
| 4 | 7 | 20 | 21 | 21 |

The final value 21 comes from selecting indices 1, 3, and 5 in 1-based indexing (10 + 10 + 7). The table shows how each state explicitly compares skipping versus taking, ensuring adjacency constraints are respected.

### Example 2

Input:

```
4
8 9 8 9
```

| i | b[i] | skip | take | dp |
| --- | --- | --- | --- | --- |
| 0 | 8 | 0 | 8 | 8 |
| 1 | 9 | 8 | 9 | 9 |
| 2 | 8 | 9 | 16 | 16 |
| 3 | 9 | 16 | 17 | 17 |

The optimal solution alternates selections to avoid adjacency. The DP correctly accumulates alternating picks, confirming that greedy local choices are insufficient without tracking previous decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each element is processed once with constant-time transition |
| Space | $O(1)$ | Only two rolling DP states are stored |

The linear scan is optimal for $N = 10^5$, and constant memory ensures no pressure on the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input().strip())
    b = list(map(int, input().split()))
    
    if n == 0:
        return "0"
    if n == 1:
        return str(b[0])

    prev2 = 0
    prev1 = b[0]

    for i in range(1, n):
        cur = max(prev1, prev2 + b[i])
        prev2 = prev1
        prev1 = cur

    return str(prev1)

# provided sample
assert run("5\n5 10 9 10 7\n") == "21"

# minimum size
assert run("1\n42\n") == "42"

# two elements
assert run("2\n5 100\n") == "100"

# all equal
assert run("5\n7 7 7 7 7\n") == "21"

# alternating high values
assert run("4\n10 1 10 1\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 42 | base case correctness |
| 2 elements | 100 | correct max choice between adjacent pair |
| all equal | 21 | handling multiple optimal selections |
| alternating peaks | 20 | DP picks alternating indices optimally |

## Edge Cases

For $N=1$, the algorithm directly returns the single value, since the loop is skipped entirely. This avoids accessing invalid DP states.

For $N=2$, the transition correctly compares taking the first or second element without needing any special logic beyond initialization.

For example:

```
2
5 100
```

Initialization gives `prev2 = 0`, `prev1 = 5`. At index 2, we compute `take = 100`, `skip = 5`, so the result is 100. This matches the optimal choice of selecting only the second element.

This shows the recurrence naturally handles adjacency constraints even in minimal configurations without additional branching logic.
