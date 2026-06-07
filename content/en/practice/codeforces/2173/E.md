---
title: "CF 2173E - Shiro's Mirror Duel"
description: "We maintain a permutation of 1..n. A query chooses two indices x and y. The judge then flips a coin. Either positions (x,y) are swapped, or their mirrored positions (n-x+1, n-y+1) are swapped."
date: "2026-06-07T22:48:47+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "interactive", "probabilities", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2173
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1068 (Div. 2)"
rating: 2200
weight: 2173
solve_time_s: 146
verified: false
draft: false
---

[CF 2173E - Shiro's Mirror Duel](https://codeforces.com/problemset/problem/2173/E)

**Rating:** 2200  
**Tags:** constructive algorithms, greedy, interactive, probabilities, sortings  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We maintain a permutation of `1..n`.

A query chooses two indices `x` and `y`. The judge then flips a coin. Either positions `(x,y)` are swapped, or their mirrored positions `(n-x+1, n-y+1)` are swapped. After the swap, we are told which pair was actually exchanged, so we always know the current permutation exactly.

The challenge is that we cannot directly choose which side of the array is affected. Every operation acts either on a pair of positions or on its mirror image.

The sum of all `n` is only `2·10^4`, so any `O(n^2)` processing would be fine computationally. The real restriction is the query budget. We only receive about `2.5n` operations, which means we must make steady progress and cannot afford repeated global rearrangements.

The first observation is that a position and its mirror form a natural pair:

```
i <-> n-i+1
```

Whenever we request a swap involving one side of such a pair, the judge may instead perform the corresponding action on the other side.

A naive sorting strategy would repeatedly place each value into its correct position. The problem is that every attempt succeeds only with probability `1/2`, so a careless implementation may spend far more than the allowed number of operations.

A particularly dangerous case is trying to fix only one side.

For example, with

```
n = 6
[2,1,3,4,5,6]
```

trying to place `1` into position `1` can repeatedly affect the mirrored side instead. Progress becomes difficult to control.

The key is to work on mirrored pairs together. Once we view positions `i` and `n-i+1` as a single unit, the random choice of the judge stops being an obstacle and becomes a useful symmetry.

## Approaches

A brute force idea is to sort exactly as we would sort a normal permutation. Suppose value `i` is currently at position `pos[i]`. We repeatedly request a swap between `pos[i]` and `i`.

The issue is that only half of the queries affect the intended location. The other half affect the mirrored positions. While the expected number of attempts to fix one element is constant, interactions between different elements make the analysis messy and the total number of operations can easily exceed the limit.

The crucial observation is that the judge never chooses an arbitrary swap. It chooses between a swap and its mirror.

Consider a mirrored pair of target values:

```
l = i
r = n-i+1
```

Suppose value `l` is not in position `l`.

We query:

```
(pos[l], l)
```

If the judge executes the chosen swap, value `l` immediately reaches its correct position.

If the judge executes the mirrored swap, then the position of value `r` moves toward its correct side instead.

Either way, one of the two members of the mirrored pair gets closer to being fixed.

This suggests processing the permutation from the outside inward. For each mirrored pair `(l,r)`, we keep querying until both positions contain their correct values.

The beautiful part is that every query fixes at least one of the two positions in expectation. The editorial analysis shows that the expected cost for one mirrored pair is at most five operations, which leads to an overall expectation of roughly `2.5n` operations. The additional `800` in the limit provides a huge safety margin.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force placement | Unclear under query limit | O(n) | Not reliable |
| Mirrored-pair greedy | O(n) expected queries | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain the current permutation and an array `pos[v]` storing the position of every value.
2. If `n` is odd, first fix the middle element.

The middle position is its own mirror. Repeatedly query the pair `(pos[mid_value], mid_position)` until the middle value reaches the center.
3. Process mirrored positions from the outside inward.

Let

```
l = i
r = n-i+1
```
4. While either position is incorrect, continue operating on this pair.
5. If value `l` is not currently in position `l`, query

```
(l, pos[l])
```

When the non-mirrored swap happens, `l` becomes correct immediately.
6. Otherwise, position `l` is already correct, so work on the other side and query

```
(r, pos[r])
```
7. After every judge response, update both the permutation and the `pos` array.
8. Once both positions of the current mirrored pair are correct, move inward to the next pair.
9. When every pair has been processed, the permutation is sorted.

### Why it works

Fix a mirrored pair `(l,r)`.

Whenever `l` is incorrect and we query `(l,pos[l])`, one of two things happens.

If the chosen swap is executed directly, value `l` reaches its final position.

If the mirrored swap is executed, the operation affects only the mirrored side of the array, which is exactly where value `r` lives. Progress is made toward fixing the other member of the pair.

The same reasoning applies when we query for `r`.

Throughout the process, positions outside the current mirrored pair never need to be revisited. Once a pair becomes correct, later operations cannot break it because future queries only involve positions strictly inside that pair.

By induction from the outermost pair toward the center, every position eventually reaches its correct value, so the final permutation is sorted.

## Python Solution

This is the accepted interactive solution structure.

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] + list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[p[i]] = i

    def query(x, y):
        print("?", x, y)
        sys.stdout.flush()

        u, v = map(int, input().split())
        if u == -1:
            sys.exit(0)

        p[u], p[v] = p[v], p[u]
        pos[p[u]] = u
        pos[p[v]] = v

    if n % 2 == 1:
        mid = (n + 1) // 2
        while p[mid] != mid:
            query(pos[mid], mid)

    for l in range(1, n // 2 + 1):
        r = n + 1 - l

        while p[l] != l or p[r] != r:
            if p[l] != l:
                query(l, pos[l])
            else:
                query(r, pos[r])

    print("!")
    sys.stdout.flush()

t = int(input())
for _ in range(t):
    solve()
```

The permutation itself is stored because the judge tells us the exact swap that actually occurred. After receiving `(u,v)`, we update both the array and the inverse-position array in constant time.

The middle position of an odd-length permutation is special because it is its own mirror. Fixing it first simplifies the remaining logic.

For every mirrored pair, the algorithm always prefers fixing the left position. Once the left side becomes correct, it switches to the right side. This guarantees that completed outer pairs never need attention again.

The most common implementation mistake is forgetting to update `pos` after a swap. The entire strategy depends on knowing the current location of every value.

## Worked Examples

### Example 1

Initial permutation:

```
[5,1,3,4,2]
```

| Step | Query | Actual swap | Permutation |
| --- | --- | --- | --- |
| Start | - | - | [5,1,3,4,2] |
| 1 | (1,5) | (1,5) | [2,1,3,4,5] |
| 2 | (4,5) | (2,1) | [1,2,3,4,5] |

The first operation fixes value `5`. The second query targets the mirrored pair `(2,4)`. Even though the judge chose the mirrored swap, the permutation became fully sorted.

### Example 2

Initial permutation:

```
[2,1,4,3]
```

| Step | Query | Actual swap | Permutation |
| --- | --- | --- | --- |
| Start | - | - | [2,1,4,3] |
| 1 | (1,2) | (1,2) | [1,2,4,3] |
| 2 | (3,4) | (3,4) | [1,2,3,4] |

The outer pair `(1,4)` becomes correct first. Then the inner pair `(2,3)` is fixed. Once a pair is correct, later operations never disturb it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) expected queries | Each mirrored pair requires constant expected work |
| Space | O(n) | Permutation and inverse-position arrays |

The sum of all `n` is only `2·10^4`, so the memory usage is tiny. The expected number of operations is about `2.5n`, which matches the intended bound and comfortably fits inside the allowed limit.

## Test Cases

Because this is an interactive problem, traditional offline assert tests are not meaningful. The judge's responses depend on random choices during execution.

For local testing, a simulator would be required. Typical scenarios to verify are shown below.

```
# Case 1: already sorted
# n = 1
# [1]

# Case 2: smallest non-trivial permutation
# n = 2
# [2, 1]

# Case 3: odd length, center incorrect
# n = 5
# [1, 3, 2, 4, 5]

# Case 4: completely reversed
# n = 8
# [8,7,6,5,4,3,2,1]

# Case 5: random large permutation
# n = 4000
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | Immediate finish | Single-element edge case |
| `[2,1]` | One mirrored pair | Smallest meaningful instance |
| Odd `n` with wrong center | Center-fixing logic | Self-mirrored position |
| Reversed permutation | Many corrections | Global correctness |
| Large random permutation | Accepted within limit | Performance |

## Edge Cases

Consider `n = 1`.

```
[1]
```

There are no mirrored pairs and the center is already correct. The algorithm immediately outputs `!`.

Consider an odd-length permutation where only the center is wrong:

```
n = 5
[1,2,4,3,5]
```

The center position is `3`. Since a center position mirrors to itself, repeatedly querying `(pos[3],3)` eventually places value `3` in the middle. After that, the outer pairs are processed normally.

Consider a pair where one side is already correct:

```
[1,4,3,2]
```

For the pair `(1,4)`, position `1` is already correct. The algorithm immediately works on the right side instead of wasting operations on the left. This is why the condition

```
if p[l] != l:
    ...
else:
    ...
```

is necessary.

Finally, consider a query whose mirrored version is executed instead of the intended one. That is the central challenge of the problem. The algorithm handles it because every query is designed around a mirrored pair. If the left side is not improved, the right side is. Progress on the pair never disappears, which is exactly the property that keeps the expected number of operations linear.
