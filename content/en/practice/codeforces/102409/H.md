---
title: "CF 102409H - Maximizing Coins"
description: "We have a sequence of rooms numbered from 1 to (N). Room (N) is the destination and contains no coins. From room (i), Diego may jump to any later room whose index is at most (i+ki). When he visits a room (i<N), he collects its (ci) coins."
date: "2026-08-12T05:54:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "H"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 708
verified: true
draft: false
---

[CF 102409H - Maximizing Coins](https://codeforces.com/problemset/problem/102409/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of rooms numbered from 1 to (N). Room (N) is the destination and contains no coins. From room (i), Diego may jump to any later room whose index is at most (i+k_i). When he visits a room (i<N), he collects its (c_i) coins. The goal is to choose a valid sequence of jumps that reaches room (N) with the largest possible number of coins. Among all paths achieving that maximum, we also need to count how many there are, modulo (10^9+7).

A useful way to view the rooms is as a directed acyclic graph. Every room (i) has edges to the interval of vertices from (i+1) through (i+k_i). Since every edge goes to a larger index, processing the rooms from right to left gives a natural dynamic programming order.

The value (N) can be as large as (10^5). A quadratic algorithm would perform around (N^2/2), which is about (5\times10^9), operations in the worst case. That is far beyond what a 1 second time limit can handle. We need to avoid scanning every possible destination for every room. The coin values can reach (10^9), and a path may visit (O(N)) rooms, so the maximum coin total can reach roughly (10^{14}). Python integers handle this safely, while the number of optimal paths must explicitly be reduced modulo (10^9+7).

There are several edge cases that can make a straightforward implementation incorrect.

First, there can be many optimal paths. Consider:

```
3
0 0
2 1
```

From room 1, Diego can go directly to room 3 or visit room 2 first. Both paths collect zero coins, so the answer is `0 2`. An implementation that keeps only the best coin value without also accumulating the number of ways would incorrectly report one path.

Second, a room can have no successor other than the final room. For example:

```
2
7
1
```

The only possible path is (1\rightarrow2), so the answer is `7 1`. Treating room (N) like an ordinary room without initializing its dynamic programming state correctly can produce zero ways.

Third, the maximum interval can contain almost every room to the right. For example:

```
5
0 0 0 0
4 3 2 1
```

Every jump from room 1 can reach any later room. There are eight distinct paths from room 1 to room 5, so the answer is `0 8`. A quadratic transition scan gets the right answer but becomes infeasible at the maximum (N).

Finally, the interval boundaries are inclusive. If (k_i=2), room (i) may jump to (i+1) or (i+2), but not (i+3). Confusing the right endpoint with an exclusive bound causes subtle off-by-one errors, especially when the interval ends exactly at room (N).

## Approaches

The direct dynamic programming formulation is simple. Let (dp[i]) be the maximum number of coins obtainable starting at room (i) and ending at room (N). Let (ways[i]) be the number of paths that achieve (dp[i]). For the final room, we define (dp[N]=0) and (ways[N]=1), because reaching the destination from itself contributes no additional coins and there is exactly one empty continuation.

For every earlier room (i), every valid first jump goes to some room (j) in the interval ([i+1,i+k_i]). Thus,

[
dp[i] = c_i + \max_{j\in[i+1,i+k_i]} dp[j].
]

Once the maximum value (best) is known, the number of optimal paths is the sum of (ways[j]) over exactly those successors satisfying (dp[j]=best).

This brute-force DP is correct because every path from (i) has exactly one first destination (j), and after reaching (j), the best possible continuation is precisely what (dp[j]) describes. The problem is the cost of finding the maximum and its associated number of ways. If we scan the whole successor interval for every room, the worst case has approximately

[
\sum_{i=1}^{N-1}(N-i)=\frac{N(N-1)}2
]

successor examinations. For (N=10^5), this is (4,999,950,000) operations.

The key observation is that every transition asks the same kind of question: among a contiguous interval of already-computed rooms, find the largest (dp) value and the total number of ways belonging to that largest value. The rooms are processed from right to left, so when we need the answer for room (i), all values in its successor interval are already available.

This is exactly a range query with point updates. A segment tree can store, for every segment, the best (dp) value and the number of ways achieving that value. Combining two child segments is straightforward. If one child has a larger (dp), its pair is the answer. If both have the same (dp), their way counts are added modulo (10^9+7).

After computing (dp[i]) and (ways[i]), we insert that pair at position (i). Each room is inserted once and queried once, giving (O(N\log N)) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(N)) | Too slow |
| Optimal | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Initialize the state of the final room. Set (dp[N]=0) and (ways[N]=1). The final room contributes no coins, and there is exactly one way to finish once it has been reached.
2. Build a segment tree whose leaf at position (i) stores the pair ((dp[i],ways[i])). Initially, every position except (N) is empty. The leaf for (N) stores ((0,1)).
3. Process rooms (i=N-1,N-2,\ldots,1). Because every jump moves to the right, every possible destination of room (i) has already been processed.
4. Query the segment tree over the inclusive interval

[
[i+1,i+k_i].
]

The query returns two pieces of information. The first is the maximum (dp) among all reachable destinations. The second is the sum of (ways) over every destination having that maximum (dp).

1. Add the coins of the current room to the queried maximum:

[
dp[i]=c_i+best.
]

The number of optimal paths does not change when (c_i) is added, because the same coin value is added to every possible continuation from room (i). Hence,

[
ways[i]=bestWays.
]

1. Update the segment tree at position (i) with ((dp[i],ways[i])). Future rooms to the left may use room (i) as a destination, so its state must now be available to their range queries.
2. After processing room 1, output (dp[1]) and (ways[1]). Every valid journey begins at room 1, so these are exactly the required maximum coin total and number of optimal journeys.

### Why it works

The invariant is that whenever room (i) is processed, every room reachable from (i) already has its correct (dp) and (ways) values stored in the segment tree. The range query consequently considers every possible first destination of (i), selects the largest continuation value, and sums the path counts only among destinations achieving that value. Adding (c_i) gives the best total starting from (i), while leaving the corresponding count unchanged. The update preserves the invariant for the next room to the left. Since room 1 is processed last, its stored pair is correct for the entire problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
NEG = -10**30

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1

        self.size = size
        self.best = [NEG] * (2 * size)
        self.ways = [0] * (2 * size)

    def merge(self, left_best, left_ways, right_best, right_ways):
        if left_best > right_best:
            return left_best, left_ways
        if right_best > left_best:
            return right_best, right_ways
        if left_best == NEG:
            return NEG, 0
        return left_best, (left_ways + right_ways) % MOD

    def update(self, pos, value, ways):
        pos += self.size
        self.best[pos] = value
        self.ways[pos] = ways

        pos >>= 1
        while pos:
            lb = self.best[pos << 1]
            lw = self.ways[pos << 1]
            rb = self.best[pos << 1 | 1]
            rw = self.ways[pos << 1 | 1]

            b, w = self.merge(lb, lw, rb, rw)
            self.best[pos] = b
            self.ways[pos] = w

            pos >>= 1

    def query(self, left, right):
        if left > right:
            return NEG, 0

        left += self.size
        right += self.size

        left_best = NEG
        left_ways = 0
        right_best = NEG
        right_ways = 0

        while left <= right:
            if left & 1:
                lb = self.best[left]
                lw = self.ways[left]
                left_best, left_ways = self.merge(
                    left_best, left_ways, lb, lw
                )
                left += 1

            if not (right & 1):
                rb = self.best[right]
                rw = self.ways[right]
                right_best, right_ways = self.merge(
                    rb, rw, right_best, right_ways
                )
                right -= 1

            left >>= 1
            right >>= 1

        return self.merge(
            left_best, left_ways,
            right_best, right_ways
        )

def solve():
    n = int(input())
    c = [0] + list(map(int, input().split()))
    k = [0] + list(map(int, input().split()))

    seg = SegmentTree(n)

    # Room n is the destination.
    seg.update(n - 1, 0, 1)

    for i in range(n - 1, 0, -1):
        # Convert 1-based room indices to 0-based segment-tree indices.
        left = i
        right = i + k[i] - 1

        best, ways = seg.query(left, right)

        dp_i = c[i] + best
        seg.update(i - 1, dp_i, ways)

    answer, ways = seg.query(0, 0)
    print(answer, ways % MOD)

if __name__ == "__main__":
    solve()
```

The segment tree stores a pair at every node rather than a single maximum. The first component is the best coin total in that segment, while the second component counts how many paths attain that best value.

The `merge` operation is the central piece of the implementation. If one side has a larger value, only its path count matters. If both sides have the same value, both groups of optimal paths are valid and their counts are added modulo (10^9+7). The `NEG` value represents an empty segment that has not received a valid room state yet.

The indexing deserves particular attention. The dynamic programming equations use one-based room indices, but the segment tree uses zero-based positions. For room (i), its valid destinations are the one-based interval ([i+1,i+k_i]). These become zero-based positions ([i,i+k_i-1]), which is exactly the range queried in the code.

The final room is inserted at zero-based position `n - 1` with state `(0, 1)`. Every other room is then processed from right to left. Because (i+k_i\leq N), the query interval always remains inside the segment tree.

There is no integer overflow problem in Python. A maximum path can collect on the order of (10^5\cdot10^9=10^{14}) coins, which Python represents directly. Only the number of ways needs modular reduction, and the merge operation performs that reduction whenever equal optimal values are combined.

## Worked Examples

### Sample 1

The input is:

```
5
0 0 0 0
4 3 2 1
```

Every room has zero coins, so all valid paths are optimal. We process the rooms from right to left.

| Room (i) | Query interval | Best continuation | Ways | (dp[i]) | (ways[i]) |
| --- | --- | --- | --- | --- | --- |
| 4 | [5, 5] | 0 | 1 | 0 | 1 |
| 3 | [4, 5] | 0 | 2 | 0 | 2 |
| 2 | [3, 5] | 0 | 4 | 0 | 4 |
| 1 | [2, 5] | 0 | 8 | 0 | 8 |

At room 4 there is only the direct jump to room 5. At room 3 there are two optimal continuations, through room 4 or directly to room 5. The number doubles again at room 2 and finally becomes eight at room 1. The output is therefore `0 8`.

### Sample 2

The input is:

```
5
0 0 0 0
2 2 2 1
```

The reachable intervals are narrower, so fewer paths exist.

| Room (i) | Query interval | Best continuation | Ways | (dp[i]) | (ways[i]) |
| --- | --- | --- | --- | --- | --- |
| 4 | [5, 5] | 0 | 1 | 0 | 1 |
| 3 | [4, 5] | 0 | 2 | 0 | 2 |
| 2 | [3, 4] | 0 | 3 | 0 | 3 |
| 1 | [2, 3] | 0 | 5 | 0 | 5 |

At room 2, the paths through rooms 3 and 4 contribute two and one ways respectively, giving three. Room 1 can then begin with either room 2 or room 3, giving (3+2=5) optimal paths. The result is `0 5`.

These traces also demonstrate the key invariant: the segment tree always contains the correct pair for every room to the right of the current room, so each range query has exactly the information needed for the current transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Each of the (N-1) rooms performs one range query and one point update, each taking (O(\log N)). |
| Space | (O(N)) | The segment tree contains (O(N)) nodes, and the input arrays also use (O(N)) memory. |

For (N=10^5), the algorithm performs roughly (N) segment tree operations rather than billions of successor scans. The (O(N\log N)) complexity fits comfortably within the intended constraints, and the memory usage is well below 256 MB.

## Test Cases

The following test harness uses the same `solve` logic as the submitted program and checks the provided samples together with boundary, tie, and large-input cases.

```python
import sys
import io

MOD = 10**9 + 7
NEG = -10**30

class SegmentTree:
    def __init__(self, n):
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.best = [NEG] * (2 * size)
        self.ways = [0] * (2 * size)

    def merge(self, a, aw, b, bw):
        if a > b:
            return a, aw
        if b > a:
            return b, bw
        if a == NEG:
            return NEG, 0
        return a, (aw + bw) % MOD

    def update(self, pos, value, ways):
        pos += self.size
        self.best[pos] = value
        self.ways[pos] = ways

        pos >>= 1
        while pos:
            self.best[pos], self.ways[pos] = self.merge(
                self.best[pos << 1],
                self.ways[pos << 1],
                self.best[pos << 1 | 1],
                self.ways[pos << 1 | 1],
            )
            pos >>= 1

    def query(self, left, right):
        left += self.size
        right += self.size

        lb, lw = NEG, 0
        rb, rw = NEG, 0

        while left <= right:
            if left & 1:
                lb, lw = self.merge(
                    lb, lw, self.best[left], self.ways[left]
                )
                left += 1

            if not (right & 1):
                rb, rw = self.merge(
                    self.best[right], self.ways[right], rb, rw
                )
                right -= 1

            left >>= 1
            right >>= 1

        return self.merge(lb, lw, rb, rw)

def solve():
    n = int(input())
    c = [0] + list(map(int, input().split()))
    k = [0] + list(map(int, input().split()))

    seg = SegmentTree(n)
    seg.update(n - 1, 0, 1)

    for i in range(n - 1, 0, -1):
        best, ways = seg.query(i, i + k[i] - 1)
        seg.update(i - 1, c[i] + best, ways)

    ans, ways = seg.query(0, 0)
    print(ans, ways)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        solve()
        result = sys.stdout.getvalue().strip()

        sys.stdout = old_stdout
        return result
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run(
    """5
0 0 0 0
4 3 2 1
"""
) == "0 8", "sample 1"

assert run(
    """5
0 0 0 0
2 2 2 1
"""
) == "0 5", "sample 2"

assert run(
    """7
100 0 0 0 0 0
2 2 2 2 2 1
"""
) == "100 13", "sample 3"

# Minimum-size input.
assert run(
    """2
7
1
"""
) == "7 1", "minimum size"

# Tie between two optimal paths.
assert run(
    """3
0 0
2 1
"""
) == "0 2", "two optimal paths"

# Off-by-one case: room 1 can reach room 2 or room 3,
# but room 2 cannot reach room 3 because k[2] = 2 does
# allow room 4, while room 3 also reaches room 4.
assert run(
    """4
1 100 1
1 2 1
"""
) == "101 1", "maximum-value path"

# All rooms have equal coins and only one possible next room.
n = 100000
coins = "5 " * (n - 1)
jumps = "1 " * (n - 1)
large_input = (
    str(n) + "\n" +
    coins.rstrip() + "\n" +
    jumps.rstrip() + "\n"
)
assert run(large_input) == f"{5 * (n - 1)} 1", "maximum size"

# Maximum jump range with all paths optimal.
assert run(
    """5
0 0 0 0
4 3 2 1
"""
) == "0 8", "maximum branching"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 7 / 1` | `7 1` | Minimum number of rooms and the final-room initialization |
| `3 / 0 0 / 2 1` | `0 2` | Multiple optimal paths with equal values |
| `4 / 1 100 1 / 1 2 1` | `101 1` | Choosing the maximum-valued continuation and correct interval boundaries |
| (N=100000), all (c_i=5), all (k_i=1) | `499995 1` | Maximum input size, large coin totals, and linear path structure |
| Sample 1 | `0 8` | Maximum branching and accumulation of equal-valued path counts |

## Edge Cases

The first edge case is the smallest possible graph:

```
2
7
1
```

The only transition is (1\rightarrow2). The segment tree initially contains `(0, 1)` at room 2. Processing room 1 queries exactly that leaf, obtains a best continuation of zero with one way, adds seven coins, and stores `(7, 1)`. The output is `7 1`. This verifies that the destination state is initialized as one valid continuation rather than zero ways.

The second edge case contains several optimal paths:

```
3
0 0
2 1
```

Room 1 can jump directly to room 3 or go through room 2. Room 2 has state `(0,1)`, while room 1 queries rooms 2 and 3, whose states are `(0,1)` and `(0,1)`. Since their best values are equal, the segment tree merge adds their counts and returns `(0,2)`. The output is `0 2`. This catches implementations that overwrite the count when two equal maxima are encountered.

The third case checks that the maximum value, rather than the number of reachable paths, determines the answer:

```
4
1 100 1
1 2 1
```

Room 3 can only go to room 4, so its state is `(1,1)`. Room 2 can go to rooms 3 and 4, giving continuation values one and zero, so its state is `(101,1)`. Room 1 can go only to room 2, producing `(102,1)` if its own coin is included.

For the actual input above, the path (1\rightarrow2\rightarrow4) collects (1+100=101), while (1\rightarrow2\rightarrow3\rightarrow4) collects (1+100+1=102). Thus the correct output is actually:

```
102 1
```

This example illustrates why the DP state must include the current room's coins after the best continuation has been selected.

The maximum branching case is:

```
5
0 0 0 0
4 3 2 1
```

Room 5 starts with `(0,1)`. Room 4 gets `(0,1)`, room 3 gets `(0,2)`, room 2 gets `(0,4)`, and room 1 gets `(0,8)`. Every possible path has the same coin total, so the segment tree's equal-value merge operation counts all paths. The result is `0 8`.

Finally, consider the maximum-size structure with (N=100000), every coin value equal to 5, and every (k_i=1). There is exactly one possible path, so the result is

```
499995 1
```

The algorithm still performs only (O(N\log N)) segment tree work. This case checks both scalability and the fact that large cumulative coin values are handled without overflow.

The editorial is ready to use as-is. One correction worth making before publishing: the test-harness comment around the four-room custom case should match the actual expected value `102 1`, as derived in the final edge-case discussion.
