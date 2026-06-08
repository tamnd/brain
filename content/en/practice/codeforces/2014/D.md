---
title: "CF 2014D - Robert Hood and Mrs Hood"
description: "Each job occupies an interval of days [l, r]. A visitor stays for exactly d consecutive days, so choosing a start day s means the visit covers the interval [s, s + d - 1]. A job is counted if it overlaps the visit at least once. The amount of overlap does not matter."
date: "2026-06-08T13:01:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 1400
weight: 2014
solve_time_s: 121
verified: true
draft: false
---

[CF 2014D - Robert Hood and Mrs Hood](https://codeforces.com/problemset/problem/2014/D)

**Rating:** 1400  
**Tags:** brute force, data structures, greedy, sortings  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

Each job occupies an interval of days `[l, r]`. A visitor stays for exactly `d` consecutive days, so choosing a start day `s` means the visit covers the interval `[s, s + d - 1]`.

A job is counted if it overlaps the visit at least once. The amount of overlap does not matter. A single shared day is enough.

For every possible valid start day, we need to know how many jobs intersect that length-`d` window. Among all valid starts, we want:

- The earliest start day whose window intersects the maximum number of jobs.
- The earliest start day whose window intersects the minimum number of jobs.

The visit must remain inside the calendar, so valid start days are from `1` through `n - d + 1`.

The constraints are what drive the solution. A single test can have up to `10^5` days and `10^5` jobs, and the sum of all `n` values over the entire input is at most `2 · 10^5`. This means an `O(n)` or `O(n log n)` solution per test case is comfortable. An `O(nk)` solution is impossible because it could require about `10^10` operations.

The tricky part is that jobs are intervals and visits are intervals. A naive overlap check for every pair of intervals is far too expensive.

Several edge cases deserve attention.

Consider:

```
n = 5
d = 2
job = [2,3]
```

The visit `[1,2]` overlaps the job because they share day `2`. The visit `[3,4]` also overlaps because they share day `3`. A careless implementation that only checks whether the visit start lies inside the job would miss one of these overlaps.

Consider ties:

```
n = 4
d = 1
jobs:
[1,1]
[4,4]
```

Counts are:

| Start | Jobs overlapped |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 1 |

The maximum count occurs on days `1` and `4`. The correct answer is day `1`, the earliest one. The same rule applies to the minimum.

Another subtle case appears when a job is longer than the visit:

```
n = 10
d = 2
job = [2,8]
```

Every visit starting from day `1` through day `8` overlaps this job. We need a way to mark all such starts efficiently rather than checking each window individually.

## Approaches

The most direct solution is to examine every valid start day and count how many jobs intersect its window.

For a start day `s`, the visit interval is `[s, s+d-1]`. A job `[l,r]` overlaps this visit if:

```
l ≤ s+d-1
and
r ≥ s
```

Checking this condition against all `k` jobs for every valid start gives a complexity of:

```
O((n-d+1) · k)
```

In the worst case both values are around `10^5`, producing roughly `10^10` overlap tests. That is far beyond the limit.

The key observation is to reverse the perspective.

Instead of asking:

> For a start day, which jobs overlap it?

ask:

> For a job, which start days overlap it?

Let the visit start at `s`.

The overlap condition is:

```
[s, s+d-1] intersects [l,r]
```

which is equivalent to:

```
s ≤ r
s+d-1 ≥ l
```

Rearranging:

```
s ≤ r
s ≥ l-d+1
```

So every start day in the range

```
[l-d+1, r]
```

produces an overlapping visit.

This is extremely useful because a job contributes `+1` to an entire contiguous range of start days.

Whenever many interval updates must be applied to an array, a difference array is the natural tool.

For each job:

```
add 1 to all starts in [l-d+1, r]
```

After clamping that range to valid start days `[1, n-d+1]`, we perform a range update in `O(1)` using a difference array.

A final prefix sum reconstructs, for every start day, the exact number of overlapping jobs.

Once those counts are known, finding the earliest maximum and earliest minimum is a simple linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(1) | Too slow |
| Optimal | O(n + k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Let `m = n - d + 1`, the number of valid start days.
2. Create a difference array large enough to support range updates on indices `1...m`.
3. For each job `[l, r]`, determine which start days overlap it.

From the overlap condition:

```
l-d+1 ≤ s ≤ r
```
4. Clamp this range to valid start days:

```
L = max(1, l-d+1)
R = min(m, r)
```

Any start outside `1...m` cannot represent a valid visit.
5. If `L ≤ R`, add one to all starts in `[L, R]` using the difference array:

```
diff[L] += 1
diff[R+1] -= 1
```
6. Compute prefix sums of the difference array.

The resulting value at position `s` equals the number of jobs overlapping the visit starting on day `s`.
7. Scan all start days from left to right.

Track the largest count seen so far and the earliest day achieving it.
8. In the same scan, track the smallest count seen so far and the earliest day achieving it.
9. Output the two recorded start days.

### Why it works

A job overlaps a visit exactly when the visit start satisfies:

```
l-d+1 ≤ s ≤ r
```

Every such start should receive one contribution from that job, and no other start should.

The difference array adds one to precisely that range of starts. Since contributions from different jobs are independent, the final prefix sum at each start day equals the total number of overlapping jobs.

The scan for maxima and minima is correct because it processes start days in increasing order. When equal counts appear later, they are ignored, preserving the earliest occurrence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n, d, k = map(int, input().split())

        m = n - d + 1
        diff = [0] * (m + 3)

        for _ in range(k):
            l, r = map(int, input().split())

            L = max(1, l - d + 1)
            R = min(m, r)

            if L <= R:
                diff[L] += 1
                diff[R + 1] -= 1

        cur = 0

        max_cnt = -1
        max_day = 1

        min_cnt = 10**18
        min_day = 1

        for day in range(1, m + 1):
            cur += diff[day]

            if cur > max_cnt:
                max_cnt = cur
                max_day = day

            if cur < min_cnt:
                min_cnt = cur
                min_day = day

        ans.append(f"{max_day} {min_day}")

    sys.stdout.write("\n".join(ans))

solve()
```

The variable `m = n - d + 1` represents all legal start positions. Every computation is performed on this compressed domain rather than on the original calendar.

For each job, the critical derivation is:

```
s+d-1 ≥ l
⇒ s ≥ l-d+1
```

Together with `s ≤ r`, this gives the exact interval of starts that overlap the job.

The clamping step is essential. A job may theoretically affect starts less than `1` or greater than `m`, but those starts do not correspond to valid visits.

The scan uses strict comparisons:

```
if cur > max_cnt:
```

and

```
if cur < min_cnt:
```

rather than `>=` or `<=`.

This preserves the earliest position whenever multiple days achieve the same count.

The difference array is allocated with a few extra cells because updates may touch `R + 1`.

## Worked Examples

### Example 1

Input:

```
n = 7
d = 2
jobs:
[1,2]
[1,3]
[6,7]
```

Valid starts are `1..6`.

For each job:

| Job | Raw range | Clamped range |
| --- | --- | --- |
| [1,2] | [0,2] | [1,2] |
| [1,3] | [0,3] | [1,3] |
| [6,7] | [5,7] | [5,6] |

After applying updates and taking prefix sums:

| Start day | Overlapping jobs |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 1 |
| 4 | 0 |
| 5 | 1 |
| 6 | 1 |

The maximum count is `2`, first achieved at day `1`.

The minimum count is `0`, first achieved at day `4`.

Output:

```
1 4
```

This example shows how a single job contributes to an entire interval of start days rather than one position.

### Example 2

Input:

```
n = 9
d = 2
jobs:
[7,9]
[4,8]
[1,3]
[2,3]
```

Valid starts are `1..8`.

Contribution ranges:

| Job | Start range |
| --- | --- |
| [7,9] | [6,8] |
| [4,8] | [3,8] |
| [1,3] | [1,3] |
| [2,3] | [1,3] |

Prefix-sum result:

| Start day | Count |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 3 |
| 4 | 1 |
| 5 | 1 |
| 6 | 2 |
| 7 | 2 |
| 8 | 2 |

The largest value is `3` at day `3`.

The smallest value is `1` at day `4`.

Output:

```
3 4
```

This trace demonstrates that jobs of very different lengths are handled uniformly by interval updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + k) | One range update per job, one scan over all valid start days |
| Space | O(n) | Difference array of size `n - d + 1` |

Since the sum of all `n` values over the input is at most `2 · 10^5`, the total work across all test cases is linear in the input size. This easily fits within the 2-second limit and the memory usage remains small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, d, k = map(int, input().split())

        m = n - d + 1
        diff = [0] * (m + 3)

        for _ in range(k):
            l, r = map(int, input().split())

            L = max(1, l - d + 1)
            R = min(m, r)

            if L <= R:
                diff[L] += 1
                diff[R + 1] -= 1

        cur = 0

        mx = -1
        mx_day = 1

        mn = 10**18
        mn_day = 1

        for day in range(1, m + 1):
            cur += diff[day]

            if cur > mx:
                mx = cur
                mx_day = day

            if cur < mn:
                mn = cur
                mn_day = day

        ans.append(f"{mx_day} {mn_day}")

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return "\n".join(ans)

# provided sample
assert run(
"""6
2 1 1
1 2
4 1 2
1 2
2 4
7 2 3
1 2
1 3
6 7
5 1 2
1 2
3 5
9 2 1
2 8
9 2 4
7 9
4 8
1 3
2 3
"""
) == """1 1
2 1
1 4
1 1
1 1
3 4"""

# minimum size
assert run(
"""1
1 1 1
1 1
"""
) == "1 1"

# tie for maximum, earliest should win
assert run(
"""1
4 1 2
1 1
4 4
"""
) == "1 2"

# d = n, only one possible start
assert run(
"""1
5 5 2
1 1
5 5
"""
) == "1 1"

# long interval covering many starts
assert run(
"""1
10 2 1
2 8
"""
) == "1 9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1,d=1,k=1` | `1 1` | Minimum constraints |
| Two jobs at days 1 and 4 | `1 2` | Earliest maximum tie handling |
| `d=n` | `1 1` | Single valid start day |
| One long interval `[2,8]` | `1 9` | Correct conversion from job interval to start interval |

## Edge Cases

Consider:

```
1
5 2 1
2 3
```

The job overlaps starts:

```
[2-2+1, 3] = [1,3]
```

Counts become:

| Start | Count |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 0 |

The algorithm marks exactly the interval `[1,3]` in the difference array and correctly outputs:

```
1 4
```

This verifies that sharing only one endpoint day still counts as overlap.

Now consider a tie case:

```
1
4 1 2
1 1
4 4
```

Counts are:

| Start | Count |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 1 |

During the scan, day `1` becomes the recorded maximum. When day `4` reaches the same value, the strict comparison prevents replacement. The answer remains the earliest maximum day.

Finally, consider:

```
1
10 2 1
2 8
```

The overlap range is:

```
[1,8]
```

after clamping.

The difference array adds one to every start from `1` through `8`, leaving start `9` with count `0`. The algorithm outputs:

```
1 9
```

which confirms that long jobs affecting many windows are handled in constant update time rather than repeated overlap checks.
