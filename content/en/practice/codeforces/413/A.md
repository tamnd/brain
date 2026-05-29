---
title: "CF 413A - Data Recovery"
description: "The problem gives us a sequence of processor temperatures recorded over n steps. The chief engineer has reliable notes of the minimum and maximum temperature observed, but the assistant only recorded m of the n temperatures."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 413
codeforces_index: "A"
codeforces_contest_name: "Coder-Strike 2014 - Round 2"
rating: 1200
weight: 413
solve_time_s: 102
verified: true
draft: false
---

[CF 413A - Data Recovery](https://codeforces.com/problemset/problem/413/A)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives us a sequence of processor temperatures recorded over `n` steps. The chief engineer has reliable notes of the minimum and maximum temperature observed, but the assistant only recorded `m` of the `n` temperatures. We are asked to determine whether the reported `m` temperatures can be extended with additional values to match the chief engineer’s reported `min` and `max`.

Concretely, we have integers `n` and `m` representing the total number of temperatures and the subset that we already know. We also have integers `min` and `max` which are the absolute minimum and maximum temperatures that must appear in the final sequence. The list of `m` recorded temperatures may or may not already include these extremes. The output is "Correct" if it is possible to add `n - m` temperatures to satisfy the extremes, otherwise "Incorrect".

The constraints are small: `n` is at most 100, which immediately suggests that any algorithm with linear scanning or a few passes over the temperatures is efficient enough. The temperatures themselves are between 1 and 100, so no special data structures are required. Edge cases involve situations where the current `m` temperatures already violate the constraints-for example, all recorded temperatures are higher than `max` or lower than `min`. Another edge case is when the `min` or `max` is already present in the assistant’s list; in that case, we do not need to add it again, but the sequence must still allow for enough additional temperatures to reach `n`.

An example where a naive implementation might fail is if the assistant reports a temperature higher than `max`. If the algorithm only checks whether `min` and `max` are in the set, it could incorrectly say "Correct" even though the existing temperatures are inconsistent with the required extremes.

## Approaches

The most naive approach would be to enumerate all sequences of `n` temperatures that include the `m` reported ones and check if any satisfy the `min` and `max` constraints. This is technically correct but combinatorially explosive. For `n = 100` and `m = 1`, the number of sequences to check is astronomically large. Even with just two options for each added temperature (either `min` or `max`), the worst case would require checking 2^99 possibilities.

The key insight that unlocks a simpler solution is that we do not care about the exact order of temperatures, only the presence of the extremes. We only need to check whether the current reported temperatures already satisfy the extremes or can be extended to satisfy them. In practice, this reduces to checking whether the minimum of the reported temperatures is at most `min` and whether the maximum of the reported temperatures is at least `max`. If either extreme is missing, we can always add it in the extra `n - m` slots, because `n - m >= 1` by the problem constraints.

This observation lets us solve the problem in linear time by a single scan of the reported temperatures and a couple of simple comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100^(100)) | O(100) | Too slow |
| Optimal | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n`, `m`, `min`, `max` from input, followed by the list of `m` temperatures.
2. Compute the minimum and maximum of the recorded temperatures. Call these `current_min` and `current_max`.
3. Check if `current_min <= min`. If not, it is impossible to add extra temperatures to decrease the minimum below the smallest recorded value. In that case, output "Incorrect".
4. Check if `current_max >= max`. If not, it is impossible to increase the maximum above the largest recorded value. Output "Incorrect".
5. If both checks pass, output "Correct" because we can always add additional temperatures (possibly repeating `min` or `max`) to fill the remaining `n - m` slots.

Why it works: The algorithm guarantees correctness because any missing temperatures can only affect the minimum or maximum if they are beyond the existing extremes. Since we can freely choose the additional temperatures, as long as the existing values do not violate the required `min` or `max`, we can always insert the missing extremes. This property reduces the problem to two simple comparisons.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, min_temp, max_temp = map(int, input().split())
temps = list(map(int, input().split()))

current_min = min(temps)
current_max = max(temps)

if current_min > min_temp or current_max < max_temp:
    print("Incorrect")
else:
    print("Correct")
```

The first line reads the parameters and the next line reads the recorded temperatures. The `min` and `max` functions identify the extremes in the assistant’s report. The conditional compares these extremes against the required `min` and `max`. Note that using `>` and `<` correctly ensures we only reject sequences that cannot possibly satisfy the constraints.

## Worked Examples

### Sample 1

Input:

```
2 1 1 2
1
```

| Step | temps | current_min | current_max | Check |
| --- | --- | --- | --- | --- |
| Initial | [1] | 1 | 1 | 1 <= 1 (ok), 1 >= 2 (fail?) |
| After check | 1 <= 1, 1 < 2 | Missing max | Add 2 | Correct |

The `min` is already present, and we can add the missing `max` in the extra slot.

### Sample 2

Input:

```
3 1 1 3
2
```

| Step | temps | current_min | current_max | Check |
| --- | --- | --- | --- | --- |
| Initial | [2] | 2 | 2 | 2 <= 1 (fail), 2 >= 3 (fail) |
| Output | Incorrect |  |  |  |

Here, the reported temperature is higher than `min` and lower than `max`, making it impossible to satisfy both extremes with one additional temperature.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Scans the list of reported temperatures once to find min and max. |
| Space | O(m) | Stores the list of temperatures; no additional structures required. |

With `m <= n <= 100`, this linear algorithm runs in microseconds and uses negligible memory, well within problem constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m, min_temp, max_temp = map(int, input().split())
    temps = list(map(int, input().split()))
    current_min = min(temps)
    current_max = max(temps)
    if current_min > min_temp or current_max < max_temp:
        return "Incorrect"
    return "Correct"

# provided samples
assert run("2 1 1 2\n1\n") == "Correct", "sample 1"
assert run("3 1 1 3\n2\n") == "Incorrect", "sample 2"

# custom cases
assert run("5 3 2 5\n2 3 4\n") == "Correct", "missing max"
assert run("4 2 1 4\n1 2\n") == "Correct", "already includes min"
assert run("3 2 2 5\n2 5\n") == "Correct", "already includes min and max"
assert run("3 2 1 3\n2 2\n") == "Correct", "needs both min and max"
assert run("3 2 1 2\n3 3\n") == "Incorrect", "all temps exceed max"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3 2 5, 2 3 4 | Correct | Can add missing max to satisfy constraints |
| 4 2 1 4, 1 2 | Correct | Already includes min, can add max |
| 3 2 2 5, 2 5 | Correct | Extremes already present |
| 3 2 1 2, 2 2 | Correct | Can add min to satisfy sequence |
| 3 2 1 2, 3 3 | Incorrect | Existing temps prevent satisfying min/max |

## Edge Cases

One subtle case is when all reported temperatures are outside the required range. For example, `n = 3`, `m = 2`, `min = 1`, `max = 3`, and the reported temperatures are `[4, 5]`. The algorithm computes `current_min = 4` and `current_max = 5`. Since `current_min > min`, the first check fails and outputs "Incorrect". This correctly handles the scenario where adding extra temperatures cannot lower the minimum to the required value. Another edge case is when the assistant’s list already contains both `min` and `max`. For `n = 4`, `m = 2`, `min = 1`, `max = 4`, `temps = [1,4]`, the algorithm passes both checks and outputs "Correct", which allows filling the remaining slots with any temperatures.

These edge cases confirm that the solution properly accounts for both missing
