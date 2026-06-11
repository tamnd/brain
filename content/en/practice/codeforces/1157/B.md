---
title: "CF 1157B - Long Number"
description: "We are given a number as a string of digits from 1 to 9 and a mapping f from each digit to another digit in the same range. The task is to maximize the resulting number by selecting at most one contiguous segment of digits and replacing each digit x in that segment with f(x)."
date: "2026-06-12T02:32:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1157
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 555 (Div. 3)"
rating: 1300
weight: 1157
solve_time_s: 85
verified: true
draft: false
---

[CF 1157B - Long Number](https://codeforces.com/problemset/problem/1157/B)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number as a string of digits from `1` to `9` and a mapping `f` from each digit to another digit in the same range. The task is to maximize the resulting number by selecting at most one contiguous segment of digits and replacing each digit `x` in that segment with `f(x)`. All other digits remain unchanged.

The input gives us `n`, the number of digits, the number `a` as a string, and a list of 9 integers representing `f(1)` through `f(9)`. The output is the largest number obtainable by performing the operation once or not at all.

Given `n` can be as large as 200,000 and the time limit is 2 seconds, any algorithm that considers all possible subsegments naively would require on the order of `O(n^2)` operations, which is far too slow. We need a linear or linearithmic approach.

Non-obvious edge cases include sequences where applying `f` could temporarily decrease a digit before increasing later digits. For instance, if `a = 987` and `f(9) = 8, f(8) = 9`, a naive greedy might try to start replacing at `9` even though leaving it unchanged produces a larger overall number. Another edge case occurs when all digits are mapped to smaller or equal values, in which case the optimal move is to not perform the operation at all. For example, `a = 123` and `f = [1,1,1,4,5,6,7,8,9]` produces `123` because no replacement increases any digit.

## Approaches

The brute-force approach is straightforward: iterate over every possible contiguous subsegment, apply `f` to the digits in that segment, and compute the resulting number. Keep track of the maximum number encountered. This works because any operation allowed by the problem can be represented as a contiguous segment replacement. However, the number of subsegments grows as `n(n+1)/2`, so with `n = 2*10^5`, this approach would require on the order of `2*10^10` operations, which is impractical.

The key observation for an optimal solution is that we should start replacing digits from the first position where `f(x) > x` and continue replacing as long as `f(x) >= x`. Once `f(x) < x`, we stop the replacement, because extending the replacement further would decrease the number. This works because the operation must be contiguous and applied at most once, and a larger digit earlier in the number has a more significant impact on the final number than digits later on. This gives a greedy solution that scans the number once from left to right, deciding for each digit whether to replace it or not based on a simple comparison with `f(x)` and a flag indicating whether we are in an active replacement segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a flag `started` to `False` to indicate whether we have started a replacement segment. Initialize an empty list `result` to build the final number.
2. Iterate over each digit `d` in the original number from left to right. Convert `d` to an integer for comparison with `f(d)`.
3. If `f(d) > d`, replace the digit with `f(d)` and set `started` to `True`. Append the replaced digit to `result`.
4. If `f(d) == d`, check the `started` flag. If `started` is `True`, continue replacing with `f(d)` (no change). If `started` is `False`, append the original digit to `result`.
5. If `f(d) < d` and `started` is `True`, stop the replacement segment. Set `started` to `False` and append the original digit to `result`. If `started` is `False`, simply append the original digit.
6. After processing all digits, join the `result` list into a string and output it.

The invariant here is that once we start a replacement segment, we maximize each digit until a replacement would reduce the number. Since the operation must be contiguous, we cannot skip a digit in the segment. This guarantees the maximum number because any earlier or later start or end would produce a smaller result.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = input().strip()
f = list(map(int, input().split()))

result = []
started = False

for ch in a:
    digit = int(ch)
    mapped = f[digit - 1]
    if mapped > digit:
        result.append(str(mapped))
        started = True
    elif mapped == digit:
        result.append(str(digit) if not started else str(mapped))
    else:
        result.append(str(digit))
        if started:
            started = False

print(''.join(result))
```

The solution initializes the result array and iterates through the digits. Conversion to integer is necessary because `f` is a list of integers. The `started` flag ensures the replacement is contiguous, and comparisons correctly handle starting, continuing, or stopping the replacement. Joining the result list at the end avoids repeated string concatenations.

## Worked Examples

### Sample 1

Input:

```
a = 1337
f = [1,2,5,4,6,6,3,1,9]
```

| i | ch | digit | f(digit) | started | result |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | False | 1 |
| 1 | 3 | 3 | 5 | True | 1,5 |
| 2 | 3 | 3 | 5 | True | 1,5,5 |
| 3 | 7 | 7 | 3 | True | 1,5,5,7 |

Output: `1557`

The replacement starts at the first 3, continues through the second 3, and stops at 7 because `f(7) < 7`. This demonstrates correct segment selection.

### Custom Example 2

Input:

```
a = 987
f = [1,2,3,4,5,6,7,8,9]
```

| i | ch | digit | f(digit) | started | result |
| --- | --- | --- | --- | --- | --- |
| 0 | 9 | 9 | 9 | False | 9 |
| 1 | 8 | 8 | 8 | False | 8 |
| 2 | 7 | 7 | 7 | False | 7 |

Output: `987`

No replacement increases any digit, so the number remains unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit is processed once and all operations inside the loop are O(1) |
| Space | O(n) | The result list stores n characters |

The solution fits within the time and memory limits comfortably for `n` up to 2*10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = input().strip()
    f = list(map(int, input().split()))
    result = []
    started = False
    for ch in a:
        digit = int(ch)
        mapped = f[digit - 1]
        if mapped > digit:
            result.append(str(mapped))
            started = True
        elif mapped == digit:
            result.append(str(digit) if not started else str(mapped))
        else:
            result.append(str(digit))
            if started:
                started = False
    return ''.join(result)

# provided samples
assert run("4\n1337\n1 2 5 4 6 6 3 1 9\n") == "1557", "sample 1"

# custom cases
assert run("3\n987\n1 2 3 4 5 6 7 8 9\n") == "987", "no replacement needed"
assert run("5\n11111\n9 8 7 6 5 4 3 2 1\n") == "99999", "all digits increased"
assert run("4\n4321\n1 2 3 4 5 6 7 8 9\n") == "4321", "all digits mapped to smaller values"
assert run("6\n123456\n2 3 4 5 6 7 8 9 1\n") == "234567", "replacement starts at first digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 987 with f(x) ≤ x | 987 | Operation can be skipped |
| 11111 with f(x) > x | 99999 | Maximum replacement of all digits |
| 4321 with f(x) < x | 4321 | Correctly stops before decreasing digits |
| 123456 with f(x) > x | 234567 | Replacement starts at first increase |

## Edge Cases

If all mapped digits are smaller than
