---
title: "CF 102180A - \u041a\u0430\u0442\u044f \u0438 \u0441\u0431\u043e\u0440\u044b"
description: "Katya has two kinds of clothing: T-shirts and jeans. She packs n T-shirts and m pairs of jeans, while one additional T-shirt and one additional pair of jeans are already worn when she travels."
date: "2026-08-19T06:55:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "A"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 65
verified: true
draft: false
---

[CF 102180A - \u041a\u0430\u0442\u044f \u0438 \u0441\u0431\u043e\u0440\u044b](https://codeforces.com/problemset/problem/102180/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

Katya has two kinds of clothing: T-shirts and jeans. She packs `n` T-shirts and `m` pairs of jeans, while one additional T-shirt and one additional pair of jeans are already worn when she travels. Thus, during the training camp she has `n + 1` different T-shirts and `m + 1` different pairs of jeans available.

Each day she must choose one T-shirt and one pair of jeans. The same complete outfit cannot appear on two different days. Reusing a T-shirt with different jeans is allowed, and reusing jeans with a different T-shirt is also allowed.

The input contains `k`, the number of camp days, followed by `n` and `m`, the numbers of T-shirts and jeans packed into the suitcase. We need to print `Yes` if it is possible to choose a different complete outfit for every day, and `No` otherwise.

The key constraint is that `k` can be as large as `10^9`, while `n` and `m` are at most `1000`. This immediately suggests that simulating the days is undesirable. Even an algorithm that performs only constant work per day could require up to one billion iterations. On the other hand, the number of clothing types is small enough that the total number of distinct combinations can be computed directly.

There are several boundary cases that can fool a solution that counts only the clothes packed in the suitcase. For example, `1 0 0` must produce `Yes`, because the one outfit Katya is already wearing is available for the only camp day. A solution using only `n * m` would incorrectly obtain zero possible outfits.

The input `2 0 0` must produce `No`. Katya has only one T-shirt and one pair of jeans in total, so there is only one possible complete outfit. The second day would necessarily repeat it.

Another useful boundary case is `2 1 0`. There are two T-shirts in total and one pair of jeans, giving exactly two different outfits, so the answer is `Yes`. The distinction between `n` and `n + 1`, and between `m` and `m + 1`, is essential.

## Approaches

A direct brute-force solution could explicitly generate outfits for each of the `k` days and keep track of which pairs have already been used. This is correct because every generated pair can be checked against the previous choices, and the process fails exactly when there is no unused pair left. However, in the worst case it requires processing up to `10^9` days. Even with a hash set giving average constant-time insertion and lookup, that is far beyond what can fit into a one-second contest limit. A version that compares every new outfit with all previous outfits is even worse, reaching `O(k^2)` comparisons.

The structure of the problem lets us avoid constructing any outfit at all. Once Katya has `n + 1` T-shirts and `m + 1` jeans, every T-shirt can be paired with every pair of jeans. The multiplication principle gives exactly

`(n + 1) * (m + 1)`

distinct complete outfits.

The requirement is simply to have at least `k` different outfits for the `k` days. If the number of available combinations is at least `k`, we can select any `k` distinct pairs. If it is smaller, no schedule can work because there are not enough distinct outfits in the first place.

The brute-force approach works because it explicitly explores the available combinations, but fails because the number of days can be enormous. The observation that only the total number of possible pairs matters reduces the entire problem to one multiplication and one comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) with a set, or O(k²) with direct comparisons | O(k) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `k`, `n`, and `m`. The two clothing categories include the items already being worn, so the available counts are `n + 1` T-shirts and `m + 1` jeans.
2. Compute `(n + 1) * (m + 1)`. This is the number of distinct complete outfits, because each T-shirt can be combined independently with each pair of jeans.
3. Compare this number with `k`. If it is at least `k`, print `Yes`, because we can choose `k` different combinations. Otherwise, print `No`, because some outfit would have to be repeated.

The reasoning behind the multiplication is the central invariant of the solution: every pair consisting of a particular T-shirt and a particular pair of jeans represents exactly one complete outfit, and every possible complete outfit is represented by exactly one such pair.

### Why it works

There are `n + 1` possible T-shirts and `m + 1` possible jeans. For each fixed T-shirt, there are exactly `m + 1` choices of jeans, so there are `(n + 1) * (m + 1)` distinct complete outfits. A valid schedule needs `k` distinct outfits, and such a schedule exists exactly when the number of available outfits is at least `k`. The algorithm checks precisely this condition, so it returns `Yes` exactly for the feasible cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

k, n, m = map(int, input().split())

outfits = (n + 1) * (m + 1)

print("Yes" if outfits >= k else "No")
```

The input consists of a single line, so one call to `input()` is sufficient. We add one to both `n` and `m` because the T-shirt and jeans Katya wears while traveling are also available during the camp.

The multiplication is performed before the comparison. Python integers have arbitrary precision, although the actual product here is at most `1001 * 1001`, so integer overflow is not a concern even in languages with fixed-width integer types.

The comparison uses `>=`, not `>`. If there are exactly as many distinct outfits as camp days, every day can receive a unique outfit, so the answer must be `Yes`.

## Worked Examples

For the first sample, the input is `1 0 0`. There is one camp day, zero packed T-shirts, and zero packed jeans.

| `k` | `n` | `m` | Total T-shirts | Total jeans | Distinct outfits | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 1 | 1 | `1 >= 1`, Yes |

The single outfit consists of the T-shirt and jeans Katya already has. Since there is only one day, no outfit needs to be repeated.

For the second sample, the input is `2 0 0`.

| `k` | `n` | `m` | Total T-shirts | Total jeans | Distinct outfits | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 0 | 0 | 1 | 1 | 1 | `1 < 2`, No |

There is only one possible complete outfit, but two days require two different outfits. The second day would necessarily repeat the first day's combination.

For the third sample, `5 1 2`, Katya has two T-shirts and three pairs of jeans in total.

| `k` | `n` | `m` | Total T-shirts | Total jeans | Distinct outfits | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 1 | 2 | 2 | 3 | 6 | `6 >= 5`, Yes |

There are six possible combinations, so five distinct outfits can be selected. One combination can remain unused.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs one multiplication and one comparison. |
| Space | O(1) | Only the three input values and one product are stored. |

The largest possible value of `k` is `10^9`, but the algorithm never iterates over the days. The only relevant calculation uses `n` and `m`, both at most `1000`, so the solution is comfortably within the time and memory limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    k, n, m = map(int, input().split())
    return "Yes" if (n + 1) * (m + 1) >= k else "No"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("1 0 0\n") == "Yes", "sample 1"
assert run("2 0 0\n") == "No", "sample 2"
assert run("5 1 2\n") == "Yes", "sample 3"

# Minimum-size input
assert run("1 0 0\n") == "Yes", "one day, no packed clothes"

# Exact boundary: exactly enough combinations
assert run("4 1 1\n") == "Yes", "exactly four outfits are available"

# Just beyond the boundary
assert run("5 1 1\n") == "No", "only four outfits are available"

# Maximum values
assert run("1000000000 1000 1000\n") == "No", "maximum k exceeds all possible outfits"

# Maximum possible number of outfits
assert run("1002001 1000 1000\n") == "Yes", "exact maximum number of outfits"

# One clothing category has no packed items
assert run("3 2 0\n") == "Yes", "three shirts and one pair of jeans give three outfits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 0` | `Yes` | Minimum input and the contribution of the outfit already being worn |
| `4 1 1` | `Yes` | Exact equality at the feasibility boundary |
| `5 1 1` | `No` | One day beyond the boundary, catching `>` versus `>=` mistakes |
| `1000000000 1000 1000` | `No` | Very large `k` without simulating days |
| `1002001 1000 1000` | `Yes` | Maximum possible number of combinations |
| `3 2 0` | `Yes` | Zero packed jeans while the worn jeans remain available |

## Edge Cases

The first non-obvious case is `1 0 0`. The calculation gives `(0 + 1) * (0 + 1) = 1`, which is enough for one day, so the algorithm prints `Yes`. A solution that counts only packed clothes would incorrectly conclude that there are no outfits.

The second case is `2 0 0`. The calculation gives only one available outfit, while two distinct outfits are required. Since `1 < 2`, the algorithm prints `No`. There is no way to change either part of the outfit.

The equality boundary is represented by `4 1 1`. There are two T-shirts and two pairs of jeans, giving exactly four combinations. The comparison is `4 >= 4`, so the answer is `Yes`. This catches implementations that accidentally require strictly more outfits than days.

The immediately impossible case `5 1 1` gives the same four combinations but requires five days. The comparison becomes `4 >= 5`, which is false, so the algorithm prints `No`. This is the natural off-by-one companion to the previous test.

Finally, consider `1002001 1000 1000`. There are `1001 * 1001 = 1002001` possible outfits, exactly matching the number of days. The algorithm accepts the case in constant time, showing why there is no need to construct or store the individual clothing combinations.
