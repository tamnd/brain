---
title: "CF 105789C - Coatless in Yakutsk"
description: "We are given a sequence of daily temperatures and a coat that can be used only in limited stretches. Once you wear it for a number of consecutive days, it becomes dirty and cannot be used again until it is washed."
date: "2026-06-21T13:21:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105789
codeforces_index: "C"
codeforces_contest_name: "The 2025 ICPC Latin America Championship"
rating: 0
weight: 105789
solve_time_s: 59
verified: true
draft: false
---

[CF 105789C - Coatless in Yakutsk](https://codeforces.com/problemset/problem/105789/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily temperatures and a coat that can be used only in limited stretches. Once you wear it for a number of consecutive days, it becomes dirty and cannot be used again until it is washed. You are allowed to choose wash days freely, including washing earlier than necessary, but on any day when you are not wearing the coat, you are exposed to the weather.

The goal is not to minimize the number of coatless days or anything additive like that. Instead, we care about the worst day among all coatless days. We want to schedule wearing and washing so that the coldest day we ever face without a coat is as warm as possible.

Another way to view the objective is to maximize a temperature threshold T such that we can ensure: every day with temperature below T is safely covered by the coat, while days at or above T are allowed to be coatless only in controlled bursts that respect the washing constraint.

A key structural constraint comes from the coat usage limit C. Any consecutive block of coatless days longer than C is impossible to sustain, because it would imply wearing the coat for more than C consecutive days without a wash or interruption.

The input is simply a list of temperatures over N days and an integer C describing the maximum consecutive coat usage. The output is a single integer representing the best achievable minimum temperature among coatless days under an optimal strategy.

The main difficulty is that we are not choosing individual days independently. The constraint couples consecutive days, so local decisions about coatless days can force global infeasibility.

A subtle failure case appears when one tries to greedily mark all “bad” (warm) days as coatless without checking contiguous structure.

For example, consider N = 6, C = 2, and temperatures `[5, 5, 5, 5, 5, 5]`. If we decide a threshold T = 5, all days become coatless, forming a single segment of length 6. Since C = 2, this is invalid. A naive approach that only counts total coatless days would incorrectly accept this configuration.

Another edge case arises when coatless days are split into multiple segments. For instance, `[10, -100, 10]` with C = 1 and threshold T = 10 produces coatless pattern `[1, 0, 1]`, which is valid because no segment exceeds length 1 even though total coatless count is 2. Any solution that ignores contiguity would mis-evaluate feasibility.

These observations show that feasibility depends entirely on contiguous run lengths, not global counts.

## Approaches

A direct approach is to guess a threshold T and check whether it is possible to enforce that all coatless days have temperature at least T without violating the constraint on consecutive coatless stretches. For a fixed T, we mark every day with temperature at least T as coatless. Then we scan the array and measure the longest consecutive run of such days. If that run exceeds C, the threshold is impossible.

This brute-force works because the condition depends only on whether each day crosses a threshold, so each candidate T induces a binary classification of the array. However, trying all possible T values requires up to 101 checks (since temperatures are bounded between -50 and 50), each scanning N days. That leads to about 100N operations, which is acceptable for N up to 10^5.

If temperatures were not bounded, we could instead sort unique values or binary search T. The feasibility check is monotonic: if a threshold T works, any lower threshold also works because fewer days become coatless, never increasing run lengths. This monotonicity allows binary search in O(N log N).

A different perspective avoids thresholds entirely. We can slide a window of size C + 1 over the array. Any such window guarantees that at least one day inside it must be coatless under any valid scheduling strategy, because the coat cannot be worn continuously for more than C days. For each window, we compute its maximum temperature, which represents the worst exposure if that window forces a coatless day. The answer becomes the minimum over all windows of these maxima. This converts the problem into a classic sliding window minimum-of-maximums structure, solvable with a monotonic deque.

Another way to see the structure is to start from a fully coatless world and gradually “protect” the coldest days first. As we reintroduce protection from lowest temperature upward, we track contiguous coatless segments. The moment all segments shrink to length at most C, we have reached the optimal cutoff temperature.

All these views are equivalent. The sliding window and threshold simulation are the most direct and easiest to implement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over thresholds | O(100N) | O(1) | Accepted |
| Sliding window (deque) | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We use the sliding window interpretation, which avoids explicit threshold enumeration and directly computes the limiting structure.

### Steps

1. Consider every contiguous segment of length C + 1 in the array. The reason for this window size is that any violation of the coat constraint must appear inside some block where coat usage would exceed C, which corresponds exactly to C + 1 consecutive coatless days.
2. For each such window, compute the maximum temperature inside it. This value represents the “worst exposure point” if that entire window were forced to contain at least one coatless day.
3. Maintain a running minimum over all these window maximums. This aggregation captures the best possible global guarantee, since every valid schedule must respect every local constraint window.
4. Compute window maximums efficiently using a monotonic deque that stores indices of elements in decreasing order of temperature. As we slide the window, we remove outdated indices and maintain the front as the maximum.
5. After processing all windows, output the minimum recorded maximum.

Each step is driven by the observation that feasibility is controlled by worst contiguous violations, not global distribution.

### Why it works

Any valid strategy must ensure that in every segment of length C + 1, at least one day is coatless. Otherwise, the coat would be used continuously for more than C days, which is impossible. This forces every such segment to “expose” at least one temperature. The worst exposed temperature in a segment is governed by its maximum value, since we are concerned with the highest unavoidable exposure. Minimizing over all segments ensures we choose a threshold that avoids overly cold unavoidable exposures anywhere in the array.

This converts a global scheduling problem into a local window constraint problem where the limiting factor is the worst window.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, c = map(int, input().split())
    a = list(map(int, input().split()))
    
    if c >= n:
        print(max(a))
        return

    k = c + 1
    dq = deque()
    best = float('inf')

    for i, x in enumerate(a):
        while dq and dq[-1][1] <= x:
            dq.pop()
        dq.append((i, x))

        while dq and dq[0][0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            best = min(best, dq[0][1])

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation maintains a deque of candidate maximums for each sliding window of size C + 1. Each element is stored with its index so we can discard elements that fall outside the current window. The deque is kept in decreasing order of temperature so the front always gives the maximum of the current window.

The special case C >= N is handled separately. In that case, the coat never becomes unusable due to consecutive usage limits, so we can effectively choose not to wash in a restrictive way, and the answer reduces to the maximum temperature in the array since we can avoid being coatless except if we choose otherwise.

The most subtle part is window maintenance: the condition `i >= k - 1` ensures we only start recording valid windows after the first full window is formed, and the index pruning ensures correctness when sliding.

## Worked Examples

### Example 1

Input:

`N = 5, C = 1, A = [3, 1, 4, 1, 5]`

We use window size C + 1 = 2.

| i | value | deque (index,value) | window max | best |
| --- | --- | --- | --- | --- |
| 0 | 3 | (0,3) | - | inf |
| 1 | 1 | (0,3),(1,1) | 3 | 3 |
| 2 | 4 | (2,4) | 4 | 3 |
| 3 | 1 | (2,4),(3,1) | 4 | 3 |
| 4 | 5 | (4,5) | 5 | 3 |

Final answer is 3.

This confirms that even though 5 is the maximum temperature, unavoidable exposure inside any length-2 window is governed by the smallest possible window maxima, and the best achievable cutoff is limited by a tighter local structure.

### Example 2

Input:

`N = 4, C = 2, A = [2, 2, 2, 2]`

Window size is 3.

| i | value | deque | window max | best |
| --- | --- | --- | --- | --- |
| 0 | 2 | (0,2) | - | inf |
| 1 | 2 | (0,2),(1,2) | - | inf |
| 2 | 2 | (0,2),(1,2),(2,2) | 2 | 2 |
| 3 | 2 | (1,2),(2,2),(3,2) | 2 | 2 |

Final answer is 2.

This shows that when all values are identical, every window has the same maximum, and the constraint does not force any reduction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element enters and leaves the deque once while maintaining window maxima |
| Space | O(C) | Deque stores at most C + 1 elements |

The algorithm runs comfortably within limits for N up to 10^5. Each operation is constant amortized time, and memory usage is linear in the window size rather than the full array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from collections import deque

    def solve():
        n, c = map(int, input().split())
        a = list(map(int, input().split()))
        
        if c >= n:
            print(max(a))
            return

        k = c + 1
        dq = deque()
        best = float('inf')

        for i, x in enumerate(a):
            while dq and dq[-1][1] <= x:
                dq.pop()
            dq.append((i, x))

            while dq and dq[0][0] <= i - k:
                dq.popleft()

            if i >= k - 1:
                best = min(best, dq[0][1])

        print(best)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided sample-like checks
assert run("5 1\n3 1 4 1 5\n") == "3"
assert run("4 2\n2 2 2 2\n") == "2"

# custom cases
assert run("1 0\n-5\n") == "-5", "single element"
assert run("6 0\n1 2 3 4 5 6\n") == "1", "no consecutive allowance"
assert run("6 10\n1 2 3 4 5 6\n") == "6", "large C"
assert run("3 1\n10 -100 10\n") == "10", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | -5 | minimal boundary |
| C = 0 case | 1 | strict alternation constraint |
| C >= n case | 6 | full flexibility |
| alternating pattern | 10 | correctness under splits |

## Edge Cases

One edge case is when C is zero, meaning you cannot wear the coat on consecutive days at all. For input `N = 6, C = 0, A = [1, 2, 3, 4, 5, 6]`, the algorithm uses window size 1. Each window maximum is just the element itself, so the minimum over all windows is 1. The deque processes each element independently, and no adjacency issues arise because every window is isolated. This matches the fact that every day becomes a separate forced coatless exposure.

Another edge case is when C is very large, such as `N = 5, C = 10, A = [3, 1, 4, 1, 5]`. Here, the condition never binds, so no window of size C + 1 fully exists inside the array. The algorithm directly returns the maximum temperature, which is 5. The special check `if c >= n` ensures we do not run empty-window logic.

A third case is uniform arrays like `A = [7, 7, 7, 7]` with any C. Every window maximum is 7, so the running minimum remains 7. The deque always collapses to a single representative index, and the output remains stable regardless of segmentation.
