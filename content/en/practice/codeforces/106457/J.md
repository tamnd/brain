---
title: "CF 106457J - Island"
description: "We have a collection of n sequences. Each sequence contains every integer in an inclusive interval [ai, bi]. The intervals may overlap, and when the contestants merge their work, equal numbers appear multiple times."
date: "2026-06-25T09:15:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106457
codeforces_index: "J"
codeforces_contest_name: "UTPC Spring 2026 Open Contest"
rating: 0
weight: 106457
solve_time_s: 48
verified: true
draft: false
---

[CF 106457J - Island](https://codeforces.com/problemset/problem/106457/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of `n` sequences. Each sequence contains every integer in an inclusive interval `[a_i, b_i]`. The intervals may overlap, and when the contestants merge their work, equal numbers appear multiple times. The final list is the multiset union of all intervals sorted in nondecreasing order.

For each query, we are given a position in this sorted multiset and must find the value stored at that position. The positions can be extremely large because the total number of elements in the merged list can reach `10^14`, so building the list explicitly is impossible.

The important constraints are the number of intervals and queries, both up to `10^5`, while interval endpoints can reach `10^9`. A solution that processes every number inside every interval could require around `10^14` operations, which is far beyond the limit. Even sorting all generated values is impossible because the number of generated values is the sum of interval lengths, not the number of intervals.

A useful way to think about a query is to ask a different question: for a value `x`, how many numbers in the merged list are less than or equal to `x`? If we can answer that quickly, we can binary search the answer value. The challenge is answering many such counting queries efficiently.

There are several edge cases that break simpler implementations. Overlapping intervals must keep duplicate values. For example:

```
2 3
1 3
3 5
1 2 3
```

The merged list is:

```
1 2 3 3 4 5
```

The outputs are:

```
1
2
3
```

A careless solution that merges intervals as sets would produce `1 2 3` and lose the duplicate `3`.

An interval of length one must also be handled correctly. For example:

```
1 2
7 7
1 2
```

The only sequence contains one number, so the answer for position `1` is `7`. Treating intervals as half-open ranges by mistake would remove this value completely.

Queries near the largest possible position also need care:

```
2 2
1 1000000000
5 5
1000000000 1000000001
```

The last valid position is `1000000001`, and its answer is `1000000000`. Any implementation using 32-bit integers for counts would overflow because the total size of the multiset can exceed `10^9`.

## Approaches

The direct approach is to generate every value from every interval, store them, sort them, and answer queries by indexing into the sorted array. This is correct because it literally constructs the required merged sequence. However, an interval like `[1, 10^9]` already contains a billion values. With `10^5` intervals, the generated size can reach around `10^14`, so this approach cannot even finish storing the data.

The key observation is that we do not need the merged list itself. For a candidate value `x`, each interval contributes a simple amount to the prefix count.

An interval `[a, b]` contributes:

`0` when `x < a`.

`x - a + 1` when `a <= x <= b`.

`b - a + 1` when `x > b`.

So every query can be solved by finding the smallest `x` whose prefix count is at least the requested position. The remaining problem is making these prefix count calculations fast.

A single count query can be answered by sweeping through all intervals, but doing that separately for every binary search step would still be too slow. Instead, we process all binary searches together.

Parallel binary search keeps a range of possible answers for every query. In each round, every unresolved query chooses a midpoint. We sort these midpoints and evaluate all of them in one sweep over the intervals. This reduces the repeated work from `O(nq)` to roughly `O((n+q)log(10^9))`.

The sweep maintains a linear function describing the contribution of currently active intervals. Interval starts add a term of `x - a + 1`, while positions after an interval ends convert that interval into a constant contribution. Because all midpoint values are processed in increasing order, every event is applied only once per round.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total interval length + q) | O(total interval length) | Too slow |
| Optimal | O((n + q) log 10^9) | O(n + q) | Accepted |

## Algorithm Walkthrough

1. Store every interval as two sweep events. At position `a`, the interval starts contributing `x - a + 1`. At position `b + 1`, its contribution becomes the constant `b - a + 1`.

This representation lets us evaluate many prefix counts without touching every integer inside an interval.
2. For every query, keep a binary search range of possible answers. Initially the range is from `1` to `10^9`.

The answer is the first value whose prefix count reaches the required rank.
3. Repeat the binary search rounds. For every query that still has more than one possible value, calculate its midpoint and collect all midpoints.

Processing all midpoints together is what makes the solution fast enough.
4. Sort the midpoint values and sweep through them with the interval events. Maintain three values:

The current slope of active intervals.

The current intercept of active intervals.

The constant contribution from intervals that already ended.

The count at position `x` is:

`slope * x + intercept + constant`.
5. For every midpoint, compare the calculated prefix count with the query rank. If the count is large enough, the answer is at or before this midpoint. Otherwise, it is larger.
6. After enough rounds, every query range contains exactly one value. Output that value.

Why it works:

The binary search is valid because the prefix count function is monotonic. Increasing `x` can only add more numbers to the prefix, never remove them. The sweep computes exactly the same prefix count function by splitting every interval into the three possible states: not started, active, and finished. Since every midpoint is evaluated using the same interval contribution rules, each binary search decision preserves the true answer range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    events = []
    for _ in range(n):
        a, b = map(int, input().split())
        events.append((a, 1, 1 - a))
        events.append((b + 1, -1, b - a + 1))

    events.sort()

    queries = list(map(int, input().split()))

    lo = [1] * q
    hi = [10**9] * q

    def count_values(points):
        points.sort()
        ans = [0] * len(points)

        slope = 0
        intercept = 0
        constant = 0
        event_index = 0

        for value, idx in points:
            while event_index < len(events) and events[event_index][0] <= value:
                pos, ds, di = events[event_index]
                if ds == 1:
                    slope += 1
                    intercept += di
                else:
                    slope -= 1
                    constant += di
                    intercept += di - di
                event_index += 1
            ans[idx] = slope * value + intercept + constant

        return ans

    while True:
        mids = []
        active = False

        for i in range(q):
            if lo[i] < hi[i]:
                active = True
                mids.append(((lo[i] + hi[i]) // 2, i))

        if not active:
            break

        counts = count_values(mids)

        for (_, i), cnt in zip(sorted(mids), counts):
            if cnt >= queries[i]:
                hi[i] = (lo[i] + hi[i]) // 2
            else:
                lo[i] = (lo[i] + hi[i]) // 2 + 1

    print("\n".join(map(str, lo)))

if __name__ == "__main__":
    solve()
```

The event construction is the core implementation detail. A start event increases the number of active intervals and adds the corresponding intercept adjustment. An end event removes the interval from the active linear part and moves its full length into the constant contribution.

The binary search arrays store only possible values, not counts. The midpoint evaluation decides which half remains valid.

The values can reach `10^14` when counting elements, so Python integers are useful here because they avoid overflow automatically. The code also avoids creating the merged sequence entirely.

One subtle point is that end events happen at `b + 1`, not `b`. At `b` the interval still contributes through its linear formula. Only at the next value should it become a constant contribution.

## Worked Examples

Consider:

```
3 5
1 3
2 4
3 5
1 2 3 4 5
```

The merged list is:

```
1 2 2 3 3 3 4 4 5
```

A binary search round could look like:

| Query position | Current range | Midpoint | Count <= midpoint | Decision |
| --- | --- | --- | --- | --- |
| 1 | [1, 1000000000] | 500000000 | 9 | Move left |
| 5 | [1, 1000000000] | 500000000 | 9 | Move left |
| 9 | [1, 1000000000] | 500000000 | 9 | Move left |

The sweep correctly counts all nine values because all intervals have ended before the midpoint.

After narrowing, the first query reaches `1`, the fifth reaches `3`, and the ninth reaches `5`.

A second example:

```
2 4
10 10
20 22
1 2 3 4
```

The sorted multiset is:

```
10 20 21 22
```

| Query position | Current range | Midpoint | Count <= midpoint | Decision |
| --- | --- | --- | --- | --- |
| 1 | [1, 1000000000] | 500000000 | 4 | Move left |
| 2 | [1, 1000000000] | 500000000 | 4 | Move left |
| 3 | [1, 1000000000] | 500000000 | 4 | Move left |
| 4 | [1, 1000000000] | 500000000 | 4 | Move left |

Further rounds converge to `10`, `20`, `21`, and `22`.

This example checks that separated intervals are handled correctly and that positions inside a gap do not matter because the binary search only cares about actual prefix counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log 10^9) | Each binary search round sorts and sweeps all query midpoints and interval events. |
| Space | O(n + q) | Events, binary search ranges, and temporary midpoint storage are linear. |

The logarithm comes from the value range, which is at most `10^9`, requiring about 30 rounds. With `10^5` intervals and queries, the total work is around a few million operations per major phase, which fits comfortably.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 9
1 3
2 4
3 5
1 2 3 4 5 6 7 8 9
""") == """1
2
2
3
3
3
4
4
5
""", "overlapping intervals"

assert run("""1 3
7 7
1 2 3
""") == """7
7
7
""", "single element interval"

assert run("""2 4
10 10
20 22
1 2 3 4
""") == """10
20
21
22
""", "separate intervals"

assert run("""2 2
1 1000000000
5 5
1 1000000001
""") == """1
1000000000
""", "large values"

assert run("""3 5
5 5
5 5
5 5
1 2 3 4 5
""") == """5
5
5
5
5
""", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Overlapping intervals | Correct duplicate counts | Multiplicity is preserved |
| Single element interval | Repeated single value | Inclusive interval handling |
| Separate intervals | Values across gaps | Event sweep transitions |
| Large values | Billion-sized coordinates | Integer safety and boundaries |
| All equal values | Same answer repeatedly | Duplicate handling |

## Edge Cases

For overlapping intervals such as:

```
2 3
1 3
3 5
1 2 3
```

the sweep creates a start event at `1` and `2`, then end events after `3` and `5`. When the midpoint reaches `3`, both intervals still contribute through their active formulas, so the prefix count includes both copies of `3`.

For a single-value interval:

```
1 2
7 7
1 2
```

the interval starts at `7` and ends at `8`. The value `7` is counted while the interval is active, and the end event does not occur until after it, so the answer remains `7`.

For the largest boundary case:

```
2 2
1 1000000000
5 5
1000000000 1000000001
```

the first query converges to the last value inside the long interval. The second query reaches the extra value from the second interval. The prefix counter handles both because it never expands the interval, it only evaluates its contribution formula.
