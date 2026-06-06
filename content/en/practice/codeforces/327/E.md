---
title: "CF 327E - Axis Walking"
description: "We have n positive segment lengths. Their total sum is d, which is also the destination point on the number line. A route is simply an ordering of these lengths. While following a route, we keep a running prefix sum."
date: "2026-06-06T08:58:49+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "constructive-algorithms", "dp", "meet-in-the-middle"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 2300
weight: 327
solve_time_s: 145
verified: true
draft: false
---

[CF 327E - Axis Walking](https://codeforces.com/problemset/problem/327/E)

**Rating:** 2300  
**Tags:** bitmasks, combinatorics, constructive algorithms, dp, meet-in-the-middle  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` positive segment lengths. Their total sum is `d`, which is also the destination point on the number line.

A route is simply an ordering of these lengths. While following a route, we keep a running prefix sum. After taking the first segment we stop once, after the second segment we stop again, and so on. The final stop is always at position `d`.

Some positions are unlucky. A route is good if none of its stopping points coincide with an unlucky position.

The task is to count how many permutations of the given lengths are good, modulo `10^9 + 7`.

The most important observation is that every stopping point is the sum of some prefix of the permutation. Since all lengths are positive, prefix sums are strictly increasing. This monotonicity is what makes the problem tractable.

The constraint `n ≤ 24` immediately rules out anything involving all permutations. Even `20!` is astronomically large. A solution must work with subsets instead of permutations.

The number of unlucky positions is at most two. That tiny bound is the second crucial clue. It suggests inclusion-exclusion over unlucky positions, leaving only a few counting subproblems.

There are several easy-to-miss corner cases.

If an unlucky position cannot be represented as a subset sum, then no route can ever stop there. For example:

```
n = 3
a = [2, 4, 8]
unlucky = 5
```

No subset sums to `5`, so every permutation is valid.

If an unlucky position equals the total sum `d`, every route is invalid because the final stop is always at `d`. For example:

```
n = 2
a = [3, 7]
unlucky = 10
```

The answer is `0`.

When there are two unlucky positions, a route may hit both. Inclusion-exclusion must add these routes back once. For example:

```
a = [1, 2, 3]
unlucky = {1, 3}
```

The permutation `[1,2,3]` hits both unlucky positions, so subtracting each bad set independently would remove it twice.

## Approaches

The brute-force solution generates all `n!` permutations, computes all prefix sums, and checks whether any prefix is unlucky.

This is correct because it directly follows the definition of a route. Unfortunately it becomes useless almost immediately. Even for `n = 15`, the number of permutations exceeds `10^12`.

To obtain something feasible, we need to count permutations indirectly.

Consider a single unlucky position `x`.

A route reaches `x` exactly when the elements placed before that stop form a subset whose sum is `x`.

Suppose a subset `S` has sum `x` and size `s`. Every permutation where all elements of `S` appear before all elements outside `S` will reach `x`. The elements inside `S` can be ordered arbitrarily, and the remaining elements can also be ordered arbitrarily.

Hence that subset contributes

```
s! · (n - s)!
```

bad permutations.

So the problem becomes:

```
For every subset whose sum is x,
add size! · remaining_size!
```

This is a subset-sum counting problem, not a permutation problem.

Since `n ≤ 24`, meet-in-the-middle is the natural tool. Splitting the array into two halves of size at most `12` reduces `2^24` subsets to about `2 · 2^12 = 8192` enumerations.

For two unlucky positions `x < y`, inclusion-exclusion requires counting routes that hit both positions.

Such a route contains:

```
S          -> prefix sum x
S ∪ U      -> prefix sum y
```

where

```
sum(S) = x
sum(U) = y - x
S and U are disjoint
```

If

```
|S| = a
|U| = b
```

then the corresponding permutations are

```
a! · b! · (n - a - b)!
```

because all elements of `S` must come first, then all elements of `U`, then everything else.

Now each element has three possible states:

```
belongs to S
belongs to U
belongs to neither
```

This leads to a ternary meet-in-the-middle over `3^(n/2)` states.

For `n = 24`, each half has at most `3^12 = 531441` states, which is entirely manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Optimal | O(2^(n/2) + 3^(n/2)) | O(3^(n/2)) | Accepted |

## Algorithm Walkthrough

### Counting routes that hit one unlucky position

1. Split the array into two halves.
2. Enumerate every subset of the right half and group them by `(sum, size)`.
3. Enumerate every subset of the left half.
4. For a target unlucky position `x`, suppose the left subset contributes `(sumL, sizeL)`. We need right subsets with sum `x - sumL`.
5. Every matching pair forms a complete subset whose total size is `sizeL + sizeR`.
6. Add

```
count · (sizeL + sizeR)! · (n - sizeL - sizeR)!
```

to the answer.

This yields the number of permutations that hit `x`.

### Counting routes that hit both unlucky positions

Assume `x < y` and let

```
d = y - x
```

1. Split the array into two halves.
2. Enumerate all ternary assignments of the right half.
3. For every assignment record:

```
(sumS, sumU, sizeS, sizeU)
```

and its frequency.

1. Enumerate all ternary assignments of the left half.
2. For a left assignment, the required right assignment must satisfy:

```
sumS_right = x - sumS_left
sumU_right = d - sumU_left
```

1. Every matching pair determines a disjoint pair `(S,U)`.
2. If the combined sizes are:

```
a = sizeS_left + sizeS_right
b = sizeU_left + sizeU_right
```

add

```
a! · b! · (n - a - b)!
```

times the number of matching pairs.

### Inclusion-exclusion

If there are no unlucky positions:

```
answer = n!
```

If there is one unlucky position:

```
answer = n! - bad(x)
```

If there are two unlucky positions:

```
answer = n! - bad(x) - bad(y) + bad_both(x,y)
```

All arithmetic is performed modulo `10^9 + 7`.

### Why it works

For a single unlucky position, every route reaching that position determines exactly one subset of elements that appear before the stop. Conversely, every subset with the required sum generates exactly `s!(n-s)!` such routes. This establishes a bijection between bad routes and counted subset configurations.

For two unlucky positions, positivity of all lengths guarantees that the smaller unlucky position must be reached first. Thus every route hitting both positions uniquely decomposes into disjoint sets `S` and `U`, where `S` reaches the first position and `S ∪ U` reaches the second. The counting formula follows directly from the required block ordering of these sets inside the permutation.

Since inclusion-exclusion is exact, every route is counted with the correct multiplicity.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

MOD = 1000000007

def subset_bad(arr, target, fact):
    n = len(arr)
    m = n // 2
    left = arr[:m]
    right = arr[m:]

    right_map = defaultdict(lambda: [0] * (len(right) + 1))

    rlen = len(right)
    for mask in range(1 << rlen):
        s = 0
        cnt = 0
        for i in range(rlen):
            if mask >> i & 1:
                s += right[i]
                cnt += 1
        right_map[s][cnt] += 1

    ans = 0

    llen = len(left)
    for mask in range(1 << llen):
        s = 0
        cnt = 0
        for i in range(llen):
            if mask >> i & 1:
                s += left[i]
                cnt += 1

        need = target - s
        if need not in right_map:
            continue

        vec = right_map[need]

        for rsz, ways in enumerate(vec):
            if ways == 0:
                continue

            sz = cnt + rsz
            ans = (ans + ways * fact[sz] * fact[n - sz]) % MOD

    return ans

def both_bad(arr, x, y, fact):
    if x > y:
        x, y = y, x

    diff = y - x
    n = len(arr)

    m = n // 2
    left = arr[:m]
    right = arr[m:]

    right_map = defaultdict(lambda: defaultdict(int))

    def gen_half(values):
        res = []

        def dfs(idx, sum_s, sum_u, cnt_s, cnt_u):
            if idx == len(values):
                res.append((sum_s, sum_u, cnt_s, cnt_u))
                return

            v = values[idx]

            dfs(idx + 1, sum_s, sum_u, cnt_s, cnt_u)
            dfs(idx + 1, sum_s + v, sum_u, cnt_s + 1, cnt_u)
            dfs(idx + 1, sum_s, sum_u + v, cnt_s, cnt_u + 1)

        dfs(0, 0, 0, 0, 0)
        return res

    right_states = gen_half(right)

    for ss, su, cs, cu in right_states:
        right_map[(ss, su)][(cs, cu)] += 1

    ans = 0

    left_states = gen_half(left)

    for ss, su, cs, cu in left_states:
        need = (x - ss, diff - su)

        if need not in right_map:
            continue

        bucket = right_map[need]

        for (rs, ru), ways in bucket.items():
            a = cs + rs
            b = cu + ru
            c = n - a - b

            ans += ways * fact[a] * fact[b] * fact[c]
            ans %= MOD

    return ans

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    k = int(input())

    unlucky = []
    if k:
        unlucky = list(map(int, input().split()))

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    total = fact[n]

    if k == 0:
        print(total)
        return

    if k == 1:
        ans = (total - subset_bad(a, unlucky[0], fact)) % MOD
        print(ans)
        return

    x, y = unlucky

    bad_x = subset_bad(a, x, fact)
    bad_y = subset_bad(a, y, fact)
    bad_both = both_bad(a, x, y, fact)

    ans = (total - bad_x - bad_y + bad_both) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The first helper computes the number of permutations that hit a single unlucky position. It performs a standard meet-in-the-middle subset-sum count, but instead of merely counting subsets, it weights them by `size!(n-size)!`.

The second helper computes the intersection term for inclusion-exclusion. Each element is assigned to one of three groups: `S`, `U`, or neither. The meet-in-the-middle combines ternary states whose sums complete the required targets.

A subtle point is that the weight depends only on the final group sizes, not on the particular elements. That allows all states with identical `(sumS, sumU, sizeS, sizeU)` information to be aggregated.

Another detail is handling the unlucky positions in sorted order. Since all segment lengths are positive, reaching both positions means reaching
