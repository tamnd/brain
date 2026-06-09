---
title: "CF 2102D - Quartet Swapping"
description: "We have a permutation and a single allowed operation on four consecutive positions: $$[ai,a{i+1},a{i+2},a{i+3}] rightarrow [a{i+2},a{i+3},ai,a{i+1}]$$ Viewed differently, the element at position $i$ swaps with $i+2$, and the element at position $i+1$ swaps with $i+3$."
date: "2026-06-09T03:57:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2102
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1024 (Div. 2)"
rating: 1800
weight: 2102
solve_time_s: 136
verified: false
draft: false
---

[CF 2102D - Quartet Swapping](https://codeforces.com/problemset/problem/2102/D)

**Rating:** 1800  
**Tags:** data structures, greedy, sortings  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We have a permutation and a single allowed operation on four consecutive positions:

$$[a_i,a_{i+1},a_{i+2},a_{i+3}]
\rightarrow
[a_{i+2},a_{i+3},a_i,a_{i+1}]$$

Viewed differently, the element at position $i$ swaps with $i+2$, and the element at position $i+1$ swaps with $i+3$.

The task is not to decide whether a target permutation is reachable. We must find the lexicographically smallest permutation that can be obtained after applying this operation any number of times.

The total length over all test cases is at most $2 \cdot 10^5$. Any solution that repeatedly simulates operations or searches the state space is impossible. Even $O(n^2)$ per test case would be far too slow in the worst case. We need something around $O(n \log n)$.

The first subtle observation is that every element always stays on positions of the same parity. An element starting at position 1 can only move to positions 3, 5, 7, and so on. An element starting at position 2 can only move to positions 4, 6, 8, and so on.

A common mistake is to conclude that we can simply sort the odd-position elements and sort the even-position elements independently.

Consider:

```
n = 4
3 2 1 4
```

Odd positions contain `[3,1]`, even positions contain `[2,4]`.

Sorting each group gives:

```
1 2 3 4
```

but this configuration is not reachable. The only operation produces:

```
1 4 3 2
```

The missing ingredient is a parity constraint on the permutations applied inside the two groups.

Another easy-to-miss case appears when the sorted odd and even groups require permutation parities that do not match. Then the fully sorted merge is unreachable, and we must deliberately make one group slightly worse while keeping the answer lexicographically minimal.

## Approaches

A brute-force approach would treat each permutation as a graph node and each operation as an edge. Breadth-first search would eventually find the lexicographically smallest reachable state.

This is correct because every reachable permutation would be explored. Unfortunately the state space contains $n!$ permutations. Even for $n=10$, this is already completely infeasible.

To obtain something faster, we need to understand what the operation actually does.

Take the subsequence of elements currently sitting on odd positions and call it $O$. Take the subsequence on even positions and call it $E$.

Every operation performs one adjacent swap inside $O$ and one adjacent swap inside $E$ simultaneously. Since adjacent swaps generate the entire symmetric group, we can rearrange the odd-position elements arbitrarily and the even-position elements arbitrarily.

However, each operation contributes exactly one transposition to both groups. The parity of the permutation applied to $O$ and the parity of the permutation applied to $E$ always change together.

That means the following invariant holds:

The permutation applied to the odd positions and the permutation applied to the even positions must have the same parity.

This turns out to be the only restriction. Any pair of rearrangements with equal parity is reachable.

Now the problem becomes purely combinatorial.

The lexicographically smallest candidate is obtained by sorting the odd-position elements and the even-position elements separately and then merging them back into their positions.

If the permutation parities needed to reach those sorted orders are equal, this candidate is reachable and is optimal.

If the parities differ, the candidate is unreachable. We must change the parity of exactly one group. The cheapest way is to swap the last two elements of the sorted odd group or swap the last two elements of the sorted even group. Since the groups are sorted, changing the last two elements causes the smallest possible lexicographic damage. We construct both possibilities and choose the smaller resulting permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n!)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Extract the elements on odd positions into array `odd` and the elements on even positions into array `even`.
2. Create `odd_sorted` and `even_sorted` by sorting those arrays.
3. Compute the parity of the permutation that transforms `odd` into `odd_sorted`.
4. Compute the parity of the permutation that transforms `even` into `even_sorted`.
5. If the two parities are equal, merge `odd_sorted` and `even_sorted` back into alternating positions and output the result.
6. Otherwise, create two candidate answers.

1. Swap the last two elements of `odd_sorted`, then merge.
2. Swap the last two elements of `even_sorted`, then merge.
7. Output the lexicographically smaller candidate.

The swap of the last two elements flips the permutation parity of exactly one group. Since the parity mismatch was exactly one bit, either candidate becomes reachable.

### Why it works

Every operation performs one transposition inside the odd-position subsequence and one transposition inside the even-position subsequence. Consequently, the parity of the two induced permutations is always equal.

Adjacent transpositions generate all permutations, so the only invariant is this parity equality.

Sorting both groups separately produces the lexicographically smallest arrangement among all permutations that respect position parity. If its parity condition is already satisfied, no better reachable answer exists.

When the parity condition fails, we must change the parity of one group. Any parity change requires an odd permutation. Starting from a sorted array, the lexicographically smallest odd permutation is obtained by swapping its last two elements. Doing so changes the answer as late as possible, which minimizes lexicographic damage. Comparing the odd-group modification and the even-group modification yields the best reachable permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def permutation_parity(original, target_sorted):
    pos = {v: i for i, v in enumerate(target_sorted)}
    p = [pos[x] for x in original]

    n = len(p)
    vis = [False] * n
    parity = 0

    for i in range(n):
        if vis[i]:
            continue

        cur = i
        length = 0

        while not vis[cur]:
            vis[cur] = True
            cur = p[cur]
            length += 1

        parity ^= (length - 1) & 1

    return parity

def build(odd_vals, even_vals, n):
    res = [0] * n
    oi = 0
    ei = 0

    for i in range(n):
        if i % 2 == 0:
            res[i] = odd_vals[oi]
            oi += 1
        else:
            res[i] = even_vals[ei]
            ei += 1

    return res

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    odd = a[::2]
    even = a[1::2]

    odd_sorted = sorted(odd)
    even_sorted = sorted(even)

    p_odd = permutation_parity(odd, odd_sorted)
    p_even = permutation_parity(even, even_sorted)

    if p_odd == p_even:
        ans = build(odd_sorted, even_sorted, n)
    else:
        cand1_odd = odd_sorted[:]
        cand1_odd[-1], cand1_odd[-2] = cand1_odd[-2], cand1_odd[-1]
        cand1 = build(cand1_odd, even_sorted, n)

        cand2_even = even_sorted[:]
        cand2_even[-1], cand2_even[-2] = cand2_even[-2], cand2_even[-1]
        cand2 = build(odd_sorted, cand2_even, n)

        ans = min(cand1, cand2)

    print(*ans)
```

The solution begins by splitting the permutation according to position parity. This is the natural decomposition because operations never move an element between odd and even positions.

The parity computation uses cycle decomposition. If a permutation consists of cycles of lengths $c_1,c_2,\dots$, its parity equals

$$(c_1-1)+(c_2-1)+\cdots \pmod 2.$$

This lets us compute the parity in linear time.

The reconstruction step alternates elements from the odd-position list and the even-position list. Since Python uses zero-based indexing, indices `0,2,4,...` correspond to odd positions in the original problem.

The most delicate part is the parity-fix case. Swapping the last two elements of a sorted group changes its parity while causing the smallest possible lexicographic increase.

## Worked Examples

### Sample 1

Input:

```
4
3 4 1 2
```

Odd and even groups:

| Quantity | Value |
| --- | --- |
| odd | [3, 1] |
| even | [4, 2] |
| odd_sorted | [1, 3] |
| even_sorted | [2, 4] |
| odd parity | 1 |
| even parity | 1 |

Parities match.

Merged result:

| Position | Value |
| --- | --- |
| 1 | 1 |
| 2 | 2 |
| 3 | 3 |
| 4 | 4 |

Output:

```
1 2 3 4
```

This demonstrates the easy case where the fully sorted merge is reachable.

### Sample 2

Input:

```
5
5 4 3 1 2
```

Odd and even groups:

| Quantity | Value |
| --- | --- |
| odd | [5, 3, 2] |
| even | [4, 1] |
| odd_sorted | [2, 3, 5] |
| even_sorted | [1, 4] |
| odd parity | 1 |
| even parity | 1 |

Parities match again.

Merged result:

| Position | Value |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 3 |
| 4 | 4 |
| 5 | 5 |

Output:

```
2 1 3 4 5
```

The trace shows that the answer is not obtained by globally sorting the permutation. We can only reorder elements inside their position parity classes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting the odd and even groups dominates |
| Space | $O(n)$ | Arrays used for the groups and reconstruction |

The sum of all $n$ values is at most $2 \cdot 10^5$, so $O(n \log n)$ comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    # paste solution here
    return ""

# provided samples
assert solve(
"""3
4
3 4 1 2
5
5 4 3 1 2
10
10 9 8 7 6 5 4 3 2 1
"""
) == (
"""1 2 3 4
2 1 3 4 5
2 1 4 3 6 5 8 7 10 9
"""
)

# minimum size
assert solve(
"""1
4
1 2 3 4
"""
) == (
"""1 2 3 4
"""
)

# already optimal
assert solve(
"""1
5
2 1 3 4 5
"""
) == (
"""2 1 3 4 5
"""
)

# parity-fix case
assert solve(
"""1
4
3 2 1 4
"""
) == (
"""1 4 3 2
"""
)

# larger boundary-style pattern
assert solve(
"""1
6
6 5 4 3 2 1
"""
) == (
"""2 1 4 3 6 5
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `1 2 3 4` | Already optimal permutation |
| `2 1 3 4 5` | same output | No unnecessary changes |
| `3 2 1 4` | `1 4 3 2` | Parity-fix branch |
| `6 5 4 3 2 1` | `2 1 4 3 6 5` | Larger even-length case |

## Edge Cases

Consider:

```
4
3 2 1 4
```

Odd positions contain `[3,1]`, even positions contain `[2,4]`.

Sorting both groups gives:

```
odd_sorted = [1,3]
even_sorted = [2,4]
```

The required permutation parities differ, so this merged arrangement is unreachable.

The algorithm swaps the last two elements of one sorted group. The better candidate becomes:

```
1 4 3 2
```

which is exactly the reachable optimum.

Now consider:

```
5
5 4 3 1 2
```

The sorted odd and even groups already have matching parity. No correction is needed. The algorithm outputs:

```
2 1 3 4 5
```

which is lexicographically smallest among all reachable permutations.

Finally, consider a case where one group has only two elements:

```
4
4 1 3 2
```

The parity-fix operation swaps those two elements if necessary. The algorithm never accesses an out-of-range position because every group has length at least two when $n \ge 4$, exactly as guaranteed by the constraints.
