---
title: "CF 104135C - \u041a\u0440\u043e\u0448 \u0438 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f"
description: "We are given a sequence of numbers representing a row of elements, each element having two attributes: a value and a removal cost. The game allows us to repeatedly pick two adjacent elements and delete the smaller-valued one, paying its associated removal cost."
date: "2026-07-02T01:40:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104135
codeforces_index: "C"
codeforces_contest_name: "\u0417\u0438\u043c\u043d\u0438\u0439 \u043b\u0438\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 2023"
rating: 0
weight: 104135
solve_time_s: 44
verified: true
draft: false
---

[CF 104135C - \u041a\u0440\u043e\u0448 \u0438 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/104135/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers representing a row of elements, each element having two attributes: a value and a removal cost. The game allows us to repeatedly pick two adjacent elements and delete the smaller-valued one, paying its associated removal cost. The structure of the array changes after each deletion because elements close up, so adjacency is always dynamic.

The process continues any number of times, but we must always leave at least one element in the array. We also have a fixed budget, and every deletion consumes part of that budget. The goal is to maximize the smallest value remaining in the array after performing some sequence of deletions under the budget constraint.

From a constraints perspective, the array size can reach up to 100000, and the budget can be as large as 10^18. This immediately rules out any solution that simulates operations step by step or tries to enumerate sequences of deletions. Any approach that is quadratic in n or even n log n with heavy constants is potentially acceptable, but anything worse than O(n log n) would be too slow.

The key difficulty is that deletions are not arbitrary: they depend on adjacency, and each operation removes the smaller of a chosen adjacent pair. This means that removing a specific element is not independent of the others; instead, feasibility depends on whether we can "expose" that element as the smaller in some adjacent pair repeatedly.

A few subtle edge cases are worth keeping in mind. If all elements are already large but costs are zero, we can delete aggressively and leave a very high minimum. If costs are very large, we may not be able to delete anything at all, so the answer is simply the minimum element of the array. Another corner case is when the optimal strategy leaves only one element; since the problem requires at least one element to remain, we must ensure we never delete everything.

A simple misleading example is a case where a globally cheap element is in the middle but surrounded by expensive ones. Even if it is cheap to remove locally, the structure might block its removal because it can never be the smaller in a valid adjacent pair without first removing neighbors.

## Approaches

A brute-force interpretation would try to simulate all possible deletion sequences. At each step, we choose any adjacent pair, remove the smaller, and subtract its cost from the budget. This forms a huge state space because the array changes shape after every operation, and the number of possible sequences grows exponentially with n. Even for n = 40, this becomes infeasible.

The key observation is that we are not actually asked to simulate the process, but only to determine whether we can eliminate enough elements to ensure a certain minimum value remains. This suggests reversing the perspective: instead of simulating deletions, we test whether a candidate answer x is achievable.

Fix a value x. We want to know if it is possible to remove every element with value less than x while spending at most s. If we can do this, then all remaining elements have value at least x, so the minimum is at least x. This turns the problem into a decision problem that can be solved independently for each x, which naturally leads to binary search on the answer.

The non-trivial part is determining feasibility for a fixed x. An element with value at least x can never be deleted if we choose not to remove it, so we treat those as "protected". Elements with value less than x must be removed. Each such element has a cost, but whether it can actually be removed depends on whether it can be paired with some neighbor during the process.

A crucial structural simplification is that any removable element can eventually be deleted as long as we always ensure it participates in a valid adjacent pair before being blocked by surviving elements. This reduces the problem to a cost accumulation over all elements with value less than x, because we can always organize deletions in an order that allows them to be removed independently of each other’s exact positions, provided at least one neighbor exists at the time of removal.

Thus, for a fixed x, feasibility reduces to summing costs of all elements with value less than x and checking whether this sum is within budget s, while also ensuring that not all elements are removed (at least one element with value ≥ x must exist).

This transforms the problem into a monotone predicate over x, enabling binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Binary Search + Feasibility Check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort or conceptually treat values as candidates for the final minimum answer, since the answer must equal some existing element value. This reduces the search space to at most n possibilities.
2. Binary search over a candidate threshold x representing the minimum allowed value in the final array.
3. For a fixed x, iterate through the array and identify all elements with value strictly less than x, since these are the ones we must remove.
4. Accumulate the total cost of removing these elements. This represents the minimum possible spending required to eliminate all elements that would violate the threshold.
5. Check whether this total cost is within the budget s. If it exceeds s, then x is not feasible because we cannot eliminate all offending elements.
6. Ensure that at least one element with value ≥ x exists. If none exists, then even with enough budget we cannot leave a valid final element meeting the threshold.
7. If both conditions are satisfied, mark x as feasible and try increasing it; otherwise decrease it.
8. After binary search completes, output the maximum feasible x.

### Why it works

The key invariant is that feasibility depends only on whether we can eliminate all elements below the threshold without exceeding the budget, and not on the exact order of deletions. Any valid deletion sequence that removes a given element always pays its cost exactly once, and the adjacency constraint does not increase the total required cost, it only restricts ordering. Since we can always schedule deletions so that each removable element is eventually paired and eliminated before it becomes blocked by surviving higher elements, the total cost is exactly the sum of costs of all elements below the threshold. Therefore the decision problem is monotone in x, which guarantees correctness of binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def feasible(a, c, s, x):
    total = 0
    has_good = False
    n = len(a)

    for i in range(n):
        if a[i] >= x:
            has_good = True
        else:
            total += c[i]

    return has_good and total <= s

def solve():
    n, s = map(int, input().split())
    a = list(map(int, input().split()))
    c = list(map(int, input().split()))

    vals = sorted(set(a))
    
    lo, hi = 0, len(vals) - 1
    ans = vals[0]

    while lo <= hi:
        mid = (lo + hi) // 2
        x = vals[mid]

        if feasible(a, c, s, x):
            ans = x
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code first reads the array and cost structure, then compresses candidate answers to only distinct values of the array. The feasibility function computes the cost of removing all elements below a threshold and checks whether at least one valid survivor exists.

The binary search maintains the invariant that all values up to `ans` are feasible, and it expands upward whenever the current midpoint is valid.

A subtle implementation detail is that we never simulate adjacency operations explicitly. This is intentional because the total cost is independent of deletion order under optimal scheduling, even though the original problem is phrased dynamically.

## Worked Examples

Consider an input where values are `[3, 1, 4, 2, 5, 6]` and costs are `[3, 2, 5, 5, 2, 7]` with budget `12`.

We test a candidate threshold x = 4.

| i | a[i] | c[i] | a[i] < 4? | total cost |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | yes | 3 |
| 1 | 1 | 2 | yes | 5 |
| 2 | 4 | 5 | no | 5 |
| 3 | 2 | 5 | yes | 10 |
| 4 | 5 | 2 | no | 10 |
| 5 | 6 | 7 | no | 10 |

Total cost is 10, which is within budget, and we still have elements ≥ 4, so 4 is feasible. This shows the mechanism correctly identifies that we can eliminate all smaller elements.

Now consider x = 5.

| i | a[i] | c[i] | a[i] < 5? | total cost |
| --- | --- | --- | --- | --- |
| 0 | 3 | 3 | yes | 3 |
| 1 | 1 | 2 | yes | 5 |
| 2 | 4 | 5 | yes | 10 |
| 3 | 2 | 5 | yes | 15 |
| 4 | 5 | 2 | no | 15 |
| 5 | 6 | 7 | no | 15 |

Now total cost is 15, which exceeds 12, so 5 is not feasible. This demonstrates how the threshold check captures budget infeasibility directly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each feasibility check is O(n), and binary search runs over at most log n candidate values |
| Space | O(n) | Stores arrays and compressed value set |

The complexity fits comfortably within constraints for n up to 100000, since about 20 feasibility checks are performed, each linear over the array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, s = map(int, input().split())
    a = list(map(int, input().split()))
    c = list(map(int, input().split()))

    def feasible(a, c, s, x):
        total = 0
        has_good = False
        for i in range(len(a)):
            if a[i] >= x:
                has_good = True
            else:
                total += c[i]
        return has_good and total <= s

    vals = sorted(set(a))
    lo, hi = 0, len(vals) - 1
    ans = vals[0]

    while lo <= hi:
        mid = (lo + hi) // 2
        x = vals[mid]
        if feasible(a, c, s, x):
            ans = x
            lo = mid + 1
        else:
            hi = mid - 1

    return str(ans)

# sample
assert run("""6 12
3 1 4 2 5 6
3 2 5 5 2 7
""") == "4"

# all equal
assert run("""5 0
2 2 2 2 2
1 1 1 1 1
""") == "2"

# cannot delete anything
assert run("""4 0
1 2 3 4
10 10 10 10
""") == "1"

# tight budget
assert run("""3 3
5 1 4
2 2 2
""") == "4"

# large budget
assert run("""3 100
1 2 3
1 1 1
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 4 | correctness on mixed values |
| all equal | 2 | handling zero removals |
| tight budget | 4 | pruning under constraints |
| large budget | 3 | full deletion capability |

## Edge Cases

When all elements are below a candidate threshold, the feasibility check fails immediately because there is no surviving element to anchor the final minimum. The algorithm correctly rejects such thresholds because `has_good` remains false, preventing invalid answers.

When the budget is zero, the only feasible answer is the minimum element, since any attempt to remove a lower-valued element incurs positive cost. The check naturally enforces this because `total` becomes positive whenever removals are required.

When all costs are zero, every element below a threshold can be removed freely, so the answer becomes the maximum possible element value. The algorithm captures this because `total` never exceeds `s`, and feasibility depends only on existence of a surviving element.

When values are strictly increasing or decreasing, the binary search still works because feasibility depends only on partitioning by threshold, not structure or adjacency, making order irrelevant to the cost computation.
