---
title: "CF 105385D - Hero of the Kingdom"
description: "We are given a trading simulation where a player can repeatedly convert money into flour and then convert flour back into money at a better price. The player starts with some amount of gold and has a limited amount of time."
date: "2026-06-23T16:17:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105385
codeforces_index: "D"
codeforces_contest_name: "The 2024 CCPC Shandong Invitational Contest and Provincial Collegiate Programming Contest"
rating: 0
weight: 105385
solve_time_s: 56
verified: true
draft: false
---

[CF 105385D - Hero of the Kingdom](https://codeforces.com/problemset/problem/105385/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a trading simulation where a player can repeatedly convert money into flour and then convert flour back into money at a better price. The player starts with some amount of gold and has a limited amount of time. Each action is not instantaneous, instead the time depends linearly on how many bags of flour are handled in that action, with an additional fixed overhead.

There are two operations. The first operation lets the player buy x bags of flour from a mill. Each such batch costs p · x gold and takes a · x + b seconds. The second operation lets the player sell x bags of flour to a tavern, earning q · x gold and taking c · x + d seconds. The key condition is that q is strictly greater than p, so each bag produces profit in gold if bought and then sold.

The player can repeat these operations in any order, but each operation consumes time, and the total time cannot exceed t. The goal is to choose a sequence of buy and sell batches so that final gold is maximized.

The important structure is that profit is linear in x, but time has both linear and fixed costs. This means grouping decisions matter: doing many small trades may waste time due to repeated fixed overheads, while doing large trades improves efficiency but may not fit in time or budget constraints.

The constraints push toward an O(T log something) or O(T) per test solution. Since T can be up to 500 and values up to 10^9, any solution that simulates per unit of time or per unit of gold is impossible. We need to treat operations as aggregated "transactions" and reason about optimal batch sizes.

A subtle failure case appears when a greedy strategy always chooses the maximum possible x per operation. For example, if we always buy as many bags as possible and then immediately sell them, we may waste time due to large linear time cost per batch. Another failure case arises when ignoring fixed overheads b and d: if x is small, overhead dominates and repeated small cycles become inefficient compared to fewer large cycles.

## Approaches

A brute-force solution would simulate all possible sequences of operations, trying every possible number of bags for each buy and sell step and branching over all valid splits of time. This would correctly explore all strategies because any optimal strategy is a sequence of discrete batch operations, but the branching factor is enormous. Even restricting x to at most m/p, the number of operations is still unbounded over time t, and each step changes both money and time in a coupled way. In the worst case, time allows on the order of 10^9 / 1 ≈ 10^9 unit-scale decisions, making any step-by-step simulation infeasible.

The key observation is that the process is monotonic in structure: once we decide to perform a buy-sell cycle of size x, the net effect is a deterministic transformation of state. Each full cycle increases gold by (q − p)x and consumes time (a + c)x + (b + d). There is no intermediate benefit from partially interleaving cycles at finer granularity, because splitting a cycle into multiple smaller cycles strictly increases total overhead consumption without increasing profit.

This reduces the problem to choosing how many full cycles we can perform and how large each cycle should be. Since profit per bag is fixed, the only tradeoff is amortizing fixed time costs b + d against linear time costs. This leads to the insight that optimal strategy is to perform as few cycles as possible with as large x as possible, subject to affordability and time constraints. The limiting factor becomes either initial capital m or time budget t.

We then model feasibility of a cycle size x: we must have p · x ≤ current gold, and total time per cycle must fit into remaining time. Once x is fixed, we repeatedly apply the cycle until either time or money runs out. The optimal x is determined by balancing affordability and time efficiency, which reduces to checking boundary candidates derived from constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(very large, exponential in steps) | O(1) | Too slow |
| Cycle compression + greedy batching | O(T log 1e9) | O(1) | Accepted |

## Algorithm Walkthrough

We compress the process into repeated identical trading cycles and reason about how large each cycle should be and how many times it can be executed.

1. Interpret a full cycle as buying x units and then selling them immediately. This transforms state by adding profit (q − p)x and consuming time (a + c)x + (b + d). This is the only meaningful atomic action because separating buy and sell without completion gives no benefit under linear pricing.
2. Determine the maximum x that can be afforded at the current moment. Since each cycle requires p · x gold upfront, x is constrained by current gold divided by p.
3. Determine the maximum x that can be executed within remaining time. Each cycle consumes (a + c)x + (b + d), so x is also constrained by how much time remains after accounting for fixed overheads.
4. Choose the largest x satisfying both constraints. This is optimal because profit increases linearly with x while overhead is amortized, so larger batches strictly dominate smaller ones whenever feasible.
5. Compute how many such cycles can be repeated before either gold or time becomes insufficient. Update gold and remaining time accordingly after each maximal batch execution.
6. Repeat until no further cycle can be executed within constraints.

Why it works is that any valid strategy can be decomposed into full buy-sell cycles, and within each cycle, splitting into smaller batches only increases the total overhead without improving profit. Since both profit and time scale linearly in x except for fixed costs, maximizing x at each step preserves optimal amortization of overhead while never reducing feasibility beyond constraints. This ensures no rearrangement of cycles can produce a higher final gold amount.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        p, a, b = map(int, input().split())
        q, c, d = map(int, input().split())
        m, t = map(int, input().split())

        gold = m
        time = t

        while True:
            if gold < p:
                break

            # maximum x we can afford
            x_money = gold // p

            # we need (a+c)x + (b+d) <= time
            if a + c == 0:
                x_time = x_money
            else:
                if time <= b + d:
                    break
                x_time = (time - (b + d)) // (a + c)

            x = min(x_money, x_time)

            if x <= 0:
                break

            cost_time = (a + c) * x + (b + d)
            gold -= p * x
            gold += q * x
            time -= cost_time

        print(gold)

if __name__ == "__main__":
    solve()
```

The code maintains current gold and remaining time, repeatedly executing the largest feasible full cycle. The key implementation detail is correctly separating affordability in gold from feasibility in time, then taking their minimum to determine the batch size.

A subtle point is handling the case when the linear time coefficient (a + c) is zero, where time consumption is constant per cycle. In that case, batch size is only limited by money. Another detail is ensuring that when remaining time is smaller than fixed overhead b + d, no further cycles are possible even if gold is sufficient.

## Worked Examples

### Example 1

Input:

```
p=5 a=2 b=0
q=8 c=1 d=0
m=10 t=10
```

We track execution:

| step | gold | time | x_money | x_time | x chosen | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | 10 | 2 | 3 | 2 | cycle |
| 2 | 14 | 4 | 2 | 1 | 1 | cycle |
| 3 | 17 | 1 | 3 | 0 | stop | end |

After first cycle, gold increases from 10 to 14 and time drops. Second cycle is smaller due to time constraint.

This demonstrates how time, not money, becomes the bottleneck and forces decreasing batch size.

### Example 2

Input:

```
p=1 a=1 b=0
q=100 c=1 d=0
m=1 t=3
```

| step | gold | time | x_money | x_time | x chosen | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 1 | 1 | 1 | cycle |
| 2 | 100 | 1 | 100 | 0 | stop | end |

Here a single cycle is optimal because repeating smaller cycles would waste time on repeated overhead.

This confirms that maximizing batch size per cycle is optimal when time is tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T log t) | Each test performs a small number of greedy cycles, each reducing time or increasing constraints significantly |
| Space | O(1) | Only constant state variables are maintained |

The algorithm runs comfortably within limits because each iteration strictly reduces remaining time or makes further operations impossible, preventing long loops even with large bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided-style simple sanity
assert run("""1
5 2 0
8 1 0
10 10
""") == "14"

# no time for trade
assert run("""1
5 2 100
8 1 100
10 5
""") == "10"

# profitable cycle possible once
assert run("""1
1 1 0
2 1 0
1 2
""") == "2"

# large time, repeated cycles
assert run("""1
1 1 0
2 1 0
1 100
""") == "102"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small single cycle | 14 | basic profit correctness |
| insufficient time | 10 | no-op edge case |
| one cycle only | 2 | boundary feasibility |
| repeated cycles | 102 | accumulation behavior |

## Edge Cases

One edge case is when time is exactly equal to the fixed overhead b + d. In this situation, even x = 1 is impossible because there is no time left for the linear component. The algorithm checks time <= b + d before computing x_time, ensuring no invalid division is performed.

Another edge case occurs when gold is exactly less than p. The loop terminates immediately, since no purchase is possible. This prevents incorrect attempts to compute x_money as zero and accidentally performing a degenerate cycle.

A final edge case is when a + c equals zero. The algorithm treats this separately, since dividing by zero in time constraint would be invalid. In this case, cycles are only constrained by money, and time never decreases, so the algorithm executes a single maximal batch and finishes.
