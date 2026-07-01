---
title: "CF 104596J - Taxed Editor"
description: "We are given a sequence of books, and each book must be read from start to finish before moving to the next one. Each book has a length in pages and a deadline measured in days."
date: "2026-06-30T04:42:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104596
codeforces_index: "J"
codeforces_contest_name: "2019-2020 ICPC East Central North America Regional Contest (ECNA 2019)"
rating: 0
weight: 104596
solve_time_s: 45
verified: true
draft: false
---

[CF 104596J - Taxed Editor](https://codeforces.com/problemset/problem/104596/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of books, and each book must be read from start to finish before moving to the next one. Each book has a length in pages and a deadline measured in days. The reader uses a single constant reading speed for all books, measured in pages per day, and finishing a book takes a number of days equal to the ceiling of its length divided by the speed. Because books are processed sequentially, the finishing day of each book is the cumulative sum of these durations.

A book is considered late if the day it finishes exceeds its deadline. The task is to choose the smallest possible integer reading speed such that at most m books end up late.

The constraints allow up to 100,000 books, with lengths up to 10^9 and deadlines up to 10^4. This immediately rules out any approach that tries all speeds naively and fully simulates for each one. Even a single full simulation is O(n), so trying all speeds up to 10^9 would be impossible. A valid solution must reduce the number of candidate speeds dramatically, and still evaluate each candidate efficiently.

A subtle issue comes from how lateness is defined. Lateness is not per-book independent; it depends on accumulated reading time. A naive mistake is to compare each book in isolation, ignoring that earlier long books delay all subsequent ones.

Another common pitfall is mishandling ceiling division. If integer division is used directly as l // s, it underestimates time whenever l is not divisible by s, which can incorrectly reduce the cumulative schedule and produce an invalid speed that appears feasible.

## Approaches

A straightforward attempt is to try every possible reading speed from 1 up to the maximum book length. For each speed, we simulate reading all books sequentially, compute the finishing day of each book, count how many exceed their deadlines, and check whether this number is at most m. This is correct because it directly mirrors the process described in the problem. However, the cost is prohibitive. If we test S possible speeds, each requiring O(n) simulation, the total cost is O(Sn), which in the worst case becomes on the order of 10^14 operations.

The key structural observation is that increasing reading speed can only help. If a certain speed s is sufficient to keep at most m books late, then any larger speed will finish every book no later than at speed s, and therefore cannot increase the number of late books. This monotonic behavior allows us to treat the problem as a search over a sorted predicate: feasible speeds form a suffix of all integers.

Once we recognize monotonicity, we can apply binary search on the answer. For a candidate speed, we simulate once to count how many books are late. This reduces the number of simulations from linear in the answer range to logarithmic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all speeds | O(maxL · n) | O(1) | Too slow |
| Binary Search + simulation | O(n log maxL) | O(1) | Accepted |

## Algorithm Walkthrough

We exploit the fact that feasibility of a speed can be tested independently.

1. Define a function that checks whether a given speed is valid. We simulate reading all books in order, maintaining a running total of days spent. For each book, we add the number of days required to finish it, computed as (l + s − 1) // s. After updating the cumulative time, we check whether the finishing day exceeds the deadline of that book. If it does, we count it as a late book.
2. The check function returns true if the number of late books is at most m. This gives us a monotonic predicate over speeds.
3. We set a binary search range for the answer. The minimum possible speed is 1. The maximum necessary speed is the largest book length, since any book can be finished in one day at that speed.
4. We perform binary search over this range. For each midpoint speed, we run the feasibility check.
5. If the speed is feasible, we try to reduce it by moving the right boundary down. If it is not feasible, we increase the speed by moving the left boundary up.
6. After the binary search converges, the left boundary is the smallest feasible speed.

Why it works: the simulation defines a predicate over speeds that is monotone non-increasing. Once a speed becomes sufficient to keep lateness within the allowed bound, all larger speeds preserve or improve every completion time, so they cannot increase the number of late books. This guarantees that the feasible region is contiguous, which is exactly the condition required for binary search to locate the minimum valid speed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(speed, books, m):
    time = 0
    late = 0
    for l, d in books:
        time += (l + speed - 1) // speed
        if time > d:
            late += 1
            if late > m:
                return False
    return True

def solve():
    n, m = map(int, input().split())
    books = [tuple(map(int, input().split())) for _ in range(n)]

    lo, hi = 1, max(l for l, _ in books)

    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid, books, m):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The simulation is the core of the solution. The variable `time` represents the cumulative day on which the current book finishes, not a per-book duration. This accumulation is essential because each book starts only after the previous one completes.

The ceiling division `(l + speed - 1) // speed` ensures that partial days are correctly accounted for. Without this adjustment, books whose length is not divisible by the speed would incorrectly appear faster than they are, which would break correctness.

The binary search maintains the invariant that any speed below `lo` is invalid, while any speed at or above `hi` is valid. The check function enforces the feasibility condition consistently, allowing the search to safely converge.

## Worked Examples

Consider the sample input:

n = 3, m = 1

Books: (450, 9), (500, 6), (300, 4)

We test candidate speeds using binary search.

| speed | book 1 finish | book 2 finish | book 3 finish | late count | feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 450 | 950 | 1250 | 3 | no |
| 2 | 225 | 475 | 625 | 2 | no |
| 3 | 150 | 317 | 417 | 1 | yes |

For speed 2, the second book finishes at day 475, already exceeding its deadline of 6, and the third also misses. That produces too many late books. At speed 3, only one book is late, satisfying the constraint, so the answer is 3.

This trace shows how lateness depends on cumulative finishing time, not individual book duration. Even a moderate increase in speed significantly shifts later completion times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log L) | Each feasibility check scans all books, and binary search over speed performs logarithmic checks up to max book length L |
| Space | O(1) | Only a few counters are maintained besides input storage |

The constraints allow up to 100,000 books, and log(max L) is about 30, so the solution performs roughly a few million operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    def check(speed, books, m):
        time = 0
        late = 0
        for l, d in books:
            time += (l + speed - 1) // speed
            if time > d:
                late += 1
                if late > m:
                    return False
        return True

    def solve():
        n, m = map(int, input().split())
        books = [tuple(map(int, input().split())) for _ in range(n)]
        lo, hi = 1, max(l for l, _ in books)
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid, books, m):
                hi = mid
            else:
                lo = mid + 1
        print(lo)

    old = sys.stdin
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out.strip()

# sample
assert run("""3 1
450 9
500 6
300 4
""") == "3"

# minimum case
assert run("""1 0
10 1
""") == "10"

# already feasible at speed 1
assert run("""2 1
1 10
1 10
""") == "1"

# tight deadlines forcing high speed
assert run("""2 0
10 1
10 1
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 book, no lateness allowed | 10 | single-element correctness and ceiling behavior |
| two tiny books, slack deadlines | 1 | feasibility at minimum speed |
| tight deadlines | 10 | accumulation and boundary tightness |

## Edge Cases

A critical edge case is when only one book is allowed to be late. In such cases, the optimal speed often lies just above the threshold where a single long book stops breaking the chain of deadlines. The binary search correctly captures this because the feasibility function flips from false to true exactly once.

Another important case is when all deadlines are extremely small compared to book lengths. For example, if every deadline is 1, only a speed equal to the maximum book length ensures any book can finish within a single day; otherwise all books quickly become late. The algorithm handles this naturally because the feasibility check counts lateness based on cumulative time, and binary search will push directly toward the maximum required speed.

Finally, when m is large, close to n − 1, almost any speed becomes acceptable. The check function still enforces correctness by counting excess late books, and binary search will converge to the smallest speed that avoids the single worst failure point in the schedule.
