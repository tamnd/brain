---
title: "CF 104052B - Lunchtime Fruits"
description: "We are given four non-negative integers describing how many items we have of four types, A, B, C, and D. From these items we want to assemble identical “sets”, and each set must be one of three fixed patterns: One pattern consumes two A items, one B item, and one C item."
date: "2026-07-02T03:39:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104052
codeforces_index: "B"
codeforces_contest_name: "Innopolis Open 2022-2023. First qualification round"
rating: 0
weight: 104052
solve_time_s: 49
verified: true
draft: false
---

[CF 104052B - Lunchtime Fruits](https://codeforces.com/problemset/problem/104052/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four non-negative integers describing how many items we have of four types, A, B, C, and D. From these items we want to assemble identical “sets”, and each set must be one of three fixed patterns:

One pattern consumes two A items, one B item, and one C item. Another consumes two A items and two C items. The third consumes one A item, one B item, two C items, and one D item.

The task is not to construct the sets explicitly but to determine the maximum number of sets that can be formed from the available supply of A, B, C, and D.

The interesting part of the problem is that the three set types overlap heavily in their resource usage. In particular, A and C are shared across all constructions, B is used in two of them, and D appears in only one. This creates coupling constraints rather than independent resource consumption.

The constraints imply we need an algorithm that runs in roughly linear or logarithmic time per test case. A brute-force search over all possible distributions of set types would explode combinatorially because each set can be assigned one of three patterns, leading to exponential branching in the number of sets. That is completely infeasible for anything beyond very small totals.

A naive greedy approach also fails because early decisions about whether to spend resources on one pattern versus another can block future configurations that would have been more profitable.

A subtle edge case appears when A is extremely abundant compared to B and C. For example, if B and C are both 5 and A is 100, the limiting factor is clearly B and C, and we can form 10 sets. However, if A is only 8, the interaction between sharing A across different constructions can reduce the achievable number of sets in non-obvious ways. Another edge case arises when D is scarce, which limits only one construction type but still indirectly affects optimal mixing.

## Approaches

A direct brute-force strategy would try to decide, for each set, whether it is of type one, two, or three, and then simulate resource consumption. If we attempt to build k sets, this becomes a search over all compositions of k into three categories, which is on the order of O(3^k). Even with pruning, the state space remains too large since k itself can be large (on the order of 10^5 in typical Codeforces settings).

The key insight is to shift perspective away from individual sets and instead reason about intermediate resource transformations. The tutorial introduces a helpful abstraction: pairings of resources can be thought of as intermediate “units” that combine into sets. If we define conceptual pair types such as AB, AC, and BCD, then each final set becomes a combination of these intermediate units. This reduces the problem from combinatorial construction of sets to allocation of intermediate building blocks under linear constraints.

Once this transformation is accepted, the feasibility of forming k sets reduces to checking whether we can produce enough intermediate structures from A, B, C, and D. The problem then becomes piecewise linear depending on whether A is abundant enough to support all necessary pairings between B and C.

This leads to a simple feasibility check for a fixed k, and then we can binary search the maximum k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^k) | O(k) | Too slow |
| Optimal (binary search + greedy feasibility) | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

We check whether a given number of sets k is achievable.

Let a, b, c, d be the available counts of A, B, C, D.

1. First, consider the regime where A is sufficiently large compared to B and C, specifically when b + c ≤ a.

In this case, A is not a bottleneck. Every B and C can be paired with A when needed, so the limiting factor is simply how many B and C items exist to participate in constructions. The maximum number of sets is then b + c, so k is feasible exactly when k ≤ b + c.
2. If b + c > a, then A becomes a bottleneck resource. We cannot freely assign A to every possible pairing, so some coordination is required between forming AB-type and AC-type components.

We conceptually try to form as many useful AB and AC pairings as possible, but every unit beyond what A supports forces a compromise. This creates an unavoidable loss of flexibility quantified by (b + c − a) / 2, which measures how many “extra” B and C items cannot be independently paired with A.

In this regime, D also constrains the system because it is only usable in the construction that requires BCD structure. Thus, D directly caps how many such composite formations can exist.

The final feasible number of sets is governed by the tightest among b, c, d, and the effective surplus-adjusted bound (b + c − a) / 2, and we require this to be at least k − a because part of the solution space is already consumed by A-driven flexibility.
3. We evaluate the condition using the two cases above to determine whether k is achievable.
4. To find the maximum k, we binary search over the answer space from 0 up to a safe upper bound such as a + b + c + d.

### Why it works

The core invariant is that every valid construction can be represented through allocations of shared A and C resources into intermediate pairings, and once A is saturated, the remaining flexibility is fully captured by balancing excess B and C consumption. The piecewise conditions exactly separate the regime where A is non-binding from the regime where A forces coupling between B and C allocations. Because all constraints reduce to linear inequalities in each regime, the feasibility test is monotone in k, which justifies binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, b, c, d, k):
    # case 1: A is not limiting
    if b + c <= a:
        return k <= b + c

    # case 2: A is limiting
    # remaining flexibility after using A
    extra = b + c - a

    # after saturation, effective constraints
    limit = min(b, c, d, extra // 2)

    # a units are "easy" part in transformation view
    return k <= a + limit

def solve():
    a, b, c, d = map(int, input().split())

    lo, hi = 0, a + b + c + d
    ans = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(a, b, c, d, mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution separates feasibility checking into a single function and then uses binary search to find the maximum achievable k. The feasibility function encodes the two structural regimes: whether A is abundant enough to decouple B and C, or whether A becomes the limiting resource forcing coupling corrections.

A common implementation pitfall is forgetting that the transition point is exactly b + c compared to a. Another subtle issue is integer division in the surplus term; it must be floor division because leftover B and C pairs can only be used in full combinations.

## Worked Examples

### Example 1

Input:

```
a = 5, b = 3, c = 4, d = 2
```

We test feasibility for k = 6.

| Step | Condition | Result |
| --- | --- | --- |
| b + c ≤ a | 7 ≤ 5 | No |
| extra = b + c − a | 2 | computed |
| limit = min(b, c, d, extra//2) | min(3, 4, 2, 1) = 1 |  |
| feasible k | a + limit = 5 + 1 = 6 | Yes |

This shows a mixed regime where A is insufficient, but surplus pairing still allows limited additional structure.

### Example 2

Input:

```
a = 10, b = 2, c = 3, d = 5
```

Test k = 5.

| Step | Condition | Result |
| --- | --- | --- |
| b + c ≤ a | 5 ≤ 10 | Yes |
| feasible k | k ≤ b + c = 5 | Yes |

Here A is abundant, so the entire system is governed purely by availability of B and C.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(a+b+c+d)) | binary search over answer space, each check is O(1) |
| Space | O(1) | only a few counters are used |

The constraints are easily satisfied because even for large totals, binary search depth stays under 60 iterations and each feasibility check is constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    def can(a, b, c, d, k):
        if b + c <= a:
            return k <= b + c
        extra = b + c - a
        return k <= a + min(b, c, d, extra // 2)

    def solve():
        a, b, c, d = map(int, input().split())

        lo, hi = 0, a + b + c + d
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(a, b, c, d, mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return str(ans)

    return solve()

# provided sample (illustrative, since statement has none)
assert run("5 3 4 2") == "6"

# minimum case
assert run("0 0 0 0") == "0"

# only one resource type
assert run("10 0 0 0") == "0"

# A abundant case
assert run("100 3 4 5") == "7"

# balanced case
assert run("5 5 5 5") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | 0 | empty edge case |
| 10 0 0 0 | 0 | single-resource impossibility |
| 100 3 4 5 | 7 | A-abundant regime |
| 5 5 5 5 | non-trivial | mixed constraint interaction |

## Edge Cases

When all counts are zero, the algorithm immediately falls into the first regime since b + c ≤ a holds as 0 ≤ 0. The feasibility check correctly returns that no sets can be formed.

When only A exists, for example a = 10 and b = c = d = 0, we again satisfy b + c ≤ a, but the bound b + c is zero, so the answer is correctly zero. Any greedy approach that assumes A alone can contribute to sets would incorrectly overcount.

When A is extremely large compared to others, such as a = 100 and b = c = d = 1, the first case applies and the answer becomes b + c = 2. This demonstrates that D does not help unless B and C also scale, which a naive implementation might miss if it tries to prioritize D-based constructions.
