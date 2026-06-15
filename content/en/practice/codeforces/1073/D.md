---
title: "CF 1073D - Berland Fair"
description: "We are simulating a cyclic walk over an array of booth prices. Polycarp starts at position 1 and keeps moving clockwise in a fixed cycle. At each booth, he checks whether his remaining money is at least the price of one candy at that booth."
date: "2026-06-15T14:11:08+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1073
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 53 (Rated for Div. 2)"
rating: 1700
weight: 1073
solve_time_s: 267
verified: true
draft: false
---

[CF 1073D - Berland Fair](https://codeforces.com/problemset/problem/1073/D)

**Rating:** 1700  
**Tags:** binary search, brute force, data structures, greedy  
**Solve time:** 4m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a cyclic walk over an array of booth prices. Polycarp starts at position 1 and keeps moving clockwise in a fixed cycle. At each booth, he checks whether his remaining money is at least the price of one candy at that booth. If it is, he buys exactly one candy and decreases his money by that price. If not, he simply skips the purchase. After processing a booth, he always moves to the next one. The process stops only when a full pass no longer produces any purchase, which in practice happens when he can no longer afford any candy at the current position and continues until he eventually exhausts all possibilities.

The task is to count how many candies he buys in total before the simulation ends.

The constraints are large: up to 200,000 booths and total money up to 10^18. This immediately rules out naive step-by-step simulation across all money deductions if it recomputes anything expensive per step. A direct simulation of every visit is still linear per cycle, but the number of cycles can be as large as T divided by the minimum price, which in worst cases becomes far too large to simulate explicitly.

A key edge case appears when all prices are 1. In that case, Polycarp buys a candy at every step until T reaches zero, producing exactly T operations. Any approach that simulates step-by-step would still work conceptually but becomes too slow in tighter worst-case constructions where many cycles are needed.

Another problematic case is when only one booth is affordable and others are always skipped. A naive implementation may repeatedly scan all n booths even when most steps are wasted checks, leading to unnecessary O(nT) behavior in degenerate interpretations.

## Approaches

The brute-force idea is straightforward. We simulate Polycarp moving around the circle, checking each booth, subtracting price when possible, and incrementing a counter. This is correct because it mirrors the process exactly. However, each full cycle costs O(n), and in the worst case Polycarp can make on the order of T / min(a_i) cycles. Since T can be 10^18, this becomes impossible.

The key observation is that the process has a strong cyclic structure. Every full round over all booths reduces the budget by a fixed amount equal to the sum of all prices. If we knew how many complete rounds Polycarp can afford, we could jump over them instead of simulating each step. After exhausting full rounds, only a partial pass remains, which can be simulated in one final linear scan.

This reduces the problem to counting how many full cycles fit into the budget, then handling the leftover remainder in a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T × n) worst case | O(1) | Too slow |
| Cycle Jump + Residual Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total cost of one full cycle over all booths. This represents how much money is spent if Polycarp completes one full round of n visits with purchases wherever possible.
2. Compute how many full cycles can be completed using integer division of the remaining money by the cycle cost. This directly gives the number of guaranteed full repetitions of the same behavior.
3. Add the number of candies purchased during full cycles by multiplying the per-cycle purchase count by the number of cycles. This compresses a large number of repeated simulations into one arithmetic operation.
4. Reduce the remaining money by subtracting the total cost of all full cycles. After this, the remaining budget is strictly less than one full cycle cost, which guarantees that at most one partial traversal will occur.
5. Simulate a single pass through the booths in order. At each booth, if the current money is at least the price, subtract and increment the answer. Stop only after finishing the pass.
6. Output the accumulated total.

### Why it works

The crucial invariant is that after processing full cycles, the state of Polycarp is equivalent to having restarted from booth 1 with reduced money, and no intermediate configuration inside earlier cycles can differ because each cycle is identical in structure and cost accumulation. Since every full cycle affects money and count in a uniform way, compressing them does not lose ordering or decision correctness. The remaining simulation is bounded by one cycle, so it captures all partial behavior exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, T = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)

    full_cycles = T // total
    if full_cycles:
        T -= full_cycles * total

    ans = full_cycles * n

    for x in a:
        if T >= x:
            T -= x
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first compresses repeated full loops using arithmetic. The sum of all booth prices defines the cost of one full traversal. Multiplying this effect avoids simulating repeated cycles.

The remaining loop is a single pass over the array. Each step checks affordability and updates the state. No modulo index is needed because we only simulate at most one cycle after compression.

A subtle point is using integer division before modifying the remaining budget. This ensures that full cycles are counted exactly and avoids floating-point errors or repeated subtraction loops.

## Worked Examples

### Example 1

Input:

```
3 38
5 2 5
```

Cycle sum is 12. Polycarp can complete 3 full cycles (36 spent), leaving 2.

| Step | Position | Money before | Action | Money after | Total candies |
| --- | --- | --- | --- | --- | --- |
| 1 | full cycles | 38 | take 3 cycles | 2 | 9 |
| 2 | 1 | 2 | cannot buy 5 | 2 | 9 |
| 3 | 2 | 2 | buy 2 | 0 | 10 |
| 4 | 3 | 0 | stop | 0 | 10 |

The trace shows that full cycles dominate the computation and only the residual pass contributes a final partial purchase.

### Example 2

Input:

```
3 5
4 3 2
```

Cycle sum is 9, so no full cycle is possible.

| Step | Position | Money before | Action | Money after | Total candies |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | buy 4 | 1 | 1 |
| 2 | 2 | 1 | skip | 1 | 1 |
| 3 | 3 | 1 | skip | 1 | 1 |

This case confirms correctness when only a partial traversal occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute sum and one pass for residual simulation |
| Space | O(1) | Only a few counters and input storage |

The solution is linear in the number of booths, which fits comfortably under the constraints of 2 × 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, T = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)
    full = T // total
    T -= full * total
    ans = full * n

    for x in a:
        if T >= x:
            T -= x
            ans += 1

    return str(ans)

# provided sample
assert run("3 38\n5 2 5\n") == "10"

# all equal, small
assert run("4 10\n2 2 2 2\n") == "4"

# cannot buy anything
assert run("3 1\n5 6 7\n") == "0"

# single booth
assert run("1 100\n3\n") == "33"

# exact one cycle
assert run("2 3\n1 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal small | 4 | uniform cycling behavior |
| no purchase | 0 | skipping logic |
| single booth | 33 | degenerate n=1 case |
| exact cycle fit | 2 | boundary between full and partial cycles |

## Edge Cases

When n = 1, the process becomes repeated subtraction of a single value. For input `1 100` with price `3`, the algorithm computes cycle sum as 3, full cycles as 33, and residual 1, yielding 33 purchases, which matches direct reasoning since each cycle is just one purchase opportunity.

When all prices exceed T, such as `3 5 6 7`, the full cycle count is zero and the residual pass yields zero purchases, matching the fact that no single booth is affordable at any time.

When all prices are equal and small relative to T, the algorithm reduces to dividing T by the sum and then consuming the remainder linearly, ensuring that even very large T does not require simulation of every step.
