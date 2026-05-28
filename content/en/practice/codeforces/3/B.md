---
title: "CF 3B - Lorry"
description: "We have two kinds of vehicles: - Kayaks, which take 1 unit of space. - Catamarans, which take 2 units of space. Each veh"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 3
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 3"
rating: 1900
weight: 3
solve_time_s: 168
verified: true
draft: false
---
## Solution
## Problem Understanding

We have two kinds of vehicles:

- Kayaks, which take 1 unit of space.
- Catamarans, which take 2 units of space.

Each vehicle also has a value, its carrying capacity. The truck has total capacity `v`, and we want to choose a subset of vehicles whose total occupied space does not exceed `v`, while maximizing the sum of carrying capacities.

This is very close to a knapsack problem, but the item sizes are only `1` and `2`. That small restriction completely changes the problem. A general knapsack with `n = 10^5` and `v = 10^9` would be impossible with dynamic programming over capacity, because even an `O(n * v)` solution would explode immediately. With `10^14` states, there is no chance.

The input size also rules out any quadratic approach. With `n = 10^5`, an `O(n^2)` algorithm performs around `10^10` operations in the worst case, which is far beyond the limit for a 2 second Codeforces problem.

The important observation is that all size-1 items are interchangeable from a space perspective, and all size-2 items are interchangeable as well. Only their values differ. That means after sorting by value, the optimal solution always prefers the best remaining items of each type.

There are several easy-to-miss corner cases.

Suppose the truck has odd capacity:

```
v = 5
```

A careless greedy solution might repeatedly take the highest-value item available. That can fail because using too many size-2 items may leave unusable space. For example:

```
4 5
2 100
2 99
2 98
1 97
```

Taking the top two catamarans gives value `199` and leaves capacity `1`, so we can still take the kayak for total `296`. That works. But if the kayak were slightly stronger, the best solution could depend on preserving one unit of space intentionally.

Another common mistake is assuming that taking the best size-2 item is always better than taking two size-1 items. Consider:

```
3 2
1 100
1 99
2 150
```

The catamaran has larger individual value, but two kayaks together give `199`, which is better than `150`.

There is also the case where the optimal solution does not fully use the truck capacity. For example:

```
2 10
1 5
2 6
```

We can only take both items for total value `11`. The remaining space stays unused, and that is perfectly valid.

Finally, when one type is missing entirely, the solution still needs to work correctly:

```
3 4
2 10
2 20
2 30
```

The answer is simply the best two catamarans. No special handling should be required.

## Approaches

The brute-force idea is straightforward. Every vehicle can either be chosen or skipped, so we could enumerate all subsets, compute total occupied volume and total carrying capacity, then keep the best valid subset.

That works logically because it checks every possible answer. The problem is the number of subsets. With `n` vehicles, there are `2^n` possibilities. Even for `n = 40`, this is already around `10^12` subsets. With `n = 10^5`, brute force is completely impossible.

A slightly less terrible approach is dynamic programming over capacity. Let `dp[x]` represent the best carrying capacity achievable with used volume `x`. Since item sizes are only `1` and `2`, transitions are easy.

The problem is the capacity limit. `v` can be as large as `10^9`, so even storing the DP array is impossible.

The key insight is that item sizes are extremely restricted. Every item is either size `1` or size `2`. Once we separate them into two groups, the only thing that matters is which highest-value items we choose from each group.

Suppose we decide to take exactly `k` catamarans. They occupy `2k` space. The remaining space can only be filled optimally by taking the strongest available kayaks. Since all kayaks have identical size, the best choice is simply the top few after sorting.

This turns the problem into:

- Sort kayaks by value descending.
- Sort catamarans by value descending.
- Precompute prefix sums for both groups.
- Try every possible number of catamarans.
- Fill the remaining capacity with the best possible kayaks.

Now every candidate solution can be evaluated in `O(1)` time using prefix sums.

The total complexity becomes dominated by sorting, which is `O(n log n)`, easily fast enough for `10^5` items.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Capacity DP | O(nv) | O(v) | Impossible for large v |
| Optimal Greedy + Prefix Sums | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all vehicles and split them into two arrays.

Store kayaks separately from catamarans. For each item, keep both its carrying capacity and its original index because the output requires original numbering.
2. Sort both arrays in descending order of carrying capacity.

If we ever want the best `k` kayaks, they will always be the first `k` items after sorting. The same idea applies to catamarans.
3. Build prefix sums for both arrays.

Let `pref1[i]` be the total carrying capacity of the first `i` kayaks. Let `pref2[i]` be the total carrying capacity of the first `i` catamarans.

This allows us to compute the total value of taking any number of items in constant time.
4. Iterate over the number of catamarans taken.

Suppose we take `i` catamarans. They consume `2 * i` space.

If this exceeds the truck capacity, skip this choice.
5. Compute the remaining capacity for kayaks.

The remaining volume is:

```
rem = v - 2 * i
```

Since each kayak uses exactly one unit, we can take at most `rem` kayaks.
6. Compute the total value for this combination.

The total carrying capacity becomes:

```
pref2[i] + pref1[min(rem, number_of_kayaks)]
```
7. Track the best answer.

Whenever we find a larger total carrying capacity, store the current counts of kayaks and catamarans.
8. Reconstruct the chosen indices.

Output the indices of the selected kayaks and catamarans from the sorted arrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, v = map(int, input().split())

one = []
two = []

for idx in range(1, n + 1):
    t, p = map(int, input().split())

    if t == 1:
        one.append((p, idx))
    else:
        two.append((p, idx))

one.sort(reverse=True)
two.sort(reverse=True)

pref1 = [0]
for val, _ in one:
    pref1.append(pref1[-1] + val)

pref2 = [0]
for val, _ in two:
    pref2.append(pref2[-1] + val)

best = 0
best_one = 0
best_two = 0

m1 = len(one)
m2 = len(two)

for take_two in range(m2 + 1):
    used = 2 * take_two

    if used > v:
        break

    rem = v - used
    take_one = min(rem, m1)

    total = pref2[take_two] + pref1[take_one]

    if total > best:
        best = total
        best_one = take_one
        best_two = take_two

answer = []

for i in range(best_one):
    answer.append(str(one[i][1]))

for i in range(best_two):
    answer.append(str(two[i][1]))

print(best)
print(" ".join(answer))
```

The first part separates the items into two groups while preserving original indices. Keeping indices is necessary because after sorting, the original order disappears.

Sorting in descending order is what makes the greedy choice valid. Once sorted, the best `k` items of a type are always just the first `k`.

The prefix sum arrays are built with an extra leading zero. This avoids special cases when taking zero items.

The main loop tries every feasible number of catamarans. Since each catamaran consumes exactly two units of space, we immediately know how much room remains for kayaks.

One subtle detail is:

```
take_one = min(rem, m1)
```

The remaining capacity may allow more kayaks than actually exist. Without the `min`, the code would access invalid prefix sum positions.

Another small but important optimization is:

```
if used > v:
    break
```

Because the number of used units only increases as we take more catamarans, all later iterations are impossible too.

Finally, reconstruction is simple because the chosen items are exactly the first `best_one` kayaks and first `best_two` catamarans in sorted order.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
2 7
1 3
```

After sorting:

- Kayaks: `(3, idx=3), (2, idx=1)`
- Catamarans: `(7, idx=2)`

Prefix sums:

- `pref1 = [0, 3, 5]`
- `pref2 = [0, 7]`

| take_two | used space | remaining | take_one | total value | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 5 | 5 |
| 1 | 2 | 0 | 0 | 7 | 7 |

The optimal solution is taking the single catamaran with index `2`.

This example shows why larger items are not automatically worse despite occupying more space. The single catamaran beats both kayaks combined.

### Example 2

Input:

```
5 5
1 10
1 9
1 8
2 25
2 24
```

After sorting:

- Kayaks: `10, 9, 8`
- Catamarans: `25, 24`

Prefix sums:

- `pref1 = [0, 10, 19, 27]`
- `pref2 = [0, 25, 49]`

| take_two | used space | remaining | take_one | total value |
| --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 3 | 27 |
| 1 | 2 | 3 | 3 | 52 |
| 2 | 4 | 1 | 1 | 59 |

The best answer uses both catamarans and one kayak for total value `59`.

This trace demonstrates how trying every possible count of size-2 items guarantees the optimal mix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | Arrays and prefix sums store all items |

The solution easily fits within the limits. Sorting `10^5` elements is fast in Python, and all remaining operations are linear. Memory usage is also small because we only store a few arrays of size `n`.

## Test Cases

### Test Case 1

Input:

```
1 1
1 100
```

Expected output:

```
100
1
```

This verifies the minimum-size input.

### Test Case 2

Input:

```
3 2
1 100
1 99
2 150
```

Expected output:

```
199
1 2
```

This catches greedy solutions that incorrectly prefer the single larger-valued catamaran.

### Test Case 3

Input:

```
4 5
2 100
2 99
1 1
1 1
```

Expected output:

```
201
1 2 3 4
```

This verifies that leftover space should still be filled whenever beneficial.

### Test Case 4

Input:

```
5 4
2 10
2 10
2 10
2 10
2 10
```

Expected output:

```
20
1 2
```

This checks handling when only one item type exists.

## Edge Cases

Consider the case where two size-1 items beat one size-2 item:

```
3 2
1 100
1 99
2 150
```

After sorting:

- Kayaks: `100, 99`
- Catamarans: `150`

The algorithm checks:

- `take_two = 0`, total = `199`
- `take_two = 1`, total = `150`

The maximum is correctly identified as `199`.

Now consider an input where capacity is not fully used:

```
2 10
1 5
2 6
```

The algorithm evaluates:

- Take no catamarans: total `5`
- Take one catamaran: total `11`

No more items exist, so unused space remains. The algorithm still outputs the correct maximum.

Finally, consider the case where only catamarans exist:

```
3 4
2 10
2 20
2 30
```

Sorted catamarans become `30, 20, 10`.

The algorithm checks:

- `take_two = 0`, total `0`
- `take_two = 1`, total `30`
- `take_two = 2`, total `50`

The answer is the first two catamarans, exactly as expected.
