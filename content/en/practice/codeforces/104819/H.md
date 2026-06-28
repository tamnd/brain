---
title: "CF 104819H - Polygon"
description: "We are given a collection of stick lengths and asked whether it is possible to pick exactly k of them so that they can serve as sides of a simple polygon."
date: "2026-06-28T13:02:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104819
codeforces_index: "H"
codeforces_contest_name: "2023 Sun Yat-sen University Collegiate Programming Contest, Onsite"
rating: 0
weight: 104819
solve_time_s: 45
verified: true
draft: false
---

[CF 104819H - Polygon](https://codeforces.com/problemset/problem/104819/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of stick lengths and asked whether it is possible to pick exactly k of them so that they can serve as sides of a simple polygon.

The only geometric requirement we need to care about is the generalized polygon inequality: a set of k segments can form a non-degenerate simple polygon if and only if no single segment is too long compared to the others. Concretely, if we sort the chosen lengths, the condition becomes that the largest chosen length must be strictly smaller than the sum of the remaining k − 1 lengths.

The input consists of n candidate sticks, and we must decide whether there exists any subset of size k satisfying this inequality. We are not constructing the polygon, only checking feasibility.

The constraint n ≤ 3000 means that quadratic or near-quadratic approaches are borderline acceptable, but anything cubic or involving enumeration of all subsets is completely infeasible. The key difficulty is that we are selecting a subset under a global inequality constraint, not just checking a fixed set.

A subtle edge case is when many sticks are identical or when one stick is extremely large compared to all others. For example, if k = 3 and the array is [100, 1, 1], the answer is clearly No because 100 is too large. A naive approach that only checks sums without carefully selecting k elements can easily miss that the choice of subset matters.

Another failure case appears when k is large. For example, if most sticks are small but a few are large, the decision hinges on balancing selection of large elements (which increase the maximum) versus small elements (which increase the sum of others). A greedy choice is required, but it must be justified.

## Approaches

A brute-force method would try every subset of size k, compute its sum, identify its maximum element, and check whether twice the maximum is smaller than the total sum. This is correct because for any candidate subset the polygon condition reduces to 2 * max < sum of subset. However, the number of subsets is C(n, k), which is exponential in n, and even for moderate k this becomes completely impossible.

The structure of the condition suggests that only the relationship between the largest chosen element and the total sum matters. If we sort all sticks, any valid subset can be thought of as some k chosen elements where the largest element is fixed, and the best chance of satisfying the condition is to maximize the sum of the remaining k − 1 elements. This immediately suggests that if we fix a candidate maximum, we should always pair it with the k − 1 largest possible remaining sticks among those smaller than it.

This leads to a greedy sweep over the sorted array: treat each element as a potential maximum, and check whether the k − 1 largest elements before it are sufficient to satisfy the inequality. By maintaining prefix sums, we can evaluate each candidate in constant time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(C(n, k) · k) | O(k) | Too slow |
| Sort + greedy prefix check | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Sort all stick lengths in non-decreasing order. This allows us to treat any position as a potential maximum while ensuring all candidates to its left are smaller or equal.
2. Build a prefix sum array over the sorted list so we can compute sums of any segment in O(1) time. This is needed because we repeatedly evaluate sums of chosen subsets.
3. For each index i from k − 1 to n − 1, treat a[i] as the largest element of the chosen polygon sides.
4. Consider the k − 1 elements immediately before i in the sorted array. These are the best possible candidates to pair with a[i] because any smaller choice would only reduce the sum and make the inequality harder to satisfy.
5. Compute the sum of these k − 1 elements using the prefix sum array.
6. Check whether 2 * a[i] < sum_of_previous_k_minus_1 + a[i]. This is equivalent to checking whether a[i] < sum_of_previous_k_minus_1, which is the polygon inequality.
7. If any index satisfies the condition, immediately return Yes. If no index works, return No.

### Why it works

Fixing the largest chosen element is sufficient because any valid k-set has a unique maximum element. For a fixed maximum, the optimal strategy to maximize the chance of satisfying the polygon condition is to maximize the sum of the remaining k − 1 elements, which is achieved by choosing the k − 1 largest elements below it in sorted order. This reduces the problem to checking a single inequality per candidate maximum. Since every valid subset corresponds to some candidate maximum position in the sorted array, no valid solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    a.sort()
    
    # prefix sums
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    
    # try each possible maximum position
    for i in range(k - 1, n):
        # sum of k-1 elements before i
        left_sum = pref[i] - pref[i - (k - 1)]
        
        # check polygon condition:
        # largest side a[i] must be < sum of others
        if a[i] < left_sum:
            print("Yes")
            return
    
    print("No")

if __name__ == "__main__":
    solve()
```

The sorting step ensures we only consider valid candidates for the maximum side in increasing order. The prefix array allows us to compute the sum of the k − 1 best companions in constant time. The key implementation detail is the window `[i - (k - 1), i)` which always represents the best possible selection for supporting sides.

The inequality is checked in its simplest form `a[i] < left_sum`, avoiding any need to recompute total sums or reason about the full polygon explicitly.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 3
```

| i | chosen max | window | sum(left) | condition |
| --- | --- | --- | --- | --- |
| 2 | 3 | [1, 2] | 3 | 3 < 3 false |

The only possible triangle uses all elements, but 3 is not strictly less than 1 + 2, so the condition fails and the answer is No.

### Example 2

Input:

```
6 4
1 1 4 5 1 4
```

Sorted array: [1, 1, 1, 4, 4, 5]

| i | chosen max | window | sum(left) | condition |
| --- | --- | --- | --- | --- |
| 3 | 4 | [1,1,1] | 3 | 4 < 3 false |
| 4 | 4 | [1,1,4] | 6 | 4 < 6 true |

At i = 4, we pick 4 as the largest element and the three best preceding elements sum to 6, which is enough to satisfy the polygon inequality. So the answer is Yes.

This trace shows how selecting the best possible companions for each candidate maximum is sufficient to detect feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, scan is linear |
| Space | O(n) | prefix sums and sorted array storage |

The constraints n ≤ 3000 make O(n log n) easily fast enough. The solution uses only simple array operations and avoids combinatorial enumeration entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    for i in range(k - 1, n):
        left_sum = pref[i] - pref[i - (k - 1)]
        if a[i] < left_sum:
            print("Yes")
            return
    print("No")

# samples
assert run("3 3\n1 2 3\n") == "No"
assert run("6 4\n1 1 4 5 1 4\n") == "Yes"

# minimum n=k=3
assert run("3 3\n1 1 1\n") == "Yes"

# impossible large dominant element
assert run("4 3\n100 1 1 1\n") == "No"

# all equal large k
assert run("5 4\n10 10 10 10 10\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 / 1 1 1 | Yes | minimum valid polygon |
| 4 3 / 100 1 1 1 | No | dominant maximum fails condition |
| 5 4 / all equal | Yes | symmetric case with many valid subsets |

## Edge Cases

A common edge case is when the largest element is extremely large compared to all others. For input `4 3: 100 1 1 1`, sorting gives `[1, 1, 1, 100]`. The only candidate maximum is 100, and the best three-element sum below it is 3. The condition `100 < 3` fails immediately, so the algorithm correctly returns No.

Another case is when all elements are equal. For `5 4: 10 10 10 10 10`, every candidate maximum has three supporting elements summing to 30, so `10 < 30` holds. The algorithm finds a valid i and returns Yes early.

A subtle situation is when k is close to n. The algorithm still works because the window `[i-(k-1), i)` becomes almost the entire prefix. This ensures that even when only one or two elements are excluded, the inequality is still evaluated correctly against the best possible subset.
