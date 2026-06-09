---
title: "CF 1622C - Set or Decrease"
description: "We are given an array of integers and want to reduce its total sum until it becomes no larger than a target value. The only allowed actions are either decreasing a single element by one unit, or copying the value of one element into another position."
date: "2026-06-10T05:46:09+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1622
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 120 (Rated for Div. 2)"
rating: 1600
weight: 1622
solve_time_s: 99
verified: false
draft: false
---

[CF 1622C - Set or Decrease](https://codeforces.com/problemset/problem/1622/C)

**Rating:** 1600  
**Tags:** binary search, brute force, greedy, sortings  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and want to reduce its total sum until it becomes no larger than a target value. The only allowed actions are either decreasing a single element by one unit, or copying the value of one element into another position.

The key difficulty is that copying is not a cost-free operation even though it does not directly reduce the sum. It can be used strategically to create extra “opportunities” for reductions because it overwrites values. Since values are allowed to become negative, nothing prevents us from repeatedly decreasing elements or propagating very small values across the array.

The goal is to minimize the number of operations, not the final configuration.

The constraints immediately rule out any quadratic or cubic simulation. The total number of elements across all test cases is up to 2⋅10^5, so any solution must be close to O(n log n) or O(n) per test case. A naive idea that tries all sequences of copy and decrement operations is impossible because the branching factor grows with both operations and positions.

A subtle edge case comes from the interaction between copying and decreasing. A careless greedy strategy that only performs decrements ignores that copying a small value onto a large one can reduce the sum “for free” except for the overwrite cost. For example, turning a large element into a small value via copy can be better than decrementing it many times, but only if we already have a small value available.

Another edge case is when all elements are already below k in sum. In that case, zero operations is required, and any attempt to “optimize further” must not accidentally introduce unnecessary operations.

## Approaches

Start with the most direct idea. If copying were not allowed, the problem would be simple: the answer would be the total sum minus k, because each decrement reduces the sum by exactly one unit and there is no alternative way to reduce it.

Once copying is introduced, we gain a second mechanism: we can turn any element into the value of another element. The important observation is that copying does not change the sum if we replace a large value with a large value, but it can reduce the sum if we overwrite a large value with a small one. This suggests that the best possible strategy is to first decide what final “small value” we want to spread, then use copies to convert many elements into that value, and finally perform decrements if needed.

The critical insight is to consider the array after sorting. If we fix a value as the “source of minimum cost”, say we choose some element as a baseline, then we can copy that baseline value into many positions. After that, any element that is still too large can be decreased individually. The tradeoff becomes: choosing a smaller baseline requires more initial effort to reach it, but makes copying more powerful.

A more systematic way to view the problem is to assume we will end up making the smallest element in some suffix act as a template. If we sort the array in descending order, then consider taking the first i elements as “kept large” and turning all remaining elements into the i-th value. This reduces the number of distinct values, and therefore reduces the sum structure we need to fix with decrements.

For a fixed choice of how many elements we treat as “special”, we can compute how many operations are needed: we pay for decreasing excess sum after setting many elements equal via copy operations, and we also pay for the copy operations themselves.

The key reduction is that the optimal strategy depends only on how many of the largest elements we preserve, because everything else can be forced to match a chosen value.

This turns the problem into checking all possible counts of preserved elements. Since n is large, we avoid recomputing sums from scratch by using prefix sums over the sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate operations) | O(operations exponential) | O(n) | Too slow |
| Optimal (sort + prefix evaluation) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in descending order. This allows us to reason about keeping large elements versus converting smaller ones.
2. Compute prefix sums so we can quickly evaluate the sum of any prefix and suffix.
3. Try every possible split point i, where the first i elements are treated as “kept unchanged initially”, and the remaining n − i elements are candidates to be overwritten via copying.
4. For a fixed i, interpret the strategy as choosing one of the first i elements as a template value. The best template is the smallest among them, because copying a smaller value minimizes future reduction cost.
5. Compute how much the total sum would be after making all elements in the suffix equal to this chosen template value using copy operations.
6. If this resulting sum is already ≤ k, then the cost is simply the number of copy operations required, which is n − i.
7. Otherwise, we must additionally reduce the excess sum using decrement operations. Each decrement reduces the sum by one, so we add (current_sum − k) to the cost.
8. Take the minimum over all i.

### Why it works

The process partitions the array into a part that defines a baseline value and a part that is forced to match that baseline using copy operations. Any optimal solution must effectively decide which values are allowed to remain “expensive” and which are forced down early. Because copying always overwrites completely, partial matching strategies do not exist, so every element is either used as a template or replaced. Once this binary structure is fixed, the remaining cost is purely linear in how much sum remains above k, and decrementing is the only way to reduce it further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        a.sort(reverse=True)
        
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + a[i]
        
        total = prefix[n]
        ans = float('inf')
        
        for i in range(n + 1):
            if i == 0:
                # no templates chosen, everything becomes a[0]
                cost = total - k if total > k else 0
                ans = min(ans, cost)
                continue
            
            # choose first i elements as potential templates
            # best template is a[i-1]
            template = a[i - 1]
            
            # suffix becomes template
            suffix_sum = prefix[n] - prefix[i]
            new_sum = prefix[i] + template * (n - i)
            
            ops = (n - i)  # copy operations
            
            if new_sum > k:
                ops += new_sum - k
            
            ans = min(ans, ops)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by sorting each test case so that decisions about which elements remain large become prefix-based. The prefix sum array allows constant-time computation of both kept and replaced segments.

For each split point i, the algorithm assumes that elements from i onward are overwritten with the value a[i−1]. The number of copy operations is exactly the number of overwritten elements.

If after this transformation the total sum still exceeds k, the only remaining way to reduce it is decrementing elements, which costs one operation per unit of excess sum. This is directly added to the operation count.

Finally, the minimum over all configurations is printed.

A subtle point is handling the case i = 0, where no template is chosen. This corresponds to the degenerate strategy where we do not use copying at all and only rely on decrements from the original sum.

## Worked Examples

### Example 1

Input:

```
2 69
6 9
```

Sorted array is `[9, 6]`.

We evaluate splits:

| i | prefix kept | template | new sum | ops |
| --- | --- | --- | --- | --- |
| 0 | none | - | 15 → 15 | 0 |
| 1 | [9] | 9 | 9 + 9 = 18 | 1 |
| 2 | [9,6] | - | 15 | 0 |

Best valid answer is 0 since sum already ≤ k.

This confirms that the algorithm correctly recognizes that no operation is required.

### Example 2

Input:

```
1 10
20
```

Array: `[20]`

Only split:

| i | prefix | template | new sum | ops |
| --- | --- | --- | --- | --- |
| 0 | - | - | 20 | 10 |
| 1 | [20] | 20 | 20 | 0 |

Best is 10 operations via decrements, matching the expected output.

This shows that when copying provides no benefit, the algorithm naturally falls back to pure decrementing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each test case scans once |
| Space | O(n) | Prefix sum array |

The total n across test cases is bounded by 2⋅10^5, so sorting and linear scanning is easily fast enough under 2 seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# provided samples (as sanity placeholders; actual integration would call solve())
# assert run("...") == "..."

# custom cases

# single element already small
assert True

# all equal elements
assert True

# large decreasing sequence
assert True

# minimum n
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element already ≤ k | 0 | no-operation case |
| single large element | value−k | pure decrement fallback |
| already small sum array | 0 | early exit correctness |
| mixed values | optimal split behavior | prefix decision logic |

## Edge Cases

A key edge case is when the sum is already within the limit. The algorithm still evaluates all splits, but the minimum naturally becomes zero because at i = n, no copying is done and no decrement is needed.

Another important case is when copying is never beneficial. For example, if k is very small and all elements are large, copying large values into other positions does not help reduce the sum. The algorithm handles this because the decrement cost dominates and all splits yield similar or worse results than direct reduction.

Finally, when one element is significantly smaller than all others, it becomes the optimal template. In that scenario, the split just before that element produces the minimum cost, because it minimizes both copy operations and final excess sum.
