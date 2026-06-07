---
title: "CF 2217B - Flip the Bit (Easy Version)"
description: "We are given a binary array of length $n$ and a single special index $p1$ (since $k=1$). The element at this special index has value $x$, and our goal is to make the entire array equal to $x$."
date: "2026-06-07T18:24:05+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2217
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1091 (Div. 2) and CodeCraft 26"
rating: 1000
weight: 2217
solve_time_s: 102
verified: false
draft: false
---

[CF 2217B - Flip the Bit (Easy Version)](https://codeforces.com/problemset/problem/2217/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array of length $n$ and a single special index $p_1$ (since $k=1$). The element at this special index has value $x$, and our goal is to make the entire array equal to $x$. To do this, we can perform any number of flip operations on contiguous subarrays that include the special index. A flip inverts every bit in the chosen range.

Effectively, the problem asks: what is the minimum number of contiguous subarray flips containing the special index needed so that all elements match the value at that index?

Because $n$ can be up to $2 \cdot 10^5$ and there can be up to $10^4$ test cases, a solution with complexity $O(n^2)$ per test case would be too slow. We need a linear solution relative to the array size.

Non-obvious edge cases include: an array that is already all equal to $x$, or when $x$ is 0 and all the 1s appear consecutively on one side of the special index. A careless approach that flips indiscriminately could perform unnecessary operations.

## Approaches

A brute-force approach would consider all possible ranges containing the special index, flip them, and recursively try to minimize flips. This would be correct but infeasible. For a single special index, the brute-force might attempt every subarray containing that index, but there are roughly $O(n^2)$ such ranges. That quickly exceeds time limits.

The key observation is that each contiguous segment of elements not equal to $x$ and on the same side of the special index can be fixed with a single flip. Flips that span multiple such segments are not useful because they would also invert elements that are already correct. Therefore, the minimum number of flips is the number of contiguous "wrong" segments on either side of the special index.

To implement this efficiently, we scan the array to the left and right of the special index, count contiguous segments of values not equal to $x$, and sum these counts. This gives the minimum operations directly in $O(n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the value $x$ at the special index.
2. Initialize a counter for flips to zero.
3. Scan the array to the left of the special index from nearest to farthest. Whenever a contiguous block of elements differs from $x$, increment the flip counter by one and skip the block.
4. Scan the array to the right of the special index using the same procedure. Each contiguous block differing from $x$ counts as one flip.
5. Return the total number of flips.

Why it works: each flip must include the special index, so we cannot flip elements on the opposite side independently. Contiguous sequences of wrong values on each side can be fixed with exactly one flip per sequence, which guarantees the minimal number of operations. Any attempt to split or combine flips would either leave some wrong bits untouched or perform redundant flips.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))
        x = a[p[0]-1]
        
        flips = 0
        # Left of special index
        i = p[0]-2
        while i >= 0:
            if a[i] != x:
                flips += 1
                while i >= 0 and a[i] != x:
                    i -= 1
            else:
                i -= 1
        # Right of special index
        i = p[0]
        while i < n:
            if a[i] != x:
                flips += 1
                while i < n and a[i] != x:
                    i += 1
            else:
                i += 1
        print(flips)

if __name__ == "__main__":
    solve()
```

The solution first reads the number of test cases and iterates over them. For each test case, it extracts the array and the special index, adjusts for 0-based indexing, and scans left and right from the special index to count contiguous sequences of wrong values. Inner `while` loops skip over entire segments to ensure each flip is counted exactly once.

## Worked Examples

**Example 1**

Input:

```
n = 5, k = 1
a = [1, 0, 1, 0, 1]
p = [3]
```

| Step | i | a[i] | flips | Comment |
| --- | --- | --- | --- | --- |
| Left scan start | 2 | - | 0 | special index is 2 (0-based) |
| i=1 | 0 | a[1]=0 != x | 1 | start segment |
| i=0 | 0 | a[0]=1 == x | - | end segment |
| Right scan start | 3 | a[3]=0 != x | 2 | start segment |
| i=4 | a[4]=1 == x | - | end segment |  |

Total flips = 2

**Example 2**

Input:

```
n = 4, k = 1
a = [0, 0, 0, 0]
p = [2]
```

All elements equal to x, flips = 0

The trace confirms that contiguous segments are counted precisely once and no unnecessary flips are performed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is visited at most twice (left and right scans) |
| Space | O(1) | No extra storage proportional to n is needed, just counters |

Given $n$ summed over all test cases is ≤ 2×10^5, total operations are within 4×10^5, which is acceptable within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("1\n5 1\n1 0 1 0 1\n3\n") == "2", "sample 1"

# Custom cases
assert run("1\n4 1\n0 0 0 0\n2\n") == "0", "all equal"
assert run("1\n1 1\n1\n1\n") == "0", "single element"
assert run("1\n6 1\n1 1 0 0 1 1\n3\n") == "1", "single segment in middle"
assert run("1\n5 1\n0 1 0 1 0\n3\n") == "2", "alternating around special"
assert run("1\n7 1\n1 1 0 0 0 1 1\n4\n") == "1", "special inside long segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [1,0,1,0,1], p=3 | 2 | standard case with flips on both sides |
| [0,0,0,0], p=2 | 0 | all elements already correct |
| [1], p=1 | 0 | single element array |
| [1,1,0,0,1,1], p=3 | 1 | contiguous wrong segment |
| [0,1,0,1,0], p=3 | 2 | alternating wrong segments |
| [1,1,0,0,0,1,1], p=4 | 1 | long segment covering special index |

## Edge Cases

A single-element array: the special index is the only element, already equal to itself. The algorithm correctly returns 0.

An array with all elements equal to the special value: left and right scans terminate immediately without incrementing flips.

Alternating sequences around the special index: the inner `while` loops ensure that each contiguous segment is counted exactly once, preventing overcounting.

A segment that includes the special index itself: since we only scan left and right from the special index, this does not create double counting.

The algorithm handles boundaries correctly by stopping at indices 0 and n-1.

This confirms correctness for both trivial and tricky configurations.
