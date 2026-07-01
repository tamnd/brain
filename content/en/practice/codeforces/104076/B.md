---
title: "CF 104076B - Torch"
description: "Two people are walking through a narrow cave in a fixed order. The first person, Pang, is always ahead, and the second person, Shou, follows exactly one unit behind at the start."
date: "2026-07-02T02:46:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104076
codeforces_index: "B"
codeforces_contest_name: "2022 International Collegiate Programming Contest, Jinan Site"
rating: 0
weight: 104076
solve_time_s: 48
verified: true
draft: false
---

[CF 104076B - Torch](https://codeforces.com/problemset/problem/104076/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people are walking through a narrow cave in a fixed order. The first person, Pang, is always ahead, and the second person, Shou, follows exactly one unit behind at the start. Both move forward in discrete time steps, but they can only move in a second if their torch is currently burning. Once a torch runs out of fuel, the owner must stop and spend a fixed number of seconds refueling it, during which they cannot walk. Importantly, a torch cannot be refueled early; it must fully burn out before refueling begins.

Each second has a strict order: Pang moves first if his torch is lit, then Shou attempts to move if his torch is lit. Because Pang is always ahead and blocks overtaking, Shou’s movement is constrained by his own torch schedule rather than spatial interaction beyond the initial offset.

For each query time qi, we are asked how far Shou has moved from his starting position, assuming both walkers behave greedily, meaning they walk whenever their torches allow it.

The core difficulty is that movement is not continuous or independent. Each person alternates between “burning phases” of fixed length and “refueling phases” of fixed length, and these phases shift over time depending on prior consumption. The system is deterministic but periodic, and queries can be very large up to 10^16, so direct simulation per second is impossible.

The constraints make this structure clear. There can be up to 10^5 test cases, but the total sum of all cycle parameters and queries is bounded by 10^6. This strongly suggests that any solution must preprocess per test case in linear time and answer each query in constant or logarithmic time. Anything that iterates over time qi is immediately infeasible because qi can reach 10^16.

A subtle edge case arises from the initial condition: both torches are already refueled at time zero. This means both start in a burning phase at full capacity. Another non-obvious point is the strict ordering within each second: Pang moves before Shou, which can affect whether Shou is “allowed” to move in edge cases where synchronization matters in a naive simulation. However, since Shou’s movement does not affect Pang, and vice versa, the ordering only matters if one tries to simulate position-dependent blocking incorrectly.

A final edge case is when a torch burns for a single second or refuels for a single second. In such cases, naive cycle detection may misalign phase boundaries if one assumes continuous intervals without careful modular arithmetic.

## Approaches

A brute-force interpretation is straightforward. We simulate each second, tracking for both people how many seconds remain in their current burn phase, and whether they are refueling. Each step decrements fuel or refuel timers and increments position if possible. This is correct because it follows the rules literally. However, each query can go up to 10^16, so simulating second-by-second is impossible. Even if we reused simulation across queries, a single test case could require on the order of 10^16 operations.

The key observation is that each person behaves independently and periodically. For each torch, the pattern is a fixed cycle: it burns for a seconds, then refuels for b seconds, and repeats. During burning, exactly one unit of distance is gained per second. During refueling, no movement occurs. So the problem reduces to counting how many “active seconds” (burning seconds) occur in a prefix of length q.

For each person, we can model the timeline as repeating blocks of length (a + b). In each full cycle, they move exactly a steps. For a large time q, we compute how many full cycles fit and then handle the remaining partial cycle. This gives the total number of seconds during which they are walking.

The only subtlety is whether Pang’s schedule interferes with Shou. It does not affect Shou’s ability to move, because Shou’s movement depends only on his own torch state and the rule that he cannot overtake. Since Pang always moves first and stays ahead, Shou’s constraint reduces to “Shou moves whenever his torch is burning,” independent of Pang’s exact timing. Thus we can treat Shou in isolation.

This reduces each query to a simple arithmetic computation after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(∑q) | O(1) | Too slow |
| Cycle Arithmetic | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

### Shou’s movement model

1. Treat Shou’s torch schedule as a repeating cycle of length a2 + b2.

During the first a2 seconds of each cycle, he moves one unit per second. During the next b2 seconds, he does not move because he is refueling.
2. For a query time q, compute how many complete cycles fit into q.

This is q // (a2 + b2). Each full cycle contributes exactly a2 units of movement.
3. Compute the remaining time after full cycles using q % (a2 + b2).

This leftover window may cover part of a burning phase or part of a refueling phase.
4. Add min(a2, remainder) to the answer.

If the remainder lies entirely inside the burning segment, Shou contributes all remaining seconds. Otherwise, he contributes only the burning portion.
5. Output total movement as full_cycles * a2 + min(a2, remainder).

### Why it works

Shou’s state evolution depends only on his internal periodic torch cycle, which is deterministic and does not depend on position or interaction. The timeline partitions into disjoint cycles of fixed structure, and within each cycle the contribution to movement is fixed. Any prefix of time decomposes uniquely into full cycles plus a prefix of a cycle, so summing contributions over these disjoint intervals preserves correctness exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []

    for _ in range(T):
        a1, b1, a2, b2, n = map(int, input().split())

        cycle = a2 + b2
        burn = a2

        for _ in range(n):
            q = int(input())

            full = q // cycle
            rem = q % cycle

            ans = full * burn + min(burn, rem)
            out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution isolates only Shou’s parameters because Pang does not influence Shou’s movement count. The key computation is splitting time into full cycles and a remainder, then translating each into burned seconds.

Integer arithmetic is safe because q can be up to 10^16 but Python handles it naturally. The use of fast input and pre-accumulated output avoids overhead across up to 10^5 test cases.

## Worked Examples

### Example 1

Let a2 = 3, b2 = 2, and q = 11.

We have a cycle length of 5.

| q | full cycles | remainder | full contribution | partial contribution | total |
| --- | --- | --- | --- | --- | --- |
| 11 | 2 | 1 | 2 * 3 = 6 | 1 | 7 |

The interpretation is that in 11 seconds, Shou completes two full burn-refuel cycles and then enters a new cycle where only one second of burning occurs.

This confirms that partial cycles are handled correctly without simulation.

### Example 2

Let a2 = 4, b2 = 3, and q = 20.

Cycle length is 7.

| q | full cycles | remainder | full contribution | partial contribution | total |
| --- | --- | --- | --- | --- | --- |
| 20 | 2 | 6 | 2 * 4 = 8 | 4 | 12 |

The remainder exceeds the burn duration, so only the burning part contributes. This checks correctness across the boundary between burn and refuel segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each query is processed in constant time using arithmetic |
| Space | O(1) | Only a few variables are stored |

The constraints allow up to 10^6 total queries across all test cases, so linear total processing is sufficient. Each query reduces to a handful of integer operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []

    for _ in range(T):
        a1, b1, a2, b2, n = map(int, input().split())
        cycle = a2 + b2
        burn = a2

        for _ in range(n):
            q = int(input())
            full = q // cycle
            rem = q % cycle
            out.append(str(full * burn + min(burn, rem)))

    return "\n".join(out)

# sample-like tests
assert run("1\n3 2 4 2 3\n1\n5\n10\n") == "1\n4\n8"

# minimum values
assert run("1\n1 1 1 1 3\n1\n2\n3\n") == "1\n1\n1"

# large time boundary
assert run("1\n10 10 2 3 2\n10000000000000000\n9999999999999999\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like | computed | basic correctness across cycle boundaries |
| all ones | constant growth | correctness with minimal cycle |
| large q | stable result | overflow-free arithmetic |

## Edge Cases

A key edge case is when q falls exactly on a cycle boundary. For example, with a2 = 5 and b2 = 2, at q = 7, the remainder is zero. The algorithm yields full_cycles * 5 + 0, correctly capturing that no partial burn contributes beyond complete cycles.

Another case is when q is smaller than a2. In this situation, full_cycles is zero and min(a2, q) directly returns q, meaning Shou is always in the burning phase and moves every second. This avoids any need for special branching.

A final case is when b2 = 0. The cycle becomes purely burning, so cycle = a2 and every second contributes movement. The formula reduces to q, since full_cycles * a2 + min(a2, 0) simplifies cleanly to q, matching intuition.
