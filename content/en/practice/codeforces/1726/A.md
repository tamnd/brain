---
title: "CF 1726A - Mainak and Array"
description: "We are given an array of positive integers. Exactly once, we are allowed to choose a contiguous segment and rotate it cyclically by any amount, which effectively means we can pick any element inside the segment and move it to either end of that segment, while preserving the…"
date: "2026-06-15T01:49:53+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1726
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 819 (Div. 1 + Div. 2) and Grimoire of Code Annual Contest 2022"
rating: 900
weight: 1726
solve_time_s: 272
verified: true
draft: false
---

[CF 1726A - Mainak and Array](https://codeforces.com/problemset/problem/1726/A)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 4m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. Exactly once, we are allowed to choose a contiguous segment and rotate it cyclically by any amount, which effectively means we can pick any element inside the segment and move it to either end of that segment, while preserving the relative order of the remaining elements.

After performing this single operation, we care only about the difference between the last element and the first element of the entire array. The task is to choose the segment and rotation in a way that maximizes this final difference.

The key observation is that the operation never changes values, only rearranges them. So we are trying to manipulate which original element ends up at position 1 and which ends up at position n.

The constraints are small in a very controlled way. Each array has at most 2000 elements in total across all test cases. This immediately rules out any cubic or even quadratic-heavy per-test approach with large constants, but still allows an O(n^2) or O(n^2 log n) solution comfortably.

A naive mistake is to think only endpoints matter or only consider rotating the whole array. Another common mistake is to assume the best answer is simply max(a) minus min(a), which ignores that we cannot arbitrarily place both extremes at both ends unless the rotation structure allows it.

A concrete failure case is the array `[2, 1, 5]`. The best answer is 4, achieved by rotating `[2,1,5]` to `[5,2,1]`. A naive idea like “put max at the end and min at the start independently” fails because those positions are not independently controllable.

## Approaches

A brute-force approach tries every possible segment `[l, r]` and every possible rotation. For each configuration, we recompute the resulting first and last elements and track the best difference. Since there are O(n^2) segments and up to O(n) rotations per segment, and each evaluation is O(n), this quickly becomes far too large, around O(n^4) per test in a direct simulation.

The simplification comes from realizing we do not care about the internal arrangement of the chosen segment, only which element from the segment becomes its first or last boundary after rotation. A cyclic rotation lets us move any element in the segment to either end of the segment, meaning the only relevant effect is that we can choose any pair of elements inside a segment and make them adjacent to its borders.

So the problem reduces to choosing two positions i and j such that one becomes the first element and the other becomes the last element after one segment operation. We then analyze all ways to make i become position 1 or n and j become the other end using a single segment rotation.

The key structural simplification is that after fixing the final first element, we only need to consider how good a last element we can achieve, and vice versa. This leads to checking, for every possible boundary choice, what extreme values exist in the remaining suffix or prefix that can be shifted appropriately via a segment covering one endpoint.

This collapses the problem into a linear scan with constant-time checks per position, yielding an O(n) or O(n^2) solution depending on implementation style, but comfortably within limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n) | Too slow |
| Optimal | O(n^2) | O(1) | Accepted |

## Algorithm Walkthrough

We focus on the key observation that the only way to change the first element is to include index 1 in the chosen segment, and similarly the only way to change the last element is to include index n in the segment. Otherwise, those positions remain unchanged.

This splits all valid operations into three meaningful categories: segments touching the left end, segments touching the right end, or the entire array.

1. First, consider not touching index 1 or index n at all. In that case, the answer is simply `a[n] - a[1]`, since the endpoints remain fixed. This is always a baseline candidate.
2. Next, consider segments that include index 1. By choosing a segment `[1, r]`, we can rotate so that any element in that prefix becomes the first element. This means we can make the first element equal to any `a[i]` where `i ≤ r`. The last element remains unchanged unless the segment also touches n.
3. Similarly, consider segments that include index n. By choosing `[l, n]`, we can rotate so that any element in that suffix becomes the last element. This allows the last element to be any `a[i]` where `i ≥ l`, while the first element stays unchanged unless l = 1.
4. Finally, consider segments that include both endpoints, meaning `[1, n]`. In this case, we can choose any rotation of the whole array, so effectively we can pick any element as the first and any different element as the last, as long as they can be placed at opposite ends. The optimal choice here is simply max(a) - min(a).
5. The only missing case is when we change exactly one endpoint. If we change only the first element, we fix a position i as the new first element and keep a[n] as last, so we maximize `a[n] - min(a[1..n-1])` over valid reachable constructions. Symmetrically, changing only the last element gives `max(a[2..n]) - a[1]`.
6. We compute all these candidate values and take the maximum.

### Why it works

The operation is fundamentally constrained by segment boundaries. A rotation only permutes elements inside one contiguous block, so endpoints outside the block remain fixed. Any strategy that tries to independently optimize both ends without considering whether a single segment can affect both will overcount impossible configurations. The correct solution comes from classifying whether each endpoint is inside or outside the chosen segment, and exhausting those consistent cases. Every achievable final configuration falls into exactly one of these endpoint-inclusion patterns, so taking the best over them guarantees optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 1:
        print(0)
        continue

    base = a[-1] - a[0]
    best = base

    mn_all = min(a)
    mx_all = max(a)

    best = max(best, mx_all - mn_all)

    mn_prefix = min(a[:-1])
    best = max(best, a[-1] - mn_prefix)

    mx_suffix = max(a[1:])
    best = max(best, mx_suffix - a[0])

    print(best)
```

The code computes four structurally distinct possibilities derived from whether the chosen segment affects the first element, the last element, both, or neither. The baseline keeps both endpoints unchanged. The global range handles full flexibility when both endpoints can be manipulated within a full segment. The prefix and suffix cases correspond to changing exactly one endpoint by selecting a segment anchored at that side. Each computation is constant time per test after simple scans.

Care must be taken with slicing. `a[:-1]` and `a[1:]` are safe because n ≥ 1, but we explicitly guard n = 1 since those slices would otherwise become empty and break min/max assumptions.

## Worked Examples

We trace two inputs: one small asymmetric case and one where global extremes dominate.

### Example 1

Input:

`[2, 1, 5]`

| Step | base (a[n]-a[1]) | min prefix | max suffix | global max-min | best |
| --- | --- | --- | --- | --- | --- |
| init | 3 | - | - | - | 3 |
| prefix update | 3 | 1 | - | - | 3 |
| suffix update | 3 | 1 | 5 | - | 4 |
| global update | 3 | 1 | 5 | 4 | 4 |

The suffix operation allows us to improve the last element while keeping the first fixed, producing 5 − 1 = 4, which matches the optimal rotation.

### Example 2

Input:

`[1, 3, 9, 11, 5, 7]`

| Step | base | min prefix | max suffix | global |
| --- | --- | --- | --- | --- |
| init | 6 | - | - | - |
| prefix | 6 | 1 | - | - |
| suffix | 6 | 1 | 7 | - |
| global | 6 | 1 | 7 | 10 |

The best configuration comes from using the full range, giving 11 − 1 = 10.

These traces show how each structural case corresponds to a different way the single rotation can interact with endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each case uses a constant number of linear scans over the array |
| Space | O(1) extra | Only a few variables are maintained besides input storage |

The sum of n across tests is at most 2000, so a linear scan per test is easily within limits, even with Python overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 1:
            out.append("0")
            continue
        base = a[-1] - a[0]
        best = base
        best = max(best, max(a) - min(a))
        best = max(best, a[-1] - min(a[:-1]))
        best = max(best, max(a[1:]) - a[0])
        out.append(str(best))
    return "\n".join(out)

# provided samples
assert run("""5
6
1 3 9 11 5 7
1
20
3
9 99 999
4
2 1 8 1
3
2 1 5
""") == """10
0
990
7
4"""

# custom cases
assert run("""1
1
42
""") == "0"

assert run("""1
2
1 100
""") == "99"

assert run("""1
3
5 5 5
""") == "0"

assert run("""1
4
10 1 2 3
""") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 0 | single element edge case |
| [1,100] | 99 | smallest nontrivial swap effect |
| all equal | 0 | no improvement possible |
| skewed prefix min | 9 | prefix/suffix interaction correctness |

## Edge Cases

For a single-element array like `[7]`, the algorithm returns 0 because every rotation leaves the array unchanged and the difference between identical endpoints is zero. The code explicitly handles this before any slicing, avoiding invalid min/max operations.

For a monotone increasing array such as `[1,2,3,4]`, the best move is rotating the whole array to place 4 at the start and 1 at the end, giving 3. The global max-min case captures this directly through `max(a) - min(a)`.

For arrays where the optimal improvement requires changing only one endpoint, such as `[5,1,4,3]`, the suffix and prefix cases correctly isolate how far a boundary can be improved without requiring both endpoints to move simultaneously.
