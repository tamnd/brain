---
title: "CF 1418E - Expected Damage"
description: "We have a fixed multiset of monster strengths. For each query, a shield starts with durability a and defence value b. Monsters are fought in a uniformly random order. A monster whose strength is at least b consumes one durability point but deals no damage."
date: "2026-06-11T06:51:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1418
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 95 (Rated for Div. 2)"
rating: 2400
weight: 1418
solve_time_s: 84
verified: true
draft: false
---

[CF 1418E - Expected Damage](https://codeforces.com/problemset/problem/1418/E)

**Rating:** 2400  
**Tags:** binary search, combinatorics, probabilities  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed multiset of monster strengths. For each query, a shield starts with durability `a` and defence value `b`. Monsters are fought in a uniformly random order.

A monster whose strength is at least `b` consumes one durability point but deals no damage. A weaker monster does nothing while durability remains positive. Once durability reaches zero, every remaining monster deals damage equal to its strength.

The question asks for the expected total damage over all possible orders.

The limits are large. Both the number of monsters and the number of queries reach `2·10^5`, so anything quadratic is hopeless. Even processing every query in linear time would require about `4·10^10` operations. We need something around `O((n+m) log n)`.

The first subtle case appears when there are not enough strong monsters to exhaust the shield.

```
3 1
1 2 10
5 100
```

No monster has strength at least `100`, so durability never decreases. Damage is always zero, and the answer is `0`. A careless formula that divides by the number of strong monsters would crash.

Another tricky situation happens when the number of strong monsters equals the durability.

```
4 1
1 2 5 8
2 5
```

The strong monsters are `5` and `8`. They consume exactly two durability points, leaving no durability afterward, but there are no strong monsters left to attack. Only the weaker monsters remain, so the expected damage is `1+2=3`. Treating every monster equally after the shield breaks would overcount.

Duplicates also matter.

```
3 1
7 7 7
1 7
```

Exactly one monster consumes durability and the other two deal damage. The expected damage is always `14`, not some average over distinct values. Sorting and using multiplicities correctly avoids this mistake.

## Approaches

A brute force view is straightforward. For one query, enumerate all `n!` orders, simulate the fight, and average the resulting damages. This is mathematically correct but absurdly expensive.

Even replacing permutation enumeration with probability calculations and processing each query independently in `O(n)` is too slow. With `2·10^5` queries, this becomes roughly `4·10^10` operations.

The key observation is that only monsters with strength at least `b` affect durability. Suppose there are `k` such monsters. If `k<a`, the shield never breaks and the answer is zero.

Assume `k≥a`. Consider one strong monster. Among the `k` strong monsters, all relative orders are equally likely. The shield survives the first `a` strong monsters and breaks immediately after that. A particular strong monster deals damage exactly when it appears after position `a` among those `k` monsters.

The probability of that event equals

$$\frac{k-a}{k}.$$

Weak monsters never consume durability. Once the shield has been exhausted by `a` strong monsters, every weak monster that appears afterward deals damage. Since weak monsters are randomly interleaved with the strong ones, their probability of appearing after the breaking point is

$$\frac{k-a+1}{k+1}.$$

These probabilities depend only on `k`, not on individual strengths. After sorting the strengths and building prefix sums, we can obtain the sum of strong strengths and weak strengths in logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·n) | O(n) | Too slow |
| Optimal | O((n+m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the monster strengths.
2. Build prefix sums so that the sum of any suffix or prefix can be obtained in constant time.
3. For a query `(a,b)`, binary search for the first position whose value is at least `b`.
4. Let `k` be the number of monsters with strength at least `b`.

These are exactly the monsters that consume durability.
5. If `k<a`, output `0`.

The shield never reaches durability zero.
6. Compute the sum of strong monsters, denoted `Sstrong`, and the sum of weak monsters, denoted `Sweak`.
7. Every strong monster contributes with probability `(k-a)/k`.

Their expected contribution equals

$$S_{strong}\cdot\frac{k-a}{k}.$$

1. Every weak monster contributes with probability `(k-a+1)/(k+1)`.

Their expected contribution equals

$$S_{weak}\cdot\frac{k-a+1}{k+1}.$$

1. Add the two contributions and take everything modulo `998244353`.

### Why it works

Among the strong monsters, only their relative order matters for durability consumption. Exactly the first `a` strong monsters are blocked, while the remaining `k-a` strong monsters attack after the shield has broken. Symmetry gives each strong monster probability `(k-a)/k`.

The breaking point occurs immediately after the `a`-th strong monster. A weak monster is equally likely to occupy any of the `k+1` gaps around the strong monsters. There are `k-a+1` gaps after the breaking point, giving probability `(k-a+1)/(k+1)`. Summing these independent expectations over all monsters yields the correct expected damage.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

MOD = 998244353

n, m = map(int, input().split())
d = list(map(int, input().split()))

d.sort()

pref = [0]
for x in d:
    pref.append(pref[-1] + x)

inv = [1] * (n + 2)
for i in range(2, n + 2):
    inv[i] = pow(i, MOD - 2, MOD)

total_sum = pref[n]

ans = []

for _ in range(m):
    a, b = map(int, input().split())

    pos = bisect_left(d, b)
    k = n - pos

    if k < a:
        ans.append("0")
        continue

    strong_sum = total_sum - pref[pos]
    weak_sum = pref[pos]

    p_strong = (k - a) * inv[k] % MOD
    p_weak = (k - a + 1) * inv[k + 1] % MOD

    res = (
        strong_sum % MOD * p_strong
        + weak_sum % MOD * p_weak
    ) % MOD

    ans.append(str(res))

print("\n".join(ans))
```

The sorted array allows binary search to identify the strong monsters for each query. Prefix sums give the total strength of both groups without scanning the array.

The condition `k<a` must be handled before computing probabilities. Otherwise we would incorrectly assign negative numerators.

The weak probability uses `k+1` in the denominator, not `k`. This is the most common source of mistakes. A weak monster is inserted among the gaps around the strong monsters, and there are one more gaps than strong monsters.

All divisions are implemented with modular inverses because the modulus is prime.

## Worked Examples

Consider the sample.

```
3 2
1 3 1
2 1
1 2
```

Sorted strengths are `[1,1,3]`.

### Query `(2,1)`

| Quantity | Value |
| --- | --- |
| k | 3 |
| Strong sum | 5 |
| Weak sum | 0 |
| Strong probability | 1/3 |
| Weak probability | 2/4 |
| Expected damage | 5/3 |

Modulo `998244353`, `5/3` becomes `665496237`.

This example shows that even strong monsters can deal damage when there are more of them than durability.

### Query `(1,2)`

| Quantity | Value |
| --- | --- |
| k | 1 |
| Strong sum | 3 |
| Weak sum | 2 |
| Strong probability | 0 |
| Weak probability | 1/2 |
| Expected damage | 1 |

The single strong monster consumes the only durability point. Afterwards both weak monsters have probability `1/2` of appearing later.

Consider another example.

```
4 1
1 2 5 8
2 5
```

| Quantity | Value |
| --- | --- |
| k | 2 |
| Strong sum | 13 |
| Weak sum | 3 |
| Strong probability | 0 |
| Weak probability | 1/3 |
| Expected damage | 1 |

This trace highlights the fact that strong monsters contribute nothing when their count exactly equals durability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Sorting plus one binary search per query |
| Space | O(n) | Sorted array and prefix sums |

The sorting cost is paid once. Each query performs only a binary search and a few arithmetic operations, which easily fits within the limits for `2·10^5` queries.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MOD = 998244353

    n, m = map(int, input().split())
    d = list(map(int, input().split()))
    d.sort()

    pref = [0]
    for x in d:
        pref.append(pref[-1] + x)

    total_sum = pref[n]
    inv = [1] * (n + 2)
    for i in range(2, n + 2):
        inv[i] = pow(i, MOD - 2, MOD)

    out = []

    for _ in range(m):
        a, b = map(int, input().split())
        pos = bisect_left(d, b)
        k = n - pos

        if k < a:
            out.append("0")
            continue

        strong_sum = total_sum - pref[pos]
        weak_sum = pref[pos]

        p1 = (k - a) * inv[k] % MOD
        p2 = (k - a + 1) * inv[k + 1] % MOD

        val = (
            strong_sum % MOD * p1
            + weak_sum % MOD * p2
        ) % MOD

        out.append(str(val))

    return "\n".join(out)

# provided sample
assert run(
"""3 2
1 3 1
2 1
1 2
"""
) == """665496237
1"""

# minimum size
assert run(
"""1 1
5
1 10
"""
) == "0"

# all equal
assert run(
"""3 1
7 7 7
1 7
"""
) == "14"

# no shield break
assert run(
"""4 1
1 2 3 4
4 5
"""
) == "0"

# boundary k = a
assert run(
"""4 1
1 2 5 8
2 5
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single monster, large defence | 0 | Shield never breaks |
| All strengths equal | 14 | Multiplicity handling |
| No monster reaches defence | 0 | `k<a` branch |
| `k=a` | 1 | Boundary between surviving and breaking |

## Edge Cases

When no monster is strong enough,

```
3 1
1 2 10
2 100
```

binary search gives `k=0`. Since `0<2`, the algorithm immediately outputs `0`. No probability computation is performed.

When the number of strong monsters equals durability,

```
4 1
1 2 5 8
2 5
```

we obtain `k=2`. The strong probability becomes zero because `k-a=0`. Weak monsters contribute with probability `1/3`, producing expected damage

$$(1+2)\cdot\frac13=1.$$

When all values are identical,

```
3 1
7 7 7
1 7
```

all monsters belong to the strong group. Here `k=3`, strong sum is `21`, and each monster contributes with probability `2/3`. The expected damage equals `14`. Sorting preserves all copies, so duplicate strengths are handled naturally.
