---
title: "CF 106189D - An oscillating subsequence"
description: "We are given an integer sequence and may delete any elements while preserving the order of the remaining ones. The goal is to keep as many elements as possible so that in the resulting subsequence every internal element is a strict peak or a strict valley."
date: "2026-06-25T06:47:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106189
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest, 2025"
rating: 0
weight: 106189
solve_time_s: 39
verified: true
draft: false
---

[CF 106189D - An oscillating subsequence](https://codeforces.com/problemset/problem/106189/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer sequence and may delete any elements while preserving the order of the remaining ones.

The goal is to keep as many elements as possible so that in the resulting subsequence every internal element is a strict peak or a strict valley. For every position inside the subsequence, its value must be either larger than both neighbors or smaller than both neighbors. In other words, the differences between consecutive elements must alternate in sign.

The output is not the subsequence itself. We must print the indices of the chosen elements in the original array. If no oscillating subsequence of length at least three exists, we print `0`.

The array length can reach 50,000. A quadratic dynamic programming solution would require roughly 2.5 billion comparisons in the worst case, which is far beyond the available time. Anything around `O(n²)` is ruled out immediately. A linear or `O(n log n)` solution is required.

The tricky cases come from equal values and long monotone runs.

Consider:

```
3
1 1 2
```

The correct answer is `0`. A careless implementation that only checks increasing versus decreasing might incorrectly treat the first two values as a valid direction change.

Consider:

```
5
1 2 3 4 5
```

Every subsequence is monotone. No oscillation of length at least three exists, so the answer is `0`.

Consider:

```
5
1 5 3 4 2
```

The whole sequence already alternates:

```
1 < 5 > 3 < 4 > 2
```

The answer contains all five indices.

Consider:

```
6
1 4 7 5 2 6
```

The values `4` and `5` are not both needed. The longest oscillating subsequence keeps only the turning points:

```
1 < 7 > 2 < 6
```

A naive strategy that keeps every change of value would not produce a valid oscillation.

## Approaches

The brute-force idea is dynamic programming.

For every position and every previous position, we could try to extend a subsequence while remembering whether the last step was increasing or decreasing. This correctly finds the longest oscillating subsequence, but it requires examining all pairs of indices. With `n = 50,000`, the worst-case work is on the order of `50,000²`, which is completely infeasible.

The key observation is that inside a strictly increasing run, only the last element matters. Suppose we currently have:

```
... < 3 < 5 < 8
```

If we want a future decrease, keeping `8` is always at least as good as keeping `5` or `3`, because `8` gives more freedom for the next downward step.

The same reasoning applies to decreasing runs. Inside

```
... > 10 > 7 > 4
```

only the smallest endpoint is useful.

This means every monotone segment can be compressed to its endpoint. The elements that survive are exactly the turning points, peaks and valleys. A greedy algorithm can maintain this online.

We build the answer indices from left to right.

Whenever the last three considered values are monotone:

```
x ≤ y ≤ z
```

or

```
x ≥ y ≥ z
```

the middle value `y` can never be a peak or valley in an optimal oscillating subsequence. We remove it and keep the more extreme endpoint.

After processing the whole array, the remaining indices form a maximum-length oscillating subsequence. This is the same greedy principle used in the classical wiggle subsequence problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP | O(n²) | O(n²) or O(n) | Too slow |
| Greedy Turning Points | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start the answer list with index `0`.
2. Process indices from left to right.
3. For the current index `i`, check the last two selected indices and `i`.
4. Let their values be `x`, `y`, and `z`.
5. If `x ≤ y ≤ z`, then `y` lies inside a non-decreasing segment. Remove `y` and replace it with `i`.
6. If `x ≥ y ≥ z`, then `y` lies inside a non-increasing segment. Remove `y` and replace it with `i`.
7. Otherwise, the direction changes between `y` and `z`. The point `y` becomes a peak or valley, so append `i`.
8. After all indices are processed, the stored indices describe a longest oscillating subsequence.
9. If fewer than three indices remain, print `0`. Otherwise print the length and the indices.

### Why it works

The invariant is that after processing any prefix of the array, the stored indices form the longest possible oscillating subsequence ending inside that prefix.

Whenever three consecutive candidate values satisfy

```
x ≤ y ≤ z
```

the middle value is never useful. Any future element that can follow `y` can also follow `z`, and `z` is at least as extreme. Replacing `y` with `z` cannot reduce the maximum achievable oscillating length.

The same argument holds for

```
x ≥ y ≥ z
```

where the newest value is at least as useful as the middle one.

As a result, every removed element is provably redundant. Every kept internal element corresponds to a genuine direction change, making it a peak or valley. Since only redundant points are discarded, the resulting subsequence has maximum possible length.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

ans = [0]

for i in range(1, n):
    while len(ans) >= 2:
        x = a[ans[-2]]
        y = a[ans[-1]]
        z = a[i]

        if (x <= y <= z) or (x >= y >= z):
            ans.pop()
        else:
            break

    ans.append(i)

if len(ans) < 3:
    print(0)
else:
    print(len(ans))
    print(*ans)
```

The list `ans` stores indices, not values, because the problem asks for positions in the original sequence.

The `while` loop is the heart of the greedy strategy. If the newest value continues the current monotone trend, the previous endpoint is no longer useful and is removed.

Using a `while` instead of a single `if` is important. After removing one index, a new triple is formed and may also be monotone. The process continues until the last selected point becomes a genuine turning point or only one previous point remains.

Equal values are handled naturally by the conditions

```
x <= y <= z
x >= y >= z
```

This prevents flat segments from creating fake oscillations.

Every index is inserted once and removed at most once, so the total running time remains linear.

## Worked Examples

### Example 1

Input:

```
5
1 4 7 5 2
```

| Current index | Value | Stored indices | Stored values |
| --- | --- | --- | --- |
| 0 | 1 | [0] | [1] |
| 1 | 4 | [0,1] | [1,4] |
| 2 | 7 | [0,2] | [1,7] |
| 3 | 5 | [0,2,3] | [1,7,5] |
| 4 | 2 | [0,2,4] | [1,7,2] |

The value `4` disappears because it lies inside an increasing run. Later, `5` disappears because it lies inside a decreasing run. The surviving elements are exactly the turning points.

### Example 2

Input:

```
6
1 3 2 4 3 5
```

| Current index | Value | Stored indices | Stored values |
| --- | --- | --- | --- |
| 0 | 1 | [0] | [1] |
| 1 | 3 | [0,1] | [1,3] |
| 2 | 2 | [0,1,2] | [1,3,2] |
| 3 | 4 | [0,1,2,3] | [1,3,2,4] |
| 4 | 3 | [0,1,2,3,4] | [1,3,2,4,3] |
| 5 | 5 | [0,1,2,3,4,5] | [1,3,2,4,3,5] |

Every internal element is already a peak or valley, so nothing is removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every index is pushed once and popped at most once |
| Space | O(n) | The answer indices are stored |

With `n = 50,000`, a linear scan is easily fast enough for the given limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    ans = [0]

    for i in range(1, n):
        while len(ans) >= 2:
            x = a[ans[-2]]
            y = a[ans[-1]]
            z = a[i]

            if (x <= y <= z) or (x >= y >= z):
                ans.pop()
            else:
                break

        ans.append(i)

    out = []

    if len(ans) < 3:
        out.append("0")
    else:
        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# sample-like cases
assert run("3\n1 3 2\n") == "3\n0 1 2"
assert run("3\n1 2 3\n") == "0"

# minimum size
assert run("1\n5\n") == "0"

# all equal
assert run("5\n7 7 7 7 7\n") == "0"

# already oscillating
assert run("5\n1 5 2 6 3\n") == "5\n0 1 2 3 4"

# long monotone run compressed to endpoints
assert run("6\n1 4 7 5 2 6\n") == "4\n0 2 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `0` | Minimum size |
| `7 7 7 7 7` | `0` | Equal values do not create oscillations |
| `1 5 2 6 3` | All indices | Already optimal sequence |
| `1 4 7 5 2 6` | Turning points only | Compression of monotone segments |

## Edge Cases

Consider:

```
3
1 1 2
```

Processing `2` creates the pattern:

```
1 ≤ 1 ≤ 2
```

The middle index is removed. The final index set becomes:

```
[0, 2]
```

Its length is only two, so the algorithm prints `0`. Equal values never generate a false peak or valley.

Consider:

```
3
1 2 3
```

The pattern is always increasing:

```
1 ≤ 2 ≤ 3
```

The middle point is discarded and only endpoints remain. Again the final length is two, so the answer is `0`.

Consider:

```
6
5 4 3 2 1 0
```

Every new value continues the same decreasing trend. The algorithm repeatedly removes the previous endpoint and keeps the newest one. The final subsequence contains only the first and last indices, which is correct because no oscillation of length at least three exists.

Consider:

```
5
1 3 2 4 1
```

Every internal element is already a strict peak or valley:

```
1 < 3 > 2 < 4 > 1
```

None of the monotonicity conditions trigger, all indices remain, and the algorithm returns the full sequence.
