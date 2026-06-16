---
title: "CF 946A - Partition"
description: "We are given a list of integers, and we are allowed to split this list into two groups in any way we like, with the only rule that every element must belong to exactly one of the two groups."
date: "2026-06-17T02:29:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 946
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 39 (Rated for Div. 2)"
rating: 800
weight: 946
solve_time_s: 82
verified: true
draft: false
---

[CF 946A - Partition](https://codeforces.com/problemset/problem/946/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers, and we are allowed to split this list into two groups in any way we like, with the only rule that every element must belong to exactly one of the two groups. One group contributes positively to a score, while the other group contributes negatively. More precisely, if we call the two groups $b$ and $c$, the value we care about is the sum of elements in $b$ minus the sum of elements in $c$, and we want to make this value as large as possible.

This setup immediately suggests that each element independently influences the final expression depending on which group it is placed in. Since each element is either added once (if placed in $b$) or subtracted once (if placed in $c$), the decision for each element is local, but the objective couples them through a single global sum.

The constraints are small, with at most 100 numbers, each ranging between -100 and 100. This rules out any need for advanced optimization or pruning strategies. Even an exponential enumeration of assignments over all elements would still be conceptually valid at this scale, though unnecessary. A linear or near-linear greedy reasoning is sufficient.

A subtle edge case appears when all numbers are negative. A naive intuition might suggest mixing them between groups could help balance values, but because every element is forced into exactly one group, placing a negative number into the positive group actually reduces the score, while placing it into the negative group turns it into a positive contribution. For example, with input $[-5]$, putting it into $b$ yields $-5$, but putting it into $c$ yields $5$, so the optimal answer is $5$. Any strategy that assumes “positive group should contain larger numbers” without considering sign inversion will fail here.

Another edge case is zero values. Zeros do not affect the total regardless of assignment, but careless implementations that try to “balance” group sizes or rely on sorting might mishandle them by accidentally changing structure without improving the objective.

## Approaches

A brute-force solution considers every possible assignment of each element into either group $b$ or group $c$. For each of the $n$ elements, there are two choices, which leads to $2^n$ possible partitions. For each partition, computing the sums of both groups takes $O(n)$, giving an overall complexity of $O(n \cdot 2^n)$. With $n = 100$, this becomes astronomically large and completely infeasible.

The key observation is that the expression $B - C$ can be rewritten in a way that removes any dependency between elements. If an element $a_i$ is placed in $b$, it contributes $+a_i$. If it is placed in $c$, it contributes $-a_i$. So each element independently contributes either $+a_i$ or $-a_i$, and we want to maximize the total sum of these signed contributions.

This immediately reduces the problem to deciding, for each element, whether $a_i$ or $-a_i$ is larger. To maximize contribution, we always choose the positive value of $|a_i|$, because between $a_i$ and $-a_i$, the larger is always $|a_i|$ if we assign it correctly: positive numbers go to $b$, negative numbers go to $c$.

Thus, the optimal strategy is simply to sum absolute values of all elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Optimal (sign choice) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the list of integers.

Each element is treated independently because its contribution depends only on which group it is assigned to.
2. Initialize an accumulator variable to zero.

This will store the maximum achievable value of $B - C$.
3. For each element $a_i$, compute its absolute value and add it to the accumulator.

This corresponds to choosing the better of placing $a_i$ in $b$ or placing it in $c$, since those choices yield $a_i$ and $-a_i$ respectively.
4. After processing all elements, output the accumulator.

The reasoning behind step 3 is the core of the solution: every element independently contributes either positively or negatively, and we always select the orientation that maximizes its contribution.

### Why it works

The objective function decomposes into a sum over independent choices:

$$B - C = \sum_{i=1}^{n} x_i$$

where each $x_i$ is either $a_i$ or $-a_i$. Since each term is independent of the others, maximizing the total reduces to maximizing each term individually. Choosing $\max(a_i, -a_i)$ for each index yields $|a_i|$, ensuring no local improvement is possible and therefore no global improvement exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ans = 0
for x in a:
    ans += abs(x)

print(ans)
```

The solution reads the input in linear time and iterates once through the array. The accumulator `ans` directly reflects the decomposition of the objective into independent per-element contributions. The key implementation detail is using `abs(x)` rather than conditional branching; both are equivalent, but the absolute value form reduces the risk of sign mistakes.

## Worked Examples

### Example 1

Input:

```
3
1 -2 0
```

| Element | Value | Choice | Contribution | Running Sum |
| --- | --- | --- | --- | --- |
| 1 | 1 | b | +1 | 1 |
| 2 | -2 | c | +2 | 3 |
| 3 | 0 | either | 0 | 3 |

This trace shows that each element is independently assigned to maximize its contribution. The zero contributes nothing regardless of placement, confirming it does not affect the decision process.

### Example 2

Input:

```
4
-5 -1 3 2
```

| Element | Value | Choice | Contribution | Running Sum |
| --- | --- | --- | --- | --- |
| 1 | -5 | c | +5 | 5 |
| 2 | -1 | c | +1 | 6 |
| 3 | 3 | b | +3 | 9 |
| 4 | 2 | b | +2 | 11 |

This example highlights that negative values are always flipped into the positive group effectively, and positive values stay in the positive group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is processed once to compute its absolute value |
| Space | $O(1)$ | Only a running sum is maintained |

The linear scan easily fits within the constraints since $n \le 100$, and even much larger inputs would not pose a problem.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    return str(sum(abs(x) for x in a))

# provided samples
assert run("3\n1 -2 0\n") == "3"

# all positive
assert run("4\n1 2 3 4\n") == "10"

# all negative
assert run("4\n-1 -2 -3 -4\n") == "10"

# single element
assert run("1\n-100\n") == "100"

# includes zeros
assert run("5\n0 0 0 0 0\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all positive | 10 | no need to flip signs |
| all negative | 10 | optimal flipping into c-group |
| single element | 100 | boundary correctness |
| all zeros | 0 | neutral elements handled correctly |

## Edge Cases

For a single negative element like `[-7]`, the algorithm computes `abs(-7) = 7`, which corresponds to placing it in group $c$. If instead it were placed in group $b$, the contribution would be $-7$, which is strictly worse, confirming the greedy choice is correct.

For an array of zeros like `[0, 0, 0]`, each element contributes zero regardless of placement. The algorithm correctly accumulates zero without making any special-case decisions, and no rearrangement can improve the result since all assignments are equivalent.
