---
title: "CF 34B - Sale"
description: "Bob is at a sale with a collection of old TVs, each with a price. Some TVs are free, some have positive prices, and some"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 34
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 34 (Div. 2)"
rating: 900
weight: 34
solve_time_s: 79
verified: true
draft: false
---

[CF 34B - Sale](https://codeforces.com/problemset/problem/34/B)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Bob is at a sale with a collection of old TVs, each with a price. Some TVs are free, some have positive prices, and some even have negative prices, which means the owner is willing to pay Bob to take them away. Bob can carry at most _m_ TVs, and he wants to maximize the total money he can earn. The input gives the number of TVs _n_, the carrying limit _m_, and the array of TV prices. The output is the maximum sum of money Bob can earn by picking at most _m_ TVs.

The constraints are small: _n_ and _m_ are at most 100, and TV prices are between -1000 and 1000. This means we can afford algorithms with time complexity up to roughly O(n log n) or even O(n²) without worrying about efficiency.

A subtle point is that Bob only benefits from TVs with negative prices. Picking a TV with a positive price reduces his total gain. A naive implementation that sums the cheapest TVs blindly without checking their sign would incorrectly include positive prices and lower the total money. For example, if _n = 5_, _m = 3_, and prices are `-5 2 4 1 3`, the correct answer is `5` (only pick `-5`), not `2 + 4 + 1 = 7` which a careless approach might do if it just sorted ascending and summed the first three.

Another edge case is when there are fewer than _m_ TVs with negative prices. In that case, Bob should only take the available negative prices and ignore the rest, since taking free or positive TVs does not increase his gain.

## Approaches

The brute-force method would consider every subset of TVs of size up to _m_ and compute the total money for each subset. For each combination, Bob sums the negative prices. This is correct because it checks all possibilities, but it is exponential in complexity: there are O(2ⁿ) subsets. With _n = 100_, this is clearly infeasible.

The key insight is that the only TVs that contribute positively to Bob's total are those with negative prices. Therefore, we only need to pick the smallest negative prices, up to _m_ TVs. Sorting the array in ascending order ensures that all negative prices come first. Then we can iterate through the first _m_ elements, summing only the negative values. This reduces the problem from considering all subsets to a simple sort followed by a linear scan.

The brute-force approach works because it explores all possibilities, but it fails when _n_ grows due to exponential combinations. The observation that only negative prices matter allows us to reduce the problem to sorting and summing a small prefix of the array, achieving an O(n log n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ) | O(n) | Too slow |
| Optimal | O(n log n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of TVs `n` and the carrying limit `m`, along with the array of prices.
2. Sort the array of prices in ascending order. This brings all negative prices to the front.
3. Initialize a variable `total` to 0. This will accumulate Bob's earnings.
4. Iterate over the first `m` elements of the sorted array.
5. For each price, if it is negative, add its absolute value (or equivalently subtract it) to `total`. If it is zero or positive, stop the iteration because further TVs do not increase the total.
6. Output the accumulated `total`.

This works because after sorting, the first `m` elements are the smallest, and only negative numbers contribute positively to Bob's gain. The invariant is that at any step, `total` equals the sum of absolute values of the negative prices Bob has chosen so far. No positive number will increase the sum, so ignoring them is safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
prices = list(map(int, input().split()))

prices.sort()
total = 0

for i in range(min(m, n)):
    if prices[i] < 0:
        total += -prices[i]
    else:
        break

print(total)
```

The code first reads `n` and `m` and the price list. Sorting ensures that negative prices are at the front. The loop iterates at most `m` times, stopping early if a non-negative price is encountered. Adding `-prices[i]` converts the negative cost into positive money earned. The `min(m, n)` ensures we never go out of bounds if `m > n`, though the problem guarantees `m ≤ n`.

## Worked Examples

### Example 1

Input: `5 3` and prices `-6 0 35 -2 4`

| Step | Sorted Prices | i | Price | Total |
| --- | --- | --- | --- | --- |
| 0 | -6 -2 0 4 35 | 0 | -6 | 6 |
| 1 |  | 1 | -2 | 8 |
| 2 |  | 2 | 0 | 8 |

Bob picks -6 and -2, earning 6 + 2 = 8. Iteration stops at 0 because no money is earned from non-negative prices.

### Example 2

Input: `4 2` and prices `1 -3 -2 0`

| Step | Sorted Prices | i | Price | Total |
| --- | --- | --- | --- | --- |
| 0 | -3 -2 0 1 | 0 | -3 | 3 |
| 1 |  | 1 | -2 | 5 |

Bob picks -3 and -2, earning 5. The two-TVs limit is reached.

These traces show that the algorithm always picks the most negative prices up to the carrying limit, maximizing earnings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime, iterating over at most m elements is O(n) in worst case |
| Space | O(1) or O(n) | Sorting may require O(n) additional space depending on implementation, otherwise we just use a single variable `total` |

Given n ≤ 100, O(n log n) operations are around 700 steps, far below the 2-second limit. Memory usage is negligible relative to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    prices.sort()
    total = 0
    for i in range(min(m, n)):
        if prices[i] < 0:
            total += -prices[i]
        else:
            break
    return str(total)

# provided sample
assert run("5 3\n-6 0 35 -2 4\n") == "8", "sample 1"

# custom test cases
assert run("5 3\n-5 2 4 1 3\n") == "5", "only negative TV picked"
assert run("3 3\n1 2 3\n") == "0", "all positive, pick none"
assert run("4 5\n-1 -2 -3 -4\n") == "10", "m > number of TVs negative"
assert run("1 1\n-1000\n") == "1000", "single negative TV"
assert run("2 1\n0 -1\n") == "1", "zero and negative, pick negative"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3, -5 2 4 1 3 | 5 | Only negative TV contributes |
| 3 3, 1 2 3 | 0 | All positive, earn nothing |
| 4 5, -1 -2 -3 -4 | 10 | m greater than number of negative TVs |
| 1 1, -1000 | 1000 | Single TV with large negative price |
| 2 1, 0 -1 | 1 | Zero and negative, pick negative |

## Edge Cases

If there are fewer negative prices than `m`, the algorithm still works. For input `4 5` and prices `-1 -2 -3 -4`, the sorted array is `-4 -3 -2 -1`. We iterate over all four negative prices, sum their absolute values to get `10`, and stop because there are no more TVs. Even though `m = 5`, we never access an out-of-bounds element. This confirms the algorithm handles the case where `m` exceeds the number of negative prices correctly.

When all prices are positive, such as `1 2 3` with `m = 3`, the first sorted element is 1, which is non-negative. The loop breaks immediately, and the total is `0`. This shows that the algorithm correctly avoids picking TVs that would reduce Bob's earnings.
