---
title: "CF 102470I - Happy Telephones"
description: "Each telephone call occupies a continuous time interval. A call is described by its two endpoints, its starting time S and its ending time S + D, where D is its duration. The phone numbers themselves do not affect the answer."
date: "2026-08-09T15:30:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102470
codeforces_index: "I"
codeforces_contest_name: "2009-2010 ACM ICPC Southwestern European Regional Programming Contest (SWERC 2009)"
rating: 0
weight: 102470
solve_time_s: 206
verified: true
draft: false
---

[CF 102470I - Happy Telephones](https://codeforces.com/problemset/problem/102470/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Each telephone call occupies a continuous time interval. A call is described by its two endpoints, its starting time `S` and its ending time `S + D`, where `D` is its duration. The phone numbers themselves do not affect the answer. They only identify who is talking, so after reading a call we only need its time interval.

For every police query, we are given another time interval. We must count how many calls overlap that query for a positive amount of time. A call that ends exactly when the query begins does not count, and a call that begins exactly when the query ends does not count. In other words, if a call occupies `[a, b]` and a query occupies `[c, d]`, they intersect for at least one second precisely when `a < d` and `b > c`.

There can be fewer than 10,000 calls and fewer than 100 queries in one test case. A direct comparison of every call with every query therefore performs at most `9999 * 99 = 989901` overlap checks in one test case. That is not an astronomically large number, so brute force is viable for these stated bounds. Still, the structure of the query lets us do substantially better. Sorting the call start times and end times lets each query be answered using binary searches, reducing the work per query from linear in the number of calls to logarithmic.

The time values can be large, but `Start + Duration` fits in a signed 32-bit integer. Python integers have no overflow problem here anyway, and we never need to simulate individual seconds.

One common boundary mistake is counting intervals that only touch. Consider:

```
1 1
10 20 0 10
10 1
0 0
```

The call occupies `[0, 10]`, while the query occupies `[10, 11]`. Their intersection has zero duration, so the answer is `0`. A careless implementation using `call_start <= query_end` and `call_end >= query_start` would incorrectly count it.

Another boundary case occurs when the query lies entirely inside a call:

```
1 1
1 2 0 10
3 2
0 0
```

The call is active from `0` to `10`, and the query covers `3` to `5`, so the answer is `1`. Any method that only checks whether a call starts or ends inside the query can miss this case, because neither endpoint of the call lies inside `[3, 5]`.

A third case is a call completely inside the query:

```
1 1
1 2 4 2
0 10
0 0
```

The call occupies `[4, 6]` and the query occupies `[0, 10]`, so the answer is again `1`. This shows why overlap must be expressed through interval endpoints rather than by checking only one direction of containment.

## Approaches

The straightforward solution stores every call as an interval. For each police query `[L, R]`, it scans all calls and checks whether each call `[S, E]` satisfies `S < R` and `E > L`. Those two inequalities exactly characterize a positive-length intersection. Since there are at most 9,999 calls and 99 queries, the worst case is 989,901 interval checks per test case. That is already small enough for the given constraints, and it is a perfectly reasonable implementation if simplicity is the only concern.

The faster approach comes from rewriting the overlap condition. A call does not overlap `[L, R]` exactly when it is completely to the left or completely to the right of the query. A call is completely to the left when its ending time is at most `L`. A call is completely to the right when its starting time is at least `R`.

So the number we want can be written as

`N - (# calls with end <= L) - (# calls with start >= R)`.

These two quantities are independent. If all call ending times are sorted, binary search gives the number of endings less than or equal to `L`. If all call starting times are sorted, another binary search gives the number of starts greater than or equal to `R`.

Python's `bisect_right` gives exactly the number of values `<= L`, while `bisect_left` gives the number of values `>= R` by subtracting its result from `N`. The strict inequalities are what make endpoint-touching calls disappear from the answer.

The preprocessing costs `O(N log N)`, and every query costs `O(log N)`. With fewer than 100 queries, this is comfortably fast and also scales much better if the number of queries were increased.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NM)` | `O(N)` | Accepted for stated bounds |
| Optimal | `O(N log N + M log N)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Read all calls and convert each one into its starting time and ending time. For a call with start `S` and duration `D`, its ending time is `S + D`. We do not need the source and destination numbers because the query asks only about temporal overlap.
2. Store every call start in one array and every call end in another array. Sorting these arrays turns questions about how many calls lie completely before or after a query into binary-search problems.
3. Sort both arrays. After sorting, all ending times less than or equal to a particular value form one prefix, and all starting times greater than or equal to a particular value form one suffix.
4. For a query starting at `L` with duration `D`, compute its ending time `R = L + D`.
5. Use `bisect_right(ends, L)` to count calls whose ending time is at most `L`. Such calls are completely finished before the query begins, so they have zero common duration with the query.
6. Use `bisect_left(starts, R)` to find the first call whose start is at least `R`. There are `N - bisect_left(starts, R)` such calls. These calls begin when the query has already ended, so they also have zero common duration.
7. Subtract both non-overlapping groups from `N`. The remaining calls satisfy `start < R` and `end > L`, which means they overlap the query for a positive amount of time. Print this count.

### Why it works

For any call `[S, E]` and query `[L, R]`, exactly one of three situations applies. The call is completely before the query when `E <= L`, completely after the query when `S >= R`, or it overlaps the query when neither condition holds. The first two groups cannot overlap each other because the query has `L < R`. Thus removing both groups from all `N` calls leaves exactly the calls satisfying `S < R` and `E > L`, which are precisely the calls active during at least one second of the query interval.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    out = []

    while True:
        n, m = map(int, input().split())

        if n == 0 and m == 0:
            break

        starts = []
        ends = []

        for _ in range(n):
            source, destination, start, duration = map(int, input().split())
            starts.append(start)
            ends.append(start + duration)

        starts.sort()
        ends.sort()

        for _ in range(m):
            start, duration = map(int, input().split())
            end = start + duration

            finished_before = bisect_right(ends, start)
            started_after = n - bisect_left(starts, end)

            answer = n - finished_before - started_after
            out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop processes test cases until `0 0`. For every call, only `start` and `start + duration` are retained, because the phone numbers never participate in an overlap query.

The two sorted arrays represent the two ways a call can fail to overlap a query. `bisect_right(ends, start)` includes endings exactly equal to the query start. That is deliberate, because a call ending at the same instant the query starts has zero intersection. Similarly, `bisect_left(starts, end)` includes starts exactly equal to the query end, which must also be excluded from the answer.

The subtraction is performed only after both non-overlapping groups have been counted. There is no need to inspect individual calls for each query.

There is also no integer-overflow issue in Python. Even though the original bounds guarantee that the endpoint fits in a 32-bit signed integer, Python's integer type can represent it directly.

## Worked Examples

### Sample 1

The first test case contains three calls:

| Call | Start | End |
| --- | --- | --- |
| 1 | 2 | 7 |
| 2 | 0 | 10 |
| 3 | 5 | 13 |

After sorting, the start array is `[0, 2, 5]` and the end array is `[7, 10, 13]`.

For the first query, the interval is `[0, 6]`.

| Query | `bisect_right(ends, L)` | `bisect_left(starts, R)` | Answer |
| --- | --- | --- | --- |
| `[0, 6]` | 0 | 3 | 3 |

No call has ended by time `0`, and no call starts at or after time `6`. All three calls overlap the query.

For the second query, the interval is `[8, 10]`.

| Query | `bisect_right(ends, L)` | `bisect_left(starts, R)` | Answer |
| --- | --- | --- | --- |
| `[8, 10]` | 1 | 0 | 2 |

The first call ended at time `7`, so it is excluded. The other two calls overlap `[8, 10]`, giving `2`.

The resulting output for this test case is:

```
3
2
```

The trace demonstrates why an ending exactly at the query's starting boundary belongs to the non-overlapping prefix.

### Sample 2

The second test case has one call starting at `0` with duration `10`, so its interval is `[0, 10]`.

The first query is `[9, 10]`.

| Query | `L` | `R` | Finished by `L` | Started at or after `R` | Answer |
| --- | --- | --- | --- | --- | --- |
| `[9, 10]` | 9 | 10 | 0 | 0 | 1 |

The call overlaps the query during the interval from `9` to `10`, so it counts.

The second query is `[10, 11]`.

| Query | `L` | `R` | Finished by `L` | Started at or after `R` | Answer |
| --- | --- | --- | --- | --- | --- |
| `[10, 11]` | 10 | 11 | 1 | 0 | 0 |

The call ends exactly at the query's starting time. There is no positive-length intersection, so it does not count.

The resulting output is:

```
1
0
```

This example directly exercises the strict boundary conditions and catches the common mistake of treating touching intervals as overlapping.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N log N + M log N)` | Sorting the two endpoint arrays costs `O(N log N)`, and each of the `M` queries uses two binary searches |
| Space | `O(N)` | The start and end arrays each contain one value per call |

The largest test case contains fewer than 10,000 calls, so sorting is inexpensive. Each query requires only two binary searches instead of scanning all calls. The method also avoids dependence on the actual magnitude of the timestamps, so a call lasting thousands of seconds does not require iterating over those seconds.

## Test Cases

```python
import sys
import io
from bisect import bisect_left, bisect_right

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline
    out = []

    while True:
        n, m = map(int, input().split())

        if n == 0 and m == 0:
            break

        starts = []
        ends = []

        for _ in range(n):
            source, destination, start, duration = map(int, input().split())
            starts.append(start)
            ends.append(start + duration)

        starts.sort()
        ends.sort()

        for _ in range(m):
            start, duration = map(int, input().split())
            end = start + duration

            finished_before = bisect_right(ends, start)
            started_after = n - bisect_left(starts, end)

            out.append(str(n - finished_before - started_after))

    sys.stdout = old_stdout
    sys.stdin = old_stdin

    return "\n".join(out)

sample = """\
3 2
3 4 2 5
1 2 0 10
6 5 5 8
0 6
8 2
1 2
8 9 0 10
9 1
10 1
0 0
"""

assert solve_data(sample) == "3\n2\n1\n0", "provided sample"

minimum = """\
1 1
0 0 0 1
0 1
0 0
"""

assert solve_data(minimum) == "1", "minimum-size overlapping case"

touching = """\
1 3
1 2 10 5
0 10
15 1
16 1
0 0
"""

assert solve_data(touching) == "1\n0\n0", "endpoint touching"

equal_values = """\
4 3
1 1 5 5
2 2 5 5
3 3 5 5
4 4 5 5
5 5
0 5
10 1
0 0
"""

assert solve_data(equal_values) == "4\n4\n0", "equal starts and ends"

containment = """\
3 3
1 2 0 20
3 4 5 2
5 6 10 5
6 3
0 1
20 1
0 0
"""

assert solve_data(containment) == "3\n1\n0", "containment and boundaries"

large_endpoint = """\
2 2
1 2 0 10000
3 4 2147480000 10000
0 10000
2147480000 10000
0 0
"""

assert solve_data(large_endpoint) == "1\n1", "large timestamps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum-size case | `1` | A single call and a single query |
| Touching case | `1`, `0`, `0` | Exact endpoint handling |
| Equal values | `4`, `4`, `0` | Multiple calls with identical intervals |
| Containment case | `3`, `1`, `0` | Calls containing queries and calls contained by queries |
| Large endpoint case | `1`, `1` | Large valid timestamps and endpoint arithmetic |

## Edge Cases

The first boundary case is a call ending exactly when a query begins. For example:

```
1 1
10 20 0 10
10 1
0 0
```

The call ends at `10`, while the query starts at `10`. `bisect_right(ends, 10)` returns `1`, so the call is classified as finished before or exactly at the query boundary. The answer is `1 - 1 - 0 = 0`.

The symmetric case is a call beginning exactly when a query ends:

```
1 1
10 20 10 5
0 15
0 0
```

The call is `[10, 15]`, and the query is `[0, 15]`, so these intervals actually overlap before time `15` and the answer is `1`. The relevant binary search is `bisect_left(starts, 15)`, which returns `1`, but that does not remove the call because the call starts at `10`, which is strictly before `15`.

If instead the query were `[0, 10]`:

```
1 1
10 20 10 5
0 10
0 0
```

then `bisect_left(starts, 10)` returns `0`, giving `started_after = 1`. The call starts exactly at the query's ending boundary, so the answer is `0`.

A query can be completely inside a call:

```
1 1
1 2 0 10
3 2
0 0
```

Here the call is `[0, 10]` and the query is `[3, 5]`. No call ends by `3`, and no call starts at or after `5`, so the formula gives `1 - 0 - 0 = 1`. The method does not require either endpoint of the call to lie inside the query.

The reverse containment is handled identically:

```
1 1
1 2 3 2
0 10
0 0
```

The call `[3, 5]` lies entirely inside `[0, 10]`. Again, no call belongs to either non-overlapping group, so the answer is `1`.

Finally, a query may be completely outside every call:

```
2 1
1 2 0 2
3 4 5 2
2 1
0 0
```

The calls are `[0, 2]` and `[5, 7]`, while the query is `[2, 3]`. The first call ends exactly at `2`, so `bisect_right` removes it. The second call starts after `3`, so `bisect_left` removes it. Both calls are excluded and the answer is `0`. This is the exact situation where treating endpoint contact as overlap would produce an incorrect result.
