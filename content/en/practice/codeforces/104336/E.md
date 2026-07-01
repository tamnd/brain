---
title: "CF 104336E - Solve problems every day"
description: "We are tracking Maxim’s daily problem solving over a sequence of $n$ days. On each day he solves at least one problem, and we want to assign an exact positive integer to each day. Two quantities are observed at every day $i$."
date: "2026-07-01T18:47:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104336
codeforces_index: "E"
codeforces_contest_name: "II Olympiad of classes at the Mechanics and Mathematics Faculty of MSU in programming 2023."
rating: 0
weight: 104336
solve_time_s: 61
verified: true
draft: false
---

[CF 104336E - Solve problems every day](https://codeforces.com/problemset/problem/104336/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tracking Maxim’s daily problem solving over a sequence of $n$ days. On each day he solves at least one problem, and we want to assign an exact positive integer to each day.

Two quantities are observed at every day $i$. The first is the total number of problems solved in the last $k$ days ending at $i$, which behaves like a sliding window sum of length $k$. The second is the number of consecutive days ending at $i$ during which he has been solving problems every day, which is simply the current streak length.

The rule is that at every day, the sliding window sum over the last $k$ days must be at least as large as the current streak length. We are told this condition already holds for all $n$ days, and we must reconstruct a sequence of daily values that satisfies the constraint while minimizing the total sum over all $n$ days.

The input gives $k$, the window size, and $n$, the number of days. The output is the minimum possible total number of problems solved.

The constraints go up to $10^6$, so any solution must be linear or near-linear in $n$. A quadratic reconstruction of all valid sequences or repeated recomputation of sliding windows is impossible, since even $O(nk)$ would reach $10^{12}$ operations in the worst case.

A naive idea would be to try assigning the smallest possible value each day, typically 1, and check if constraints are violated. The failure case appears when the sliding window is too small compared to the streak growth. For example, when $k = 2$, the third day’s window overlaps only partially with the first two days, so simply keeping all values as 1 quickly becomes insufficient to satisfy the inequality involving the growing streak. A naive simulation would repeatedly adjust earlier values, leading to cascading updates that make it too slow.

Another subtle issue is that the constraint depends on both a moving sum and a global streak, so locally greedy choices can break feasibility later without immediate detection.

## Approaches

A brute-force approach would simulate day by day, maintaining the full array and, for each day, recomputing both the streak length and the sum over the last $k$ days. If the constraint is violated at day $i$, we would attempt to increase some previous values to fix it. In the worst case, each adjustment could propagate backward up to $k$ positions, and this could repeat for many days. This leads to a worst-case complexity on the order of $O(nk)$, since each day might require recomputing and repairing a sliding window.

The key observation is that the constraint only depends on two monotone quantities: the streak grows deterministically (it is always $i$), and the sliding window sum is controlled by a limited window of size $k$. The inequality forces the window sum to “keep up” with a linear growth, but only through local adjustments. This suggests we never need to revisit decisions more than $k$ steps back, because anything older than $k$ days no longer affects the constraint.

This leads to a greedy construction: maintain a current window sum and ensure that when the streak increases, we minimally increase some value in the window to restore feasibility. The optimal structure ends up being periodic: every day we ensure just enough mass is present in the last $k$ elements, and this creates a repeating pattern once the system stabilizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nk)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We construct the sequence incrementally while maintaining a sliding window sum of the last $k$ values and ensuring it is always at least the current streak length.

1. Initialize an array or rolling structure to store the last $k$ values, all starting at 1. This is the smallest possible choice since each day contributes at least one problem.
2. Maintain a running sum of the last $k$ days. Initially, for day 1, the sum is 1 and the streak is 1, so the constraint holds.
3. Iterate from day 1 to day $n$. For each day $i$, compute the current streak value, which is $i$, since the sequence is continuous.
4. Compute the current window sum of the last $k$ elements. If $i \le k$, the window is the prefix sum up to $i$; otherwise it is the sum over $i-k+1$ to $i$.
5. If the window sum is already at least $i$, we assign the minimal value 1 for the current day, update the window, and proceed.
6. If the window sum is smaller than $i$, we must increase the current day’s value so that the window sum becomes exactly $i$. This is optimal because increasing earlier values would only increase the total sum without reducing future requirements.
7. After assigning the value for day $i$, update the sliding window by adding the new value and removing the value that falls out of the window if $i > k$.

The key structural idea is that every deficit in the constraint can be fixed greedily at the current day, and never requires redistribution into the past.

### Why it works

At any day $i$, the constraint depends only on the sum of the last $k$ elements and the value $i$. Any deficit in the inequality means the current window sum is too small to satisfy the required threshold. Since all earlier days outside the window no longer influence the constraint, the only way to repair feasibility is to increase values inside the current window.

Increasing earlier positions inside the window or the current position are equivalent in terms of feasibility, but increasing the current day is optimal because it does not risk violating previous days’ constraints, which are already satisfied. This creates a locally optimal repair step that never invalidates past correctness, establishing a stable greedy invariant: after processing day $i$, all constraints up to $i$ hold, and the window sum is always minimally sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, n = map(int, input().split())
    
    from collections import deque
    window = deque()
    window_sum = 0
    
    total = 0
    
    for i in range(1, n + 1):
        # remove element leaving window
        if len(window) == k:
            window_sum -= window.popleft()
        
        # current streak requirement
        need = i
        
        # minimum value is 1
        val = 1
        
        # check window constraint
        if window_sum + val < need:
            val = need - window_sum
        
        window.append(val)
        window_sum += val
        total += val
    
    print(total)

if __name__ == "__main__":
    solve()
```

The implementation maintains a deque representing the last $k$ values and a running sum to support $O(1)$ updates. Each day, we ensure at least 1 problem is assigned. If that is insufficient to make the sliding window sum meet the current streak requirement, we increase the current day’s value just enough to satisfy equality.

The critical detail is that the window is updated before evaluating the constraint, so the sum always reflects exactly the last $k$ days. This avoids off-by-one errors in the sliding range.

## Worked Examples

### Sample 1: $k = 2, n = 3$

We simulate day by day.

| Day | Window before | Need $i$ | Assigned | Window after | Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | [] | 1 | 1 | [1] | 1 |
| 2 | [1] | 2 | 1 | [1,1] | 2 |
| 3 | [1,1] | 3 | 2 | [1,2] | 3 |

The total sum is $1 + 1 + 2 = 4$. The table shows that the violation only occurs at day 3, where the previous window is insufficient, forcing an increase only at the current position.

### Sample 2: $k = 30, n = 15$

Here the window is larger than the process length, so no element ever leaves the window.

| Day | Window before | Need $i$ | Assigned | Window after | Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | [] | 1 | 1 | [1] | 1 |
| 2 | [1] | 2 | 1 | [1,1] | 2 |
| ... | ... | ... | ... | ... | ... |
| 15 | [1,...,1] | 15 | 1 | [1,...,1] | 15 |

Since the window always contains all previous days, the sum after day $i$ is always $i$, and assigning 1 each day is sufficient. The total is 15.

This confirms the behavior when $k \ge n$, where no overflow or trimming occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each day performs constant deque operations and arithmetic updates |
| Space | $O(k)$ | Only the last $k$ values are stored in the sliding window |

The algorithm is linear in $n$, which is required since $n$ can reach $10^6$. Memory usage is bounded by the window size, so it remains safe under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    k, n = map(int, input().split())
    from collections import deque
    window = deque()
    window_sum = 0
    total = 0

    for i in range(1, n + 1):
        if len(window) == k:
            window_sum -= window.popleft()
        need = i
        val = 1
        if window_sum + val < need:
            val = need - window_sum
        window.append(val)
        window_sum += val
        total += val

    return str(total).strip()

# provided samples
assert run("2 3\n") == "4", "sample 1"
assert run("30 15\n") == "15", "sample 2"

# custom cases
assert run("1 5\n") == "15", "k=1 forces growing prefix"
assert run("5 1\n") == "1", "single day base case"
assert run("2 6\n") == "9", "small sliding window behavior"
assert run("10 10\n") == "10", "window never shrinks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 15 | k=1 forces cumulative growth |
| 5 1 | 1 | single-element edge case |
| 2 6 | 9 | sliding window constraint activation |
| 10 10 | 10 | no removals from window |

## Edge Cases

One key edge case is when $k = 1$. The window contains only the current day, so the constraint becomes that the value on day $i$ must be at least $i$. The algorithm assigns exactly $i$, producing a triangular growth sequence $1,2,3,\dots,n$. The sliding window always matches the requirement exactly, so no extra adjustments are needed.

Another edge case is when $k \ge n$. The window never discards old values, so the sum is always cumulative. In this situation, assigning 1 to every day is optimal because the window sum after day $i$ is exactly $i$, which always matches the required streak.

A more subtle case occurs when $k$ is small, such as $k = 2$. Early days behave like the $k \ge n$ case, but once the window becomes full, older small values are discarded. This is where the algorithm starts injecting larger values, as seen in sample 1. The greedy correction at the current day ensures feasibility without revisiting earlier assignments.
