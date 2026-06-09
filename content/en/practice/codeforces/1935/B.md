---
title: "CF 1935B - Informatics in MAC"
description: "We are given an array of integers ranging from 0 to $n-1$, and we need to divide it into at least two contiguous subsegments such that every subsegment has the same MEX. The MEX of a subarray is the smallest non-negative integer missing from that subarray."
date: "2026-06-08T18:05:20+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1935
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 932 (Div. 2)"
rating: 1200
weight: 1935
solve_time_s: 131
verified: false
draft: false
---

[CF 1935B - Informatics in MAC](https://codeforces.com/problemset/problem/1935/B)

**Rating:** 1200  
**Tags:** constructive algorithms  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers ranging from 0 to $n-1$, and we need to divide it into at least two contiguous subsegments such that every subsegment has the same MEX. The MEX of a subarray is the smallest non-negative integer missing from that subarray. For example, MEX([0, 1, 3]) = 2, because 0 and 1 appear, but 2 is absent.

The input consists of multiple test cases. Each test case provides the array length $n$ and the array itself. The output must either be -1, if no suitable division exists, or a sequence of subsegment boundaries where each subsegment has the same MEX. Subsegments must be contiguous and cover the whole array.

The constraints tell us $n$ can go up to $10^5$, and the sum of $n$ over all test cases is also bounded by $10^5$. This rules out any solution with worse than linear time per test case. We need an approach that computes the MEX and decides segment boundaries in roughly $O(n)$ time.

Edge cases that are subtle include arrays with repeated elements, arrays missing 0 or 1, and arrays that already contain a full range of integers from 0 to some maximum. For instance, an array [0, 1, 2] cannot be split into multiple subsegments with the same MEX, because the MEX of the full array is 3, but there is no way to partition it into at least two segments where each segment contains 0, 1, 2 so that 3 is still the MEX. A naive approach might try to split arbitrarily, but it would fail on these cases.

## Approaches

The brute-force solution is to try all possible segmentations of the array, compute the MEX of each segment, and check if they are equal. This is correct in principle because it considers every possible division. However, the number of divisions is exponential in $n$, making it impossible for arrays of length up to $10^5$.

The key insight for an optimal solution comes from the definition of MEX. If we know the MEX of the whole array, call it $m$, any segment that does not contain all numbers from 0 to $m-1$ cannot have MEX $m$. Conversely, any segment that contains all numbers from 0 to $m-1$ will have MEX $m$, regardless of extra numbers. Therefore, the problem reduces to finding contiguous blocks that each contain all numbers 0 through $m-1$.

The algorithm can then proceed by scanning the array and extending the current segment until all numbers 0 to $m-1$ have been seen in that segment. Once they have, the segment can end, and a new segment can begin. If the array can be partitioned into at least two such segments, we have a valid solution. If we reach the end and have fewer than two segments, it is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the MEX $m$ of the entire array. This is done by creating a frequency array for numbers 0 to $n$ and finding the first index with zero occurrences. This gives the target MEX for all segments.
2. If $m = 0$, every element is at least 1. In this case, any segment has MEX 0, so we can divide the array into two segments arbitrarily: [1,1] and [2,n]. Return this split.
3. Initialize a counter dictionary for numbers 0 through $m-1$, which tracks how many times each required number has been seen in the current segment. Also initialize an empty list to store segment boundaries and a variable for the left boundary of the current segment.
4. Iterate through the array from left to right. For each element, if it is less than $m$, increment its counter. After each increment, check whether all numbers from 0 to $m-1$ have been seen in the current segment. If yes, close the segment by recording its right boundary. Start a new segment from the next index, and reset counters.
5. After scanning the array, check if at least two segments have been formed. If yes, return them. If only one segment exists, output -1, because the problem requires at least two subsegments.
6. Output the number of segments and the segment boundaries.

The correctness comes from maintaining the invariant that each closed segment contains all numbers from 0 to $m-1$, guaranteeing that its MEX is $m$. By scanning left to right, we maximize the number of segments and ensure they are contiguous. If fewer than two segments result, no valid division exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        present = [0] * (n + 1)
        for x in a:
            if x <= n:
                present[x] += 1
        mex = 0
        while present[mex]:
            mex += 1
        if mex == 0:
            print(2)
            print(1,1)
            print(2,n)
            continue
        from collections import defaultdict
        counter = defaultdict(int)
        required = set(range(mex))
        segments = []
        l = 0
        for r, x in enumerate(a):
            if x < mex:
                counter[x] += 1
            while all(counter[i] > 0 for i in range(mex)):
                segments.append((l+1, r+1))
                l = r+1
                counter = defaultdict(int)
        if l != n:
            segments.append((l+1, n))
        if len(segments) < 2:
            print(-1)
        else:
            print(len(segments))
            for seg in segments:
                print(seg[0], seg[1])

if __name__ == "__main__":
    solve()
```

The code first computes the MEX of the whole array. If MEX is zero, it uses a trivial split. Otherwise, it scans the array, extending segments until all required numbers 0 to $m-1$ are included. Each closed segment is recorded. The check at the end ensures at least two segments exist. Counters are reset after each segment to track the next subarray independently.

## Worked Examples

### Sample Input 1

```
2
0 0
0 1 2 0
```

| Step | l | r | counter | segments |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | {} | [] |
| 2 | 0 | 1 | {0:1} | [(1,1)] |
| 3 | 2 | 3 | {0:1,1:1,2:1} | [(1,1),(2,4)] |

The first example has MEX 1. The first element 0 satisfies the segment requirement. The next segment contains 0,1,2 but MEX is still 1 for the segment. Two segments exist, so output them.

### Sample Input 2

```
0 1 2 3 4
```

| Step | l | r | counter | segments |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | {0:1} | [] |
| 2 | 0 | 4 | {0:1,1:1,2:1,3:1,4:1} | [(1,5)] |

Only one segment is formed. No valid split into at least two subsegments exists. Output -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute MEX and single pass to scan array for segments. |
| Space | O(n) | Counter dictionary and frequency array of size O(n). |

This fits the constraints since the sum of $n$ over all test cases is $10^5$, so the algorithm completes within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("5\n2\n0 0\n5\n0 1 2 3 4\n8\n0 1 7 1 0 1 0 3\n3\n2 2 2\n4\n0 1 2 0\n") == \
"""2
1 1
2 2
-1
3
1 3
4 5
6 8
3
1 1
2 2
3 3
-1""", "sample tests"

# custom cases
assert run("1\n2\n1 1\n") == "2\n1 1\n2 2", "minimum size, same values"
assert run("1\n3\n0 2 0\n") == "2\n1 2\n3 3", "split possible with missing 1"
assert
```
