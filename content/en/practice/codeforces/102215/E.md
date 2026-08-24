---
title: "CF 102215E - Third-Party Software - 2"
description: "We have n library versions. Version i provides every function whose number lies in the inclusive interval [ai, bi]. Pavel needs every function from 1 through m, so the purchased intervals must collectively cover the entire integer range [1, m]. The task has two parts."
date: "2026-08-24T16:52:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "E"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 2403
verified: true
draft: false
---

[CF 102215E - Third-Party Software - 2](https://codeforces.com/problemset/problem/102215/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` library versions. Version `i` provides every function whose number lies in the inclusive interval `[a_i, b_i]`. Pavel needs every function from `1` through `m`, so the purchased intervals must collectively cover the entire integer range `[1, m]`.

The task has two parts. First, we must decide whether such a collection of versions exists at all. If it does, we must find a collection with the smallest possible number of versions and print their original indices.

The large value of `m`, up to `10^9`, immediately rules out algorithms that iterate over every function number. The useful size parameter is `n`, which is at most `200000`, so an `O(n log n)` algorithm is appropriate for a two-second limit. An `O(n^2)` search over pairs or larger combinations would require up to about `4 * 10^10` interval comparisons, which is far beyond what the limit permits.

There are several boundary cases that can break a careless implementation. If the first interval does not start at function `1`, coverage is impossible. For example,

```
2 5
2 5
1 1
```

is actually possible, because the second version covers function `1` and the first covers `2` through `5`. A greedy algorithm that simply chooses the interval with the largest right endpoint globally would select `[2,5]` first and could incorrectly conclude that function `1` is missing. The algorithm must respect the left boundary before maximizing the right endpoint.

A more direct failure occurs when there is a genuine gap:

```
2 5
1 2
4 5
```

The correct answer is `NO`, because function `3` is unavailable. Choosing intervals according only to their right endpoints does not detect this correctly unless the next interval is required to begin at most one position after the currently covered prefix.

Another edge case is an interval that starts exactly at the first uncovered function:

```
3 6
1 2
3 4
5 6
```

The answer is `YES` with three versions. Since the functions are integers, after covering through `2`, an interval beginning at `3` is perfectly valid. The condition is `a_i <= covered + 1`, not `a_i <= covered`.

Finally, overlapping intervals can make a locally short-looking choice suboptimal:

```
3 8
1 3
2 7
6 8
```

The optimal solution uses `[1,3]` and `[2,7]` only if another interval reaches `8`, which it does not, so in this particular input the answer is `NO`. If we change the last interval to `[6,8]`, the same reasoning shows why every selected interval must extend the currently covered prefix. The greedy choice should always maximize the new right endpoint among all intervals that can continue the current coverage.

## Approaches

The brute-force approach follows directly from the definition. We could try every subset of library versions, check whether the union covers `[1,m]`, and keep the smallest valid subset. This is correct because every possible purchase decision is explicitly considered, but there are `2^n` subsets. With `n = 200000`, that is hopelessly large.

Even restricting the brute force to pairs, triples, or other small combinations does not solve the general problem. For example, examining every pair already takes `O(n^2)`, which reaches roughly `2 * 10^10` pairs when `n = 200000`. The problem needs a way to make the choice greedily rather than enumerate combinations.

The key observation is that the functions we have already covered always form a prefix `[1, x]`. Suppose `x` is the largest function currently covered. Any interval that can extend this prefix must satisfy `a_i <= x + 1`. Among all such intervals, choosing the one with the largest `b_i` is never worse than choosing one with a smaller right endpoint. Both choices can start the next portion of the coverage, but the interval reaching farther can only leave at least as much of the remaining problem solved.

This gives the standard greedy strategy for minimum interval covering. Sort intervals by their left endpoint. Starting with `covered = 0`, scan every interval whose left endpoint is at most `covered + 1` and remember the one with the largest right endpoint. Once the scan reaches an interval that starts too far to the right, we must commit to the best interval found so far, because every currently usable interval has already been considered. If that best interval does not extend `covered`, there is a gap and the answer is impossible.

The brute-force works because it explicitly searches all ways of extending the covered region, but fails because there are exponentially many choices. The observation that only the farthest-reaching usable interval matters reduces the search to one sorted scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n n)` | `O(n)` | Too slow |
| Optimal greedy | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Store every interval together with its original version number, then sort the intervals by their left endpoint. Sorting lets us process all intervals that could currently continue the covered prefix in a single forward scan.
2. Set `covered = 0`. This means that no functions have been covered yet, so the first function we need is `1`.
3. Scan the sorted intervals. While an interval has `a_i <= covered + 1`, it can connect directly to the already covered prefix. Among all such intervals, keep the one with the greatest `b_i`.
4. When the next interval starts after `covered + 1`, stop considering the current group and purchase the remembered interval. It is the best possible choice among every interval that could have extended the current prefix.
5. Update `covered` to the chosen interval's right endpoint and add its original index to the answer. Then continue scanning from the first interval that was not yet considered.
6. If no usable interval was found, the next function cannot be covered. There is a gap between `covered` and the remaining intervals, so the correct answer is `NO`.
7. If `covered >= m`, the entire required range `[1,m]` is covered. The selected intervals form a valid solution.

The reason the greedy choice is optimal is captured by an exchange argument. Assume the current prefix ends at `covered`. Every valid solution must choose some interval with `a_i <= covered + 1` to continue the coverage. Let the greedy algorithm choose an eligible interval ending at `G`, while an optimal solution chooses an eligible interval ending at `O`. Since the greedy choice maximizes the right endpoint, `G >= O`. Replacing the optimal solution's first chosen interval with the greedy interval cannot make any later coverage harder, because the greedy interval reaches at least as far. Repeating this argument at every extension shows that the greedy algorithm uses the minimum possible number of intervals.

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

    ans = []
    covered = 0
    i = 0

    while covered < m:
        best_right = covered
        best_idx = -1

        while i < n and intervals[i][0] <= covered + 1:
            a, b, idx = intervals[i]

            if b > best_right:
                best_right = b
                best_idx = idx

            i += 1

        if best_idx == -1:
            print("NO")
            return

        ans.append(best_idx)
        covered = best_right

    print("YES")
    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The input is first converted into `(left, right, original_index)` triples. Keeping the original index is necessary because sorting changes the order in which intervals are stored, while the output must refer to the versions as they appeared in the input.

The sorted scan uses `covered + 1` rather than `covered`. Since functions are numbered with integers, an interval beginning at exactly the next uncovered function connects perfectly to the current prefix. For example, coverage through `5` can be extended by `[6,8]`.

Inside the inner loop, `best_right` records the farthest endpoint among every interval that is currently usable. We advance `i` as soon as an interval is examined, so each interval enters the inner loop exactly once. When the next interval has `a_i > covered + 1`, no unexamined interval can be used in the current step because the intervals are sorted by their left endpoint.

The `best_idx == -1` check handles both an empty usable set and a situation where every usable interval ends no farther than `covered`. Since every interval has `b_i >= a_i`, an interval satisfying `a_i <= covered + 1` can still fail to extend the prefix only when it ends at or before `covered`. Such an interval cannot help, so treating it as a non-extending choice is correct.

Python integers have arbitrary precision, so the upper bound `m <= 10^9` causes no overflow issue.

## Worked Examples

### Sample 1

The intervals are already ordered by their left endpoints. Initially nothing is covered, so only an interval starting at `1` can be selected. After considering it, coverage reaches `2`. The next usable interval starts at `3`, and so on.

| `covered` before step | Usable intervals | Best right endpoint | Chosen version | `covered` after step |
| --- | --- | --- | --- | --- |
| 0 | `[1,2]` | 2 | 1 | 2 |
| 2 | `[3,4]` | 4 | 2 | 4 |
| 4 | `[5,6]` | 6 | 3 | 6 |
| 6 | `[7,8]` | 8 | 4 | 8 |

The algorithm reaches `m = 8` after four choices, producing `YES`, `4`, and the version indices `1 2 3 4`. Every selected interval is forced to continue directly from the previous prefix, so the invariant remains valid after every step.

### Sample 2

The intervals are `[1,5]`, `[2,7]`, `[3,4]`, and `[6,8]`. At the beginning, the first three intervals are usable because their left endpoints are at most `1` only for the first interval, so version `1` is chosen and coverage reaches `5`. Now every interval beginning at most `6` is usable, including version `4`, which reaches `8`.

| `covered` before step | Intervals considered in this step | Best right endpoint | Chosen version | `covered` after step |
| --- | --- | --- | --- | --- |
| 0 | `[1,5]` | 5 | 1 | 5 |
| 5 | `[2,7]`, `[3,4]`, `[6,8]` | 8 | 4 | 8 |

The result is two versions, `1` and `4`. Version `2` reaches only `7`, so choosing it instead would require another version to reach `8`. The greedy choice avoids that extra purchase.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting costs `O(n log n)`, and the subsequent scan examines each interval once |
| Space | `O(n)` | The interval array and selected version indices contain at most `n` elements |

With `n <= 200000`, sorting dominates the runtime and is well within the intended range for a two-second solution. The value of `m` can be as large as `10^9`, but the algorithm never iterates over individual functions, so that large bound has no effect on the running time. The memory usage is linear in `n`, comfortably below 256 MB.

## Test Cases

The test helper below runs the same greedy logic on an in-memory input and validates the returned version set instead of requiring one particular valid set. This matters because the problem allows any optimal solution.

```python
import sys
import io

def solve_io():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    intervals = []

    for idx in range(1, n + 1):
        a, b = map(int, input().split())
        intervals.append((a, b, idx))

    intervals.sort()

    ans = []
    covered = 0
    i = 0

    while covered < m:
        best_right = covered
        best_idx = -1

        while i < n and intervals[i][0] <= covered + 1:
            a, b, idx = intervals[i]
            if b > best_right:
                best_right = b
                best_idx = idx
            i += 1

        if best_idx == -1:
            print("NO")
            return

        ans.append(best_idx)
        covered = best_right

    print("YES")
    print(len(ans))
    print(*ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve_io()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def check(inp: str, out: str) -> bool:
    lines = out.strip().splitlines()
    first = lines[0]

    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    intervals = []
    for idx in range(1, n + 1):
        a = int(next(it))
        b = int(next(it))
        intervals.append((a, b))

    # A small independent greedy check tells us whether coverage is possible
    intervals_sorted = sorted(intervals)
    covered = 0
    i = 0
    possible = True

    while covered < m:
        best = covered

        while i < n and intervals_sorted[i][0] <= covered + 1:
            best = max(best, intervals_sorted[i][1])
            i += 1

        if best == covered:
            possible = False
            break

        covered = best

    if not possible:
        return first == "NO"

    if first != "YES":
        return False

    k = int(lines[1])
    chosen = list(map(int, lines[2].split()))

    if k != len(chosen) or k == 0:
        return False

    if len(set(chosen)) != k:
        return False

    if any(x < 1 or x > n for x in chosen):
        return False

    chosen_intervals = [intervals[x - 1] for x in chosen]
    chosen_intervals.sort()

    covered = 0
    for a, b in chosen_intervals:
        if a > covered + 1:
            return False
        covered = max(covered, b)

    return covered >= m

# Provided samples
sample1 = """\
4 8
1 2
3 4
5 6
7 8
"""
assert check(sample1, run(sample1)), "sample 1"

sample2 = """\
4 8
1 5
2 7
3 4
6 8
"""
assert check(sample2, run(sample2)), "sample 2"

sample3 = """\
3 8
1 3
4 5
6 7
"""
assert check(sample3, run(sample3)), "sample 3"

# Minimum-size input
case4 = """\
1 1
1 1
"""
assert check(case4, run(case4)), "minimum-size case"

# All intervals equal
case5 = """\
5 10
1 10
1 10
1 10
1 10
1 10
"""
assert check(case5, run(case5)), "all-equal intervals"

# Exact boundary connection: [1,2] followed by [3,5]
case6 = """\
2 5
1 2
3 5
"""
assert check(case6, run(case6)), "exact covered+1 boundary"

# Gap at function 3
case7 = """\
3 5
1 2
4 5
1 1
"""
assert check(case7, run(case7)), "gap case"

# Large n with a single interval covering everything
case8 = "200000 1000000000\n" + "1 1000000000\n" * 200000
assert check(case8, run(case8)), "maximum-n case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `YES`, one version | Minimum values and the smallest possible covered range |
| Five copies of `[1,10]` | `YES`, one version | Duplicate and all-equal intervals |
| `[1,2]`, `[3,5]` | `YES`, two versions | Correct use of the `covered + 1` boundary |
| `[1,2]`, `[4,5]`, `[1,1]` | `NO` | Detection of a genuine uncovered function |
| `200000` copies of `[1,10^9]` | `YES`, one version | Maximum `n` and large `m` without iterating over functions |

## Edge Cases

### The first usable interval must reach function 1

Consider

```
2 5
2 5
1 1
```

Initially `covered = 0`, so the condition is `a_i <= 1`. Version `2`, `[1,1]`, is the only usable interval and extends coverage to `1`. The next usable interval is `[2,5]`, which starts at `covered + 1 = 2`, so coverage reaches `5`. The algorithm outputs `YES` with two versions. A strategy that picks the interval with the largest right endpoint without first checking connectivity would fail on this case.

### A genuine gap must produce NO

For

```
2 5
1 2
4 5
```

the first step selects `[1,2]`, giving `covered = 2`. The next interval starts at `4`, while the next required function is `3`. Since `4 > 2 + 1`, no interval can cover function `3`, and `best_idx` remains unset. The algorithm immediately outputs `NO`.

### Starting exactly at the next function is valid

For

```
2 5
1 2
3 5
```

the first interval produces `covered = 2`. The second interval has `a = 3`, satisfying `a <= covered + 1`. It is selected and extends coverage to `5`. The answer is `YES` with two versions. Using `a <= covered` instead would incorrectly reject this valid case.

### An interval that does not extend coverage should not be selected

Suppose

```
3 6
1 3
2 3
4 6
```

After selecting `[1,3]`, the next interval `[2,3]` is technically eligible because `2 <= 4`, but it does not increase the covered prefix. The algorithm records it but leaves `best_right = 3` because its endpoint is not larger. Then `[4,6]` is also eligible and becomes the best choice, extending coverage to `6`. The redundant `[2,3]` is never purchased.

This detail is useful because eligibility and usefulness are different concepts. An interval can overlap the current prefix without extending it, and such an interval must not count as progress.

### Overlapping intervals require the farthest endpoint

For

```
4 8
1 3
2 5
4 7
6 8
```

the first step considers only `[1,3]`, so `covered` becomes `3`. The next step can use `[2,5]`, reaching `5`. From there `[4,7]` is usable and reaches `7`, followed by `[6,8]`. The algorithm selects four intervals.

If an alternative input contains `[2,7]` instead of `[2,5]`, the greedy algorithm immediately prefers that interval because it reaches farther. That choice can eliminate later purchases. The exchange argument guarantees that selecting the farthest reachable endpoint never increases the minimum number of intervals required afterward.
