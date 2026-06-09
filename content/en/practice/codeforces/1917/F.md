---
title: "CF 1917F - Construct Tree"
description: "We are given the lengths of all edges that must appear in a tree. The tree has exactly $n$ edges and $n+1$ vertices, so every length from the array is used exactly once as an edge weight."
date: "2026-06-08T19:48:32+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1917
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 917 (Div. 2)"
rating: 2500
weight: 1917
solve_time_s: 116
verified: true
draft: false
---

[CF 1917F - Construct Tree](https://codeforces.com/problemset/problem/1917/F)

**Rating:** 2500  
**Tags:** bitmasks, constructive algorithms, dp, trees  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the lengths of all edges that must appear in a tree. The tree has exactly $n$ edges and $n+1$ vertices, so every length from the array is used exactly once as an edge weight.

The question is whether we can connect those edges into some tree whose weighted diameter is exactly $d$.

A useful way to think about the problem is that every tree diameter is a simple path. If a tree has diameter $d$, then somewhere inside the tree there must exist a path whose total length is exactly $d$, and every other edge is attached to that path without creating a longer path.

The constraints are surprisingly small in terms of weight. Both $d$ and every $l_i$ are at most $2000$, and the sum of all $n$ over the input is also at most $2000$. This immediately suggests some kind of subset-sum or knapsack dynamic programming over the value $d$. An $O(nd)$ or $O(nd^2 / 64)$ solution is perfectly reasonable, while exponential subset enumeration is impossible.

There are several non-obvious situations that can easily mislead a naive construction.

Consider:

```
n = 2
d = 5
lengths = [3, 3]
```

The correct answer is `No`.

Any tree with two edges is just a path. Its diameter is $3+3=6$, already larger than $d$. A naive approach that only checks whether some subset sums to $d$ would miss this.

Another example:

```
n = 3
d = 10
lengths = [6, 2, 2]
```

The correct answer is `Yes`.

Use the edge of length $6$ on the diameter. The two remaining edges form a path of length $4$, producing a diameter of length $10$. A strategy that insists on building the diameter without the largest edge would incorrectly reject this case.

A more subtle case is:

```
n = 4
d = 10
lengths = [4, 4, 4, 4]
```

The correct answer is `No`.

Although many subsets sum close to $10$, every unused edge has length $4$. Any attachment point on a diameter of length $10$ is at distance at most $5$ from one endpoint, so attaching a length-$4$ edge can easily create a path longer than $10$. The geometry of the diameter matters, not only subset sums.

## Approaches

A brute-force solution would try every subset of edges as candidates for the diameter path. If a subset sums to $d$, we could then check whether the remaining edges can be attached without increasing the diameter.

This is already hopeless. There are $2^n$ subsets, and $n$ can reach $2000$.

The key observation is that only the largest edge really matters among all edges not belonging to the diameter.

Let the largest edge length be $M$.

Suppose we have already built a diameter path of total length $d$. All remaining edges can be attached to a single vertex on that path. If the largest unused edge can be attached without creating a longer diameter, then every smaller unused edge can also be attached there.

This reduces the problem to finding a diameter path and a suitable attachment vertex.

Another crucial observation is that if the two largest edge lengths satisfy

$$l_n + l_{n-1} > d,$$

then the answer is immediately `No`.

Any tree contains a path passing through those two edges, and that path already exceeds $d$.

After sorting the lengths, let $M=l_n$.

We separate the largest edge from the others and perform a DP. The DP partitions the remaining edges into three groups:

First, edges placed on one side of a chosen attachment vertex.

Second, edges placed on the other side.

Third, edges not used on the diameter.

If the two sides have lengths $x$ and $y$, then the resulting diameter length is $x+y$.

The unused largest edge has length $M$. To attach it safely, the attachment vertex must be at distance at least $M$ from both ends of the diameter. That means

$$x \ge M,\qquad y \ge M.$$

The only special case occurs when the largest edge itself lies on the diameter. Then we only need to form the remaining length $d-M$ using the other edges.

The DP state naturally becomes a two-dimensional subset-sum. Because $d \le 2000$, a bitset implementation makes it fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal Bitset DP | $O(nd^2/64)$ | $O(d^2/64)$ | Accepted |

## Algorithm Walkthrough

1. Sort all edge lengths.
2. Let $M$ be the largest length.
3. If the sum of the two largest lengths exceeds $d$, output `No`.

Any tree would necessarily have diameter larger than $d$.
4. Ignore $M$ temporarily and process the other $n-1$ lengths with DP.
5. Define `dp[a][b]` as whether we can distribute processed edges so that one side of the future diameter has total length $a$ and the other side has total length $b$.

Every edge has three choices:

It can be added to the first side.

It can be added to the second side.

It can stay unused.
6. Store the second dimension as a bitset.

If an edge has length $w$, the transitions are:

Put it on the second side:

$$dp[a] \gets dp[a] \;|\; (dp[a] \ll w)$$

Put it on the first side:

$$dp[a] \gets dp[a] \;|\; dp[a-w]$$
7. After processing all edges except $M$, check two possibilities.
8. First possibility: $M$ belongs to the diameter.

Then the remaining edges must form length $d-M$.

Check whether

$$dp[d-M][0]$$

is reachable.
9. Second possibility: $M$ does not belong to the diameter.

Then we need a diameter of length $d$ split around some attachment vertex.

Check whether there exists

$$x+y=d$$

with

$$x\ge M,\qquad y\ge M,$$

and `dp[x][y]` reachable.
10. If either condition succeeds, output `Yes`; otherwise output `No`.

### Why it works

Every valid tree can be transformed into one where all non-diameter edges are attached to a single vertex on the diameter. Only the largest non-diameter edge can potentially create a new longer path, so it is sufficient to verify that this edge can be attached safely.

If the largest edge is itself on the diameter, we only need to complete the remaining diameter length $d-M$.

If it is not on the diameter, then the attachment vertex must be at distance at least $M$ from both ends of the diameter. Writing those distances as $x$ and $y$, we obtain the conditions $x+y=d$, $x\ge M$, and $y\ge M$.

The DP enumerates exactly all possible pairs $(x,y)$ obtainable from the remaining edges. Hence the algorithm accepts exactly when one of the necessary and sufficient constructions exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, d = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        if a[-1] + a[-2] > d:
            print("No")
            continue

        dp = [0] * (d + 1)
        dp[0] = 1  # bit 0 set

        for w in a[:-1]:
            ndp = dp[:]

            for x in range(d, -1, -1):
                cur = dp[x]
                if cur == 0:
                    continue

                # put w on second side
                ndp[x] |= cur << w

                # put w on first side
                if x + w <= d:
                    ndp[x + w] |= cur

            mask = (1 << (d + 1)) - 1
            for i in range(d + 1):
                ndp[i] &= mask

            dp = ndp

        m = a[-1]

        ok = False

        if d - m >= 0:
            ok |= ((dp[d - m] >> 0) & 1) != 0

        for x in range(m, d - m + 1):
            if ((dp[x] >> (d - x)) & 1):
                ok = True
                break

        print("Yes" if ok else "No")

if __name__ == "__main__":
    solve()
```

The array is sorted first because the largest edge plays a special role.

The early rejection `a[-1] + a[-2] > d` eliminates impossible cases immediately.

The DP uses an array of bitsets. Index `x` stores all reachable values of `y`. Each edge can be ignored, added to the first side, or added to the second side. The "ignored" choice is handled automatically because we start from a copy of the previous DP.

The bit shift implements adding an edge to the second side. Moving from `x` to `x+w` implements adding it to the first side.

The final check exactly matches the two constructive cases proved above.

## Worked Examples

### Example 1

Input:

```
4 10
1 2 3 4
```

After sorting:

```
[1, 2, 3, 4]
```

Here $M=4$.

| Processed edge | Reachable side sums |
| --- | --- |
| start | (0,0) |
| 1 | (0,0), (1,0), (0,1) |
| 2 | many pairs including (3,0), (1,2), (0,3) |
| 3 | many pairs including (6,0), (3,3), (4,2) |

We check whether there exists $x+y=10$ with both sides at least $4$.

The pair $(4,6)$ is reachable, so the answer is `Yes`.

This demonstrates the case where the largest edge stays off the diameter.

### Example 2

Input:

```
4 7
1 4 3 4
```

Sorted:

```
[1, 3, 4, 4]
```

The two largest edges satisfy

$$4+4=8>7.$$

| Largest | Second largest | Check |
| --- | --- | --- |
| 4 | 4 | 8 > 7 |

The algorithm immediately outputs `No`.

This demonstrates the strongest necessary condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nd^2 / 64)$ | Bitset DP transitions |
| Space | $O(d^2 / 64)$ | DP table of bitsets |

Since $d \le 2000$ and the total sum of all $n$ is also at most $2000$, the bitset DP easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    data = io.StringIO(inp)
    out = io.StringIO()

    input = data.readline

    t = int(input())

    for _ in range(t):
        n, d = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        if a[-1] + a[-2] > d:
            out.write("No\n")
            continue

        dp = [0] * (d + 1)
        dp[0] = 1

        for w in a[:-1]:
            ndp = dp[:]

            for x in range(d, -1, -1):
                cur = dp[x]
                if cur == 0:
                    continue

                ndp[x] |= cur << w

                if x + w <= d:
                    ndp[x + w] |= cur

            mask = (1 << (d + 1)) - 1
            for i in range(d + 1):
                ndp[i] &= mask

            dp = ndp

        m = a[-1]
        ok = False

        if d - m >= 0:
            ok |= ((dp[d - m] >> 0) & 1) != 0

        for x in range(m, d - m + 1):
            if ((dp[x] >> (d - x)) & 1):
                ok = True
                break

        out.write("Yes\n" if ok else "No\n")

    return out.getvalue()

# provided sample
assert run(
"""3
4 10
1 2 3 4
4 7
1 4 3 4
6 18
2 4 3 7 6 7
"""
) == """Yes
No
Yes
"""

# minimum size
assert run(
"""1
2 5
2 3
"""
) == """Yes
"""

# impossible because two largest exceed d
assert run(
"""1
2 5
3 3
"""
) == """No
"""

# all equal
assert run(
"""1
4 8
2 2 2 2
"""
) == """Yes
"""

# boundary condition
assert run(
"""1
4 10
4 4 4 4
"""
) == """No
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 5 / 2 3` | Yes | Smallest nontrivial valid tree |
| `2 5 / 3 3` | No | Diameter already exceeds target |
| `2 2 2 2 , d=8` | Yes | All lengths equal |
| `4 4 4 4 , d=10` | No | Attachment constraints matter |

## Edge Cases

Consider:

```
1
2 5
3 3
```

The algorithm first checks the two largest lengths.

$$3+3=6>5$$

and immediately returns `No`.

This avoids falsely accepting based on subset-sum reasoning alone.

Consider:

```
1
3 10
6 2 2
```

After sorting, $M=6$. The DP on the remaining edges finds a subset summing to $d-M=4$. The algorithm accepts through the "largest edge lies on the diameter" case and outputs `Yes`.

Consider:

```
1
4 10
4 4 4 4
```

The DP can create many diameter decompositions summing to $10$, but none satisfy the requirement that both sides around the attachment vertex are at least $4$. The final validation fails and the answer is `No`.

These examples illustrate why both the diameter-sum condition and the attachment geometry must be checked simultaneously.
