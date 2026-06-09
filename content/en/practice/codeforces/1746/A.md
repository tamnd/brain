---
title: "CF 1746A - Maxmina"
description: "We are given a binary array and two types of reduction operations that shrink the array while replacing segments with either a minimum or a maximum."
date: "2026-06-09T15:47:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1746
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 23"
rating: 800
weight: 1746
solve_time_s: 452
verified: false
draft: false
---

[CF 1746A - Maxmina](https://codeforces.com/problemset/problem/1746/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 7m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array and two types of reduction operations that shrink the array while replacing segments with either a minimum or a maximum. The process continues until the array becomes a single value, and the goal is to determine whether it is possible for that final value to be `1`.

The two operations behave very differently on binary data. The minimum operation on two adjacent elements produces `1` only when both are `1`, otherwise it produces `0`. This means it is a “destroying” operation for ones. The maximum operation on a block of length `k` produces `1` if there is at least one `1` in the block, so it acts as a way to spread or preserve a `1`.

Even though the array can be transformed in many ways, the constraints are small: `n ≤ 50`. This rules out any need for complex dynamic programming over states of the array. Any correct solution should come from reasoning about what information is preserved rather than simulating all transformations.

The key edge case is when the array contains no `1` at all. In that case, every operation preserves zeros, so the result must always be `[0]`. A slightly more subtle situation would be whether some configurations with a single `1` can get “trapped” by the operations, but experimentation quickly suggests that the presence of at least one `1` is usually enough to force success.

For example, if `a = [0, 0, 0, 1]` and `k = 4`, a single max operation turns the entire array into `[1]`. If `k = 2`, we can still use max operations to move and preserve the `1`, and min operations only collapse adjacent elements without removing the possibility of isolating it. The only truly impossible case is when there is no `1` to begin with.

## Approaches

A brute-force interpretation would try to simulate all possible operations on all possible segments. Each operation reduces the array size, but the number of states grows extremely quickly because every intermediate array configuration can branch into many others. Even with `n ≤ 50`, this becomes infeasible because the number of sequences of operations is exponential.

The key observation is that neither operation creates new `1`s from scratch. The only way a `1` can appear in the final array is if the original array already contains at least one `1`. Once a `1` exists, the max operation guarantees it can be preserved within any chosen window that contains it. After that, repeated reductions can collapse the array down to a single element while keeping at least one `1` alive.

The minimum operation does not help create or spread `1`s, but it also does not prevent a `1` from surviving if we avoid pairing it with `0` in a destructive way. Since we are free to choose operations and segments, we can always arrange a sequence where a `1` is preserved until the end.

This reduces the entire problem to a single question: does the array contain at least one `1`?

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Check existence of 1 | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to checking whether any `1` exists in the array.

1. Scan the array once from left to right and check if any element equals `1`. This step captures the only necessary condition for success, since without a `1` there is no operation that can ever introduce one.
2. If at least one `1` is found, immediately conclude that it is possible to reach `[1]`. The reasoning is that a `1` can always be preserved through max operations and the array can always be collapsed afterward.
3. If no `1` exists, conclude that the answer is impossible. All operations on zeros will always produce zeros, so the final array must be `[0]`.

### Why it works

Both operations are monotonic with respect to the existence of `1`. The minimum operation cannot create a `1`, and the maximum operation only preserves an existing `1` if one is already inside the chosen segment. This means the predicate “array contains at least one `1`” never becomes true if it starts false, and once true, it can be maintained until the array is reduced to size one. Therefore the existence of a `1` is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    if any(x == 1 for x in a):
        print("YES")
    else:
        print("NO")
```

The solution directly implements the derived condition. The `any` check scans once through the array, giving linear time per test case. No simulation of operations is needed because the structure of the operations guarantees that no configuration without an initial `1` can ever produce one.

A common mistake would be trying to model the operations explicitly, but the constraints make that unnecessary. The entire transformation process collapses to a single invariant check.

## Worked Examples

Consider an input where `a = [0, 1, 0]` and `k = 2`. The scan detects a `1` immediately, so the answer is `YES`. Operationally, we could merge and shrink while preserving the `1`, but the algorithm does not need to simulate this.

Now consider `a = [0, 0, 0, 0]` with any `k`. The scan finds no `1`, so the answer is `NO`. Every possible operation produces either a minimum or maximum of zeros, which is always zero, so the array can never become `[1]`.

These two traces show that the algorithm is not reasoning about transformations at all, only about whether a single necessary resource exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single scan over the array |
| Space | O(1) | Only constant extra variables are used |

The constraints allow up to 1000 test cases with arrays of size up to 50, so the total work is at most 50,000 element checks, which is comfortably fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        out.append("YES" if any(x == 1 for x in a) else "NO")
    return "\n".join(out)

# provided samples
assert run("""7
3 2
0 1 0
5 3
1 0 1 1 0
2 2
1 1
4 4
0 0 0 0
6 3
0 0 1 0 0 1
7 5
1 1 1 1 1 1 1
5 3
0 0 1 0 0
""") == """YES
YES
YES
NO
YES
YES
YES"""

# all zeros
assert run("""1
5 3
0 0 0 0 0
""") == "NO"

# single one
assert run("""1
5 3
0 0 1 0 0
""") == "YES"

# all ones
assert run("""1
4 2
1 1 1 1
""") == "YES"

# k equals n with a one
assert run("""1
4 4
0 0 0 1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | NO | impossibility without any 1 |
| single one | YES | sufficiency of one 1 |
| all ones | YES | trivial positive case |
| k = n with one | YES | global max operation case |

## Edge Cases

When the array contains only zeros, every operation preserves the all-zero structure. For example, `[0, 0, 0, 0]` remains all zeros under both min and max operations, so it always ends as `[0]`.

When there is exactly one `1`, such as `[0, 0, 1, 0]`, the algorithm immediately accepts. Any sequence of operations can be arranged so that the segment containing the `1` is preserved by max operations until the array is reduced. Even if intermediate merges involve zeros, the presence of the `1` guarantees it can always be kept inside some chosen segment.

When all elements are `1`, any operation still produces `1`, so reduction to `[1]` is straightforward regardless of `k`.

When `k = n`, a single max operation collapses the entire array into a single value, which becomes `1` if any `1` exists. This matches the same condition derived by the general argument.
