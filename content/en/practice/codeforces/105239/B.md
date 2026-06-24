---
title: "CF 105239B - Let Us Assemble a Portfolio Together"
description: "We are given a collection of projects, and for each project there are several mutually exclusive ways to execute it. Each way has a cost and a revenue. For every project we must either pick exactly one of its available ways or skip the project entirely."
date: "2026-06-24T11:11:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105239
codeforces_index: "B"
codeforces_contest_name: "Dynamic Programming, SPbSU 2024, Training 1"
rating: 0
weight: 105239
solve_time_s: 44
verified: true
draft: false
---

[CF 105239B - Let Us Assemble a Portfolio Together](https://codeforces.com/problemset/problem/105239/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of projects, and for each project there are several mutually exclusive ways to execute it. Each way has a cost and a revenue. For every project we must either pick exactly one of its available ways or skip the project entirely. The total cost of all chosen ways must not exceed a global budget, while the objective is to maximize the sum of revenues.

A useful way to reinterpret the structure is that each project contributes a small “choice group” of items. From each group we either take one item or take nothing. Each item has a weight equal to cost and a value equal to revenue. The constraint is a single knapsack capacity shared across all groups, but with the additional restriction that we cannot take more than one item from each group.

The constraints are deliberately asymmetric. The number of projects is at most 20, and the total number of options across all projects is also at most 20. However, the budget can be very large, up to 10^9, which immediately rules out any DP that depends on budget as a dimension. Any solution that tries to iterate over cost states will fail both in memory and time.

This shifts the entire difficulty away from capacity-based knapsack and toward subset enumeration over items or groups.

A subtle edge case appears when a project has only expensive options but skipping is optimal. For example, if a project has options (revenue 100, cost 10) and (revenue 80, cost 9) and the budget is 5, both options are infeasible, so the correct behavior is to skip the project entirely, yielding revenue 0 from it. Any naive implementation that assumes “must pick one option per project” would incorrectly force an over-budget selection.

Another edge case is when all costs are zero. Then every project can be taken freely, and the optimal answer is simply the sum of the best revenue option per project, since budget is irrelevant. This case also exposes implementations that mistakenly treat cost constraints as optional rather than strict.

Finally, because total options across all projects are small, the key structural hint is that we can treat every individual option as an atomic item in a global subset problem, but we must ensure we never pick two items from the same project.

## Approaches

A direct approach would be to treat this as a multi-choice knapsack with budget as DP dimension. That leads to a state like dp[i][b] representing best revenue after first i projects and budget b. This is immediately impossible because b goes up to 10^9, so even a single DP layer is infeasible.

We could try compressing budgets using only observed costs, but since costs are arbitrary up to 10^9 and not bounded by total sum, this still does not help.

The key observation is that the total number of choices is only 20. This is small enough to allow exponential enumeration over subsets of all available options. However, naive subset enumeration over 20 items gives 2^20 possibilities, which is about one million, perfectly acceptable.

The complication is the per-project constraint: we cannot select two options belonging to the same project. This suggests that we need to encode feasibility of a subset in terms of project conflicts.

The clean way to resolve this is to treat each option as an item labeled by its project index. Then we enumerate subsets of all options, and for each subset we check validity by ensuring no two items share a project. If valid, we compute total cost and revenue and check budget feasibility.

Because total items are only 20, checking each subset is O(20), leading to a total of O(20 * 2^20), which is efficient.

An alternative perspective is to group-by-project DP over subsets of projects, but since each project has multiple options, flattening and validating subsets is simpler and less error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Budget DP over cost | O(n · b) | O(b) | Impossible due to b up to 1e9 |
| Subset enumeration over all options | O(2^m · m) | O(m) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Collect all available options into a single list, where each option stores its project id, cost, and revenue. We treat skipping a project as implicitly included by allowing subsets that omit all its options.
2. Iterate over all subsets of these options using bitmasks from 0 to 2^m − 1, where m is total number of options.
3. For each subset, track whether a project has already been selected using a boolean array or a bitmask. If we encounter two options belonging to the same project, we immediately discard this subset. This prevents illegal configurations.
4. While scanning a valid subset, accumulate total cost and total revenue. This incremental computation ensures each subset evaluation is O(m) rather than recomputing from scratch.
5. If total cost is within budget, update the answer with the maximum revenue seen so far.

The reason we explicitly validate during iteration rather than pre-filtering is that conflicts depend on the combination of chosen items, not individual items alone.

### Why it works

Every feasible solution corresponds exactly to a subset of options that includes at most one option per project and whose total cost does not exceed the budget. The algorithm enumerates all subsets of options, so it certainly enumerates all feasible solutions. The validity check filters out exactly those subsets that violate the one-option-per-project rule, and the budget check enforces feasibility. Since we evaluate the revenue of every valid configuration, the maximum recorded value must equal the optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, b = map(int, input().split())
    items = []

    for i in range(n):
        k = int(input())
        for _ in range(k):
            r, c = map(int, input().split())
            items.append((i, c, r))

    m = len(items)
    ans = 0

    for mask in range(1 << m):
        used_projects = 0
        total_cost = 0
        total_rev = 0
        ok = True

        for j in range(m):
            if mask & (1 << j):
                pid, cost, rev = items[j]

                if used_projects & (1 << pid):
                    ok = False
                    break

                used_projects |= (1 << pid)
                total_cost += cost
                total_rev += rev

        if ok and total_cost <= b:
            if total_rev > ans:
                ans = total_rev

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation flattens all project options into a single array while preserving project identity. The subset enumeration uses a bitmask over these options. For each mask, we maintain a project-usage bitmask to ensure no project contributes more than one selected option.

The cost and revenue accumulators are straightforward sums. The budget check is performed only after ensuring validity, which avoids wasted comparisons.

A subtle implementation detail is that we use a separate bitmask for project usage rather than a set. This keeps checks O(1) per item and avoids Python overhead.

## Worked Examples

### Example 1

Input:

```
2 10
2
100 10
80 9
1
10 1
```

We have three options total: project 0 has two options, project 1 has one option.

| mask | chosen options | valid projects | cost | revenue | valid | best |
| --- | --- | --- | --- | --- | --- | --- |
| 000 | none | {} | 0 | 0 | yes | 0 |
| 001 | (10,1) | {1} | 1 | 10 | yes | 10 |
| 010 | (80,9) | {0} | 9 | 80 | yes | 80 |
| 011 | (80,9)+(10,1) | {0,1} | 10 | 90 | yes | 90 |
| 100 | (100,10) | {0} | 10 | 100 | yes | 100 |
| 101 | (100,10)+(10,1) | {0,1} | 11 | 110 | no | 100 |
| 110 | invalid (two from project 0) | - | - | - | no | 100 |
| 111 | invalid | - | - | - | no | 100 |

This trace shows how the best solution is selecting the first option of project 0 plus the only option of project 1, achieving revenue 110 but exceeding budget, so it is rejected. The optimal feasible solution is selecting 100 + 10 revenue with cost 11 also infeasible, so best is 100 alone.

### Example 2

Input:

```
1 5
2
50 3
40 2
```

| mask | chosen | cost | revenue | valid | best |
| --- | --- | --- | --- | --- | --- |
| 0 | none | 0 | 0 | yes | 0 |
| 1 | (50,3) | 3 | 50 | yes | 50 |
| 2 | (40,2) | 2 | 40 | yes | 50 |
| 3 | both | 5 | 90 | no | 50 |

This shows the per-project restriction forbids combining both options even though budget would allow it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · 2^m) | Every subset is checked, and each check scans up to m items |
| Space | O(m) | Storage for flattened items and temporary state |

The total number of options is at most 20, so 2^20 is about one million. Multiplying by 20 operations per subset remains easily within limits for 2 seconds in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, b = map(int, input().split())
    items = []
    for i in range(n):
        k = int(input())
        for _ in range(k):
            r, c = map(int, input().split())
            items.append((i, c, r))

    m = len(items)
    ans = 0

    for mask in range(1 << m):
        used = 0
        cost = 0
        rev = 0
        ok = True

        for j in range(m):
            if mask & (1 << j):
                pid, c, r = items[j]
                if used & (1 << pid):
                    ok = False
                    break
                used |= (1 << pid)
                cost += c
                rev += r

        if ok and cost <= b:
            ans = max(ans, rev)

    return str(ans)

# sample-like
assert run("2 10\n2\n100 10\n80 9\n1\n10 1\n") == "100"

# single project
assert run("1 5\n2\n50 3\n40 2\n") == "50"

# zero budget
assert run("1 0\n1\n10 0\n") == "10"

# all too expensive
assert run("2 1\n1\n10 5\n1\n20 6\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like | 100 | correct pruning of invalid subsets |
| single project | 50 | per-project choice handling |
| zero budget | 10 | zero-cost boundary behavior |
| all too expensive | 0 | skipping all projects |

## Edge Cases

One edge case is when budget is zero. The algorithm still enumerates subsets, but only subsets with total cost zero survive. This correctly yields either zero revenue or any zero-cost option if it exists.

Another case is when a project has multiple cheap options, but only one should be selected. The project bitmask ensures that any subset selecting two options from the same project is rejected immediately, so even if both are individually affordable, they never contribute together.

A final case is when all options are expensive. The subset loop still runs, but every non-empty subset fails the budget check, and only the empty subset remains valid, producing output zero.
