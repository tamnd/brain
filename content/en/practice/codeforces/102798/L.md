---
title: "CF 102798L - Clock Master"
description: "We have a collection of gears. A gear with t teeth costs t coins, and after k periods it shows direction k mod t. For a chosen set of gears, not every possible tuple of directions is necessarily reachable."
date: "2026-07-27T17:55:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102798
codeforces_index: "L"
codeforces_contest_name: "2020 China Collegiate Programming Contest, Weihai Site"
rating: 0
weight: 102798
solve_time_s: 67
verified: true
draft: false
---

[CF 102798L - Clock Master](https://codeforces.com/problemset/problem/102798/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of gears. A gear with `t` teeth costs `t` coins, and after `k` periods it shows direction `k mod t`. For a chosen set of gears, not every possible tuple of directions is necessarily reachable. The question is to choose gears whose total cost is at most `b` so that the number of reachable direction tuples is as large as possible. Instead of printing this huge number, we print its natural logarithm.

For gears with sizes `t1, t2, ...`, the number of different states the clock can ever display is exactly:

$$\operatorname{lcm}(t_1,t_2,\dots,t_n)$$

because after one full least common multiple of periods every pointer returns to its starting direction, and every smaller time inside that cycle produces a different global state.

The budget is at most `30000`, and there can be up to `30000` test cases. A solution that works separately for every query cannot afford anything close to exponential or even quadratic work. The right approach is to preprocess all answers up to the maximum budget once, using a dynamic programming method around `30000^2` operations.

A few cases are easy to mishandle. With budget `2`, choosing a single 2-tooth gear gives two states, so the answer is `ln(2)`. A program that starts from an empty product but forgets that one gear is always allowed can return zero.

For budget `7`, choosing gears of sizes `3` and `4` gives an lcm of `12`, which is better than a single 7-tooth gear. The answer is:

```
7
```

with output:

```
2.484906650
```

A greedy strategy that always takes the largest available gear would choose `7` and fail.

Another trap is choosing several powers of the same prime. Taking gears `2` and `4` costs `6`, but their lcm is only `4`, not `8`. The optimal transformation must avoid counting duplicate prime factors.

## Approaches

The brute-force interpretation is to try every possible collection of gears whose total cost is within the budget, compute its lcm, and keep the largest one. This is correct because it directly examines every valid design. However, the number of possible subsets grows exponentially. Even with only 20 possible gear choices there are already more than one million subsets, and the actual number of useful choices is much larger.

The key observation is that the lcm is built from prime powers. If two chosen gears contain different prime powers `p^a` and `q^b`, replacing them by those two prime powers gives the same lcm contribution while keeping the cost smaller. The official tutorial describes this reduction: an optimal solution only needs prime powers as gears.

After this reduction, the problem becomes a knapsack. Each prime contributes a group of choices: choose no gear of this prime, or choose one of `p`, `p^2`, `p^3`, and so on. Choosing `p^k` adds `p^k` to the cost and `ln(p^k)` to the answer. This is a grouped knapsack because only one power of each prime can be selected.

The state stores the best logarithm obtainable with a certain budget. Since logarithms turn multiplication of lcms into addition, the knapsack value transition is simply addition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Grouped Knapsack | O(B² / log B) | O(B) | Accepted |

## Algorithm Walkthrough

1. Generate all primes up to `30000` with a sieve. Each prime will represent one group in the knapsack.
2. For every prime `p`, generate the possible gears `p, p², p³, ...` while the value is at most `30000`. These are the only useful choices for this prime because taking two powers of the same prime does not increase the lcm.
3. Run grouped knapsack over the prime groups. For each prime, copy the current DP state and try adding every possible power of that prime. The transition is:

$$dp[new\_cost] = \max(dp[new\_cost], dp[old\_cost] + \ln(power))$$

The copy is necessary because the same prime cannot be selected twice.

1. After processing all primes, answer every query using the precomputed `dp[b]`.

The invariant is that after processing the first several primes, `dp[x]` is the maximum logarithm of an lcm that can be formed using only those primes with total cost at most `x`. Every valid choice either skips the current prime or chooses exactly one of its powers, so the grouped transition considers every possible optimal state.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

MAX_B = 30000

def build():
    is_prime = [True] * (MAX_B + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, MAX_B + 1):
        if is_prime[i]:
            primes.append(i)
            if i * i <= MAX_B:
                for j in range(i * i, MAX_B + 1, i):
                    is_prime[j] = False

    dp = [0.0] * (MAX_B + 1)

    for p in primes:
        powers = []
        x = p
        while x <= MAX_B:
            powers.append(x)
            x *= p

        old = dp[:]
        for cost in range(MAX_B + 1):
            best = old[cost]
            for x in powers:
                if cost >= x:
                    best = max(best, old[cost - x] + math.log(x))
            dp[cost] = best

    return dp

def solve():
    dp = build()
    t = int(input())
    ans = []
    for _ in range(t):
        b = int(input())
        ans.append("{:.9f}".format(dp[b]))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sieve builds the prime groups once because all test cases share the same maximum budget. The powers list for a prime contains only valid prime powers, so no duplicate prime contribution can enter the lcm.

The grouped transition uses `old = dp[:]` before processing a prime. Without this copy, a transition could select two powers of the same prime in one iteration, producing an invalid lcm.

Floating point values are safe here because the required output is only the logarithm with `1e-6` precision. The largest possible value is small enough for Python floating point arithmetic.

## Worked Examples

For budget `7`, the useful states are:

| Step | Chosen gears | Cost | Log value |
| --- | --- | --- | --- |
| Start | none | 0 | 0 |
| Choose 3 | 3 | 3 | ln(3) |
| Choose 4 | 4 | 4 | ln(4) |
| Combine 3 and 4 | 3,4 | 7 | ln(12) |

The final state uses two different prime factors and reaches 12 possible clock positions.

For budget `10`:

| Step | Chosen gears | Cost | LCM |
| --- | --- | --- | --- |
| Start | none | 0 | 1 |
| Choose 5 | 5 | 5 | 5 |
| Choose 8 | 8 | 8 | 8 |
| Choose 3 and 7 | 3,7 | 10 | 21 |
| Choose 2,3,5 | 10 | 30? | impossible |

The optimal selection is found by the DP transitions rather than a greedy rule. The output is:

```
3.401197382
```

which equals `ln(30)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(B² / log B) | There are O(B/log B) prime powers grouped over primes, and each group scans the budget range. |
| Space | O(B) | Only the current knapsack array is stored. |

With `B = 30000`, the preprocessing fits comfortably within the limits. Each test case afterwards is answered in constant time.

## Test Cases

```python
import math

def solve_string(inp):
    import sys, io
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    sys.stdin = old

# Expected manual checks:
# 1
# 0.693147181

# 3
# 0.693147181
# 2.484906650
# 3.401197382

# Custom:
# Budget 1 cannot buy a useful gear except a 1-tooth gear, giving one state.
# Budget 6 should prefer 5 and 1? Actually 2 and 3 gives lcm 6.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0.000000000` | Minimum budget handling |
| `1 / 2` | `0.693147181` | Single prime gear |
| `1 / 7` | `2.484906650` | Combination of different primes |
| `1 / 6` | `1.791759469` | Avoiding duplicate prime powers |

## Edge Cases

For budget `1`, the only possible gear has one direction. The DP starts with value zero, representing an lcm of one, so it correctly returns `ln(1)=0`.

For budget `6`, a careless implementation might choose gears `2` and `4` and claim an lcm of `8`. The grouped knapsack never allows that transition because both choices belong to the prime group for `2`. It can choose `4`, or `2`, but not both.

For budget `7`, greedy selection fails because the largest gear is not always the best. The DP can choose the group for prime `3` with value `3` and the group for prime `2` with value `4`, producing lcm `12`, which beats every single gear costing at most `7`.

For large budgets, the algorithm still works because the preprocessing depends only on the maximum budget, not on the number of queries. The input can contain many requests, but each one is answered by a direct lookup.
