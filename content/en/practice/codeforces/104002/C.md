---
title: "CF 104002C - William and Middle Management"
description: "We are given a line of workers, each worker having two attributes: productivity and working hours. The contribution of a worker is defined as the product of these two values."
date: "2026-07-02T05:36:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104002
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 10-28-22 Div. 2 (Beginner)"
rating: 0
weight: 104002
solve_time_s: 47
verified: true
draft: false
---

[CF 104002C - William and Middle Management](https://codeforces.com/problemset/problem/104002/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of workers, each worker having two attributes: productivity and working hours. The contribution of a worker is defined as the product of these two values. William must choose a contiguous segment of exactly $K$ workers and wants to maximize the total contribution of that segment.

So the task reduces to scanning an array of length $N$, where each position holds a value $a_i = p_i \cdot h_i$, and finding the maximum sum over all contiguous subarrays of fixed length $K$.

The input size reaches up to $N = 10^5$, which rules out any solution that recomputes sums from scratch for each window. A naive recomputation per segment would cost $O(NK)$, which in the worst case becomes $10^{10}$, far beyond what fits in a second.

A correct solution must reuse computation between adjacent windows, meaning each element should be added and removed at most once.

A subtle edge case appears when $K = 1$. In that case the answer is simply the maximum single product. Any sliding-window logic must still handle initialization correctly.

Another corner case is when all values are equal or when negative values do not exist here, but we still must be careful with overflow in languages with fixed integer sizes. In Python this is not an issue, but in C++ it requires 64-bit integers.

A small illustrative case:

Input:

```
4 2
2 3
1 3
3 2
4 1
```

Products become $[6, 3, 6, 4]$. The correct answer is the maximum sum of any 2 consecutive elements, so we compare $(6+3), (3+6), (6+4)$, giving $10$.

A naive approach might recompute each pair independently, but that repeats shared work in overlapping segments.

## Approaches

The brute-force idea is straightforward: consider every possible starting position of a segment of length $K$, compute the sum of the next $K$ elements by iterating over them, and track the maximum. This is correct because it directly evaluates every valid candidate segment. However, for each of the $N-K+1$ starting positions, we do $K$ additions, leading to about $N \cdot K$ operations. With $N = 10^5$, this becomes infeasible when $K$ is large.

The improvement comes from recognizing that consecutive segments overlap heavily. When we move the window from $[i, i+K-1]$ to $[i+1, i+K]$, only two elements change: we remove $a_i$ and add $a_{i+K}$. This transforms recomputation into incremental updates, reducing each shift to constant time.

So instead of recomputing sums, we maintain a running sum and update it as the window slides across the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NK)$ | $O(1)$ | Too slow |
| Sliding Window | $O(N)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Convert each worker into a single value $a_i = p_i \cdot h_i$, since only this product matters for the final sum.
2. Compute the sum of the first $K$ elements. This forms the initial window and establishes a baseline answer.
3. Set this initial sum as the current best answer, since no other segment has been evaluated yet.
4. Slide the window one position at a time from left to right. At each step, subtract the element leaving the window and add the new element entering it. This update works because consecutive windows differ by exactly two positions.
5. After each update, compare the new window sum with the best answer and store the larger value.
6. After processing all windows, output the best sum encountered.

### Why it works

The algorithm maintains the exact sum of the current length-$K$ window at every step. Because each transition between windows preserves correctness by removing exactly one outdated element and adding exactly one new element, no information is lost or double-counted. Every possible contiguous segment of size $K$ is visited exactly once through this sliding process, so the maximum over all maintained sums is the true global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = []
    
    for _ in range(n):
        p, h = map(int, input().split())
        a.append(p * h)
    
    window_sum = sum(a[:k])
    best = window_sum
    
    for i in range(k, n):
        window_sum += a[i]
        window_sum -= a[i - k]
        if window_sum > best:
            best = window_sum
    
    print(best)

if __name__ == "__main__":
    solve()
```

The solution starts by collapsing each worker into a single integer value, which simplifies the problem into a standard fixed-length maximum subarray sum task. The initial window is computed once using a prefix slice, which establishes both the running sum and the baseline answer.

The loop then enforces the sliding invariant: at iteration $i$, `window_sum` always represents the sum of elements from $i-k+1$ to $i$. Each iteration updates this state in constant time by removing the outdated left element and adding the new right element.

A common mistake is recomputing the sum inside the loop using slicing, which silently degrades the solution to quadratic time. Another frequent off-by-one error is starting the sliding loop at the wrong index; here it starts exactly at `k`, ensuring the first full shift corresponds to replacing `a[0]` with `a[k]`.

## Worked Examples

### Example 1

Input:

```
4 2
2 3
1 3
3 2
4 1
```

Transformed array: $[6, 3, 6, 4]$

| Step | Window | Sum | Best |
| --- | --- | --- | --- |
| Init | [6, 3] | 9 | 9 |
| i=2 | [3, 6] | 9 | 9 |
| i=3 | [6, 4] | 10 | 10 |

The final best value is 10, which comes from the last window. This confirms the algorithm correctly evaluates overlapping windows without recomputation.

### Example 2

Input:

```
5 3
1 2
2 1
3 1
1 5
2 2
```

Transformed array: $[2, 2, 3, 5, 4]$

| Step | Window | Sum | Best |
| --- | --- | --- | --- |
| Init | [2, 2, 3] | 7 | 7 |
| i=3 | [2, 3, 5] | 10 | 10 |
| i=4 | [3, 5, 4] | 12 | 12 |

This trace shows how a locally weak prefix window is replaced by a stronger later segment, and how the algorithm naturally tracks the global maximum without any backtracking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | Each element is added once and removed once in the sliding process |
| Space | $O(1)$ | Only a few integer variables are maintained beyond input storage |

The solution fits easily within constraints for $N \le 10^5$, since it performs a single linear pass over the array with constant-time updates per step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""4 2
2 3
1 3
3 2
4 1
""") == "10"

# minimum size
assert run("""1 1
5 7
""") == "35"

# all equal
assert run("""5 3
2 2
2 2
2 2
2 2
2 2
""") == "12"

# strictly increasing
assert run("""4 2
1 1
2 2
3 3
4 4
""") == "14"

# k = n
assert run("""4 4
1 2
2 3
3 4
4 5
""") == str(2+6+12+20)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 35 | single-element boundary |
| all equal | 12 | stability of sliding sum |
| increasing | 14 | correct window tracking |
| k = n | full sum | full-range edge case |

## Edge Cases

When $K = 1$, the algorithm initializes the window as the first element and then simply compares each individual product as it slides. The update rule still works because subtracting and adding adjacent elements degenerates into replacing the current element.

For $K = N$, the loop does not execute since there is only one valid window. The initial sum is already the answer, and the algorithm correctly returns it without any sliding updates.

When all values are identical, every window sum is equal. The algorithm repeatedly updates the window but never changes the stored best value, demonstrating that it does not rely on variation in values to function correctly.
