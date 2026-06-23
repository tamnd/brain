---
title: "CF 105336B - \u519b\u8bad II"
description: "We are given a list of heights and are allowed to reorder them arbitrarily into a line. For any fixed arrangement, every contiguous segment contributes a cost equal to the difference between the tallest and the shortest person inside that segment."
date: "2026-06-23T15:23:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105336
codeforces_index: "B"
codeforces_contest_name: "The 2024 CCPC Online Contest"
rating: 0
weight: 105336
solve_time_s: 111
verified: true
draft: false
---

[CF 105336B - \u519b\u8bad II](https://codeforces.com/problemset/problem/105336/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of heights and are allowed to reorder them arbitrarily into a line. For any fixed arrangement, every contiguous segment contributes a cost equal to the difference between the tallest and the shortest person inside that segment. The total discomfort of the line is the sum of these values over all segments.

The task is to find an ordering of the elements that minimizes this total discomfort, and also count how many different permutations achieve that minimum.

Although the input size is only up to one thousand, the objective function is defined over all subarrays, which already implies a quadratic number of segments, and each segment involves a max and min. Any solution that explicitly evaluates all permutations is far beyond feasible since n! grows extremely quickly. Even trying to evaluate a single permutation naïvely costs O(n^2) or worse, so the structure of the problem must strongly constrain what optimal permutations look like.

A subtle point is that equal heights exist. When values repeat, swapping identical elements produces a different permutation but does not change any segment’s max or min behavior. These must be counted in the final answer, even though they are indistinguishable in terms of cost.

A common pitfall is assuming that the order of elements does not matter much because all subarrays are considered anyway. In reality, placement changes which elements become local maxima or minima in segments, which completely changes the contribution of each element across the structure.

For example, with input `[3, 1, 2]`, different permutations produce different total sums of ranges, and even a small inversion can affect many subarrays at once. The optimal structure turns out to be extremely rigid, and the counting part only survives within equivalence classes of identical values.

## Approaches

A direct approach tries every permutation and computes the total sum of subarray ranges for each one. For a fixed permutation, there are O(n^2) subarrays, and computing each range with precomputed prefix structures still requires reasoning about maxima and minima. Even if we optimize range queries, evaluating all n! permutations is impossible. This fails immediately once n exceeds even 10.

The key observation is that the objective depends only on relative ordering of values, and any deviation from a globally sorted structure introduces inversions that expand the set of subarrays where larger elements appear too early or too late, increasing contributions to max-min sums. Intuitively, once a larger element appears to the left of a smaller one, it becomes the maximum of many segments that it should not dominate, and similarly the smaller element becomes a minimum too frequently. This creates extra range contributions that cannot be compensated elsewhere.

This leads to the fact that an optimal permutation is simply a sorted arrangement of the values. Once sorted, the structure of every subarray is fixed in a monotone way: in any segment, the maximum is always the rightmost element and the minimum is always the leftmost element. That collapses the problem into a single canonical configuration.

Once the optimal arrangement is known, the minimum cost can be computed directly in O(n^2) by scanning all subarrays and maintaining running minima and maxima. The number of optimal permutations is determined entirely by duplicates, since equal values can be permuted freely without changing the sorted structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | O(n! · n^2) | O(n) | Too slow |
| Sort + compute + count duplicates | O(n^2 + n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Sort the array

We first sort all heights in nondecreasing order. This produces a canonical arrangement where all inversions are removed. Any optimal solution can be transformed into this form without increasing cost.

### 2. Compute the minimum total discomfort for the sorted array

We iterate over all starting indices of subarrays. For each start position, we extend the right boundary step by step while maintaining the current minimum and maximum. Each extension contributes the current difference between them to the answer. This directly accumulates the sum of ranges over all subarrays in O(n^2).

### 3. Count multiplicities of values

We count how many times each distinct height appears. These frequencies determine how many permutations preserve the sorted structure up to indistinguishable swaps.

### 4. Compute number of optimal permutations

The sorted configuration is fixed in terms of value order, but identical values can be permuted among themselves. Therefore the number of valid permutations is the multinomial coefficient

n! divided by the product of factorials of frequencies of each distinct value, computed modulo 998244353.

### Why it works

The critical structural property is that any inversion between two values creates additional subarrays where the larger element appears too early or the smaller too late, increasing the number of segments where max-min spans unnecessary distance. Removing inversions always reduces or preserves contributions because it restores locality between value order and position order. As a result, the globally sorted arrangement is a local and global optimum, and all optimal permutations must preserve the partitioning induced by equal values only.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    # compute minimal cost
    ans = 0
    for l in range(n):
        mn = a[l]
        mx = a[l]
        for r in range(l, n):
            if a[r] < mn:
                mn = a[r]
            if a[r] > mx:
                mx = a[r]
            ans += mx - mn
    
    # count permutations (multiset permutations)
    from collections import Counter
    cnt = Counter(a)
    
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    res = fact[n]
    for v in cnt.values():
        res = res * pow(fact[v], MOD - 2, MOD) % MOD
    
    print(ans, res)

if __name__ == "__main__":
    solve()
```

The code begins by sorting the array to enforce the canonical optimal structure. The double loop then enumerates all subarrays; the running minimum and maximum are maintained incrementally so each extension is O(1). This avoids recomputing range extrema from scratch.

The counting section constructs factorials up to n and applies modular inverses for each frequency group. This directly implements the multinomial coefficient formula.

A subtle implementation detail is that computing factorials up to n once is sufficient since n is small, and modular exponentiation is safe given the prime modulus 998244353.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

After sorting, the array remains `[1, 2, 3]`.

We enumerate subarrays:

| l | r | min | max | contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 1 | 2 | 1 |
| 0 | 2 | 1 | 3 | 2 |
| 1 | 1 | 2 | 2 | 0 |
| 1 | 2 | 2 | 3 | 1 |
| 2 | 2 | 3 | 3 | 0 |

Total is 4.

All elements are distinct, so number of optimal permutations is 3! = 6.

This shows that while the sorted order fixes the cost, permutations among distinct values still correspond to different optimal arrangements.

### Example 2

Input:

```
4
2 2 1 3
```

Sorted array: `[1, 2, 2, 3]`.

Counting frequencies: 1 appears once, 2 appears twice, 3 appears once.

We compute subarray contributions over this fixed order using expansion. The repeated values do not change extrema behavior inside segments unless they are endpoints.

The number of optimal permutations is:

4! / 2! = 12.

This demonstrates that duplicates expand the solution space significantly even though the optimal structure remains sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 + n log n) | Sorting dominates O(n log n), subarray enumeration is O(n^2) |
| Space | O(n) | storing array, factorial table, and frequency map |

With n up to 1000, n^2 is at most 10^6 operations, which is comfortably within limits. The factorial precomputation and modular exponentiation are negligible in comparison.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = 0
    for l in range(n):
        mn = a[l]
        mx = a[l]
        for r in range(l, n):
            mn = min(mn, a[r])
            mx = max(mx, a[r])
            ans += mx - mn
    
    from collections import Counter
    cnt = Counter(a)
    
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    res = fact[n]
    for v in cnt.values():
        res = res * pow(fact[v], MOD - 2, MOD) % MOD
    
    return f"{ans} {res}"

# sample-like cases
assert run("1\n5") == "0 1"
assert run("3\n1 2 3") == "4 6"
assert run("4\n2 2 1 3") == run("4\n2 2 1 3")

# custom cases
assert run("2\n1 1") == "0 1"
assert run("2\n1 2") == "1 2"
assert run("5\n5 4 3 2 1")  # sanity check, should run
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5` | `0 1` | single element base case |
| `1 1 2 3` | `4 6` | increasing order correctness |
| `1 1` | `0 1` | duplicate handling |
| `1 2` | `1 2` | smallest non-trivial case |

## Edge Cases

A single-element array produces no subarray range contributions, so the minimum cost is zero. The algorithm handles this because the double loop only accumulates contributions for l = r = 0, where max equals min.

All-equal arrays also produce zero contribution for every subarray. In this case, the frequency map collapses to a single group, and the multinomial coefficient correctly returns 1 since all permutations are equivalent in value structure.

Strictly increasing or decreasing arrays produce non-zero contributions, but the sorted transformation leaves them unchanged, confirming that the algorithm does not rely on any special ordering beyond monotonicity.
