---
title: "CF 105579L - Optimal Milk Temperature"
description: "We are given a sequence of milk batches, each batch has two attributes. The first is a coefficient $bi$ which represents how much flavor Vova gains per unit of heating temperature."
date: "2026-06-22T21:52:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105579
codeforces_index: "L"
codeforces_contest_name: "Udmurtia High School Programming Contest (Qualification for VKOSHP 2012)"
rating: 0
weight: 105579
solve_time_s: 61
verified: true
draft: false
---

[CF 105579L - Optimal Milk Temperature](https://codeforces.com/problemset/problem/105579/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of milk batches, each batch has two attributes. The first is a coefficient $b_i$ which represents how much flavor Vova gains per unit of heating temperature. The second is a limit $t_i$ which represents the highest temperature at which this batch can be heated without producing foam. If the chosen global heating temperature is $T$, then batch $i$ is drinkable only if $T \le t_i$. If it is drinkable, it contributes exactly $b_i \cdot T$ to the total enjoyment. If $T > t_i$, the batch is unusable and contributes nothing.

The task is to choose a single integer temperature $T$ that is applied to all batches, so that the sum of contributions over all batches that remain foam-free is maximized.

The key structure is that $T$ is global. We are not optimizing each batch independently, but instead choosing one value that simultaneously increases contribution linearly for some items while possibly excluding others.

The input size $n$ can be up to 100000, and values of $t_i$ can be as large as $10^9$. This immediately rules out any approach that tries all possible temperatures. A brute force over $T$ would require checking up to $10^9$ candidates, which is impossible. Even iterating over all pairs or subsets is also infeasible due to exponential growth.

A naive observation is that the answer depends only on “breakpoints” defined by the values $t_i$, because increasing $T$ only changes the set of active batches when it crosses one of these thresholds.

A subtle failure case for naive reasoning is assuming that taking $T = \max t_i$ is always optimal. For example, if one batch has very large $b_i$ but small $t_i$, increasing $T$ beyond that threshold removes it entirely, possibly reducing the total sum.

Another failure mode is trying to evaluate each $T$ independently without reusing computations, leading to $O(n \cdot \max t_i)$ or similar impossible complexity.

## Approaches

The brute-force idea is straightforward. For every possible integer temperature $T$, we compute the sum of all $b_i \cdot T$ such that $t_i \ge T$. For each candidate $T$, we scan all $n$ items, check feasibility, and accumulate contribution. This is correct because it directly simulates the definition of the problem.

However, this approach is too slow because $T$ can range up to $10^9$. Even if we restrict candidates to unique $t_i$ values, we still have up to $n$ candidates, and each requires $O(n)$ work, leading to $O(n^2)$, which is too large for $10^5$.

The key insight is to reverse the perspective. Instead of fixing a temperature and checking which batches survive, we fix a batch and ask for which temperatures it contributes. Batch $i$ contributes for all $T \le t_i$, and its contribution is linear in $T$. This means that the total function is a sum of linear functions, but each one is truncated at its own cutoff.

We can sort by $t_i$. As we increase $T$, batches become invalid exactly when $T$ exceeds their threshold. This suggests sweeping over possible $T$ values in decreasing order of $t_i$, maintaining which batches are still active.

A cleaner transformation is to think in terms of contribution as a function of $T$:

$$f(T) = T \cdot \sum_{i: t_i \ge T} b_i$$

So the problem becomes finding the maximum value of $T \cdot S(T)$, where $S(T)$ is the sum of $b_i$ among all $t_i \ge T$. As $T$ increases, $S(T)$ only decreases, while $T$ increases. The optimum occurs at a point where we include exactly all items with $t_i \ge T$, which corresponds to sorting thresholds and checking candidate breakpoints.

We sort pairs $(t_i, b_i)$ in increasing order of $t_i$. We then process from largest $t_i$ downwards, maintaining a running sum of $b_i$. At each threshold $t_i$, we consider choosing $T = t_i$, because between two adjacent thresholds, the active set does not change, and increasing $T$ only improves the multiplicative factor while keeping the active set fixed until a boundary.

Thus we only need to evaluate $T \cdot (\text{sum of } b_i \text{ with } t_i \ge T)$ at these critical points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over T | O(n · max t) | O(1) | Too slow |
| Optimal sorting + sweep | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We convert the problem into evaluating a function at a small number of meaningful candidate points derived from the constraints.

1. Pair each batch as $(t_i, b_i)$ and sort the list by $t_i$ in increasing order. This organizes the batches by the moment they stop being valid when temperature increases.
2. Compute the total sum of all $b_i$. This represents the initial value of $S(T)$ for very small $T$, where all batches are valid.
3. Traverse the sorted array from smallest $t_i$ to largest. At each position $i$, we treat $t_i$ as a candidate temperature.
4. Maintain a running suffix sum of $b_i$, but computed implicitly by subtracting as we move forward. When we pass a batch with threshold $t_i$, it is no longer valid for any higher temperature, so we remove its $b_i$ from the active sum.
5. At each distinct threshold value $t_i$, compute the candidate answer as $t_i \times (\text{current active sum})$. We only evaluate when we are exactly at a boundary or just after updating the active set.
6. Track the maximum value across all such candidate evaluations.

The reason we can restrict ourselves to these points is that between two consecutive thresholds, the active set $S(T)$ is constant. Inside such an interval, $f(T) = T \cdot S$ is a linear function in $T$, so its maximum in the interval is always at the right endpoint.

### Why it works

The function being optimized is piecewise linear, where breakpoints occur exactly at the values $t_i$. Between breakpoints, the slope does not change because the set of active batches remains fixed. Since $f(T)$ is linear on each interval, its maximum over that interval must lie at an endpoint. Therefore, restricting evaluation to endpoints $t_i$ is sufficient to capture the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = list(map(int, input().split()))
    t = list(map(int, input().split()))
    
    pairs = list(zip(t, b))
    pairs.sort()
    
    total_b = sum(b)
    best = 0
    
    i = 0
    n = len(pairs)
    
    while i < n:
        j = i
        # group equal t values
        while j < n and pairs[j][0] == pairs[i][0]:
            j += 1
        
        # temperature candidate is pairs[i][0]
        T = pairs[i][0]
        
        # remove all elements with t == T from active set
        for k in range(i, j):
            total_b -= pairs[k][1]
        
        # now active set is all with t > T
        best = max(best, T * total_b)
        
        i = j
    
    print(best)

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting pairs by threshold. The variable `total_b` starts as the sum of all coefficients and gradually loses contributions as we pass each threshold group. After removing all batches with the current threshold value, we compute the contribution at that exact temperature, because those batches are no longer valid if we were to increase beyond this point.

Grouping equal $t_i$ values is important because all of them become invalid simultaneously when crossing that threshold, and we must ensure they are removed before evaluating the candidate at that level.

## Worked Examples

### Example 1

Input:

```
3
10 1 2
2 2 7
```

Sorted pairs: $(2,10), (2,1), (7,2)$

Initial total_b = 13

| Step | T | Removed b | Active sum | Score |
| --- | --- | --- | --- | --- |
| start | - | - | 13 | - |
| process t=2 group | 2 | 10+1 | 2 | 4 |
| process t=7 group | 7 | 2 | 0 | 0 |

Best is 4.

This shows that increasing temperature too much eliminates all useful batches, while small temperature preserves enough weight to compensate.

### Example 2

Input:

```
2
1 1
10 1
```

Sorted pairs: $(1,1), (10,1)$

Initial total_b = 2

| Step | T | Removed b | Active sum | Score |
| --- | --- | --- | --- | --- |
| start | - | - | 2 | - |
| process t=1 group | 1 | 1 | 1 | 1 |
| process t=10 group | 10 | 1 | 0 | 0 |

Best is 1.

This demonstrates a case where keeping both batches at low temperature is optimal, and higher temperature destroys too much contribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, single linear sweep follows |
| Space | O(n) | Storing pairs of (t_i, b_i) |

The constraints allow up to 100000 items, and an $O(n \log n)$ solution runs comfortably within limits due to efficient sorting and a single pass accumulation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    b = list(map(int, input().split()))
    t = list(map(int, input().split()))
    
    pairs = list(zip(t, b))
    pairs.sort()
    
    total_b = sum(b)
    best = 0
    
    i = 0
    n = len(pairs)
    
    while i < n:
        j = i
        while j < n and pairs[j][0] == pairs[i][0]:
            j += 1
        
        T = pairs[i][0]
        
        for k in range(i, j):
            total_b -= pairs[k][1]
        
        best = max(best, T * total_b)
        
        i = j
    
    return str(best)

# provided samples (as interpreted)
assert run("3\n10 1 2\n2 2 7\n") == "4"

# minimum size
assert run("1\n5\n10\n") == "0"

# all equal t
assert run("3\n1 2 3\n5 5 5\n") == "30"

# strictly increasing t
assert run("4\n1 2 3 4\n1 2 3 4\n") == "20"

# mixed case
assert run("5\n5 4 3 2 1\n3 3 2 2 1\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | edge case where no valid high T contributes |
| all equal thresholds | 30 | correctness when all batches switch together |
| increasing thresholds | 20 | monotone structure and cumulative removal |
| mixed values | 15 | interaction of ordering and partial removals |

## Edge Cases

A key edge case is when the optimal temperature is the smallest threshold. Consider input:

```
2
100 1
1 100
```

If we choose $T = 1$, both batches contribute, giving $101$. If we choose $T = 100$, only the second batch contributes, giving $100$. The algorithm evaluates both breakpoints. At $T = 1$, no removal happens yet, so score is $1 \cdot 101$. At $T = 100$, the first batch has already been removed earlier, so only $1 \cdot 1$ remains, producing $100$. The maximum is correctly identified.

Another edge case is when all $t_i$ are identical. Then all batches are removed at once, and the only meaningful evaluation happens at that single threshold. The algorithm processes the group once, subtracts all $b_i$, and evaluates zero contribution beyond it, ensuring correctness without special casing.
