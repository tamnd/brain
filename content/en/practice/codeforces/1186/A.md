---
title: "CF 1186A - Vus the Cossack and a Contest"
description: "We are given a small distribution problem. There are several participants in a contest, and each participant must receive two items: one pen and one notebook."
date: "2026-06-13T12:19:48+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1186
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 571 (Div. 2)"
rating: 800
weight: 1186
solve_time_s: 188
verified: true
draft: false
---

[CF 1186A - Vus the Cossack and a Contest](https://codeforces.com/problemset/problem/1186/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small distribution problem. There are several participants in a contest, and each participant must receive two items: one pen and one notebook. The organizer has a fixed stock of pens and notebooks, and the task is to decide whether it is possible to satisfy everyone simultaneously.

Formally, each of the n participants needs one pen and one notebook, so the total demand is n pens and n notebooks. The question is simply whether the available quantities m and k are sufficient to cover these two independent requirements at the same time.

The constraints are extremely small, with all values bounded by 100. This immediately rules out any need for optimization or complex data structures. Any solution that performs a constant number of operations will be sufficient, since even a naive simulation would at most perform a few hundred steps.

The only meaningful failure cases arise when one of the two resources is insufficient even if the other is abundant. For example, if n = 8, m = 5, k = 100, pens alone make the task impossible even though notebooks are more than enough. Similarly, if m = 100, k = 2, n = 5, notebooks alone block feasibility. A slightly more subtle mistake happens if one incorrectly tries to compare total items m + k against 2n, which would allow invalid distributions where one category is missing entirely.

## Approaches

A brute-force interpretation would try to assign items participant by participant. For each of the n participants, we would decrement one pen and one notebook from the inventory and check whether we ever go below zero. This is correct because it directly simulates the process of distribution.

However, even though this brute-force is simple, it is unnecessary. It performs n iterations, each doing constant work, which is still fine here but conceptually redundant. More importantly, it obscures the structure of the problem: each participant independently consumes exactly one unit from each resource pool, meaning the feasibility condition decomposes into two independent checks.

The key insight is that there is no interaction between participants beyond counting. Once we realize each participant consumes exactly one pen and one notebook, the entire problem reduces to verifying two inequalities: whether pens are at least n and whether notebooks are at least n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers n, m, and k, which represent the number of participants, pens, and notebooks respectively.
2. Check whether the number of pens is at least n. This condition ensures that we can assign one pen to every participant without running out.
3. Check whether the number of notebooks is at least n. This ensures the same feasibility condition for notebooks.
4. If both conditions hold simultaneously, output "Yes". Otherwise, output "No".

### Why it works

Each participant requires exactly one unit from each of two independent resources. There is no sharing, reuse, or substitution between pens and notebooks. This means feasibility is determined entirely by whether each resource pool individually meets the demand n. Since assignments are independent and identical for every participant, satisfying both global constraints guarantees a valid distribution, and failing either constraint makes it impossible regardless of how the other resource is distributed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    if m >= n and k >= n:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The code reads the three input values and directly checks the two necessary conditions. The comparison is done independently for pens and notebooks because neither resource can compensate for a shortage in the other. The output is printed immediately based on this boolean condition, making the solution constant time.

A common implementation mistake would be to check only m + k >= 2 * n, which ignores the requirement that each participant must receive both items simultaneously. Another mistake would be to subtract greedily from a combined pool, which incorrectly allows mixing resources.

## Worked Examples

### Example 1

Input:

```
5 8 6
```

| Step | n | m | k | m ≥ n | k ≥ n | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 5 | 8 | 6 | - | - | - |
| Check pens | 5 | 8 | 6 | True | - | - |
| Check notebooks | 5 | 8 | 6 | True | True | Yes |

Both resources exceed or match the required number of participants, so every participant can receive both items.

### Example 2

Input:

```
3 9 3
```

| Step | n | m | k | m ≥ n | k ≥ n | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 3 | 9 | 3 | - | - | - |
| Check pens | 3 | 9 | 3 | True | - | - |
| Check notebooks | 3 | 9 | 3 | True | True | Yes |

Even though pens are abundant, notebooks exactly match the requirement, which is still sufficient.

This confirms that equality is acceptable and only strict deficiency causes failure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only two comparisons are performed regardless of input size |
| Space | O(1) | No additional data structures are used |

The constant-time nature fits easily within the constraints, as the input size is trivial and no iteration over participants is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, k = map(int, sys.stdin.readline().split())
    return "Yes" if m >= n and k >= n else "No"

# provided samples
assert run("5 8 6") == "Yes"
assert run("3 9 3") == "Yes"

# custom cases
assert run("1 1 1") == "Yes"
assert run("1 0 1") == "No"
assert run("10 100 9") == "No"
assert run("100 100 100") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | Yes | Minimum valid case |
| 1 0 1 | No | Failure due to pens |
| 10 100 9 | No | Failure due to notebooks |
| 100 100 100 | Yes | Maximum balanced case |

## Edge Cases

One important edge case is when one resource exactly equals n while the other is much larger. For example, n = 4, m = 4, k = 100. The algorithm checks m ≥ n and k ≥ n, so it returns True. This matches reality because every participant still requires one notebook regardless of surplus pens.

Another edge case is when both resources are large in total but unbalanced per category, such as n = 10, m = 19, k = 1. Even though m + k is 20 which exceeds 2n, the algorithm correctly returns No because k < n. Step-by-step, the notebook check fails immediately, preventing an invalid distribution.

A final edge case is the smallest input n = 1, m = 0, k = 1. The pen condition fails, so the algorithm outputs No, which matches the fact that even a single participant cannot be fully equipped.
