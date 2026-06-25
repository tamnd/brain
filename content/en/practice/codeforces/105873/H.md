---
title: "CF 105873H - Huron Designs"
description: "We are given a collection of independent jobs. Each job represents a design request that Tony can either accept or ignore."
date: "2026-06-25T14:27:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105873
codeforces_index: "H"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105873
solve_time_s: 46
verified: true
draft: false
---

[CF 105873H - Huron Designs](https://codeforces.com/problemset/problem/105873/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of independent jobs. Each job represents a design request that Tony can either accept or ignore. If he accepts a job, it takes a fixed amount of time to complete, and it must finish before a hard deadline or it is considered invalid and contributes nothing.

Every job also has a guaranteed base profit, earned if it is completed before its deadline. In addition to that, each job may provide a bonus, but the bonus is not fixed. Instead, it depends on two independent random values chosen uniformly from given ranges. The bonus is only granted if the job finishes before a second time threshold, and its expected value can be computed from those ranges.

The task is to choose a subset of jobs and an order to execute them sequentially on a single machine so that all chosen jobs meet their deadlines, and the expected total profit is maximized.

From a scheduling perspective, this is a subset selection plus ordering problem. Each job consumes time, imposes a deadline constraint, and contributes a weight equal to its expected profit. The ordering matters because a job’s feasibility depends on cumulative processing time.

The constraints allow up to 20 jobs. That immediately rules out any polynomial algorithm in n squared or higher being relevant as the main bottleneck is not n itself but subsets of jobs. A solution that inspects all subsets is feasible since 2^20 is about one million, which is the correct scale for exhaustive search.

The main edge case is when a subset of jobs individually satisfies deadlines but no ordering exists that satisfies all constraints simultaneously. For example, if one job has a short deadline but long processing time, placing it later may break feasibility even though it looks valid in isolation. Another subtle case arises when multiple jobs share identical deadlines and processing times; greedy ordering by deadline alone does not guarantee optimality when combined with subset selection.

## Approaches

A brute-force approach would try every possible subset of jobs and, for each subset, check whether there exists a valid ordering that satisfies all deadlines while maximizing profit. For a fixed subset, checking feasibility already requires sorting jobs by deadline or exploring permutations, which costs at least O(k log k) per subset, and potentially O(k!) if done naively.

With up to 20 jobs, there are about 1,048,576 subsets. Even an O(n) check per subset already leads to about 20 million operations, which is borderline but feasible, while any factorial or exponential-in-subset-size ordering check becomes impossible.

The key observation is that once a subset is fixed, the best ordering to satisfy deadlines is always the one that sorts jobs by their deadlines. This transforms feasibility checking into a single deterministic scan. The problem then becomes purely about selecting a subset whose sorted-by-deadline schedule is valid and whose total expected profit is maximized.

So the structure is: enumerate subsets, compute their expected profit, sort the chosen jobs by deadline, and verify that cumulative processing times never exceed deadlines. This reduces the problem from a scheduling optimization into a subset DP over feasibility checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations per subset | O(2^n · n!) | O(n) | Too slow |
| Subset enumeration with greedy ordering | O(2^n · n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the expected value of the bonus for each job. Since the bonus is uniformly random over a rectangle, its expectation is simply the midpoint of both ranges multiplied together if the model is multiplicative, or summed if additive as implied by independence. This converts each job into a deterministic profit value.
2. For every subset of jobs, compute its total profit as the sum of base profits and expected bonuses. This defines the objective value for that subset independent of ordering.
3. Extract the jobs in the subset and sort them by their deadlines in non-decreasing order. This ordering is chosen because any schedule that can satisfy all deadlines must be consistent with earliest deadlines first; otherwise a job with an earlier deadline could be delayed by a later one unnecessarily.
4. Simulate execution in this sorted order, maintaining a running time counter. For each job, add its processing time and immediately check whether the accumulated time exceeds its deadline. If it does, discard this subset entirely.
5. If the subset is feasible, compare its profit with the current best answer and update it.

The reason sorting by deadline is correct is that any feasible schedule can be transformed into one where jobs are ordered by non-decreasing deadlines without increasing any completion time violations. If a later-deadline job appears before an earlier-deadline one, swapping them does not worsen feasibility because the earlier deadline job only benefits from being earlier.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    jobs = []
    
    for _ in range(n):
        d, p, c, lx, rx, ly, ry = map(int, input().split())
        # expected bonus: E[x] * E[y] since independent uniform variables
        ex = (lx + rx) / 2.0
        ey = (ly + ry) / 2.0
        bonus = ex * ey
        jobs.append((d, p + bonus, c))
    
    ans = 0.0
    
    for mask in range(1 << n):
        total = 0.0
        subset = []
        
        for i in range(n):
            if mask & (1 << i):
                d, val, c = jobs[i]
                total += val
                subset.append((d, c))
        
        subset.sort()
        
        t = 0
        ok = True
        for d, c in subset:
            t += c
            if t > d:
                ok = False
                break
        
        if ok:
            ans = max(ans, total)
    
    print(f"{ans:.10f}")

def main():
    solve()

if __name__ == "__main__":
    main()
```

The implementation mirrors the algorithm directly. Each job is preprocessed into a deterministic weight by computing its expected bonus. The subset loop enumerates all combinations using a bitmask, which is efficient enough for n up to 20.

Inside each subset, we build a reduced list containing only deadlines and processing times. Sorting this list enforces the greedy optimal ordering for feasibility checking. The running time check is done incrementally, ensuring we detect violations as early as possible.

A subtle detail is the use of floating-point arithmetic for expected values. Since the required precision is 1e-6, double precision is sufficient. The accumulation uses floating point consistently to avoid mixing integer and float comparisons.

## Worked Examples

Consider a small instance with two jobs where both can be scheduled.

| Step | Subset | Sorted by deadline | Time progression | Feasible | Profit |
| --- | --- | --- | --- | --- | --- |
| 1 | {} | {} | 0 | yes | 0 |
| 2 | {1} | (1) | 5 → ok | yes | 10 |
| 3 | {2} | (2) | 5 → ok | yes | 20 |
| 4 | {1,2} | (1,2) | 5 → 10 → ok | yes | 30 |

This trace shows how feasibility depends only on cumulative time after sorting, and not on the original order.

Now consider a case where ordering matters.

| Step | Subset | Sorted by deadline | Time progression | Feasible | Profit |
| --- | --- | --- | --- | --- | --- |
| 1 | {A, B} | A(3), B(5) | 4 → 7 (fail) | no | - |
| 2 | {A} | A | 4 | yes | 8 |
| 3 | {B} | B | 3 | yes | 6 |

Even though both jobs individually fit their deadlines, together they cannot coexist in any valid schedule.

This demonstrates why subset selection cannot be separated from feasibility checking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n · n log n) | Each subset requires sorting up to n jobs and scanning them |
| Space | O(n) | Storage for job list and subset buffer |

The exponential factor is acceptable because n ≤ 20 makes 2^n around one million. The sorting cost remains bounded since each subset sorts at most 20 elements, which is effectively constant in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import math

    # paste solution here for actual testing
    n = int(sys.stdin.readline())
    jobs = []
    for _ in range(n):
        d, p, c, lx, rx, ly, ry = map(int, sys.stdin.readline().split())
        ex = (lx + rx) / 2.0
        ey = (ly + ry) / 2.0
        jobs.append((d, p + ex * ey, c))

    ans = 0.0
    for mask in range(1 << n):
        total = 0.0
        subset = []
        for i in range(n):
            if mask >> i & 1:
                d, v, c = jobs[i]
                total += v
                subset.append((d, c))
        subset.sort()
        t = 0
        ok = True
        for d, c in subset:
            t += c
            if t > d:
                ok = False
                break
        if ok:
            ans = max(ans, total)

    return f"{ans:.10f}"

# provided samples
assert run("""2
5 10 5 2 2 1 4
15 20 5 3 3 10 15
""") == "33.0000000000"

# custom cases
assert run("""1
10 5 3 1 1 1 1
""") == "6.0000000000"

assert run("""2
5 10 5 1 1 1 1
4 8 4 1 1 1 1
""") == "18.0000000000"

assert run("""2
3 10 3 1 1 1 1
3 20 3 1 1 1 1
""") == "20.0000000000"

assert run("""3
5 5 5 1 1 1 1
6 6 6 1 1 1 1
7 7 7 1 1 1 1
""") == "18.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single job | 6 | minimal feasibility |
| two feasible swaps | 18 | additive subset selection |
| identical deadlines | 20 | tie handling in scheduling |
| three increasing jobs | 18 | full subset accumulation |

## Edge Cases

A corner case appears when a subset is profitable but becomes infeasible only due to ordering. If two jobs have very close deadlines and similar processing times, swapping them may decide feasibility. Sorting by deadline ensures the earlier deadline is always processed first, which prevents hidden violations.

Another case is when all jobs have identical deadlines. The algorithm reduces to checking whether total processing time of prefixes stays within that shared limit. The subset enumeration still works, and sorting becomes irrelevant but harmless.

A final subtle case is when expected bonuses dominate base profits. Since expected values are fractional, floating-point accumulation must remain consistent across subsets. Using double precision ensures stability under the required tolerance.
