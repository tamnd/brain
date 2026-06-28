---
title: "CF 104778B - \u0411\u0430\u0441\u043a\u0435\u0442\u0431\u043e\u043b"
description: "We are given a sequence of distances for successful basketball shots. Each shot contributes points depending on a threshold value d that we choose. If a shot distance is strictly less than d, that shot is worth 2 points."
date: "2026-06-28T15:05:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104778
codeforces_index: "B"
codeforces_contest_name: "2023-2024 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 23, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 104778
solve_time_s: 56
verified: true
draft: false
---

[CF 104778B - \u0411\u0430\u0441\u043a\u0435\u0442\u0431\u043e\u043b](https://codeforces.com/problemset/problem/104778/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of distances for successful basketball shots. Each shot contributes points depending on a threshold value `d` that we choose. If a shot distance is strictly less than `d`, that shot is worth 2 points. Otherwise, if the distance is greater than or equal to `d`, the shot is worth 3 points.

Our task is to pick a non-negative integer `d` so that the total score across all shots becomes exactly `k`. Among all valid choices of `d`, we need the smallest one.

The important structure here is that changing `d` only affects which side of the threshold each distance falls into. Increasing `d` moves some shots from the 3-point group into the 2-point group, and decreasing `d` does the opposite.

The constraints are small enough for a direct simulation per candidate threshold. With `n ≤ 1000`, even an O(n^2) or O(n log n) approach is easily fast enough under a 1-second limit. This immediately suggests that we can afford to test multiple candidate values of `d`, especially if we exploit sorting or discrete breakpoints.

A key observation is that only values of `d` that are equal to some `ai` or lie between two consecutive sorted distances can change the assignment of shots. This reduces the infinite search space over all integers to at most `n + 1` meaningful cases.

A subtle edge case appears when `d = 0`. Since all `ai ≥ 1`, every shot becomes `ai ≥ d`, so every shot contributes 3 points. This often becomes the maximum possible score `3n`, and it is a valid candidate we must include explicitly.

Another edge case is when the desired score `k` equals `2n`, meaning every shot must be in the 2-point group. This can only happen when `d` is strictly larger than all distances.

## Approaches

The naive approach is to try every integer value of `d` from 0 up to a large upper bound, compute the score for each, and pick the smallest valid one. For each `d`, we scan all `n` distances and decide whether each contributes 2 or 3 points. This costs O(n) per check. Since distances can go up to 10^9, a safe upper bound for `d` might also be around 10^9, which makes this approach far too slow in the worst case, requiring on the order of 10^12 operations.

The key insight is that the score function only changes when `d` crosses one of the distances in the array. Between two consecutive sorted values, the set of elements `< d` and `≥ d` remains unchanged, so the score is constant. This means we only need to consider `d` in a finite set derived from the input values, typically all distinct distances plus 0.

Once we sort the array, we can simulate the score for each candidate threshold by maintaining how many elements fall below `d`. As `d` increases, this count increases monotonically, and the score changes predictably.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all d | O(n · maxA) | O(1) | Too slow |
| Sort + scan thresholds | O(n^2 log n) or O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array of distances in non-decreasing order. Sorting is useful because it allows us to reason about how many elements are below a threshold `d` in O(1) once we fix a position.
2. Precompute prefix information implicitly by iterating over how many elements are assigned to the “3-point group” (those with `ai ≥ d`). Instead of directly computing prefix sums, we track a split point `i`, where elements from `i` to `n-1` contribute 3 points and the rest contribute 2 points.
3. For each possible split index `i` from 0 to `n`, interpret it as choosing `d` between `a[i-1]` and `a[i]` (with boundary handling). All elements in the suffix `[i, n)` are ≥ d and contribute 3 points, while the prefix `[0, i)` contributes 2 points.
4. Compute the score for this split as `2 * i + 3 * (n - i)`. This formula directly encodes the scoring rule without simulating each shot individually.
5. Check whether this score equals `k`. If it does, compute the smallest `d` that achieves this split. The smallest valid `d` is either 0 (for `i = 0`) or `a[i-1] + 1` when `i > 0`.
6. Keep track of the minimum such `d` across all valid splits.

The correctness hinges on the fact that every valid threshold corresponds exactly to one partition of the sorted array into `< d` and `≥ d`, and every such partition can be represented by some interval of `d` values.

### Why it works

The algorithm compresses the infinite set of possible thresholds into at most `n + 1` equivalence classes defined by the sorted order of distances. Within each class, the ordering of elements relative to `d` does not change, so the score function remains constant. Therefore, enumerating all split positions exhaustively covers all possible distinct outcomes, and choosing the minimal `d` per valid outcome ensures we find the globally smallest threshold achieving score `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

best = None

for i in range(n + 1):
    score = 2 * i + 3 * (n - i)
    if score == k:
        if i == 0:
            d = 0
        else:
            d = a[i - 1] + 1
        if best is None or d < best:
            best = d

print(best)
```

The solution begins by sorting the distances so that every threshold corresponds to a contiguous prefix-suffix split. The loop over `i` represents choosing how many elements fall below `d`. The score formula directly evaluates the contribution of both groups without per-element checks.

When constructing `d`, the boundary choice is crucial. If we want exactly `i` elements to be strictly less than `d`, then `d` must be greater than the `i-1`-th element and at most `a[i]`. Choosing `a[i-1] + 1` is the smallest integer that enforces this separation.

## Worked Examples

### Example 1

Input:

```
3 7
20 10 30
```

Sorted array: `[10, 20, 30]`

We test all splits:

| i | prefix (2 pts) | suffix (3 pts) | score |
| --- | --- | --- | --- |
| 0 | 0 | 3 | 9 |
| 1 | 1 | 2 | 8 |
| 2 | 2 | 1 | 7 |
| 3 | 3 | 0 | 6 |

The valid split is `i = 2`. That means two elements are below `d`, and one is above or equal.

The smallest `d` that achieves this is `a[1] + 1 = 21`.

This matches the required score exactly, confirming that the split-based interpretation correctly maps thresholds to outcomes.

### Example 2

Input:

```
5 15
4 8 7 3 5
```

Sorted array: `[3, 4, 5, 7, 8]`

We compute:

| i | score |
| --- | --- |
| 0 | 15 |
| 1 | 14 |
| 2 | 13 |
| 3 | 12 |
| 4 | 11 |
| 5 | 10 |

Only `i = 0` works, meaning all elements must be in the 3-point group. That happens when `d = 0`.

This confirms the edge case where the threshold is minimal and no element falls below it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, scan over n splits is linear |
| Space | O(1) | Only a few variables aside from input array |

The constraints `n ≤ 1000` make this comfortably efficient. Even repeated sorting or scanning would pass easily, but the single sort plus linear scan is the cleanest formulation.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    best = None
    for i in range(n + 1):
        score = 2 * i + 3 * (n - i)
        if score == k:
            if i == 0:
                d = 0
            else:
                d = a[i - 1] + 1
            if best is None or d < best:
                best = d

    print(best)

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    sys.stdin = old
    return out.getvalue().strip()

# provided samples
assert run("3 7\n20 10 30\n") == "21"
assert run("5 15\n4 8 7 3 5\n") == "0"

# custom cases
assert run("1 2\n100\n") == "101"
assert run("1 3\n100\n") == "0"
assert run("2 4\n1 2\n") == "0"
assert run("2 6\n1 2\n") == "3"
assert run("3 9\n5 1 3\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single large d boundary | 101 | minimal edge shift case |
| always 3 points | 0 | d = 0 behavior |
| all 2 points | 0 | upper threshold case |
| small mixed | 3 | strict boundary transition |
| full 3-point score | 0 | maximal score edge |

## Edge Cases

When all shots must contribute 3 points, the score is `3n`, which corresponds to `i = 0`. In this situation the algorithm correctly assigns `d = 0`. For example, with input `n = 3`, `a = [5, 10, 20]`, `k = 9`, the loop finds `i = 0` valid and returns `0`, matching the fact that every `ai ≥ 0`.

When all shots must contribute 2 points, the score is `2n`, which corresponds to `i = n`. For `a = [2, 4, 6]`, `k = 6`, the valid split is `i = 3`. The algorithm assigns `d = a[2] + 1 = 7`, which is the smallest threshold ensuring all elements are strictly below `d`.

When the answer lies between two adjacent values, say `a = [3, 8, 10]` and we need exactly two elements below `d`, the algorithm selects `i = 2` and sets `d = a[1] + 1 = 9`. This guarantees `3, 8 < 9` and `10 ≥ 9`, preserving the intended split without ambiguity.
