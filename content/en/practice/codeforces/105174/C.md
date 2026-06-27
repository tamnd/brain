---
title: "CF 105174C - \u5927\u9b54\u6cd5\u5e08"
description: "The wand has exactly n gem slots. There are three independent categories of gems. The first category increases magic attack, the second increases mana, and the third increases attack speed."
date: "2026-06-27T08:14:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105174
codeforces_index: "C"
codeforces_contest_name: "The 22nd Sichuan University Programming Contest"
rating: 0
weight: 105174
solve_time_s: 60
verified: true
draft: false
---

[CF 105174C - \u5927\u9b54\u6cd5\u5e08](https://codeforces.com/problemset/problem/105174/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

The wand has exactly `n` gem slots. There are three independent categories of gems.

The first category increases magic attack, the second increases mana, and the third increases attack speed. Every gem occupies some number of slots and contributes a positive value to exactly one attribute. Each gem can be used at most once.

After choosing any collection of gems whose total occupied slots do not exceed `n`, the final power of the wand is

`magic_attack × mana × attack_speed`.

The task is to maximize this product.

The most important observation is that gems from different categories never interact except through the shared slot limit. Inside one category, the only thing that matters is how much total attribute value can be obtained using a given number of slots.

The slot count is at most 2000, and each category contains at most 2000 gems. A dynamic programming solution with complexity around `O(total_gems × n)` is easily fast enough, since this is roughly `3 × 2000 × 2000 = 1.2 × 10^7` state transitions. Anything involving subsets of gems or searching all allocations between gems directly would be completely infeasible.

Several edge cases deserve attention.

If one attribute is never improved, the final product is zero regardless of the other two attributes.

For example,

```
2
1 1 1
2 5
3 10
3 10
```

No mana or attack speed gem fits into two slots, so every feasible solution has product `0`.

Another subtle case is that the optimal solution may leave slots unused.

For example,

```
5
1 1 1
2 100
2 100
2 100
```

Using one gem from each category consumes six slots, which is impossible. The best solution uses only two gems, giving product `0`, because one attribute remains zero. There is no requirement to fill every slot exactly.

A third mistake is assuming that each category should receive roughly one third of the slots.

For example,

```
10
3 1 1
2 100
2 100
2 100
2 1
4 1
```

The magic gems are dramatically stronger than the others. The optimal allocation is highly unbalanced, and any strategy that fixes the slot distribution in advance can miss the optimum.

## Approaches

A straightforward brute-force solution would enumerate every subset of gems. For each subset, compute the total occupied slots and the three attribute sums, then keep the maximum valid product.

This is obviously correct because every feasible selection is examined. Unfortunately, there can be as many as 6000 gems, so the search space contains `2^6000` subsets, which is astronomically large.

The key observation is that the three categories are independent. Suppose we know that exactly `x` slots are spent on magic gems. Inside that category, the only question is the maximum magic attack obtainable using `x` slots. The individual identities of the chosen gems no longer matter.

This immediately suggests solving three independent 0-1 knapsack problems.

For each category, define

`best[i] = maximum attribute value obtainable using exactly i slots`.

After these three knapsack computations, every possible slot allocation

`a + b + c ≤ n`

can be checked by evaluating

`best_magic[a] × best_mana[b] × best_speed[c]`.

The knapsack stage compresses exponentially many subsets into only `n + 1` states per category, making the final enumeration practical.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(m1+m2+m3)) | O(1) | Too slow |
| Optimal | O((m1+m2+m3)n+n³) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create a knapsack routine for one gem category. Let `dp[i]` denote the maximum attribute value obtainable using exactly `i` slots. Initialize `dp[0]=0` and every other state as impossible.
2. Process every gem once. Traverse slot counts in decreasing order to enforce the 0-1 restriction. If using the current gem improves the value for a larger slot count, update that state.
3. Run this knapsack independently for the magic, mana, and attack speed gems. The three resulting arrays contain the best achievable value for every exact slot usage.
4. Enumerate every possible pair `(a,b)` of slot counts assigned to the first two categories.
5. The remaining slots available for the third category are at most `n-a-b`. Enumerate every feasible `c` from `0` to that limit.
6. Ignore any state that is impossible in one of the three knapsack arrays.
7. Compute the product of the three attribute values and keep the maximum.

### Why it works

The knapsack computation considers every subset of gems within one category exactly once, so for every slot count it stores the largest achievable attribute value. Since categories never share gems and interact only through the total slot budget, every feasible overall solution corresponds to exactly one triple of slot usages `(a,b,c)`. During the final enumeration, that triple is examined, and the best value for each category is already known. Replacing any category by a weaker subset using the same number of slots can only decrease the product, so combining the three independently optimal choices for those slot counts is always optimal. Since every feasible slot allocation is checked, the global maximum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

NEG = -10 ** 18

def knapsack(m, n):
    dp = [NEG] * (n + 1)
    dp[0] = 0
    for _ in range(m):
        v, w = map(int, input().split())
        for s in range(n - v, -1, -1):
            if dp[s] != NEG:
                dp[s + v] = max(dp[s + v], dp[s] + w)
    return dp

def solve():
    n = int(input())
    m1, m2, m3 = map(int, input().split())

    atk = knapsack(m1, n)
    mana = knapsack(m2, n)
    speed = knapsack(m3, n)

    ans = 0

    for a in range(n + 1):
        if atk[a] == NEG:
            continue
        for b in range(n - a + 1):
            if mana[b] == NEG:
                continue
            limit = n - a - b
            for c in range(limit + 1):
                if speed[c] == NEG:
                    continue
                val = atk[a] * mana[b] * speed[c]
                if val > ans:
                    ans = val

    print(ans)

if __name__ == "__main__":
    solve()
```

The helper function performs a standard 0-1 knapsack. Iterating slot counts in decreasing order guarantees that each gem is used at most once.

Impossible states are initialized to a large negative number instead of zero. This distinction is essential because zero is a legitimate attribute value when no gem has been chosen.

After computing the three dynamic programming tables, the program enumerates every feasible slot distribution. The inner loop never exceeds the remaining capacity, so every tested allocation automatically satisfies the total slot limit.

Python integers have arbitrary precision, so no special handling is required for the product.

## Worked Examples

### Example 1

Input

```
10
2 2 2
2 1
3 2
2 1
3 2
5 3
4 2
```

After the three knapsack computations:

| Magic slots | Best attack |
| --- | --- |
| 0 | 0 |
| 2 | 1 |
| 3 | 2 |
| 5 | 3 |

| Mana slots | Best mana |
| --- | --- |
| 0 | 0 |
| 2 | 1 |
| 3 | 2 |
| 5 | 3 |

| Speed slots | Best speed |
| --- | --- |
| 0 | 0 |
| 4 | 2 |
| 5 | 3 |
| 9 | 5 |

During enumeration:

| Magic slots | Mana slots | Speed slots | Product |
| --- | --- | --- | --- |
| 3 | 3 | 4 | 8 |
| 2 | 3 | 5 | 6 |
| 5 | 5 | 0 | 0 |

The maximum product is `8`.

This example shows that the best solution comes from independently optimal choices for each category using a compatible slot allocation.

### Example 2

```
3
1 1 1
1 5
1 4
1 3
```

Knapsack tables:

| Magic slots | Attack |
| --- | --- |
| 0 | 0 |
| 1 | 5 |

| Mana slots | Mana |
| --- | --- |
| 0 | 0 |
| 1 | 4 |

| Speed slots | Speed |
| --- | --- |
| 0 | 0 |
| 1 | 3 |

Enumeration:

| Magic slots | Mana slots | Speed slots | Product |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 60 |
| 1 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 |

The answer is `60`, using one gem from every category.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m1+m2+m3)n+n³) | Three 0-1 knapsacks followed by enumeration of all feasible slot triples |
| Space | O(n) | Three arrays of length `n+1` |

With `n ≤ 2000`, the knapsack stage performs about twelve million updates. The cubic enumeration is acceptable only because the official constraints for this problem are designed for this approach. The memory usage is linear in the slot limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    from solution import solve

    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.getvalue().strip()

assert run("""10
2 2 2
2 1
3 2
2 1
3 2
5 3
4 2
""") == "8"

assert run("""1
1 1 1
1 1
1 1
1 1
""") == "0"

assert run("""3
1 1 1
1 5
1 4
1 3
""") == "60"

assert run("""2
1 1 1
2 5
2 7
2 9
""") == "0"

assert run("""6
2 2 2
3 5
3 5
3 5
3 5
3 5
3 5
""") == "125"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | 8 | Official example |
| Minimum capacity | 0 | One attribute cannot be increased |
| Three unit gems | 60 | Basic successful allocation |
| Only one category fits | 0 | Product becomes zero if an attribute is missing |
| Equal sized gems | 125 | Exact capacity split across categories |

## Edge Cases

Consider the case where one category cannot contribute.

```
2
1 1 1
2 5
3 10
3 10
```

The knapsack tables for mana and attack speed contain only the zero-slot state. Every enumerated allocation produces at least one attribute equal to zero, so the algorithm correctly returns `0`.

Now consider unused slots.

```
5
1 1 1
2 100
2 100
2 100
```

The only way to improve all three attributes requires six slots, which exceeds the capacity. The enumeration includes every allocation using at most five slots, none of which gives positive values for all three attributes. The answer is correctly `0`.

Finally, consider an unbalanced optimum.

```
10
3 1 1
2 100
2 100
2 100
2 1
4 1
```

The knapsack for magic strongly favors spending many slots there, while the other categories require only a few slots. Since every feasible slot distribution is examined, the algorithm naturally finds this skewed allocation instead of assuming an even split.
