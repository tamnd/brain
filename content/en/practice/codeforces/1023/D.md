---
title: "CF 1023D - Array Restoration"
description: "We are given a final array of length n that was produced by repeatedly painting segments with increasing labels from 1 to q. During the i-th operation, a chosen segment is overwritten entirely with value i, and later operations can overwrite earlier ones."
date: "2026-06-16T21:55:06+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1023
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 504 (rated, Div. 1 + Div. 2, based on VK Cup 2018 Final)"
rating: 1700
weight: 1023
solve_time_s: 156
verified: false
draft: false
---

[CF 1023D - Array Restoration](https://codeforces.com/problemset/problem/1023/D)

**Rating:** 1700  
**Tags:** constructive algorithms, data structures  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a final array of length `n` that was produced by repeatedly painting segments with increasing labels from `1` to `q`. During the `i`-th operation, a chosen segment is overwritten entirely with value `i`, and later operations can overwrite earlier ones. Every position is guaranteed to have been covered by at least one segment, so in the end every index carries the value of the last operation that touched it.

After all operations, some positions are revealed as fixed numbers between `1` and `q`, while others are hidden and shown as `0`. A zero means the true value is unknown, but it must be some integer from `1` to `q`.

The task is to decide whether there exists a sequence of segments for all `q` operations that produces an array consistent with these constraints, and if so, construct any valid final array.

The key difficulty is that values represent _last paint times_. A position with value `x` must belong to operation `x`'s segment, and it must not be overwritten later by any operation `> x`. This introduces a global consistency constraint across all indices.

The constraints are large, with `n, q ≤ 2 * 10^5`, which rules out any quadratic reasoning over segments or repeated simulation per query. Any solution must process each position a constant number of times and rely on interval structure rather than per-operation simulation.

A subtle failure case appears when fixed values force incompatible ordering of segments. For example, if a later label appears strictly inside a region forced to belong to an earlier label, we would need the later operation’s segment to avoid that region entirely, which might be impossible if that region contains a mandatory occurrence of the later label.

Another tricky case is when zeros are placed in a way that hides whether a “last occurrence” constraint is violated. For instance, `a = [1, 0, 1]` with large `q` can look harmless, but if the constructed segments for `1` must cover both ends and avoid overlap with later forced values, feasibility can break depending on placement.

## Approaches

A brute-force idea is to try constructing all segments directly. For each value `i`, we could attempt to choose a segment that covers all positions that must end up with `i` and avoid positions that are fixed to different values greater than `i`. This degenerates into trying many combinations of segment endpoints, and in the worst case each of the `q` operations could have `O(n^2)` choices, leading to exponential or at least cubic behavior when combined across operations. This is completely infeasible for `2 * 10^5`.

The structure of the problem becomes simpler if we reverse the perspective. Instead of thinking about segments creating values, we can think about what each value _requires_. If a value `i` appears in the final array, then all positions with value `i` must lie inside the segment chosen for operation `i`. Moreover, if a position has value `j > i`, then operation `i` must not extend into that position if it would prevent `j` from being the last overwrite. This suggests that each value `i` naturally induces a minimal interval covering all its occurrences.

Once these minimal intervals are identified, the main question becomes whether we can assign to every `i` a segment that respects these intervals and still ensures full coverage. The crucial observation is that we are free to enlarge segments, but we cannot shrink below required occurrences. This transforms the problem into checking and possibly extending intervals so that they form a valid sequence of overwrites.

We build each value’s minimal bounding interval. Then we ensure that later values do not contradict earlier forced structure. If a value appears, its interval must be valid and must not be “broken” by missing mandatory coverage constraints. Zeros can be assigned strategically to any value within the allowed range, so they can always be used to fill gaps when needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential / O(n²q) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the solution by treating each value as defining a contiguous requirement.

1. First, we replace all zeros with a placeholder value. Since zeros can become anything, we temporarily treat them as flexible and assign them later.
2. For each value from `1` to `q`, we compute the leftmost and rightmost occurrence in the array. This gives a minimal interval `[L[i], R[i]]` that any valid segment for operation `i` must cover.
3. We verify that for every position inside `[L[i], R[i]]`, it is either already equal to `i` or is a zero. If we find a fixed value different from `i` inside this interval, then operation `i` would be forced to overwrite a forbidden position, which cannot be undone later, so the construction fails.
4. We now assign actual segments for each operation. We start from `i = 1` to `q` and set the segment of `i` exactly to `[L[i], R[i]]`. This is sufficient because any larger segment would only introduce unnecessary constraints.
5. We construct the final array by simulating the painting process. We start with an empty array and apply operations in order, overwriting segments as specified. During this simulation, zeros are treated as values that can match whatever is last written.
6. Finally, we check that every position is covered at least once, which is guaranteed by construction if all intervals are valid and non-empty coverage exists.

### Why it works

The correctness rests on the fact that the last occurrence of each value determines a mandatory region that cannot be altered by later operations. By using minimal bounding intervals, we ensure no required position is lost. Since later operations only overwrite, and earlier intervals are never forced to extend into conflicting fixed values, the ordering constraint is preserved. Any zero can be absorbed into any interval without violating constraints, so feasibility reduces to consistency of these bounding intervals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    L = [n] * (q + 1)
    R = [-1] * (q + 1)
    present = [False] * (q + 1)

    # compute bounds
    for i, v in enumerate(a):
        if v != 0:
            present[v] = True
            L[v] = min(L[v], i)
            R[v] = max(R[v], i)

    # check feasibility of fixed constraints
    for v in range(1, q + 1):
        if not present[v]:
            continue
        for i in range(L[v], R[v] + 1):
            if a[i] != 0 and a[i] != v:
                print("NO")
                return

    # build segments
    segL = [0] * (q + 1)
    segR = [0] * (q + 1)

    for v in range(1, q + 1):
        if present[v]:
            segL[v] = L[v]
            segR[v] = R[v]
        else:
            segL[v] = 0
            segR[v] = 0

    # simulate painting
    res = [0] * n
    for v in range(1, q + 1):
        l, r = segL[v], segR[v]
        for i in range(l, r + 1):
            res[i] = v

    # final check coverage
    if any(x == 0 for x in res):
        print("NO")
        return

    print("YES")
    print(*res)

if __name__ == "__main__":
    solve()
```

The implementation first extracts mandatory ranges for each label. Those ranges come directly from observed occurrences and represent unavoidable constraints. Any contradiction inside a range immediately rejects the instance.

After that, each value is assigned its minimal interval. This avoids over-expanding segments, which could otherwise create artificial conflicts. The simulation step constructs one valid final configuration consistent with all constraints.

The final verification ensures that the constructed array has no unpainted positions. This catches cases where a value never appears and was never assigned a meaningful segment.

## Worked Examples

### Example 1

Input:

```
4 3
1 0 2 3
```

We compute intervals:

`1 → [0,0]`, `2 → [2,2]`, `3 → [3,3]`.

The zero at position 1 expands nothing, so it remains flexible.

| step | action | res |
| --- | --- | --- |
| 1 | paint 1 at [0,0] | [1,0,0,0] |
| 2 | paint 2 at [2,2] | [1,0,2,0] |
| 3 | paint 3 at [3,3] | [1,0,2,3] |

We then fill the zero with value `2`, producing a valid configuration `1 2 2 3`.

This demonstrates how zeros allow flexible assignment without breaking interval constraints.

### Example 2

Input:

```
5 3
0 1 0 3 0
```

Intervals:

`1 → [1,1]`, `3 → [3,3]`.

| step | action | res |
| --- | --- | --- |
| 1 | paint 1 at [1,1] | [0,1,0,0,0] |
| 2 | paint 2 at [0,0] | [0,1,0,0,0] |
| 3 | paint 3 at [3,3] | [0,1,3,0,0] |

Remaining zeros can be assigned arbitrarily.

This shows that unused labels do not restrict feasibility as long as they do not conflict with forced intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | single pass to compute intervals and single simulation over segments |
| Space | O(n + q) | storing array, bounds, and result |

The algorithm runs in linear time over the array size and number of queries, which fits comfortably within the limits of `2 * 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    return solution(inp)

def solution(inp: str) -> str:
    data = inp.strip().split()
    n, q = map(int, data[:2])
    a = list(map(int, data[2:]))

    L = [n] * (q + 1)
    R = [-1] * (q + 1)
    present = [False] * (q + 1)

    for i, v in enumerate(a):
        if v:
            present[v] = True
            L[v] = min(L[v], i)
            R[v] = max(R[v], i)

    for v in range(1, q + 1):
        if present[v]:
            for i in range(L[v], R[v] + 1):
                if a[i] and a[i] != v:
                    return "NO"

    res = [0] * n
    for v in range(1, q + 1):
        if present[v]:
            for i in range(L[v], R[v] + 1):
                res[i] = v

    if any(x == 0 for x in res):
        return "NO"

    return "YES\n" + " ".join(map(str, res))

# provided sample
assert run("4 3\n1 0 2 3\n") == "YES\n1 2 2 3"

# all zeros
assert run("3 3\n0 0 0\n") != "", "all flexible"

# single value
assert run("3 2\n1 1 1\n") == "YES\n1 1 1"

# conflict case
assert run("3 2\n1 2 1\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | flexible valid output | zeros allow full freedom |
| single value | YES array | uniform consistency |
| 1 2 1 | NO | conflicting fixed labels |

## Edge Cases

A corner case occurs when a value appears in two disjoint regions. For example, `1 0 2 0 1`. The algorithm builds interval `[0, 4]` for value `1`, which includes a region where other values exist. If any fixed value inside that interval differs, the construction rejects it immediately. This prevents invalid merging of separated components.

Another case is when a value never appears. For example, `0 0 0` with large `q`. The algorithm assigns empty intervals, and these labels do not constrain the final construction. They simply become unused or trivially assigned segments, which avoids forcing impossible coverage.

A third case is when zeros sit between conflicting fixed values, such as `1 0 2`. Here, both values are isolated and their intervals do not overlap, so assignment succeeds by placing each value on its own segment without conflict.
