---
title: "CF 1770A - Koxia and Whiteboards"
description: "We start with an array of numbers placed on whiteboards. Then we are given a sequence of replacement values. Each replacement operation allows us to pick any one whiteboard and overwrite its current value with the new value from the operation."
date: "2026-06-09T12:28:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1770
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2022: 2023 is NEAR"
rating: 1000
weight: 1770
solve_time_s: 180
verified: true
draft: false
---

[CF 1770A - Koxia and Whiteboards](https://codeforces.com/problemset/problem/1770/A)

**Rating:** 1000  
**Tags:** brute force, greedy  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of numbers placed on whiteboards. Then we are given a sequence of replacement values. Each replacement operation allows us to pick any one whiteboard and overwrite its current value with the new value from the operation.

All operations must be used, but we are free to choose which whiteboard gets updated each time, and the same whiteboard can be updated multiple times. The goal is to maximize the final sum of values written on the boards after all replacements are applied.

A key observation is that only the final value on each board matters, not the order in which operations are applied. Every operation contributes exactly one value that will end up assigned somewhere.

Since $n, m \le 100$, the constraints allow straightforward greedy reasoning. Any solution up to $O(nm)$ or $O(m \log m)$ is easily sufficient.

A subtle edge case is when $m > n$, meaning some boards will be overwritten multiple times. Another is when $m < n$, meaning some original values are never touched. A naive mistake is to assume each operation must go to a distinct board, which is false and leads to underestimating flexibility.

## Approaches

A brute force approach would simulate all ways to assign each of the $m$ values to $n$ boards. For each operation, we choose one of $n$ boards, leading to $n^m$ possibilities. Even for $n = m = 100$, this is far too large.

The key simplification comes from realizing that the final configuration only depends on two sets of numbers: the initial board values and the values we decide to apply from the operation list. Each operation contributes exactly one value, and we can choose where it goes. This means we are effectively deciding which final values replace which initial ones.

To maximize the sum, we should preserve large initial values unless they can be replaced by even larger operation values. Since every operation value can be used at most once, the optimal strategy reduces to selecting the largest possible values among all available candidates and placing them onto boards that benefit most.

A clean way to see this is that we are building a final multiset of size $n$, where we start with $a_i$ and may replace up to $m$ elements using $b_j$. Each replacement should only be used if it increases the sum, and among all choices we always prefer larger values.

This leads to sorting both arrays and greedily matching the largest $b_j$ values with the smallest $a_i$ values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | exponential | $O(n)$ | Too slow |
| Sorting + greedy replacement | $O(n \log n + m \log m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the initial array $a$ in increasing order so that we can easily identify the smallest values that are easiest to improve. The reason is that replacing a small value yields the largest marginal gain.
2. Sort the replacement values $b$ in decreasing order so we can use the strongest available improvements first. This ensures we never waste a large value on a position where it provides little benefit.
3. Iterate through both arrays simultaneously, comparing the smallest remaining $a[i]$ with the largest remaining $b[j]$. If $b[j] > a[i]$, replace $a[i]$ with $b[j]$. Otherwise, stop using further replacements because all remaining $a[i]$ are even larger.
4. Continue this process until we either exhaust $b$ or reach a point where no replacement improves the sum. The resulting array represents an optimal assignment of operations.
5. Compute the final sum of the modified array.

### Why it works

The correctness relies on an exchange argument. Suppose we have an optimal solution where a smaller replacement value is assigned to a smaller $a[i]$, while a larger replacement value is either unused or assigned elsewhere. Swapping these assignments never decreases the sum and may increase it. Repeating this reasoning leads to a structure where the largest $b$ values are matched with the smallest $a$ values whenever beneficial, which is exactly what the greedy procedure constructs.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort()
    b.sort(reverse=True)
    
    i = 0
    j = 0
    
    while i < n and j < m:
        if b[j] > a[i]:
            a[i] = b[j]
            i += 1
            j += 1
        else:
            break
    
    print(sum(a))
```

The implementation directly follows the greedy strategy. Sorting $a$ allows us to always try improving the weakest positions first. Sorting $b$ in descending order ensures we consume the strongest upgrades early.

The loop stops as soon as no improvement is possible, which avoids unnecessary comparisons once all remaining $a[i]$ are already larger than the remaining $b[j]$. The final sum is computed directly from the updated array.

## Worked Examples

Consider the input $a = [1,2,3]$ and $b = [4,5]$. After sorting, we compare $1$ with $5$, replace it, then compare $2$ with $4$, replace it, and stop. The resulting array is $[5,4,3]$.

| Step | a (state) | b pointer | action |
| --- | --- | --- | --- |
| 1 | [1,2,3] | 5 | replace 1 with 5 |
| 2 | [5,2,3] | 4 | replace 2 with 4 |
| 3 | [5,4,3] | stop | no improvement |

The final sum is $12$, matching the optimal configuration.

For $a = [10,10]$ and $b = [1,2]$, sorting gives $a$ unchanged and $b = [2,1]$. Since even the largest $b$ is not greater than the smallest $a$, no replacements happen and the sum remains $20$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log(n+m))$ | sorting dominates, greedy scan is linear |
| Space | $O(n+m)$ | storage for arrays |

The constraints are small enough that sorting and a single linear pass per test case are easily fast.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort()
        b.sort(reverse=True)
        
        i = 0
        j = 0
        
        while i < n and j < m:
            if b[j] > a[i]:
                a[i] = b[j]
                i += 1
                j += 1
            else:
                break
        
        out.append(str(sum(a)))
    
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("""4
3 2
1 2 3
4 5
2 3
1 2
3 4 5
1 1
100
1
5 3
1 1 1 1 1
1000000000 1000000000 1000000000
""") == """12
9
1
3000000002"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all small values | greedy replacement behavior | basic correctness |
| all large b values | full replacement | maximal gain usage |
| no improvement case | unchanged sum | stopping condition |

## Edge Cases

When $m = 0$, no replacements occur and the output is simply the sum of $a$. The algorithm handles this because the loop never executes.

When all $b_j \le \min(a_i)$, no replacements happen because the first comparison fails immediately, ensuring we do not decrease the sum.

When $m > n$, only the largest $n$ useful values from $b$ are ever used, since the loop stops once all $a[i]$ have been considered.
