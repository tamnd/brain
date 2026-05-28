---
title: "CF 101B - Buses"
description: "We have bus stops placed on a line from 0 to n. Gerald starts at stop 0 and wants to reach stop n. Each bus is described by an interval [s, t]. Gerald may board that bus at any stop from s through t - 1, but once he rides it, he must stay on until stop t."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 101
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 79 (Div. 1 Only)"
rating: 1700
weight: 101
solve_time_s: 117
verified: true
draft: false
---

[CF 101B - Buses](https://codeforces.com/problemset/problem/101/B)

**Rating:** 1700  
**Tags:** binary search, data structures, dp  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have bus stops placed on a line from `0` to `n`. Gerald starts at stop `0` and wants to reach stop `n`.

Each bus is described by an interval `[s, t]`. Gerald may board that bus at any stop from `s` through `t - 1`, but once he rides it, he must stay on until stop `t`. He cannot move backward and he cannot walk between stops.

Two routes are considered different if there exists at least one segment between adjacent stops where Gerald rides a different bus. In practice, this means the exact sequence of buses matters.

The task is to count how many valid ways exist to reach stop `n`.

The constraints completely shape the solution. The number of stops `n` can be as large as `10^9`, so any algorithm that iterates over every stop is impossible. At the same time, the number of buses is only `10^5`, which strongly suggests that only stops appearing in the input are relevant.

A direct graph interpretation helps. Every bus creates transitions from every stop in `[s, t-1]` into stop `t`. If we define `dp[x]` as the number of ways to reach stop `x`, then every bus contributes:

$$dp[t] += dp[s] + dp[s+1] + \dots + dp[t-1]$$

The difficulty is computing these range sums efficiently.

Several edge cases are easy to mishandle.

Consider:

```
3 1
0 2
```

The correct answer is `0`. Gerald can reach stop `2`, but there is no way to continue to stop `3`. A careless implementation that assumes reaching the farthest bus endpoint is enough would incorrectly return `1`.

Another subtle case is multiple buses ending at the same stop:

```
2 2
0 2
1 2
```

The correct answer is `1`.

The second bus is useless because stop `1` itself is unreachable. A naive implementation that only counts buses ending at `2` might incorrectly produce `2`.

Overlapping buses also matter:

```
4 4
0 1
0 2
1 4
2 4
```

The correct answer is `2`.

Gerald can either take `0→1→4` or `0→2→4`. The buses overlap heavily, so counting transitions independently without respecting reachability causes overcounting.

The most dangerous mistake comes from trying to process stops directly. Since `n` may be `10^9`, even allocating an array of size `n+1` is impossible.

## Approaches

The brute-force idea follows the recurrence directly.

Define `dp[x]` as the number of ways to arrive at stop `x`. Initially, `dp[0] = 1`. For every bus `(s, t)`, we add the number of ways to reach every possible boarding stop:

$$dp[t] += \sum_{i=s}^{t-1} dp[i]$$

If we literally compute this sum for every bus, the complexity becomes quadratic in the worst case. With `10^5` buses, and each interval potentially spanning `10^5` relevant positions, the total work can approach `10^{10}` operations.

The bottleneck is obvious: repeatedly summing large ranges.

The key observation is that the recurrence only depends on prefix sums of `dp`.

If we maintain:

$$pref[i] = dp[0] + dp[1] + \dots + dp[i]$$

then:

$$dp[t] += pref[t-1] - pref[s-1]$$

Now each transition becomes constant time.

That alone is still not enough because stop numbers reach `10^9`. The second observation is that only bus endpoints matter. If no bus starts or ends at some stop, then nothing interesting happens there.

We compress coordinates by collecting all distinct stop values appearing in the buses, along with `0` and `n`. After sorting them, we work only on compressed indices.

The buses are then sorted by their ending stop. As we sweep from left to right, we maintain prefix sums over compressed positions. Every bus contributes a range sum into its destination.

This transforms the problem into dynamic programming with prefix sums and coordinate compression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(m) | Too slow |
| Optimal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all buses and collect every stop that appears in the input, along with `0` and `n`.

We cannot work on the original coordinate range because stops may be as large as `10^9`.
2. Sort and deduplicate the collected coordinates.

This creates the compressed coordinate system.
3. Map every original stop value to its compressed index.

After compression, all relevant stops lie in a dense range `[0, k-1]`.
4. Group buses by their destination stop.

We process stops from left to right, so when computing ways to reach some stop `t`, every earlier stop already has a finalized value.
5. Initialize `dp[start_index_of_0] = 1`.

Gerald starts at stop `0` in exactly one way.
6. Maintain a Fenwick tree storing prefix sums of `dp`.

The Fenwick tree supports:

- adding a value to a compressed stop
- querying the sum over a range of compressed stops
7. Process compressed stops in increasing order.

For every bus `(s, t)` ending at the current stop:

- query the total number of ways to reach any stop in `[s, t-1]`
- add that value into `dp[t]`

This exactly matches the recurrence relation.
8. After finishing all buses ending at a stop, insert `dp[stop]` into the Fenwick tree.

Future buses may use this stop as a boarding position.
9. Output `dp[n] mod 10^9+7`.

### Why it works

The invariant is:

`dp[x]` always equals the number of valid ways to reach stop `x` using only buses whose destinations are already processed.

When processing a bus `(s, t)`, Gerald may board at any reachable stop in `[s, t-1]`. The Fenwick tree stores exactly the sum of `dp` values for processed stops, so querying that range gives the total number of valid ways to use this bus.

Since stops are processed in increasing order, every path contributing to `dp[t]` is already finalized before `t` is computed. No future transition can create a path to an earlier stop because buses only move forward.

Thus every valid route is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        idx += 1
        while idx <= self.n:
            self.bit[idx] = (self.bit[idx] + val) % MOD
            idx += idx & -idx

    def sum(self, idx):
        idx += 1
        res = 0
        while idx > 0:
            res = (res + self.bit[idx]) % MOD
            idx -= idx & -idx
        return res

    def range_sum(self, left, right):
        if left > right:
            return 0
        return (self.sum(right) - self.sum(left - 1)) % MOD

def main():
    n, m = map(int, input().split())

    buses = []
    coords = {0, n}

    for _ in range(m):
        s, t = map(int, input().split())
        buses.append((s, t))
        coords.add(s)
        coords.add(t)

    coords = sorted(coords)
    comp = {x: i for i, x in enumerate(coords)}

    k = len(coords)

    ending = [[] for _ in range(k)]

    for s, t in buses:
        cs = comp[s]
        ct = comp[t]
        ending[ct].append(cs)

    dp = [0] * k

    start = comp[0]
    dp[start] = 1

    fw = Fenwick(k)
    fw.add(start, 1)

    for t_idx in range(k):
        if t_idx == start:
            continue

        ways = 0

        for s_idx in ending[t_idx]:
            ways += fw.range_sum(s_idx, t_idx - 1)
            ways %= MOD

        dp[t_idx] = ways
        fw.add(t_idx, ways)

    print(dp[comp[n]] % MOD)

if __name__ == "__main__":
    main()
```

The solution begins with coordinate compression. Since stop values may be enormous, we only keep stops that actually appear in the buses or as endpoints `0` and `n`.

The buses are grouped by destination index. This avoids repeatedly scanning all buses during the sweep.

The Fenwick tree stores prefix sums of reachable ways. Its `range_sum(l, r)` method computes:

$$dp[l] + dp[l+1] + \dots + dp[r]$$

in logarithmic time.

One subtle implementation detail is the processing order. We must first finish all contributions into `dp[t]` before inserting `dp[t]` into the Fenwick tree. Otherwise a bus ending at `t` could incorrectly use stop `t` itself as a boarding point.

Another easy mistake is handling empty ranges. If `s_idx > t_idx - 1`, then the bus contributes nothing. The helper method returns `0` in that case.

Modulo operations are applied after every update because the number of paths grows exponentially.

## Worked Examples

### Sample 1

Input:

```
2 2
0 1
1 2
```

Compressed coordinates:

```
[0, 1, 2]
```

| Current Stop | Incoming Buses | Queried Range | Added Ways | dp |
| --- | --- | --- | --- | --- |
| 0 | none | none | none | [1,0,0] |
| 1 | (0,1) | [0,0] | 1 | [1,1,0] |
| 2 | (1,2) | [1,1] | 1 | [1,1,1] |

Final answer: `1`.

This trace shows the fundamental recurrence. Each bus collects all reachable boarding positions before jumping to its endpoint.

### Example 2

Input:

```
4 4
0 1
0 2
1 4
2 4
```

Compressed coordinates:

```
[0,1,2,4]
```

| Current Stop | Incoming Buses | Queried Range | Added Ways | dp |
| --- | --- | --- | --- | --- |
| 0 | none | none | none | [1,0,0,0] |
| 1 | (0,1) | [0,0] | 1 | [1,1,0,0] |
| 2 | (0,2) | [0,1] | 2 | [1,1,2,0] |
| 4 | (1,4), (2,4) | [1,2], [2,2] | 3 + 2 | [1,1,2,5] |

Final answer: `5`.

The five routes are:

1. `0→1→4`
2. `0→2→4`
3. `0→1→2→4`
4. `0→2→4` using the second bus directly
5. `0→1→2→4` through different bus choices

This demonstrates why overlapping intervals naturally combine through prefix sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Coordinate compression, Fenwick updates, and range queries |
| Space | O(m) | Stored buses, compressed coordinates, Fenwick tree, and DP array |

With at most `10^5` buses, `O(m log m)` easily fits within the time limit. The memory usage also stays linear in the number of buses, far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            idx += 1
            while idx <= self.n:
                self.bit[idx] = (self.bit[idx] + val) % MOD
                idx += idx & -idx

        def sum(self, idx):
            idx += 1
            res = 0
            while idx > 0:
                res = (res + self.bit[idx]) % MOD
                idx -= idx & -idx
            return res

        def range_sum(self, l, r):
            if l > r:
                return 0
            return (self.sum(r) - self.sum(l - 1)) % MOD

    n, m = map(int, input().split())

    buses = []
    coords = {0, n}

    for _ in range(m):
        s, t = map(int, input().split())
        buses.append((s, t))
        coords.add(s)
        coords.add(t)

    coords = sorted(coords)
    comp = {x: i for i, x in enumerate(coords)}

    k = len(coords)

    ending = [[] for _ in range(k)]

    for s, t in buses:
        ending[comp[t]].append(comp[s])

    dp = [0] * k

    start = comp[0]
    dp[start] = 1

    fw = Fenwick(k)
    fw.add(start, 1)

    for t_idx in range(k):
        if t_idx == start:
            continue

        ways = 0

        for s_idx in ending[t_idx]:
            ways += fw.range_sum(s_idx, t_idx - 1)
            ways %= MOD

        dp[t_idx] = ways
        fw.add(t_idx, ways)

    return str(dp[comp[n]]) + "\n"

# provided sample
assert run(
"""2 2
0 1
1 2
"""
) == "1\n", "sample 1"

# unreachable destination
assert run(
"""3 1
0 2
"""
) == "0\n", "unreachable destination"

# direct bus only
assert run(
"""5 1
0 5
"""
) == "1\n", "single direct bus"

# overlapping intervals
assert run(
"""4 4
0 1
0 2
1 4
2 4
"""
) == "5\n", "overlapping buses"

# no buses
assert run(
"""1 0
"""
) == "0\n", "empty graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 / 0 2` | `0` | Destination unreachable |
| `5 1 / 0 5` | `1` | Single direct route |
| Overlapping intervals example | `5` | Multiple interacting transitions |
| `1 0` | `0` | No buses at all |

## Edge Cases

Consider the unreachable destination case:

```
3 1
0 2
```

Compressed coordinates become `[0,2,3]`.

Initially:

```
dp[0] = 1
```

Processing stop `2`:

- bus `(0,2)` queries range `[0,1]`
- only stop `0` contributes
- `dp[2] = 1`

Processing stop `3`:

- no buses end here
- `dp[3] = 0`

The algorithm correctly outputs `0` because no transition reaches the school.

Now consider overlapping buses:

```
2 2
0 2
1 2
```

Compressed coordinates are `[0,1,2]`.

When processing stop `2`:

- bus `(0,2)` contributes ways from `[0,1]`
- only stop `0` is reachable
- contribution = `1`
- bus `(1,2)` contributes ways from `[1,1]`
- stop `1` is unreachable
- contribution = `0`

Total:

```
dp[2] = 1
```

This confirms the algorithm never counts buses whose boarding range contains only unreachable stops.

Finally, consider sparse coordinates:

```
1000000000 2
0 5
5 1000000000
```

The algorithm compresses coordinates into:

```
[0,5,1000000000]
```

Only three states are stored, despite the enormous original coordinate range. This is exactly why coordinate compression is necessary.
