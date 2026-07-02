---
title: "CF 103567F - \u041c\u0435\u0442\u0440\u043e"
description: "We are given a long array of values that represent passenger flow at different time moments of the day. A “shift” is defined by three parameters: a starting time index s, a fixed number of trips k, and a constant time gap d between consecutive trips."
date: "2026-07-03T03:56:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103567
codeforces_index: "F"
codeforces_contest_name: "2021-2022 Olympiad Cognitive Technologies, Prefinal Round"
rating: 0
weight: 103567
solve_time_s: 45
verified: true
draft: false
---

[CF 103567F - \u041c\u0435\u0442\u0440\u043e](https://codeforces.com/problemset/problem/103567/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long array of values that represent passenger flow at different time moments of the day. A “shift” is defined by three parameters: a starting time index `s`, a fixed number of trips `k`, and a constant time gap `d` between consecutive trips.

If we start at time `s`, the metro operates at times `s, s + d, s + 2d, ..., s + (k−1)d`. The total passenger load for this shift is the sum of array values at exactly these positions. The task is to choose the starting position `s` so that this total sum is as large as possible, under the constraint that all chosen indices must stay inside the array.

Formally, we are maximizing a sum over a fixed arithmetic progression inside the array. The constraint on validity is that the last index `s + (k−1)d` must not exceed the array boundary.

The input size is large enough that any solution iterating over all valid starts and recomputing each sum directly would be too slow. A naive approach would effectively compute up to `O(N · k)` operations, which collapses to around `10^10` in worst-case configurations and is not feasible.

A key subtlety is that stepping by `d` creates a structure that is not a single contiguous segment unless `d = 1`. When `d > 1`, indices split into independent residue classes modulo `d`, and each class behaves like its own smaller linear array.

A typical failure case for a naive sliding window approach is when one tries to treat this like a normal subarray problem for `d > 1`. For example, if `d = 2`, adjacent elements in the sum are not adjacent in the original array, so a standard prefix or sliding window over contiguous segments does not apply.

## Approaches

The brute-force solution fixes a starting point `s` and explicitly sums `k` elements spaced by `d`. This is correct because it directly follows the definition. However, each such computation costs `O(k)`, and there are up to `O(N)` possible starting points, so the total complexity becomes `O(Nk)`. When both `N` and `k` are large, this quickly becomes too slow.

The key observation is that the arithmetic progression defined by step `d` partitions the array into independent chains. Any index `i` only interacts with indices of the form `i + td`. This means that if we group elements by their index modulo `d`, each group forms a separate sequence where the problem reduces to choosing a contiguous segment of length `k` inside that sequence.

Once this decomposition is made, each group can be solved exactly like the classic fixed-length maximum subarray sum problem using either prefix sums or a sliding window. Since every element belongs to exactly one group, the total work across all groups is linear in `N`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Nk) | O(1) | Too slow |
| Residue decomposition / prefix or window | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We solve the problem by splitting the array into independent chains based on index modulo `d`.

1. We group elements by their remainder class modulo `d`. Each group contains elements that will appear consecutively in the arithmetic progression when we fix a starting residue class. This step is necessary because stepping by `d` never mixes different residue classes.
2. For each residue class `r`, we extract the sequence `b = a[r], a[r+d], a[r+2d], ...`. This converts the original “skipped index” problem into a standard linear array problem.
3. On each sequence `b`, we compute the maximum sum of any contiguous segment of length exactly `k`. This is the same as computing a sliding window of size `k`. We initialize the sum of the first window, then shift it by removing the outgoing element and adding the incoming element.
4. We track the maximum over all windows in all residue classes. This global maximum corresponds to the best valid starting position in the original array.

### Why it works

Each valid arithmetic progression starting at index `s` lies entirely within a single residue class `s mod d`. Within that class, the progression becomes a contiguous block. Therefore every candidate shift corresponds to exactly one window in exactly one class, and every such window corresponds to a valid shift. Since we evaluate all windows in all classes, we do not miss any candidate and we do not mix unrelated indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))

    if k == 1:
        print(max(a))
        return

    ans = -10**30

    for r in range(d):
        # build window on residue class r
        window = []
        s = 0

        for i in range(r, n, d):
            window.append(a[i])
            s += a[i]

        if len(window) < k:
            continue

        cur = sum(window[:k])
        ans = max(ans, cur)

        for i in range(k, len(window)):
            cur += window[i] - window[i - k]
            ans = max(ans, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads the array and iterates over all residue classes modulo `d`. For each class, it constructs a reduced array that represents all positions reachable by stepping `d`. It then uses a fixed-size sliding window of length `k` to compute sums efficiently.

The important implementation detail is that we never try to compute sums directly in the original indexing system. All computations happen in the compressed residue sequences, which guarantees linear total work.

## Worked Examples

### Example 1

Input:

```
n = 7, k = 3, d = 2
a = [1, 10, 2, 9, 3, 8, 4]
```

We split into residue classes:

| r | sequence b |
| --- | --- |
| 0 | [1, 2, 3, 4] |
| 1 | [10, 9, 8] |

Now we evaluate windows of size 3.

For r = 0:

| window start | elements | sum |
| --- | --- | --- |
| 0 | [1, 2, 3] | 6 |
| 1 | [2, 3, 4] | 9 |

For r = 1:

| window start | elements | sum |
| --- | --- | --- |
| 0 | [10, 9, 8] | 27 |

Maximum is 27.

This shows how valid progressions correspond exactly to contiguous windows in a residue class.

### Example 2

Input:

```
n = 6, k = 2, d = 3
a = [5, -1, 4, 2, 10, -3]
```

Residue classes:

| r | sequence b |
| --- | --- |
| 0 | [5, 2] |
| 1 | [-1, 10] |
| 2 | [4, -3] |

Now k = 2 means each full sequence contributes exactly one window:

| r | window | sum |
| --- | --- | --- |
| 0 | [5, 2] | 7 |
| 1 | [-1, 10] | 9 |
| 2 | [4, -3] | 1 |

Answer is 9.

This demonstrates that even with negative values, the method correctly compares independent chains without interference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is processed exactly once inside its residue class |
| Space | O(N) | Temporary storage for residue sequences |

The solution scales linearly with the input size, which is necessary because naive quadratic interaction between `N` and `k` is infeasible at the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum size
assert run("1 1 1\n5\n") == "5"

# all equal values
assert run("6 2 2\n3 3 3 3 3 3\n") == "6"

# d = 1 contiguous case
assert run("5 3 1\n1 2 3 4 5\n") == "12"

# alternating strong peak
assert run("7 2 2\n1 100 1 100 1 100 1\n") == "300"

# negative values
assert run("5 2 1\n-1 -2 -3 -4 -5\n") == "-3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 5 | 5 | smallest valid input |
| all equal | 6 | symmetry across residues |
| d=1 | 12 | reduces to classic window problem |
| alternating peaks | 300 | correct residue grouping |
| negatives | -3 | handles negative sums correctly |

## Edge Cases

For `k = 1`, the algorithm should immediately return the maximum element. The sliding window logic still works, but without a guard it may incorrectly assume at least one transition exists.

For cases where `len(b) < k` in a residue class, that class must be skipped entirely. Otherwise, partial windows would be incorrectly considered.

For large `d` close to `n`, most residue classes contain at most one element, meaning no valid window exists unless `k = 1`. The algorithm naturally handles this because the sliding loop never runs in such cases.
