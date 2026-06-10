---
title: "CF 1440B - Sum of Medians"
description: "We are given a sorted list of $nk$ numbers and asked to split it into $k$ groups, each containing exactly $n$ elements."
date: "2026-06-11T04:23:39+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1440
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 684 (Div. 2)"
rating: 900
weight: 1440
solve_time_s: 71
verified: true
draft: false
---

[CF 1440B - Sum of Medians](https://codeforces.com/problemset/problem/1440/B)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sorted list of $nk$ numbers and asked to split it into $k$ groups, each containing exactly $n$ elements. Once the split is done, we compute the median of each group using the upper middle position in its sorted order, and we want the sum of all these medians to be as large as possible.

The key constraint is that we are not free to reorder the input array arbitrarily inside groups without cost, but the global array is already sorted. The task is entirely about how to partition consecutive values into groups so that the selected median positions become as large as possible.

The constraints allow up to $2 \cdot 10^5$ total elements across all test cases. This immediately rules out any solution that tries to simulate all possible partitions or repeatedly sort subsets. Any approach must essentially be linear in the array size per test case, or at worst $O(nk \log(nk))$, though sorting is unnecessary because the array is already sorted.

A subtle edge case appears when $n = 1$. In that situation, every element is its own median, so the answer is just the sum of the array. A naive grouping strategy that tries to “balance” groups can easily miss this simplification.

Another non-obvious corner case occurs when $k = 1$. Then we have only one group, so the answer is simply the median of the entire array, i.e. the element at index $\lceil nk/2 \rceil$.

The main difficulty arises when both $n$ and $k$ are large, because we must decide how to distribute elements so that medians come from the largest possible available values.

## Approaches

If we think about brute force, we would try all possible ways to split the sorted array into $k$ groups of size $n$. Even if we restrict ourselves to maintaining order, the number of ways to choose positions is combinatorial, on the order of multinomial coefficients. For $nk \le 2000$, this is already infeasible; for $2 \cdot 10^5$, it is completely impossible.

The key observation is that the array is sorted, and we only care about medians, not full group structure. Inside each group of size $n$, the median is the element at position $\lceil n/2 \rceil$. So each group contributes one “important” element, and the rest are only constraints ensuring feasibility.

This suggests we should think in terms of selecting $k$ median positions from the array. The structure becomes clearer if we imagine building groups greedily from the largest values backward: to maximize medians, we want each median to be as large as possible, but we are forced to “spend” other elements around it to complete each group.

Each median effectively consumes $n - 1$ supporting elements. Since we want to maximize medians, we should assign the largest available elements as medians, but we must ensure enough elements remain to form valid groups.

If we process from the largest values, every time we pick a median, we must skip enough elements so that the group can be completed. The optimal pattern turns out to be deterministic: we repeatedly take one element as a median, then discard $n - 1$ elements that would otherwise interfere with forming valid groups.

Equivalently, we can work from the end of the array and select every second element starting from a specific offset determined by $n$. The spacing between chosen medians is exactly $n - 1$, but because groups overlap in the sorted structure, the effective step becomes $n - 1$ elements skipped between consecutive chosen medians when scanning from right to left.

Thus, the optimal solution reduces to selecting $k$ elements from the sorted array at fixed intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all partitions) | exponential | high | Too slow |
| Optimal greedy selection | $O(nk)$ | $O(1)$ extra | Accepted |

## Algorithm Walkthrough

1. Compute $m = \lceil n/2 \rceil$, which is the median position inside any group. This tells us how far the median lies from the start of its group when sorted.
2. Work on the global sorted array from the end, since larger values should contribute to medians whenever possible.
3. Starting from index $nk - 1$, pick elements as medians while moving left in steps of size $n - m + 1$ or, more simply, by the pattern derived from grouping constraints: every time we pick one median, we skip $n - m$ elements that must belong to the same or previous group.

The clean implementation simplifies this further: we move backwards and pick every $(n - m + 1)$-th element starting from a specific offset.
4. Collect exactly $k$ such elements, since there are $k$ groups and therefore $k$ medians.
5. Sum these selected elements and output the result.

The subtle part is that we are not explicitly constructing groups. Instead, we simulate the constraints imposed by grouping: each median must have enough elements to its right (in sorted order) to fill its group.

### Why it works

The invariant is that after selecting a median, we always leave enough unused elements to form complete groups for all remaining medians. Because the array is sorted, taking medians from the right maximizes their value, and skipping exactly the required number of elements ensures feasibility without wasting larger elements on non-median positions. Any deviation that selects a smaller median earlier would either reduce the sum directly or force even larger elements into non-median slots, which cannot increase the total.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        # median position in each group (1-indexed)
        m = (n + 1) // 2
        
        # step size between useful medians when scanning from right
        step = n - m + 1
        
        # start from the last element
        idx = len(a) - step
        
        ans = 0
        
        for _ in range(k):
            ans += a[idx]
            idx -= step
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation works entirely on index arithmetic over the sorted array. The key is computing the correct spacing between chosen medians. The variable `m` determines where the median lies inside each group, and from that we derive how many elements must be skipped so that each chosen median can belong to a valid group without overlap.

The backward traversal ensures we always pick the largest available valid candidate.

## Worked Examples

### Example 1

Input:

```
n = 2, k = 4
a = [0, 24, 34, 58, 62, 64, 69, 78]
```

Here $m = 1$, so every first element in a group of size 2 is the median after sorting each pair.

We compute `step = 2`.

| Step | idx | Selected value | Remaining k |
| --- | --- | --- | --- |
| 1 | 6 | 69 | 3 |
| 2 | 4 | 62 | 2 |
| 3 | 2 | 34 | 1 |
| 4 | 0 | 0 | 0 |

Sum = 165.

This confirms that we are consistently taking the largest possible valid median while respecting spacing constraints.

### Example 2

Input:

```
n = 3, k = 3
a = [2, 4, 16, 18, 21, 27, 36, 53, 82]
```

Here $m = 2$, so median is the second element in each group, and `step = 2`.

| Step | idx | Selected value | Remaining k |
| --- | --- | --- | --- |
| 1 | 7 | 53 | 2 |
| 2 | 5 | 27 | 1 |
| 3 | 3 | 18 | 0 |

Sum = 98.

Each selection ensures that enough elements remain to form valid groups, and we always prioritize the largest feasible median.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk)$ | Each element is processed once in a linear scan per test case |
| Space | $O(1)$ | Only index arithmetic and accumulator used |

The constraints allow up to $2 \cdot 10^5$ elements, so a linear pass over the array is easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    
    input = sys.stdin.readline
    t = int(sys.stdin.readline())
    
    out = []
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        a = list(map(int, sys.stdin.readline().split()))
        
        m = (n + 1) // 2
        step = n - m + 1
        
        idx = len(a) - step
        ans = 0
        
        for _ in range(k):
            ans += a[idx]
            idx -= step
        
        out.append(str(ans))
    
    return "\n".join(out)

# provided samples (abbreviated check)
assert run("""6
2 4
0 24 34 58 62 64 69 78
2 2
27 61 81 91
4 3
2 4 16 18 21 27 36 53 82 91 92 95
3 4
3 11 12 22 33 35 38 67 69 71 94 99
2 1
11 41
3 3
1 1 1 1 1 1 1 1 1
""") == """165
108
145
234
11
3"""

# custom cases
assert run("""1
1 5
5 4 3 2 1
""") == "15"

assert run("""1
2 1
100 200
""") == "100"

assert run("""1
3 2
1 2 3 4 5 6
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | sum | trivial median behavior |
| k=1 case | single median | full array median correctness |
| mixed case | 8 | spacing correctness |

## Edge Cases

When $n = 1$, every element is its own group and also its own median. The algorithm reduces to selecting every element with step 1. The index arithmetic still works because $m = 1$ gives `step = n - m + 1 = 1`, so we simply sum the entire array.

When $k = 1$, we only pick one element. The starting index becomes the correct median position of the whole array, since `step` aligns the first chosen index with the global median position. The algorithm effectively returns the central element of the sorted array.

When all values are equal, every grouping yields identical medians. The algorithm still selects evenly spaced elements but the sum remains consistent regardless of partitioning, confirming correctness under degeneracy.

In boundary cases where $n$ is large and $k$ is small, the step size ensures we never over-consume elements, because each chosen median implicitly reserves enough elements to form a valid group around it.
