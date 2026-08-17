---
title: "CF 102222H - Fight Against Monsters"
description: "Each monster has a health value HP and an attack value ATK. During every second, all monsters that are still alive attack the hero first, so the hero loses the sum of their attack values. The hero then chooses exactly one living monster and attacks it."
date: "2026-08-17T22:12:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "H"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 138
verified: true
draft: false
---

[CF 102222H - Fight Against Monsters](https://codeforces.com/problemset/problem/102222/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Each monster has a health value `HP` and an attack value `ATK`. During every second, all monsters that are still alive attack the hero first, so the hero loses the sum of their attack values. The hero then chooses exactly one living monster and attacks it.

The damage dealt to a particular monster depends only on how many times that monster has already been attacked. Its first received hit deals `1`, its second deals `2`, its third deals `3`, and so on. Consequently, if a monster needs `k` attacks to die, those attacks must deal

[
1+2+\cdots+k=\frac{k(k+1)}2
]

damage in total. The question is how to choose the order of attacks so that the total damage received by the hero is as small as possible.

The input contains up to `10^3` test cases, with at most `10^5` monsters in one test case and at most `10^6` monsters across all test cases. The health and attack values are at most `10^5`. These bounds rule out anything involving subsets or permutations of the monsters. Even an `O(n^2)` method would be too expensive when `n=10^5`, so the intended solution must reduce the problem to essentially sorting.

For each monster, the number of attacks it requires is very small despite the potentially large health. With `HP <= 10^5`, `447` attacks already deal `100128` damage, so every monster needs at most `447` attacks. The original constraints and output format are confirmed by the official problem page.

There are several edge cases that can make a straightforward implementation wrong.

For a single monster, there is no ordering decision at all. For example,

```
1
1
1 1
```

has answer `1`. A formula that accidentally counts the monster as alive for one extra second would produce `2`, which is wrong because the monster attacks once and then dies immediately after the hero's first attack.

A health value exactly equal to a triangular number also needs correct handling. For

```
1
1
3 2
```

the monster needs exactly two attacks because `1 + 2 = 3`, so the answer is `4`. Using a strict `>` instead of `>=` when finding the required number of attacks would incorrectly require a third attack.

Equal ordering ratios are another boundary case. If two monsters have `(k_1, ATK_1) = (1, 2)` and `(k_2, ATK_2) = (2, 4)`, then both have ratio `k / ATK = 1/2`. Either order has the same total cost. A comparator must treat this as a tie rather than imposing an inconsistent ordering.

Finally, the answer can exceed a 32-bit integer. For `100000` monsters with `HP=1` and `ATK=1`, the completion times are `1,2,...,100000`, giving

[
\frac{100000\cdot100001}{2}=5000050000.
]

A 32-bit integer would overflow. Python integers do not have this problem, but the corresponding C++ implementation needs `long long`.

## Approaches

The direct brute-force approach is to try every possible order in which the monsters are completely killed. For one fixed order, we can calculate the number of attacks needed by every monster and then simulate the accumulated time. This is correct because every possible ordering is considered, so the best one must appear among the candidates.

The problem is the number of candidates. With `n` monsters there are `n!` permutations, and evaluating one permutation takes `O(n)` time. The worst-case work is therefore `Theta(n * n!)`. Even `20! * 20` is about `4.87 * 10^19` basic order-processing steps, far beyond practical limits. For `n=10^5`, permutation enumeration is not remotely feasible.

The useful observation is that a monster's total required number of attacks is fixed before the battle begins. If a monster needs `k` attacks, the actual attacks can be thought of as a job of processing time `k`. Its attack value `ATK` is the cost paid for every second that this monster remains alive.

Suppose all monsters have total attack value `S`, and consider one monster that needs `k` attacks. If it is killed after `C` hero attacks have occurred, it contributes exactly `ATK * C` to the hero's total damage. Thus the whole problem becomes a scheduling problem: every monster is a job with processing time `k` and weight `ATK`, and we want to minimize the sum of weighted completion times.

The optimal order can be derived with a two-monster exchange argument. Consider monsters `A` and `B`, with required attack counts `k_A`, `k_B` and attack values `w_A`, `w_B`. Ignore everything before these two monsters and let the current time be `C`.

If `A` is killed first, their contribution is

[
w_A(C+k_A)+w_B(C+k_A+k_B).
]

If `B` is killed first, their contribution is

[
w_B(C+k_B)+w_A(C+k_B+k_A).
]

The common terms cancel. Putting `A` first is no worse exactly when

[
k_A w_B \le k_B w_A.
]

Equivalently,

[
\frac{k_A}{w_A}\le\frac{k_B}{w_B}.
]

So monsters should be sorted by increasing `required_attacks / ATK`. This is the same exchange argument used in the standard weighted-completion-time scheduling rule, and the same cross-product comparison appears in existing solutions to this problem.

The brute-force works because a complete ordering completely determines the completion time of every monster, but it fails because there are factorially many orderings. The exchange argument lets us eliminate all orderings containing an inversion, leaving one sorted order that is globally optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · n!)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. For every monster, calculate the minimum number `k` of hero attacks required to kill it. We need the smallest `k` satisfying

[
\frac{k(k+1)}2\ge HP.
]

Since `HP <= 10^5`, `k <= 447`, so these values can be found efficiently using a precomputed table of triangular numbers.
2. Treat each monster as a job with processing time `k` and weight `ATK`. The processing time means how many hero turns are required before the monster dies, while the weight means how much damage the hero receives from that monster during every second it stays alive.
3. Sort the monsters by increasing `k / ATK`. The comparison can be understood without division: monster `A` belongs before monster `B` when

[
k_A ATK_B \le k_B ATK_A.
]

This cross-product form is the exact mathematical comparison and avoids division-related ordering problems.
4. Traverse the sorted monsters. Maintain `time`, the total number of hero attacks used to kill all previously processed monsters. For the current monster, increase `time` by its required attack count `k`. Its death occurs at this new time, so it contributes

[
ATK \times time
]

damage to the answer.
5. Sum these weighted completion costs and print the result in the required `Case #x: answer` format.

The invariant is that after processing the first `i` monsters in sorted order, `time` is exactly the number of hero attacks needed to kill those monsters, and `answer` is the minimum possible weighted damage contribution among all schedules that complete those same monsters in that order. The exchange argument shows that whenever two adjacent monsters violate the ratio order, swapping them cannot increase the result. Repeatedly removing every inversion produces the sorted order, so no other schedule can have a smaller total cost.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

# The largest possible number of attacks is 447 because
# 447 * 448 // 2 = 100128 >= 100000.
MAX_HITS = 447

triangular = [0]
for k in range(1, MAX_HITS + 1):
    triangular.append(triangular[-1] + k)

def solve(inp=input):
    t = int(inp())
    out = []

    for case_id in range(1, t + 1):
        n = int(inp())
        monsters = []

        for _ in range(n):
            hp, atk = map(int, inp().split())

            # Smallest k such that k * (k + 1) / 2 >= hp.
            k = bisect_left(triangular, hp, 1)

            monsters.append((k, atk))

        # Under the given bounds, distinct rational ratios k / atk
        # are separated by at least 1 / 10^10, much more than the
        # floating-point precision around these values.
        monsters.sort(key=lambda x: x[0] / x[1])

        time = 0
        answer = 0

        for hits, atk in monsters:
            time += hits
            answer += time * atk

        out.append(f"Case #{case_id}: {answer}")

    return "\n".join(out)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The triangular-number array is built once. Since the largest health is `100000`, the required number of attacks is at most `447`. `bisect_left` finds the first triangular number that reaches the monster's health, giving exactly the required attack count.

Each monster is stored as `(hits, atk)`. The sorting key is the ratio `hits / atk`, in increasing order. The mathematical rule is based on exact cross multiplication, but the implementation can safely use floating-point ratios here because `hits <= 447` and `atk <= 100000`. Two distinct such fractions differ by at least `1 / 10^10`, while double precision has much finer absolute resolution over the interval from `0` to `447`.

The important boundary is the use of `bisect_left`. If the health is exactly triangular, such as `HP=3`, the first valid value must be `2`, not `3`. The lower-bound search gives exactly that.

During the final traversal, `time` is updated before adding the current monster's contribution. This matches the battle order: the monster attacks during every second up to and including the second in which the hero kills it. Consequently, a monster completed at time `C` contributes `ATK * C`.

The answer can be several billions or more, so the implementation deliberately keeps the calculation in Python's arbitrary-precision integers.

## Worked Examples

For Sample 1, the monsters are

```
HP  ATK
1   1
2   2
3   3
```

Their required attack counts are `1`, `2`, and `2`.

| Monster | HP | ATK | Required attacks | Ratio `hits / ATK` | Completion time | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 2 | `2/3` | 2 | 6 |
| 1 | 1 | 1 | 1 | `1` | 3 | 3 |
| 2 | 2 | 2 | 2 | `1` | 5 | 10 |

The sorted order is monster `3`, monster `1`, monster `2`. The total is `6 + 3 + 10 = 19`, matching the sample output. The trace shows why a monster with high attack value should generally be killed early, even if it takes more hero attacks.

For Sample 2, the monsters are

```
HP  ATK
3   1
2   2
1   3
```

The required attack counts are `2`, `2`, and `1`.

| Monster | HP | ATK | Required attacks | Ratio `hits / ATK` | Completion time | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 1 | 3 | 1 | `1/3` | 1 | 3 |
| 2 | 2 | 2 | 2 | `1` | 3 | 6 |
| 1 | 3 | 1 | 2 | `2` | 5 | 5 |

The optimal order is monster `3`, then monster `2`, then monster `1`. The total is `3 + 6 + 5 = 14`.

This example demonstrates the ratio rule clearly. Monster `3` has the largest attack value and needs only one attack, so leaving it alive even briefly is expensive. The sorted ratio puts it first automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Computing required attacks takes `O(n log 447)`, then sorting dominates with `O(n log n)` |
| Space | `O(n)` | The monster array stores one pair per monster |

Across all test cases there are at most `10^6` monsters, so the total sorting work is bounded by the corresponding sum of `n log n` terms. The algorithm performs no subset enumeration, simulation by individual seconds, or pairwise `O(n^2)` processing, which makes it suitable for the stated `10^5` per-test and `10^6` total bounds. The official statement gives a 10 second time limit and 256 MB memory limit.

## Test Cases

The following tests assume the `solve` function from the solution above is available.

```python
import sys
import io

def run(inp: str) -> str:
    return solve(io.StringIO(inp).readline) + "\n"

# Sample 1
assert run(
    """1
3
1 1
2 2
3 3
"""
) == "Case #1: 19\n", "sample 1"

# Sample 2
assert run(
    """1
3
3 1
2 2
1 3
"""
) == "Case #1: 14\n", "sample 2"

# Minimum-size case
assert run(
    """1
1
1 1
"""
) == "Case #1: 1\n", "single monster"

# Exact triangular number, k = 2
assert run(
    """1
1
3 2
"""
) == "Case #1: 4\n", "exact triangular HP"

# Different ratios, catches incorrect attack-value-only sorting
assert run(
    """1
2
1 2
2 3
"""
) == "Case #1: 11\n", "ratio ordering"

# All values equal
assert run(
    """1
4
3 2
3 2
3 2
3 2
"""
) == "Case #1: 40\n", "equal ratios"

# Boundary HP = 100000, requiring 447 attacks
assert run(
    """1
1
100000 1
"""
) == "Case #1: 447\n", "maximum HP"

# Maximum number of monsters
max_input = "1\n100000\n" + "1 1\n" * 100000
assert run(max_input) == "Case #1: 5000050000\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1 1` | `Case #1: 1` | Minimum input and immediate death |
| `1 / 1 / 3 2` | `Case #1: 4` | Exact triangular-number boundary |
| `1 / 2 / 1 2 / 2 3` | `Case #1: 11` | Correct `hits / ATK` ordering |
| Four copies of `3 2` | `Case #1: 40` | Equal ratios and arbitrary tie order |
| `1 / 1 / 100000 1` | `Case #1: 447` | Maximum health and attack-count boundary |
| `100000` copies of `1 1` | `Case #1: 5000050000` | Maximum `n` and large answer |

## Edge Cases

For the minimum-size case

```
1
1
1 1
```

the triangular-number search finds `k=1`. The sorted array contains one monster, so `time` becomes `1` and the answer becomes `1 * 1 = 1`. The monster attacks once, then dies, so there is no extra damage after its death.

For the exact triangular boundary

```
1
1
3 2
```

the triangular numbers begin `0, 1, 3, 6`. `bisect_left` finds index `2`, so the monster requires exactly two attacks. Its completion time is `2`, giving `2 * 2 = 4`. This avoids the common off-by-one mistake of treating equality as insufficient damage.

For the ratio-ordering case

```
1
2
1 2
2 3
```

the first monster requires `1` attack and has attack value `2`, giving ratio `1/2`. The second requires `2` attacks and has attack value `3`, giving ratio `2/3`. The algorithm kills the first monster at time `1`, contributing `2`, then kills the second at time `3`, contributing `9`, for a total of `11`. Reversing them would give `6 + 6 = 12`, so sorting only by attack value or only by required attacks would miss the optimum.

For equal ratios, consider

```
1
2
1 2
2 4
```

Both monsters have ratio `1/2`. If the first is processed first, the cost is `2*1 + 4*3 = 14`. If the second is processed first, the cost is `4*2 + 2*3 = 14`. The exchange condition becomes equality, so either order is optimal.

For maximum health,

```
1
1
100000 1
```

the algorithm finds `447` because

[
\frac{446\cdot447}{2}=99681<100000
]

while

[
\frac{447\cdot448}{2}=100128\ge100000.
]

The monster therefore dies on the 447th hero attack, and since its attack value is `1`, the answer is `447`.

The maximum-size equal-monster case contains `100000` monsters, each requiring one attack and having attack value `1`. Every ordering is equivalent. Their completion times are `1` through `100000`, so the answer is

[
1+2+\cdots+100000=5000050000.
]

This case exercises both the `O(n log n)` sorting implementation and the need for an integer type capable of holding an answer larger than `2^32`.
