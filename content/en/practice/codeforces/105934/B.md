---
title: "CF 105934B - Treasure"
description: "The cities lie on a single river in order. The treasure hunters start in city 1. Reaching city i + 1 from city i costs ci coins, and there is no alternative route. Each city contains a chest worth ai coins."
date: "2026-06-25T13:57:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105934
codeforces_index: "B"
codeforces_contest_name: "MEPhI Spring Cup 2025"
rating: 0
weight: 105934
solve_time_s: 54
verified: true
draft: false
---

[CF 105934B - Treasure](https://codeforces.com/problemset/problem/105934/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The cities lie on a single river in order. The treasure hunters start in city 1. Reaching city `i + 1` from city `i` costs `c_i` coins, and there is no alternative route.

Each city contains a chest worth `a_i` coins. The hunters own at most `k` keys, so during the whole expedition they can open at most `k` chests. They may skip any city even if they visit it.

At some point they decide to stop exploring. Returning downstream is free, so the only travel cost is the cost paid to reach the farthest visited city.

For every possible stopping city, we must determine the best profit:

`coins collected from opened chests - travel costs paid`

and output the maximum achievable value.

The constraints are large, up to `10^5` cities, while treasure values and travel costs can reach `10^9`. Any solution that repeatedly scans prefixes or repeatedly sorts large ranges will be too slow. An `O(n^2)` approach would require around `10^10` operations in the worst case, which is completely infeasible. We need something close to `O(n log n)`.

A subtle point is that opening a chest is optional. Suppose:

```
n = 3, k = 2
a = [100, 1, 1]
```

The optimal choice is to open only the valuable chests available in the visited prefix. We never want to waste a key on a smaller chest if a larger one exists in the same reachable set.

Another easy mistake is to think the destination city must contain an opened chest.

```
n = 3, k = 1
a = [100, 1, 1000]
c = [10, 10000]
```

Stopping at city 2 gives profit `100 - 10 = 90`. Traveling to city 3 is disastrous because the additional travel cost exceeds the extra treasure. The stopping point and the opened chests are independent decisions.

A third edge case appears when fewer than `k` cities have been visited.

```
n = 2, k = 2
a = [5, 7]
c = [1]
```

After reaching city 1, the best collectible treasure is `5`, not "the sum of two treasures". The algorithm must naturally handle prefixes whose length is smaller than `k`.

## Approaches

A brute-force solution considers every stopping city `i`.

If we stop at city `i`, only cities `1...i` are reachable. Among those cities, the best strategy is obvious: open the chests with the largest values, up to `k` of them. The travel cost is fixed and equals:

```
c1 + c2 + ... + c(i-1)
```

So we could compute:

```
profit(i) =
(sum of k largest values in a[1..i])
-
(prefix travel cost)
```

The brute-force implementation would recompute the `k` largest values for every prefix independently. Sorting each prefix costs `O(i log i)`, leading to roughly `O(n^2 log n)` overall. With `n = 10^5`, this is far too slow.

The key observation is that prefixes grow one city at a time. When city `i` is added, only one new treasure value enters consideration. We do not need to recompute the entire set of top `k` treasures from scratch.

Maintain the current `k` largest treasure values seen so far. A min-heap is perfect for this. The heap stores exactly the treasures currently selected for opening. Its size never exceeds `k`.

When a new treasure arrives:

If the heap contains fewer than `k` elements, we must include it.

Otherwise, compare it with the smallest selected treasure, which is at the top of the min-heap. If the new value is larger, replacing the smallest selected treasure increases the total sum of chosen treasures. If it is not larger, the optimal set of chosen treasures remains unchanged.

This gives the sum of the largest `k` values in every prefix in `O(log k)` time per city.

The travel cost is even simpler. Let `cost` be the cumulative cost paid to reach the current city. As we move from city `i` to city `i + 1`, add `c_i`.

For every prefix we compute:

```
current_profit = sum_top_k - cost
```

and keep the maximum.

The official observation is exactly that if the hunters stop in city `i`, the best profit equals the sum of the `k` largest treasure values in the prefix `a[1..i]` minus the travel cost needed to reach that city.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n) | Too slow |
| Optimal | O(n log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, the treasure values `a`, and the travel costs `c`.
2. Create an empty min-heap and a variable `selected_sum = 0`.
3. Maintain `travel_cost`, the total cost paid to reach the current city.
4. Process cities from left to right.
5. For the current treasure value `a[i]`, update the heap of selected treasures.

If the heap size is smaller than `k`, push the value and add it to `selected_sum`.
6. If the heap already contains `k` elements, compare `a[i]` with the smallest selected treasure.

If `a[i]` is larger, remove the smallest selected treasure, insert `a[i]`, and update `selected_sum` accordingly.
7. After updating the heap, `selected_sum` equals the sum of the largest `k` treasure values in the current prefix.
8. Compute:

```
profit = selected_sum - travel_cost
```

Update the answer with the maximum profit seen so far.
9. Before moving to the next city, add the corresponding travel cost to `travel_cost`.
10. After all cities are processed, print the maximum profit.

### Why it works

For any stopping city `i`, the reachable cities are exactly the prefix `1...i`. Among those cities, any optimal strategy opens the most valuable available chests, up to `k` of them. Choosing a smaller chest while skipping a larger reachable one can only decrease profit.

The heap invariant is that it always stores the largest `k` treasure values among all cities processed so far. Whenever a new treasure enters the prefix, the only possible change to the optimal set is replacing the smallest currently selected treasure. The heap performs exactly this update.

Since `selected_sum` always equals the sum of the largest `k` treasures in the current prefix, and `travel_cost` equals the cost required to reach that prefix's last city, the computed profit is exactly the best profit for that stopping point. Taking the maximum over all stopping points yields the global optimum.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    c = []
    if n > 1:
        c = list(map(int, input().split()))
    
    heap = []
    selected_sum = 0
    travel_cost = 0
    answer = 0

    for i in range(n):
        x = a[i]

        if len(heap) < k:
            heapq.heappush(heap, x)
            selected_sum += x
        elif x > heap[0]:
            removed = heapq.heapreplace(heap, x)
            selected_sum += x - removed

        answer = max(answer, selected_sum - travel_cost)

        if i < n - 1:
            travel_cost += c[i]

    print(answer)

solve()
```

The heap stores the currently selected treasures. Because it is a min-heap, the smallest selected treasure is always available in `O(1)` time.

When the heap size is below `k`, every new treasure automatically belongs to the current top-`k` set. Once the heap reaches size `k`, a new treasure matters only if it is larger than the smallest selected one.

`selected_sum` is updated incrementally. Recomputing the sum from the heap every iteration would turn the solution into `O(nk)`.

The order of operations matters. The profit for city `i` must be computed before adding the cost of traveling to city `i + 1`. At that moment, `travel_cost` should represent exactly the amount spent to reach city `i`.

All arithmetic uses Python integers, which safely handle values far larger than the maximum possible answer.

## Worked Examples

### Example 1

```
n = 5, k = 2
a = [10, 3, 2, 20, 45]
c = [5, 5, 5, 50]
```

| City | Treasure | Heap Contents | selected_sum | travel_cost | Profit |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | [10] | 10 | 0 | 10 |
| 2 | 3 | [3,10] | 13 | 5 | 8 |
| 3 | 2 | [3,10] | 13 | 10 | 3 |
| 4 | 20 | [10,20] | 30 | 15 | 15 |
| 5 | 45 | [20,45] | 65 | 65 | 0 |

The maximum profit is `15`, achieved by stopping at city 4. The chosen chests are worth `20` and `10`, and the total travel cost is `15`.

### Example 2

```
n = 7, k = 3
a = [0, 0, 5, 8, 13, 17, 20]
c = [9, 5, 7, 10, 1, 8]
```

| City | Treasure | selected_sum | travel_cost | Profit |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 9 | -9 |
| 3 | 5 | 5 | 14 | -9 |
| 4 | 8 | 13 | 21 | -8 |
| 5 | 13 | 26 | 31 | -5 |
| 6 | 17 | 38 | 32 | 6 |
| 7 | 20 | 50 | 40 | 10 |

The best answer is `10`, obtained at the final city.

This trace shows that a larger prefix is not always worse despite higher travel costs. The growing set of available treasures can eventually outweigh the additional expense.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log k) | Each city performs at most one heap operation |
| Space | O(k) | The heap stores at most `k` treasures |

With `n ≤ 10^5`, `O(n log k)` easily fits within typical competitive programming limits. The memory usage is tiny because only the selected treasures are kept in the heap.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    c = []
    if n > 1:
        c = list(map(int, input().split()))

    heap = []
    selected_sum = 0
    travel_cost = 0
    answer = 0

    for i in range(n):
        x = a[i]

        if len(heap) < k:
            heapq.heappush(heap, x)
            selected_sum += x
        elif x > heap[0]:
            removed = heapq.heapreplace(heap, x)
            selected_sum += x - removed

        answer = max(answer, selected_sum - travel_cost)

        if i < n - 1:
            travel_cost += c[i]

    return str(answer) + "\n"

# provided samples
assert run(
"""5 2
10 3 2 20 45
5 5 5 50
"""
) == "15\n", "sample 1"

assert run(
"""7 3
0 0 5 8 13 17 20
9 5 7 10 1 8
"""
) == "10\n", "sample 2"

# minimum size
assert run(
"""1 1
7
"""
) == "7\n", "single city"

# all equal values
assert run(
"""4 2
5 5 5 5
1 1 1
"""
) == "10\n", "all treasures equal"

# large travel costs discourage movement
assert run(
"""3 1
100 1 1000
10 10000
"""
) == "100\n", "best stop is first city"

# k equals n
assert run(
"""3 3
5 6 7
1 2
"""
) == "15\n", "can open every reachable chest"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single city | 7 | Minimum constraints |
| Equal treasures | 10 | Heap replacement logic with duplicates |
| Huge travel cost | 100 | Best answer may occur early |
| k = n | 15 | All reachable treasures can be taken |

## Edge Cases

Consider the case where traveling farther is harmful.

```
3 1
100 1 1000
10 10000
```

At city 1, the heap contains `{100}` and profit is `100`. At city 2, the best treasure is still `100`, but profit drops to `90` because of travel cost. At city 3, the heap changes to `{1000}`, yet profit becomes `1000 - 10010`, which is negative. The algorithm correctly keeps the maximum value `100`.

Now consider a prefix shorter than `k`.

```
2 2
5 7
1
```

After city 1, the heap contains only one treasure and `selected_sum = 5`. The algorithm never assumes that exactly `k` treasures must exist. After city 2, the heap contains both treasures and the answer becomes `12 - 1 = 11`.

Finally, consider duplicate values.

```
4 2
5 5 5 5
1 1 1
```

The heap always stores two copies of value `5`. Equal values do not trigger unnecessary replacements because replacing a selected `5` with another `5` changes nothing. The invariant that the heap contains the largest `k` values remains valid throughout the execution.
