---
title: "CF 105198B - 21---0?"
description: "We are given a sequence of daily solve counts indirectly. The original array contains how many problems were solved on each day, but only the sum of the recent days is provided."
date: "2026-06-27T02:56:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105198
codeforces_index: "B"
codeforces_contest_name: "ShellBeeHaken Presents Intra SUST Programming Contest 2024 - Replay"
rating: 0
weight: 105198
solve_time_s: 57
verified: true
draft: false
---

[CF 105198B - 21---0?](https://codeforces.com/problemset/problem/105198/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily solve counts indirectly. The original array contains how many problems were solved on each day, but only the sum of the recent days is provided. For the first `k` days, the value represents the total number of solved problems from the beginning of the month until that day. After that, each value represents the sum of exactly the previous `k` days ending at that day.

The task is to recover enough information about the original daily counts to find the longest consecutive interval where every day had a positive solve count.

The constraints force us toward a linear solution. The total number of days over all test cases is at most `3 * 10^5`, so an `O(n)` or `O(n log n)` method is realistic. A solution that checks every possible interval or repeatedly reconstructs sums would require around `O(n^2)` operations in the worst case, which is far beyond what a 2 second limit allows.

Several edge cases can break a careless implementation. When `k = n`, the whole array is just prefix sums, so treating every value as a normal sliding window sum gives incorrect differences. For example:

```
Input:
1
3 3
1 2 2
```

The original days are `[1, 1, 0]`, so the answer is `2`. A wrong sliding-window-only approach may fail because there are no full windows after the first `k` days.

Another tricky case is when the sliding sum decreases. A decrease does not directly mean the current day has zero solves, because an old positive day may leave the window. For example:

```
Input:
1
5 2
1 2 1 0 0
```

The original days are `[1, 1, 0, 0, 0]`, so the answer is `2`. Looking only at whether consecutive values increase or decrease can incorrectly classify days.

A third case is when all days are positive:

```
Input:
1
5 2
1 2 2 2 2
```

The answer is `5`. A method that searches for changes in the given array rather than reconstructing the daily counts would incorrectly stop the streak early.

## Approaches

The direct approach is to rebuild the original daily counts. Let the hidden array be `x`. For the first `k` days, the given values are prefix sums, so each day can be found by subtracting the previous prefix sum. After day `k`, the current value is a window sum. Removing the previous window and adding the new day gives the relation:

`a[i] - a[i-1] = x[i] - x[i-k]`

so:

`x[i] = a[i] - a[i-1] + x[i-k]`

This lets us compute each hidden value in constant time.

A brute-force solution could first reconstruct the full array and then test every possible streak by expanding from every starting day. This is correct because every possible interval is checked, but in the worst case it performs `O(n^2)` work. With `n = 300000`, that can mean about 90 billion operations.

The observation that each hidden day depends only on the value `k` positions earlier changes the problem completely. We do not need to search intervals repeatedly. While reconstructing the days, we can maintain the current streak length. Whenever the recovered value is positive, the streak grows. Whenever it is zero, the streak ends and we update the best answer. Since every day is processed once, the whole problem becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `days` that will store the recovered number of solved problems for each day. The recurrence for later days needs the value from `k` days earlier, so keeping previous values makes the transition possible.
2. Recover the first `min(n, k)` days using prefix sums. The first day equals `a[0]`. Every later day in this prefix region is `a[i] - a[i-1]`. These values represent the actual daily solves because the given values are cumulative totals.
3. For every day after the first `k` days, compute the hidden value using `a[i] - a[i-1] + days[i-k]`. The subtraction represents the old day leaving the window, and adding `days[i-k]` restores the contribution that was removed.
4. While recovering each day, update the current streak. If the recovered value is greater than zero, increase the current streak and update the maximum. If it is zero, reset the current streak because a zero-solve day breaks consecutive solving.
5. Print the maximum streak found after all days have been processed.

Why it works: the reconstruction formula exactly follows the definition of each sliding window. For the first `k` days, prefix differences give the only possible daily values. For later days, the difference between two adjacent window sums tells us the change caused by removing one old day and adding one new day. Since the array is guaranteed to be valid, the reconstructed values are exactly the original daily counts. The streak calculation then directly measures the longest run of positive values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        days = [0] * n
        best = 0
        cur = 0

        for i in range(n):
            if i == 0:
                days[i] = a[i]
            elif i < k:
                days[i] = a[i] - a[i - 1]
            else:
                days[i] = a[i] - a[i - 1] + days[i - k]

            if days[i] > 0:
                cur += 1
                if cur > best:
                    best = cur
            else:
                cur = 0

        ans.append(str(best))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The array `days` stores the reconstructed daily solve counts. It is indexed from zero, so `days[i-k]` is the day that leaves the sliding window when calculating day `i`.

The first branch handles day zero separately because there is no previous prefix sum. The second branch covers the prefix-sum part of the input, where subtraction of adjacent values gives the exact daily count. The last branch uses the sliding-window recurrence.

Python integers are used automatically, so the large possible values of `a[i]` do not create overflow problems. The order of operations in the recurrence is also important: the previous window difference must be corrected by adding back the outgoing day's contribution.

## Worked Examples

For the first sample:

```
n = 5, k = 2
a = [1, 2, 1, 4, 5]
```

| Day | Formula used | Recovered solves | Current streak | Maximum |
| --- | --- | --- | --- | --- |
| 1 | `a[0]` | 1 | 1 | 1 |
| 2 | `a[1]-a[0]` | 1 | 2 | 2 |
| 3 | `a[2]-a[1]+days[0]` | 0 | 0 | 2 |
| 4 | `a[3]-a[2]+days[1]` | 4 | 1 | 2 |
| 5 | `a[4]-a[3]+days[2]` | 1 | 2 | 2 |

The reconstruction gives `[1, 1, 0, 4, 1]`. The zero on day three breaks the first streak, leaving the answer as `2`.

For the third sample:

```
n = 5, k = 2
a = [1, 2, 2, 2, 2]
```

| Day | Formula used | Recovered solves | Current streak | Maximum |
| --- | --- | --- | --- | --- |
| 1 | `a[0]` | 1 | 1 | 1 |
| 2 | `a[1]-a[0]` | 1 | 2 | 2 |
| 3 | `a[2]-a[1]+days[0]` | 1 | 3 | 3 |
| 4 | `a[3]-a[2]+days[1]` | 1 | 4 | 4 |
| 5 | `a[4]-a[3]+days[2]` | 1 | 5 | 5 |

Every recovered value is positive, so the streak reaches the entire month.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each day is reconstructed and processed once. |
| Space | O(n) | The recovered array is stored because future days need values from `k` positions earlier. |

The total `n` across all test cases is bounded by `3 * 10^5`, so a linear pass easily fits the time limit. The memory usage is also within the 256 MB limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))

            days = [0] * n
            cur = 0
            best = 0

            for i in range(n):
                if i == 0:
                    days[i] = a[i]
                elif i < k:
                    days[i] = a[i] - a[i - 1]
                else:
                    days[i] = a[i] - a[i - 1] + days[i - k]

                if days[i] > 0:
                    cur += 1
                    best = max(best, cur)
                else:
                    cur = 0

            out.append(str(best))

        return "\n".join(out)

    result = solve()
    sys.stdin = old_stdin
    return result

assert run("""3
2 2
1 2
5 2
1 2 1 4 5
5 2
1 2 2 2 2
""") == "2\n2\n5", "samples"

assert run("""1
2 1
5 0
""") == "1", "minimum k"

assert run("""1
3 3
1 2 2
""") == "2", "full prefix case"

assert run("""1
5 2
1 2 1 0 0
""") == "2", "decreasing windows"

assert run("""1
6 3
0 0 0 0 0 0
""") == "0", "all zero days"

assert run("""1
6 6
1 3 6 6 7 9
""") == "3", "large k boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 2` | `2` | Smallest month and normal prefix reconstruction |
| `3 3 / 1 2 2` | `2` | Case where the entire month is a prefix sum |
| `5 2 / 1 2 1 0 0` | `2` | Sliding windows that decrease |
| `6 3 / 0 0 0 0 0 0` | `0` | No positive day exists |
| `6 6 / 1 3 6 6 7 9` | `3` | Large `k` and prefix boundary |

## Edge Cases

When `k = n`, every value is a prefix sum. For:

```
1
3 3
1 2 2
```

the algorithm uses only the prefix reconstruction branch. It obtains days `[1, 1, 0]`, updates the streak to `2`, then resets after the zero. The output is `2`.

When a window decreases, the algorithm does not assume the new day is zero. For:

```
1
5 2
1 2 1 0 0
```

the recovered days are `[1, 1, 0, 0, 0]`. The recurrence correctly accounts for the old day leaving the window, so the answer remains `2`.

When every day is positive, there is no reset. For:

```
1
5 2
1 2 2 2 2
```

each reconstructed day equals `1`, so the current streak grows from `1` to `5` and the final answer is `5`. The algorithm handles this because it checks the reconstructed daily values rather than patterns in the input array.
