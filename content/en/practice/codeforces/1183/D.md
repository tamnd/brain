---
title: "CF 1183D - Candy Box (easy version)"
description: "We are given several independent candy collections. Each collection is just a multiset of integers, where each integer represents a candy type. From each collection, we want to build a single “gift” by selecting some candies."
date: "2026-06-13T11:31:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 1400
weight: 1183
solve_time_s: 142
verified: true
draft: false
---

[CF 1183D - Candy Box (easy version)](https://codeforces.com/problemset/problem/1183/D)

**Rating:** 1400  
**Tags:** greedy, sortings  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent candy collections. Each collection is just a multiset of integers, where each integer represents a candy type. From each collection, we want to build a single “gift” by selecting some candies.

The restriction is on how many candies of each type we are allowed to take. If we pick some amount of a given type, that amount must be unique among all chosen types. For example, if we take 3 candies of type 5, then no other type in the gift is allowed to appear exactly 3 times. However, we could take 3 of type 5, 2 of type 7, 1 of type 9, and so on, as long as all these counts are distinct.

The goal for each query is to maximize the total number of candies in the gift.

The input size is large across queries, up to 2·10^5 total elements. This immediately rules out any quadratic reasoning over frequencies or greedy simulations that repeatedly adjust counts one-by-one per type. A solution must process each query in roughly linear or linearithmic time.

A subtle failure case appears when many types share the same frequency. For instance, if we have frequencies [5, 5, 5, 5], a naive approach might try to assign all of them value 5, but that violates uniqueness, and we must carefully decrease some counts while preserving maximal total sum.

Another tricky scenario is when frequencies are small but numerous, such as many types appearing once. Assigning all of them value 1 is invalid because counts must be distinct, so only one type can take 1, another must take 0, and so on.

These constraints make it clear that the problem is not about the identities of types, but only about their frequencies and how we assign distinct positive integers to a subset of them to maximize sum.

## Approaches

The first natural idea is to count how many candies each type has. Suppose we obtain frequencies f1, f2, ..., fk. Now we need to assign each chosen type a distinct positive integer x, where x ≤ fi, and maximize the sum of all chosen x.

A brute force idea is to try all subsets of types and all assignments of distinct values, checking feasibility and tracking the maximum sum. Even if we fix a subset, assigning distinct values is a permutation-like problem. The number of subsets is 2^k, and k can be large, so this quickly becomes infeasible even for small inputs.

A more structured brute force would try values from largest frequency downward, greedily assigning the largest available distinct numbers but recomputing conflicts. This still risks O(k^2) behavior when many frequencies are similar.

The key observation is that we never care which type gets which count, only that we assign strictly decreasing or at least distinct integers. To maximize the sum, we should always prefer larger assigned counts first, but we are limited by each frequency.

This transforms the problem into: we have a list of capacities fi, and we want to assign to each chosen element a distinct integer xi such that 1 ≤ xi ≤ fi, maximizing sum xi. The optimal strategy is to sort frequencies in descending order and greedily assign the largest possible unused integer, but never exceeding the frequency.

As we iterate through sorted frequencies, we maintain the next available integer value. If a frequency is smaller than or equal to or equal to the current available value, we clamp it down; otherwise we reduce it to maintain distinctness.

This works because any assignment that violates the sorted greedy structure can be rearranged to increase or preserve the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k · k) | O(k) | Too slow |
| Optimal Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We focus on one query and reduce it to frequency processing.

1. Count occurrences of each candy type.

We build a frequency array or dictionary that stores how many candies belong to each type. This compresses the input into at most n meaningful values.
2. Extract all non-zero frequencies into a list.

Only frequencies matter; types themselves are irrelevant after counting.
3. Sort frequencies in descending order.

This ensures we assign larger usable values first, which prevents wasting capacity on small assignments.
4. Initialize a variable `cur = infinity` (or a very large number).

This represents the largest allowed distinct count we can still assign.
5. Iterate over each frequency `f` in sorted order.

We assign `use = min(f, cur - 1)` because we must keep values strictly decreasing across types.

If `use` becomes negative or zero, we stop, since no valid positive distinct assignment remains.
6. Add `use` to the answer and update `cur = use`.

Each step ensures we always pick the largest possible valid distinct count for the current type while respecting previous assignments.

### Why it works

The core invariant is that after processing i frequencies, we have assigned strictly decreasing values to the chosen types, and at every step we never leave a feasible assignment unused. Sorting guarantees that we consider higher-capacity types first, and the greedy reduction ensures that if a frequency is too large to fit into the remaining “slots”, we compress it minimally. Any deviation from this choice would either violate uniqueness or replace a larger feasible assignment with a smaller one, reducing the total sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n = int(input())
        arr = list(map(int, input().split()))

        freq = {}
        for x in arr:
            freq[x] = freq.get(x, 0) + 1

        vals = sorted(freq.values(), reverse=True)

        cur = n
        ans = 0

        for f in vals:
            if cur <= 0:
                break
            use = min(f, cur)
            ans += use
            cur = use - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation first compresses the array into frequencies using a dictionary. This is necessary because types themselves are irrelevant after counting.

We sort frequencies in descending order so that larger groups are assigned first, maximizing the chance of using large distinct counts early.

The variable `cur` tracks the largest remaining integer we are allowed to assign. Each time we assign `use = min(f, cur)`, we ensure we do not exceed either the available frequency or the remaining allowed distinct value. Then we reduce `cur` to `use - 1` to maintain strict uniqueness.

A common implementation mistake is forgetting that assigned values must be strictly distinct. This is enforced entirely through `cur - 1`.

## Worked Examples

### Example 1

Input:

```
n = 8
a = [1, 4, 8, 4, 5, 6, 3, 8]
```

Frequencies:

| Type | Frequency |
| --- | --- |
| 1 | 1 |
| 3 | 1 |
| 4 | 2 |
| 5 | 1 |
| 6 | 1 |
| 8 | 2 |

Sorted frequencies: [2, 2, 1, 1, 1, 1]

We simulate:

| Step | f | cur | use | ans | next cur |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 8 | 2 | 2 | 1 |
| 2 | 2 | 1 | 1 | 3 | 0 |
| 3 | 1 | 0 | stop | 3 | - |

Final answer is 3.

This shows how large frequencies get truncated early because uniqueness forces rapid shrinking.

### Example 2

Input:

```
n = 9
a = [2, 2, 4, 4, 4, 7, 7, 7, 7]
```

Frequencies:

[4, 3, 2]

| Step | f | cur | use | ans | next cur |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 9 | 4 | 4 | 3 |
| 2 | 3 | 3 | 3 | 7 | 2 |
| 3 | 2 | 2 | 2 | 9 | 1 |

Final answer is 9.

This demonstrates how the greedy choice fully uses each frequency until constrained by uniqueness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting frequencies dominates each query |
| Space | O(n) | Frequency map and list of counts |

The sum of n over all queries is 2·10^5, so sorting within each query remains efficient overall. The greedy scan is linear in the number of distinct types.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 3 | decreasing assignment constraint |
| all distinct | 5 | each frequency is 1 |
| single type | 3 | long run truncation |
| mixed | 4 | interaction of different frequencies |

## Edge Cases

A key edge case is when many types have frequency 1. For input like [1, 2, 3, 4, 5], the algorithm assigns 1 to the first type, then must assign 0 to all others. The greedy reduction handles this naturally because cur quickly drops to 0.

Another case is when one type dominates, such as [1,1,1,1,1,1]. The first assignment uses 6, then 5, then 4, producing a staircase until exhaustion. The invariant ensures we never assign the same count twice.

A third case is alternating medium frequencies, such as [3,3,3,2,2]. Sorting ensures larger groups are processed first, preventing early blocking of higher possible assignments.
