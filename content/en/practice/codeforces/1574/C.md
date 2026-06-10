---
title: "CF 1574C - Slay the Dragon"
description: "We have a squad of heroes, each with a fixed strength. For every dragon, we must choose exactly one hero to fight it, while all remaining heroes stay behind to defend the castle. A dragon has two requirements."
date: "2026-06-10T11:07:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1574
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 114 (Rated for Div. 2)"
rating: 1300
weight: 1574
solve_time_s: 353
verified: false
draft: false
---

[CF 1574C - Slay the Dragon](https://codeforces.com/problemset/problem/1574/C)

**Rating:** 1300  
**Tags:** binary search, greedy, sortings, ternary search  
**Solve time:** 5m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We have a squad of heroes, each with a fixed strength. For every dragon, we must choose exactly one hero to fight it, while all remaining heroes stay behind to defend the castle.

A dragon has two requirements. The chosen attacker must have strength at least `x`, and the total strength of all defenders must be at least `y`.

We are allowed to spend coins to increase hero strengths. Every point of strength costs one coin, and upgrades are temporary because each dragon is handled independently.

For each dragon, we must determine the minimum number of coins needed so that some hero can satisfy the attack requirement while the remaining heroes satisfy the defense requirement.

The constraints immediately rule out any solution that examines every hero for every dragon. Both `n` and `m` can reach `2 · 10^5`, so an `O(nm)` algorithm would perform roughly `4 · 10^10` operations, which is far beyond what fits into a two second limit.

The hero strengths can be as large as `10^12`, and the defense requirement can be as large as `10^18`. This means we must use 64-bit integer arithmetic. Python handles this automatically.

Several edge cases are easy to mishandle.

Consider:

```
Heroes: [10]
Dragon: x = 5, y = 100
```

The attacker already satisfies the attack requirement, but once that hero leaves, the defenders have strength `0`. The answer is `100`, not `0`. Focusing only on the attacking hero gives the wrong result.

Consider:

```
Heroes: [5, 100]
Dragon: x = 50, y = 5
```

Choosing the strongest hero seems attractive because no attack upgrade is needed. But then defenders have strength `5`, which is exactly enough. Cost is `0`.

If we instead choose hero `5`, we need `45` coins to reach attack power `50`. The choice of attacker matters.

Another subtle case:

```
Heroes: [4, 8]
Dragon: x = 6, y = 100
```

Choosing hero `8` costs:

```
attack = 0
defense = 100 - 4 = 96
total = 96
```

Choosing hero `4` costs:

```
attack = 6 - 4 = 2
defense = 100 - 8 = 92
total = 94
```

The hero closest to `x` is not always optimal. Sometimes paying more for the attacker improves the defenders enough to reduce the total cost.

These examples suggest that we must carefully evaluate which hero becomes the attacker.

## Approaches

The brute force idea is straightforward. For each dragon, try every hero as the attacker.

Suppose hero strength is `a[i]` and the total strength of all heroes is `S`.

If this hero attacks, the defenders contribute `S - a[i]`.

The attack requirement costs:

```
max(0, x - a[i])
```

The defense requirement costs:

```
max(0, y - (S - a[i]))
```

The total cost is the sum of these two values.

Checking every hero gives the correct answer because it explicitly evaluates all possible attackers and takes the minimum. Unfortunately, each query needs `O(n)` work. With `2 · 10^5` heroes and `2 · 10^5` dragons, this becomes roughly `4 · 10^10` evaluations.

The key observation is that the cost function changes in a very structured way.

Let a hero have strength `h`.

The attack contribution is:

```
max(0, x - h)
```

As `h` increases, this quantity decreases.

The defense contribution is:

```
max(0, y - (S - h))
```

which is equivalent to:

```
max(0, y - S + h)
```

As `h` increases, this quantity increases.

One part prefers larger heroes, the other prefers smaller heroes.

This means the optimum occurs near the point where the attack requirement changes from unsatisfied to satisfied, namely around strength `x`.

After sorting the heroes, we can binary search for the first hero whose strength is at least `x`.

Any hero much smaller than `x` requires extra attack coins. Any hero much larger than `x` weakens the defenders unnecessarily. The minimum can only occur among the heroes nearest to `x`.

Specifically, we only need to check:

1. The first hero with strength at least `x`.
2. The hero immediately before it.

Those are the only candidates that can beat all others.

Each query becomes one binary search and two evaluations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n log n + m log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read all hero strengths and compute their total strength `S`.
2. Sort the hero strengths.

Sorting allows binary search on hero strengths.
3. For each dragon `(x, y)`, find the first hero whose strength is at least `x`.

Use binary search (`bisect_left`).
4. If such a hero exists, evaluate using that hero as the attacker.

The attack requirement already holds, so the attack cost may be zero. The defense cost is:

```
max(0, y - (S - hero))
```
5. If there is a hero immediately before the binary search position, evaluate that hero as well.

This hero is the strongest hero below `x`. It may need attack upgrades:

```
max(0, x - hero)
```

plus any defense upgrades.
6. Take the minimum cost among the evaluated candidates.
7. Output the answer for the query.

### Why it works

Let the attacking hero have strength `h`.

The cost is

```
f(h) =
max(0, x - h)
+
max(0, y - (S - h))
```

The first term decreases as `h` increases. The second term increases as `h` increases.

For heroes below `x`, moving to a larger hero never increases the first term and can only increase the second term gradually. The best hero below `x` is the largest one below `x`.

For heroes at least `x`, the first term becomes zero. Among such heroes, choosing a larger hero only weakens the defenders and never helps. The best hero at least `x` is the smallest one at least `x`.

After sorting, these two heroes are exactly the predecessor and successor of `x` in the sorted array. Every other hero is dominated by one of these candidates, so checking only these two possibilities always finds the optimum.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()
total = sum(a)

m = int(input())

for _ in range(m):
    x, y = map(int, input().split())

    pos = bisect_left(a, x)
    ans = 10**30

    if pos < n:
        hero = a[pos]
        cost = max(0, y - (total - hero))
        ans = min(ans, cost)

    if pos > 0:
        hero = a[pos - 1]
        cost = max(0, x - hero) + max(0, y - (total - hero))
        ans = min(ans, cost)

    print(ans)
```

The first part sorts the heroes and computes their total strength. The total is reused for every query, allowing defender strength to be computed instantly as `total - hero`.

For each dragon, `bisect_left` finds the first hero whose strength is at least the required attack value. That hero is the smallest hero capable of fighting without attack upgrades.

The predecessor is also checked because it is the strongest hero below the threshold. Any weaker hero would need even more attack upgrades while providing no compensating advantage.

The initial answer is set to a very large number. Every valid candidate updates it.

A common mistake is forgetting that the defender strength excludes the attacking hero. The correct defender strength is `total - hero`, not `total`.

Another common mistake is checking only the binary search result and ignoring the predecessor. Several optimal solutions require choosing a hero slightly below `x` because the stronger defenders save more coins overall.

## Worked Examples

### Sample 1, Query `(7, 9)`

Heroes after sorting:

```
[2, 3, 3, 6]
```

Total strength:

```
S = 14
```

Binary search for `x = 7`.

| Candidate Hero | Attack Cost | Defender Strength | Defense Cost | Total |
| --- | --- | --- | --- | --- |
| 6 | 1 | 8 | 1 | 2 |

No hero is at least `7`.

Answer:

```
2
```

This example shows the case where only the predecessor candidate exists.

### Sample 1, Query `(4, 14)`

Sorted heroes:

```
[2, 3, 3, 6]
```

Total:

```
14
```

Binary search gives hero `6`.

| Candidate Hero | Attack Cost | Defender Strength | Defense Cost | Total |
| --- | --- | --- | --- | --- |
| 6 | 0 | 8 | 6 | 6 |
| 3 | 1 | 11 | 3 | 4 |

Minimum cost is:

```
4
```

The weaker hero is actually better because removing the strongest hero from the defenders is expensive.

This demonstrates why both neighboring candidates must be checked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | Sorting once, then one binary search per query |
| Space | O(1) extra | Aside from the hero array itself |

The sorting phase costs `O(n log n)`. Each dragon query performs a binary search and evaluates at most two candidates, so it costs `O(log n)`.

With `n, m ≤ 2 · 10^5`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    a.sort()
    total = sum(a)

    m = int(sys.stdin.readline())

    out = []

    for _ in range(m):
        x, y = map(int, sys.stdin.readline().split())

        pos = bisect_left(a, x)
        ans = 10**30

        if pos < n:
            hero = a[pos]
            ans = min(ans, max(0, y - (total - hero)))

        if pos > 0:
            hero = a[pos - 1]
            ans = min(
                ans,
                max(0, x - hero) +
                max(0, y - (total - hero))
            )

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""4
3 6 2 3
5
3 12
7 9
4 14
1 10
8 7
"""
) == """1
2
4
0
2
"""

# minimum size
assert run(
"""2
5 10
1
5 1
"""
) == """0
"""

# all equal heroes
assert run(
"""3
5 5 5
1
5 10
"""
) == """0
"""

# only predecessor exists
assert run(
"""2
4 6
1
10 1
"""
) == """4
"""

# predecessor better than successor
assert run(
"""2
4 8
1
6 100
"""
) == """94
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 5 10 / (5,1)` | `0` | Minimum-size valid configuration |
| `5 5 5 / (5,10)` | `0` | All heroes equal |
| `4 6 / (10,1)` | `4` | Binary search position at end of array |
| `4 8 / (6,100)` | `94` | Optimal answer comes from predecessor |

## Edge Cases

Consider:

```
2
5 100
1
50 5
```

The sorted array is `[5, 100]`, total strength is `105`.

Binary search finds hero `100`.

For hero `100`:

```
attack cost = 0
defense cost = max(0, 5 - 5) = 0
total = 0
```

For hero `5`:

```
attack cost = 45
defense cost = 0
total = 45
```

The algorithm returns `0`, correctly selecting the stronger hero.

Now consider:

```
2
4 8
1
6 100
```

Total strength is `12`.

For hero `8`:

```
0 + (100 - 4) = 96
```

For hero `4`:

```
(6 - 4) + (100 - 8) = 94
```

The algorithm checks both neighboring candidates and returns `94`. Any solution that only chooses the smallest hero at least `x` would incorrectly output `96`.

Finally, consider:

```
2
10 20
1
5 100
```

Both heroes already satisfy the attack requirement. Binary search points to hero `10`.

For hero `10`:

```
attack cost = 0
defense cost = 80
```

For hero `20`:

```
attack cost = 0
defense cost = 90
```

The algorithm chooses the smaller eligible hero because it leaves more strength defending the castle. This is exactly why the successor candidate is the smallest hero at least `x`, not an arbitrary eligible hero.
