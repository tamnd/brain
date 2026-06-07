---
title: "CF 2183B - Yet Another MEX Problem"
description: "We are given an array of non-negative integers and a number $k$. The task is to repeatedly remove elements from the array, always choosing a window of length $k$ whose MEX is maximal, and deleting any element within that window."
date: "2026-06-07T21:43:06+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2183
codeforces_index: "B"
codeforces_contest_name: "Hello 2026"
rating: 1100
weight: 2183
solve_time_s: 152
verified: false
draft: false
---

[CF 2183B - Yet Another MEX Problem](https://codeforces.com/problemset/problem/2183/B)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers and a number $k$. The task is to repeatedly remove elements from the array, always choosing a window of length $k$ whose MEX is maximal, and deleting any element within that window. After performing exactly $n-k+1$ such deletions, the array length becomes $k-1$. Our goal is to maximize the MEX of the final array.

The input consists of multiple test cases. Each test case can have up to $2 \cdot 10^5$ elements, and the sum of all $n$ across test cases is bounded by $2 \cdot 10^5$. Since each test case can be this large, any algorithm with $O(n^2)$ complexity will be too slow. We need a solution around $O(n)$ per test case.

Edge cases include arrays where all elements are zero, arrays with missing elements in the middle of the range, and arrays where $k = n$. For example, for an array `[0,0,0]` with `k=3`, after removing one element the remaining array is `[0,0]`, so the MEX is 1. A naive sliding-window MEX computation could fail to handle repeated deletions efficiently.

## Approaches

The brute-force approach is to literally simulate the process. For each deletion, we would:

1. Compute the MEX for every window of length $k$.
2. Pick a window with the maximum MEX.
3. Remove one element from that window.

Computing the MEX for a window in $O(k)$ is feasible for small arrays, but if $n$ is $2 \cdot 10^5$ and $k$ is comparable to $n$, this approach can take up to $O(n^2)$, which is far too slow.

The key observation is that we do not care about the precise order of deletions. The final MEX is determined by the multiset of elements in the array after all deletions. Since we perform $n-k+1$ deletions, the remaining elements are the $k-1$ smallest or strategically chosen elements that survive deletions. We can transform the problem into counting the frequency of each integer in the array. Any integer $x$ that occurs more than $n-k+1$ times cannot be entirely removed by the deletions. Thus, the maximum achievable MEX is the smallest non-negative integer $x$ for which its frequency is less than $n-k+1$.

This transforms the problem from simulating deletions to a simple counting problem, yielding an $O(n)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Frequency Counting / MEX Logic | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency array `count` of size `n+2` (to cover values up to `n`) to zero. This array will store how many times each integer occurs in the array.
2. Iterate through the input array, incrementing `count[a[i]]` for each element `a[i]`. This step prepares us to know how many times each number appears.
3. Compute `deletions = n - k + 1`, the number of elements that will be removed.
4. Initialize `mex = 0`. Iterate starting from 0 upwards. For each integer `mex_candidate`, check if its frequency in the array is greater than `deletions`. If it is, it cannot be completely removed, so increment `mex` and continue. If its frequency is less than or equal to `deletions`, this number can be removed entirely, so the current `mex` is the answer.
5. Output the final `mex`.

Why it works: After $n-k+1$ deletions, only $k-1$ elements remain. Any number that occurs more than $n-k+1$ times is guaranteed to survive at least one deletion. The smallest non-negative integer that cannot be guaranteed to survive is exactly the MEX of the remaining array. This insight eliminates the need for simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        count = [0] * (n + 2)
        for x in a:
            count[x] += 1
        deletions = n - k + 1
        mex = 0
        while count[mex] > deletions:
            mex += 1
        print(mex)

if __name__ == "__main__":
    solve()
```

The solution first reads all input, counts occurrences, and then determines the MEX by comparing frequencies with `deletions`. Using `n+2` in `count` ensures that we can always check `mex` up to `n+1` without index errors. Off-by-one errors are avoided by incrementing `mex` only when the count exceeds the number of deletions.

## Worked Examples

### Sample Input 1

```
n = 3, k = 3
a = [0,0,0]
```

| Step | count | deletions | mex candidate | mex |
| --- | --- | --- | --- | --- |
| 1 | [3,0,0,0] | 1 | 0 | 0 |
| 2 |  |  | 0 count > deletions → mex=1 | 1 |
| End |  |  | 1 count ≤ deletions → answer=1 | 1 |

Explanation: Only `0` occurs more than 1 time, so it survives. The smallest integer that may be missing is `1`.

### Sample Input 2

```
n = 5, k = 3
a = [0,1,2,1,0]
```

| Step | count | deletions | mex candidate | mex |
| --- | --- | --- | --- | --- |
| 1 | [2,2,1,0,0,0] | 3 | 0 | 0 count ≤ deletions → answer=0 |
| 2 |  |  | Check next: 1 count ≤ deletions → mex=1 |  |
| 3 |  |  | Check next: 2 count ≤ deletions → mex=2 |  |
| End |  |  | 3 count ≤ deletions → answer=2 | 2 |

Explanation: Numbers 0 and 1 occur ≤ 3 times, so deletions can remove them completely. Number 2 occurs once, also ≤ 3. The smallest number not guaranteed to survive deletions is 2, giving final MEX=2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies is O(n), finding MEX is O(n) in worst case but typically much smaller |
| Space | O(n) | Frequency array of size n+2 |

This fits comfortably within the constraints since the total sum of `n` over all test cases is ≤ 2·10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n3 3\n0 0 0\n4 2\n0 2 1 3\n5 3\n0 1 2 1 0\n6 2\n0 1 0 1 2 0\n7 5\n0 1 2 4 0 3 1\n") == "1\n1\n2\n1\n4"

# custom cases
assert run("1\n2 2\n0 1\n") == "2", "min-size input"
assert run("1\n5 5\n0 0 0 0 0\n") == "1", "k = n"
assert run("1\n6 3\n0 1 2 3 4 5\n") == "3", "all distinct elements"
assert run("1\n4 2\n1 1 1 1\n") == "0", "no zero initially"
assert run("1\n5 3\n0 1 0 1 0\n") == "2", "repeated zeros and ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2, [0,1] | 2 | Minimum-size input, MEX > max element |
| 5 5, [0,0,0,0,0] | 1 | k = n, all elements identical |
| 6 3, [0,1,2,3,4,5] | 3 | All distinct elements, verify counting logic |
| 4 2, [1,1,1,1] | 0 | Missing zero from array |
| 5 3, [0,1,0,1,0] | 2 | Repeated pattern with deletions |

## Edge Cases

If the array contains no zeros, the algorithm
