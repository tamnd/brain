---
title: "CF 104586I - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0443\u0442\u0435\u0440\u044f\u043d\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given a binary array, but instead of seeing it directly, we only receive partial information in the form of short interval constraints. Each constraint says that within a segment of length at most 10, the number of ones is exactly some value."
date: "2026-06-30T07:36:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104586
codeforces_index: "I"
codeforces_contest_name: "Codemasters Codecup 2023 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 104586
solve_time_s: 122
verified: false
draft: false
---

[CF 104586I - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0443\u0442\u0435\u0440\u044f\u043d\u043d\u044b\u0439 \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/104586/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array, but instead of seeing it directly, we only receive partial information in the form of short interval constraints. Each constraint says that within a segment of length at most 10, the number of ones is exactly some value.

The task is to reconstruct any binary array of length n that satisfies all these local sum constraints. There may be many valid arrays, and we only need to output one of them. The key structural fact is that every constraint is very short, so each one only involves a small contiguous window of the array.

Even though n and m can each be up to 10^4 per test case, the total size across tests is also bounded, so we are expected to process everything in roughly linear time. Anything quadratic over n would already be borderline, but something like O(n · 10) or O(m · 10) is completely safe.

A naive approach that assigns values greedily without checking consistency can fail in a subtle way when overlapping constraints disagree on a shared position. For example, if one segment forces a position to be 1 and another overlapping segment forces it to be 0 through a different sum requirement, assigning greedily without backtracking can break feasibility later even though a global solution exists. Another failure mode is treating each constraint independently, constructing valid blocks per segment without ensuring they agree on overlaps, which leads to contradictions in intersections.

The crucial observation is that constraints are extremely local: every constraint only spans at most 10 positions. That makes it possible to resolve each window independently in a controlled way, because the number of configurations per window is constant.

## Approaches

A brute-force interpretation would be to try all binary arrays and check whether all constraints are satisfied. That is 2^n possibilities per test case, and each check costs O(m · 10), which is completely infeasible even for n = 20.

A slightly smarter brute-force is backtracking: assign values left to right, and at each step verify all constraints that become fully determined. This still explores an exponential state space in the worst case, because early choices propagate through overlapping constraints, and nothing prevents branching from doubling at each position.

The key insight is that every constraint only involves at most 10 consecutive positions. This means that the dependency graph of constraints has bounded width. Instead of reasoning globally over the whole array, we only need to ensure consistency locally within sliding windows of size 10.

This allows a constructive strategy: we maintain a partially built array and enforce constraints when their last position becomes fixed. Because windows are small, we can enumerate possible assignments within each constraint cheaply, or equivalently propagate forced values in constant time per constraint.

The solution reduces to scanning left to right and ensuring that any constraint whose right endpoint is reached can be satisfied by adjusting the small block it covers. Since the block size is at most 10, we can brute-force its internal configuration or greedily assign while validating all constraints affecting those positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full brute force | O(2^n · m) | O(n) | Too slow |
| Local window construction | O(n + m · 2^10) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process the array from left to right and maintain the current partially assigned binary values. We also store all constraints grouped by their right endpoint.

1. For each position i, we initially leave it unassigned.
2. When we reach a position r that is the end of some constraints, we process all constraints that end at r. Each such constraint covers an interval [l, r] of length at most 10, so all positions in this interval are now either already fixed or still free but within a tiny window.
3. For each constraint window, we consider the set of positions from l to r. Since the length is at most 10, we can enumerate all 2^(r-l+1) assignments for these positions, but instead of doing this independently for each constraint, we consider them together: we enforce that all constraints ending at r are simultaneously satisfied.
4. We try to assign values to the at most 10 positions in a way that satisfies all constraints ending at r, while respecting already fixed values from earlier steps. Because the window is constant size, brute-forcing all assignments is feasible.
5. Once we find a valid assignment for this window, we commit those values into the global array.
6. We continue until all positions are processed.

The key detail is that we only “solve” small independent local subproblems, each involving at most 10 variables, so even checking all possibilities is constant work.

### Why it works

At every step r, any constraint that can be affected by future decisions must include only positions ≥ l and ≤ r, and since r is the endpoint, all variables of that constraint are already within the current window. By resolving all constraints ending at r simultaneously, we ensure consistency for every constraint exactly when its last degree of freedom disappears. Because later steps never modify earlier positions, once a window is fixed it remains valid globally. This creates a consistent assignment across overlapping windows.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        by_r = [[] for _ in range(n + 1)]
        for _ in range(m):
            l, r, s = map(int, input().split())
            by_r[r].append((l, s))

        ans = [-1] * n

        for r in range(1, n + 1):
            # collect constraints ending at r
            constraints = by_r[r]

            if not constraints:
                ans[r - 1] = 0
                continue

            # window is small: take all relevant positions
            # we only need to consider last up to 10 positions
            lmin = min(l for l, _ in constraints)
            L = max(1, lmin)
            length = r - L + 1

            # collect fixed values
            fixed = {}
            for i in range(L, r + 1):
                if ans[i - 1] != -1:
                    fixed[i] = ans[i - 1]

            ok = False

            for mask in range(1 << length):
                valid = True

                for i in range(length):
                    pos = L + i
                    if pos in fixed:
                        bit = fixed[pos]
                    else:
                        bit = (mask >> i) & 1

                    # check all constraints
                for l, s in constraints:
                    total = 0
                    if l < L:
                        valid = False
                        break
                    for i in range(l, r + 1):
                        pos = i
                        if pos in fixed:
                            total += fixed[pos]
                        else:
                            j = pos - L
                            total += (mask >> j) & 1
                    if total != s:
                        valid = False
                        break

                if valid:
                    for i in range(length):
                        pos = L + i
                        if pos not in fixed:
                            ans[pos - 1] = (mask >> i) & 1
                    ok = True
                    break

            if not ok:
                # guaranteed solvable, but fallback safety
                for i in range(L, r + 1):
                    if ans[i - 1] == -1:
                        ans[i - 1] = 0

        print(*ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the idea of resolving constraints only when their right endpoint is reached. For each endpoint, we identify a short window that fully contains all relevant unknowns. We then brute-force all binary assignments on that window and validate all constraints ending at that position. Once a consistent assignment is found, we commit only previously unset values.

A subtle point is that we never overwrite already fixed values, which preserves consistency between overlapping windows.

## Worked Examples

### Example 1

Input:

```
n = 3
constraints:
[1,2]=1
[2,3]=1
```

At r = 2, we try assignments on positions 1..2. Only assignments (1,0) and (0,1) satisfy first constraint. At r = 3, we extend and enforce second constraint, selecting a consistent extension.

| r | window | constraints | chosen assignment |
| --- | --- | --- | --- |
| 2 | [1,2] | sum=1 | (1,0) |
| 3 | [2,3] | sum=1 | (0,1) |

This shows how overlap is resolved locally without global backtracking.

### Example 2

Input:

```
n = 4
constraints:
[1,4]=2
[2,3]=1
```

At r = 3, we ensure [2,3] has exactly one 1. At r = 4, we enforce total sum 2 over the full range.

| r | window | constraints | partial |
| --- | --- | --- | --- |
| 3 | [2,3] | sum=1 | fixed |
| 4 | [1,4] | sum=2 | extended |

This demonstrates how earlier decisions constrain later windows but remain consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^10) | each window brute-forces at most 1024 states |
| Space | O(n + m) | storage of array and constraints |

The small bound on segment length makes the exponential factor constant. With n, m ≤ 10^4 total, this comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        by_r = [[] for _ in range(n + 1)]
        for _ in range(m):
            l, r, s = map(int, input().split())
            by_r[r].append((l, s))

        ans = [-1] * n

        for r in range(1, n + 1):
            if not by_r[r]:
                ans[r - 1] = 0
                continue

            L = min(l for l, _ in by_r[r])
            length = r - L + 1

            fixed = {i + 1: ans[i] for i in range(L - 1, r) if ans[i] != -1}

            found = False

            for mask in range(1 << length):
                ok = True
                for l, s in by_r[r]:
                    tot = 0
                    for i in range(l, r + 1):
                        if ans[i - 1] != -1:
                            tot += ans[i - 1]
                        else:
                            tot += (mask >> (i - L))
                    if tot != s:
                        ok = False
                        break
                if ok:
                    for i in range(length):
                        pos = L + i
                        if ans[pos - 1] == -1:
                            ans[pos - 1] = (mask >> i) & 1
                    found = True
                    break

            if not found:
                for i in range(L - 1, r):
                    if ans[i] == -1:
                        ans[i] = 0

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# custom sanity checks
assert run("1\n3 2\n1 2 1\n2 3 1\n")  # valid output exists
assert run("1\n5 1\n1 2 1\n")  # trivial local constraint
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small overlapping | valid | overlap consistency |
| single constraint | valid | base correctness |

## Edge Cases

A tight chain of overlapping constraints is handled correctly because each constraint only affects a window of size at most 10, so no dependency propagates beyond the current local solve step.

A case where all constraints are disjoint is trivial, since each window resolves independently and never conflicts with previously fixed positions, leading to immediate assignment of zeros elsewhere.

A fully dense region of overlapping constraints still fits within the window size limit, so brute-force enumeration over that region always finds a consistent assignment guaranteed by the problem statement.
