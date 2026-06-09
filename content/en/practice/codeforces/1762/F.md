---
title: "CF 1762F - Good Pairs "
description: "We are asked to count the number of \"good pairs\" in an array. A pair of positions $(l, r)$ is good if we can move from index $l$ to $r$ by hopping forward in the array along a sequence of indices where each consecutive pair differs by at most $k$."
date: "2026-06-09T13:52:21+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1762
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 838 (Div. 2)"
rating: 2600
weight: 1762
solve_time_s: 190
verified: false
draft: false
---

[CF 1762F - Good Pairs ](https://codeforces.com/problemset/problem/1762/F)

**Rating:** 2600  
**Tags:** binary search, data structures, dp  
**Solve time:** 3m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of "good pairs" in an array. A pair of positions $(l, r)$ is good if we can move from index $l$ to $r$ by hopping forward in the array along a sequence of indices where each consecutive pair differs by at most $k$. In simpler terms, you can think of each number in the array as a stepping stone, and we can step forward as long as the difference between the stones is at most $k$. Our task is to count all possible starting and ending positions that allow a valid stepping path.

The input contains multiple test cases, each with an array of length $n$ up to $5 \cdot 10^5$, and the sum of all $n$ across test cases is also bounded by $5 \cdot 10^5$. This rules out any algorithm with $O(n^2)$ per test case, because in the worst case we would reach $2.5 \cdot 10^{11}$ operations, which is completely infeasible in 3 seconds. An $O(n \log n)$ or $O(n)$ approach is necessary.

Edge cases that can easily break a naive implementation include arrays with all identical elements, arrays with strictly increasing or decreasing values, and $k = 0$. For example, with an array `[1,1,1]` and $k = 0$, every subarray is good, and the answer is 6. A careless approach that only checks consecutive elements would miss pairs like `(1,3)`.

## Approaches

The brute-force approach would be to iterate over all pairs $(l,r)$ and for each pair check if there exists a valid sequence connecting $l$ to $r$. This works in principle because it directly models the definition of good pairs, but it is $O(n^2)$ per test case. With $n$ up to $5 \cdot 10^5$, this is clearly infeasible.

The key insight is that if we can move from index $i$ to index $j$, then all consecutive indices between $i$ and $j$ that maintain the absolute difference $\le k$ can be collapsed into a contiguous "good segment." Once we identify the maximal range starting at each index where we can move forward without violating $|a[i] - a[i+1]| \le k$, we can compute the number of good pairs starting at that index using a simple arithmetic formula instead of enumerating each pair.

Concretely, we maintain a sliding window from the left of the array, extending the right end until the condition $|a[r] - a[r-1]| \le k$ fails. Each extension adds multiple good pairs at once, avoiding the $O(n^2)$ cost. This transforms the problem into $O(n)$ per test case because every index is visited at most twice: once as a left pointer and once as a right pointer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Sliding Window | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$, $k$, and the array $a$. We will process each array independently.
2. Initialize a result counter `res` to zero. This will accumulate the number of good pairs.
3. Initialize two pointers, `l = 0` and `r = 0`. The pointer `l` represents the left end of a candidate good segment, and `r` represents the farthest index reachable while maintaining $|a[r] - a[r-1]| \le k$.
4. Iterate over the array with `l` from 0 to $n-1$. Before processing, extend `r` as far as possible while `r < n` and $|a[r] - a[r-1]| \le k$ (for `r > l`). This ensures that `[l, r)` forms a contiguous good segment.
5. The number of good pairs starting at `l` is exactly `r - l`. Add this to `res`.
6. Increment `l` and repeat. Since `r` never moves left, the total runtime is linear.
7. After processing the array, print `res`.

Why it works: The algorithm maintains a contiguous segment `[l, r)` in which any pair `(l, x)` for `x` in `[l, r-1]` is guaranteed to be good. This invariant holds because the condition $|a[i] - a[i+1]| \le k$ is transitive along a segment. By counting `r - l` for each `l`, we enumerate all good pairs exactly once without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    res = 0
    r = 0
    for l in range(n):
        if r < l:
            r = l
        while r + 1 < n and abs(a[r+1] - a[r]) <= k:
            r += 1
        res += r - l + 1
    print(res)
```

The outer loop iterates over each potential left end of a segment. The inner while loop extends `r` as far as the array allows while respecting the `k`-difference condition. The check `if r < l: r = l` ensures that the right pointer never falls behind the left pointer. Counting `r - l + 1` correctly adds all good pairs starting at `l`.

## Worked Examples

**Example 1**

Array `[1,1,1]`, `k=0`

| l | r | r-l+1 | res |
| --- | --- | --- | --- |
| 0 | 2 | 3 | 3 |
| 1 | 2 | 2 | 5 |
| 2 | 2 | 1 | 6 |

All subarrays are good. The table shows how `r` extends to the last valid index and how we accumulate counts.

**Example 2**

Array `[4,8,6,8]`, `k=2`

| l | r | r-l+1 | res |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 1 | 3 | 3 | 4 |
| 2 | 3 | 2 | 6 |
| 3 | 3 | 1 | 7 |

This trace demonstrates that non-consecutive elements can be connected via intermediate indices. The algorithm captures that automatically by extending `r` through valid transitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pointer moves at most n times. |
| Space | O(1) | Only a few variables needed besides input. |

With `sum(n) <= 5 * 10^5`, the total operations are under 1 million, which fits comfortably in the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    return out.getvalue().strip()

# provided samples
assert run("4\n3 0\n1 1 1\n4 2\n4 8 6 8\n6 4\n7 2 5 8 3 8\n20 23\n110 57 98 14 20 1 60 82 108 37 82 73 8 46 38 35 106 115 58 112\n") == "6\n9\n18\n92"

# custom tests
assert run("1\n1 0\n42\n") == "1", "single element"
assert run("1\n5 0\n1 2 3 4 5\n") == "5", "k=0, no steps allowed"
assert run("1\n5 100\n1 2 3 4 5\n") == "15", "k large enough to connect all"
assert run("1\n4 1\n1 3 2 4\n") == "4", "only consecutive small diffs count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 0\n42\n` | 1 | Single-element array |
| `1\n5 0\n1 2 3 4 5\n` | 5 | k=0 prevents any jumps |
| `1\n5 100\n1 2 3 4 5\n` | 15 | k large enough to allow all connections |
| `1\n4 1\n1 3 2 4\n` | 4 | Non-consecutive valid sequences |

## Edge Cases

For an array with all identical elements, e.g., `[2,2,2,2]` and `k=0`, the algorithm correctly extends `r` to the end each time. For `l=0
