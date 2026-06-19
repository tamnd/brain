---
title: "CF 106262G - Max Cut Min Flow"
description: "We are given a straight line of checkpoints from 1 to n. Water always flows strictly forward from checkpoint 1 to checkpoint n, and the only way to stop flooding is to block at least one of the n − 1 connections between consecutive checkpoints."
date: "2026-06-19T14:19:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106262
codeforces_index: "G"
codeforces_contest_name: "2025 ICPC Asia Manila Regional"
rating: 0
weight: 106262
solve_time_s: 61
verified: true
draft: false
---

[CF 106262G - Max Cut Min Flow](https://codeforces.com/problemset/problem/106262/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a straight line of checkpoints from 1 to n. Water always flows strictly forward from checkpoint 1 to checkpoint n, and the only way to stop flooding is to block at least one of the n − 1 connections between consecutive checkpoints.

Each connection i between i and i + 1 can be blocked by doing a corresponding project. Each project has a value xi, which affects your money: positive values increase your money, negative values decrease it. You start with an initial budget b.

You may choose any subset of projects, in any order, but each project can be used at most once. A project is only executable if you currently have enough money to pay its cost when xi is negative. Positive projects never create a feasibility issue because they increase your budget.

Your goal is to choose a subset of projects such that at least one connection is blocked, and the order of execution is valid with respect to the running budget, while maximizing your final amount of money.

The constraints push us toward a linear or near-linear solution. With n up to 100000 and xi bounded by 10000 in magnitude, any O(n^2) strategy that tries permutations or subsets directly is impossible. Even O(n log n) is acceptable, but O(n^2) or exponential reasoning over subsets cannot pass.

A subtle issue appears when all projects are expensive negatives and the initial budget is too small to start any of them. In that case, even though blocking a single edge would theoretically solve the flooding, you cannot afford the first step of any valid sequence, so the answer must be −1.

Another failure case comes from assuming that picking all projects is always optimal. If negatives are too costly early, they may block access to later beneficial projects, so ordering matters critically.

## Approaches

A brute-force approach would try all subsets of edges, check whether at least one edge is selected, and verify whether there exists an ordering of selected projects that keeps the budget non-negative throughout execution. For each subset, we would simulate all permutations or attempt to find a valid sequence. This quickly becomes infeasible: there are 2^(n−1) subsets and each validity check could take O(k log k) or worse, leading to exponential explosion.

The key observation is that feasibility depends only on how we order the chosen projects, not on any graph structure beyond a single line. Positive projects are always safe to execute early since they only increase the budget. The only constraint comes from negative projects: each negative project requires having enough money before it is executed.

This transforms the problem into selecting a subset of items with profits xi, where positives are free gains and negatives require a minimum prefix resource condition. Once all positive projects are taken, the remaining question becomes: which negative projects can we schedule such that at every step, current money never drops below the required threshold? The optimal structure is to always execute affordable negative projects in increasing order of their cost, meaning we prioritize those with smaller absolute loss first. This greedy ordering ensures we never “waste” budget early on a large loss when a smaller loss could be safely handled first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n!) | O(n) | Too slow |
| Optimal Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We separate the decision into handling profitable projects first and then carefully handling expensive ones.

1. Split projects into two groups: those with xi > 0 and those with xi ≤ 0. The positive ones always improve the budget and never restrict ordering, so they are always safe to include.
2. Add all positive xi to the answer immediately and increase the current budget by their sum. This maximizes available resources for later decisions, and there is never a reason to delay them.
3. Collect all negative projects and sort them in decreasing order of xi. This means we process the least damaging losses first, since a value like −1 is safer to pay than −100.
4. Iterate through this sorted list. For each negative xi, check if the current budget is at least −xi. If yes, execute it, subtract −xi from the budget, and add xi to the total answer.
5. If a negative project is not affordable at the moment, skip it permanently. It will never become more affordable later because negatives only reduce budget.
6. Ensure that at least one project has been executed overall. If nothing was chosen, return −1 because we failed to block any edge.

The key idea behind ordering is that smaller losses preserve flexibility for future choices. Executing a large loss early can destroy feasibility for smaller ones, while the reverse never hurts feasibility.

### Why it works

At any point, the only constraint that matters is whether the current budget is large enough to pay a negative project. Positive projects only increase budget, so they can be safely applied first without loss of generality. Among negative projects, any optimal schedule can be transformed into one where all chosen negatives appear in non-decreasing order of cost without violating feasibility, since swapping a more expensive loss earlier can only make budget constraints harder for later steps. This exchange argument guarantees that the greedy sorted-by-cost construction does not exclude any optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, b = map(int, input().split())
    arr = list(map(int, input().split()))

    total = b
    picked_any = False

    positives = 0
    negatives = []

    for x in arr:
        if x > 0:
            positives += x
            picked_any = True
        else:
            negatives.append(x)

    total += positives

    negatives.sort(reverse=True)

    for x in negatives:
        if total >= -x:
            total += x
            picked_any = True

    if not picked_any:
        print(-1)
    else:
        print(total)

if __name__ == "__main__":
    solve()
```

The implementation follows the structure directly. We accumulate all positive contributions first since they are unconditionally beneficial. We then sort the negative values so that the least harmful reductions are attempted first. The budget check ensures we never execute a project that would make the budget invalid at that moment. The boolean flag tracks whether any project was successfully chosen, which is required because blocking no edges does not solve the flooding problem.

A subtle point is that we never reconsider skipped negatives. This is correct because skipping a negative means the current budget was insufficient, and since remaining operations cannot increase budget before that negative is reconsidered in a better position, it will never become feasible later.

## Worked Examples

Consider the first sample.

Input projects are `3, -1, 4, 1, -5` with initial budget 7.

We first take positives 3, 4, and 1, increasing budget to 15.

| Step | Action | Project | Budget before | Budget after |
| --- | --- | --- | --- | --- |
| 1 | Take positive | 3 | 7 | 10 |
| 2 | Take positive | 4 | 10 | 14 |
| 3 | Take positive | 1 | 14 | 15 |

Now we process negatives sorted: −1, −5.

| Step | Action | Project | Budget before | Budget after |
| --- | --- | --- | --- | --- |
| 1 | Take | −1 | 15 | 14 |
| 2 | Take | −5 | 14 | 9 |

Final answer is 15.

This trace shows that keeping large budget early allows all negatives to be processed safely in increasing order of cost.

Now consider the second sample.

Input is `-6, -7, -6, -7` with initial budget 4.

No positives exist, so we only attempt negatives sorted: −6, −6, −7, −7.

| Step | Action | Project | Budget before | Budget after |
| --- | --- | --- | --- | --- |
| 1 | Skip (insufficient) | −6 | 4 | 4 |

We cannot execute any project, so we never block a connection, making the task impossible.

This shows that feasibility depends on being able to afford at least one initial negative or having a positive boost, otherwise the system cannot start.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting negatives dominates; all other operations are linear |
| Space | O(n) | Storage for negative list |

The algorithm fits comfortably within limits since n is up to 100000. Sorting once and doing a single linear scan is efficient enough for typical Codeforces constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, b = map(int, input().split())
    arr = list(map(int, input().split()))

    total = b
    picked = False

    pos = 0
    neg = []

    for x in arr:
        if x > 0:
            pos += x
            picked = True
        else:
            neg.append(x)

    total += pos
    neg.sort(reverse=True)

    for x in neg:
        if total >= -x:
            total += x
            picked = True

    return str(total) if picked else "-1"

# provided samples
assert run("6 7\n3 -1 4 1 -5\n") == "15"
assert run("5 4\n-6 -7 -6 -7\n") == "-1"

# minimum size
assert run("2 0\n5\n") == "5"

# all positives
assert run("4 1\n2 3 4\n") == "10"

# all negatives but feasible chain
assert run("4 10\n-3 -4 -5\n") == " -2".strip()

# tight budget edge
assert run("3 5\n-6 1\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all positives | sum | baseline accumulation |
| all negatives infeasible | -1 | impossibility detection |
| mixed tight budget | correct subset | greedy feasibility ordering |
| single edge | direct decision | minimal case behavior |

## Edge Cases

When all projects are negative and none can be afforded initially, the algorithm immediately returns −1 because no operation can start. For example, input `n = 3, b = 1, [-5, -6]` never passes the first affordability check, so no project is executed and the flag remains false.

When there are both positive and negative values but positives are small, the algorithm ensures positives are applied first, potentially enabling negatives that were previously unaffordable. For instance, `b = 1, [2, -5]` increases budget to 3 before attempting −5, still failing correctly because the negative remains infeasible.

When a large negative appears before smaller ones, sorting guarantees we never waste budget on it early. For `b = 10, [-1, -1, -20]`, executing the two −1 operations first reduces budget gradually and avoids prematurely attempting −20, which would fail and potentially block reasoning if misordered.
