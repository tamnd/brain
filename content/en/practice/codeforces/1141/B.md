---
title: "CF 1141B - Maximal Continuous Rest"
description: "We are given a binary sequence representing a single day, where each position corresponds to an hour. A value of 1 means Polycarp is resting during that hour, while 0 means he is working."
date: "2026-06-12T03:40:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1141
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 547 (Div. 3)"
rating: 900
weight: 1141
solve_time_s: 72
verified: true
draft: false
---

[CF 1141B - Maximal Continuous Rest](https://codeforces.com/problemset/problem/1141/B)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary sequence representing a single day, where each position corresponds to an hour. A value of `1` means Polycarp is resting during that hour, while `0` means he is working. The same sequence repeats forever, so after the last hour of a day, the next hour is again the first hour of the same schedule.

The task is to determine the longest uninterrupted stretch of resting hours if we are allowed to move across the boundary between the end of the day and the beginning of the next one.

A key point is that the sequence is circular. Any segment that starts near the end of the array can continue at the beginning, as if the array were connected end-to-end in a loop.

The input size can be as large as 200,000 hours. That rules out any solution that tries to check every possible starting position and expand outward, since that would lead to quadratic behavior in the worst case. A linear scan is the only realistic target.

A naive mistake happens when one treats the array as linear and ignores wrap-around. For example, in `1 1 0 1 1 1`, the correct answer is 4, because the run `1 1` at the end connects with `1 1 1` at the beginning. A linear scan would incorrectly report 3.

Another common edge case is when the array is entirely zeros except for a single one. The correct answer is 0 since there are no rest hours, and a naive circular merging strategy might incorrectly treat gaps as rest.

## Approaches

A brute-force solution would try every starting hour and extend forward while encountering `1`s, wrapping around using modulo arithmetic. For each start position, we walk up to `n` steps. This produces an `O(n^2)` algorithm in the worst case, since each starting point may traverse almost the entire array. With `n = 2 * 10^5`, this is far too slow.

The structure of the problem suggests a circular array, and the goal is to find the longest contiguous block of `1`s on a circle. A standard trick for circular sequences is to duplicate the array, turning wrap-around segments into normal contiguous segments.

If we build `a + a`, any segment that crosses the boundary in the original array becomes a normal segment in the doubled array. The only caution is that valid segments cannot exceed length `n`, because we are still representing one full rotation of the day.

So the problem reduces to finding the maximum number of consecutive `1`s in the doubled array, while ensuring we do not count more than `n` elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal (circular doubling / linear scan) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array of length `n`. We will treat it as circular, meaning index `n - 1` connects back to index `0`.
2. Create a new array `b` which is `a` concatenated with itself. This transforms circular adjacency into normal adjacency, so wrap-around sequences become straight segments.
3. Initialize two variables: `best = 0` to store the maximum streak of ones, and `current = 0` to track the current streak length while scanning.
4. Iterate through each element in `b` from left to right.

If the current element is `1`, increment `current` by one because the streak continues. If it is `0`, reset `current` to zero because the streak is broken.
5. After updating `current`, update `best` as `max(best, current)`.
6. If `current` exceeds `n`, clamp it back to `n`. This prevents counting a segment that spans more than one full cycle of the original day.
7. Continue until the end of `b`. The final answer is `best`.

### Why it works

Every valid circular segment of consecutive ones in the original array corresponds exactly to some contiguous segment in the doubled array. By scanning the doubled array, we enumerate all possible wrap-around segments implicitly. The only restriction is that we cannot use more than `n` consecutive elements, since that would imply traversing more than one full cycle of the day. Maintaining a simple running count ensures every maximal block is captured, and resetting on zeros guarantees correctness of segmentation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

b = a + a

best = 0
current = 0

for i in range(len(b)):
    if b[i] == 1:
        current += 1
        if current > n:
            current = n
    else:
        current = 0
    best = max(best, current)

print(best)
```

The implementation directly follows the idea of converting the circular array into a linear one. The doubling step ensures wrap-around segments are handled naturally.

The only subtlety is the cap at `n`, which prevents overstating a run when the doubled array allows artificially long streaks.

## Worked Examples

### Example 1

Input:

```
5
1 0 1 0 1
```

We build `b = [1,0,1,0,1,1,0,1,0,1]`.

| i | b[i] | current | best |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 2 | 1 | 1 | 1 |
| 3 | 0 | 0 | 1 |
| 4 | 1 | 1 | 1 |
| 5 | 1 | 2 | 2 |
| 6 | 0 | 0 | 2 |
| 7 | 1 | 1 | 2 |
| 8 | 0 | 0 | 2 |
| 9 | 1 | 1 | 2 |

The best segment is `2`, coming from the boundary wrap between the end and start of the day.

### Example 2

Input:

```
6
1 1 0 1 1 1
```

We build `b = [1,1,0,1,1,1,1,1,0,1,1,1]`.

| i | b[i] | current | best |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 1 | 2 | 2 |
| 2 | 0 | 0 | 2 |
| 3 | 1 | 1 | 2 |
| 4 | 1 | 2 | 2 |
| 5 | 1 | 3 | 3 |
| 6 | 1 | 4 | 4 |
| 7 | 1 | 5 | 5 |
| 8 | 0 | 0 | 5 |
| 9 | 1 | 1 | 5 |
| 10 | 1 | 2 | 5 |
| 11 | 1 | 3 | 5 |

The maximum wrap-around segment is `5`, formed by taking the tail of the day and continuing into its beginning.

These traces show how duplication turns circular structure into a simple linear scan.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We traverse a list of size `2n` once, with O(1) work per element |
| Space | O(n) | We store the duplicated array |

The solution fits easily within constraints since even `4 * 10^5` operations are trivial in Python, and memory usage is linear in the input size.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))
    b = a + a

    best = 0
    cur = 0

    for x in b:
        if x == 1:
            cur += 1
            if cur > n:
                cur = n
        else:
            cur = 0
        best = max(best, cur)

    print(best)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided samples
assert run("5\n1 0 1 0 1\n") == "2", "sample 1"
assert run("4\n1 1 1 1\n") == "4", "sample 2 (all rest)".__class__

# custom cases
assert run("1\n0\n") == "0", "single working hour"
assert run("1\n1\n") == "1", "single rest hour"
assert run("5\n0 0 0 0 0\n") == "0", "no rest at all"
assert run("6\n1 1 0 1 1 1\n") == "5", "wrap-around maximum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 0 | no rest hours |
| single 1 | 1 | minimal valid rest |
| all zeros | 0 | no streaks exist |
| mixed wrap case | 5 | boundary-crossing correctness |

## Edge Cases

Consider the input `6 1 1 0 1 1 1`. The optimal segment wraps from the end into the beginning, giving a streak of five ones.

In the doubled array, we see `1 1 0 1 1 1 1 1 0 1 1 1`. The scan starts a streak at index 0 reaching length 2, breaks at 2, restarts at 3, and grows through the boundary to reach 5 at index 7. At that point, `best` becomes 5 and remains unchanged.

This confirms that wrap-around cases are naturally captured without explicit modular arithmetic.
