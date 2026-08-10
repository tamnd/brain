---
title: "CF 102397D - Bashar and the bad land (Easy)"
description: "There are n houses arranged in a line, and house i contains a[i] coins. Bashar may choose any house as his starting point and any house as his stopping point. While walking between them, he visits every house on that segment and collects all its coins."
date: "2026-08-10T17:58:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "D"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 414
verified: true
draft: false
---

[CF 102397D - Bashar and the bad land (Easy)](https://codeforces.com/problemset/problem/102397/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` houses arranged in a line, and house `i` contains `a[i]` coins. Bashar may choose any house as his starting point and any house as his stopping point. While walking between them, he visits every house on that segment and collects all its coins.

The task is to find the minimum walking distance needed to collect at least `x` coins. If the chosen segment starts at house `l` and ends at house `r`, its walking distance is `r - l`, because adjacent houses are one unit apart. If no segment contains enough coins, the answer is `-1`.

The input contains `x` and `n`, followed by the `n` coin values. The constraints have `n <= 1000`, so even an `O(n^2)` algorithm performs at most about half a million segment checks, which is easily manageable. The small constraint makes a brute-force solution possible, but the structure of the problem also allows an `O(n)` solution.

The fact that every `a[i]` is positive is the key property. Adding another house to a segment can only increase its total, and removing a house from the left can only decrease it. This monotonic behavior lets us maintain a moving interval without reconsidering every possible pair of endpoints.

There are several boundary cases that can cause an incorrect implementation to silently return the wrong distance. If one house already contains enough coins, for example

```
5 1
5
```

the answer is `0`, because Bashar can start and stop at the same house. An implementation that initializes the answer to at least `1` would be wrong.

A second case is when the entire array is still insufficient:

```
6 5
1 1 1 1 1
```

The total is only `5`, so the correct output is `-1`. A careless sliding-window implementation might leave its initial answer unchanged and print an invalid distance.

A third case tests the distance versus the number of houses. For

```
7 3
2 5 1
```

the segment containing the first two houses has `7` coins. It contains two houses, but Bashar walks only from house `1` to house `2`, so the answer is `1`, not `2`.

## Approaches

The direct approach is to try every possible starting house and extend the ending house one position at a time. For each pair of endpoints, we can calculate or maintain the sum and check whether it reaches `x`. There are `n(n+1)/2` contiguous segments, so the worst case has roughly `500,500` segments when `n = 1000`. With prefix sums, each segment can be checked in constant time, giving an `O(n^2)` algorithm. It is correct because every possible interval is explicitly considered, and the smallest valid interval is selected.

The brute-force method works because the answer is guaranteed to be one of the contiguous segments. However, it does unnecessary work because many intervals overlap. If an interval `[l, r]` already has enough coins, extending it farther right cannot improve its walking distance. More importantly, since all coin values are positive, once a window reaches the required sum, we can safely move its left boundary forward and see whether it can become shorter.

This gives a sliding-window solution. We maintain a window `[left, right]` and its current coin sum. As `right` moves forward, we add the new house to the window. Whenever the sum is at least `x`, the current window is valid, so we record its distance and repeatedly remove houses from the left while the window remains valid. This process examines every house only a constant number of times, reducing the complexity to `O(n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted for the easy constraints |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `left = 0`, `current_sum = 0`, and `answer = n` as a value larger than every possible walking distance. The window will represent the houses from `left` through the current right endpoint.
2. Move `right` from `0` through `n - 1`. Add `a[right]` to `current_sum`, because the new right endpoint has just entered the active window.
3. While `current_sum >= x`, the current window already contains enough coins. Its walking distance is `right - left`, so update `answer` with the smaller of the current answer and this distance.
4. Remove `a[left]` from `current_sum` and increment `left`. This tries to make the valid window shorter. We keep doing this while the remaining window still contains at least `x` coins.
5. After processing every possible right endpoint, check whether `answer` was updated. If not, no contiguous segment reached `x`, so print `-1`; otherwise print `answer`.

The reason we can discard the old left endpoint permanently is that all coin values are positive. Once `[left, right]` has enough coins, keeping `left` fixed while extending `right` can never produce a shorter interval than the one we already found. Moving `left` forward is the only way to improve the distance.

### Why it works

At every point, `current_sum` is exactly the sum of the houses in the current window `[left, right]`. Whenever that sum reaches `x`, the window is valid, and we record its distance. We then move `left` forward as far as possible while preserving validity, so for this particular `right`, the resulting window is the shortest valid window ending at `right`. Every possible right endpoint is processed, so the globally shortest valid segment must be considered. Since all values are positive, no discarded left endpoint can later become useful after the right endpoint moves forward, which is what makes the one-pass algorithm correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, n = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    answer = n

    for right in range(n):
        current_sum += a[right]

        while current_sum >= x:
            answer = min(answer, right - left)
            current_sum -= a[left]
            left += 1

    if answer == n:
        print(-1)
    else:
        print(answer)

if __name__ == "__main__":
    solve()
```

The first line reads the required number of coins and the number of houses. The array is then stored so that the sliding window can remove values from its left boundary in constant time.

The main loop adds `a[right]` exactly when house `right` enters the window. The inner `while` loop runs only while the current segment has enough coins. Before removing `a[left]`, we record the current distance `right - left`, which is the distance between the two endpoint houses.

The order here matters. We must evaluate the valid window before removing its leftmost house. Otherwise, a one-house solution could be skipped. For example, if `a[left] >= x`, the correct distance is `0`, and that value must be recorded before the house is removed.

The initial answer is `n`. The maximum possible distance is `n - 1`, so `n` is safely outside the range of real answers. After the scan, an unchanged value means no valid window was ever found.

Python integers do not overflow, and the largest possible total is only `1000 * 1000 = 10^6` anyway.

## Worked Examples

### Sample 1

The sample is interpreted as `x = 12`, `n = 5`, with coin values `[1, 3, 4, 5, 2]`.

| right | left | current_sum before shrinking | Valid window | answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | No | 5 |
| 1 | 0 | 4 | No | 5 |
| 2 | 0 | 8 | No | 5 |
| 3 | 0 | 13 | Yes, `[0,3]` | 3 |
| 3 | 1 | 12 | Yes, `[1,3]` | 2 |
| 4 | 2 | 11 | No | 2 |

When `right = 3`, the first valid window is `[0, 3]`, containing `1 + 3 + 4 + 5 = 13` coins and having distance `3`. Removing the first house leaves `[1, 3]`, whose sum is exactly `12`, and its distance is `2`.

The stated sample explanation describes walking from the second house to the fourth house, which corresponds to this final window. Thus the answer is `2` under the definition of distance as the difference between house positions. The supplied statement's displayed sample output is corrupted in the prompt, but the intended result from the described movement is `2`.

### Sample 2

Here `x = 13`, `n = 5`, and the array is `[5, 1, 2, 3, 4]`.

| right | left | current_sum before shrinking | Valid window | answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 5 | No | 5 |
| 1 | 0 | 6 | No | 5 |
| 2 | 0 | 8 | No | 5 |
| 3 | 0 | 11 | No | 5 |
| 4 | 0 | 15 | Yes, `[0,4]` | 4 |
| 4 | 1 | 10 | No | 4 |

The only valid segment is the entire array, because removing the first house reduces the sum from `15` to `10`, below the required `13`. The distance from house `1` to house `5` is `4`.

This example demonstrates why the algorithm does not shrink a window blindly. It removes the leftmost house only after recording the current valid interval, and it stops immediately once removing another house would make the sum too small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | `right` advances `n` times, while `left` also advances at most `n` times. |
| Space | O(n) | The input array is stored; the sliding-window state itself uses O(1) extra space. |

With `n <= 1000`, this is comfortably within the given limits. Even the quadratic solution would fit the easy constraints, but the linear solution is simpler once the positive-value property is recognized and also scales naturally to the harder version.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    x, n = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    answer = n

    for right in range(n):
        current_sum += a[right]

        while current_sum >= x:
            answer = min(answer, right - left)
            current_sum -= a[left]
            left += 1

    print(-1 if answer == n else answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

# Provided samples, reconstructed from the formatting in the statement.
assert run("12 5\n1 3 4 5 2\n") == "2", "sample 1"
assert run("13 5\n5 1 2 3 4\n") == "4", "sample 2"
assert run("6 5\n1 1 1 1 1\n") == "-1", "sample 3"

# Minimum-size input, one house is already enough.
assert run("7 1\n7\n") == "0", "single house"

# One house in the middle is enough, catching endpoint handling.
assert run("5 3\n2 5 1\n") == "0", "single-house window"

# The answer requires the last two houses.
assert run("7 4\n1 1 4 3\n") == "1", "last two houses"

# Every house is needed, so the answer is n - 1.
assert run("10 4\n1 2 3 4\n") == "3", "entire array"

# Maximum-size input, all equal values.
assert run("1000 1000\n" + "1 " * 999 + "1\n") == "999", "maximum size"

# Exact boundary: a segment reaches x exactly.
assert run("9 5\n2 3 4 1 1\n") == "2", "exact sum"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 1 / 7` | `0` | Minimum-size input and zero walking distance |
| `5 3 / 2 5 1` | `0` | A single house in the middle is sufficient |
| `7 4 / 1 1 4 3` | `1` | Correct handling of the final two houses |
| `10 4 / 1 2 3 4` | `3` | The entire array is required |
| `1000 1000 / all ones` | `999` | Maximum-size input and largest possible answer |
| `9 5 / 2 3 4 1 1` | `2` | Exact sum and boundary shrinking |

## Edge Cases

A single house containing enough coins must produce distance `0`. For

```
7 1
7
```

the algorithm adds the only value, sees that the sum is at least `7`, records `right - left = 0`, and then removes that house. The final answer is `0`.

If the total amount of gold is insufficient, no window ever enters the shrinking loop. For

```
6 5
1 1 1 1 1
```

the final sum reaches only `5`, so `answer` remains equal to its initial value `n`. The algorithm prints `-1`.

A valid window can appear at the very end of the array. For

```
7 4
1 1 4 3
```

the last two houses contain `4 + 3 = 7`. When `right = 3`, the window eventually shrinks to `[2, 3]`, and the recorded distance is `3 - 2 = 1`. This catches implementations that accidentally stop before processing the final house.

The distance is one less than the number of houses in a segment. For

```
10 4
1 2 3 4
```

all four houses are required because their total is exactly `10`. The algorithm records `right - left = 3`, not `4`. This distinction is essential because Bashar walks between houses, rather than counting the houses themselves.

Finally, an exact match must be treated as valid. For

```
9 5
2 3 4 1 1
```

the first three houses contain exactly `9` coins, so the algorithm records distance `2`. Using `>` instead of `>=` would incorrectly reject this segment and is a common boundary error in sliding-window implementations.
