---
title: "CF 105535K - Know Your Duration of Stay"
description: "We are given a calendar that is no longer the standard one year structure, but instead consists of a sequence of months, each with its own number of days. A date is represented as a pair of integers: a day inside a month and the month index."
date: "2026-06-23T23:06:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105535
codeforces_index: "K"
codeforces_contest_name: "2024 ICPC Belarus Regional Contest"
rating: 0
weight: 105535
solve_time_s: 54
verified: true
draft: false
---

[CF 105535K - Know Your Duration of Stay](https://codeforces.com/problemset/problem/105535/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a calendar that is no longer the standard one year structure, but instead consists of a sequence of months, each with its own number of days. A date is represented as a pair of integers: a day inside a month and the month index.

Each query describes a trip: a client arrives on a specific day in a month and leaves on another day in another month, with the guarantee that the departure is not earlier than the arrival in the cyclic sense of a single year. The task is to compute how many calendar days the client stays, counting both the arrival day and the departure day.

The structure suggests we are working inside a single linear timeline of length equal to the sum of all month lengths. Every date can be mapped to a single integer position in this timeline. Once that mapping exists, each query becomes a simple difference between two positions plus one.

The constraints are large enough that any solution must process each query in constant time after preprocessing. The total number of months and queries across all test cases is at most 100000, and the total number of days across a year can be up to 10^9. This rules out any per-query simulation over days or months.

A subtle edge case arises from the inclusive nature of the interval. If arrival and departure are the same day, the answer must be 1, not 0. Another potential pitfall is incorrectly handling month boundaries when converting dates into a linear index. For example, if months are [3, 5] and a query is (3rd day of month 1) to (1st day of month 2), the correct answer is 3, not 2 or 1 depending on indexing mistakes.

## Approaches

A direct approach is to simulate the passage of days for each query. Starting from the arrival date, we increment day by day until we reach the departure date, counting steps. This is conceptually correct, but in the worst case a single query could span nearly an entire year, and there can be up to 100000 queries. With a year size up to 10^9 in total length, this becomes completely infeasible.

The key observation is that the calendar is static. Once we convert each date into its absolute position in a flattened array of days, every query becomes a simple arithmetic difference. This is a classic prefix sum setting: we precompute the starting index of each month in the flattened timeline. Then any date (d, m) maps to prefix[m - 1] + d.

After this transformation, each query answer is computed in O(1) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(total days per query) | O(1) | Too slow |
| Prefix Sum Mapping | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the calendar into a prefix sum array over months, then use it to map dates into a linear timeline.

1. Build a prefix sum array where prefix[i] stores the total number of days from month 1 up to month i. This allows us to compute the absolute day index of any date in constant time. The reason this works is that months form a contiguous partition of the year.
2. For each query, convert the arrival date (sd, sm) into an absolute position using prefix[sm - 1] + sd. This gives the 1-based index of the day in the full year.
3. Convert the departure date (ed, em) in the same way using prefix[em - 1] + ed. Both values now lie on the same linear scale.
4. The answer is the difference between these two positions plus one. The +1 accounts for inclusive counting of both endpoints.

Why it works

The prefix sum array defines a bijection between calendar dates and integer positions in a continuous sequence of days. Each month contributes a contiguous block, so no overlaps or gaps exist in the mapping. Since both endpoints are mapped into this consistent global ordering, the distance between them in the flattened array exactly equals the number of days between them in the original calendar, including both endpoints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + a[i - 1]

    out = []
    for _ in range(m):
        sd, sm, ed, em = map(int, input().split())

        start = pref[sm - 1] + sd
        end = pref[em - 1] + ed

        out.append(str(end - start + 1))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    solve()
```

The prefix array construction accumulates month lengths so that each month is assigned a fixed starting offset. The key detail is using pref[sm - 1], since month indices are 1-based in input but prefix is 0-based. The same applies to the departure month.

The subtraction end - start + 1 enforces inclusive counting. Without the +1, identical start and end dates would incorrectly yield zero.

## Worked Examples

Consider a simple calendar with months [3, 5].

The prefix array becomes [0, 3, 8].

First query: (2, 1) to (1, 2).

| Step | sm | sd | em | ed | start | end | answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | 1 | 0 + 2 = 2 | 3 + 1 = 4 | 3 |

The interval corresponds to days 2 through 4 in the flattened array, so the result is 3.

This confirms that cross-month transitions are handled cleanly by the prefix mapping.

Now consider a single-month case with [10], query (1, 1) to (10, 1).

| Step | sm | sd | em | ed | start | end | answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 10 | 1 | 10 | 10 |

This shows that within a single month, the formula reduces correctly to simple difference inside a contiguous block.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | prefix construction is linear in months, each query is O(1) |
| Space | O(n) | prefix array stores cumulative month lengths |

The constraints allow up to 100000 total months and queries, so linear preprocessing and constant-time query handling comfortably fit within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip()

# We assume solve() is defined above; in real use, you'd import it.

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# minimal case
assert run("""1 1
10
1 1 10 1
""") == "10"

# same day
assert run("""2 1
5 7
3 1 3 1
""") == "1"

# cross month
assert run("""2 2
3 5
2 1 1 2
1 2 5 2
""") == "3\n5"

# full year
assert run("""3 1
2 3 4
1 1 4 3
""") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single month full span | 10 | inclusive counting |
| same day query | 1 | off-by-one handling |
| cross month transitions | 3, 5 | prefix correctness |
| full year query | 9 | global mapping correctness |

## Edge Cases

A critical edge case is when both dates lie in the same month and even the same day. For example, in a calendar [5, 6], query (3, 2) to (3, 2) maps both start and end to prefix[1] + 3, giving identical values. The formula end - start + 1 correctly returns 1, which matches the requirement that a single-day stay is valid.

Another important case is crossing month boundaries at the exact edges. In [4, 7], going from (4, 1) to (1, 2) produces start = 4 and end = 5. The answer becomes 2, correctly counting the last day of month 1 and the first day of month 2. Any off-by-one error in prefix indexing would shift this by one and break boundary correctness.

Finally, when the query spans the entire year, such as (1, 1) to (a_n, n), both endpoints map cleanly to 1 and sum(a_i). The subtraction naturally yields the full year length without special casing, which confirms the robustness of the linearization approach.
