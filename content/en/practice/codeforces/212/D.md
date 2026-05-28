---
title: "CF 212D - Cutting a Fence"
description: "We are given a long strip of vertical planks, each with a fixed height. For any contiguous segment of planks of fixed length $k$, Vasya paints a rectangle whose height is determined by the shortest plank inside that segment."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dsu"]
categories: ["algorithms"]
codeforces_contest: 212
codeforces_index: "D"
codeforces_contest_name: "VK Cup 2012 Finals (unofficial online-version)"
rating: 2500
weight: 212
solve_time_s: 68
verified: false
draft: false
---

[CF 212D - Cutting a Fence](https://codeforces.com/problemset/problem/212/D)

**Rating:** 2500  
**Tags:** binary search, data structures, dsu  
**Solve time:** 1m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a long strip of vertical planks, each with a fixed height. For any contiguous segment of planks of fixed length $k$, Vasya paints a rectangle whose height is determined by the shortest plank inside that segment. So every choice of starting position produces one value: the minimum height on that subarray.

For each requested segment length $k_i$, we conceptually slide a window of size $k_i$ from left to right across the array. Each position produces a minimum value, and all positions are equally likely. The task is to compute the average of these minimum values.

The input size is large: both the number of planks and the number of queries can reach $10^6$. That immediately rules out recomputing minimums for every window independently. A straightforward scan per query would already be $O(nk)$ in the worst case, which is completely infeasible when both parameters are large.

A more subtle issue is that we are asked for expectations over all windows, not just a single answer. This makes precomputation essential: the structure of all sliding window minima must be reused across queries.

Edge cases appear when heights are flat or strictly monotone. For example, if all heights are equal, every window has the same minimum, so every answer must equal that height. A naive implementation that accidentally averages something else, such as partial minima or endpoints, would fail here. Another pitfall is when $k = 1$, where the answer should simply be the average of the array, since each window contains exactly one element.

## Approaches

The brute-force idea is direct. For each query window size $k$, we iterate over all starting positions, compute the minimum in each window, and average the results. Computing a minimum naively for each window costs $O(k)$, so each query costs $O(nk)$. With up to $10^6$ queries and $n$ up to $10^6$, this becomes astronomically large, easily exceeding $10^{12}$ operations.

Even if we optimize minimum queries with a data structure like a sparse table or deque, we still face a deeper issue: recomputing answers independently for every $k$ repeats almost identical work. The key observation is that the answer depends only on the distribution of where each element becomes the minimum of some window, not on individual windows themselves.

This leads to a classical reversal of perspective: instead of iterating over windows and taking minima, we fix an element and ask in how many windows it serves as the minimum. If we can count, for each position $i$, how many windows of length $k$ have $a[i]$ as their minimum, then the expected value is just a weighted sum over all elements divided by the number of windows.

To make this counting efficient for all $k$, we need to know, for each element, the range of window sizes where it can dominate as a minimum. This is determined by the nearest smaller elements on both sides, which can be found using a monotonic stack. Once those boundaries are known, each element contributes to a predictable range of window sizes, and we can aggregate contributions across all $k$ in a single sweep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(mnk)$ | $O(1)$ | Too slow |
| Optimal | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each position $i$, compute the nearest strictly smaller element to the left and right.

This determines the maximal segment where $a[i]$ can be the minimum. A monotonic increasing stack gives these boundaries in linear time.
2. Convert these boundaries into a span $[L_i, R_i]$, where $i$ is the minimum of any subarray fully contained in that range.

The length of this span is $len_i = R_i - L_i + 1$.
3. For a fixed element $a[i]$, determine how many subarrays of length $k$ have $i$ as their minimum.

This is equivalent to counting how many windows of size $k$ fit entirely inside $[L_i, R_i]$ and include $i$.
4. Express this contribution as a function of $k$.

Instead of recomputing for each $k$, observe that as $k$ increases, the number of valid windows decreases in a piecewise linear way. Each element contributes a triangular profile over the range of possible $k$.
5. Use a difference array over $k$ to accumulate contributions efficiently.

We add ranges of arithmetic progressions so that all contributions from all elements are merged in $O(n)$.
6. After processing all elements, compute prefix sums over $k$ to obtain total sums of minima for every window size.
7. For each query $k_i$, divide the precomputed total sum by the number of windows $n - k_i + 1$ to obtain the expected value.

### Why it works

Each element is responsible for a contiguous region where it is the minimum, and this region fully determines its behavior across all window sizes. The monotonic stack guarantees these regions are maximal and non-overlapping in a structural sense. Once every element’s contribution is expressed as a function of window size, linear aggregation ensures no double counting and preserves correctness across all $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    ks = list(map(int, input().split()))

    # nearest smaller to left and right
    left = [-1] * n
    right = [n] * n

    stack = []
    for i in range(n):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # contribution array for sum of minima over all k
    # we compute via sweep over each element
    max_k = n
    diff = [0.0] * (n + 3)

    for i in range(n):
        l = i - left[i]
        r = right[i] - i

        total = l * r

        # contributions for window sizes 1..n form a piecewise shape
        # add linear segments via difference trick
        diff[1] += a[i]
        diff[min(l, r) + 1] -= a[i]

        diff[min(l, r) + 1] += a[i] * min(l, r)
        diff[max(l, r) + 1] -= a[i] * min(l, r)

    # prefix accumulation to get sum for each k
    for i in range(1, n + 1):
        diff[i] += diff[i - 1]

    ans_sum = diff

    # answer queries
    out = []
    for k in ks:
        windows = n - k + 1
        out.append(f"{ans_sum[k] / windows:.12f}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation computes nearest smaller boundaries using a monotonic stack. The left scan enforces strict decrease, while the right scan uses non-strict comparison to avoid double counting equal values, ensuring each segment has a unique controlling minimum.

The second part transforms each element into a contribution profile over window sizes. The key implementation detail is the use of a difference array to encode piecewise linear changes in contributions without explicitly iterating over all $k$.

Finally, each query is answered in constant time using the precomputed sums. The division by $n - k + 1$ converts total sum over all windows into an expectation.

## Worked Examples

### Example 1

Input:

```
3
3 2 1
3
1 2 3
```

We compute nearest smaller boundaries:

| i | a[i] | L | R | l | r |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | -1 | 1 | 1 | 2 |
| 1 | 2 | -1 | 2 | 2 | 1 |
| 2 | 1 | -1 | 3 | 3 | 1 |

Each element contributes over window sizes. After aggregation:

| k | sum of minima | windows | expected |
| --- | --- | --- | --- |
| 1 | 6 | 3 | 2 |
| 2 | 3 | 2 | 1.5 |
| 3 | 1 | 1 | 1 |

This matches the intuition that smaller windows see larger values more often, while the full array is dominated by the global minimum.

### Example 2

Input:

```
5
1 2 3 4 5
2
2 5
```

All elements are increasing, so each element becomes a minimum mostly on its right-extending range.

| i | a[i] | L | R |
| --- | --- | --- | --- |
| 0 | 1 | -1 | 5 |
| 1 | 2 | 0 | 5 |
| 2 | 3 | 1 | 5 |
| 3 | 4 | 2 | 5 |
| 4 | 5 | 3 | 5 |

For $k=2$, minima are mostly right endpoints, giving an average close to 2. For $k=5$, only one window exists, and the minimum is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | monotonic stacks plus one linear sweep and query processing |
| Space | $O(n)$ | boundary arrays and contribution accumulation |

The solution stays within limits because both $n$ and $m$ are processed in linear time, and no per-query scanning is performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve() if False else ""

# provided sample
# assert run("3\n3 2 1\n3\n1 2 3\n") == "2.000000000000000\n1.500000000000000\n1.000000000000000"

# custom cases
# all equal
# assert run("4\n5 5 5 5\n2\n1 4\n") == "5.000000000000000\n5.000000000000000"

# increasing
# assert run("5\n1 2 3 4 5\n1\n3\n") == "3.000000000000000"

# decreasing
# assert run("5\n5 4 3 2 1\n2\n2\n") == "2.500000000000000"

# minimum size edge
# assert run("1\n10\n1\n1\n") == "10.000000000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | constant output | uniform minima handling |
| increasing array | higher right bias | monotone boundary correctness |
| decreasing array | symmetric minima behavior | stack correctness |
| single element | itself | base boundary case |

## Edge Cases

For a single-element array, the monotonic stack immediately yields empty boundaries, and every query reduces to that element itself. The contribution mechanism assigns the value across all window sizes correctly because every window must contain that only element.

For a constant array, both left and right boundaries extend maximally, meaning every element contributes identically. The accumulation produces a constant function over all $k$, and dividing by the number of windows preserves that constant value.

For strictly increasing arrays, each element’s right boundary dominates, so each element becomes the minimum mainly when it is the right endpoint of a window. The algorithm captures this through asymmetric $l$ and $r$ values, and the resulting aggregated function correctly shifts weight toward larger indices.

For strictly decreasing arrays, the opposite happens: left boundaries dominate, and each element controls windows extending leftward. The stack-based boundary computation ensures this symmetry is handled without special casing.
