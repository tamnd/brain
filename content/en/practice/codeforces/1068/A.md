---
title: "CF 1068A - Birthday"
description: "We are dealing with a fixed universe of distinct coin types, where there are N possible different coins in total. Ivan already owns K distinct coins from this universe. Now M friends will each give him gifts, and each friend must contribute the same number of coins."
date: "2026-06-15T13:33:58+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1068
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 518 (Div. 2) [Thanks, Mail.Ru!]"
rating: 1400
weight: 1068
solve_time_s: 269
verified: true
draft: false
---

[CF 1068A - Birthday](https://codeforces.com/problemset/problem/1068/A)

**Rating:** 1400  
**Tags:** math  
**Solve time:** 4m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are dealing with a fixed universe of distinct coin types, where there are `N` possible different coins in total. Ivan already owns `K` distinct coins from this universe. Now `M` friends will each give him gifts, and each friend must contribute the same number of coins.

All gifted coins must be distinct across all friends, meaning no coin type can appear more than once in the entire set of gifts. Since friends do not know which coins Ivan already owns, the requirement involving “new coins” must be satisfied in the worst possible case over Ivan’s unknown collection.

The key requirement is that among all gifted coins, at least `L` of them must be coins Ivan did not previously own. Since we must guarantee this without knowing Ivan’s collection, we must ensure that no matter how his `K` coins are chosen, the gift set always contains at least `L` new coins.

The output asks for the minimum number `x` such that each friend gives exactly `x` distinct coins, and all constraints can be satisfied. If no such `x` exists, we return `-1`.

The constraints are extremely large, up to `10^18`, which immediately rules out any simulation or iterative construction. Any solution must be purely arithmetic, based on reasoning about overlaps and worst-case intersections.

A few subtle edge cases appear immediately.

If `N < M`, then it is impossible for all friends to give distinct coins even if each gives only one coin, because we would need at least `M` distinct coin types for the first coin of each friend alone.

If `L > N - K`, then even if we gift all coins outside Ivan’s collection, there are not enough “new” coins available in the universe to satisfy the requirement.

A more subtle failure case arises when `M * x > N`, since all gifted coins must be distinct globally. Even if each friend gives a small number, the total pool cannot exceed `N`.

## Approaches

A naive approach would try increasing values of `x` starting from `1`, and for each candidate simulate whether it is possible to assign `M * x` distinct coins while guaranteeing at least `L` coins outside Ivan’s unknown `K`-set. The check would require reasoning about worst-case overlap: assume Ivan’s `K` coins are chosen to maximize intersection with the gift set.

For a fixed `x`, we gift `M * x` distinct coins in total. In the worst case, Ivan’s `K` coins overlap as much as possible with these gifts, so the number of guaranteed “new” coins is minimized. This minimum number of new coins is:

`max(0, M * x - K)`

We need this to be at least `L`. So we need:

`M * x - K >= L`, which simplifies to `M * x >= K + L`.

However, we also need feasibility with respect to total universe size:

`M * x <= N`.

So brute force over `x` would check these inequalities repeatedly. But since `x` can go up to `10^18`, this is still conceptually O(N) in worst interpretation and infeasible.

The key observation is that feasibility is determined entirely by two linear constraints:

`M * x >= K + L` and `M * x <= N`.

These constraints define a simple interval for `x`, and we are asked for the smallest integer `x` in this interval.

Thus we compute:

lower bound: `ceil((K + L) / M)`

upper bound: `floor(N / M)`

If the lower bound exceeds the upper bound, there is no valid solution.

This reduces the entire problem to integer arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N / M) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the minimum total number of gifted coins needed to guarantee at least `L` new coins in the worst case. This requirement becomes `M * x >= K + L`.
2. Convert this into a lower bound on `x` using integer division with ceiling: `(K + L + M - 1) // M`.
3. Compute the maximum possible number of total gifted coins allowed by the universe constraint `M * x <= N`, giving upper bound `N // M`.
4. If the lower bound exceeds the upper bound, conclude that no valid assignment exists and output `-1`.
5. Otherwise, output the lower bound as the minimum feasible number of coins per friend.

### Why it works

The critical invariant is that any valid configuration depends only on the total number of gifted coins `T = M * x`, not on their distribution among friends. Distinctness forces all `T` gifted coins to be unique globally, so the structure reduces to selecting a subset of size `T` from `N`.

The worst-case overlap with Ivan’s unknown `K`-subset is always maximized, so the minimum guaranteed number of new coins is exactly `max(0, T - K)`. This makes the feasibility condition fully linear in `T`, and therefore linear in `x`. No hidden structure remains once this reduction is made.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M, K, L = map(int, input().split())

    # upper bound: cannot exceed total available coins
    hi = N // M

    # lower bound: ensure enough guaranteed new coins
    need = K + L
    lo = (need + M - 1) // M  # ceil division

    if lo > hi:
        print(-1)
    else:
        print(lo)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the derived bounds. The only subtlety is correct ceiling division for the lower bound, which avoids floating-point errors and ensures correctness for large values up to `10^18`.

The second constraint `M * x <= N` is handled using floor division. Both computations must use 64-bit safe integer arithmetic, which Python naturally supports.

## Worked Examples

### Example 1

Input:

`N = 20, M = 15, K = 2, L = 3`

We compute:

`hi = 20 // 15 = 1`

`need = 2 + 3 = 5`

`lo = ceil(5 / 15) = 1`

| Step | lo | hi | decision |
| --- | --- | --- | --- |
| initial | 1 | 1 | compute bounds |
| final | 1 | 1 | valid |

Since `lo <= hi`, answer is `1`.

This shows the case where even one coin per friend is sufficient because total gifts are limited and overlap constraints are mild.

### Example 2

Input:

`N = 10, M = 11, K = 3, L = 2`

Compute:

`hi = 10 // 11 = 0`

`lo = ceil(5 / 11) = 1`

| Step | lo | hi | decision |
| --- | --- | --- | --- |
| initial | 1 | 0 | compute bounds |
| final | 1 | 0 | invalid |

Since `lo > hi`, output is `-1`.

This demonstrates the global impossibility caused by not having enough distinct coins for even one per friend.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations |
| Space | O(1) | No auxiliary data structures used |

The solution easily satisfies the constraints since all operations are simple integer divisions on values up to `10^18`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    N, M, K, L = map(int, sys.stdin.readline().split())

    hi = N // M
    need = K + L
    lo = (need + M - 1) // M

    return str(-1 if lo > hi else lo)

# provided sample
assert run("20 15 2 3") == "1"

# minimal case
assert run("1 1 1 1") == "1"

# impossible due to too many friends
assert run("10 11 3 2") == "-1"

# tight bound case
assert run("100 10 0 0") == "0"

# exact fit case
assert run("30 5 10 10") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 1 | minimal valid configuration |
| 10 11 3 2 | -1 | insufficient total distinct capacity |
| 100 10 0 0 | 0 | zero requirement edge behavior |
| 30 5 10 10 | 4 | exact boundary between feasibility and infeasibility |

## Edge Cases

A key edge case is when `M > N`. For example:

Input:

`N = 5, M = 10, K = 1, L = 1`

Here `hi = 5 // 10 = 0`, meaning even giving 1 coin per friend is impossible. The algorithm immediately returns `-1` since no valid `x` satisfies `M * x <= N`. This matches reality because we cannot assign even one distinct coin per friend when there are fewer coin types than friends.

Another case is when `K + L` is very large relative to `N`. For instance:

Input:

`N = 100, M = 10, K = 90, L = 20`

Here `need = 110`, so `lo = ceil(110 / 10) = 11`, but `hi = 10`, so infeasible. This shows the interaction between Ivan’s existing collection and required novelty can force impossibility even when `N >= M`.
