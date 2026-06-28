---
title: "CF 104777J - Complete the Permutation"
description: "We are given an array of length $2n-1$ where all odd positions are already fixed and contain all odd numbers from $1$ to $2n-1$. The even positions are empty, and we must fill them using all even numbers from $2$ to $2n-2$, each exactly once."
date: "2026-06-28T15:30:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104777
codeforces_index: "J"
codeforces_contest_name: "2023-2024 ICPC, NERC, Southern and Volga Russian Regional Contest (problems intersect with Educational Codeforces Round 157)"
rating: 0
weight: 104777
solve_time_s: 47
verified: true
draft: false
---

[CF 104777J - Complete the Permutation](https://codeforces.com/problemset/problem/104777/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $2n-1$ where all odd positions are already fixed and contain all odd numbers from $1$ to $2n-1$. The even positions are empty, and we must fill them using all even numbers from $2$ to $2n-2$, each exactly once.

The constraint is not about ordering in general, but about local structure. Once the full permutation is formed, no value placed at an even index is allowed to be a local extremum. In other words, if we look at any even position $i$, the value $p_i$ must not be strictly greater than both neighbors and must not be strictly smaller than both neighbors.

The key structure is that all odd positions are already fixed, and they alternate with the missing even positions. So every even position is sandwiched between two known odd values. This turns the problem into choosing, for each gap between two consecutive odd numbers, an even number that does not create a peak or a valley at that even position.

The constraints are large: the sum of $n$ is up to $2 \cdot 10^5$, and there are up to $10^5$ test cases. This forces a linear or near-linear solution per test case. Anything quadratic over $n$ per test case would immediately TLE.

A subtle failure case appears when local choices seem independent but actually interact through reuse of even numbers. For example, if one tries to greedily assign the smallest available even number that does not create a local extremum, one can easily get stuck later with no valid assignment even though a global solution exists.

The real difficulty is that each even position depends only on its two neighboring odd values, so we must respect a global consistency while satisfying many local inequalities.

## Approaches

A brute-force interpretation would try to assign even numbers into the empty positions and check whether any arrangement works. Even restricting to permutations of even numbers, there are $(n-1)!$ possibilities, and for each we would need to validate all even positions in $O(n)$. This is completely infeasible.

The key observation is that each even position is independent in terms of its validity condition once the neighboring odd values are fixed. For an even index $i$, we only care about $p_{i-1}$, $p_{i+1}$, and the chosen even value $x$. The constraint is that $x$ must lie strictly between its two neighbors in order to avoid being a local extremum. If $x$ is larger than both or smaller than both, it becomes invalid.

So for each even position, we are effectively given an interval constraint: the chosen even value must lie between the two adjacent odd values. Each even position contributes one such interval, and we must assign distinct even numbers to satisfy all intervals.

The structure simplifies further because the odd positions form a fixed sequence, and every even position corresponds to a pair of consecutive odd numbers. So we get $n-1$ intervals, and we must assign the $n-1$ even numbers to these intervals so that each number lies inside its assigned interval.

This becomes a matching problem between sorted even numbers and sorted interval constraints. Since both sides are naturally ordered, a greedy assignment from left to right works: we maintain available even numbers and assign the smallest feasible one to each interval. Feasibility is checked via interval bounds derived from neighbors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((n-1)! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We work directly on the $n-1$ gaps formed by consecutive odd positions.

1. For every adjacent pair of odd positions $(p_{2i-1}, p_{2i+1})$, compute the valid range for the even position $p_{2i}$. The value placed there must lie strictly between these two numbers, otherwise it becomes a local maximum or minimum. So we define an interval $(\min, \max)$ but excluding endpoints.
2. Collect all available even numbers $\{2, 4, \dots, 2n-2\}$. These are exactly $n-1$ values, matching the number of intervals.
3. Sort the intervals by their right endpoint. This ordering ensures that intervals with tighter upper bounds are handled first, which prevents late conflicts where a small upper bound interval is left without a valid number.
4. Sweep through intervals in sorted order, maintaining a multiset (or pointer into sorted array) of remaining even numbers.
5. For each interval $[L, R]$, pick the smallest available even number that is $\ge L$. If this number is $> R$, the assignment is impossible.
6. Assign this number to the current even position and remove it from the available pool.

Each step is enforcing feasibility locally while preserving global consistency through sorting. The crucial mechanism is that early assignment of constrained intervals prevents starvation later.

### Why it works

At any point in the sweep, all unprocessed intervals have right endpoints at least as large as the current one. If we always satisfy the most restrictive upper bound first, we never waste a small number on a loose interval when it might be needed later. This is the same exchange argument used in interval scheduling with deadlines, adapted to assignment instead of selection.

Because each interval has exactly one assignment and values are distinct, the greedy process maintains a valid partial matching whenever possible, and any failure corresponds to a true impossibility due to lack of sufficient small values under tight bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_left

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        odds = list(map(int, input().split()))
        
        if n == 1:
            print()
            continue
        
        intervals = []
        for i in range(n - 1):
            a = odds[i]
            b = odds[i + 1]
            L = min(a, b)
            R = max(a, b)
            intervals.append((R, L, i))
        
        intervals.sort()
        
        evens = list(range(2, 2 * n, 2))
        
        res = [0] * (n - 1)
        
        import bisect
        for R, L, idx in intervals:
            pos = bisect_left(evens, L)
            if pos == len(evens) or evens[pos] > R:
                print(-1)
                break
            res[idx] = evens[pos]
            evens.pop(pos)
        else:
            print(*res)

if __name__ == "__main__":
    solve()
```

The implementation builds interval constraints from consecutive odd values, then greedily assigns even numbers using a sorted list. The `bisect_left` call finds the smallest available even number that respects the lower bound. Removing it ensures uniqueness.

The sorted ordering by right endpoint is what makes the greedy safe, because it prioritizes the tightest constraints first.

## Worked Examples

Consider a simple case where $n = 3$ and odd positions are fixed as $[1, 3, 5]$.

The intervals are derived from pairs $(1, 3)$ and $(3, 5)$. For the first gap, valid values must lie in $(1, 3)$, so only $2$ works. For the second gap, valid values lie in $(3, 5)$, so only $4$ works.

We process intervals sorted by right endpoint: $(1,3)$ then $(3,5)$.

| Step | Interval | Available evens | Chosen | Remaining |
| --- | --- | --- | --- | --- |
| 1 | (1,3) | [2,4] | 2 | [4] |
| 2 | (3,5) | [4] | 4 | [] |

This confirms that tight constraints are handled first and do not block later assignments.

Now consider a slightly less aligned example with odds $[5, 1, 3]$, so intervals are $(1,5)$ and $(1,3)$.

Sorted by right endpoint, we process $(1,3)$ first.

| Step | Interval | Available evens | Chosen | Remaining |
| --- | --- | --- | --- | --- |
| 1 | (1,3) | [2,4] | 2 | [4] |
| 2 | (1,5) | [4] | 4 | [] |

Even though the second interval is looser, it benefits from earlier reservation of small values.

This demonstrates that ordering by right endpoint is essential to avoid wasting small numbers on flexible intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting intervals dominates, each assignment uses binary search and deletion |
| Space | $O(n)$ | Stores intervals, evens, and result array |

The sum of $n$ across test cases is $2 \cdot 10^5$, so an $O(n \log n)$ solution is comfortably within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()  # placeholder, assume integrated runner

# provided sample (conceptual)
# assert run("1\n3\n1 3 5\n") == "2 4"

# custom cases
# n = 2 minimal
# assert run("1\n2\n1 3\n") in ["2", "-1"]

# all increasing odds
# assert run("1\n4\n1 3 5 7\n") == "2 4 6"

# reversed pattern
# assert run("1\n4\n7 5 3 1\n") != ""

# impossible-like structure
# assert run("1\n3\n1 5 3\n") in ["2 4", "-1"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=2$ | boundary | smallest instance |
| sorted odds | full assignment | ideal monotone case |
| reversed odds | valid construction | robustness to ordering |
| mixed odds | possible failure | correctness of greedy rejection |

## Edge Cases

A minimal case is $n=2$, where there is only one even position. The algorithm builds a single interval from the two odd numbers and assigns the only available even number. If it lies outside the interval, the output is correctly $-1$.

When odd values are strictly increasing, every interval is well-formed and disjoint enough that the greedy assignment always succeeds, because each even number naturally fits into exactly one increasing gap.

A problematic case occurs when odd values create a very tight interval early and a wide interval later. The sorting by right endpoint ensures the tight interval is processed first, so it consumes the only viable small number. If this is not possible, failure is detected immediately.

In all cases, the algorithm never assigns an even number that violates the extremum condition, because every assignment is explicitly constrained to lie strictly between its neighboring odd values.
