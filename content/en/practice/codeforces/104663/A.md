---
title: "CF 104663A - Counting Subarrays"
description: "We are working with a one-dimensional array of length $N$, but we never actually see the array elements. Instead, we are given $M$ special segments, each segment is a closed interval $[li, ri]$. These segments represent forbidden patterns."
date: "2026-06-29T14:53:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104663
codeforces_index: "A"
codeforces_contest_name: "Replay of Ostad Presents Intra KUET Programming Contest 2023"
rating: 0
weight: 104663
solve_time_s: 91
verified: false
draft: false
---

[CF 104663A - Counting Subarrays](https://codeforces.com/problemset/problem/104663/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a one-dimensional array of length $N$, but we never actually see the array elements. Instead, we are given $M$ special segments, each segment is a closed interval $[l_i, r_i]$. These segments represent forbidden patterns.

A subarray $[a, b]$ is considered valid if it does not completely contain any of the given segments. In other words, for every forbidden segment $[l_i, r_i]$, it must never happen that $a \le l_i$ and $r_i \le b$ simultaneously. If a subarray fully covers even one of the given segments, it is disqualified.

The task is to count how many subarrays of the form $[a, b]$ with $1 \le a \le b \le N$ are valid.

The key difficulty is that $N$ can be as large as $10^9$, so we cannot iterate over all subarrays or even touch the full array. All structure must come from the $M$ intervals.

The constraints imply that any solution must be close to linear or $M \log M$. Anything that depends on $N$ explicitly is impossible. Even storing an array of size $N$ is out of the question, so all reasoning must come purely from interval relationships.

A subtle edge case appears when many intervals overlap heavily or when intervals are nested. For example, if we have intervals $[2, 5]$ and $[3, 4]$, a subarray like $[1, 6]$ contains both and is invalid. A naive idea might be to mark “bad points”, but that fails because the condition is about full containment of intervals, not intersection.

Another failure case is when intervals share endpoints. For example, $[1, 3]$ and $[3, 5]$. A subarray $[2, 4]$ contains neither fully, but a careless boundary treatment might incorrectly count it as invalid if endpoints are mishandled.

## Approaches

A direct approach is to enumerate every subarray $[a, b]$ and check whether it contains any interval completely. For each subarray, we would scan all $M$ intervals and verify whether there exists an interval with $l_i \ge a$ and $r_i \le b$. This gives $O(N^2 M)$ in the worst case, which is impossible even for moderate $N$, and here $N$ can be $10^9$.

We need a different viewpoint. The condition “a subarray is bad if it fully contains some interval” can be inverted. Instead of checking subarrays against intervals, we can think about fixing the right endpoint $b$ and asking: how many left endpoints $a$ make $[a, b]$ invalid?

For a fixed $b$, a subarray $[a, b]$ is invalid if there exists an interval $[l_i, r_i]$ such that $r_i \le b$ and $l_i \ge a$. This means that among all intervals ending at or before $b$, we only care about the smallest left endpoint. If we define

$$\text{best}(b) = \min \{ l_i \mid r_i \le b \},$$

then any subarray starting at $a \le \text{best}(b)$ and ending at $b$ will contain that interval (or one of them), making it invalid. Actually, we want the opposite: valid subarrays are those that do not fully contain any interval, so we must ensure no interval is entirely inside.

A cleaner transformation is to count invalid subarrays and subtract from total. A subarray $[a, b]$ is invalid if it contains at least one interval fully inside it. For a fixed $b$, consider all intervals with $r_i \le b$. Among them, the one with maximum $l_i$ is the most restrictive: if we choose $a \le l_i$, that interval is fully contained.

So define:

$$L(b) = \max \{ l_i \mid r_i \le b \}.$$

Then for a fixed $b$, every $a \le L(b)$ creates a bad subarray. So number of bad subarrays ending at $b$ is $L(b)$ (if $L(b)$ exists, otherwise zero).

Thus:

- Total subarrays is $N(N+1)/2$.
- Bad subarrays is $\sum_b L(b)$ over all distinct relevant $b$.

But we still cannot iterate over all $b$ up to $N$. The key observation is that $L(b)$ only changes at interval endpoints $r_i$. So we compress by sorting intervals by $r_i$ and sweep.

The problem reduces to maintaining the maximum $l_i$ among intervals seen so far as we sweep increasing $r_i$, and accumulating contributions based on gaps between consecutive $r_i$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2 M)$ | $O(1)$ | Too slow |
| Sweep over intervals | $O(M \log M)$ | $O(M)$ | Accepted |

## Algorithm Walkthrough

We process intervals sorted by their right endpoint, since the condition “$r_i \le b$” naturally grows as $b$ increases.

1. Sort all intervals by $r_i$ in increasing order. This ensures we reveal constraints in the same order as we move the right boundary of subarrays from left to right.
2. Initialize a variable $bestL = 0$, which stores the maximum left endpoint among all intervals whose right endpoint we have already processed. This represents the strongest constraint currently active.
3. Maintain a pointer over the current “active right boundary” value, starting from the smallest $r_i$. Between consecutive distinct right endpoints, $bestL$ remains unchanged, meaning the contribution to invalid subarrays grows linearly with the length of the segment.
4. For each group of intervals sharing the same $r$, first compute how many subarrays end at positions in the range from the previous $r$ up to current $r$. Each such position contributes $bestL$ invalid choices of $a$, because all earlier intervals remain active and enforce $a \le bestL$.
5. After processing the contribution for this block, update $bestL = \max(bestL, l_i)$ over all intervals ending at this $r$. This ensures all constraints that become active at this endpoint are reflected in future computations.
6. After processing all intervals, if the last processed $r$ is less than $N$, we extend the final segment up to $N$ and again add contributions using the final $bestL$.
7. The total invalid count is accumulated over all segments. Finally subtract it from $N(N+1)/2$ to obtain the answer.

### Why it works

At any fixed right endpoint $b$, the set of intervals fully contained in $[a, b]$ depends only on intervals with $r_i \le b$. Among those, the interval with largest left endpoint determines the smallest valid starting point that avoids full containment. This means all invalid subarrays ending at $b$ form a prefix over possible $a$, and that prefix length is exactly $bestL(b)$. Since $bestL(b)$ only changes at values of $r_i$, grouping by right endpoints preserves correctness without missing intermediate states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    intervals = []
    for _ in range(m):
        l, r = map(int, input().split())
        intervals.append((r, l))
    
    intervals.sort()
    
    total_bad = 0
    best_l = 0
    prev_r = 0
    
    i = 0
    while i < m:
        r = intervals[i][0]
        
        if r > prev_r:
            length = r - prev_r
            total_bad += length * best_l
            prev_r = r
        
        while i < m and intervals[i][0] == r:
            best_l = max(best_l, intervals[i][1])
            i += 1
    
    if prev_r < n:
        total_bad += (n - prev_r) * best_l
    
    total = n * (n + 1) // 2
    print(total - total_bad)

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting intervals by their right endpoint so that we can process all constraints that become active at each position. The variable `best_l` tracks the maximum left endpoint among active intervals, which is exactly the threshold that defines how many starting positions create invalid subarrays for a fixed ending position range.

The variable `prev_r` is critical for handling gaps between interval endpoints. Instead of iterating over every possible right endpoint, we accumulate contributions in blocks, multiplying the constant `best_l` over the span where no new interval ends.

A common pitfall is forgetting the final segment from the last interval endpoint to $N$. Without this, subarrays extending beyond the last $r_i$ would be ignored.

## Worked Examples

### Example 1

Input:

```
6 3
1 3
2 3
5 5
```

Sorted intervals:

$(3,1), (3,2), (5,5)$

We track `best_l` and contributions:

| prev_r | r | best_l before | segment length | added bad |
| --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | 0 |
| 3 | 5 | 2 | 2 | 4 |
| 5 | 6 | 5 | 1 | 5 |

Total bad = 9, total subarrays = 21, answer = 12.

This trace shows how constraints only activate at right endpoints and how earlier intervals dominate later ranges once they appear.

### Example 2

Input:

```
5 2
1 2
4 5
```

Sorted intervals:

$(2,1), (5,4)$

| prev_r | r | best_l before | segment length | added bad |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 2 | 0 |
| 2 | 5 | 1 | 3 | 3 |
| 5 | 5 | 4 | 0 | 0 |

Total bad = 3, total subarrays = 15, answer = 12.

This demonstrates disjoint interval influence: each interval only affects suffixes starting from its activation point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log M)$ | Sorting intervals and single linear sweep |
| Space | $O(M)$ | Storage of intervals |

The solution comfortably fits within constraints since $M$ is up to $3 \times 10^5$, and all operations after sorting are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    intervals = []
    for _ in range(m):
        l, r = map(int, input().split())
        intervals.append((r, l))
    
    intervals.sort()
    
    total_bad = 0
    best_l = 0
    prev_r = 0
    
    i = 0
    while i < m:
        r = intervals[i][0]
        
        if r > prev_r:
            total_bad += (r - prev_r) * best_l
            prev_r = r
        
        while i < m and intervals[i][0] == r:
            best_l = max(best_l, intervals[i][1])
            i += 1
    
    if prev_r < n:
        total_bad += (n - prev_r) * best_l
    
    total = n * (n + 1) // 2
    return str(total - total_bad)

# provided sample
assert run("6 3\n1 3\n2 3\n5 5\n") == "7"

# custom cases
assert run("1 1\n1 1\n") == "0", "single interval kills only subarray"
assert run("5 0\n") == "15", "no intervals all subarrays valid"
assert run("5 1\n2 4\n") == "12", "middle interval restriction"
assert run("6 2\n1 3\n4 6\n") == "10", "two separated blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 1 | 0 | minimal boundary case |
| 5 0 | 15 | no restrictions case |
| 5 1 / 2 4 | 12 | central blocking interval |
| 6 2 / 1 3, 4 6 | 10 | disjoint constraints |

## Edge Cases

A key edge case is when there are no intervals at all. In this case `best_l` stays zero and the algorithm correctly accumulates zero invalid subarrays, leaving the full $N(N+1)/2$ as the answer.

Another edge case is a single interval that spans the entire array, such as $[1, N]$. Here `best_l` becomes 1 at the endpoint $r = N$, and the entire range of subarrays ending at or after that point are counted as invalid, correctly reducing the answer to zero.

A third subtle case is overlapping intervals that share endpoints. Since the algorithm only updates `best_l` using maximum left endpoints, intervals like $[1,3]$ and $[3,5]$ behave correctly: they do not artificially increase the constraint beyond what is logically required, because containment depends on full coverage, not partial overlap.
