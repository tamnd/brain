---
title: "CF 105272D - Dividing the solar pizzas"
description: "We are given an even number of friends, say 2n, and each friend has a single integer value representing a pizza flavor preference. The group wants to order exactly n pizzas, and each pizza must be made from two different friends’ preferences."
date: "2026-06-23T14:02:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105272
codeforces_index: "D"
codeforces_contest_name: "IX MaratonUSP Freshman Contest"
rating: 0
weight: 105272
solve_time_s: 42
verified: true
draft: false
---

[CF 105272D - Dividing the solar pizzas](https://codeforces.com/problemset/problem/105272/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an even number of friends, say 2n, and each friend has a single integer value representing a pizza flavor preference. The group wants to order exactly n pizzas, and each pizza must be made from two different friends’ preferences. Each preference value must be used exactly once, meaning we are pairing up all 2n numbers into n pairs.

Each pair forms one pizza, and the cost of a pizza is defined as the maximum of the two values in that pair. The goal is to choose a pairing strategy that minimizes the total sum of these maximums.

So the problem reduces to pairing 2n numbers into n pairs, minimizing the sum of pairwise maxima.

The constraints allow n up to 100,000, meaning up to 200,000 numbers. Any solution worse than O(n log n) risks being too slow. A quadratic pairing strategy that tries all pair combinations or uses dynamic programming over subsets is immediately impossible because it would involve roughly n² or 2^(2n) behavior, both far beyond feasible limits.

A subtle edge case arises when values are highly unbalanced. For example, if most values are small and one is extremely large, a naive greedy pairing that attaches the large value incorrectly can inflate the total cost. Consider input like 1 1 1 1 100. If paired poorly, 100 might end up increasing multiple pair costs in an indirect greedy scheme, but the optimal structure isolates it in exactly one pair.

Another edge case is when values are already sorted or nearly identical. In such cases, different pairing strategies might appear equivalent locally, but only one structure guarantees global optimality.

## Approaches

The brute-force idea is straightforward: try all possible ways to pair 2n elements and compute the sum of maxima for each pairing. This is correct because it explores every valid partition of the array into pairs. However, the number of pairings is (2n - 1)!!, which grows faster than exponential in n. Even for n = 20, this becomes infeasible, and at n = 100,000 it is completely impossible.

To improve, we look for structure in how pair maxima contribute to the total. Each pair contributes the larger of its two elements. If we sort the array, we gain control over which elements are likely to become maxima. The key observation is that to minimize wasted large values, we want to “pair large elements carefully so that each large element only pays once, and is not paired with something even larger unnecessarily.”

Sorting reveals that the optimal strategy is to pair adjacent elements in sorted order. This ensures that within each pair, the larger element is as small as possible among remaining choices. Any attempt to skip pairing adjacency risks pairing a large element with a much larger one later, increasing the sum.

So the problem reduces to sorting and summing every second element from the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n−1)!!) | O(n) | Too slow |
| Optimal (sort + greedy pairing) | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We start by sorting the array of 2n values in non-decreasing order.

1. Sort all values. This creates a global structure where local adjacency reflects closeness in value, which is crucial for minimizing the maximum in each pair.
2. Iterate from the largest value downward, stepping by two positions each time. In other words, take indices 2n−1, 2n−3, 2n−5, and so on.
3. Sum these selected elements. Each of these corresponds to the maximum of a pair formed with the element just before it in the sorted order.
4. Output the sum.

The pairing is implicitly: (a[0], a[1]), (a[2], a[3]), ..., (a[2n−2], a[2n−1]) after sorting. We do not explicitly construct pairs because only the maxima matter.

### Why it works

After sorting, consider any optimal pairing. Focus on the largest element. In any valid solution, it must be paired with some other element. The best possible partner for minimizing cost contribution is the largest remaining element that is as small as possible while still forming a valid pair. Pairing it with anything smaller does not reduce the cost, because the maximum is still the largest element itself. However, pairing large elements together avoids wasting the second-largest element as a separate maximum when it could be paired with a slightly smaller element. Repeating this argument inductively shows that pairing consecutive elements in sorted order yields an arrangement where each pair’s maximum is exactly one of the selected “second elements from the end,” and no rearrangement can reduce the sum further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = 0
    for i in range(2 * n - 1, -1, -2):
        ans += a[i]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading n and the 2n values. Sorting is essential because it aligns elements so that optimal pairing becomes a local decision rather than a global search problem.

The loop walks from the end of the array in steps of two, directly accumulating the elements that act as maxima in each optimal pair. We never explicitly build pairs because only the maximum contributes to the final answer.

A common implementation mistake is iterating incorrectly over indices, especially mixing n and 2n or stopping at the wrong boundary. The correct range is exactly 2n elements, and the stride must be two.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [5, 3, 4, 1, 2, 6]
```

After sorting:

```
[1, 2, 3, 4, 5, 6]
```

We pair adjacent elements:

(1,2), (3,4), (5,6)

| Step | Index chosen | Value | Running sum |
| --- | --- | --- | --- |
| 1 | 5 | 6 | 6 |
| 2 | 3 | 4 | 10 |
| 3 | 1 | 2 | 12 |

Output is 12.

This trace shows that taking every second element from the end correctly captures the maximum of each optimal pair.

### Example 2

Input:

```
n = 2
a = [10, 1, 9, 2]
```

After sorting:

```
[1, 2, 9, 10]
```

Pairs are:

(1,2), (9,10)

| Step | Index chosen | Value | Running sum |
| --- | --- | --- | --- |
| 1 | 3 | 10 | 10 |
| 2 | 1 | 2 | 12 |

Output is 12.

This confirms that large values are isolated efficiently, and each contributes exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, linear scan afterward |
| Space | O(1) to O(n) | In-place sort plus input storage |

The input size up to 200,000 elements makes sorting the only feasible heavy operation. The linear scan after sorting ensures the solution remains well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n = int(input().strip())
        a = list(map(int, input().split()))
        a.sort()
        ans = 0
        for i in range(2 * n - 1, -1, -2):
            ans += a[i]
        print(ans)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# sample-like cases
assert run("3\n5 3 4 1 2 6\n") == "12"
assert run("2\n10 1 9 2\n") == "12"

# minimum case
assert run("1\n5 1\n") == "5"

# all equal
assert run("3\n4 4 4 4 4 4\n") == "12"

# already sorted
assert run("2\n1 2 3 4\n") == "6"

# reverse sorted
assert run("2\n4 3 2 1\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 1 | 5 | minimum edge case |
| all equal | 12 | symmetry correctness |
| sorted / reverse sorted | 6 | stability under ordering |

## Edge Cases

When all values are identical, sorting produces no meaningful structure change. The algorithm still pairs adjacent elements and sums every second element from the end, which yields exactly n times the same value. For input 4 4 4 4 4 4, sorted array remains unchanged, and the sum becomes 12 for n = 3, matching any valid pairing.

When the array is already sorted in ascending order, such as 1 2 3 4, the algorithm pairs (1,2) and (3,4). The selection of 2 and 4 as maxima is consistent with stepping through every second element from the end, and no alternative pairing can reduce the sum because any cross pairing like (1,4) forces (2,3) and increases the total.

When values are reverse sorted, such as 4 3 2 1, sorting normalizes the structure first. The same logic applies, and the algorithm behaves identically after sorting, ensuring that input order never affects correctness.
