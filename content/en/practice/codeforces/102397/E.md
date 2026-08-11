---
title: "CF 102397E - Bashar and the bad land (Hard)"
description: "The invariant is that before processing each new right endpoint, left points to the smallest possible left boundary after all previous shrinking."
date: "2026-08-11T15:48:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "E"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 91
verified: true
draft: false
---

[CF 102397E - Bashar and the bad land (Hard)](https://codeforces.com/problemset/problem/102397/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Why it works

The invariant is that before processing each new right endpoint, `left` points to the smallest possible left boundary after all previous shrinking. Whenever the window `[left, right]` reaches the target, the algorithm removes houses from the left for as long as the target remains satisfied. Thus, for this particular `right`, the final valid window is the shortest valid window ending at `right`. Every possible optimal segment has some right endpoint, and when that endpoint is processed, the algorithm finds a window no longer than it. Taking the minimum over all right endpoints therefore produces the globally shortest valid segment. Converting its number of houses from `k` to walking distance `k - 1` gives the required answer.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, n = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    best = n + 1

    for right in range(n):
        current_sum += a[right]

        while current_sum >= x:
            best = min(best, right - left + 1)
            current_sum -= a[left]
            left += 1

    if best == n + 1:
        print(-1)
    else:
        print(best - 1)

if __name__ == "__main__":
    solve()
```

The input is read once, and the array is stored so that the left endpoint can later remove its corresponding value from the running sum. The variables `left` and `right` define the current contiguous segment, while `current_sum` stores its total without repeatedly summing the entire segment.

The outer loop adds each house exactly once. Once `current_sum >= x`, the inner loop tries to remove houses from the left. The expression `right - left + 1` is the number of houses currently in the segment, so it is the quantity that must be minimized during the sliding-window process.

The order of operations inside the shrinking loop matters. The current window is valid before `a[left]` is removed, so its length must be considered before changing `left`. After removal, the window may become invalid, in which case the loop stops naturally.

There is no integer-overflow issue in Python. The largest possible total is `10^5 * 10^5 = 10^10`, which is also safely representable by Python integers.

Finally, `best - 1` converts the minimum number of visited houses into walking distance. If one house is sufficient, `best` is `1` and the printed distance is correctly `0`.

# Worked Examples

## Sample 1

Consider `x = 12` and `a = [1, 3, 4, 5, 2]`. The useful window eventually becomes `[3, 4, 5]`, which contains three houses and has a walking distance of two.

| `right` | Added value | `current_sum` before shrinking | `left` | Best window length |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | not found |
| 1 | 3 | 4 | 0 | not found |
| 2 | 4 | 8 | 0 | not found |
| 3 | 5 | 13 | 0 | 3 |
| 4 | 2 | 11 | 1 | 3 |

At `right = 3`, the sum becomes 13. The window `[1, 3, 4, 5]` is valid, then the algorithm removes `1`, leaving `[3, 4, 5]` with sum 12. It cannot remove another house because the sum would fall below 12. Thus three houses are necessary for this endpoint, corresponding to distance `3 - 1 = 2`.

## Sample 2

For `x = 13` and `a = [5, 1, 2, 3, 4]`, the total sum is 15, but no proper subarray reaches 13. The whole array is required.

| `right` | Added value | `current_sum` | `left` | Best window length |
| --- | --- | --- | --- | --- |
| 0 | 5 | 5 | 0 | not found |
| 1 | 1 | 6 | 0 | not found |
| 2 | 2 | 8 | 0 | not found |
| 3 | 3 | 11 | 0 | not found |
| 4 | 4 | 15 | 0 | 5 |

When the last house is added, the complete array reaches 15. Removing the first house would leave only 10, which is below the target, so the five-house window is minimal. Its walking distance is `5 - 1 = 4`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | The right pointer moves from left to right once, and the left pointer also moves only forward, so each house is added and removed at most once. |
| Space | `O(n)` | The array is stored in memory so the left endpoint can remove its values. |

With `n <= 100000`, roughly `200000` pointer movements are enough for the sliding-window portion. This is comfortably within the required time limit, and storing `100000` integers is well within the memory limit.

# Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    x, n = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    best = n + 1

    for right in range(n):
        current_sum += a[right]

        while current_sum >= x:
            best = min(best, right - left + 1)
            current_sum -= a[left]
            left += 1

    print(-1 if best == n + 1 else best - 1)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples, interpreted according to the displayed input.
assert run("12 5\n1 3 4 5 2\n") == "2", "sample 1"
assert run("13 5\n5 1 2 3 4\n") == "4", "sample 2"
assert run("6 5\n1 1 1 1 1\n") == "-1", "sample 3"

# Minimum-size input, one house is enough, so no walking is required.
assert run("7 1\n7\n") == "0", "single house exactly reaches target"

# One house is enough even though other houses exist.
assert run("5 3\n2 5 1\n") == "0", "single-house window"

# Entire array is required.
assert run("10 4\n1 2 3 4\n") == "3", "whole array required"

# All values equal, target reached by the first three houses.
assert run("9 5\n3 3 3 3 3\n") == "2", "equal values"

# Target cannot be reached.
assert run("100 4\n10 20 30 39\n") == "-1", "insufficient total"

# Maximum-size input.
n = 100000
assert run(f"{n} {n}\n" + " ".join(["1"] * n) + "\n") == str(n - 1), \
    "maximum-size all-equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 1 / 7` | `0` | Minimum size and zero walking distance |
| `5 3 / 2 5 1` | `0` | A single house satisfying the target |
| `10 4 / 1 2 3 4` | `3` | The entire array is required and catches `length` versus `distance` errors |
| `9 5 / 3 3 3 3 3` | `2` | Repeated values and exact shrinking |
| `100 4 / 10 20 30 39` | `-1` | Total gold is insufficient |
| `100000 100000 / 1 ... 1` | `99999` | Maximum `n` and linear-time behavior |

# Edge Cases

A single house can satisfy the target. For `x = 5`, `n = 3`, and `a = [2, 7, 1]`, the window reaches the target when `right = 1`. The algorithm records a window length of `1` after removing the preceding `2` from the window. It cannot remove the `7` because that would make the sum zero, so `best = 1` and the answer is `best - 1 = 0`. The key detail is that walking from a house to itself costs zero.

If the total amount of gold is insufficient, the shrinking loop is never able to produce a valid final answer. For `x = 10` and `a = [2, 3, 4]`, the largest sum reached is 9. `best` remains at its sentinel value, so the algorithm prints `-1` instead of treating the last partial window as a solution.

When the entire array is required, the window reaches the target only at the last position. For `x = 10` and `a = [1, 2, 3, 4]`, the sum becomes 10 at `right = 3`. The window has length 4, and removing `1` immediately drops the sum to 9, so it is minimal. The answer is `4 - 1 = 3`, which represents the three movements between the four houses.

The distance conversion is also relevant when the target is reached by several houses. If the optimal window is `[l, r]`, there are `r - l + 1` houses but only `r - l` steps between the first and last house. Returning the window length directly introduces an off-by-one error on every valid answer, including the simplest case where the correct distance is zero.

The positivity of the array is what makes the sliding window valid. If negative values were allowed, removing the leftmost value could increase the sum, and the monotonic shrinking argument would no longer hold. Under the given constraints every house contributes a positive amount, so each pointer only moves forward and the linear bound is guaranteed.
