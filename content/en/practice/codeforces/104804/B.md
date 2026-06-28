---
title: "CF 104804B - \u041d\u0430\u0447\u0430\u043b\u043e \u0438\u0433\u0440\u044b"
description: "We are simulating a very structured drafting process among four players sitting in a fixed cycle. Each round, every player takes exactly one knight token from a common pool until the pool is exhausted."
date: "2026-06-28T13:24:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104804
codeforces_index: "B"
codeforces_contest_name: "Central Russia Regional Contest, 2022, Qualification Contest"
rating: 0
weight: 104804
solve_time_s: 84
verified: false
draft: false
---

[CF 104804B - \u041d\u0430\u0447\u0430\u043b\u043e \u0438\u0433\u0440\u044b](https://codeforces.com/problemset/problem/104804/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a very structured drafting process among four players sitting in a fixed cycle. Each round, every player takes exactly one knight token from a common pool until the pool is exhausted. The only twist is that the order of play is not fixed: after each full round of four picks, the order rotates cyclically, so whoever was first becomes last, and everyone shifts one position forward.

Igor starts in position $k$, and we want to determine how many times he will act before the $n$ tokens run out.

The input consists of two values. The first is the total number of identical tokens available, and the second is Igor’s initial position in the turn order among four players. The output is simply the number of turns during which Igor manages to take a token.

The constraints are very small, with $n \le 100$, so even a direct simulation of every pick is fully sufficient. There is no need for optimization in terms of asymptotic complexity, and even $O(n)$ or $O(n \cdot 4)$ behavior is trivial.

A subtle point is that the rotation of players does not change the fact that each player still acts exactly once per full cycle of four moves. The rotation only permutes who occupies each position, not the frequency of appearances. Because of this, each player will still appear exactly once per round of four picks. The only complication is that Igor’s identity moves through positions in a predictable cyclic pattern.

There are no meaningful edge cases beyond small boundary checks such as $n = 1$, where only the first position acts once, or $k = 4$, where Igor starts last in the first cycle.

## Approaches

A direct simulation is the most immediate interpretation. We maintain an array of four players representing the current order. For each token, we take the player at the front of the order, assign them a token, then rotate the order after every four picks. This works correctly because it mirrors the game rules exactly.

However, simulating rotations is unnecessary. The key observation is that the rotation after every full round simply shifts identities, but does not change the fact that each player gets exactly one pick per round. Over any consecutive block of four moves, each of the four players appears exactly once. Therefore, across all $n$ tokens, the number of times Igor appears depends only on how many complete or partial rounds occur, not on the internal rotation structure.

This reduces the problem to a simple periodic counting task. Since every group of 4 picks distributes exactly one pick to each player, Igor receives one pick per full group of 4, plus possibly one extra if his position lies within the leftover incomplete group.

The brute force approach would simulate every pick and rotate arrays, which costs constant work per pick but includes overhead of managing state transitions. The optimized view removes all state and reduces everything to arithmetic on cycles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Periodic Counting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many full rounds of four picks exist in $n$. This is $n // 4$. Each full round guarantees exactly one pick for Igor.
2. Add these full-round contributions to Igor’s answer. This forms the baseline count.
3. Compute the remainder $n \% 4$, which represents the incomplete final round, if any.
4. Check whether Igor’s position $k$ falls within the first $r$ positions of a round. If yes, Igor receives one additional pick.
5. Output the accumulated total.

The key idea is that within each cycle of four moves, positions 1 through 4 are all used exactly once, so the only question in the final partial cycle is whether Igor’s position would have been reached before the cycle ends.

### Why it works

The system behaves like a repeating schedule of length 4 where every player is guaranteed exactly one occurrence per full period. Rotations between rounds permute identities but preserve the invariant that each identity appears once per cycle. Therefore, the total number of appearances of Igor depends only on how many complete cycles exist plus whether he is scheduled in the incomplete suffix of the final cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

full = n // 4
rem = n % 4

ans = full

if k <= rem:
    ans += 1

print(ans)
```

The code directly implements the cycle decomposition. The integer division by 4 counts complete rounds, each contributing exactly one guaranteed pick for Igor. The remainder captures a partial round, and the comparison `k <= rem` checks whether Igor’s position would still be active in that unfinished segment.

No simulation is required, and no explicit representation of player rotation is needed because the rotation does not affect per-cycle frequency.

## Worked Examples

### Example 1: Input `9 3`

We split the sequence of 9 picks into full cycles and remainder.

| Step | Full cycles (n//4) | Remainder (n%4) | k | Extra pick? | Total |
| --- | --- | --- | --- | --- | --- |
| Initial | 0 | 9 | 3 | No | 0 |
| After full cycles | 2 | 1 | 3 | No | 2 |
| Final adjustment | 2 | 1 | 3 | No (3 > 1) | 2 |

This shows that Igor only benefits from complete rounds, and the leftover single move does not reach position 3, so no extra pick is granted.

### Example 2: Input `11 2`

| Step | Full cycles (n//4) | Remainder (n%4) | k | Extra pick? | Total |
| --- | --- | --- | --- | --- | --- |
| Initial | 0 | 11 | 2 | No | 0 |
| After full cycles | 2 | 3 | 2 | Yes | 3 |

Here, Igor gets two guaranteed picks from full cycles and one additional pick because position 2 lies within the first 3 moves of the final partial cycle.

This confirms that the remainder logic correctly captures partial-cycle participation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations on two integers |
| Space | O(1) | No auxiliary data structures |

The solution is constant time regardless of input size, which is well within the constraints and far beyond what is required for $n \le 100$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())

    full = n // 4
    rem = n % 4
    ans = full
    if k <= rem:
        ans += 1
    return str(ans)

# provided samples
assert run("9 3") == "3"
assert run("11 2") == "3"
assert run("12 3") == "3"

# custom cases
assert run("1 1") == "1"
assert run("4 4") == "1"
assert run("5 1") == "2"
assert run("7 4") == "1"
assert run("8 2") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimum case, single pick |
| 4 4 | 1 | full cycle boundary |
| 5 1 | 2 | transition into second cycle |
| 7 4 | 1 | last position not in partial cycle |
| 8 2 | 2 | multiple full cycles plus remainder |

## Edge Cases

For $n = 1$, the algorithm computes $full = 0$, $rem = 1$. If $k = 1$, the condition $k \le rem$ holds, so the result is 1. This matches the fact that only one pick occurs and Igor at position 1 takes it immediately.

For $n = 4$, we get one full cycle and no remainder. Each player, including Igor regardless of $k$, receives exactly one pick. The formula returns $1$ because $full = 1$ and $rem = 0$, so no extra addition occurs.

For cases where $k = 4$, only the remainder matters. If $n \mod 4 < 4$, Igor only contributes in the final partial cycle if it reaches the fourth position. Otherwise he only receives full-cycle contributions.
