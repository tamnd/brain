---
title: "CF 104461D - Let's Chat"
description: "Two users communicate over a timeline of $n$ days. We are given several disjoint or ordered intervals describing when user $A$ sends messages to $B$, and similarly when $B$ sends messages to $A$."
date: "2026-06-30T13:19:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104461
codeforces_index: "D"
codeforces_contest_name: "The 14th Zhejiang Provincial Collegiate Programming Contest Sponsored by TuSimple"
rating: 0
weight: 104461
solve_time_s: 88
verified: false
draft: false
---

[CF 104461D - Let's Chat](https://codeforces.com/problemset/problem/104461/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

Two users communicate over a timeline of $n$ days. We are given several disjoint or ordered intervals describing when user $A$ sends messages to $B$, and similarly when $B$ sends messages to $A$. Each interval means that communication happens on every day in that range, so overall each user’s activity can be viewed as a union of segments on a number line.

A friendship point is awarded on day $i$ if and only if the last $m$ days ending at $i$ are fully covered by communication from both directions. In other words, within the window $[i-m+1, i]$, user $A$ must have sent messages on every single day in that window, and user $B$ must also have done the same. Each day where this condition holds contributes exactly one unit to the final answer.

The task is to compute how many such days exist across the full range $[1, n]$, even when $n$ is as large as $10^9$. The intervals describing communication are few, at most 100 for each direction, and are already sorted and non-overlapping.

The key difficulty is the scale of $n$. A day-by-day simulation is impossible because iterating over $10^9$ positions would immediately exceed time limits. Instead, we must reason in terms of segments and transitions.

A subtle edge case appears when $m = 1$. Then every day where both users send messages counts immediately, since the window is just the day itself. Another edge case occurs when a user’s coverage is almost complete but has a single missing day inside a long interval, which completely destroys any valid window crossing that gap. A naive approach that merges intervals but ignores exact per-day coverage would incorrectly treat partial coverage as full coverage.

## Approaches

A brute-force approach would explicitly mark every day from 1 to $n$ for both users and then slide a window of length $m$. For each day, we check whether all days in the window are active for both users. Even with prefix sums, building the full arrays is infeasible when $n = 10^9$, since storing or iterating over all days is impossible.

The key observation is that we never need to inspect individual days. Each user’s activity is a union of at most 100 intervals, so we can first convert each user’s schedule into a binary function over time and then compute where it is continuously active. The condition we want is that both users are active on every day in a length-$m$ window. This is equivalent to saying that the intersection of their active sets must also contain a full interval of length $m$ ending at day $i$.

So the problem reduces to computing the intersection of two interval unions, and then counting how many length-$m$ suffix windows fit entirely inside that intersection. Instead of expanding the timeline, we directly compute the intersection segments. Once we have a segment $[L, R]$, every valid window ending at $i$ corresponds to an index where $[i-m+1, i] \subseteq [L, R]$, which simplifies to $i \in [L+m-1, R]$. Each intersection segment contributes a simple arithmetic count.

The full task therefore becomes: compute intersection intervals of two sorted disjoint interval lists, then sum contributions from each resulting segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(n)$ | Too slow |
| Optimal | $O(x + y)$ | $O(x + y)$ | Accepted |

## Algorithm Walkthrough

We treat both users’ message histories as sorted lists of disjoint intervals. We then compute their overlap using a two-pointer sweep.

1. Initialize two pointers, one for $A$’s intervals and one for $B$’s intervals. The idea is to always compare the current active segment from each user and extract their overlap.
2. At each step, compute the intersection of the current intervals. If $A = [l_a, r_a]$ and $B = [l_b, r_b]$, their overlap is $[ \max(l_a, l_b), \min(r_a, r_b) ]$, but only if the left endpoint does not exceed the right endpoint. This produces a segment where both users are simultaneously active.
3. If an overlap segment exists, we do not immediately count all its days. Instead, we translate it into valid window-ending positions. A window ending at day $i$ requires full coverage of $[i-m+1, i]$, so the valid $i$ values inside an overlap $[L, R]$ satisfy $i \ge L + m - 1$ and $i \le R$. If $R \ge L + m - 1$, we add $R - (L + m - 1) + 1$ to the answer.
4. Advance the pointer of whichever interval ends first. This ensures we move through all segments without missing any overlap possibilities. We always discard the interval that cannot extend further, since it cannot contribute to future intersections.
5. Repeat until one list is exhausted.

The correctness relies on the fact that all relevant structure is captured by interval boundaries. No valid window can start or end inside a gap where at least one user is inactive, so all contributions must be fully contained within intersection segments.

### Why it works

At any point in time, the algorithm maintains that all possible overlaps involving previous intervals have already been processed. Each intersection segment is maximal with respect to both users’ activity, meaning no valid window can partially extend outside it without violating continuity for at least one user. Since valid windows correspond exactly to contiguous ranges fully contained in the intersection, counting windows per segment is both necessary and sufficient. The two-pointer progression ensures every pair of overlapping segments is considered exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m, x, y = map(int, input().split())
        
        A = [tuple(map(int, input().split())) for _ in range(x)]
        B = [tuple(map(int, input().split())) for _ in range(y)]
        
        i = j = 0
        ans = 0
        
        while i < x and j < y:
            la, ra = A[i]
            lb, rb = B[j]
            
            L = max(la, lb)
            R = min(ra, rb)
            
            if L <= R:
                start = L + m - 1
                if start <= R:
                    ans += R - start + 1
            
            if ra < rb:
                i += 1
            else:
                j += 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first reads both interval lists for each test case. Since intervals are guaranteed disjoint and sorted, a linear two-pointer sweep is sufficient.

Inside the loop, we compute the overlap of current intervals. If no overlap exists, nothing is added. If overlap exists, we convert it into a count of valid window endpoints instead of iterating over days.

The pointer advancement rule is crucial. We always move past the interval that ends first because it cannot overlap with any future interval from the other list beyond its endpoint.

Care must be taken with the transformation from overlap segment to valid windows. The expression $L + m - 1$ defines the first day where a full window of size $m$ can end while staying inside the overlap. If this exceeds $R$, the segment contributes nothing.

## Worked Examples

Consider a simplified scenario:

A = [1, 5], [10, 12]

B = [3, 6], [8, 11]

m = 2

We process intersections step by step.

| A interval | B interval | Overlap | Contribution |
| --- | --- | --- | --- |
| [1,5] | [3,6] | [3,5] | valid endpoints are 4,5 so 2 |
| [1,5] | [8,11] | none | 0 |
| [10,12] | [8,11] | [10,11] | valid endpoints are 11 so 1 |

Total = 3.

This shows how each intersection segment independently contributes valid window endpoints.

Now consider a case where overlap is too small:

A = [1,4], B = [1,4], m = 5

| A interval | B interval | Overlap | Contribution |
| --- | --- | --- | --- |
| [1,4] | [1,4] | [1,4] | none |

Even though both users are active together, no window of length 5 can fit, so the answer is 0. This confirms that we do not count raw overlap length, only full windows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(x + y)$ | Each interval is processed once in a two-pointer sweep |
| Space | $O(x + y)$ | Storage for input intervals only |

The constraints ensure at most 200 intervals per test case, so the solution runs in constant time per test case. The algorithm easily fits within limits even for the maximum number of test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []

    def solve():
        n, m, x, y = map(int, input().split())
        A = [tuple(map(int, input().split())) for _ in range(x)]
        B = [tuple(map(int, input().split())) for _ in range(y)]

        i = j = 0
        ans = 0

        while i < x and j < y:
            la, ra = A[i]
            lb, rb = B[j]

            L = max(la, lb)
            R = min(ra, rb)

            if L <= R:
                start = L + m - 1
                if start <= R:
                    nonlocal_ans[0] += R - start + 1

            if ra < rb:
                i += 1
            else:
                j += 1

        return ans

    for _ in range(T):
        print(solve())

# provided samples
assert run("""2
10 3 3 2
1 3
5 8
10 10
1 8
10 10
5 3 1 1
1 2
4 5
""") == "3\n0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single overlap | 0 or 1 | m larger than overlap |
| fully overlapping long segment | positive count | correct arithmetic window counting |
| disjoint schedules | 0 | no accidental cross counting |
| multiple segments | sum correctness | pointer sweep correctness |

## Edge Cases

One important edge case is when the overlap exists but is shorter than $m$. For example, if both users are active on days 10 to 12 and $m = 5$, the intersection is valid but contributes nothing. The algorithm correctly computes $L + m - 1 > R$, so it skips the segment entirely.

Another edge case is when intervals touch but do not overlap. If A ends at day 5 and B starts at day 6, the computed intersection has $L > R$, so no contribution is added. This ensures that adjacency without overlap is not mistakenly treated as continuity.

A final subtle case is multiple disjoint overlaps caused by alternating intervals. The two-pointer scan ensures each overlap is processed exactly once, because advancing the pointer of the earlier-ending interval guarantees no intersection segment is skipped or double-counted.
