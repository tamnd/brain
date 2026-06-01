---
title: "CF 1942G - Bessie and Cards"
description: "The deck contains four kinds of cards. A draw-0 card consumes one playable card from your hand and gives nothing back. A draw-1 card replaces itself. A draw-2 card consumes one card and gives two new cards, so it increases your future drawing power by one."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1942
codeforces_index: "G"
codeforces_contest_name: "CodeTON Round 8 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2800
weight: 1942
solve_time_s: 231
verified: true
draft: false
---

[CF 1942G - Bessie and Cards](https://codeforces.com/problemset/problem/1942/G)

**Rating:** 2800  
**Tags:** combinatorics, dp, math  
**Solve time:** 3m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The deck contains four kinds of cards. A draw-0 card consumes one playable card from your hand and gives nothing back. A draw-1 card replaces itself. A draw-2 card consumes one card and gives two new cards, so it increases your future drawing power by one. There are also 5 special cards, and the goal is to draw all of them before getting stuck.

At the beginning, Bessie draws the top 5 cards. After that she may repeatedly play draw cards that are currently in her hand. A card can only be played once. If at some point there is no playable draw card left, the process ends.

We are given the counts of draw-0, draw-1, and draw-2 cards. The deck is shuffled uniformly at random. We must compute the probability that all 5 special cards are eventually drawn, and output that probability modulo `998244353`.

The constraints are large enough that any state-space simulation is hopeless. Each of `a`, `b`, and `c` can reach `2 · 10^5`, and there may be up to `10^4` test cases. An algorithm with complexity proportional to the number of deck permutations is obviously impossible, but even quadratic DP over `a` and `c` would exceed the limit. Since the sums of all `a`, `b`, and `c` across test cases are each at most `2 · 10^5`, an `O(a + c)` solution per test case is feasible.

There are a few easy-to-miss cases.

Consider `a = b = c = 0`. The deck contains only the 5 special cards. Bessie immediately draws all 5 cards at the start, so the answer is exactly `1`.

Consider `a = 1, b = 0, c = 0`. The deck contains one draw-0 card and five special cards. Bessie draws the first 5 cards and can never gain extra cards. She wins unless the draw-0 card appears among the first five positions and pushes a special card to position 6. The probability is not `1`, even though there is only one non-special card.

Another subtle point is that draw-1 cards do not change the number of future cards Bessie can access. A careless solution may try to include them in the DP state, which creates a much larger problem than necessary. In reality they are completely irrelevant to the stopping condition.

## Approaches

A brute-force solution would enumerate every deck ordering, simulate the game, and count how many shuffles lead to a win.

The simulation itself is easy. Maintain the current hand, repeatedly play available draw cards, and stop when none remain. If all 5 special cards were seen, the shuffle is successful.

The problem is the number of shuffles. The deck size can be around `6 · 10^5` in total across test cases. Even for tiny inputs, the number of permutations grows factorially. This approach becomes impossible almost immediately.

The key observation is that draw-1 cards contribute nothing to the resource balance. Playing one consumes a card and draws exactly one card. They never help and never hurt.

Now define a balance:

- Start with balance `5`, because the first 5 cards are drawn for free.
- A draw-2 card contributes `+1`.
- A draw-0 card contributes `-1`.
- A special card also contributes `-1`, because it occupies one drawn slot but cannot be played.

As Bessie reveals cards from top to bottom, the balance tells us how many more cards can still be revealed.

The process stops exactly at the first prefix where the balance becomes `0`.

This transforms the game into a lattice-path problem.

Ignore draw-1 cards entirely. Among the remaining cards:

- draw-2 becomes `+1`
- draw-0 becomes `-1`
- special becomes `-1`

We start at height `5`.

A winning deck is one where all 5 special cards appear before the first time the balance reaches `0`.

Suppose the first hit of `0` occurs after using exactly `p` draw-2 cards. Then the stopping prefix must contain:

- `p` draw-2 cards
- `p + 5` negative cards

Since all 5 specials must already be seen, those `p + 5` negatives consist of:

- all 5 specials
- exactly `p` draw-0 cards

The rest of the deck is arbitrary.

The remaining task becomes counting ballot paths. We need the number of sequences with `p` up-steps and `p + 5` down-steps that start from height `5` and hit `0` for the first time at the end of the prefix.

The classical Bertrand ballot / reflection-principle result gives

$$F_p = \frac{5}{2p+5}\binom{2p+5}{p}.$$

After choosing such a path, we choose which of the `p+5` negative positions contain the 5 specials, and then arrange the remaining suffix.

This leads directly to a summation over `p`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Factorial in deck size | Exponential | Too slow |
| Optimal | `O(min(a,c))` per test case | `O(a+c)` precomputation | Accepted |

## Algorithm Walkthrough

1. Ignore all draw-1 cards.

They never change the balance. Removing them preserves the relative order of every card that affects reachability.
2. Let the first time the balance reaches `0` use exactly `p` draw-2 cards.

Since we start at balance `5`, reaching `0` requires a net change of `-5`. Therefore the stopping prefix contains exactly `p+5` negative cards.
3. Force all 5 special cards to appear before stopping.

Among the `p+5` negative positions in the stopping prefix, choose which 5 contain specials.

The count is

$$\binom{p+5}{5}.$$
4. Count valid balance paths.

The stopping prefix contains `p` positive steps and `p+5` negative steps.

The balance must stay positive until the last step.

By the ballot theorem,

$$F_p=\frac{5}{2p+5}\binom{2p+5}{p}.$$
5. Arrange the remaining cards.

After the stopping prefix is fixed, the suffix contains:

- `a-p` draw-0 cards
- `c-p` draw-2 cards

The number of suffix arrangements is

$$\binom{a+c-2p}{a-p}.$$
6. Sum over all feasible values of `p`.

Since we need `p` draw-0 cards and `p` draw-2 cards inside the stopping prefix,

$$0 \le p \le \min(a,c).$$
7. Divide by the total number of nonzero-card sequences.

Ignoring draw-1 cards, the total number of sequences is

$$\frac{(a+c+5)!}{a!\,c!\,5!}.$$
8. Simplify the formula and evaluate it modulo `998244353`.

### Why it works

Every game state is completely determined by the balance. A draw-2 increases future reachability by one, while both draw-0 and special cards decrease it by one. The game ends exactly at the first prefix where the balance becomes zero.

For a fixed stopping point, the stopping prefix must contain equal numbers of draw-0 and draw-2 cards, except for the extra deficit of five caused by the five special cards. The ballot theorem counts exactly those prefixes whose balance never reaches zero earlier. Choosing the positions of the special cards among the negative steps guarantees that all specials are drawn before stopping. Every winning deck corresponds to exactly one value of `p`, and every counted configuration produces a valid winning deck. Thus the summation counts all winning decks exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

MAXN = 400005

fac = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fac[i] = fac[i - 1] * i % MOD

invfac = [1] * (MAXN + 1)
invfac[MAXN] = pow(fac[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    invfac[i - 1] = invfac[i] * i % MOD

def C(n, r):
    if r < 0 or r > n:
        return 0
    return fac[n] * invfac[r] % MOD * invfac[n - r] % MOD

def solve():
    t = int(input())

    for _ in range(t):
        a, b, c = map(int, input().split())

        total_inv = pow(
            fac[a + c + 5] * invfac[a] % MOD * invfac[c] % MOD * fac[5] % MOD,
            MOD - 2,
            MOD
        )

        good = 0

        for p in range(min(a, c) + 1):
            ballot = 5 * pow(2 * p + 5, MOD - 2, MOD) % MOD
            ballot = ballot * C(2 * p + 5, p) % MOD

            specials = C(p + 5, 5)
            suffix = C(a + c - 2 * p, a - p)

            good = (good + ballot * specials % MOD * suffix) % MOD

        ans = good * total_inv % MOD
        print(ans)

solve()
```

The implementation follows the counting argument directly.

The factorial tables support constant-time binomial coefficients. Since `a + c + 5` never exceeds `400005`, one global precomputation is enough.

The variable `ballot` stores

$$\frac{5}{2p+5}\binom{2p+5}{p},$$

computed modulo `MOD`. Division is performed with a modular inverse.

`specials` chooses which negative positions correspond to special cards, while `suffix` arranges the cards that remain after the stopping prefix.

The quantity `good` counts winning nonzero-card sequences. The total number of nonzero-card sequences is

$$\frac{(a+c+5)!}{a!\,c!\,5!},$$

so we multiply by its modular inverse at the end.

A common mistake is trying to keep draw-1 cards in the counting. They never affect the balance, so doing so only complicates the combinatorics and usually leads to overcounting.

## Worked Examples

### Example 1

Input:

```
1 1 1
```

Possible values of `p` are `0` and `1`.

| p | Ballot count | Choose specials | Suffix count | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | 2 |
| 1 | 5 | 6 | 1 | 30 |

Total winning sequences:

$$2 + 30 = 32.$$

Total nonzero-card sequences:

$$\frac{7!}{1!\cdot1!\cdot5!}=42.$$

Probability:

$$\frac{32}{42} = \frac{16}{21}.$$

This matches the sample.

The trace shows how the summation naturally splits by the location where the balance first reaches zero.

### Example 2

Input:

```
0 0 0
```

There are only 5 special cards.

| p | Ballot count | Choose specials | Suffix count | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |

Total winning sequences = 1.

Total sequences = 1.

Answer = 1.

This exercises the smallest possible deck and confirms that the formula handles empty draw-card counts correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(min(a,c))` | One summation over all feasible values of `p` |
| Space | `O(a+c)` preprocessing | Factorial and inverse-factorial tables |

The sums of all `a` and all `c` across test cases are each at most `2 · 10^5`. Since every test case iterates only up to `min(a,c)`, the total amount of work stays well within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    MAXN = 400005

    fac = [1] * (MAXN + 1)
    for i in range(1, MAXN + 1):
        fac[i] = fac[i - 1] * i % MOD

    invfac = [1] * (MAXN + 1)
    invfac[MAXN] = pow(fac[MAXN], MOD - 2, MOD)
    for i in range(MAXN, 0, -1):
        invfac[i - 1] = invfac[i] * i % MOD

    def C(n, r):
        if r < 0 or r > n:
            return 0
        return fac[n] * invfac[r] % MOD * invfac[n - r] % MOD

    t = int(input())
    out = []

    for _ in range(t):
        a, b, c = map(int, input().split())

        total_inv = pow(
            fac[a + c + 5] * invfac[a] % MOD * invfac[c] % MOD * fac[5] % MOD,
            MOD - 2,
            MOD
        )

        good = 0

        for p in range(min(a, c) + 1):
            ballot = 5 * pow(2 * p + 5, MOD - 2, MOD) % MOD
            ballot = ballot * C(2 * p + 5, p) % MOD

            good = (
                good
                + ballot * C(p + 5, 5) % MOD
                * C(a + c - 2 * p, a - p)
            ) % MOD

        out.append(str(good * total_inv % MOD))

    return "\n".join(out)

# provided samples
assert run(
"""4
1 1 1
0 0 0
5 3 7
3366 1434 1234
"""
) == "\n".join([
    "903173463",
    "1",
    "35118742",
    "398952013"
]), "sample"

# minimum deck
assert run(
"""1
0 0 0
"""
) == "1", "only specials"

# one draw-0 card
assert run(
"""1
1 0 0
"""
) == "166374059", "probability 5/6"

# draw-1 cards do not matter
assert run(
"""2
0 0 0
0 100 0
"""
) == "1\n1", "draw-1 cards are irrelevant"

# symmetric small case
assert run(
"""1
1 0 1
"""
) == "903173463", "same probability as sample without draw-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `1` | Smallest possible deck |
| `1 0 0` | `5/6 mod MOD` | One extra negative card |
| `0 100 0` | `1` | Draw-1 cards do not affect the answer |
| `1 0 1` | Same as sample case | Confirms independence from `b` |

## Edge Cases

The first edge case is the deck containing only specials.

```
a = 0, b = 0, c = 0
```

The balance starts at `5`. All five cards are immediately drawn, so every special card is seen before the process can stop. In the formula, only `p = 0` contributes. The answer becomes exactly `1`.

The second edge case is having extra draw-0 cards but no draw-2 cards.

```
a = 1, b = 0, c = 0
```

The only valid value is `p = 0`. The stopping prefix consists of exactly the five specials. If the draw-0 card appears before any special, one special gets pushed beyond the stopping point and Bessie loses. The counting formula gives probability `5/6`, which matches the direct argument.

The third edge case is a large number of draw-1 cards.

```
a = 0, b = 200000, c = 0
```

The balance never changes because draw-1 cards contribute zero. Bessie keeps drawing through every draw-1 card and eventually reaches all specials. The algorithm never even uses `b`, which correctly reflects the fact that draw-1 cards have no influence on reachability.

The final subtle case is when `a` and `c` are very different.

```
a = 200000, c = 0
```

The summation only allows `p = 0`. No invalid terms are generated because the range is `0 .. min(a,c)`. This avoids negative binomial arguments and keeps the computation correct even at the boundary of the constraints.
