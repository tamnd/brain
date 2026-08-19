---
title: "CF 102215E - Third-Party Software - 2"
description: "We have (n) library versions. Version (i) provides every function whose number lies in the inclusive interval ([ai,bi]). Pavel needs every function from (1) through (m), so the chosen versions must collectively cover the entire interval ([1,m]). The task has two parts."
date: "2026-08-20T02:46:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "E"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 384
verified: false
draft: false
---

[CF 102215E - Third-Party Software - 2](https://codeforces.com/problemset/problem/102215/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have (n) library versions. Version (i) provides every function whose number lies in the inclusive interval ([a_i,b_i]). Pavel needs every function from (1) through (m), so the chosen versions must collectively cover the entire interval ([1,m]).

The task has two parts. First, we must determine whether such a collection of versions exists. If it does, we must find the smallest possible number of versions and output their indices. The intervals may overlap, and a version can be used only once.

The value of (m) can be as large as (10^9), so treating every function number as a separate array position is not viable. The number of intervals is at most (2\cdot10^5), which means an (O(n^2)) algorithm would already require around (4\cdot10^{10}) interval operations in the worst case. With a 2-second limit, we need something close to (O(n\log n)) or (O(n)). Sorting the intervals once is acceptable, while repeatedly comparing every pair is not.

There are several boundary cases that can make an otherwise plausible solution fail. If the first useful interval does not start at function (1), the answer is immediately impossible. For example,

```
2 5
2 5
3 5
```

has no version containing function (1), so the answer is `NO`. A solution that merely checks whether the largest right endpoint reaches (m) would incorrectly accept it.

A second case is a gap in the middle:

```
3 8
1 3
4 5
7 8
```

The intervals cover (1) through (5), then leave function (6) uncovered. The correct output is `NO`. Checking only the union's minimum and maximum endpoints is insufficient because disconnected intervals cannot cover the gap.

Another subtle case is overlapping intervals where taking the first available interval is not optimal:

```
3 8
1 3
1 5
5 8
```

The optimal answer uses versions (2) and (3), covering ([1,5]) and then ([5,8]). Choosing version (1) first leads to a shorter prefix and requires an additional version. A greedy algorithm must choose the interval that extends the covered prefix farthest, not simply the first interval that can continue it.

Finally, when one interval already covers everything, the answer must contain exactly one version:

```
1 10
1 10
```

The correct result is `YES`, followed by `1` and version `1`. An algorithm that insists on finding a second interval after reaching (m) would introduce an unnecessary selection.

## Approaches

The direct brute-force approach is to consider every subset of the (n) versions. For each subset, we can collect its intervals, determine the union, and check whether that union contains every function from (1) to (m). Among all successful subsets, we keep one with minimum size. This is correct because every possible purchase decision corresponds to exactly one subset.

The problem is the number of subsets. There are (2^n) of them, and even checking a subset by scanning all (n) intervals gives (O(n2^n)) time. With (n=200000), this is far beyond any practical limit. Even an algorithm that somehow checked each subset in constant time would still have an impossible (2^{200000}) states.

The useful structure comes from the fact that all functions form one ordered line, from (1) to (m). Suppose we have already purchased some versions and they cover every function through (x). To continue the coverage without a gap, the next interval must start at or before (x+1). Among every interval that satisfies this condition, choosing the one with the largest right endpoint is always at least as good as choosing any other one. It reaches at least as far while using exactly one version.

This gives a greedy strategy. Sort intervals by their left endpoint. Starting with nothing covered, repeatedly consider every interval whose left endpoint is at most the first uncovered function. Among those intervals, take the one extending farthest to the right. If no such interval extends the current coverage, a gap is unavoidable and the answer is `NO`.

The reason this greedy choice is optimal is an exchange argument. Assume the currently covered prefix ends at (x), and let the greedy algorithm choose an interval ending at (g). Any valid solution that continues from (x) must choose some interval whose left endpoint is at most (x+1). If that interval ends at (r), then (g\ge r). Replacing it with the greedy interval cannot make the remaining coverage harder, because the greedy choice reaches at least as far. Repeating this argument at every step gives a solution with the minimum possible number of intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Greedy after sorting | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read all intervals together with their original version indices, then sort them by their left endpoint. Sorting lets us process intervals in the exact order in which they can become usable.
2. Set `covered = 0`. This means that the functions (1) through `covered` are already guaranteed to be available. Initially no function has been covered.
3. Maintain a pointer `i` into the sorted intervals. At each iteration, inspect every interval with `a[i] <= covered + 1`. Such an interval can be attached to the current covered prefix without leaving a gap.
4. Among all currently usable intervals, keep the one with the largest right endpoint. Call this endpoint `best_end` and remember its version index. We do not immediately commit to the first usable interval because a later interval may extend the coverage much farther.
5. After all intervals starting at or before `covered + 1` have been examined, check whether `best_end` is greater than `covered`. If it is not, no interval can cover the next function, so the complete range cannot be covered and we output `NO`.
6. Otherwise, select the remembered version, append its original index to the answer, and set `covered = best_end`. The next iteration now tries to extend this larger prefix.
7. Stop as soon as `covered >= m`. Every function from (1) through (m) is then covered, and the selected versions form a valid solution.
8. Because each iteration selects the interval reaching farthest from the current prefix, the greedy exchange argument proves that no solution with fewer versions can exist. The selected interval can replace the first interval of any optimal continuation without reducing its ability to cover the remaining functions.

### Why it works

The invariant is that before every selection, all functions from (1) through `covered` are covered, and the selected intervals use the minimum possible number of versions for reaching at least that far under the greedy choices. Every interval capable of continuing the coverage is considered before the next selection, and the algorithm chooses the one with maximum right endpoint. Any alternative valid next choice reaches no farther, so replacing that choice by the greedy interval cannot increase the number of intervals needed afterward. If no usable interval extends `covered`, the next function is uncovered by every remaining interval, so no valid solution exists. When `covered` reaches (m), the selected intervals cover the entire required range with the minimum possible number of versions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    intervals = []
    for idx in range(1, n + 1):
        a, b = map(int, input().split())
        intervals.append((a, b, idx))

    intervals.sort()

    covered = 0
    i = 0
    answer = []

    while covered < m:
        best_end = covered
        best_idx = -1

        # Every interval starting at or before the next uncovered
        # function can extend the current prefix.
        while i < n and intervals[i][0] <= covered + 1:
            a, b, idx = intervals[i]

            if b > best_end:
                best_end = b
                best_idx = idx

            i += 1

        # No usable interval can extend the covered prefix.
        if best_idx == -1:
            print("NO")
            return

        answer.append(best_idx)
        covered = best_end

    print("YES")
    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The tuple `(a, b, idx)` stores both endpoints and the original version number. Sorting these tuples primarily sorts by `a`, which is exactly the ordering needed by the greedy scan.

`covered + 1` is the first function that has not yet been covered. An interval is usable when its left endpoint is at most this value. This condition also handles overlapping intervals correctly. For example, if `covered == 5`, an interval beginning at `5` is usable because it already overlaps the covered region, while one beginning at `7` leaves function `6` uncovered.

The inner loop advances `i` permanently. Once an interval has been considered as a candidate for the current prefix, it never needs to be examined again. If its right endpoint was not the best extension now, it cannot become a better candidate after the covered prefix moves forward, because its endpoint is fixed and the algorithm is only interested in intervals that extend the current frontier.

The check `best_idx == -1` detects both an initial gap and a gap appearing later. For example, if `covered == 3` and every remaining interval starts at `5` or later, none can cover function `4`, so continuing would be impossible.

The algorithm stops as soon as `covered >= m`, so an interval extending beyond (m) is perfectly acceptable. There is no need to clip its endpoint. Python integers also have arbitrary precision, so there is no overflow concern.

## Worked Examples

### Sample 1

The intervals are already arranged in increasing order of their left endpoints. The table shows the greedy frontier after each selection.

| Iteration | Next uncovered | Usable intervals | Chosen version | New covered |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1:[1,2] | 1 | 2 |
| 2 | 3 | 2:[3,4] | 2 | 4 |
| 3 | 5 | 3:[5,6] | 3 | 6 |
| 4 | 7 | 4:[7,8] | 4 | 8 |

After selecting version (1), function (3) becomes the next uncovered function, so version (2) is exactly the kind of interval the greedy rule needs. The same process continues until `covered = 8`, giving the four selected versions `1 2 3 4`.

This example also shows why intervals are interpreted inclusively. The interval ([1,2]) followed by ([3,4]) has no gap because function (2) and function (3) are consecutive.

### Sample 2

The intervals are

```
1: [1,5]
2: [2,7]
3: [3,4]
4: [6,8]
```

After sorting, they are already in the displayed order. The scan behaves as follows.

| Iteration | Next uncovered | Usable intervals examined | Chosen version | New covered |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1:[1,5] | 1 | 5 |
| 2 | 6 | 2:[2,7], 3:[3,4], 4:[6,8] | 4 | 8 |

At the first iteration, only the interval beginning at (1) can start the coverage, so version (1) is selected. Once functions (1) through (5) are covered, both version (2) and version (4) can continue the range. Version (4) reaches (8), while version (2) reaches only (7), so the greedy choice is version (4).

The final answer is `1 4`, using two versions. No single version covers both function (1) and function (8), so two is minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting costs (O(n\log n)), and every interval is scanned once afterward. |
| Space | (O(n)) | The intervals and selected version indices require linear storage. |

With (n\le200000), sorting (200000) intervals and then making one linear pass is well within the intended scale for a 2-second limit in Python. The value of (m) does not appear in the complexity because the algorithm never iterates over individual functions. Even when (m=10^9), it only compares interval endpoints.

## Test Cases

The output can contain any optimal set of version indices, so a robust test harness should validate the returned solution rather than require one particular ordering of indices. The following tests do that while also checking that the number of selected versions is optimal for the supplied cases.

```python
# This test harness reimplements the solution as a callable function.
import sys
import io

def solve_io(data: str) -> str:
    inp = io.StringIO(data)
    out = io.StringIO()

    n, m = map(int, inp.readline().split())
    intervals = []

    for idx in range(1, n + 1):
        a, b = map(int, inp.readline().split())
        intervals.append((a, b, idx))

    intervals.sort()

    covered = 0
    i = 0
    answer = []

    while covered < m:
        best_end = covered
        best_idx = -1

        while i < n and intervals[i][0] <= covered + 1:
            a, b, idx = intervals[i]
            if b > best_end:
                best_end = b
                best_idx = idx
            i += 1

        if best_idx == -1:
            out.write("NO\n")
            return out.getvalue()

        answer.append(best_idx)
        covered = best_end

    out.write("YES\n")
    out.write(str(len(answer)) + "\n")
    out.write(" ".join(map(str, answer)) + "\n")
    return out.getvalue()

def validate(data: str, output: str, expected_k=None):
    lines = output.strip().splitlines()
    assert lines, "empty output"

    if lines[0] == "NO":
        assert expected_k is None
        return

    assert lines[0] == "YES"
    assert len(lines) == 3

    n, m = map(int, data.splitlines()[0].split())
    intervals = [None]

    for line in data.splitlines()[1:]:
        a, b = map(int, line.split())
        intervals.append((a, b))

    k = int(lines[1])
    chosen = list(map(int, lines[2].split()))

    assert len(chosen) == k
    assert len(set(chosen)) == k
    assert all(1 <= x <= n for x in chosen)

    covered = [False] * (m + 1)
    for idx in chosen:
        a, b = intervals[idx]
        for x in range(a, b + 1):
            covered[x] = True

    assert all(covered[1:]), "selected intervals do not cover [1, m]"

    if expected_k is not None:
        assert k == expected_k

# Provided sample 1
sample1 = """\
4 8
1 2
3 4
5 6
7 8
"""
out = solve_io(sample1)
validate(sample1, out, expected_k=4)

# Provided sample 2
sample2 = """\
4 8
1 5
2 7
3 4
6 8
"""
out = solve_io(sample2)
validate(sample2, out, expected_k=2)

# Provided sample 3
sample3 = """\
3 8
1 3
4 5
6 7
"""
out = solve_io(sample3)
assert out.strip() == "NO"

# Minimum-size input: one version covers the only function.
case4 = """\
1 1
1 1
"""
out = solve_io(case4)
validate(case4, out, expected_k=1)

# All intervals equal. One copy is sufficient.
case5 = """\
5 10
1 10
1 10
1 10
1 10
1 10
"""
out = solve_io(case5)
validate(case5, out, expected_k=1)

# Greedy choice matters. Taking [1, 3] first would need more intervals.
case6 = """\
4 10
1 3
1 6
4 8
7 10
"""
out = solve_io(case6)
validate(case6, out, expected_k=2)

# Boundary gap at the beginning.
case7 = """\
3 5
2 5
3 5
1 1
"""
out = solve_io(case7)
validate(case7, out, expected_k=2)

# Maximum-size input pattern. Each interval covers one function.
n = 200000
case8 = str(n) + " " + str(n) + "\n"
case8 += "".join(f"{i} {i}\n" for i in range(1, n + 1))
out = solve_io(case8)
validate(case8, out, expected_k=n)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `YES`, (k=1) | Minimum-size input and immediate termination |
| Five copies of `[1,10]` | `YES`, (k=1) | Duplicate intervals and avoiding unnecessary selections |
| `[1,3], [1,6], [4,8], [7,10]` | `YES`, (k=2) | Choosing the farthest-reaching interval |
| `[2,5], [3,5], [1,1]` | `YES`, (k=2) | Beginning boundary and `covered + 1` handling |
| (200000) singleton intervals | `YES`, (k=200000) | Maximum (n), linear scan after sorting, and consecutive boundaries |

The provided samples additionally cover exact consecutive intervals, overlapping intervals, and an impossible gap.

## Edge Cases

The first edge case is an uncovered beginning. Consider

```
2 5
2 5
3 5
```

The initial value is `covered = 0`, so the next required function is `1`. Both intervals have left endpoint greater than `1`, meaning the inner loop examines no usable interval. `best_idx` remains `-1`, and the algorithm prints `NO`. It does not matter that some interval reaches function (5), because function (1) is already impossible to obtain.

The middle-gap case is

```
3 8
1 3
4 5
7 8
```

The first selection changes `covered` from `0` to `3`. The next required function is `4`, so `[4,5]` is usable and changes `covered` to `5`. The next required function is `6`, but `[7,8]` starts too late. No candidate can extend the prefix, so the algorithm prints `NO`. The check is performed at every frontier, which is what prevents disconnected coverage from being mistaken for complete coverage.

The greedy-choice case is

```
3 8
1 3
1 5
5 8
```

Initially both `[1,3]` and `[1,5]` are usable. The scan keeps the larger endpoint and selects version (2), giving `covered = 5`. The next required function is `6`, so `[5,8]` is usable and extends the coverage to `8`. The answer uses two versions. A careless implementation that selected the first usable interval would choose `[1,3]`, after which `[5,8]` cannot cover function (4), forcing an incorrect extra step or incorrectly reporting failure.

The one-version case is

```
1 10
1 10
```

The first iteration considers the only interval and sets `covered = 10`. The outer loop condition `covered < m` is now false, so the algorithm stops immediately and outputs one selected version. This demonstrates why the termination condition must be checked after updating the frontier rather than unconditionally searching for another interval.

The maximum-size boundary case uses (200000) singleton intervals `[1,1], [2,2], ..., [200000,200000]`. After selecting `[i,i]`, the next required function is exactly (i+1), so the next singleton is usable. Every interval is processed once, and the algorithm finishes after (200000) selections. This confirms that the solution does not depend on (m) being small and handles the largest allowed number of versions within the intended (O(n\log n)) bound.
