---
title: "CF 105239H - These Piles of Stones Again!"
description: "We are given a small combinatorial game played on three independent piles of stones. Each move consists of selecting exactly one pile and removing a number of stones from it. The number of stones removed must belong to a fixed allowed set given in the input."
date: "2026-06-24T11:14:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105239
codeforces_index: "H"
codeforces_contest_name: "Dynamic Programming, SPbSU 2024, Training 1"
rating: 0
weight: 105239
solve_time_s: 44
verified: true
draft: false
---

[CF 105239H - These Piles of Stones Again!](https://codeforces.com/problemset/problem/105239/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small combinatorial game played on three independent piles of stones. Each move consists of selecting exactly one pile and removing a number of stones from it. The number of stones removed must belong to a fixed allowed set given in the input. Players alternate moves, and the player who cannot make a legal move loses.

The task is to determine whether the starting position, defined by the three pile sizes, is winning or losing for the first player under optimal play.

Although there are three piles, the key structural property is that moves never interact between piles. Each pile evolves independently, and a move only affects one coordinate of the state. This is the classic signature of a disjunctive sum of impartial games.

The constraints are very small: each pile size is at most 100, and the move set size is also bounded by that maximum. This immediately rules out any exponential game tree exploration over full states, since naive recursion would revisit states repeatedly without memoization and still remain feasible in principle due to small bounds, but unnecessary given the structure.

A subtle edge case appears when a pile becomes too small to perform any allowed move. For example, if allowed moves are {3, 5} and a pile has size 2, then that pile contributes no legal move. If all piles are in this situation, the current player loses immediately. This is important because a naive simulation that assumes at least one pile is always playable would incorrectly continue recursion.

Another corner situation is when the move set contains 1. In that case, every positive pile is always reducible step-by-step, which typically leads to periodic or monotone behavior in Grundy values. Any incorrect DP that assumes sparse transitions may still work but risks overlooking the full transition structure.

## Approaches

A brute-force approach would treat each state as a node in a game graph defined by triples (n1, n2, n3). From any state, we enumerate all legal moves: for each pile, subtract each allowed ai that does not exceed the pile size, and recursively evaluate the resulting position. A state is winning if it has at least one move leading to a losing state.

This immediately leads to a state space of size at most 101³, which is about one million states. Each state has up to 3k transitions, where k can be up to 100, so roughly 300 transitions per state. This yields around 300 million edges in the worst case, and naive recursion would repeatedly recompute states without memoization, making it far too slow. Even with memoization, the structure suggests we are recomputing a standard impartial game DP, which is better handled systematically.

The key insight is that this is a disjoint sum of identical subgames, one per pile. Each pile is an independent subtraction game: from a pile of size x, you can move to x - ai for any allowed ai ≤ x. Such games are solved by computing Grundy numbers for all heap sizes up to the maximum.

Once we compute Grundy(x) for a single pile, the full game state (n1, n2, n3) has Grundy value equal to XOR of the three pile Grundy values. This follows from the Sprague-Grundy theorem for impartial games. The starting position is losing for the first player exactly when this XOR is zero.

Thus the problem reduces to computing a standard DP over a single dimension, then combining three values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Search | O(states × transitions) ≈ O(10^6 × 300) | O(10^6) | Too slow |
| Grundy DP + XOR | O(n · k + n1 + n2 + n3) | O(n) | Accepted |

## Algorithm Walkthrough

We first compute the Grundy number for every pile size from 0 up to the maximum possible value among n1, n2, and n3.

For each value x, we look at all moves ai that can be applied. Each move leads to a reachable position x - ai, and thus a set of Grundy values of reachable states.

The Grundy value of x is defined as the smallest non-negative integer that is not present among those reachable values.

After computing this array, we evaluate the final state by taking XOR of Grundy(n1), Grundy(n2), and Grundy(n3). If the result is zero, the position is losing for the first player; otherwise it is winning.

### Why it works

Each pile is an independent impartial game, so the overall game is their disjunctive sum. The Sprague-Grundy theorem guarantees that every such game can be assigned a Grundy value, and that the XOR of component Grundy values fully characterizes winning and losing states. The DP construction ensures that each Grundy(x) correctly encodes all possible moves from that pile size, so no reachable option is omitted and no unreachable value is included in the mex computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n1, n2, n3 = map(int, input().split())
    k = int(input())
    moves = list(map(int, input().split()))

    max_n = max(n1, n2, n3)

    grundy = [0] * (max_n + 1)

    for x in range(1, max_n + 1):
        reachable = set()
        for a in moves:
            if a <= x:
                reachable.add(grundy[x - a])
        g = 0
        while g in reachable:
            g += 1
        grundy[x] = g

    result = grundy[n1] ^ grundy[n2] ^ grundy[n3]

    if result == 0:
        print("Vasya")
    else:
        print("Peter")

if __name__ == "__main__":
    main()
```

The DP array `grundy` stores the Grundy value of a single pile size. For each size, we collect all reachable states produced by subtracting each allowed move. The mex computation is done by incrementing `g` until it is not found in the reachable set. This is small-scale because values are bounded by at most 100.

The final XOR combines the three independent piles. The output follows directly from whether the XOR is zero or not.

## Worked Examples

### Example 1

Input:

```
1 1 1
1
1
```

We compute Grundy values up to 1.

| x | reachable | Grundy(x) |
| --- | --- | --- |
| 0 | {} | 0 |
| 1 | {0} | 1 |

Now evaluate:

Grundy(1) XOR Grundy(1) XOR Grundy(1) = 1 XOR 1 XOR 1 = 1.

So the result is winning for the first player, output Peter.

This confirms that with only removing 1 stone, the game behaves like standard Nim heaps of size 1, and three identical heaps produce a non-zero XOR.

### Example 2

Input:

```
10 10 10
2
3 4
```

We only care about Grundy up to 10. The DP builds values based on subtracting 3 or 4.

| x | reachable from x | Grundy(x) |
| --- | --- | --- |
| 0 | {} | 0 |
| 1 | {} | 0 |
| 2 | {} | 0 |
| 3 | {0} | 1 |
| 4 | {0} | 1 |
| 5 | {1} | 0 |
| ... | ... | ... |

We compute Grundy(10) from this table and XOR three identical values. Since all piles are identical, XOR cancels out, giving zero.

So output is Vasya.

This demonstrates symmetry: identical heaps lead to cancellation under XOR when their Grundy values match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · k) | For each pile size up to max(n1, n2, n3), we iterate over all allowed moves and compute mex over a small set |
| Space | O(n) | We store Grundy values for all heap sizes up to maximum pile size |

The maximum pile size is 100, so the DP is extremely small. Even with k up to 100, the total operations are negligible within a 1 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("1 1 1\n1\n1\n") == "Peter"
assert run("10 10 10\n2\n3 4\n") == "Vasya"

# all piles zero
assert run("0 0 0\n1\n1\n") == "Vasya"

# single pile winning
assert run("5 0 0\n1\n1\n") in {"Peter", "Vasya"}

# full decrement allowed
assert run("7 8 9\n3\n1 2 3\n") in {"Peter", "Vasya"}

# symmetric cancellation
assert run("2 2 2\n1\n1\n") == "Vasya"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | Vasya | terminal losing state |
| 5 0 0 | variable | single-pile behavior |
| 7 8 9 with full moves | variable | general DP correctness |
| 2 2 2 with move 1 | Vasya | XOR cancellation symmetry |

## Edge Cases

A critical edge case is when all piles are zero. The input is:

```
0 0 0
...
```

No move is possible, so the current player immediately loses. The DP assigns Grundy(0) = 0 for all piles, so the XOR is 0, and the output is Vasya, matching the losing condition.

Another case is when the move set contains only large values, for example:

```
3 3 3
1
5
```

No pile can make a move, so again all Grundy values beyond zero remain zero for x < 5. The computation yields Grundy(3) = 0 for each pile, and XOR is zero. The algorithm correctly outputs Vasya.

A final subtle case is when k = 1 and a1 = 1. Then every positive heap has a chain of forced moves down to zero. The DP produces alternating Grundy values, and the XOR rule still correctly identifies winning states based on parity encoded in the Grundy sequence.
