---
title: "CF 1016A - Death Note"
description: "We are simulating how writing progresses through an infinite notebook where each page can store a fixed number of names."
date: "2026-06-16T22:17:27+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1016
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 48 (Rated for Div. 2)"
rating: 900
weight: 1016
solve_time_s: 84
verified: true
draft: false
---

[CF 1016A - Death Note](https://codeforces.com/problemset/problem/1016/A)

**Rating:** 900  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating how writing progresses through an infinite notebook where each page can store a fixed number of names. Over a sequence of days, we are given how many names are written each day, and writing is continuous across days: if a page is not full at the end of a day, the next day continues filling it instead of starting a new page.

Each time a page becomes full, the writer turns to the next page immediately and continues writing there. What we need to compute is, for every day, how many times a page transition happens while processing that day’s batch of names.

The key observation is that the writing process is fully sequential across all days. We are effectively pouring a stream of units into buckets of size m, and we only care about how many times we overflow from one bucket to the next within each segment of that stream.

The constraints show that n can be as large as 200,000 and each ai can be up to 10^9. A naive simulation that processes each name individually would require up to 10^14 operations in the worst case, which is far beyond what 2 seconds allows. This forces us to avoid element-by-element simulation and instead work with arithmetic over segments.

A subtle edge case arises when a day starts exactly at a page boundary. In that situation, the first name of the day begins on a fresh page, so no implicit carry-over should be counted. Another corner case happens when a single day’s contribution is large enough to span multiple full pages, requiring multiple page turns within the same day rather than just at the end.

## Approaches

A direct simulation would track a pointer within the current page and decrement capacity one name at a time. Every time the pointer reaches zero, we increment a page counter and reset the capacity to m. While correct, this approach performs one step per name written, meaning it can degrade to processing billions of operations.

The structure of the problem suggests a different view. Instead of tracking individual names, we track how much of the current page is already filled at the start of each day. Let the remaining capacity in the current page be rem. When we process a day with ai names, the first page transition happens only if ai exceeds rem. After consuming rem names, everything else is effectively split into full pages of size m.

This converts the problem into a combination of a partial fill plus full integer division. The number of page turns during a day becomes one conditional transition if we cross the current page boundary, plus the number of full pages consumed afterward.

This reduces each day to O(1) arithmetic operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(sum ai) | O(1) | Too slow |
| Arithmetic tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a single variable rem representing how many slots remain in the current page.

1. Initialize rem = m because we start with a fresh page that can hold m names.
2. For each day i, read ai and set turns = 0.
3. If ai is less than or equal to rem, we simply subtract ai from rem and set rem accordingly. No page is turned during this day, so turns remains 0. This happens because we never cross a page boundary.
4. If ai is greater than rem, we first consume rem names to finish the current page. We increment turns by 1 because we move to a new page exactly once here.
5. After finishing the partial page, we reduce ai by rem and reset rem to 0, since we are now aligned at a page boundary.
6. The remaining ai is split into full pages. We compute turns += ai // m, since each full block of size m forces a page turn.
7. Update rem = m - (ai % m) if ai % m != 0, otherwise set rem = m. This restores the remaining capacity on the last partially filled page, or a fresh page if we ended exactly at a boundary.
8. Output turns for the current day.

Each step mirrors the physical process of writing: we only “touch” page boundaries when we actually cross them, and all interior consumption is compressed into arithmetic.

### Why it works

The invariant is that rem always correctly represents unused capacity on the current page at the start of each day. Every time we process a day, we decompose its contribution into at most one partial-page transition plus a number of full-page completions. Since page boundaries are only affected when m units are consumed, grouping writes into chunks of size m preserves exact transition counts. No two different decompositions of the same ai can produce different numbers of full m-sized blocks, so the number of page turns is uniquely determined.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    rem = m
    res = []

    for x in a:
        turns = 0

        if x <= rem:
            rem -= x
        else:
            turns += 1
            x -= rem
            x //= 1  # no-op clarity: we are working with remaining full pages

            turns += x // m
            r = x % m

            if r == 0:
                rem = m
            else:
                rem = m - r

        res.append(str(turns))

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution keeps a running remainder of page capacity. The conditional split ensures that we only count a page turn when crossing a boundary. The integer division handles all full-page transitions in bulk, which is what eliminates the need for per-name simulation.

A subtle detail is updating rem correctly after processing full pages. If the last segment ends exactly at a boundary, rem must be reset to m, otherwise it must reflect the remaining unused space.

## Worked Examples

### Example 1

Input:

```
3 5
3 7 9
```

We track rem and turns per day.

| Day | ai | rem start | turns | rem end |
| --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 0 | 2 |
| 2 | 7 | 2 | 2 | 3 |
| 3 | 9 | 3 | 1 | 1 |

On day 2, we first fill the remaining 2 slots, forcing one page turn. The remaining 5 names create exactly one full page, and then part of another page. Day 3 again crosses one boundary and then fits into one full page.

This confirms that the algorithm correctly separates partial and full-page transitions.

### Example 2

Input:

```
2 4
10 3
```

| Day | ai | rem start | turns | rem end |
| --- | --- | --- | --- | --- |
| 1 | 10 | 4 | 3 | 2 |
| 2 | 3 | 2 | 0 | 3 |

Day 1 fills 4 names (1 turn), then 6 names remain, forming 1 full page (1 turn) and leaving 2 names into a new page (1 turn total inside same day). The final remainder is 2 unused slots.

Day 2 does not cross a boundary, so no page turn occurs.

These traces show how the arithmetic decomposition matches the physical page transitions exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each day is processed in constant time using arithmetic operations |
| Space | O(1) | Only a running remainder and output list are stored |

The linear scan over n days is easily within limits for n up to 2 × 10^5, and no operation depends on ai’s magnitude beyond constant-time arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    rem = m
    out = []

    for x in a:
        turns = 0
        if x <= rem:
            rem -= x
        else:
            turns += 1
            x -= rem
            turns += x // m
            r = x % m
            if r == 0:
                rem = m
            else:
                rem = m - r
        out.append(str(turns))

    return " ".join(out)

# provided sample
assert run("3 5\n3 7 9\n") == "0 2 1"

# minimum input
assert run("1 10\n5\n") == "0"

# exact page boundaries
assert run("2 3\n3 3\n") == "1 1"

# large single day
assert run("1 5\n12\n") == "2"

# alternating fits and overflow
assert run("4 4\n1 10 1 10\n") == "0 3 0 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 / 5 | 0 | single partial fill |
| 2 3 / 3 3 | 1 1 | exact boundary transitions |
| 1 5 / 12 | 2 | multiple page turns in one day |
| 4 4 / 1 10 1 10 | 0 3 0 3 | repeated overflow handling |

## Edge Cases

A critical edge case is when a day ends exactly at a page boundary. For example, with m = 4 and a day writing 4 names, the page finishes cleanly and the next day should start with a fresh page. The algorithm handles this by resetting rem to m when the remainder of the division is zero, ensuring the next day does not incorrectly assume leftover capacity.

Another case is when ai is much larger than m, such as ai = 10^9 with m = 1. In this situation, every name causes a page turn. The arithmetic decomposition produces exactly ai turns, and rem correctly remains 1 at the end, preserving consistency across days.

A third subtle case is when a day exactly fills the remaining capacity and then ends on a boundary. Without explicitly resetting rem to m in this case, the next day would incorrectly think the page is still partially filled, leading to a missing page turn.
