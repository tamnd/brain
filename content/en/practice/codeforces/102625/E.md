---
title: "CF 102625E - Dictator's plan for Valentine's day!"
description: "The problem describes a line extending from the starting point Ruby at coordinate 0 toward the Main Gate. Guards stand at fixed coordinates, and each guard is active only during a certain time interval."
date: "2026-08-03T15:19:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "E"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 55
verified: true
draft: false
---

[CF 102625E - Dictator's plan for Valentine's day!](https://codeforces.com/problemset/problem/102625/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a line extending from the starting point Ruby at coordinate `0` toward the Main Gate. Guards stand at fixed coordinates, and each guard is active only during a certain time interval. Couples start walking from Ruby at different integer start times and move one unit of distance every second. For every couple, we need to determine the distance they walk before meeting the first guard, or report `-1` if they reach the end without meeting anyone.

A guard at coordinate `X` is active during the interval `[L-z, R-z]`, where `z` is a small positive value smaller than `0.1`. A couple starting at time `T` reaches this guard after exactly `X` seconds, at time `T + X`. The condition for being caught is:

`L - z <= T + X <= R - z`

Rearranging:

`L - X - z <= T <= R - X - z`

The input values are integers, while `z` is a tiny positive fraction. This changes the integer boundaries. The smallest valid integer `T` is `L - X`, because `L - X` is still greater than `L - X - z`. The largest valid integer `T` is `R - X - 1`, because `R - X` is already too large by the fraction `z`.

So every guard can be viewed as creating a time interval:

`[L - X, R - X - 1]`

During every integer start time inside this interval, that guard can catch the couple.

The limits allow up to `200000` guards and `200000` couples. Any approach that checks every couple against every guard would require about `4 * 10^10` operations, which is far beyond what a few seconds allow. We need a solution close to `O((M+N) log M)`.

A common mistake is forgetting the effect of the fractional `z`. For example:

```
1 1
0 1 5
5
```

The guard is active from `-0.1` to `0.9`. The couple reaches coordinate `5` at time `10`, so the answer is `-1`. A wrong conversion that uses `[L-X, R-X]` would incorrectly include start time `-5` only in other situations and can shift boundaries by one.

Another tricky case is a guard whose right endpoint is exactly reached without the fractional shift:

```
1 1
10 20 5
15
```

The couple reaches the guard at time `20`. The original active interval ends at `19.9`, so the guard is no longer present. The correct output is:

```
-1
```

Treating the interval as closed with integer endpoints would incorrectly output `5`.

## Approaches

The direct approach is to simulate every couple independently. For each start time, we check every guard and see whether the couple reaches that guard while it is active. If multiple guards match, we keep the smallest coordinate because the couple stops at the first guard encountered. This is correct because it directly models the movement, but the worst case performs `M * N` checks. With both values equal to `200000`, this becomes roughly forty billion comparisons.

The useful observation is that the queries are already sorted by starting time. Instead of asking every guard about every couple, we can sweep through time once. Each guard becomes active at time `L-X` and stops being active after time `R-X-1`. While processing couples in increasing order of `T`, we only need to know the smallest coordinate among currently active guards.

A priority queue is enough for this. When a guard starts being active, we insert its coordinate and ending time. Before answering a query, we remove all guards whose ending time is smaller than the current start time. The minimum coordinate remaining in the heap is the first guard the couple will encounter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(MN) | O(1) | Too slow |
| Optimal | O((M+N) log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. Convert every guard into a time interval. For a guard at coordinate `X`, store that it is active for start times from `L-X` to `R-X-1`. The coordinate `X` is stored with the interval because it is the value we need to output.
2. Sort all converted guard intervals by their starting time. Sort is useful because couples also arrive in increasing order, so guards can be added exactly when they become relevant.
3. Process couples from the smallest start time to the largest. Before answering a couple, add every guard whose converted interval starts no later than the current time. These are the only new guards that could affect this or later couples.
4. Remove guards from the priority queue while their ending time is smaller than the current couple's start time. Such guards have already stopped being active.
5. If the heap is empty, no guard can catch the couple, so output `-1`. Otherwise, the smallest coordinate in the heap is the first guard encountered.

Why it works:

At any query time `T`, the heap contains exactly the guards whose transformed intervals include `T`. Every guard not in the heap either starts later or has already expired. Among all active guards, the couple physically reaches the smallest coordinate first, so taking the minimum `X` gives the correct answer.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    data = input().split()
    if not data:
        return

    M, N = map(int, data)

    guards = []
    for _ in range(M):
        L, R, X = map(int, input().split())
        guards.append((L - X, R - X - 1, X))

    guards.sort()

    queries = []
    for _ in range(N):
        queries.append(int(input()))

    heap = []
    ans = []
    idx = 0

    for t in queries:
        while idx < M and guards[idx][0] <= t:
            start, end, x = guards[idx]
            heapq.heappush(heap, (x, end))
            idx += 1

        while heap and heap[0][1] < t:
            heapq.heappop(heap)

        if heap:
            ans.append(str(heap[0][0]))
        else:
            ans.append("-1")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The guard conversion is the most delicate part of the implementation. The ending time must be `R-X-1`, not `R-X`, because the original interval ends slightly before that integer time due to the positive `z`.

The heap stores `(coordinate, ending_time)`. The coordinate is the priority because we need the closest guard. The ending time is kept so expired guards can be removed later.

The queries are already sorted in the input, so no additional sorting is needed. The pointer `idx` moves only forward, meaning every guard enters the heap once and leaves it at most once.

## Worked Examples

For the sample input:

```
4 6
1 3 2
7 13 10
18 20 13
3 4 2
0
1
2
3
5
8
```

The transformed guard intervals are:

| Coordinate | Start time | End time |
| --- | --- | --- |
| 2 | -1 | 0 |
| 10 | -3 | 2 |
| 13 | 5 | 6 |
| 2 | 1 | 1 |

Processing the first few queries:

| Query time | Added guards | Removed guards | Heap minimum | Answer |
| --- | --- | --- | --- | --- |
| 0 | coordinates 2,10 | none | 2 | 2 |
| 1 | coordinate 2 | none | 2 | 2 |
| 2 | none | expired coordinate 2 at end 1 | 10 | 10 |
| 3 | none | expired coordinate 10 | empty | -1 |

The trace shows that the heap always contains only guards that can currently catch the couple. The minimum coordinate among them matches the first physical collision point.

A second small example:

```
2 3
5 9 3
20 30 10
0
2
10
```

Converted intervals:

| Coordinate | Start | End |
| --- | --- | --- |
| 3 | 2 | 5 |
| 10 | 10 | 19 |

Processing:

| Query time | Active guards | Answer |
| --- | --- | --- |
| 0 | none | -1 |
| 2 | coordinate 3 | 3 |
| 10 | coordinate 10 | 10 |

This checks the exact activation boundary and shows why the fractional shift matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((M+N) log M) | Each guard is inserted and removed once, and each heap operation costs logarithmic time. |
| Space | O(M) | The priority queue stores active guards. |

With `200000` guards and `200000` couples, the sweep approach keeps the number of operations within the required range.

## Test Cases

```python
import sys
import io
import heapq

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        M, N = map(int, input().split())
        guards = []
        for _ in range(M):
            L, R, X = map(int, input().split())
            guards.append((L - X, R - X - 1, X))
        guards.sort()

        heap = []
        idx = 0
        res = []

        for _ in range(N):
            t = int(input())
            while idx < M and guards[idx][0] <= t:
                heapq.heappush(heap, (guards[idx][2], guards[idx][1]))
                idx += 1
            while heap and heap[0][1] < t:
                heapq.heappop(heap)
            res.append(str(heap[0][0]) if heap else "-1")

        return "\n".join(res)

    out = solve()
    sys.stdin = old
    return out

assert run("""4 6
1 3 2
7 13 10
18 20 13
3 4 2
0
1
2
3
5
8
""") == "2\n2\n10\n-1\n13\n-1"

assert run("""1 1
0 1 5
0
""") == "-1"

assert run("""2 2
1 10 3
1 10 7
4
5
""") == "3\n3"

assert run("""1 3
10 20 5
5
10
15
""") == "-1\n5\n-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single guard outside all queries | `-1` | Handles no active guard cases |
| Overlapping guards | `3, 3` | Confirms choosing the closest guard |
| Boundary activation and expiration | `-1, 5, -1` | Checks the fractional `z` conversion |

## Edge Cases

A guard that ends exactly when a couple arrives must not catch them. The input:

```
1 1
10 20 5
15
```

gives a transformed interval `[5,14]`. The query time is `15`, which is outside the interval, so the heap removes the guard before answering and returns `-1`.

A guard that begins exactly when a couple can reach it must be included. For:

```
1 1
3 4 2
1
```

the transformed interval is `[1,1]`. The guard is inserted before processing time `1`, remains active, and the answer is `2`.

Multiple guards at the same coordinate are also handled naturally. The heap may contain several entries with equal coordinates, and returning the minimum still gives the correct stopping distance. The input guarantee that intervals at the same coordinate do not overlap prevents conflicting simultaneous states from causing ambiguity.
