---
title: "CF 64D - Presents"
description: "We are given three positive integers representing the prices of three presents. There are three sisters, ranked by age: eldest, middle, and youngest."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "greedy"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "D"
codeforces_contest_name: "Unknown Language Round 1"
rating: 1800
weight: 64
solve_time_s: 100
verified: true
draft: false
---

[CF 64D - Presents](https://codeforces.com/problemset/problem/64/D)

**Rating:** 1800  
**Tags:** *special, greedy  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three positive integers representing the prices of three presents. There are three sisters, ranked by age: eldest, middle, and youngest. The task is to assign each present to a sister according to the rule that the most expensive present goes to the eldest sister, the second most expensive to the middle sister, and the cheapest to the youngest sister. If two presents have the same price, the corresponding sisters can receive them in any order.

The input consists of three integers $a_1, a_2, a_3$, each between 1 and 100. This is a tiny input size, which implies we can safely use any approach with constant time complexity. The problem is essentially about sorting three values while keeping track of their original positions. Edge cases arise when two or all three prices are equal. For example, if the prices are `5 5 10`, the eldest sister should get `10`, but the other two presents can be assigned to the middle and youngest sisters in any order. A naive implementation that just assigns positions based on comparison without handling equality can misassign the sisters in such cases.

## Approaches

The brute-force approach would enumerate all permutations of the three presents and check which permutation satisfies the ordering constraint. With three elements, there are 3! = 6 permutations, so this is feasible but unnecessary.

The key insight is that we only need to sort the presents by price while remembering their original indices. Once sorted, the highest price maps to the eldest sister, the middle price to the second sister, and the lowest price to the youngest. We can do this by pairing each price with its original index, sorting by price, and then assigning sisters accordingly. This approach is linear for three elements and trivially handles equality because Python’s sort is stable.

The brute-force works because checking all permutations guarantees correctness, but it fails in general if the input size grows. The observation that the problem reduces to sorting with index tracking lets us solve it in constant time with zero risk of misassignment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Acceptable but overkill |
| Sorting with indices | O(1) | O(1) | Optimal, accepted |

## Algorithm Walkthrough

1. Read the three integers representing present prices. Store them in a list along with their original positions: `[(price, position), ...]`. This allows us to sort without losing track of which present is which.
2. Sort the list in descending order by price. This ensures that the most expensive present is first, the middle price is second, and the cheapest is last.
3. Assign the sisters according to this order. The first element in the sorted list corresponds to the eldest sister (1), the second to the middle sister (2), and the third to the youngest sister (3).
4. Build an output list where the i-th position indicates which sister receives the i-th present in the original order. Use the stored positions from step 1 to place the sister numbers correctly.
5. Print the final list of sister assignments.

The invariant is that at each point after sorting, the price order strictly matches the intended sister ranking. Since we only have three elements, sorting guarantees that no two sisters get misassigned except in the case of equal prices, which the stable sort handles automatically.

## Python Solution

```python
import sys
input = sys.stdin.readline

# read input
prices = list(map(int, input().split()))
# store original positions
indexed_prices = [(price, i) for i, price in enumerate(prices)]
# sort descending by price
indexed_prices.sort(reverse=True, key=lambda x: x[0])

# assign sisters: 1=eldest, 2=middle, 3=youngest
result = [0, 0, 0]
sisters = [1, 2, 3]
for sister, (_, idx) in zip(sisters, indexed_prices):
    result[idx] = sister

print(*result)
```

The code first creates tuples of `(price, original_index)` to preserve the mapping of presents to input positions. Sorting descending ensures that the most expensive present is at index 0, the second at index 1, and the cheapest at index 2. The `zip` with `[1,2,3]` assigns sister numbers in the correct order. Finally, we write the sister numbers back into the result array based on original positions, which produces the correct output.

## Worked Examples

### Sample 1

Input: `11 13 1`

| Step | Indexed Prices | Sorted | Assignment |
| --- | --- | --- | --- |
| Initial | [(11,0),(13,1),(1,2)] | [(13,1),(11,0),(1,2)] | 1->idx1, 2->idx0, 3->idx2 |
| Result |  |  | [2,1,3] |

Explanation: The present worth 13 goes to the eldest, 11 to the middle, 1 to the youngest. The original indices determine placement.

### Sample 2

Input: `5 5 10`

| Step | Indexed Prices | Sorted | Assignment |
| --- | --- | --- | --- |
| Initial | [(5,0),(5,1),(10,2)] | [(10,2),(5,0),(5,1)] | 1->idx2, 2->idx0, 3->idx1 |
| Result |  |  | [2,3,1] |

This demonstrates handling equal prices correctly. Both 5-value presents are interchangeable for middle and youngest sisters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting three elements is constant time |
| Space | O(1) | Only three tuples and a result array of size 3 are used |

Even with the largest possible inputs (all prices 100), the algorithm completes in negligible time and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    prices = list(map(int, input().split()))
    indexed_prices = [(price, i) for i, price in enumerate(prices)]
    indexed_prices.sort(reverse=True, key=lambda x: x[0])
    result = [0,0,0]
    sisters = [1,2,3]
    for sister, (_, idx) in zip(sisters, indexed_prices):
        result[idx] = sister
    return " ".join(map(str,result))

# provided samples
assert run("11 13 1\n") == "2 1 3", "sample 1"
assert run("5 5 10\n") in ["2 3 1","3 2 1"], "sample 2"

# custom cases
assert run("1 2 3\n") == "3 2 1", "ascending order"
assert run("100 100 100\n") in ["1 2 3","1 3 2","2 1 3","2 3 1","3 1 2","3 2 1"], "all equal"
assert run("50 100 50\n") in ["1 2 3","3 2 1"], "two equal max/med"
assert run("1 1 100\n") in ["2 3 1","3 2 1"], "two equal min"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3` | `3 2 1` | ascending order mapping to sisters |
| `100 100 100` | any permutation | all equal values |
| `50 100 50` | `1 2 3` or `3 2 1` | two equal values in non-max position |
| `1 1 100` | `2 3 1` or `3 2 1` | two equal values in min position |

## Edge Cases

For input `50 100 50`, after sorting we get `[(100,1),(50,0),(50,2)]`. Eldest gets present at index 1, middle and youngest get the remaining two. The algorithm correctly handles equal 50-value presents.

For input `100 100 100`, sorting yields the same list but any order of assignment is valid. The stable sort and index mapping guarantee that the original positions are respected, producing one valid permutation of sister numbers.

For input `1 1 100`, the most expensive present goes to the eldest, while the two cheapest (both 1) can be assigned to the middle and youngest sisters in any order. The algorithm handles this correctly because it iterates through the sorted list in order and assigns sister numbers sequentially.
