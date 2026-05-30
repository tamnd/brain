---
title: "CF 452C - Magic Trick"
description: "There are $m$ complete decks, each containing the same $n$ card values. After mixing all decks together, there are $mn$ physical cards in total, and every value appears exactly $m$ times."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 452
codeforces_index: "C"
codeforces_contest_name: "MemSQL Start[c]UP 2.0 - Round 1"
rating: 2100
weight: 452
solve_time_s: 104
verified: true
draft: false
---

[CF 452C - Magic Trick](https://codeforces.com/problemset/problem/452/C)

**Rating:** 2100  
**Tags:** combinatorics, math, probabilities  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

There are $m$ complete decks, each containing the same $n$ card values. After mixing all decks together, there are $mn$ physical cards in total, and every value appears exactly $m$ times.

Alex randomly takes $n$ cards from this large pile and uses them as the working deck for the trick.

A spectator then chooses a random card from that working deck, remembers its value, and puts it back. Alex shuffles and draws a random card. Assuming Alex is not doing any magic and is simply drawing uniformly at random, we must compute the probability that the drawn card has the same value as the remembered one.

The input consists of $n$ and $m$. The output is a single floating point number, the probability that the trick succeeds.

The constraints are small, only up to $1000$, but the interesting part is finding the probability analytically. Any approach that tries to enumerate all possible $n$-card selections is impossible because the number of such selections is

$$\binom{mn}{n},$$

which becomes astronomically large even for moderate values.

A few edge cases deserve attention.

When $n=1$, the working deck always contains exactly one card. The spectator picks that card and Alex must draw the same card, so the answer is always $1$. For example:

```
1 5
```

The correct output is:

```
1
```

A formula containing a factor $mn-1$ in the denominator would divide by zero when $n=m=1$, so that case must be handled separately.

Another easy mistake is to assume that every value appears at most once in the working deck. For example:

```
2 2
```

The selected deck can be $\{A,A\}$, which makes success certain. Ignoring duplicates produces the wrong probability.

## Approaches

A brute-force viewpoint is useful because it reveals the quantity we actually need.

Suppose a particular selected deck contains counts

$$c_1,c_2,\dots,c_n,$$

where $c_i$ is the number of copies of value $i$, and

$$c_1+c_2+\cdots+c_n=n.$$

The spectator chooses value $i$ with probability $c_i/n$. After replacement, Alex draws value $i$ with probability $c_i/n$. For this fixed deck, the success probability is

$$\sum_{i=1}^{n}\frac{c_i}{n}\cdot\frac{c_i}{n}
=
\frac{1}{n^2}\sum_{i=1}^{n} c_i^2.$$

A brute-force solution would enumerate every possible selected deck, compute this quantity, and average over all selections. The number of selections is $\binom{mn}{n}$, which is completely infeasible.

The key observation is that we only need the expected value of

$$\sum c_i^2.$$

All card values are symmetric. Let $X$ be the number of copies of one particular value in the selected deck.

Then

$$E\!\left[\sum_{i=1}^{n} c_i^2\right]
=
nE[X^2].$$

So the answer becomes

$$\frac{E[X^2]}{n}.$$

Now $X$ follows a hypergeometric distribution.

There are $mn$ cards total.

Exactly $m$ of them have the chosen value.

We draw $n$ cards.

Thus

$$X \sim \text{Hypergeometric}(N=mn,\ K=m,\ n).$$

For a hypergeometric random variable,

$$E[X]
=
\frac{nK}{N},$$

and

$$\mathrm{Var}(X)
=
n\frac{K}{N}
\left(1-\frac{K}{N}\right)
\frac{N-n}{N-1}.$$

Substituting $N=mn$ and $K=m$,

$$E[X]=1,$$

and

$$\mathrm{Var}(X)
=
\frac{(n-1)(m-1)}{mn-1}.$$

Since

$$E[X^2]
=
\mathrm{Var}(X)+E[X]^2,$$

we obtain

$$E[X^2]
=
1+\frac{(n-1)(m-1)}{mn-1}.$$

Hence

$$P
=
\frac{1}{n}
\left(
1+\frac{(n-1)(m-1)}{mn-1}
\right).$$

This is already sufficient for implementation.

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of all selected decks | Exponential in $n$ | Exponential | Too slow |
| Hypergeometric expectation formula | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $n$ and $m$.
2. Handle the special case $n=m=1$.

In this situation there is only one card in existence, so the success probability is exactly $1$.
3. Compute

$$\mathrm{Var}(X)
=
\frac{(n-1)(m-1)}{mn-1}.$$

This is the variance of the number of copies of a fixed value appearing in the selected deck.

1. Compute

$$E[X^2]
=
1+\mathrm{Var}(X).$$

The mean of $X$ equals $1$, so $E[X]^2=1$.

1. Compute

$$P=\frac{E[X^2]}{n}.$$

By symmetry, the expected value of $\sum c_i^2$ equals $nE[X^2]$.

1. Print the result as a floating point number.

### Why it works

For a fixed selected deck, the success probability equals

$$\frac{1}{n^2}\sum c_i^2.$$

The overall answer is the expectation of this quantity over all random deck selections. Linearity of expectation lets us replace the sum of $n$ symmetric terms by $nE[X^2]$, where $X$ counts copies of a single value. Since $X$ is hypergeometric, its mean and variance are known exactly. Substituting those formulas gives the exact expected success probability. Every step is an equality, so the algorithm computes the true probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    if n == 1 and m == 1:
        print(1.0)
        return

    var = (n - 1) * (m - 1) / (n * m - 1)
    ans = (1.0 + var) / n

    print(ans)

solve()
```

The implementation follows the derivation directly.

The only special handling is $(n,m)=(1,1)$. The closed-form variance contains the factor $mn-1$ in the denominator, which becomes zero there. Probabilistically, the answer is trivially $1$ because only one card exists.

All arithmetic is performed in floating point. The required precision is only $10^{-6}$, so standard Python `float` arithmetic is more than sufficient.

No loops are needed because the entire solution reduces to evaluating a constant-size formula.

## Worked Examples

### Example 1

Input:

```
2 2
```

| Variable | Value |
| --- | --- |
| $n$ | 2 |
| $m$ | 2 |
| $mn-1$ | 3 |
| $(n-1)(m-1)$ | 1 |
| Variance | $1/3$ |
| $E[X^2]$ | $4/3$ |
| Answer | $2/3$ |

Output:

```
0.6666666666666666
```

This is the sample from the statement. Duplicate values can appear in the selected deck, increasing the probability above $1/2$.

### Example 2

Input:

```
3 1
```

| Variable | Value |
| --- | --- |
| $n$ | 3 |
| $m$ | 1 |
| $mn-1$ | 2 |
| $(n-1)(m-1)$ | 0 |
| Variance | 0 |
| $E[X^2]$ | 1 |
| Answer | $1/3$ |

Output:

```
0.3333333333333333
```

With only one copy of every value, the selected deck is always a normal deck containing three distinct cards. The probability of matching the remembered card is exactly $1/3$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The constraints are tiny compared to what this solution can handle. Since the computation is constant time and constant memory, it easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())

    if n == 1 and m == 1:
        return "1.0"

    var = (n - 1) * (m - 1) / (n * m - 1)
    ans = (1.0 + var) / n
    return str(ans)

# provided sample
assert abs(float(run("2 2\n")) - 0.6666666666666666) < 1e-9, "sample 1"

# minimum size
assert abs(float(run("1 1\n")) - 1.0) < 1e-9, "single card"

# one deck only
assert abs(float(run("3 1\n")) - (1.0 / 3.0)) < 1e-9, "all values distinct"

# one card chosen
assert abs(float(run("1 1000\n")) - 1.0) < 1e-9, "deck size one"

# large boundary
expected = (1.0 + (999 * 999) / (1000000 - 1)) / 1000
assert abs(float(run("1000 1000\n")) - expected) < 1e-9, "maximum bounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `0.6666666666666666` | Sample case |
| `1 1` | `1.0` | Division-by-zero special case |
| `3 1` | `0.3333333333333333` | No duplicate values possible |
| `1 1000` | `1.0` | Single-card working deck |
| `1000 1000` | Formula value | Maximum constraints |

## Edge Cases

Consider the smallest possible input:

```
1 1
```

There is only one card in existence. The spectator chooses that card and Alex draws the same card. The algorithm immediately returns `1.0` before evaluating the variance formula, avoiding division by zero and producing the correct answer.

Consider:

```
3 1
```

Every value exists exactly once. The selected deck is always the complete set of three distinct cards. The algorithm computes

$$\mathrm{Var}(X)=0,$$

because a fixed value appears exactly once with certainty. Then

$$P=\frac{1}{3}.$$

This matches the intuitive probability of drawing the remembered card from three distinct cards.

Consider:

```
1 5
```

The working deck contains exactly one card, even though five copies of that value exist in the large pile. The algorithm computes

$$\mathrm{Var}(X)=0,
\qquad
P=1.$$

The spectator and Alex are forced to interact with the same single card, so success is guaranteed.

Finally, consider a case where duplicates matter:

```
2 2
```

A careless solution might assume two distinct values are always selected and answer $1/2$. The hypergeometric calculation correctly accounts for selections such as $\{A,A\}$, which increase the probability. The resulting answer is

$$\frac{2}{3},$$

which matches the sample output.
