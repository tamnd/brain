---
title: "CF 102428M - Mountain Ranges"
description: "The trail contains N viewpoints in the order encountered while walking toward the mountain peak. Their altitudes form a non-decreasing array, so moving forward never requires going downhill. The couple may choose any viewpoint as their starting point."
date: "2026-08-12T07:23:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "M"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 67
verified: true
draft: false
---

[CF 102428M - Mountain Ranges](https://codeforces.com/problemset/problem/102428/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The trail contains `N` viewpoints in the order encountered while walking toward the mountain peak. Their altitudes form a non-decreasing array, so moving forward never requires going downhill.

The couple may choose any viewpoint as their starting point. From there, they visit viewpoints one by one in increasing array order. A move from viewpoint `i` to viewpoint `i + 1` is allowed only when the altitude increase `A[i + 1] - A[i]` is at most `X`. As soon as one adjacent increase is larger than `X`, the hike must stop. The task is to find the largest number of consecutive viewpoints that can be visited.

The key consequence of the non-decreasing order is that every possible hike corresponds to a contiguous segment of the array. We only need to find the longest segment whose every adjacent altitude difference is at most `X`.

Here `N` is at most `1000`, so even an `O(N^2)` solution performs at most roughly half a million adjacent comparisons in the worst case. That is small enough for these constraints. However, the structure of the problem gives an `O(N)` solution, which is both simpler and more scalable. The altitude and `X` bounds are also small enough that Python integers have no overflow concerns.

There are several edge cases that can expose mistakes in the transition logic. First, with one viewpoint, there is no move to make, so the answer must be `1`. For example,

```
1 0
500
```

has answer `1`. A solution that initializes its best length to zero would incorrectly return zero.

A second edge case is `X = 0`. Since the array is non-decreasing, the only allowed moves are between viewpoints with exactly equal altitude. For example,

```
5 0
10 10 10 11 11
```

has answer `3`, because the first three viewpoints form the longest valid segment. A careless implementation using `< X` instead of `<= X` would reject even equal-altitude moves.

A third case occurs when every transition is allowed. For example,

```
4 3
2 3 5 8
```

has answer `4`. The final viewpoint must be counted when a valid segment reaches the end of the array. Implementations that update the answer only when an invalid transition is encountered can accidentally miss this case.

Finally, an invalid transition breaks the current segment completely. For

```
5 2
1 2 10 11 12
```

the answer is `3`, from `10, 11, 12`. Once the jump from `2` to `10` is too large, the valid segment before it cannot be extended across that jump.

## Approaches

The direct approach is to try every possible starting viewpoint. Starting at index `i`, we walk toward the peak while consecutive altitude differences remain at most `X`, counting how many viewpoints are reachable. The maximum count over all starting positions is the answer. This is correct because every possible hike has exactly one starting viewpoint, and from that starting point there is only one direction to follow.

In the worst case, when every transition is valid, starting from index `0` checks `N - 1` transitions, starting from index `1` checks `N - 2`, and so on. The total is

`(N - 1) + (N - 2) + ... + 1 = N(N - 1)/2`

comparisons, which is `499,500` when `N = 1000`. That is completely manageable for the stated constraint, so the brute-force solution is actually acceptable here. Its weakness is that it repeats the same transition checks many times.

The observation that removes this repetition is that a transition is either valid or invalid independently of where the current hike started. If `A[i + 1] - A[i] <= X`, a valid segment can continue across that boundary. If the difference is larger than `X`, no hike can cross that boundary at all. Thus we can scan the array once and maintain the length of the current consecutive valid segment.

Whenever a transition is valid, the current segment grows by one viewpoint. Whenever it is invalid, the current segment must restart at the next viewpoint, whose length is `1`. The largest value ever reached is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Accepted for N ≤ 1000 |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `current = 1` and `answer = 1`. A single viewpoint is always a valid hike because no movement is required.
2. Scan every adjacent pair `A[i - 1]` and `A[i]`.
3. If `A[i] - A[i - 1] <= X`, extend the current valid segment by setting `current += 1`. This is valid because the couple can move from the previous viewpoint to the current one.
4. Otherwise, set `current = 1`. The transition between these two viewpoints cannot be crossed, so the only valid segment ending at the current viewpoint starts at the current viewpoint itself.
5. After processing each viewpoint, update `answer = max(answer, current)`. The current segment may be the longest one seen so far, including when it reaches the final viewpoint.
6. Print `answer`.

### Why it works

Maintain the invariant that `current` is exactly the maximum number of consecutive viewpoints in the segment ending at the current index whose every adjacent altitude increase is at most `X`. If the current transition is allowed, the previous valid segment can be extended by one. If the transition is forbidden, no valid segment ending at the current viewpoint can contain the previous viewpoint, so its best possible length is exactly `1`. Since every possible hike is a contiguous segment and every boundary is checked, taking the maximum `current` over the scan gives the maximum number of viewpoints that can be visited.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    current = 1
    answer = 1

    for i in range(1, n):
        if a[i] - a[i - 1] <= x:
            current += 1
        else:
            current = 1

        answer = max(answer, current)

    print(answer)

if __name__ == "__main__":
    solve()
```

The first line reads the number of viewpoints and the maximum permitted altitude increase. The second line contains the already sorted viewpoint altitudes.

`current` represents the valid segment ending at the current position. It starts at `1` because the first viewpoint can always be visited by itself. `answer` also starts at `1` for the same reason.

The loop begins at index `1` because a transition requires two viewpoints. The expression `a[i] - a[i - 1] <= x` deliberately uses `<=`, since an increase exactly equal to `X` is allowed.

When a transition is too large, `current` becomes `1`, not `0`. The current viewpoint itself is still a perfectly valid starting point. Updating `answer` after both branches also handles a valid segment that continues all the way to the last viewpoint.

There is no need for special handling of `N = 1`. The initialization already produces the correct answer, and the loop simply executes zero times.

## Worked Examples

### Sample 1

For the sample with `X = 2`, the altitude differences are `11, 1, 77, 561, 5244, 0, 1, 2`. Only the final four viewpoints form one continuous valid segment.

| Index | Altitude | Difference | `current` | `answer` |
| --- | --- | --- | --- | --- |
| 0 | 3 | - | 1 | 1 |
| 1 | 14 | 11 | 1 | 1 |
| 2 | 15 | 1 | 2 | 2 |
| 3 | 92 | 77 | 1 | 2 |
| 4 | 653 | 561 | 1 | 2 |
| 5 | 5897 | 5244 | 1 | 2 |
| 6 | 5897 | 0 | 2 | 2 |
| 7 | 5898 | 1 | 3 | 3 |
| 8 | 5900 | 2 | 4 | 4 |

The final answer is `4`. The trace demonstrates why an invalid transition resets the segment and why a transition exactly equal to `X` is accepted.

### Sample 2

Here `X = 0`, so only equal consecutive altitudes can be connected.

| Index | Altitude | Difference | `current` | `answer` |
| --- | --- | --- | --- | --- |
| 0 | 3 | - | 1 | 1 |
| 1 | 14 | 11 | 1 | 1 |
| 2 | 15 | 1 | 1 | 1 |
| 3 | 92 | 77 | 1 | 1 |
| 4 | 653 | 561 | 1 | 1 |
| 5 | 5897 | 5244 | 1 | 1 |
| 6 | 5897 | 0 | 2 | 2 |
| 7 | 5898 | 1 | 1 | 2 |
| 8 | 5900 | 2 | 1 | 2 |

The answer is `2`, corresponding to the two consecutive viewpoints at altitude `5897`. This exercises the equality boundary for `X = 0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every adjacent pair is examined exactly once. |
| Space | O(N) | The altitude array is stored, while the algorithm itself uses O(1) additional space. |

With `N ≤ 1000`, the algorithm performs only a linear number of operations and uses a very small amount of memory. Python's integer representation also makes overflow irrelevant for the given altitude bounds.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    current = 1
    answer = 1

    for i in range(1, n):
        if a[i] - a[i - 1] <= x:
            current += 1
        else:
            current = 1

        answer = max(answer, current)

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""9 2
3 14 15 92 653 5897 5897 5898 5900
""") == "4", "sample 1"

assert run("""9 0
3 14 15 92 653 5897 5897 5898 5900
""") == "2", "sample 2"

assert run("""9 8848
3 14 15 92 653 5897 5897 5898 5900
""") == "9", "sample 3"

# Minimum-size input
assert run("""1 0
500
""") == "1", "single viewpoint"

# All viewpoints have the same altitude
assert run("""6 0
100 100 100 100 100 100
""") == "6", "all equal"

# Boundary condition: difference exactly X is allowed
assert run("""5 3
2 5 8 11 15
""") == "4", "exactly X"

# Multiple breaks, longest segment is at the end
assert run("""7 2
1 2 10 11 12 20 21
""") == "3", "multiple breaks"

# Maximum-size input
assert run(
    "1000 0\n" + " ".join(["42"] * 1000) + "\n"
) == "1000", "maximum size"

# Off-by-one case: final valid segment reaches the end
assert run("""4 2
1 10 11 13
""") == "3", "final segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 500` | 1 | Minimum input and initial answer |
| `6 0 / 100 100 100 100 100 100` | 6 | All transitions valid when `X = 0` |
| `5 3 / 2 5 8 11 15` | 4 | A difference exactly equal to `X` is allowed |
| `7 2 / 1 2 10 11 12 20 21` | 3 | Several invalid transitions and restarting |
| 1000 equal values with `X = 0` | 1000 | Maximum input size |
| `4 2 / 1 10 11 13` | 3 | Correctly counting a segment that ends at the final viewpoint |

## Edge Cases

For a single viewpoint, the input

```
1 0
500
```

initializes both `current` and `answer` to `1`. The loop has no transitions to inspect, so the output remains `1`, which is correct because visiting one viewpoint requires no uphill movement.

For `X = 0`, consider

```
5 0
10 10 10 11 11
```

The first transition has difference `0`, so `current` becomes `2`. The second also has difference `0`, giving `current = 3`. The transition from `10` to `11` has difference `1`, so `current` resets to `1`. The final equal pair raises it to `2`. The maximum is `3`.

When a transition is exactly the allowed limit, it must not break the segment. For

```
5 3
2 5 8 11 15
```

the first three differences are all `3`, so `current` grows from `1` to `4`. The last difference is `4`, which resets `current` to `1`. The output is `4`. This is the case that distinguishes `<= X` from `< X`.

For multiple breaks,

```
7 2
1 2 10 11 12 20 21
```

the first difference `1` creates a segment of length `2`. The difference `8` breaks it, so the viewpoint at altitude `10` starts a new segment. The next two differences are `1` and `1`, giving a segment of length `3`. The difference `8` breaks it again, and the final pair has length `2`. The answer is consequently `3`.

When the longest segment reaches the end, the answer must already have been updated while processing its final viewpoint. In

```
4 2
1 10 11 13
```

the first transition breaks immediately, then the differences `1` and `2` extend the segment starting at `10` to length `3`. Because `answer` is updated on every iteration, that final segment is counted even though there is no later invalid transition to trigger a separate update.
