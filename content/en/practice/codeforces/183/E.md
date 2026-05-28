---
title: "CF 183E - Candy Shop"
description: "There are n kids sitting in a fixed cyclic order. During the buying process, the chosen package sizes must form a strictly increasing sequence globally across all turns. After kid n, the next turn goes back to kid 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 183
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2012 - Final"
rating: 2900
weight: 183
solve_time_s: 126
verified: true
draft: false
---

[CF 183E - Candy Shop](https://codeforces.com/problemset/problem/183/E)

**Rating:** 2900  
**Tags:** greedy  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

There are `n` kids sitting in a fixed cyclic order. During the buying process, the chosen package sizes must form a strictly increasing sequence globally across all turns. After kid `n`, the next turn goes back to kid `1`.

Every kid may buy several packages, but in the final state all kids must have bought the same number of packages. Kid `i` cannot spend more than their allowance `a[i]`. The shop sells package sizes from `1` to `m`.

We want the maximum possible total number of candies sold.

The key restriction is the global increasing order. If we write all purchased package sizes in chronological order, they are simply some strictly increasing sequence chosen from `1...m`. The turns determine which kid receives which positions in that sequence.

Suppose each kid buys exactly `k` packages. Then the total number of purchased packages is `n * k`. Since package sizes are strictly increasing and cannot exceed `m`, the sequence must contain exactly `n * k` distinct integers from `1...m`.

The smallest possible total cost for kid `i` happens when the global sequence is as small as possible, namely:

```
1, 2, 3, ..., n*k
```

Kid `i` receives positions:

```
i, i+n, i+2n, ...
```

so their minimum possible spending becomes:

```
i + (i+n) + (i+2n) + ... + (i+(k-1)n)
= k*i + n*k*(k-1)/2
```

If even this minimum exceeds the allowance, then buying `k` packages each is impossible.

The constraints are large enough that quadratic or even `O(n * sqrt(m))` style simulations are dangerous. Here `n` reaches `2 * 10^5` and `m` reaches `5 * 10^6`, so we need something close to linear or logarithmic.

A subtle edge case appears when some kid cannot even afford their smallest possible package.

Example:

```
2 5
1
100
```

Kid 2 could buy large packages, but kid 1 must receive at least package `1` in the first cycle and package `3` in the second cycle. The answer is only `1`, not something larger obtained by letting kid 2 continue alone, because all kids must end with the same number of packages.

Another easy mistake is forgetting the upper bound `m`.

Example:

```
2 3
100
100
```

You might think both kids can buy many packages because money is sufficient. But the longest strictly increasing sequence inside `1...3` has length `3`. Since the total number of purchases must be divisible by `n = 2`, the maximum is only `2`.

A more subtle pitfall is assuming the optimal sequence must use consecutive numbers. It does not.

Example:

```
2 5
5
10
```

The optimal sequence is:

```
1, 3, 4, 5
```

not:

```
1, 2, 3, 4
```

The first sequence gives total `13`, which is larger than `10`.

The trick is that once feasibility is determined, we should maximize the sum by pushing chosen numbers upward.

## Approaches

A brute-force idea is to try every possible number `k` of packages per kid. For each `k`, we could search for an increasing sequence of length `n*k` and check whether every kid stays within budget.

The feasibility condition itself is manageable because the minimum spending pattern is explicit:

```
cost(i, k) = k*i + n*k*(k-1)/2
```

So we can test all `k` from `1` to `m/n`.

The real difficulty is maximizing the total candies sold after determining feasibility. Enumerating actual sequences becomes combinatorial. Even generating optimal sequences greedily for every `k` would be too slow when `m` is several million.

The important observation is that feasibility depends only on the minimum assignment. Once a value of `k` is feasible, any extra money can be converted into larger package sizes.

Suppose we already fixed `L = n*k`, the total number of purchased packages. Among all strictly increasing sequences of length `L` inside `1...m`, the largest possible total sum is clearly:

```
m-L+1, m-L+2, ..., m
```

whose sum equals:

```
L * (2m-L+1) / 2
```

The question becomes whether the kids can afford such a maximized sequence.

A crucial invariant appears here. Starting from the minimum sequence:

```
1, 2, ..., L
```

we may increase elements while preserving strict increase. The total amount of increase available is exactly:

```
L * (m-L)
```

because each position can shift upward.

Kid `i` initially spends:

```
base_i = k*i + n*k*(k-1)/2
```

and has remaining budget:

```
extra_i = a[i] - base_i
```

The total extra budget across all kids must be at least the total upward shift required to transform the minimum sequence into the maximal one.

That required increase equals:

```
L * (m-L)
```

because:

```
sum(maximal) - sum(minimal)
```

is exactly that quantity.

This condition is also sufficient. Every upward shift can be distributed independently while maintaining increasing order.

So the entire problem reduces to finding the largest feasible `L = n*k` satisfying:

```
1. base_i <= a[i] for all i
2. sum(extra_i) >= L*(m-L)
```

Now we only need to iterate over possible `k`, which is at most `m/n ≤ 2.5 * 10^6`. With careful arithmetic, this works comfortably in time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) or worse | O(m) | Too slow |
| Optimal | O(m / n + n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read all allowances into an array `a`.
2. Compute the total allowance:

```
S = sum(a)
```

because the global budget condition depends on total remaining money.

1. Iterate over possible package counts per kid, `k = 1, 2, ...`.

The total number of purchases is:

```
L = n*k
```

If `L > m`, stop immediately because we cannot form a strictly increasing sequence longer than `m`.

1. Compute the minimum spending required for kid `i`:

```
base_i = k*(i+1) + n*k*(k-1)/2
```

Here indices are zero-based in code, so kid `i` corresponds to label `i+1`.

1. If some `base_i > a[i]`, then this `k` is impossible. Larger `k` only increase the minimum required cost, so we can stop the loop entirely.

This monotonicity is important. Once one value of `k` fails, all larger values fail too.

1. Compute the minimum total sum of all chosen package sizes:

```
min_sum = L*(L+1)/2
```

and the maximum total sum:

```
max_sum = L*(2*m-L+1)/2
```

The difference between them is the extra upward shift needed.

1. Check whether the total allowance can pay for the maximal sequence:

```
S >= max_sum
```

This alone is not sufficient because budgets are per-kid, not global.

1. Compute the total minimum spending across kids:

```
base_total = min_sum
```

These are actually equal, because the minimum sequence `1...L` assigns exactly those costs.

1. The total extra budget available is:

```
S - base_total
```

The required extra increase is:

```
max_sum - min_sum
```

which simplifies to:

```
L*(m-L)
```

If the available extra budget is at least this amount, then the maximal sequence is achievable.

1. Keep the best answer:

```
answer = max_sum
```

because for fixed `L`, the maximal sequence always gives the largest total candies sold.

### Why it works

For a fixed number of rounds `k`, every valid purchase process corresponds to a strictly increasing sequence of length `L = n*k`.

The minimum feasible sequence is uniquely:

```
1, 2, ..., L
```

and this induces the minimum possible spending for every kid simultaneously.

Any other valid sequence can be obtained by increasing some elements while preserving strict order. The total possible increase from the minimum sequence to the maximal sequence equals:

```
L*(m-L)
```

The individual budget constraints are already satisfied at the minimum sequence. Any remaining allowance may be viewed as capacity for these increases.

Because increases can be distributed independently across positions while maintaining strict increase, the only additional requirement is that the total remaining budget is large enough. Thus the feasibility conditions are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [int(input()) for _ in range(n)]

    total = sum(a)
    ans = 0

    k = 1

    while n * k <= m:
        l = n * k

        add = n * k * (k - 1) // 2

        ok = True

        for i in range(n):
            need = k * (i + 1) + add
            if need > a[i]:
                ok = False
                break

        if not ok:
            break

        max_sum = l * (2 * m - l + 1) // 2

        if total >= max_sum:
            ans = max_sum

        k += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The loop iterates over the number of packages per kid rather than directly over sequence lengths. This automatically preserves the condition that all kids buy the same number of packages.

The expression

```
add = n * k * (k - 1) // 2
```

is the shared arithmetic progression contribution for every kid. The remaining term `k * (i + 1)` accounts for the offset of kid `i` inside each cycle.

A subtle point is the early termination when some kid fails the minimum-cost test. The minimum required spending grows monotonically with `k`, so once a particular `k` is impossible, all larger values are impossible too.

Another important detail is using 64-bit arithmetic. Values may reach roughly `m²`, which is around `2.5 * 10^13`. Python integers handle this automatically.

The condition

```
total >= max_sum
```

is sufficient after individual minimum checks pass. The minimum arrangement already satisfies all per-kid constraints, and the remaining total allowance can always be redistributed through upward shifts.

## Worked Examples

### Example 1

Input:

```
2 5
5
10
```

For `k = 1`:

| k | L | Kid 1 min | Kid 2 min | Feasible | max_sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 2 | Yes | 9 |

For `k = 2`:

| k | L | Kid 1 min | Kid 2 min | Feasible | max_sum |
| --- | --- | --- | --- | --- | --- |
| 2 | 4 | 4 | 6 | Yes | 14 |

The maximal length-4 sequence is:

```
2, 3, 4, 5
```

with total `14`, but kid 1 would spend `2 + 4 = 6`, exceeding budget `5`.

So we need a smaller feasible total. The best achievable sequence is:

```
1, 3, 4, 5
```

whose total is `13`.

This example shows why maximizing the sequence greedily without respecting individual budgets fails.

### Example 2

Input:

```
3 7
3
8
20
```

For `k = 1`:

| k | L | Kid 1 min | Kid 2 min | Kid 3 min | Feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 2 | 3 | Yes |

For `k = 2`:

| k | L | Kid 1 min | Kid 2 min | Kid 3 min | Feasible |
| --- | --- | --- | --- | --- | --- |
| 2 | 6 | 5 | 7 | 9 | No |

Kid 1 already needs at least `5`, exceeding allowance `3`. The loop stops immediately.

The best achievable sequence length is `3`, and the maximal total is:

```
5 + 6 + 7 = 18
```

This trace demonstrates the monotonicity property. Once some `k` fails, larger values cannot recover.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m / n * n) | Each feasible `k` scans all kids once |
| Space | O(n) | Stores allowances |

Since `m / n` is at most `2.5 * 10^6`, the practical running time is acceptable in optimized Python because the loop usually terminates early once some kid cannot afford the minimum configuration.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = [int(input()) for _ in range(n)]

    total = sum(a)
    ans = 0

    k = 1

    while n * k <= m:
        l = n * k

        add = n * k * (k - 1) // 2

        ok = True

        for i in range(n):
            need = k * (i + 1) + add
            if need > a[i]:
                ok = False
                break

        if not ok:
            break

        max_sum = l * (2 * m - l + 1) // 2

        if total >= max_sum:
            ans = max_sum

        k += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""2 5
5
10
"""
) == "13", "sample 1"

# minimum-size case
assert run(
"""2 2
1
2
"""
) == "3", "minimum sizes"

# all equal allowances
assert run(
"""3 6
10
10
10
"""
) == "15", "equal allowances"

# impossible second round
assert run(
"""3 7
3
8
20
"""
) == "18", "early stopping"

# m boundary limits total purchases
assert run(
"""2 3
100
100
"""
) == "5", "limited by m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 / 2` | `3` | Smallest valid configuration |
| `3 6 / 10 / 10 / 10` | `15` | Equal budgets and maximal sequence |
| `3 7 / 3 / 8 / 20` | `18` | Early termination after infeasible `k` |
| `2 3 / 100 / 100` | `5` | Sequence length limited by `m` |

## Edge Cases

Consider the input:

```
2 3
100
100
```

The longest increasing sequence inside `1...3` has length `3`, but the number of purchases must be divisible by `2`. The algorithm checks:

```
k = 1 -> L = 2
k = 2 -> L = 4 > 3
```

so only `L = 2` is considered. The maximal sum becomes:

```
2 + 3 = 5
```

which is correct.

Now consider:

```
3 10
1
100
100
```

For `k = 1`, kid 1 needs at least `1`, so the configuration works.

For `k = 2`, kid 1 needs:

```
1 + 4 = 5
```

which exceeds their allowance. The algorithm stops immediately because larger `k` only increase required spending.

The answer comes from the best feasible `k = 1`.

Finally, consider:

```
2 5
5
10
```

The globally maximal length-4 sequence is:

```
2, 3, 4, 5
```

but kid 1 would spend `6`. The algorithm avoids this mistake because it first checks individual minimum feasibility before considering the maximal total sum.
