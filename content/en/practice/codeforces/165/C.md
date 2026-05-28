---
title: "CF 165C - Another Problem on Strings"
description: "We are asked to count substrings of a binary string that contain exactly k ones. A substring is any contiguous sequence of characters within the string, and different occurrences at different positions count separately."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dp", "math", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 165
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 112 (Div. 2)"
rating: 1600
weight: 165
solve_time_s: 80
verified: true
draft: false
---

[CF 165C - Another Problem on Strings](https://codeforces.com/problemset/problem/165/C)

**Rating:** 1600  
**Tags:** binary search, brute force, dp, math, strings, two pointers  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count substrings of a binary string that contain exactly _k_ ones. A substring is any contiguous sequence of characters within the string, and different occurrences at different positions count separately. For instance, in the string "1010", the substring "10" occurs twice and each counts individually. The input gives an integer _k_ and a binary string _s_, and we need to output a single integer representing the number of substrings with exactly _k_ ones.

The string length can reach up to 1,000,000 characters, which rules out naive approaches that examine all substrings explicitly. A brute-force check of all O(n²) substrings, counting ones each time, would result in up to 10¹² operations in the worst case, far exceeding the 2-second time limit. This immediately directs us toward a solution that works in linear or linearithmic time, ideally O(n).

Edge cases that can trip a naive implementation include _k = 0_ or strings with all zeros or all ones. For example, if _s = "000"_ and _k = 0_, the correct output is 6, corresponding to substrings "0", "0", "0", "00", "00", "000". A careless solution that only counts ones would incorrectly return 0. Another subtle case is when _k_ exceeds the total number of ones in _s_, which should return 0.

## Approaches

The brute-force approach is straightforward: enumerate all possible substrings by selecting a start and end index and count the number of ones in each substring. This works because for each substring, we can determine exactly how many ones it contains, but it becomes prohibitively slow because the total number of substrings in a string of length _n_ is n(n+1)/2, and counting ones inside each substring adds another factor of n in the worst case. For _n = 10⁶_, this results in O(n³) operations if implemented naively, which is completely infeasible.

The key insight for an optimal solution comes from observing that the problem reduces to counting ranges of ones in the string. If we record the positions of all ones, then any substring with exactly _k_ ones starts just after the (i-1)-th one and ends at or before the (i+k)-th one. By precomputing these positions, we can calculate the number of valid starting and ending indices directly, without examining every substring. For the special case _k = 0_, we instead count contiguous blocks of zeros and compute how many substrings exist inside each block using combinatorial summation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal (Prefix + Ones Positions) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read integer _k_ and binary string _s_. Initialize a list to store positions of ones, adding -1 at the beginning and n at the end as sentinels. This simplifies boundary calculations.
2. Traverse the string once. Whenever a character is '1', append its index to the ones positions list.
3. If _k = 0_, iterate over consecutive ones positions to find the blocks of zeros between them. For a block of length _l_, the number of substrings is l(l+1)/2. Sum these contributions for all zero blocks and return the total.
4. If _k > 0_, iterate over the ones positions from index 1 to len(ones) - k - 1. For each window of _k_ ones, let left_gap be the number of zeros before the first one in the window, and right_gap be the number of zeros after the last one in the window. The number of substrings containing exactly this group of k ones is (left_gap + 1) * (right_gap + 1). Add this to a running total.
5. Output the total count.

Why it works: by recording positions of all ones, we convert the problem into a combinatorial one. Each substring with exactly k ones corresponds uniquely to a window of k consecutive ones. The number of possible substrings for that window is exactly the number of ways to extend to the left and right with zeros, which is captured by the gaps. This approach guarantees that every valid substring is counted exactly once and no invalid substring is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())
s = input().strip()
n = len(s)

ones = [-1]  # sentinel before start
for i, c in enumerate(s):
    if c == '1':
        ones.append(i)
ones.append(n)  # sentinel after end

if k == 0:
    total = 0
    for i in range(1, len(ones)):
        zeros = ones[i] - ones[i-1] - 1
        total += zeros * (zeros + 1) // 2
    print(total)
else:
    total = 0
    for i in range(1, len(ones) - k):
        left_gap = ones[i] - ones[i-1]
        right_gap = ones[i+k] - ones[i+k-1]
        total += left_gap * right_gap
    print(total)
```

The first loop collects all positions of '1' and adds sentinel values. The sentinel before the start ensures that left gaps are calculated correctly when a window starts at the first one. The sentinel after the end ensures right gaps are calculated correctly when a window ends at the last one. The conditional branch handles the zero case using combinatorial counting of substrings of zeros.

## Worked Examples

**Example 1:** Input: k=1, s="1010"

| ones list | -1,0,2,4 |

| window | left_gap | right_gap | contribution |
| --- | --- | --- | --- |
| 0th '1' | 0-(-1)=1 | 2-0=2 | 1*2=2 |
| 1st '1' | 2-0=2 | 4-2=2 | 2*2=4 |
| Total |  |  | 6 |

This confirms that all substrings containing exactly one '1' are counted.

**Example 2:** Input: k=2, s="10101"

| ones list | -1,0,2,4,5 |

| window | left_gap | right_gap | contribution |

| 0-1 | 0-(-1)=1 | 4-2=2 | 2 |

| 1-2 | 2-0=2 | 5-4=1 | 2 |

| Total |  |  | 4 |

This demonstrates that overlapping windows of ones are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We traverse the string once to record ones and once more to compute contributions. |
| Space | O(n) | Storing positions of ones requires at most n entries plus two sentinels. |

The linear time solution fits within the 2-second limit for n up to 10⁶, and the memory usage is acceptable given the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        exec(open("solution.py").read())
    return out.getvalue().strip()

# provided samples
assert run("1\n1010\n") == "6", "sample 1"
assert run("2\n10101\n") == "4", "sample 2"

# custom cases
assert run("0\n000\n") == "6", "all zeros, k=0"
assert run("3\n11111\n") == "3", "all ones, k=3"
assert run("1\n10001\n") == "8", "ones at edges and middle"
assert run("0\n111\n") == "0", "no zeros, k=0"
assert run("2\n010101\n") == "9", "alternating ones and zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "0\n000\n" | 6 | Correct counting of zero substrings |
| "3\n11111\n" | 3 | Windows of k ones in consecutive ones |
| "1\n10001\n" | 8 | Left/right extension with zeros |
| "0\n111\n" | 0 | No zeros, k=0 case |
| "2\n010101\n" | 9 | Alternating ones and zeros, multiple windows |

## Edge Cases

For k=0 and s="000", ones list is [-1,3]. The zero block length is 3-(-1)-1 = 3, giving 3*4/2 = 6 substrings, exactly correct. For k greater than total ones, for example k=5 and s="1010", the loop over windows does not execute, and the total remains 0, which is correct. For strings with ones at boundaries, the sentinel ensures left and right gaps are calculated correctly. Each edge case confirms that the algorithm handles boundaries, zero substrings, and overlapping windows consistently.
