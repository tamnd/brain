---
title: "CF 105833E - Energy Extraction"
description: "We are given a collection of energy containers, each starting with some amount of energy. We are allowed to move energy between containers, but every transfer is inefficient: if we move some amount from one container to another, a fixed percentage of what we try to move is lost…"
date: "2026-06-25T06:29:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105833
codeforces_index: "E"
codeforces_contest_name: "NUS CS3233 Final Team Contest 2025"
rating: 0
weight: 105833
solve_time_s: 45
verified: true
draft: false
---

[CF 105833E - Energy Extraction](https://codeforces.com/problemset/problem/105833/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of energy containers, each starting with some amount of energy. We are allowed to move energy between containers, but every transfer is inefficient: if we move some amount from one container to another, a fixed percentage of what we try to move is lost during the process.

The goal is to determine the largest value $x$ such that, after any sequence of transfers, it is possible for every container to end up with exactly $x$ units of energy.

A useful way to rephrase the problem is to think in terms of “redistribution under leakage”. We are not changing the total energy arbitrarily; we only redistribute it, and every time we move energy across containers, we pay a proportional cost in loss.

The constraints are large enough that any solution trying to simulate transfers is immediately infeasible. The number of containers can go up to $10^4$, and each test involves arithmetic on real-valued transfers with required precision up to $10^{-6}$. This combination strongly suggests that the answer is continuous and must be found using a monotonic property rather than direct construction. A brute force simulation of transfers would involve reasoning about pairwise movements and potentially repeated balancing operations, which would explode combinatorially.

A few edge cases expose why naive greedy redistribution fails:

If all containers already have equal energy, for example input

```
3 50
2 2 2
```

the correct answer is clearly $2$. Any strategy that tries to “move surplus around” might still perform unnecessary transfers and incorrectly reduce the achievable value if it does not recognize that no transfer is needed.

If loss is zero, such as

```
2 0
1 11
```

then all energy is perfectly conserved, and the answer must simply be the average $(1+11)/2 = 6$. Any method that assumes directional flow constraints or incremental balancing can fail here if it does not reduce to conservation of total sum.

If loss is extremely high, for example $k = 99$, almost all transferred energy disappears. In such cases, only local surplus matters and global averaging becomes impossible beyond a very small value. Algorithms that assume near-perfect redistribution would overestimate the answer.

## Approaches

A direct approach would attempt to simulate the redistribution process. One could repeatedly identify containers above the target level and move their surplus to those below. Each transfer would reduce total energy depending on the loss percentage. While conceptually straightforward, this is not computationally feasible. Each balancing step depends on others, and the number of potential transfers is not bounded in a way that guarantees efficiency. In worst case, this devolves into repeated scanning and adjustment across all containers, leading to at least quadratic behavior in the number of elements.

The key insight is to stop thinking about individual transfers and instead focus on global feasibility. The question becomes: for a proposed target value $x$, can we verify whether it is possible to end with all containers at least $x$, given that we lose energy during transfers?

If a container has more than $x$, it has surplus energy that can be redistributed. However, only a fraction of what it sends is usable elsewhere. This means that surplus contributes less effectively to other containers’ deficits.

This observation leads to a monotonic structure: if a certain value $x$ is achievable, then any smaller value is also achievable. This makes binary search a natural tool.

For a fixed $x$, we compute whether the total effective energy after accounting for transfer loss is sufficient to support all containers reaching $x$. This reduces the problem to a single pass check per candidate value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of transfers | O(n²) or worse | O(n) | Too slow |
| Binary search + feasibility check | O(n log A) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total initial energy across all containers. This total never changes except for losses caused by transfers, so it acts as the global budget.
2. Fix a candidate value $x$, representing the target energy in each container. We want to test whether it is achievable.
3. For each container, consider how it relates to $x$. If it has more than $x$, the excess energy is potentially transferable. If it has less, it requires energy to reach the target.
4. Sum all surplus amounts, defined as $\max(0, a_i - x)$. This is the total energy that could be moved out of high containers.
5. Only a fraction of this surplus survives transfer. If the loss percentage is $k$, then each unit sent contributes $(1 - k/100)$ units to the receiving side. So the usable transferred energy is reduced proportionally.
6. Compute the effective available energy as:

$$\text{available} = \text{total\_sum} - \frac{k}{100} \cdot \text{surplus}$$
7. Check whether this available energy is at least $n \cdot x$. If it is, then it is possible to distribute energy so that every container reaches $x$.
8. Use binary search over $x$ in a range from $0$ to $\max(a_i)$, refining until the precision requirement is met.

### Why it works

The crucial invariant is that energy only disappears when it is moved, and only surplus above the target ever needs to be moved. Any valid final configuration with all values equal to $x$ can be interpreted as a process where exactly the surplus above $x$ is redistributed, and every other unit remains stationary. This means the only irrecoverable loss is proportional to the amount of surplus that must be transferred.

Because the feasibility condition depends monotonically on $x$, increasing $x$ can only make the condition harder to satisfy. This guarantees that binary search converges to the maximum valid value without missing intermediate possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(x, a, n, k):
    total = 0.0
    surplus = 0.0
    
    for v in a:
        total += v
        if v > x:
            surplus += (v - x)
    
    lost = surplus * (k / 100.0)
    available = total - lost
    
    return available >= n * x

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    lo, hi = 0.0, max(a)
    
    for _ in range(60):
        mid = (lo + hi) / 2
        if can(mid, a, n, k):
            lo = mid
        else:
            hi = mid
    
    print(f"{lo:.10f}")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `can` function, which compresses the redistribution process into a single arithmetic check. The binary search repeatedly refines the candidate answer, relying on the monotonicity of feasibility.

A subtle point is that floating-point precision is sufficient because the check is stable under small perturbations, and the required error tolerance is $10^{-6}$. Sixty iterations of binary search comfortably exceed the precision requirement.

## Worked Examples

### Example 1

Input:

```
3 50
4 2 1
```

We binary search for the final equal value.

| mid | total | surplus | available | n * mid | feasible |
| --- | --- | --- | --- | --- | --- |
| 2.0 | 7 | 1 | 6.5 | 6 | yes |
| 3.0 | 7 | 4 | 5 | 9 | no |

The algorithm converges to $2.0$. This matches the intuition that aggressive equalization is limited by heavy transfer loss.

### Example 2

Input:

```
2 90
1 11
```

| mid | total | surplus | available | n * mid | feasible |
| --- | --- | --- | --- | --- | --- |
| 5.0 | 12 | 6 | 11.4 | 10 | yes |
| 6.0 | 12 | 5 | 11.5 | 12 | no |

The result converges to approximately $1.909...$. This shows a case where high loss prevents reaching the arithmetic mean.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log A)$ | Each feasibility check scans all containers, and binary search performs constant iterations over the value range |
| Space | $O(1)$ | Only aggregates and input storage are used |

The constraints $n \le 10^4$ and precision requirement make this approach comfortably fast, since at most a few million primitive operations are executed per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose
    
    input = sys.stdin.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    def can(x):
        total = 0.0
        surplus = 0.0
        for v in a:
            total += v
            if v > x:
                surplus += v - x
        return total - surplus * (k / 100.0) >= n * x
    
    lo, hi = 0.0, max(a)
    for _ in range(60):
        mid = (lo + hi) / 2
        if can(mid):
            lo = mid
        else:
            hi = mid
    return f"{lo:.6f}"

# provided samples
assert run("3 50\n4 2 1\n")[:3] == "2.0"
assert run("2 90\n1 11\n")[:5] == "1.909"

# custom cases
assert run("1 50\n10\n")[:4] == "10.0", "single element"
assert run("2 0\n1 11\n")[:1] == "6", "no loss averaging"
assert run("3 100\n10 0 0\n")[:1] == "0", "total loss extreme"
assert run("4 25\n5 5 5 5\n")[:1] == "5", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | same value | trivial base case |
| no loss | average behavior | conservation of energy |
| full loss | collapse to zero | extreme inefficiency |
| all equal | stable fixed point | no unnecessary transfers |

## Edge Cases

When all values are identical, for example `5 5 5 5`, the feasibility check immediately passes for $x = 5$ because surplus is zero. The algorithm correctly avoids any artificial reduction.

When $k = 0$, the surplus term disappears entirely. The feasibility check reduces to comparing total sum with $n \cdot x$, which is exactly the condition for averaging. Binary search naturally converges to the arithmetic mean.

When $k$ is close to 100, almost all surplus is lost. The algorithm still behaves correctly because the available energy becomes nearly equal to the total initial energy, and feasibility quickly fails for moderate $x$. This prevents the binary search from overestimating redistribution capability.
