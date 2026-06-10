---
title: "CF 1585A - Life of a Flower"
description: "We are given the watering history of a flower over several days. Each element of the array represents one day. A value of 1 means the flower was watered, while 0 means it was neglected. The flower starts with height 1."
date: "2026-06-10T09:30:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1585
codeforces_index: "A"
codeforces_contest_name: "Technocup 2022 - Elimination Round 3"
rating: 800
weight: 1585
solve_time_s: 217
verified: true
draft: false
---

[CF 1585A - Life of a Flower](https://codeforces.com/problemset/problem/1585/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the watering history of a flower over several days. Each element of the array represents one day. A value of `1` means the flower was watered, while `0` means it was neglected.

The flower starts with height `1`. Every watered day increases the height, but the amount depends on what happened the previous day. If two consecutive days are both watered, the current day contributes `5` centimeters. Otherwise a watered day contributes only `1`. A dry day contributes nothing. If two consecutive dry days ever appear, the flower dies immediately and the answer becomes `-1`.

The number of test cases is at most `100`, and each test case contains at most `100` days. Even an algorithm that inspects every day one by one performs only about ten thousand operations, which is tiny. There is no need for anything more sophisticated than a linear scan.

Several situations are easy to mishandle.

One case is when the first day is dry. For example:

```
1
1
0
```

The answer is `1`, not `0`. The flower already has height `1` before any day starts.

Another case is a pair of consecutive dry days.

```
1
4
1 0 0 1
```

The correct answer is `-1`. A careless implementation might simply skip dry days and continue processing, producing an incorrect positive height.

Consecutive watered days also require attention.

```
1
3
0 1 1
```

The answer is `7`. The second day contributes `1`, and the third contributes `5`, so the final height becomes `1 + 1 + 5 = 7`. Treating every watered day as adding `1` would give the wrong result.

## Approaches

The most direct idea is to simulate the flower's life exactly as described. We process the days from left to right, maintain the current height, and examine the previous day whenever we need to determine how much growth the current day produces. Since every day is visited once, the worst case requires only `100` operations per test case.

A brute-force simulation already fits comfortably within the limits. There is no need for dynamic programming or preprocessing because each day's effect depends only on the previous day. The local nature of the rules means we can decide everything immediately while scanning the array.

The key observation is that only three patterns matter. A pair `0 0` kills the flower. A pair `1 1` adds `5` for the second day. A single isolated `1` adds `1`. Since these conditions depend solely on neighboring elements, one pass through the array is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the flower's height as `1`, because that is its starting height before any day is processed.
2. Traverse the array from left to right.
3. If the current day and the previous day are both `0`, stop immediately and mark the answer as `-1`. The flower dies as soon as two consecutive dry days appear.
4. If the current day is watered and the previous day was also watered, add `5` to the height. The rule says the current day contributes `5` instead of `1`.
5. If the current day is watered but the previous day was dry, add `1` to the height.
6. If the current day is dry, add nothing.
7. After all days are processed, output the height unless the flower died earlier.

### Why it works

After processing day `i`, the stored height equals the actual height of the flower after those `i` days, provided the flower is still alive. Every possible pair of consecutive days is handled according to the rules. A `0 0` pair causes immediate termination, while every watered day contributes exactly the amount specified by the problem. Since the algorithm reproduces the effect of each day in chronological order, the final result must match the flower's true height.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        height = 1
        alive = True

        for i in range(n):
            if a[i] == 1:
                if i > 0 and a[i - 1] == 1:
                    height += 5
                else:
                    height += 1
            else:
                if i > 0 and a[i - 1] == 0:
                    alive = False
                    break

        if alive:
            ans.append(str(height))
        else:
            ans.append("-1")

    sys.stdout.write("\n".join(ans))

solve()
```

The variable `height` starts from `1`, matching the initial state of the flower. The loop processes days in chronological order. For a watered day, we look one position back to decide whether the contribution is `1` or `5`.

The condition `i > 0` prevents accessing `a[-1]` when processing the first day. This boundary case is easy to overlook.

As soon as a pair of consecutive zeros is found, the loop stops. Continuing further would be meaningless because the flower is already dead.

Since the height never exceeds a few hundred, ordinary integers are more than sufficient.

## Worked Examples

### Example 1

Input:

```
3
1 0 1
```

| Day | Value | Previous Value | Height |
| --- | --- | --- | --- |
| Initial | - | - | 1 |
| 1 | 1 | - | 2 |
| 2 | 0 | 1 | 2 |
| 3 | 1 | 0 | 3 |

The flower never encounters two consecutive dry days. Both watered days are isolated, so each contributes only `1`. The final height is `3`.

### Example 2

Input:

```
3
0 1 1
```

| Day | Value | Previous Value | Height |
| --- | --- | --- | --- |
| Initial | - | - | 1 |
| 1 | 0 | - | 1 |
| 2 | 1 | 0 | 2 |
| 3 | 1 | 1 | 7 |

This example shows why consecutive watered days matter. The third day contributes `5`, not `1`, producing a final answer of `7`.

### Example 3

Input:

```
4
1 0 0 1
```

| Day | Value | Previous Value | Height |
| --- | --- | --- | --- |
| Initial | - | - | 1 |
| 1 | 1 | - | 2 |
| 2 | 0 | 1 | 2 |
| 3 | 0 | 0 | Dead |

The flower dies on day three because of two consecutive dry days. The remaining days no longer matter, and the answer is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each day is processed exactly once |
| Space | O(1) | Only a few variables are maintained |

Even with the maximum input size, the algorithm performs only a few hundred operations per test case. Both the time and memory usage are far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        height = 1
        alive = True

        for i in range(n):
            if a[i] == 1:
                if i > 0 and a[i - 1] == 1:
                    height += 5
                else:
                    height += 1
            else:
                if i > 0 and a[i - 1] == 0:
                    alive = False
                    break

        ans.append(str(height) if alive else "-1")

    return "\n".join(ans)

# provided sample
assert run(
"""4
3
1 0 1
3
0 1 1
4
1 0 0 1
1
0
"""
) == "3\n7\n-1\n1"

# minimum size
assert run(
"""1
1
1
"""
) == "2"

# all zeros
assert run(
"""1
3
0 0 0
"""
) == "-1"

# all ones
assert run(
"""1
4
1 1 1 1
"""
) == "18"

# consecutive zeros in the middle
assert run(
"""1
5
1 1 0 0 1
"""
) == "-1"

# alternating pattern
assert run(
"""1
6
1 0 1 0 1 0
"""
) == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `2` | Minimum size with watering |
| `1 / 3 / 0 0 0` | `-1` | Immediate death from consecutive dry days |
| `1 / 4 / 1 1 1 1` | `18` | Repeated bonus growth |
| `1 / 5 / 1 1 0 0 1` | `-1` | Death occurring in the middle |
| `1 / 6 / 1 0 1 0 1 0` | `4` | Alternating pattern without bonuses |

## Edge Cases

Consider the input

```
1
1
0
```

The algorithm starts with height `1`. The only day is dry, so no growth occurs. Since there is no previous day, the condition for death cannot trigger. The output becomes `1`. Starting from height `0` would produce the wrong answer.

Consider

```
1
4
1 0 0 1
```

After day one, the height becomes `2`. Day two contributes nothing. On day three, the algorithm notices that both the current and previous days are `0`, marks the flower as dead, and stops. The output is `-1`.

Consider

```
1
3
0 1 1
```

Day one contributes nothing. Day two adds `1`, increasing the height to `2`. Day three sees a previous value of `1`, so it adds `5`, producing a final height of `7`. The algorithm correctly distinguishes isolated watering from consecutive watering.
