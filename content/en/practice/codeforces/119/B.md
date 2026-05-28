---
title: "CF 119B - Before Exam"
description: "We have n theorems, and each theorem has a proficiency value assigned to it. The exam contains exactly k different cards. Every card contains exactly floor(n / k) distinct theorems, and no theorem appears in more than one card."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 119
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 90"
rating: 1900
weight: 119
solve_time_s: 122
verified: true
draft: false
---

[CF 119B - Before Exam](https://codeforces.com/problemset/problem/119/B)

**Rating:** 1900  
**Tags:** constructive algorithms, implementation, sortings  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` theorems, and each theorem has a proficiency value assigned to it. The exam contains exactly `k` different cards. Every card contains exactly `floor(n / k)` distinct theorems, and no theorem appears in more than one card. Some theorems may remain unused if `n` is not divisible by `k`.

Several students already revealed the exact theorem sets on their cards. These revealed cards are guaranteed to be valid, and identical cards may appear multiple times because different students can draw the same card.

Vasya may receive any one of the `k` cards. Some cards are already known from the reports, while the remaining cards are unknown. We must compute the smallest and largest possible average proficiency among all cards Vasya could still receive, considering every valid completion of the unknown cards.

The constraints are very small. Both `n` and the number of reported cards are at most `100`. This means even quadratic or cubic algorithms are completely safe. Exhaustive search over all theorem partitions would still be impossible because the number of ways to partition sets grows extremely fast, but anything based on sorting or greedy assignment is trivial within the limit.

The tricky part is understanding what information actually matters. We do not know the exact unknown cards, only that every theorem belongs to at most one card and each card has fixed size. A careless implementation may incorrectly assume every unseen theorem can be combined arbitrarily with every other unseen theorem. That is false because cards must form a partition.

Consider this example:

```
6 2
1 2 3 100 100 100
1
1 2 3
```

Each card has size `3`. One card is already known: `{1,2,3}`. The remaining card must contain `{4,5,6}`. The minimum and maximum are both `100`. If we ignored the partition structure and tried arbitrary subsets, we might incorrectly think averages like `(1+2+100)/3` are possible.

Another subtle case happens when some cards are repeated in the reports:

```
4 2
1 2 10 20
2
1 2
2 1
```

These two reports describe the same card. There is still only one known card, not two. A buggy solution that counts both independently would think there are no unknown cards left.

The final important edge case is when `n` is not divisible by `k`.

```
7 3
1 2 3 4 5 6 7
0
```

Each card size is `2`, so only `6` theorems are used in cards. One theorem remains unused. The optimal strategy for maximizing the average is to discard the smallest theorem and build a card from the largest remaining pair. For minimizing, we discard the largest theorem instead.

## Approaches

A brute-force idea is to generate every valid partition of the theorems into cards, then compute all possible card averages. This works conceptually because the constraints are tiny, but the number of partitions explodes combinatorially. Even splitting `100` elements into groups of size around `50` is astronomically large. No amount of pruning saves this approach.

The key observation is that the exact composition of all unknown cards does not matter. We only care about the smallest and largest possible average of a single card.

Suppose each card contains `m = floor(n / k)` theorems. Some theorems are already fixed because they appear in known cards. The remaining theorems are free to be distributed among the unknown cards in any valid way.

To minimize Vasya's possible average, we want one unknown card to contain the smallest available theorem values. Since all unknown cards have the same size `m`, the minimum possible average among unknown cards is simply the average of the `m` smallest unused theorem values.

Similarly, the maximum possible average among unknown cards is the average of the `m` largest unused theorem values.

We must also compare against already known cards, because Vasya may receive one of those cards too. Their averages are fixed and already achievable.

This reduces the problem to simple bookkeeping:

1. Identify all distinct known cards.
2. Mark all theorems appearing in those cards as used.
3. Compute averages of known cards.
4. Sort unused theorem values.
5. Build the best and worst possible unknown card greedily from extremes.

The greedy choice works because there are no additional constraints between unknown cards beyond disjointness. If we want one card as small as possible, taking the globally smallest available values is always optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`, then compute `m = n // k`, which is the number of theorems per card.
2. Read all theorem proficiency values into an array.
3. Process the reported cards. Since the same card may appear multiple times in different orders, sort each card representation and store it in a set to keep only distinct cards.
4. For every distinct known card:

1. Compute its average proficiency.
2. Update the global minimum and maximum answers using this average.
3. Mark all its theorems as used.

These cards are guaranteed possible because they were explicitly observed.
5. Collect all unused theorem values into a separate array and sort it.
6. Let `remaining_cards` be the number of unknown cards:

`remaining_cards = k - number_of_distinct_known_cards`.
7. If there is at least one unknown card:

1. The smallest possible unknown-card average is obtained by taking the `m` smallest unused values.
2. The largest possible unknown-card average is obtained by taking the `m` largest unused values.
3. Update the global minimum and maximum answers with these values.
8. Print the final minimum and maximum.

### Why it works

Known cards are fixed and must remain exactly as observed. Every unused theorem belongs only to unknown cards, and the only restriction on unknown cards is that they partition the unused theorems into groups of size `m`.

To minimize the average of some unknown card, any theorem included in that card should be as small as possible. Replacing any selected theorem with a smaller unused theorem can only decrease the average. Repeating this exchange argument eventually produces the card consisting of the globally smallest `m` unused values.

The same argument applies symmetrically for the maximum using the largest values.

Because any partition of unused theorems into equal-sized groups is valid, these extremal cards are always constructible. Thus the algorithm computes the exact minimum and maximum achievable averages.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    q = int(input())

    unique_cards = set()

    for _ in range(q):
        card = tuple(sorted(map(int, input().split())))
        unique_cards.add(card)

    m = n // k

    used = [False] * n

    INF = float('inf')
    mn = INF
    mx = -INF

    for card in unique_cards:
        total = 0

        for x in card:
            total += a[x - 1]
            used[x - 1] = True

        avg = total / m

        mn = min(mn, avg)
        mx = max(mx, avg)

    remaining = []

    for i in range(n):
        if not used[i]:
            remaining.append(a[i])

    remaining.sort()

    unknown_cards = k - len(unique_cards)

    if unknown_cards > 0:
        low_avg = sum(remaining[:m]) / m
        high_avg = sum(remaining[-m:]) / m

        mn = min(mn, low_avg)
        mx = max(mx, high_avg)

    print(f"{mn:.10f} {mx:.10f}")

solve()
```

The first important detail is deduplicating reported cards. Two students may receive the same card, and theorem order inside input lines is arbitrary. Sorting the theorem indices and storing them as tuples in a set gives a canonical representation.

The second subtle point is marking used theorems only from distinct cards. If we processed duplicate reports independently, we could incorrectly think more theorems are fixed than actually are.

The remaining unused theorem values are enough to characterize every unknown card. Since all unknown cards have identical size, the minimum average comes from the smallest `m` values and the maximum from the largest `m`.

The algorithm uses floating-point division directly because the required precision is only `1e-6`. Python's `float` is more than sufficient.

## Worked Examples

### Example 1

Input:

```
7 3
7 15 0 19 10 5 12
2
1 6
7 4
```

Here `m = 7 // 3 = 2`.

Distinct known cards are `{1,6}` and `{4,7}`.

| Step | Used theorems | Known average | Current min | Current max |
| --- | --- | --- | --- | --- |
| Start | {} | - | inf | -inf |
| Card {1,6} | {1,6} | (7+5)/2 = 6 | 6 | 6 |
| Card {4,7} | {1,4,6,7} | (19+12)/2 = 15.5 | 6 | 15.5 |

Unused theorem values are:

```
15 0 10
```

Sorted:

```
0 10 15
```

Unknown cards still exist because only `2` distinct cards are known out of `3`.

| Computation | Result |
| --- | --- |
| Minimum unknown average | (0 + 10) / 2 = 5 |
| Maximum unknown average | (10 + 15) / 2 = 12.5 |

Final answer:

```
5.0000000000 15.5000000000
```

This trace demonstrates that known cards and unknown cards must both be considered. The best possible card already existed among the observed ones.

### Example 2

Input:

```
7 3
1 2 3 4 5 6 7
0
```

No cards are known.

`m = 2`.

Unused values after sorting:

```
1 2 3 4 5 6 7
```

| Computation | Result |
| --- | --- |
| Minimum possible average | (1 + 2) / 2 = 1.5 |
| Maximum possible average | (6 + 7) / 2 = 6.5 |

One theorem remains unused because only `6` theorems participate in cards.

Final answer:

```
1.5000000000 6.5000000000
```

This example demonstrates why leftover theorems must be ignored correctly when `n` is not divisible by `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the unused theorem values dominates |
| Space | O(n) | Used arrays and remaining values |

With `n ≤ 100`, this solution is extremely fast. Even a much less efficient algorithm would pass comfortably, so the implementation focuses on clarity and correctness.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    q = int(input())

    unique_cards = set()

    for _ in range(q):
        card = tuple(sorted(map(int, input().split())))
        unique_cards.add(card)

    m = n // k

    used = [False] * n

    INF = float('inf')
    mn = INF
    mx = -INF

    for card in unique_cards:
        total = 0

        for x in card:
            total += a[x - 1]
            used[x - 1] = True

        avg = total / m

        mn = min(mn, avg)
        mx = max(mx, avg)

    remaining = []

    for i in range(n):
        if not used[i]:
            remaining.append(a[i])

    remaining.sort()

    unknown_cards = k - len(unique_cards)

    if unknown_cards > 0:
        low_avg = sum(remaining[:m]) / m
        high_avg = sum(remaining[-m:]) / m

        mn = min(mn, low_avg)
        mx = max(mx, high_avg)

    return f"{mn:.10f} {mx:.10f}"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""7 3
7 15 0 19 10 5 12
2
1 6
7 4
"""
) == "5.0000000000 15.5000000000"

# minimum-size input
assert run(
"""1 1
42
0
"""
) == "42.0000000000 42.0000000000"

# duplicate known cards
assert run(
"""4 2
1 2 10 20
2
1 2
2 1
"""
) == "1.5000000000 15.0000000000"

# all equal values
assert run(
"""6 3
5 5 5 5 5 5
0
"""
) == "5.0000000000 5.0000000000"

# leftover unused theorem
assert run(
"""7 3
1 2 3 4 5 6 7
0
"""
) == "1.5000000000 6.5000000000"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 42` | `42 42` | Smallest possible input |
| Duplicate reports | `1.5 15` | Deduplication of known cards |
| All equal values | `5 5` | Stable averages regardless of grouping |
| `n % k != 0` | `1.5 6.5` | Correct handling of unused theorems |

## Edge Cases

### Duplicate card reports

Input:

```
4 2
1 2 10 20
2
1 2
2 1
```

Each card size is `2`.

Both reports describe the same card after sorting. The algorithm stores only one distinct card.

Known card average:

```
(1 + 2) / 2 = 1.5
```

Unused values:

```
10 20
```

Unknown card average:

```
15
```

Final answer:

```
1.5000000000 15.0000000000
```

Without deduplication, the program would incorrectly think all cards are already known.

### Leftover unused theorems

Input:

```
7 3
1 2 3 4 5 6 7
0
```

Each card contains `2` theorems, so only `6` theorems participate in cards.

The algorithm sorts unused values and takes only the smallest or largest `2` values when constructing extremal cards. One theorem is naturally ignored because it cannot belong to any card.

Minimum:

```
(1 + 2) / 2 = 1.5
```

Maximum:

```
(6 + 7) / 2 = 6.5
```

This matches the actual feasible partitions.

### All cards already known

Input:

```
6 3
1 2 3 4 5 6
3
1 2
3 4
5 6
```

All three distinct cards are already fixed.

Their averages are:

```
1.5, 3.5, 5.5
```

No unknown cards remain, so the algorithm skips the greedy construction step.

Final answer:

```
1.5000000000 5.5000000000
```

This confirms the solution does not accidentally use nonexistent unknown cards.
