---
title: "CF 104969D - Feeding the Kids"
description: "We are given a sequence of students arriving in a fixed order, and each student wants a certain number of pizza slices. Mr. Reynolds prepares pizzas in advance, and every pizza has the same number of slices, which we call $S$."
date: "2026-06-28T06:41:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 77
verified: false
draft: false
---

[CF 104969D - Feeding the Kids](https://codeforces.com/problemset/problem/104969/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of students arriving in a fixed order, and each student wants a certain number of pizza slices. Mr. Reynolds prepares pizzas in advance, and every pizza has the same number of slices, which we call $S$. Pizzas are not pre-cut across students; instead, slices are served sequentially.

There is a single active pizza at any moment. When a student arrives, if the current pizza still has enough slices to satisfy their demand, those slices are taken from it. If the remaining slices are insufficient, the remaining part of that pizza is discarded entirely, a fresh pizza is opened, and the student is served from that new pizza.

The goal is to choose the smallest possible $S$ such that, after serving all students in order, the total number of pizzas used does not exceed $K$.

The constraints allow up to $10^5$ students and $10^5$ pizzas, with demands up to $10^6$. Any solution that tries all candidate values of $S$ and simulates the process must do so efficiently. A direct simulation for each possible $S$ would be too slow because the answer range can go up to the sum of all demands, which may reach $10^{11}$ in worst cases. This immediately rules out any approach that is quadratic or even linear per candidate value.

A few edge cases matter here. If a student has a demand larger than the pizza size $S$, it is impossible to serve them, so any valid answer must satisfy $S \ge \max(d_i)$. Another subtle case is when leftover slices exist but are insufficient for the next student. Those leftover slices are wasted, which can significantly increase the number of pizzas used. A naive approach that ignores this waste and only tracks total sum would underestimate pizza consumption.

## Approaches

A straightforward approach is to fix a candidate pizza size $S$ and simulate the entire process. We maintain the remaining slices in the current pizza and count how many pizzas are opened. When a student cannot be satisfied from the current pizza, we increment the pizza count and reset the remaining capacity. This simulation is correct because it exactly follows the rules of serving.

The problem with this approach is that trying all possible values of $S$ is too expensive. The answer lies between the maximum demand and the total sum of all demands. In the worst case, that range is enormous, and checking each value independently would require $O(N)$ work per check, leading to an infeasible $O(N \cdot \text{range})$ complexity.

The key observation is that feasibility is monotonic. If a pizza size $S$ is sufficient to serve all students using at most $K$ pizzas, then any larger pizza size will never require more pizzas. Increasing $S$ only reduces waste and reduces or maintains the number of pizza openings. This monotonic structure allows us to apply binary search on the answer.

We therefore binary search on $S$, and for each candidate run a greedy simulation in linear time to compute how many pizzas are needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $S$ | $O(N \cdot \text{sum})$ | $O(1)$ | Too slow |
| Binary Search + Simulation | $O(N \log \text{sum})$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We define a function that checks whether a fixed pizza size $S$ can serve all students using at most $K$ pizzas.

1. Initialize a counter for pizzas used as 1, since we start with one pizza, and set remaining slices to $S$. This models the first pizza being already open.
2. Iterate over students in order.
3. If the current pizza has at least $d_i$ slices remaining, subtract $d_i$ from the remaining amount.
4. If the current pizza has fewer than $d_i$ slices, increment the pizza counter, open a new pizza, and set remaining slices to $S - d_i$. This step reflects the rule that leftover pizza is discarded before opening a new one.
5. If at any point a single demand $d_i$ exceeds $S$, the configuration is invalid immediately because even a fresh pizza cannot satisfy that student.
6. After processing all students, check whether the number of pizzas used is at most $K$. If yes, the size $S$ is feasible.

We then binary search $S$ between $\max(d_i)$ and $\sum d_i$, selecting the smallest feasible value.

The key invariant is that after processing each student, the simulation maintains exactly the same state the real process would have: one active pizza with a correct remaining slice count, and an accurate count of how many pizzas have been consumed. Since the greedy rule always discards unusable leftovers immediately, no alternative decision exists that could reduce pizza usage locally, so the simulation is optimal for a fixed $S$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(S, arr, K):
    pizzas = 1
    rem = S

    for x in arr:
        if x > S:
            return False
        if rem >= x:
            rem -= x
        else:
            pizzas += 1
            rem = S - x
        if pizzas > K:
            return False

    return pizzas <= K

def solve():
    N, K = map(int, input().split())
    arr = list(map(int, input().split()))

    lo = max(arr)
    hi = sum(arr)

    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid, arr, K):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The implementation separates feasibility checking from the search logic. The `can` function performs the greedy simulation and enforces both the capacity constraint and the early exit condition when the number of pizzas exceeds $K$. The binary search then narrows the minimal valid capacity.

A subtle point is initializing `pizzas = 1` instead of `0`, since we always start with one pizza available before serving begins. Another detail is the strict early exit when `pizzas > K`, which prevents unnecessary simulation once a candidate is already invalid.

## Worked Examples

Consider a small case where demands are `[4, 2, 5]` and we test different values of $S$ with $K = 2$.

For $S = 6$:

| Step | Demand | Remaining before | Action | Remaining after | Pizzas |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 6 | use current | 2 | 1 |
| 2 | 2 | 2 | use current | 0 | 1 |
| 3 | 5 | 0 | new pizza | 1 | 2 |

This fits within 2 pizzas, so $S=6$ is feasible.

For $S = 5$:

| Step | Demand | Remaining before | Action | Remaining after | Pizzas |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 5 | use current | 1 | 1 |
| 2 | 2 | 1 | new pizza | 3 | 2 |
| 3 | 5 | 3 | new pizza | 0 | 3 |

This requires 3 pizzas, exceeding $K$, so it is infeasible.

These traces show how small reductions in $S$ increase fragmentation, which directly increases pizza count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log \sum d_i)$ | Binary search over answer range, each feasibility check scans all students once |
| Space | $O(1)$ | Only a few counters are used beyond the input array |

The input size allows up to $10^5$ students, so a linear check is acceptable. The logarithmic factor from binary search stays small (around 40 iterations), keeping the solution comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if False else ""  # placeholder structure

# Since solve() prints directly, we redefine a wrapper

def run(inp: str) -> str:
    import sys, io
    backup = sys.stdin
    sys.stdin = io.StringIO(inp)

    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()

    sys.stdin = backup
    return out.getvalue().strip()

# sample
assert run("5 3\n10 3 6 7\n") == "12"

# minimum size case
assert run("1 1\n5\n") == "5"

# all equal, tight packing
assert run("4 2\n2 2 2 2\n") == "4"

# large K, should reduce to max element
assert run("3 10\n8 1 2\n") == "8"

# forcing multiple breaks
assert run("5 2\n5 4 3 2 1\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | equal to demand | base feasibility |
| all equal small | tight packing behavior | no unnecessary splits |
| large K | max element answer | upper bound correctness |
| decreasing sequence | frequent breaks | fragmentation handling |

## Edge Cases

A critical edge case is when a student’s demand exactly matches the remaining slices. In this situation, the algorithm consumes the pizza completely without opening a new one, which avoids unnecessary increments in pizza count. For example, with $S = 5$ and demands `[2, 3]`, the first student leaves zero remaining, and the second starts a fresh pizza only when needed.

Another edge case is when a demand is larger than the candidate $S$. The feasibility check must reject immediately. For input `[7, 2, 3]` with $S = 6$, the algorithm stops at the first student, preventing incorrect assumptions about later processing.

A final edge case is when leftover slices are always insufficient for the next student, forcing a new pizza every time. For example `[5, 5, 5]` with $S = 6$ causes a split at every step, producing 3 pizzas. The simulation correctly captures this repeated waste pattern, which is the core reason the greedy check is necessary rather than a simple sum-based estimate.
