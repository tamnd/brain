---
title: "CF 105025E - \u0411\u0430\u043d\u0430\u043d\u043e\u0432\u044b\u0439 \u0431\u0438\u0437\u043d\u0435\u0441 \u041e\u043b\u0435\u0433\u0430"
description: "We are given a sequence of banana prices arranged in a line. Each position holds one value, and we are allowed to perform exactly $k$ operations, where one operation swaps two adjacent elements."
date: "2026-06-28T01:40:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105025
codeforces_index: "E"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 105025
solve_time_s: 59
verified: true
draft: false
---

[CF 105025E - \u0411\u0430\u043d\u0430\u043d\u043e\u0432\u044b\u0439 \u0431\u0438\u0437\u043d\u0435\u0441 \u041e\u043b\u0435\u0433\u0430](https://codeforces.com/problemset/problem/105025/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of banana prices arranged in a line. Each position holds one value, and we are allowed to perform exactly $k$ operations, where one operation swaps two adjacent elements.

After performing these swaps, we look at the final array and evaluate every pair of neighboring positions. For each neighboring pair, we compute the absolute difference of their values, and we care about the maximum such difference. The goal is to arrange the array using exactly $k$ adjacent swaps so that this maximum adjacent difference becomes as large as possible.

The key difficulty is that swaps are local. Even though we are free to rearrange the array, the cost of moving values depends on how far apart they start, since each swap only moves elements by one position.

The constraints push toward an $O(n)$ or $O(n \log n)$ solution. The array length can reach $10^5$, while $k$ can be as large as $10^{18}$, which immediately implies that simulating swaps is impossible. Any approach that treats each swap explicitly will fail.

A subtle edge case appears when $k = 0$. In that situation, the array cannot be changed at all, and the answer is simply the maximum absolute difference over the initial adjacent pairs. Another edge case is when $k$ is extremely large. In that regime, the array becomes almost fully rearrangeable, and we need to understand what structural limitation remains even with many swaps.

## Approaches

We start with the most direct interpretation. We could simulate all sequences of $k$ adjacent swaps and compute the resulting best configuration. This is correct in principle because each state reachable in exactly $k$ swaps corresponds to a valid arrangement. The problem is the branching factor. Each configuration has $O(n)$ possible swaps, and after $k$ steps this grows exponentially. Even for small $n$, this is completely infeasible.

The next step is to stop thinking in terms of sequences of swaps and instead think in terms of how far elements can travel. Each swap changes the position of exactly two elements by one step. If we track two elements that we want to make adjacent, the only relevant question is how many swaps are required to bring them next to each other.

Suppose we take two values at positions $i$ and $j$, with $i < j$. To make them adjacent, we need to eliminate the gap between them. Every swap can reduce this gap by at most one. Therefore, the minimum number of swaps needed to make them adjacent is $j - i - 1$. This observation converts the problem into selecting a pair of indices whose distance is small enough.

We are free to pick any pair of values as the final adjacent pair. So we want to maximize $|c_i - c_j|$ subject to $j - i - 1 \le k$, or equivalently $j - i \le k + 1$.

This reformulation changes the structure completely. Instead of reasoning about permutations, we only need to consider pairs that lie within a bounded index distance. For each valid pair, we imagine spending swaps to bring them together, and the rest of the array can always be adjusted around them without affecting feasibility.

This leads to a sliding window perspective. Any pair of indices inside a segment of length $k + 2$ automatically satisfies the distance constraint. Conversely, any valid pair must lie inside some such segment. So the problem reduces to finding the maximum difference between any two values inside any window of size $k + 2$.

Inside a fixed window, the best pair is simply the minimum and maximum values in that window. So we need to maintain a moving window minimum and maximum over all windows of size $k + 2$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force swap simulation | Exponential | O(n) | Too slow |
| Window min/max after distance reduction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the effective window size $w = k + 2$. If $w \ge n$, treat the entire array as one window. This corresponds to the case where any two elements can be made adjacent within the allowed swaps.
2. Use a sliding window over the array to maintain the maximum and minimum values in the current window. This is done efficiently with two monotonic deques, one maintaining decreasing values for maxima and one maintaining increasing values for minima.
3. For each right endpoint of the window, insert the new element into both deques while preserving monotonic order. Elements that violate monotonicity are removed from the back.
4. Once the window size exceeds $w$, remove elements that fall out of the left boundary from the front of each deque.
5. After each window adjustment, compute the difference between the front of the max deque and the front of the min deque. Track the maximum such difference across all windows.

The reason this works is that any optimal solution corresponds to choosing two elements that become adjacent after at most $k$ swaps. Those two elements must originally lie within distance $k+1$, which guarantees they appear together in some window of size $k+2$. Within that window, the maximum possible adjacent difference after rearrangement is exactly the difference between its minimum and maximum values, since we can always place those two values next to each other using the allowed swaps inside the window constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    w = k + 2
    if w >= n:
        print(max(a) - min(a))
        return

    maxdq = deque()
    mindq = deque()
    ans = 0

    l = 0
    for r in range(n):
        while maxdq and a[maxdq[-1]] <= a[r]:
            maxdq.pop()
        maxdq.append(r)

        while mindq and a[mindq[-1]] >= a[r]:
            mindq.pop()
        mindq.append(r)

        if r - l + 1 > w:
            if maxdq[0] == l:
                maxdq.popleft()
            if mindq[0] == l:
                mindq.popleft()
            l += 1

        if r - l + 1 == w:
            ans = max(ans, a[maxdq[0]] - a[mindq[0]])

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps indices in deques rather than values so that we can efficiently remove elements that slide out of the window. The monotonic property ensures that the front of each deque always represents the extremum of the current window. The only delicate part is maintaining the window size exactly, since windows larger than $k+2$ are invalid for the reduction argument.

## Worked Examples

### Example 1

Input:

```
4 0
1 3 2 4
```

Here the window size is $k+2 = 2$. We only examine adjacent pairs.

| Window | Elements | Min | Max | Difference |
| --- | --- | --- | --- | --- |
| [1,3] | 1,3 | 1 | 3 | 2 |
| [3,2] | 3,2 | 2 | 3 | 1 |
| [2,4] | 2,4 | 2 | 4 | 2 |

The maximum is 2, which matches the best adjacent difference in the original array.

This confirms that when no swaps are allowed, the algorithm reduces to scanning adjacent pairs.

### Example 2

Input:

```
4 2
1 3 2 4
```

Now $w = 4$, so the whole array is a single window.

| Window | Elements | Min | Max | Difference |
| --- | --- | --- | --- | --- |
| [1,3,2,4] | 1,3,2,4 | 1 | 4 | 3 |

The result is 3. This corresponds to the fact that with two swaps we can bring 1 and 4 next to each other, achieving the maximum possible spread.

This demonstrates the regime where the array becomes globally flexible and only extreme values matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index enters and leaves each deque once while maintaining sliding windows |
| Space | O(n) | Deques store at most all indices in the current window |

The solution easily fits within limits because all operations are linear passes over the array, and $n \le 10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        w = k + 2
        if w >= n:
            print(max(a) - min(a))
            return

        maxdq = deque()
        mindq = deque()
        ans = 0

        l = 0
        for r in range(n):
            while maxdq and a[maxdq[-1]] <= a[r]:
                maxdq.pop()
            maxdq.append(r)

            while mindq and a[mindq[-1]] >= a[r]:
                mindq.pop()
            mindq.append(r)

            if r - l + 1 > w:
                if maxdq[0] == l:
                    maxdq.popleft()
                if mindq[0] == l:
                    mindq.popleft()
                l += 1

            if r - l + 1 == w:
                ans = max(ans, a[maxdq[0]] - a[mindq[0]])

        print(ans)

    solve()
    return ""  # placeholder, actual output comparison omitted

# custom sanity checks would normally go here
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 / 5 1 | 4 | smallest window edge case |
| 5 100 / 5 4 3 2 1 | 4 | large k global optimization |
| 6 1 / 1 100 2 3 4 5 | 99 | local window constraint |

## Edge Cases

When $k = 0$, the algorithm sets $w = 2$, so only adjacent pairs are considered. This matches the fact that no swaps are allowed, so the answer must come directly from the original configuration.

When $k \ge n - 2$, the window size becomes at least $n$, so the algorithm collapses into computing $\max(c) - \min(c)$. In this regime, any pair can be made adjacent because there is enough freedom to move elements across the entire array.

When all values are equal, every window produces zero difference, and the deques correctly maintain identical maxima and minima. The algorithm still performs full passes but never overestimates, since both ends of every window are identical.
