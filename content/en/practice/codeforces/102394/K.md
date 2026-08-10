---
title: "CF 102394K - Keeping Rabbits"
description: "We have (n) rabbits with initial weights (w1,w2,ldots,wn). On each of (k) mornings, exactly one rabbit receives one additional unit of weight."
date: "2026-08-10T19:12:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102394
codeforces_index: "K"
codeforces_contest_name: "The 2019 China Collegiate Programming Contest Harbin Site"
rating: 0
weight: 102394
solve_time_s: 60
verified: true
draft: false
---

[CF 102394K - Keeping Rabbits](https://codeforces.com/problemset/problem/102394/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) rabbits with initial weights (w_1,w_2,\ldots,w_n). On each of (k) mornings, exactly one rabbit receives one additional unit of weight. A rabbit whose current weight is (x) wins that morning's fight with probability proportional to (x), so if the current total weight is (S), rabbit (i) is chosen with probability (x_i/S).

The total weight is not random. It starts at

[
W=w_1+w_2+\cdots+w_n
]

and increases by exactly one after every carrot, so immediately before the (t)-th carrot the total weight is (W+t). The task is to find the expected final weight of every rabbit after all (k) carrots have been eaten.

The constraints make direct simulation unsuitable. A single case can have (k=10^9), so even performing one update per morning can require a billion operations. Across all test cases, (n) can reach (10^6), so an algorithm with a factor such as (n^2) is also far beyond a practical competitive-programming limit. We need a formula that processes each rabbit essentially once.

The main difficulty is that the probability of choosing a rabbit changes after every carrot. A careless solution might use the initial probability (w_i/W) for every carrot, but that ignores the reinforcement effect. For example, with weights (1,3) and (k=2), the correct expected final weights are (1.5,4.5). Simply adding (2\cdot(1/4)) and (2\cdot(3/4)) gives exactly those values in this case, but that coincidence does not justify using fixed probabilities. After the first carrot, the weights have changed, so the second probability is random.

A more revealing edge case is one rabbit. For input (n=1,k=1,w=[5]), the answer is exactly (6). Any probabilistic treatment that still performs an approximate calculation is unnecessary because the only rabbit must win every fight. More generally, for (n=1), the answer must always be (w_1+k).

Equal weights provide another useful check. For (n=3,k=2,w=[1,1,1]), symmetry says every rabbit must have the same expectation. The total final weight is (5), so the answer is (5/3,5/3,5/3). A solution that updates only the currently largest rabbit, or assumes the same rabbit wins repeatedly, would violate this symmetry.

Large initial weights also expose numerical mistakes. Suppose (n=2,k=1,w=[10^9,1]). The first rabbit's expected increase is (10^9/(10^9+1)), while the second's is (1/(10^9+1)). The denominator must be the current total weight, not a value that overflows a narrow integer type or is accidentally replaced by an individual weight.

## Approaches

The most direct exact approach is to consider every possible sequence of winners. At each morning there are (n) possible winners, and the probability of each branch depends on all previous winners. A complete winner sequence therefore has up to (n^k) possibilities. Even with (n=2) and (k=10^9), this is hopeless. Dynamic programming over the number of times each rabbit has won does not solve the fundamental problem either, because the number of possible distributions of (k) wins among (n) rabbits is (\binom{n+k-1}{n-1}), which is also enormous.

A simpler brute-force simulation can generate one random sequence of winners in (O(k)) operations, but that computes one sample path rather than the exact expectation required by the problem. Repeating the simulation only produces an approximation, and (k) itself can already be (10^9).

The useful observation is that although the individual weights are random, their total is completely deterministic. Suppose rabbit (i) has weight (X_i(t)) after (t) carrots. Before the next carrot, the total weight is exactly (W+t). During the next fight, rabbit (i) gains one with conditional probability

[
\frac{X_i(t)}{W+t}.
]

We can take the conditional expectation of its next weight:

X_i(t)+\frac{X_i(t)}{W+t}.
]

The denominator contains no random quantity, so taking expectation again gives

\left(1+\frac{1}{W+t}\right)\mathbb E[X_i(t)].
]

This is the key simplification. The complicated random process has turned into a deterministic recurrence for each rabbit's expectation.

Starting from (\mathbb E[X_i(0)]=w_i), repeatedly applying the recurrence gives

w_i
\prod_{t=0}^{k-1}\frac{W+t+1}{W+t}.
]

The product telescopes:

\frac{W+k}{W}.
]

Hence the final expected weight is simply

[
\boxed{\mathbb E[X_i(k)] = w_i\frac{W+k}{W}}.
]

The brute-force approach works because it follows the actual random process, but it fails because the number of possible histories is enormous. The observation that the total weight is deterministic lets us take expectations one step at a time, and the resulting recurrence collapses into a telescoping product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^k)) histories | (O(n)) per state | Too slow |
| Random simulation | (O(k)) per simulation | (O(n)) | Does not give the exact expectation |
| Optimal | (O(n)) per case | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the number of rabbits, the number of carrots (k), and all initial weights. Compute their sum (W), because the total weight after (t) carrots will always be (W+t).
2. Compute the common multiplier

[
M=\frac{W+k}{W}.
]

This multiplier is the same for every rabbit. The random process affects which rabbit receives each individual carrot, but it does not affect the expected multiplicative growth factor.

1. For every rabbit (i), output

[
w_iM.
]

There is no need to simulate any morning or maintain the changing weights, because the recurrence has already accounted for every possible winner sequence.

1. Print the values with enough decimal precision, such as ten digits after the decimal point. The required error is (10^{-4}), so ordinary double-precision floating-point arithmetic is more than sufficient.

### Why it works

Let (X_i(t)) be rabbit (i)'s weight after (t) carrots. The total weight at that moment is deterministically (W+t). Conditional on (X_i(t)), the probability that rabbit (i) receives the next carrot is (X_i(t)/(W+t)). Consequently,

X_i(t)\frac{W+t+1}{W+t}.
]

Taking expectations gives the same multiplicative factor for (\mathbb E[X_i(t)]). Starting from (w_i), all factors telescope, leaving (w_i(W+k)/W). Since this equation follows directly from the conditional expectation at every individual step, it accounts for every possible sequence of winners exactly, not approximately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        w = list(map(int, input().split()))

        total = sum(w)
        factor = (total + k) / total

        out.append(" ".join(f"{x * factor:.10f}" for x in w))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first computes `total`, which is the initial combined weight (W). Because exactly one carrot of weight one is consumed each day, the combined weight after all (k) days is (W+k).

The expression `(total + k) / total` computes the telescoped product directly. Computing the product one factor at a time would require (k) iterations, which defeats the purpose of the derivation.

Each initial weight is multiplied by the same factor. The multiplication is performed as a floating-point operation because the required output is a real number.

Python integers handle the potentially large value of the total weight safely. The largest possible initial total is (10^5\cdot10^9=10^{14}), and adding (10^9) is also well within Python's exact integer range. The final conversion to floating point is safe for the required (10^{-4}) error tolerance.

The code processes every weight exactly once after computing the sum, giving linear work in the number of rabbits.

## Worked Examples

### Sample 1

The first sample case has one rabbit with weight (2) and one carrot.

The initial total is (W=2). Since there is only one rabbit, it receives the carrot with probability one. The formula gives

[
2\cdot\frac{2+1}{2}=3.
]

| Step | (W) | (k) | Multiplier | Expected weight |
| --- | --- | --- | --- | --- |
| Initial | 2 | 1 | (3/2) | 2 |
| Final | 2 | 1 | (3/2) | 3 |

The result is `3.00000000`. This example confirms the (n=1) boundary case. The formula does not introduce any artificial randomness when the winner is deterministic.

### Sample 2

The second sample case has two rabbits with weights (1,3) and two carrots.

The initial total is (W=4), and the final total is (6). Both expected weights are multiplied by

[
\frac{6}{4}=1.5.
]

| Rabbit | Initial weight | (W) | (W+k) | Multiplier | Expected final weight |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 6 | 1.5 | 1.5 |
| 2 | 3 | 4 | 6 | 1.5 | 4.5 |

The output is `1.50000000 4.50000000`. The expected weights sum to (6), matching the deterministic final total. This is a useful consistency check for the formula.

### Sample 3

The third sample has three equal rabbits, each starting at (1), with two carrots.

Here (W=3) and (W+k=5), so every rabbit gets the same multiplier (5/3).

| Rabbit | Initial weight | (W) | (W+k) | Expected final weight |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 5 | (5/3) |
| 2 | 1 | 3 | 5 | (5/3) |
| 3 | 1 | 3 | 5 | (5/3) |

The result is approximately `1.66666667 1.66666667 1.66666667`. The equality is expected from symmetry, even though individual random executions can give different final weights.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) per case, (O(\sum n)) overall | The weights are summed and then each rabbit is processed once |
| Space | (O(n)) per case | The input weights and generated output are stored |

Since the sum of (n) over all test cases is at most (10^6), the entire input requires only linear work in (10^6) weights. The value of (k) does not appear in the running time at all, which is essential because (k) can be (10^9).

## Test Cases

The assertions below compare floating-point outputs numerically rather than requiring an exact textual representation. This matches the problem's error-based judging rule.

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, k = map(int, input().split())
        w = list(map(int, input().split()))

        total = sum(w)
        factor = (total + k) / total

        out.append(" ".join(f"{x * factor:.10f}" for x in w))

    sys.stdin = old_stdin
    return "\n".join(out)

def run(inp: str):
    return solve_data(inp).split()

def assert_close(actual, expected, eps=1e-7):
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert abs(float(a) - e) <= eps, (a, e)

# Provided samples
sample = """\
3
1 1
2
2 2
1 3
3 2
1 1 1
"""

assert_close(
    run(sample),
    [3.0, 1.5, 4.5, 5 / 3, 5 / 3, 5 / 3]
)

# Minimum-size input: one rabbit, one carrot.
assert_close(
    run("""\
1
1 1
1
"""),
    [2.0]
)

# No probabilistic choice exists with one rabbit, even for huge k.
assert_close(
    run("""\
1
1 1000000000
1000000000
"""),
    [2000000000.0]
)

# All equal weights. Every rabbit must have the same expectation.
assert_close(
    run("""\
1
4 5
2 2 2 2
"""),
    [3.25, 3.25, 3.25, 3.25]
)

# Strongly unequal weights and k=1.
# The expected values are w_i + w_i / total.
assert_close(
    run("""\
1
2 1
1000000000 1
"""),
    [
        1000000000 * 2000000001 / 1000000001,
        2000000001 / 1000000001
    ]
)

# k=0 is not allowed by the original constraints, but this checks
# that the formula has the correct natural boundary behavior.
assert_close(
    run("""\
1
3 0
1 4 7
"""),
    [1.0, 4.0, 7.0]
)

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1` | `2` | Minimum number of rabbits and carrots |
| `1 / 1 1000000000 / 1000000000` | `2000000000` | Very large (k) and deterministic winner |
| `1 / 4 5 / 2 2 2 2` | `3.25` for every rabbit | Symmetry and equal initial weights |
| `1 / 2 1 / 1000000000 1` | Approximately `1000000000.999999999`, `0.000000001` added to the second weight | Unequal weights and one-step boundary |
| `1 / 3 0 / 1 4 7` | `1 4 7` | Natural zero-carrot boundary of the formula |

## Edge Cases

The single-rabbit case is completely deterministic. For input

```
1
1 1
5
```

we have (W=5) and (k=1), so the multiplier is (6/5). The result is (5\cdot6/5=6). For (k=10^9), the same reasoning gives (5+10^9). The algorithm never tries to model a probability distribution where none exists.

Equal weights require the expectations to remain equal because the rabbits are interchangeable. For

```
1
3 2
1 1 1
```

the total starts at (3), the final total is (5), and every rabbit receives the multiplier (5/3). The output is (5/3) for each rabbit. Individual executions may produce weights such as ((3,1,1)) or ((2,2,1)), but their expected values are identical.

The one-carrot case is where the recurrence can be checked directly. For

```
1
2 1
2 3
```

the total is (5). Rabbit one wins with probability (2/5), so its expected final weight is (2+2/5=2.4). Rabbit two wins with probability (3/5), giving (3+3/5=3.6). The formula produces (2\cdot6/5=2.4) and (3\cdot6/5=3.6), exactly matching the direct calculation.

A very large (k) must not cause a loop over the mornings. For

```
1
2 1000000000
1 1
```

the initial total is (2), so the multiplier is (1000000002/2=500000001). Both rabbits have expected final weight (500000001). The algorithm obtains this immediately, whereas a simulation would require one billion iterations.

Finally, the expected weights must always sum to the deterministic final total (W+k). For any input, summing the formula gives

# \frac{W+k}{W}\sum_i w_i

W+k.
]

This identity is a useful debugging check because an implementation that accidentally uses different denominators or updates the multiplier incorrectly will generally violate it.
