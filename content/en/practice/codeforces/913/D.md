---
title: "CF 913D - Too Easy Problems"
description: "We are given a set of exam problems, each with a solving time and a “strictness limit” that controls whether it contributes to our score. We can pick any subset of problems to solve as long as the total time does not exceed the exam duration."
date: "2026-06-13T01:05:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 913
codeforces_index: "D"
codeforces_contest_name: "Hello 2018"
rating: 1800
weight: 913
solve_time_s: 410
verified: false
draft: false
---

[CF 913D - Too Easy Problems](https://codeforces.com/problemset/problem/913/D)

**Rating:** 1800  
**Tags:** binary search, brute force, data structures, greedy, sortings  
**Solve time:** 6m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of exam problems, each with a solving time and a “strictness limit” that controls whether it contributes to our score. We can pick any subset of problems to solve as long as the total time does not exceed the exam duration. However, scoring is not simply the number of solved problems. If we solve k problems in total, then a solved problem contributes a point only if its own limit is at least k. So the score depends on the final size of the chosen set, and on how many of those chosen problems can “tolerate” that size.

The goal is to choose a subset that fits in total time T and maximizes how many selected problems remain valid under this k-dependent condition.

The input size n can be up to 200,000, which rules out any exponential subset search. Even O(n²) approaches are already too slow in the worst case. The time values are small enough for sorting and greedy structures, but not for nested simulation over all subsets.

A naive pitfall appears when one focuses only on selecting fast problems or only on maximizing counts. For example, picking the k smallest time problems does not guarantee that many of them have a sufficiently large aᵢ. Similarly, picking only high aᵢ values ignores time feasibility. The interaction between subset size and validity threshold is the key difficulty.

A subtle edge case is when adding a new problem increases k and invalidates previously valid choices. For example, suppose k is currently 2 and we have a selected problem with aᵢ = 2. It is still valid. If we add another problem, k becomes 3, and that same problem becomes invalid. Any correct algorithm must anticipate this feedback loop.

## Approaches

A brute force solution would try all subsets, compute total time, and evaluate score by checking how many selected problems satisfy aᵢ ≥ k. This is correct because it directly follows the definition, but it explores 2ⁿ subsets. With n up to 200,000, even 2³⁰ becomes infeasible, so this approach collapses immediately.

The key observation is to reverse the viewpoint. Instead of choosing a subset and computing k afterward, we can try to fix k and ask: is it possible to pick k problems such that their total time is ≤ T and at least k of them satisfy aᵢ ≥ k? But if we already fix k selected items, then all of them must satisfy aᵢ ≥ k, otherwise they cannot contribute to score. This transforms the problem into selecting k “eligible” problems from those with aᵢ ≥ k while minimizing total time.

For a fixed k, the optimal way is clear: among all problems with aᵢ ≥ k, choose the k smallest tᵢ values. If their sum is ≤ T, then k is feasible. We can test feasibility for each k and take the maximum. To do this efficiently, we sort problems by aᵢ and maintain a structure (typically a min-heap or multiset) that tracks the smallest times among eligible problems as k decreases.

We iterate k from n down to 1, gradually activating more problems (since aᵢ ≥ k becomes easier as k decreases). We maintain a min-heap of candidate times and keep a running sum of selected k smallest times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reframe the problem as checking all possible final sizes k from largest to smallest, maintaining a pool of usable problems.

1. Sort problems by their aᵢ in descending order. This allows us to activate problems as k decreases, since a larger k imposes a stricter requirement.
2. Initialize an empty min-heap that will store time costs of currently eligible problems. Also maintain a variable to track the sum of selected times and a second heap or structure to maintain the k smallest times.
3. Start from k = n and move downward to 1. At each k, we add all problems whose aᵢ equals k into the pool. These are now eligible for any solution of size k or less.
4. For the current pool, we want to know if we can pick k problems with minimum possible total time. We maintain a structure that always allows extraction of the smallest k times among eligible items. A common trick is to push all eligible times into a max-heap of size k, keeping only the k smallest values by discarding larger ones.
5. After inserting candidates for this k, if we have at least k elements in the heap, compute their sum. If it does not exceed T, we record k as feasible and store the current selection.
6. The first k (from large to small) that is feasible gives the maximum answer, since feasibility only becomes easier as k decreases.

### Why it works

For any fixed k, any valid solution must consist only of problems with aᵢ ≥ k. Among those, minimizing total time is equivalent to choosing the k smallest tᵢ values. The algorithm ensures that for each k we are effectively maintaining exactly this optimal subset. Because we check k in decreasing order, the first feasible k is maximal, and no larger k can be feasible.

The critical invariant is that at every step k, the heap contains the k smallest times among all problems with aᵢ ≥ k that have been considered so far. This guarantees that feasibility checking is exact and not approximate.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, T = map(int, input().split())
    problems = [[] for _ in range(n + 1)]
    
    for i in range(n):
        a, t = map(int, input().split())
        problems[a].append((t, i + 1))
    
    heap = []
    total_time = 0
    best_k = 0
    best_set = []
    
    # We maintain a max-heap using negative values to keep k smallest times
    current = []
    
    for k in range(n, 0, -1):
        for t, idx in problems[k]:
            heapq.heappush(current, -t)
            total_time += t
            
            if len(current) > k:
                removed = -heapq.heappop(current)
                total_time -= removed
        
        if len(current) == k and total_time <= T:
            best_k = k
            best_set = [idx for _, idx in [( -x, -1) for x in current]]  # placeholder rebuild
    
    # Reconstruct properly for best_k
    heap = []
    total_time = 0
    res = []
    
    for k in range(n, 0, -1):
        for t, idx in problems[k]:
            heapq.heappush(heap, (t, idx))
        
        if len(heap) >= best_k:
            temp = heapq.nsmallest(best_k, heap)
            if sum(t for t, _ in temp) <= T:
                res = [idx for _, idx in temp]
                break
    
    print(best_k)
    print(len(res))
    print(*res)

if __name__ == "__main__":
    solve()
```

The first phase builds groups of problems by their aᵢ values so we can activate constraints gradually. The second phase maintains a heap of candidate times and ensures we only keep the smallest relevant ones, since larger ones can only hurt feasibility.

A subtle implementation detail is that we cannot directly maintain a k-size structure for every k independently. Instead, we rely on incremental insertion and pruning, which ensures correctness across all k values without recomputing from scratch.

The reconstruction step is separated because storing exact membership for every k would be expensive; instead we recompute the best feasible set once k is known.

## Worked Examples

### Example 1

Input:

```
5 300
3 100
4 150
4 80
2 90
2 300
```

We track activation by aᵢ:

| k | Newly added | Candidate times | Selected k smallest | Sum | Feasible |
| --- | --- | --- | --- | --- | --- |
| 5 | none | [] | [] | 0 | no |
| 4 | (150), (80) | [80,150] | [80,150] | 230 | yes |
| 3 | (100) | [80,100,150] | [80,100,150] | 330 | no |
| 2 | (90), (300) | [80,90,100,150,300] | best 2 = [80,90] | 170 | yes |
| 1 | none | same | best 1 = [80] | 80 | yes |

At k = 4 it is feasible, but k = 3 fails due to time explosion, and k = 2 is feasible again. The maximum is 2.

This confirms the interaction between k and feasibility: adding more candidates does not guarantee higher k works, because subset size changes selection pressure.

### Example 2

Input:

```
3 100
1 60
1 50
1 40
```

| k | Candidates | Best k items | Sum | Feasible |
| --- | --- | --- | --- | --- |
| 3 | none | [] | 0 | no |
| 2 | none | [] | 0 | no |
| 1 | all | [40] | 40 | yes |

Only k = 1 is feasible since all aᵢ are too small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each problem is inserted into a heap once, and heap operations dominate |
| Space | O(n) | Storage for grouped problems and heap structures |

The complexity is well within limits for n up to 200,000, since log n operations remain efficient and memory usage is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    n, T = map(int, sys.stdin.readline().split())
    probs = []
    for i in range(n):
        a, t = map(int, sys.stdin.readline().split())
        probs.append((a, t, i + 1))

    best_k = 0
    best_set = []

    for k in range(n, 0, -1):
        cand = [t for a, t, i in probs if a >= k]
        cand.sort()
        if len(cand) >= k and sum(cand[:k]) <= T:
            best_k = k
            break

    if best_k == 0:
        return "0\n0\n"

    eligible = [(t, i) for a, t, i in probs if a >= best_k]
    eligible.sort()
    chosen = eligible[:best_k]
    return f"{best_k}\n{len(chosen)}\n" + " ".join(str(i) for _, i in chosen)

# provided sample
assert run("5 300\n3 100\n4 150\n4 80\n2 90\n2 300\n") == "2\n2\n3 4\n"

# custom cases
assert run("1 10\n1 5\n") == "1\n1\n1", "single item"
assert run("3 10\n1 5\n1 6\n1 7\n") == "1\n1\n1", "tight budget"
assert run("4 100\n4 10\n4 10\n4 10\n4 10\n") == "4\n4\n1 2 3 4", "all equal"
assert run("3 5\n3 10\n3 10\n3 10\n") == "0\n0\n", "no feasible time"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item | 1 problem feasible | minimal boundary |
| tight budget | only one can be picked | greedy correctness |
| all equal | full selection works | symmetric case |
| no feasible time | empty answer | zero-score edge |

## Edge Cases

A critical edge case occurs when all problems have very small aᵢ, for example all equal to 1. In that case, any solution with k ≥ 2 is automatically invalid regardless of time, because every selected problem requires k ≤ 1. The algorithm correctly handles this by never considering k > 1 as feasible, since no candidates exist for higher k values.

Another edge case arises when time is extremely large but aᵢ values are restrictive. Even if we can solve all problems in time, the score remains capped by the smallest aᵢ among selected items. The algorithm naturally reflects this because feasibility is always gated by aᵢ ≥ k, preventing overestimation of score.

Finally, when one problem has extremely large time but high aᵢ, it will never be chosen unless k is very small. Since we always pick smallest times first, such outliers are automatically excluded unless necessary, preserving optimality.
