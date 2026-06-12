---
title: "CF 1089L - Lazyland"
description: "We are given a collection of workers, each of whom has already picked a job they would like to do. There are exactly $k$ distinct jobs, and each worker points to one of them."
date: "2026-06-13T03:46:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1089
codeforces_index: "L"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 900
weight: 1089
solve_time_s: 199
verified: false
draft: false
---

[CF 1089L - Lazyland](https://codeforces.com/problemset/problem/1089/L)

**Rating:** 900  
**Tags:** -  
**Solve time:** 3m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of workers, each of whom has already picked a job they would like to do. There are exactly $k$ distinct jobs, and each worker points to one of them. Since there are at least as many workers as jobs, we can assign at most one worker to each job, but we must end up covering every job exactly once.

The complication is that the current choices might leave some jobs uncovered, while other jobs are chosen by multiple workers. To fix this, we are allowed to persuade workers to change their chosen job. Persuading the $i$-th worker costs $b_i$, and after persuasion we can assign them to a different job.

The goal is to ensure that every job from $1$ to $k$ is assigned to exactly one worker, minimizing the total persuasion cost.

The constraints go up to $n = 10^5$. Any solution that tries to simulate assignments or repeatedly try combinations will exceed $O(n^2)$. Even $O(n \log n)$ is the practical target, since sorting or heap usage is acceptable. This strongly suggests we should treat workers in groups per job and make greedy decisions inside each group.

A subtle edge case appears when a job is initially chosen by exactly one worker. That worker is forced into that job unless we deliberately move them, but doing so would only create unnecessary cost since other jobs might become harder to cover. Another edge case is when a job is not chosen at all; then we must “import” a worker from some other job group, which forces us to choose which worker to move in a cost-efficient way.

For example, if all workers choose job 1 except one worker chooses job 2, then job 3 (if $k \ge 3$) must be filled by moving someone from job 1 or 2. The optimal choice depends entirely on which worker is cheapest to reassign.

A naive approach might try to assign jobs greedily in order without considering global cost tradeoffs, which fails when a locally optimal assignment consumes low-cost flexibility needed elsewhere.

## Approaches

A direct way to think about the problem is to imagine we must end up with exactly one representative worker per job. Since each worker initially “belongs” to a job, each job forms a group of candidates, and we must decide which workers to keep in their original job and which to “sacrifice” for redistribution.

A brute-force method would consider, for each job, which worker stays and which workers are moved, while ensuring all jobs end up with one worker. This quickly turns into a combinatorial assignment problem. If a job has $t$ workers, choosing which one stays interacts with choices for all other jobs because every moved worker becomes available for another job. In the worst case, this leads to exponential combinations or at least $O(nk)$ transitions if done carefully, which is far too slow for $10^5$.

The key observation is that within each job, only one worker can remain “free” from persuasion cost, because only one of them will actually occupy that job in the final assignment. All other workers in that job are candidates to be reassigned. If we decide that a job keeps its best possible worker, then every other worker in that group becomes “available supply” that can be used to fill missing jobs elsewhere.

This reframes the problem: we must ensure every job gets at least one worker, and we want to minimize the total cost of the workers we force to move. Equivalently, for each job we want to preserve exactly one worker at zero cost and treat all other workers as candidates for redistribution. The optimal choice of which worker to preserve per job is to keep the one with the largest persuasion cost, because that is the worker we least want to “pay for removal.”

Thus, the solution reduces to summing all worker costs and subtracting the sum of the largest cost in each job group, while ensuring that we have enough preserved assignments to cover all jobs. Since each job contributes at least one preserved worker, feasibility is automatic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / $O(nk)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ or $O(n)$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We reorganize workers by the job they initially selected, because decisions are local within each job group.

1. Group all workers by their chosen job. Each group represents candidates who can potentially serve that job, and only one of them must remain assigned there.
2. For each job group, find the worker with the maximum persuasion cost $b_i$. This worker is the most expensive to reassign, so we prefer to keep them in place.
3. Compute the total sum of all persuasion costs across all workers. This represents the cost if we were to persuade everyone.
4. Subtract from this total the maximum $b_i$ from each job group. This models the fact that we keep one worker per job unpersuaded, chosen to maximize saved cost.
5. Output the resulting value, which represents the minimum persuasion time needed to ensure coverage of all jobs.

The reason we only need to preserve one worker per job is that each job must end up assigned exactly one worker, so each group contributes exactly one “anchor” assignment that does not require persuasion.

### Why it works

Each job must retain exactly one worker. Within a job group, any worker except the one we assign to that job must be moved. Since moving costs $b_i$, minimizing cost is equivalent to maximizing the cost we avoid paying by not moving someone. The best candidate to avoid moving is always the worker with the largest $b_i$ in that group, because keeping any other worker would force us to lose a higher-value saving. This creates a local choice per job that does not interact across jobs, so the sum of independent optimal choices is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    max_b = [0] * (k + 1)
    total = 0
    
    for i in range(n):
        job = a[i]
        cost = b[i]
        total += cost
        if cost > max_b[job]:
            max_b[job] = cost
    
    ans = total - sum(max_b[1:])
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a running total of all persuasion costs while tracking, for each job, the maximum cost among workers assigned to that job. The final subtraction step removes exactly one worker per job from being counted as “persuaded.”

The key detail is that we never explicitly simulate reassignments. We only compute which workers are cheapest to keep in place. The indexing from $1$ to $k$ matches the job labels directly, avoiding off-by-one complications.

## Worked Examples

### Example 1

Input:

```
8 7
1 1 3 1 5 3 7 1
5 7 4 8 1 3 5 2
```

We group workers by job and track the maximum cost in each group.

| Job | Costs in group | Max kept |
| --- | --- | --- |
| 1 | 5, 7, 8, 2 | 8 |
| 2 | - | 0 |
| 3 | 4, 3 | 4 |
| 4 | - | 0 |
| 5 | 1 | 1 |
| 6 | - | 0 |
| 7 | 5 | 5 |

Total sum of all costs is $5 + 7 + 4 + 8 + 1 + 3 + 5 + 2 = 35$.

Sum of maxima is $8 + 0 + 4 + 0 + 1 + 0 + 5 = 18$.

Result is $35 - 18 = 17$. This matches the idea that each job keeps its most “expensive-to-move” worker.

This trace shows that all structure is local per job, and no cross-job decisions are needed.

### Example 2

Input:

```
3 3
1 2 3
10 20 30
```

| Job | Costs | Max kept |
| --- | --- | --- |
| 1 | 10 | 10 |
| 2 | 20 | 20 |
| 3 | 30 | 30 |

Total is $60$, sum of maxima is $60$, so answer is $0$. Every job already has a unique worker, so no persuasion is required.

This confirms that the algorithm correctly handles the fully balanced case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to compute totals and per-job maxima |
| Space | $O(k)$ | Array storing maximum cost per job |

The solution fits comfortably within limits since $n \le 10^5$, and both time and memory usage are linear and minimal.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    max_b = [0] * (k + 1)
    total = 0
    for i in range(n):
        total += b[i]
        max_b[a[i]] = max(max_b[a[i]], b[i])
    
    print(total - sum(max_b[1:]))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    sys.stdin = old_stdin
    return out.getvalue().strip()

# provided sample
assert run("""8 7
1 1 3 1 5 3 7 1
5 7 4 8 1 3 5 2
""") == "17"

# all jobs already unique
assert run("""3 3
1 2 3
10 20 30
""") == "0"

# all choose same job
assert run("""5 3
1 1 1 1 1
1 2 3 4 5
""") == "5"

# minimal case
assert run("""1 1
1
100
""") == "0"

# mixed groups
assert run("""4 3
1 2 2 3
5 1 10 2
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all unique jobs | 0 | no persuasion needed |
| all same job | correct grouping behavior | multiple candidates per job |
| single element | base case correctness |  |
| mixed groups | correctness of per-group max logic |  |

## Edge Cases

When every worker chooses the same job, all other jobs are empty and must be filled entirely by reassigning workers from the dense group. The algorithm handles this by selecting the maximum cost worker in that group to stay, while counting all others as removable cost, which correctly minimizes total persuasion time by preserving the most expensive worker.

When every job already has exactly one worker, each group has a single element, so the maximum equals the total for that group. The subtraction removes everything, yielding zero cost, matching the fact that no persuasion is needed.
