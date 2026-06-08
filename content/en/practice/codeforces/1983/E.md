---
title: "CF 1983E - I Love Balls"
description: "There are two kinds of balls. The first k balls are special, the remaining n-k are ordinary. Every ball has a value. The balls are removed one by one in a uniformly random order. The current player takes the chosen ball and adds its value to their score."
date: "2026-06-08T16:38:36+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1983
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 956 (Div. 2) and ByteRace 2024"
rating: 2300
weight: 1983
solve_time_s: 200
verified: true
draft: false
---

[CF 1983E - I Love Balls](https://codeforces.com/problemset/problem/1983/E)

**Rating:** 2300  
**Tags:** combinatorics, math, probabilities  
**Solve time:** 3m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

There are two kinds of balls. The first `k` balls are special, the remaining `n-k` are ordinary. Every ball has a value.

The balls are removed one by one in a uniformly random order. The current player takes the chosen ball and adds its value to their score. The interesting rule is what happens next.

If the chosen ball is ordinary, the turn passes to the other player.

If the chosen ball is special, the same player immediately plays again.

Alice starts.

We need the expected final score of Alice and the expected final score of Bob. Since the answer is a rational number, we output it modulo `10^9+7` using modular inverses.

The total number of balls across all test cases is at most `5 · 10^5`. Any algorithm that tries to enumerate permutations, game states, or probability distributions over subsets is hopeless. Even `O(n^2)` per test case would be too expensive in the worst case. We need something essentially linear in the number of balls.

The main danger is assuming that every ball has probability `1/2` of belonging to Alice. That is false because the turn changes only when an ordinary ball is taken.

Consider:

```
n = 2, k = 1
special value = 10
ordinary value = 20
```

The two possible orders are:

```
S N
```

Alice gets both balls.

```
N S
```

Alice gets only the ordinary ball.

Alice's expected score is `25`, not `(10+20)/2 = 15`.

Another easy mistake is treating special and ordinary balls identically. Their ownership probabilities are different.

For example:

```
n = 3, k = 1
values = [100, 1, 1]
```

The special ball is much more likely to belong to Alice than either ordinary ball. Any solution that computes a single probability for every ball will produce the wrong expectation.

The case `k = n` is also special. There are no ordinary balls, so the turn never changes and Alice receives every ball with probability `1`.

## Approaches

A brute-force solution would generate every possible order of the balls. For each permutation we could simulate the game, compute the resulting scores, and average over all permutations.

This is correct because every removal order is equally likely. The problem is the size of the state space. There are `n!` possible orders. Even for `n = 15`, that is already more than a trillion permutations.

The key observation is that expected value is linear.

Instead of asking for the entire score distribution, we can ask a much smaller question:

"What is the probability that a particular ball belongs to Alice?"

If we know that probability, then the ball contributes

```
value × probability
```

to Alice's expected score.

All special balls are symmetric. All ordinary balls are symmetric. So we only need two probabilities:

```
pS = probability a specific special ball belongs to Alice
pN = probability a specific ordinary ball belongs to Alice
```

Once these are known,

```
Alice =
pS × (sum of special values)
+
pN × (sum of ordinary values)
```

and Bob receives the remaining expected value.

The remaining task is purely combinatorial.

The crucial simplification is that special balls never change whose turn it is. Only ordinary balls cause alternation. If we look only at the sequence of ordinary balls, Alice owns the 1st, Bob owns the 2nd, Alice owns the 3rd, and so on.

Special balls merely get inserted into the gaps created by those ordinary balls.

This turns the whole game into counting gaps and ranks, leading to a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n! · n)` | `O(n)` | Too slow |
| Optimal | `O(n)` per test case | `O(1)` extra | Accepted |

## Algorithm Walkthrough

Let

```
m = n - k
```

be the number of ordinary balls.

### Probability for a special ball

Imagine removing all special balls and keeping only the `m` ordinary balls.

They create exactly `m + 1` gaps:

```
before first ordinary
between ordinary 1 and 2
between ordinary 2 and 3
...
after last ordinary
```

A player's identity changes whenever an ordinary ball is taken.

So the ownership of the gaps alternates:

```
Alice, Bob, Alice, Bob, ...
```

Take one particular special ball.

Its relative position among the ordinary balls is determined only by how many ordinary balls appear before it. That number can be any value from `0` to `m`.

By symmetry, all `m + 1` possibilities are equally likely.

Hence the special ball chooses a gap uniformly among the `m + 1` gaps.

Alice owns

```
ceil((m + 1) / 2)
```

of those gaps.

Therefore

```
pS = ceil((m + 1) / 2) / (m + 1)
```

### Probability for an ordinary ball

Consider a particular ordinary ball.

Among the `m` ordinary balls, its rank is equally likely to be any value from `1` to `m`.

The 1st ordinary ball belongs to Alice.

The 2nd belongs to Bob.

The 3rd belongs to Alice.

And so on.

Alice owns exactly the odd ranks.

The number of odd ranks is

```
ceil(m / 2)
```

Thus

```
pN = ceil(m / 2) / m
```

when `m > 0`.

### Computing expectations

Let

```
special_sum = sum of first k values
ordinary_sum = sum of remaining values
```

Then

```
Alice =
special_sum × pS
+
ordinary_sum × pN
```

All arithmetic is performed modulo `10^9+7`.

Bob receives the remaining expected value:

```
Bob =
(total_sum - Alice)
```

### Why it works

The ownership of any ball depends only on the number of ordinary balls that appear before it. Special balls never alter turn parity.

For a special ball, the only relevant quantity is the gap among the ordinary balls in which it lands. Every gap is equally likely, and the ownership of gaps alternates.

For an ordinary ball, the only relevant quantity is its rank among ordinary balls. Every rank is equally likely, and ownership alternates by rank parity.

Since expectation is linear, summing value times ownership probability over all balls gives the exact expected score. Symmetry reduces the computation to one probability for all special balls and one probability for all ordinary balls.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    v = list(map(int, input().split()))

    m = n - k

    special_sum = sum(v[:k]) % MOD
    ordinary_sum = sum(v[k:]) % MOD

    if m == 0:
        alice = special_sum
        bob = 0
        print(alice, bob)
        continue

    pS = ((m + 2) // 2) * pow(m + 1, MOD - 2, MOD)
    pS %= MOD

    pN = ((m + 1) // 2) * pow(m, MOD - 2, MOD)
    pN %= MOD

    alice = (special_sum * pS + ordinary_sum * pN) % MOD

    total = (special_sum + ordinary_sum) % MOD
    bob = (total - alice) % MOD

    print(alice, bob)
```

The first step computes the total value of all special balls and all ordinary balls separately.

When there are no ordinary balls, the turn never changes. Alice collects everything, so the answer is immediate.

For `m > 0`, the code evaluates the two probabilities derived above. Division under modulo arithmetic is implemented using Fermat's theorem:

```
x / y  ->  x * y^(MOD-2)
```

The expected score of Alice is computed directly from linearity of expectation.

Bob's expected score is obtained by subtracting Alice's expectation from the total value. This avoids duplicating probability calculations and automatically preserves the invariant that the two expectations sum to the total value.

The only subtle corner case is `m = 0`, because `pN` would require division by zero. That case is handled separately.

## Worked Examples

### Sample 1

Input:

```
n = 5
k = 2
values = [10, 20, 5, 15, 25]
```

We have:

```
special_sum = 30
ordinary_sum = 45
m = 3
```

| Quantity | Value |
| --- | --- |
| m | 3 |
| pS | 2 / 4 = 1/2 |
| pN | 2 / 3 |
| Special contribution | 30 × 1/2 = 15 |
| Ordinary contribution | 45 × 2/3 = 30 |
| Alice | 45 |
| Bob | 30 |

The answer is:

```
45 30
```

This example shows that special and ordinary balls use different probabilities.

### Custom Example

```
n = 3
k = 1
values = [100, 1, 1]
```

| Quantity | Value |
| --- | --- |
| m | 2 |
| pS | 2/3 |
| pN | 1/2 |
| Special contribution | 100 × 2/3 |
| Ordinary contribution | 2 × 1/2 = 1 |
| Alice | 203/3 |
| Bob | 102 - 203/3 = 103/3 |

This example highlights why the special ball cannot be treated as having probability `1/2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each ball is visited once while computing sums |
| Space | `O(1)` | Only a few variables besides the input array |

The total number of balls over all test cases is at most `5 · 10^5`, so a linear scan easily fits within the time limit. The memory usage is constant apart from storing the current test case.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        v = list(map(int, input().split()))

        m = n - k

        ss = sum(v[:k]) % MOD
        sn = sum(v[k:]) % MOD

        if m == 0:
            out.append(f"{ss} 0")
            continue

        pS = ((m + 2) // 2) * pow(m + 1, MOD - 2, MOD) % MOD
        pN = ((m + 1) // 2) * pow(m, MOD - 2, MOD) % MOD

        alice = (ss * pS + sn * pN) % MOD
        bob = (ss + sn - alice) % MOD

        out.append(f"{alice} {bob}")

    return "\n".join(out)

# sample
assert run(
"""1
5 2
10 20 5 15 25
"""
) == "45 30"

# minimum size
assert run(
"""1
1 1
7
"""
) == "7 0"

# all balls special
assert run(
"""1
4 4
1 2 3 4
"""
) == "10 0"

# one special, one ordinary
assert run(
"""1
2 1
10 20
"""
) == "25 5"

# all values equal
assert run(
"""1
5 2
1 1 1 1 1
"""
) == "3 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `7 0` | Smallest possible instance |
| `4 4 / 1 2 3 4` | `10 0` | No ordinary balls |
| `2 1 / 10 20` | `25 5` | Different probabilities for special and ordinary balls |
| `5 2 / 1 1 1 1 1` | `3 2` | Symmetry and expectation arithmetic |

## Edge Cases

### All balls are special

Input:

```
1
4 4
1 2 3 4
```

There are no ordinary balls. The turn never changes.

Alice takes every ball:

```
Alice = 10
Bob = 0
```

The implementation handles this before computing any modular inverses.

### Exactly one ordinary ball

Input:

```
1
2 1
10 20
```

There is one gap before the ordinary ball and one gap after it.

The special ball lands in either gap with equal probability.

```
pS = 1/2
pN = 1
```

Alice's expectation becomes:

```
10 × 1/2 + 20 × 1 = 25
```

which matches direct enumeration.

### Many special balls, no effect on parity

Input:

```
1
5 4
10 10 10 10 100
```

Only one ordinary ball exists.

All four special balls share the same probability:

```
pS = 1/2
```

regardless of how many special balls there are. The derivation depends only on the number of ordinary balls because only ordinary balls affect turn changes. This is exactly the property used by the algorithm.

### Even versus odd number of ordinary balls

Input:

```
1
3 1
100 1 1
```

Here `m = 2`.

Alice owns two of the three gaps, giving

```
pS = 2/3
```

instead of `1/2`.

A solution that assumes every special ball is equally likely to belong to either player would fail on this example. The gap-counting argument correctly produces the larger probability.
