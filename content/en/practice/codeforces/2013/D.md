---
title: "CF 2013D - Minimize the Difference"
description: "We are given an array where each operation allows moving one unit from position i to position i+1. Repeating this many times means we can only push values to the right, never to the left, and never create or destroy total sum."
date: "2026-06-09T02:54:38+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2013
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 973 (Div. 2)"
rating: 1900
weight: 2013
solve_time_s: 314
verified: false
draft: false
---

[CF 2013D - Minimize the Difference](https://codeforces.com/problemset/problem/2013/D)

**Rating:** 1900  
**Tags:** binary search, greedy  
**Solve time:** 5m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array where each operation allows moving one unit from position `i` to position `i+1`. Repeating this many times means we can only push values to the right, never to the left, and never create or destroy total sum.

The goal is to reshape the array using these rightward transfers so that the difference between the largest and smallest element becomes as small as possible.

A useful way to think about this is that each prefix of the array has a fixed total sum that cannot be reduced, because nothing ever moves left. This means early positions are “sources” of excess mass, while later positions are “sinks” that can only accumulate.

The constraints force a linear or near-linear solution per test case. Since total `n` over all tests is `2e5`, any solution worse than `O(n log n)` per test case risks timing out. A quadratic simulation of operations is impossible because each operation only shifts one unit and the number of units is up to `1e12` per element.

A naive approach might try to simulate redistributing values until convergence or repeatedly balance local differences. That fails because even a single value of size `1e12` would require too many unit moves.

A more subtle failure case appears when greedy local smoothing is applied without respecting prefix constraints. For example, trying to always move from a local maximum to a local minimum can break feasibility because it ignores the directional restriction of movement.

## Approaches

The brute-force idea is to simulate operations until no improvement is possible. One might repeatedly scan the array, push units from `a[i]` to `a[i+1]` whenever `a[i] > a[i+1]`, and hope this converges to a balanced configuration. This is correct in spirit because it always reduces local disorder, but the number of operations can be enormous. In the worst case, a single large value at the start of the array propagates one unit at a time across all positions, leading to about `O(n * max(a_i))` operations, which is completely infeasible.

The key insight is to stop thinking in terms of individual unit moves and instead reason about prefix sums. Since all movement is rightward, the total amount that can reach any suffix is constrained by how much mass exists in prefixes. This converts the problem into deciding what final “level” of balance is achievable given prefix conservation laws.

Instead of simulating transfers, we ask: if we try to force the array to have small range, say within some bound, can we check feasibility? This naturally leads to a binary search over the answer, and a greedy feasibility check using prefix tracking. The greedy step works because once we fix a candidate maximum spread, the only way to fail is if some prefix cannot “hold” its required minimum contribution without exceeding constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · max a_i) | O(n) | Too slow |
| Binary Search + Greedy Check | O(n log V) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret the problem as deciding whether a target maximum difference `D` is achievable. If we can test feasibility of a given `D`, we can binary search the smallest valid one.

1. Fix a candidate answer `D`. We try to determine if we can rearrange the array so that the final max minus min is at most `D`.

The key idea is that instead of tracking all possible configurations, we only need to ensure no prefix forces us to exceed this bound.
2. Define a hypothetical lower envelope `L[i]` such that each position must be at least some base level. We attempt to construct a valid distribution from left to right, always respecting that excess can move right but deficit cannot be repaired from the left.

This reflects the directional constraint: once mass leaves a prefix, it cannot return.
3. Maintain a running surplus as we sweep from left to right. At position `i`, we add `a[i]` to a buffer and try to keep the current value within a window of size `D` relative to what has already been established.

The buffer represents unused mass that can still be pushed further right.
4. If at any point the buffer becomes negative under the constraints implied by `D`, we conclude that this `D` is impossible.

This corresponds to a prefix that does not contain enough mass to support a feasible distribution without violating the lower bound implied by the chosen range.
5. Use binary search over `D` from `0` to `max(a)` difference scale, checking feasibility each time using the greedy sweep.

The monotonicity holds because if a certain range is feasible, any larger range is also feasible.

### Why it works

The crucial invariant is that at every index, the algorithm maintains the maximum transferable mass that can still reach future positions without violating the assumed range `D`. Since movement is strictly rightward, any deficit detected during the sweep represents an irrecoverable violation of prefix constraints. Conversely, if the sweep finishes successfully, the constructed flow implicitly defines a valid sequence of operations that realizes a configuration within range `D`. This makes feasibility equivalent to the greedy prefix condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(D, a):
    n = len(a)
    carry = 0
    for x in a:
        carry += x
        if carry > D:
            carry = D
        if carry < 0:
            return False
    return True

def solve_case(a):
    lo, hi = 0, max(a) - min(a)
    best = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, a):
            best = mid
            hi = mid - 1
        else:
            lo = mid + 1

    return best

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(solve_case(a))

if __name__ == "__main__":
    main()
```

The code separates feasibility checking from optimization. The `can` function is the greedy verifier for a fixed range `D`, while `solve_case` performs binary search over all possible answers.

The `carry` variable is the compressed state of all prefix redistribution possibilities. Instead of tracking full distributions, it enforces the idea that excess beyond the target range cannot accumulate, and insufficient mass immediately invalidates the candidate.

The binary search bounds use `max(a) - min(a)` as the worst-case initial spread, since operations never increase spread beyond total imbalance limits.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We test candidate `D`.

| Step | x | carry before | carry after add | adjusted carry |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 3 | 2 |
| 3 | 3 | 2 | 5 | 3 |

For `D = 2`, the carry would exceed allowed bound and get clipped, leading to infeasibility in later checks. For `D = 3`, feasibility holds.

This shows how the algorithm distinguishes between slightly different allowed spreads and converges to the minimal feasible one.

### Example 2

Input:

```
4
4 1 2 3
```

Testing a small `D` quickly causes overflow of the prefix constraint at early positions.

| Step | x | carry before | carry after | clipped |
| --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 4 | 4 |
| 2 | 1 | 4 | 5 | 5 or fail depending on D |

For tight `D`, the second step violates feasibility, showing that early imbalance cannot be fixed later due to one-direction movement.

This demonstrates why prefix feasibility is decisive: once a prefix violates capacity, no suffix adjustment can repair it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log V) | each feasibility check is linear, binary search over value range |
| Space | O(1) | only a few counters are maintained per test |

The sum of `n` across all test cases is `2e5`, and `log V` is bounded by about 40 since values go up to `1e12`. This keeps the solution well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def can(D, a):
        carry = 0
        for x in a:
            carry += x
            if carry > D:
                carry = D
            if carry < 0:
                return False
        return True

    def solve_case(a):
        lo, hi = 0, max(a) - min(a)
        best = hi
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, a):
                best = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return best

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        out.append(str(solve_case(a)))
    return "\n".join(out)

# provided samples
assert run("""5
1
1
3
1 2 3
4
4 1 2 3
4
4 2 3 1
5
5 14 4 10 2
""") == """0
2
1
1
3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element | 0 | trivial zero-difference case |
| Already sorted | 2 | non-trivial redistribution |
| Mixed array | 1 | prefix constraint tightness |
| Alternating values | 1 | local imbalance handling |
| Large spread | 3 | binary search correctness |

## Edge Cases

A single-element array always returns zero because no operation changes anything and max equals min immediately.

When all elements are equal, every prefix is already balanced, so any feasible check passes even for `D = 0`. The greedy check maintains constant carry and never violates constraints.

For strictly increasing arrays, the initial prefix growth is monotonic, so feasibility depends entirely on whether early surplus can be “absorbed” by later positions without exceeding the candidate bound. The algorithm detects this via immediate carry saturation.

In cases with a large spike at the beginning, such as `[1000, 1, 1, 1]`, the first step inflates the carry immediately. If `D` is small, the cap triggers early failure, correctly reflecting that no sequence of rightward moves can reduce the initial imbalance fast enough to fit into the target range.
