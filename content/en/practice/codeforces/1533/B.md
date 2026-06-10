---
title: "CF 1533B - Nearest Point Function"
description: "We are given a sorted list of distinct integer positions on a number line. A function, when queried with a value y, returns the closest point from this list, meaning it selects the element with the smallest absolute distance to y."
date: "2026-06-10T16:19:01+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1533
codeforces_index: "B"
codeforces_contest_name: "Kotlin Heroes: Episode 7"
rating: 0
weight: 1533
solve_time_s: 250
verified: false
draft: false
---

[CF 1533B - Nearest Point Function](https://codeforces.com/problemset/problem/1533/B)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 4m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sorted list of distinct integer positions on a number line. A function, when queried with a value `y`, returns the closest point from this list, meaning it selects the element with the smallest absolute distance to `y`.

The issue appears when `y` is exactly in the middle between two consecutive points. In that case, both neighbors are equally close, so the function has no unique answer and crashes.

The task is not to find such a `y` directly, but to determine whether any integer `y` exists that would cause this tie situation for a given array.

From the constraints, the total number of points across test cases is up to 200,000. This immediately rules out any quadratic approach that tries all pairs or all candidate `y` values. We need something linear per test case or linear overall.

A subtle edge case arises when the array has only two elements. If the gap between them is even, there is a midpoint integer that creates a tie. For example `[1, 3]` allows `y = 2`. But `[1, 2]` does not, since the midpoint is not an integer. Similarly, larger gaps behave the same way.

Another important observation is that we do not need to consider arbitrary `y`. Any crash can only occur at midpoints between adjacent elements, because the nearest point function is monotonic between sorted values and ties can only appear at boundaries between two consecutive intervals.

## Approaches

A brute-force approach would try all integer values between the minimum and maximum array elements, and for each `y`, compute the closest point and check whether there is a tie with both neighbors. This is conceptually straightforward but completely infeasible: the range of values goes up to 10^9, so even a single test case could require billions of checks.

We can refine this by noticing that only midpoints between adjacent elements matter. For each adjacent pair `(x[i], x[i+1])`, we check whether `(x[i] + x[i+1]) / 2` is an integer and whether it lies strictly between them. If the distance gap is even, then there exists an integer exactly in the middle, which produces a tie. If any such pair exists, we can immediately answer YES.

Thus the problem reduces to scanning the array once and checking parity of differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all y | O(max(x)) per test | O(1) | Too slow |
| Check adjacent gaps | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array of points and ensure it is sorted.

The sorted property guarantees that any candidate tie must occur between adjacent elements.
2. Iterate over every adjacent pair `(x[i], x[i+1])`.
3. Compute the difference `d = x[i+1] - x[i]`.
4. Check whether `d` is even.

If it is even, then `(x[i] + x[i+1]) / 2` is an integer and lies exactly in the middle.
5. If any adjacent pair has even distance, immediately conclude that a crash is possible and stop processing further pairs.
6. If no such pair exists, conclude that no integer midpoint exists anywhere, so no crash is possible.

### Why it works

Any integer `y` that produces a tie must satisfy that two distinct points are equally close to it. Because the array is sorted, the only way this can happen is if `y` lies exactly at the midpoint between two consecutive points. Any point further away would be strictly dominated by its nearest neighbor. Therefore, the existence of a valid `y` is equivalent to the existence of at least one adjacent pair with an even gap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        
        ok = False
        for i in range(n - 1):
            if (x[i + 1] - x[i]) % 2 == 0:
                ok = True
                break
        
        out.append("YES" if ok else "NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution loops over each test case and checks only adjacent differences. The key implementation detail is using the modulo operator on the difference rather than computing the midpoint explicitly. This avoids overflow concerns and keeps the logic clean.

The early break ensures we stop as soon as we find any valid pair, which preserves linear complexity.

## Worked Examples

### Example 1

Input:

```
1
3
1 50 101
```

| i | x[i] | x[i+1] | difference | even? | result state |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 50 | 49 | no | continue |
| 1 | 50 | 101 | 51 | no | no crash |

This demonstrates that not every large gap creates a valid midpoint. Only even gaps matter, not magnitude.

### Example 2

Input:

```
1
4
1 3 6 10
```

| i | x[i] | x[i+1] | difference | even? | result state |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 3 | 2 | yes | crash detected |

Here the first adjacent pair already produces a valid midpoint at `y = 2`, so we can stop immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each element is visited once to check adjacent gaps |
| Space | O(1) extra | only a few variables used besides input storage |

The total input size across all test cases is 200,000, so a single linear pass over all data easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        ok = False
        for i in range(n - 1):
            if (x[i+1] - x[i]) % 2 == 0:
                ok = True
                break
        res.append("YES" if ok else "NO")
    return "\n".join(res)

# provided samples
assert run("""7
2
1 3
2
1 100
3
1 50 101
2
1 1000000000
2
1 999999999
6
1 2 5 7 9 11
6
1 2 5 8 9 12
""") == """YES
NO
NO
NO
YES
YES
NO"""

# minimum size, even gap
assert run("""1
2
1 3
""") == "YES"

# minimum size, odd gap
assert run("""1
2
1 2
""") == "NO"

# all consecutive even gaps
assert run("""1
4
1 3 5 7
""") == "YES"

# large values boundary
assert run("""1
3
1 1000000000 2000000000
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,3]` | YES | smallest valid midpoint |
| `[1,2]` | NO | no integer midpoint exists |
| `[1,3,5,7]` | YES | multiple candidates, early detection |
| large spaced values | NO | boundary correctness |

## Edge Cases

The two-element array case is the most sensitive. For input `[1, 3]`, the algorithm computes a single difference `2`, which is even, so it immediately returns YES. The midpoint `2` is valid and lies strictly between both endpoints, confirming the crash condition.

For `[1, 2]`, the difference is `1`, which is odd, so no midpoint exists in integers. The loop finishes and returns NO, correctly handling the minimal configuration.

Another subtle case is when multiple adjacent gaps exist. In `[1, 2, 5, 8]`, the first gap `1` is ignored, the second gap `3` is ignored, but the third gap `3` is also ignored. The algorithm only needs a single even gap, so absence across all pairs correctly leads to NO.
