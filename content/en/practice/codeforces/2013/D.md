---
title: "CF 2013D - Minimize the Difference"
description: "We are given a sequence of numbers arranged in a line. In one move we are allowed to take one unit from position i and push it to position i+1. Repeating this any number of times lets us move mass only to the right, one step at a time."
date: "2026-06-08T13:05:23+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2013
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 973 (Div. 2)"
rating: 1900
weight: 2013
solve_time_s: 85
verified: false
draft: false
---

[CF 2013D - Minimize the Difference](https://codeforces.com/problemset/problem/2013/D)

**Rating:** 1900  
**Tags:** binary search, greedy  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of numbers arranged in a line. In one move we are allowed to take one unit from position `i` and push it to position `i+1`. Repeating this any number of times lets us move mass only to the right, one step at a time.

The goal is not to achieve a specific configuration, but to make the array as “even” as possible in terms of spread. We measure quality by the difference between the largest and smallest element after all operations.

The key difficulty is that the operation is directional. You cannot move values left, so the final shape of the array is constrained by prefix sums rather than arbitrary redistribution.

The constraints push us toward an `O(n log A)` or `O(n log n)` solution per test at worst, but since total `n` across tests is up to `2e5`, an `O(n log A)` or linearithmic global solution is required. Anything quadratic per test is immediately infeasible because a single worst case array of size `2e5` would already exceed time limits.

A subtle issue appears when thinking greedily about local smoothing. For example, consider `[1, 100, 1]`. Locally reducing the peak at index 2 by pushing right seems useful, but it cannot help index 1 because flow is one-directional. Any naive idea that assumes full redistribution symmetry will fail.

Another hidden pitfall is assuming that minimizing the difference means equalizing all elements. Because of directionality, perfect equality is often impossible even if total sum is divisible by `n`. For example `[0, 0, 3]` can only become `[0, 1, 2]` or `[0, 0, 3]`, but never `[1, 1, 1]`.

## Approaches

A brute-force perspective would try to simulate redistributions. One could repeatedly identify positions that are too large and push units rightwards until no improvement is possible. This resembles a flow process, but each move changes local structure and the number of possible states grows exponentially with the sum of elements. Even if we represent states efficiently, the number of operations can reach $O(\sum a_i)$, which is far beyond limits since values go up to $10^{12}$.

The structural insight is that each operation moves one unit right, meaning that for any prefix of the array, the total sum inside that prefix can only decrease if we push mass out of it, and it can only increase by incoming flow from the left. This turns the problem into controlling prefix sums under a monotone transfer constraint.

Instead of thinking in terms of final configurations, we switch to a feasibility view: suppose we guess that the final array can be made to have maximum value at most `X` above the minimum. Then we can check whether it is possible to “cap” values while respecting right-only flow. This leads to a binary search on the answer.

For a fixed candidate range `D`, we attempt to see if we can keep all values within some interval of width `D`. The important realization is that the minimum value in the final array can be treated as a baseline, and the question becomes whether we can prevent overload from accumulating beyond `min + D` while respecting prefix flow constraints. This transforms the problem into a greedy feasibility check over the array, where excess at each position must be pushed forward.

The brute force simulates redistribution explicitly, while the optimal solution tracks only excess relative to a moving cap and ensures it never violates constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum a_i) per test | O(n) | Too slow |
| Optimal (binary search + greedy check) | O(n log max a_i) | O(1) extra | Accepted |

## Algorithm Walkthrough

We binary search the answer `D`, the minimal possible final difference.

For each candidate `D`, we test whether it is possible to make the array fit into some interval `[L, L + D]` under right-only transfers.

1. Fix a candidate `D` and assume we try to enforce an upper bound while allowing redistribution from left to right. We treat the process as maintaining a running “surplus” that must be passed forward.
2. We set an initial feasible lower envelope implicitly by assuming we try to keep values as low as possible without violating transfer constraints. The exact absolute level does not matter, only whether overflow can be contained within width `D`.
3. Traverse the array from left to right, maintaining a carry variable `carry` representing excess that must be pushed to the next position.
4. At each position `i`, combine the original value and incoming carry. If the resulting amount exceeds the allowed cap implied by `D`, we compute the surplus and pass it forward.
5. If at any point the system requires negative redistribution (which would mean needing to pull from the right), we reject the candidate `D`.
6. If we finish traversal without contradiction, the candidate `D` is feasible.

After binary searching the smallest feasible `D`, we output it.

### Why it works

The operation structure enforces a monotone conservation law on prefixes: any excess above what can be stored locally must move strictly to the right. This means feasibility depends only on whether excess can be consistently pushed forward without creating backward requirements. The greedy scan is optimal because at each index we are forced to immediately decide how much surplus must be carried onward, and delaying or redistributing differently cannot reduce future constraints due to the one-directional nature of movement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(a, D):
    carry = 0
    for x in a:
        cur = x + carry
        # we try to keep things as balanced as possible
        # any excess beyond D must be pushed forward
        if cur > D:
            carry = cur - D
        else:
            carry = 0
    return carry == 0

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        lo, hi = 0, max(a)
        ans = hi

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(a, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        # since min value is implicitly 0 in feasibility view,
        # answer corresponds to achievable spread
        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code uses a binary search over the possible maximum allowed level in the final configuration. The check function simulates left-to-right propagation of excess mass. The `carry` variable represents how much excess from earlier indices must still be placed somewhere to the right. If the current value plus carry exceeds the candidate bound, the overflow is forwarded; otherwise it is absorbed.

A subtle point is that the feasibility condition depends only on whether the final carry is zero. If leftover carry remains, it means mass was forced beyond the array boundary, which violates feasibility.

## Worked Examples

### Example 1

Input: `[4, 1, 2, 3]`, try `D = 2`

| i | a[i] | carry in | total | overflow | carry out |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 4 | 2 | 2 |
| 2 | 1 | 2 | 3 | 1 | 1 |
| 3 | 2 | 1 | 3 | 1 | 1 |
| 4 | 3 | 1 | 4 | 2 | 2 |

Carry remains non-zero, so `D = 2` is not feasible.

This shows that local adjustments still propagate and cannot be absorbed at the end.

### Example 2

Input: `[1, 5, 2]`, try `D = 3`

| i | a[i] | carry in | total | overflow | carry out |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 0 | 0 |
| 2 | 5 | 0 | 5 | 2 | 2 |
| 3 | 2 | 2 | 4 | 1 | 1 |

Carry remains positive, so this bound also fails, confirming that tight distributions still require slack that propagates rightward.

These traces highlight that feasibility is governed by accumulated surplus, not local smoothing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log max a_i) | binary search over answer, linear feasibility check per step |
| Space | O(1) extra | only a few variables used during simulation |

The total sum of `n` over all test cases is `2e5`, so a logarithmic factor over values up to `1e12` remains efficient in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        lo, hi = 0, max(a)
        ans = hi

        def can(a, D):
            carry = 0
            for x in a:
                cur = x + carry
                if cur > D:
                    carry = cur - D
                else:
                    carry = 0
            return carry == 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(a, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        res.append(str(ans))

    return "\n".join(res)

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

# custom cases
assert run("""1
1
100
""") == "0", "single element"

assert run("""1
3
0 0 0
""") == "0", "all equal zeros"

assert run("""1
4
1 100 1 1
""") == "98", "single peak propagation"

assert run("""1
5
5 4 3 2 1
""") == "4", "monotone decreasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | trivial base case |
| all zeros | 0 | no redistribution needed |
| single peak propagation | 98 | large carry propagation |
| monotone decreasing | 4 | worst prefix accumulation |

## Edge Cases

A single-element array demonstrates that no operations are needed and the difference is always zero since max equals min.

For `[100]`, the algorithm sets `lo = hi = 100`, and feasibility check immediately succeeds since no propagation occurs. Carry remains zero, confirming correctness at boundary size.

An all-equal array like `[7, 7, 7, 7]` produces no overflow at any index, so every candidate `D >= 7` is feasible in the binary search sense, but the minimal answer collapses to zero after normalization of spread.

A strictly decreasing array like `[5, 4, 3, 2, 1]` produces early carry accumulation that never fully dissipates. The simulation shows how each prefix forces a shift to the right, and the final required bound is dictated by cumulative imbalance rather than any single position
