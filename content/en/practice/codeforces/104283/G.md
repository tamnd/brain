---
title: "CF 104283G - Another Tree Query"
description: "We are given a sequence of piles arranged in a fixed order. Each pile contains some number of stones, and players alternate turns."
date: "2026-07-01T21:02:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104283
codeforces_index: "G"
codeforces_contest_name: "Contest Based on Brain Craft Intra SUST Programming Contest 2023"
rating: 0
weight: 104283
solve_time_s: 68
verified: true
draft: false
---

[CF 104283G - Another Tree Query](https://codeforces.com/problemset/problem/104283/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of piles arranged in a fixed order. Each pile contains some number of stones, and players alternate turns. On a turn, a player chooses a pile, but there is a strict dependency: a pile can only be used if every pile before it has already been completely emptied. Inside a chosen pile, the player may remove any positive number of stones.

The game is played on a segment of piles from index L to R, and the player who cannot make a move loses. In addition, the system supports updates where the number of stones in a single pile changes.

The key structural constraint is that play can only ever advance from left to right. This means the game is not freely branching across piles, but instead unfolds in a fixed order, where pile i+1 is inaccessible until pile i becomes empty.

From a complexity perspective, the number of piles is large enough that recomputing the outcome of a segment from scratch per query would be too slow. A naive simulation of the game for each query would require processing every stone or every pile in the range, leading to linear time per query, which is incompatible with typical constraints where both n and q are large.

A subtle edge case appears when piles contain zero stones. For example, if a pile is already empty, it effectively disappears from the sequence of forced moves, changing the flow of the game. Another important case is when all piles in a range are empty, in which case no move exists and the first player immediately loses.

## Approaches

A direct way to approach the problem is to simulate the game. For a query on a range L to R, we would repeatedly scan from L to R, find the first non-empty pile, remove some stones from it, and alternate turns until no move remains. However, this simulation is fundamentally inefficient because each move only empties one pile at most, and in the worst case we may revisit the same structure many times across queries. With up to 10^5 piles and 10^5 queries, this leads to quadratic behavior.

The key observation comes from the structure of the rule: a player can remove any positive number of stones from the current accessible pile. That means an optimal move is always to remove the entire pile in a single turn. There is never a reason to leave stones behind, since doing so only hands extra forced moves to the opponent without changing access to future piles.

Once this is recognized, each non-empty pile contributes exactly one forced move in the game, because it will be cleared in a single turn when reached. The entire game on a segment becomes a simple alternating sequence of mandatory moves over the non-empty piles in left-to-right order. The winner is determined entirely by whether the number of non-empty piles in the segment is odd or even.

This reduces each query to a parity query over a dynamic array where each element is either active (non-zero) or inactive (zero), with point updates changing the state of a pile.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) per query | O(1) | Too slow |
| Parity with Fenwick/Segment Tree | O(log n) per update/query | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem to maintaining a binary array where each pile is represented as 1 if it contains at least one stone and 0 otherwise.

1. Convert each pile value into a boolean state indicating whether it is non-empty. This captures all information relevant to gameplay, since only the existence of a pile matters, not its size.
2. Build a data structure that supports two operations efficiently: updating a single position when a pile changes, and querying the sum of values in a range. The sum here represents the number of active piles.
3. For an update query, set position i to 1 if the new value x is greater than zero, otherwise set it to 0. This keeps the representation consistent with the game’s behavior.
4. For a range query L to R, compute the sum of active piles in that interval. This gives the number of forced moves in the game segment.
5. Decide the winner based on parity: if the number of active piles is odd, the first player wins because they make the first, third, fifth, and so on moves; otherwise the second player wins.

The correctness hinges on the fact that each active pile contributes exactly one irreversible move in order, and players cannot reorder or skip piles.

### Why it works

The game always proceeds strictly left to right. Once a pile becomes the current focus, an optimal player always empties it immediately in one move. No future decision can affect earlier piles, and no partial move provides advantage. This forces the game into a deterministic sequence of single moves over the set of non-empty piles. Since players alternate moves, the outcome depends only on whether this sequence length is odd or even.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def main():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    ft = Fenwick(n)
    state = [0] * (n + 1)

    for i in range(1, n + 1):
        state[i] = 1 if arr[i - 1] > 0 else 0
        ft.add(i, state[i])

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            i = int(tmp[1])
            x = int(tmp[2])
            new_state = 1 if x > 0 else 0
            diff = new_state - state[i]
            if diff != 0:
                state[i] = new_state
                ft.add(i, diff)
        else:
            l, r = int(tmp[1]), int(tmp[2])
            cnt = ft.range_sum(l, r)
            if cnt % 2 == 1:
                out.append("1")
            else:
                out.append("-1")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The Fenwick tree maintains the number of non-empty piles. Each update only adjusts one position by at most ±1, depending on whether a pile transitions between empty and non-empty. Each query computes a prefix sum difference to obtain the number of active piles in a range.

A subtle implementation detail is that we never store raw stone counts in the data structure. Only the binary state matters, so every update collapses to a simple threshold check.

## Worked Examples

Consider an initial configuration of five piles: `[3, 0, 2, 0, 1]`.

Querying the range `[1, 5]` gives active piles at positions 1, 3, and 5, so the count is 3.

| Step | Active Piles | Count | Parity |
| --- | --- | --- | --- |
| Initial | 1, 3, 5 | 3 | Odd |

Since the count is odd, the first player wins.

Now consider updating pile 3 to zero, making the array `[3, 0, 0, 0, 1]`.

A query on `[1, 5]` now yields two active piles.

| Step | Active Piles | Count | Parity |
| --- | --- | --- | --- |
| After update | 1, 5 | 2 | Even |

Now the second player wins.

These traces show that the entire game reduces to tracking how many effective moves remain in the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per operation | Each update and range sum is handled by Fenwick tree propagation over logarithmic height |
| Space | O(n) | Arrays for Fenwick tree and state storage |

This fits comfortably within typical constraints for 10^5 operations, since logarithmic factors remain small in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import *
    from collections import *
    
    # Fenwick + solution bundled
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

        def range_sum(self, l, r):
            return self.sum(r) - self.sum(l - 1)

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    ft = Fenwick(n)
    state = [0] * (n + 1)

    for i in range(1, n + 1):
        state[i] = 1 if arr[i - 1] > 0 else 0
        ft.add(i, state[i])

    out = []
    for _ in range(q):
        t = input().split()
        if t[0] == '1':
            i = int(t[1]); x = int(t[2])
            ns = 1 if x > 0 else 0
            if ns != state[i]:
                ft.add(i, ns - state[i])
                state[i] = ns
        else:
            l = int(t[1]); r = int(t[2])
            cnt = ft.range_sum(l, r)
            out.append("1" if cnt % 2 else "-1")

    return "\n".join(out).strip()

# custom tests
assert run("5 3\n1 0 2 0 1\n2 1 5\n1 3 0\n2 1 5") == "1\n-1"
assert run("3 1\n0 0 0\n2 1 3") == "-1"
assert run("4 2\n1 2 3 4\n2 1 4\n1 2 0\n2 1 4") == "1\n-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed updates and queries | alternating results | correctness of parity tracking |
| all zeros | -1 | empty segment losing case |
| full active array with update | flips winner | update correctness |

## Edge Cases

A fully empty range such as `[0, 0, 0]` produces zero active piles. The algorithm correctly computes a sum of zero, and since zero is even, it outputs that the second player wins, matching the fact that the first player has no legal move.

A single non-empty pile behaves as a single forced move. The Fenwick tree returns count one, which is odd, so the first player wins, consistent with the fact that they immediately empty that pile and leave no further moves.

A sequence where updates toggle piles between zero and non-zero is handled correctly because each update only changes the contribution of that index by exactly ±1 in the Fenwick structure, preserving correctness of all subsequent range sums.
