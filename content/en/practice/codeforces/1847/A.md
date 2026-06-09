---
title: "CF 1847A - The Man who became a God "
description: "The problem asks us to split a sequence of villagers, each with a numerical suspicion level, into exactly k contiguous groups in a way that minimizes the total \"power\" of these groups."
date: "2026-06-09T05:43:19+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1847
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 882 (Div. 2)"
rating: 800
weight: 1847
solve_time_s: 81
verified: true
draft: false
---

[CF 1847A - The Man who became a God ](https://codeforces.com/problemset/problem/1847/A)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to split a sequence of villagers, each with a numerical suspicion level, into exactly `k` contiguous groups in a way that minimizes the total "power" of these groups. The power of a group is defined as the sum of absolute differences between consecutive villagers in that group. For example, a group `[1, 4, 2]` has power `|1-4| + |4-2| = 3 + 2 = 5`. A group with a single villager has zero power.

The input gives multiple test cases. Each test case consists of `n`, the number of villagers, `k`, the number of required groups, and an array `a` of suspicion levels. The output is the minimum sum of powers after dividing the villagers into exactly `k` contiguous groups. The villagers must remain in their original order; we cannot reorder them.

The constraints are small: `n` can be at most 100, `k` is at most `n`, and each suspicion level is at most 500. Since `n` is small, solutions that operate in O(n log n) or even O(n²) per test case are feasible. However, we need to handle up to 100 test cases efficiently.

An important edge case is when all villagers have the same suspicion level, for instance `[5, 5, 5, 5]`. Then the absolute differences are all zero, and any grouping gives zero total power. Another subtle case is when `k = n`, which means every villager is in a singleton group; here the total power is always zero.

## Approaches

The naive approach would be to try all possible ways of placing `k-1` cuts between the villagers. For each configuration, we calculate the power of each resulting group and sum them. This is correct but computationally expensive because there are `C(n-1, k-1)` ways to choose cuts, which grows quickly with `n` and `k`. Even with `n=100`, this would be far too slow.

The key observation is that the total power of the entire array without any cuts is the sum of all consecutive absolute differences, i.e., `sum(|a[i+1]-a[i]| for i in range(n-1))`. If we must split the array into `k` groups, every cut we make removes exactly one absolute difference from the total power, namely the difference between the two elements on either side of the cut. Therefore, to minimize total power after making `k-1` cuts, we should remove the largest `k-1` consecutive differences.

This reduces the problem to a simple greedy strategy: compute all consecutive differences, sort them in descending order, and subtract the sum of the largest `k-1` differences from the total sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n-1, k-1) * n) | O(n) | Too slow |
| Greedy via differences | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and `k`, and then read the array `a` of suspicion levels.
2. Compute the absolute differences between consecutive villagers, `diff[i] = |a[i+1]-a[i]|` for `i=0` to `n-2`. These represent the contribution to total power of adjacent villagers.
3. Compute the total power without cuts as the sum of all elements in `diff`. This is the starting total before removing any differences.
4. Sort the `diff` array in descending order. The largest differences are the ones that will contribute most to total power if left intact.
5. Remove the `k-1` largest differences by subtracting their sum from the total power. This simulates placing `k-1` cuts to break the groups at these largest differences.
6. Output the resulting total power.

Why it works: the invariant is that any cut removes exactly one consecutive difference from the total. To minimize total power, we want to remove the largest differences. Sorting ensures we can select the top `k-1` differences efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        # compute consecutive differences
        diff = [abs(a[i+1] - a[i]) for i in range(n-1)]
        total = sum(diff)
        
        # remove largest k-1 differences
        diff.sort(reverse=True)
        total -= sum(diff[:k-1])
        print(total)

if __name__ == "__main__":
    solve()
```

The code reads input efficiently using `sys.stdin.readline`. The differences are computed using a list comprehension for clarity and speed. Sorting in descending order ensures that the top `k-1` differences are easily accessible to subtract from the total. The final print statement outputs the minimized total power for each test case.

## Worked Examples

Sample Input:

```
4 2
1 3 5 2
```

Compute differences: `[2, 2, 3]`

Total sum: `2 + 2 + 3 = 7`

We need `k=2` groups, so remove the largest difference `3`

Minimized power: `7 - 3 = 4`

Second example:

```
6 3
1 9 12 4 7 2
```

Differences: `[8, 3, 8, 3, 5]`

Total sum: `8 + 3 + 8 + 3 + 5 = 27`

Remove `k-1 = 2` largest differences `8 + 8 = 16`

Minimized power: `27 - 16 = 11`

This matches the expected outputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Computing differences is O(n), sorting differences is O(n log n), per test case |
| Space | O(n) | Store differences array |

Given `n <= 100` and `t <= 100`, the solution is well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    import io as _io
    f = _io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# Provided samples
assert run("3\n4 2\n1 3 5 2\n6 3\n1 9 12 4 7 2\n12 8\n1 9 8 2 3 3 1 8 7 7 9 2") == "4\n11\n2", "sample 1"

# Custom cases
assert run("1\n5 5\n1 2 3 4 5") == "0", "every villager in singleton group"
assert run("1\n5 1\n1 2 3 4 5") == "4", "all villagers in one group"
assert run("1\n6 3\n5 5 5 5 5 5") == "0", "all equal suspicion"
assert run("1\n7 4\n1 7 2 8 3 9 4") == "6", "alternating highs and lows"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 5\n1 2 3 4 5` | 0 | Singleton groups reduce all power to 0 |
| `5 1\n1 2 3 4 5` | 4 | Single group, total power is sum of all diffs |
| `6 3\n5 5 5 5 5 5` | 0 | Identical values produce zero power |
| `7 4\n1 7 2 8 3 9 4` | 6 | Correct greedy removal of largest diffs |

## Edge Cases

When `k = n`, each villager is a singleton group. The differences removed are `n-1` largest, which are all the differences. The total power is zero. When `k = 1`, no differences are removed, so the total power is sum of all consecutive differences. The algorithm correctly handles arrays with repeated elements, arrays with alternating highs and lows, and the minimum and maximum group counts.
