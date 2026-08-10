---
title: "CF 102396J - Superpermutations"
description: "The construction starts with the sequence [1]. To move from order m to order m+1, we scan every length-m window of the current sequence. Whenever such a window is a permutation of 1..m, we insert the new value m+1 followed by that same permutation immediately after the window."
date: "2026-08-10T18:55:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "J"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 448
verified: true
draft: false
---

[CF 102396J - Superpermutations](https://codeforces.com/problemset/problem/102396/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The construction starts with the sequence `[1]`. To move from order `m` to order `m+1`, we scan every length-`m` window of the current sequence. Whenever such a window is a permutation of `1..m`, we insert the new value `m+1` followed by that same permutation immediately after the window.

The resulting sequence contains every permutation exactly once as a length-`m` window. The task is not to construct this enormous sequence. Instead, for a given permutation `a` of `1..n`, we need the 1-indexed position where its unique occurrence begins, modulo `10^9+7`. The official statement gives the same recursive construction and the same bounds, including `n <= 300000`.

The constraint `n <= 300000` rules out anything that explicitly constructs the superpermutation or enumerates its permutations. Its length is

[
|s_n|=1!+2!+\cdots+n!,
]

so even storing `s_n` is impossible. A solution must process the given permutation in roughly linear or `O(n log n)` time and use `O(n)` memory. The one-second limit makes an `O(n log n)` implementation worth keeping tight, while anything involving `n!` work is completely out of reach.

There are several edge cases that expose common mistakes. For `n=1`, the only input is `[1]`, and the answer is `1`. A recurrence that assumes a previous nonempty permutation would fail here. For `n=2`, the permutation `[2,1]` starts at position `2` in `s_2=[1,2,1]`, while `[1,2]` starts at position `1`. This catches an off-by-one error in the contribution of the maximum element. When the maximum is at the end, such as `[2,3,1,4]`, its insertion occurs after the underlying permutation, but the target itself can start before that insertion. Treating every occurrence as beginning at the inserted `4` gives the wrong answer `9` instead of `6`. Finally, the input guarantees that the values form a permutation, so an all-equal input such as `3 / 1 1 1` is not a valid test case and must not be used to test the submitted solution.

## Approaches

A direct solution would construct the sequences `s_1,s_2,...,s_n`. At stage `m`, we have to inspect every length-`m` window and decide whether it contains every value from `1` through `m`. There are already `Theta(m!)` positions at that stage, and checking one window naively takes `Theta(m)` time. The final stage alone costs `Theta(n * n!)` operations in the worst case, in addition to requiring `Theta(n!)` memory just to store the sequence. With `n=300000`, this is not remotely feasible.

The brute force works because every insertion is local. If a permutation `q` of size `m-1` occurs in `s_{m-1}`, the construction inserts `[m,q]` immediately after it. This creates exactly `m` consecutive size-`m` permutations around that insertion. The useful observation is that these `m` permutations are simply cyclic rotations of `q` with `m` inserted at different positions.

Suppose the current permutation is `p`, and the maximum value `m` occurs at position `k`. Remove `m` and rotate the remaining sequence so that the element immediately after `m` becomes the first element. Call the resulting permutation `q`. Then `q` is precisely the size-`m-1` permutation whose insertion creates `p`.

There is another quantity we need. Let `R_m(p)` be the zero-based rank of `p` among the `m!` permutations in the order in which they occur in `s_m`. If `q` has rank `R_{m-1}(q)`, all of its `m` derived permutations form one consecutive group. The position of `p` inside this group is `m-k`, because `m` is at position `k`. Hence

[
R_m(p)=mR_{m-1}(q)+(m-k).
]

The actual position has an even simpler recurrence. Before the group for `q`, every earlier permutation of size `m-1` caused an insertion of `m` elements, so `q` is shifted by `mR_{m-1}(q)` positions. The target begins `m-k` positions later relative to the start of `q`. Thus

[
P_m(p)=P_{m-1}(q)+R_m(p).
]

Starting with `P_1=1`, the final answer is consequently

[
P_n=1+\sum_{m=2}^{n}R_m.
]

The remaining challenge is to obtain every value `m-k` without explicitly rotating the permutation at every level.

The rotations have a clean interpretation on a circle. Start with the original permutation as a circular list. When processing maximum `m`, all larger values have already been removed, and the current linear permutation starts immediately after the previously removed maximum. Removing `m` means that the next surviving element becomes the new start. Therefore `m-k` is exactly the number of currently alive positions after `m` and before the current start, measured cyclically.

A Fenwick tree maintains which original positions are still alive. A doubly linked list maintains the current circular successor when a position is removed. Together they let us compute every `m-k` in `O(log n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(n * n!)` | `Theta(n!)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Store `pos[x]`, the original array position of every value `x`. The values are unique, so this gives constant-time access to the position of the current maximum.
2. Treat the original array positions as a circular doubly linked list. Initially every position is alive, `next[i]` points to the next position, and `prev[i]` points to the previous position. The current linear representation starts at position `1`.
3. Initialize a Fenwick tree with `1` at every position. A Fenwick prefix sum now tells us how many currently alive elements occur up to a given original position.
4. Process `m=n,n-1,...,2`. Let `x=pos[m]`. The current permutation of `1..m` starts at `start` and follows the circular order of the alive positions until it reaches `x`.
5. Let `d_m=m-k`, where `k` is the 1-indexed position of `m` in the current permutation. If `start <= x`, then the elements after `x` before wrapping to `start` are counted by `m - prefix(x)`. If `start > x`, the relevant interval is the ordinary interval `(x,start)`, whose number of alive positions is `prefix(start-1)-prefix(x)`. This gives `d_m` without constructing the rotated permutation.
6. Remove `x` from the Fenwick tree and the linked list. The new `start` becomes `next[x]`, because removing `m` rotates the remaining permutation so that the successor of `m` is first.
7. After all `d_m` values have been computed, process `m=2,3,...,n`. Maintain `rank`, initially zero. The recurrence

[
rank=m\cdot rank+d_m
]

computes `R_m` from `R_{m-1}`. Add this rank to the answer because `P_m=P_{m-1}+R_m`.

1. Start the answer at `1`, corresponding to the only permutation of size one. Perform every multiplication and addition modulo `10^9+7`.

### Why it works

At every size `m`, removing the maximum from the target permutation and rotating after it produces exactly the permutation `q` whose insertion generated the target. The construction processes the occurrences of size `m-1` from left to right, and each such occurrence generates exactly one consecutive group of `m` size-`m` permutations. Inside that group, the permutation with maximum at position `k` is the `(m-k)`-th member, so `R_m=mR_{m-1}+(m-k)`. Earlier groups shift the corresponding occurrence by exactly `m` positions each, giving `P_m=P_{m-1}+R_m`. The circular linked list represents exactly the sequence obtained by repeatedly removing the current maximum and starting immediately after it, while the Fenwick tree counts its surviving elements. Thus every `d_m=m-k` used by the recurrence is exact, and the final accumulated position is the required occurrence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        pos[x] = i

    # Fenwick tree containing 1 for every currently alive position.
    bit = [0] * (n + 1)

    # Build the Fenwick tree in O(n).
    for i in range(1, n + 1):
        bit[i] += 1
        j = i + (i & -i)
        if j <= n:
            bit[j] += bit[i]

    def prefix(x):
        s = 0
        while x:
            s += bit[x]
            x -= x & -x
        return s

    def remove(x):
        while x <= n:
            bit[x] -= 1
            x += x & -x

    # Circular doubly linked list of alive positions.
    nxt = [0] * (n + 1)
    prv = [0] * (n + 1)

    for i in range(1, n + 1):
        nxt[i] = i + 1 if i < n else 1
        prv[i] = i - 1 if i > 1 else n

    # d[m] = m - position_of_m_in_the_current_permutation.
    d = [0] * (n + 1)

    start = 1

    for m in range(n, 1, -1):
        x = pos[m]

        px = prefix(x)

        if start <= x:
            d[m] = m - px
        else:
            d[m] = prefix(start - 1) - px

        # Remove x and rotate the remaining circular order so
        # that its successor becomes the new first position.
        nx = nxt[x]
        p = prv[x]

        nxt[p] = nx
        prv[nx] = p
        start = nx

        remove(x)

    rank = 0
    answer = 1

    for m in range(2, n + 1):
        rank = (m * rank + d[m]) % MOD
        answer += rank
        if answer >= MOD:
            answer -= MOD

    print(answer)

if __name__ == "__main__":
    solve()
```

The `pos` array lets the descending phase find the current maximum in constant time. The Fenwick tree contains one unit for every value that has not yet been removed, so its prefix sum represents the number of surviving elements in an interval of the original permutation.

The linked list is needed for a different reason. The current permutation is not the original array with some entries deleted from the left or right. It is a circular rotation whose starting point changes after every maximum is removed. `start` records that rotation, and `nxt` and `prv` update it in constant time after a deletion.

The expression for `d[m]` is deliberately written using the current size `m`. Before removing `m`, exactly `m` positions are alive. When `start <= x`, the elements after `x` before wrapping are simply all alive elements after `x`, which is `m-prefix(x)`. When `start > x`, the relevant interval does not wrap, so the difference of two prefix sums is required.

The second pass reconstructs the ranks from smallest size to largest. `rank` stores `R_{m-1}` before the update and becomes `R_m` after multiplying by `m` and adding `d[m]`. The answer starts from `P_1=1`, then receives exactly one contribution `R_m` at each level.

Python integers do not overflow, but taking the modulus after each recurrence keeps the values small and avoids unnecessary large-integer arithmetic. The Fenwick tree itself stores only values up to `n`, so its entries never become large.

## Worked Examples

### Sample 1

The input permutation is `[2,3,1]`. Its positions are `pos[1]=3`, `pos[2]=1`, and `pos[3]=2`.

| `m` | `start` | `pos[m]` | Alive prefix at `pos[m]` | `d[m]` | New `start` |
| --- | --- | --- | --- | --- | --- |
| 3 | 1 | 2 | 2 | 1 | 3 |
| 2 | 3 | 1 | 1 | 0 | 2 |

For `m=3`, the current permutation is `[2,3,1]`, so `3` is at position `2` and `d_3=3-2=1`. After removing `3`, the remaining circular order is `[1,2]` starting from position `3`.

The rank calculation is

[
R_2=0,
\qquad
R_3=3\cdot0+1=1.
]

The position is

[
P_3=1+R_2+R_3=1+0+1=2.
]

Thus the answer is `2`, matching the sample.

### Sample 2

The permutation is `[2,3,1,4]`, with positions `pos[1]=3`, `pos[2]=1`, `pos[3]=2`, and `pos[4]=4`.

| `m` | `start` | `pos[m]` | `d[m]` | New `start` | `R_m` | Answer after `R_m` |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 1 | 4 | 0 | 1 | 0 | 1 |
| 3 | 1 | 2 | 1 | 3 | 1 | 2 |
| 2 | 3 | 1 | 0 | 2 | 2 | 4 |

The final rank values are `R_2=0`, `R_3=1`, and `R_4=4`. Hence

[
P_4=1+0+1+4=6.
]

This example demonstrates why the rank contribution matters. The permutation `[2,3,1]` does not stay at position `2` after moving from `s_3` to `s_4`, because the earlier permutation group has inserted four new elements before it. Its shifted occurrence is the prefix of the target `[2,3,1,4]`, which starts at position `6`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Each of the `n` positions is removed once, with Fenwick updates and prefix queries taking `O(log n)`. The rank pass is linear. |
| Space | `O(n)` | The position array, Fenwick tree, linked-list arrays, and `d` array all have size `O(n)`. |

For `n=300000`, the algorithm never constructs a superpermutation and never enumerates its `n!` permutations. The `O(n log n)` data-structure work and linear auxiliary memory fit the intended scale of the constraints, whereas the explicit construction would already be impossible for very small values compared with the maximum input.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    pos = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        pos[x] = i

    bit = [0] * (n + 1)

    for i in range(1, n + 1):
        bit[i] += 1
        j = i + (i & -i)
        if j <= n:
            bit[j] += bit[i]

    def prefix(x):
        s = 0
        while x:
            s += bit[x]
            x -= x & -x
        return s

    def remove(x):
        while x <= n:
            bit[x] -= 1
            x += x & -x

    nxt = [0] * (n + 1)
    prv = [0] * (n + 1)

    for i in range(1, n + 1):
        nxt[i] = i + 1 if i < n else 1
        prv[i] = i - 1 if i > 1 else n

    d = [0] * (n + 1)
    start = 1

    for m in range(n, 1, -1):
        x = pos[m]
        px = prefix(x)

        if start <= x:
            d[m] = m - px
        else:
            d[m] = prefix(start - 1) - px

        nx = nxt[x]
        p = prv[x]

        nxt[p] = nx
        prv[nx] = p
        start = nx

        remove(x)

    rank = 0
    answer = 1

    for m in range(2, n + 1):
        rank = (m * rank + d[m]) % MOD
        answer += rank
        if answer >= MOD:
            answer -= MOD

    sys.stdin = old_stdin
    return str(answer)

# Provided samples
assert solution("3\n2 3 1\n") == "2", "sample 1"
assert solution("4\n2 3 1 4\n") == "6", "sample 2"
assert solution("4\n4 3 1 2\n") == "14", "sample 3"

# Minimum size
assert solution("1\n1\n") == "1", "minimum size"

# Maximum at the first position
assert solution("3\n3 1 2\n") == "3", "maximum at first"

# Maximum at the last position
assert solution("2\n1 2\n") == "1", "maximum at last, identity"

assert solution("2\n2 1\n") == "2", "maximum at first for n=2"

# A larger custom case exercising several circular rotations
assert solution("5\n5 1 4 2 3\n") == "17", "circular rotation case"

# Maximum-size valid input.
# The identity permutation has answer 1 for every n.
n = 300000
identity = " ".join(map(str, range(1, n + 1)))
assert solution(f"{n}\n{identity}\n") == "1", "maximum n"

# An all-equal input is deliberately not tested because the problem
# guarantees that the second line is a permutation, so duplicates are invalid.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum-size boundary and base case |
| `3 / 3 1 2` | `3` | Maximum at the first position |
| `2 / 1 2` | `1` | Maximum at the last position and zero rank contribution |
| `2 / 2 1` | `2` | Smallest nontrivial insertion offset |
| `5 / 5 1 4 2 3` | `17` | Multiple circular rotations and nonzero ranks |
| `300000 / 1 2 ... 300000` | `1` | Maximum input size and linear memory behavior |

## Edge Cases

For `n=1`, the input is exactly `[1]`. There is no maximum-removal loop because the loop starts at `m=2`. The rank remains zero and the answer remains its initial value `1`, which is exactly the position of `[1]` in `s_1`.

For `n=2` and permutation `[2,1]`, the current start is position `1` and the maximum `2` is also at position `1`. The Fenwick tree reports one surviving element after position `1`, so `d_2=1`. The rank becomes `R_2=1`, and the answer becomes `1+1=2`. This matches `s_2=[1,2,1]`.

For the maximum at the first position, consider `[3,1,2]`. The maximum `3` has `k=1`, so `d_3=2`. After removing it, the remaining order starts at `1`. At size two, the maximum `2` is at the end, giving `d_2=0`. Thus `R_2=0`, `R_3=2`, and the answer is `1+0+2=3`. Indeed, `[3,1,2]` starts at position `3` in `s_3`.

For the maximum at the last position, `[2,3,1,4]` has `d_4=0`, because the `4` occurs at position `4`. The next level has `d_3=1`, which gives `R_3=1` and then `R_4=4`. The final position is `1+0+1+4=6`. The target starts at position `6`, before the inserted `4`, so an algorithm that always looks for the position of the maximum itself would be incorrect.

For a circular wrap-around, `[4,3,1,2]` is particularly useful. The maximum `4` is initially at position `1`, so `d_4=3`. Removing it makes position `2` the new start. The next maximum `3` is also at the new first position, giving `d_3=2`. Finally `d_2=0`. The ranks are `R_2=0`, `R_3=2`, and `R_4=11`, so the answer is `1+0+2+11=14`. The linked list is what makes this wrap-around behavior explicit instead of forcing us to physically rotate the permutation.

An all-equal input such as `[1,1,1]` would violate the input guarantee that every value from `1` through `n` occurs exactly once. The algorithm relies on that guarantee when constructing `pos`, when interpreting the current maximum, and when removing exactly one position per value. It is consequently an invalid problem instance rather than an edge case of the required solution.
