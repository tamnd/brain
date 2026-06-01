---
title: "CF 453A - Little Pony and Expected Maximum"
description: "We roll a fair die with faces numbered from 1 to m, exactly n times. Every roll is independent, and each face appears with probability 1 / m. Among those n rolls, we look only at the largest value that appeared. The task is to compute the expected value of that maximum."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 453
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 259 (Div. 1)"
rating: 1600
weight: 453
solve_time_s: 106
verified: true
draft: false
---

[CF 453A - Little Pony and Expected Maximum](https://codeforces.com/problemset/problem/453/A)

**Rating:** 1600  
**Tags:** probabilities  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We roll a fair die with faces numbered from `1` to `m`, exactly `n` times. Every roll is independent, and each face appears with probability `1 / m`.

Among those `n` rolls, we look only at the largest value that appeared. The task is to compute the expected value of that maximum.

The input contains `m` and `n`, where `m` is the number of faces on the die and `n` is the number of throws. The output is a real number representing the expectation of the maximum result after all throws.

The constraints allow both `m` and `n` to be as large as `100000`. Enumerating all possible sequences of rolls is impossible because there are `m^n` outcomes. Even for moderate values such as `m = 100` and `n = 100`, that number is astronomically large.

A solution performing work proportional to `m` is completely fine. A solution proportional to `m^2` would already require about `10^10` operations in the worst case, which is far beyond the time limit.

One subtle case occurs when there is only one throw.

Input:

```
6 1
```

The maximum is simply the die result itself, so the answer is the average of numbers `1..6`, which equals `3.5`.

Another easy-to-miss case is when the die has only one face.

Input:

```
1 100000
```

Every roll is always `1`, so the maximum is always `1`, and the expected value is exactly `1`.

A common mistake is trying to compute the probability that the maximum equals `k` directly and making an off-by-one error. For example:

Input:

```
2 2
```

The maximum equals `1` only when both rolls are `1`, which happens with probability `1/4`. The maximum equals `2` with probability `3/4`. The expectation is

$$1 \cdot \frac14 + 2 \cdot \frac34 = 1.75.$$

Incorrect handling of cumulative probabilities often produces a different result.

## Approaches

The most direct approach is to enumerate every possible sequence of rolls, compute its maximum, and average all maxima. This is correct because expectation is simply the average value weighted by probabilities. Unfortunately, there are `m^n` possible outcomes. With `m = n = 100000`, this is completely infeasible.

The key observation is that maxima are much easier to reason about through cumulative probabilities.

Suppose we want the probability that the maximum value is at most `k`. Every roll must then be at most `k`. Since each roll independently lands in `{1,2,...,k}` with probability `k/m`, we get

$$P(\max \le k) = \left(\frac{k}{m}\right)^n.$$

From this, we can obtain the probability that the maximum is exactly `k`:

$$P(\max = k) = P(\max \le k) - P(\max \le k-1) = \left(\frac{k}{m}\right)^n - \left(\frac{k-1}{m}\right)^n.$$

The expected value is then

$$E[\max] = \sum_{k=1}^{m} k \cdot P(\max = k).$$

Substituting the formula above gives an `O(m)` solution.

Since `m ≤ 100000`, evaluating one power and a few arithmetic operations for each value of `k` easily fits within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m^n)$ | $O(n)$ | Too slow |
| Optimal | $O(m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read `m` and `n`.
2. Initialize `answer = 0`.
3. For every value `k` from `1` to `m`, compute

$$p_k = \left(\frac{k}{m}\right)^n$$

which is the probability that the maximum does not exceed `k`.
4. Compute

$$p = p_k - p_{k-1}$$

where

$$p_{k-1}=\left(\frac{k-1}{m}\right)^n.$$

This gives the probability that the maximum is exactly `k`.
5. Add

$$k \cdot p$$

to the running answer.
6. After processing all values of `k`, print the accumulated expectation.

### Why it works

For every integer `k`, the event "`maximum ≤ k`" occurs exactly when every roll is at most `k`. Because the rolls are independent, its probability is

$$\left(\frac{k}{m}\right)^n.$$

The events "`maximum = k`" partition the entire sample space. Their probabilities are obtained by subtracting consecutive cumulative probabilities:

$$P(\max = k) = P(\max \le k)-P(\max \le k-1).$$

The expectation formula

$$E[X] = \sum_x x \cdot P(X=x)$$

applied to the random variable "maximum roll" gives precisely the value accumulated by the algorithm. Every possible maximum contributes its value multiplied by its probability, so the final sum equals the expected maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())

    ans = 0.0

    for k in range(1, m + 1):
        p1 = (k / m) ** n
        p0 = ((k - 1) / m) ** n
        ans += k * (p1 - p0)

    print("{:.12f}".format(ans))

solve()
```

The implementation follows the mathematical derivation directly.

The loop iterates over all possible values of the maximum. For each `k`, it computes the cumulative probability that all rolls are at most `k`, then subtracts the corresponding probability for `k - 1`. The difference is exactly the probability that the maximum equals `k`.

Using floating-point arithmetic is sufficient because the required error tolerance is only `10^{-4}`. Python's double precision floating point type easily provides much higher accuracy.

The expression for `k = 1` works naturally because

$$\left(\frac{0}{m}\right)^n = 0.$$

No special handling is required.

Printing twelve digits after the decimal point is more than enough to satisfy the judge.

## Worked Examples

### Example 1

Input:

```
6 1
```

For a single roll, the maximum is simply the roll itself.

| k | $(k/6)^1$ | $((k-1)/6)^1$ | Probability max = k | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1/6 | 0 | 1/6 | 1/6 |
| 2 | 2/6 | 1/6 | 1/6 | 2/6 |
| 3 | 3/6 | 2/6 | 1/6 | 3/6 |
| 4 | 4/6 | 3/6 | 1/6 | 4/6 |
| 5 | 5/6 | 4/6 | 1/6 | 5/6 |
| 6 | 6/6 | 5/6 | 1/6 | 6/6 |

Summing the contributions gives

$$\frac{1+2+3+4+5+6}{6} = 3.5.$$

This confirms that the formula reduces to the ordinary average when only one throw is made.

### Example 2

Input:

```
2 2
```

| k | $(k/2)^2$ | $((k-1)/2)^2$ | Probability max = k | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1/4 | 0 | 1/4 | 0.25 |
| 2 | 1 | 1/4 | 3/4 | 1.50 |

The final answer is

$$0.25 + 1.50 = 1.75.$$

This example demonstrates how cumulative probabilities are converted into exact probabilities for each possible maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m)$ | One iteration for every possible maximum value |
| Space | $O(1)$ | Only a few floating-point variables are stored |

With `m ≤ 100000`, the algorithm performs only one hundred thousand iterations. This is easily fast enough for the time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        m, n = map(int, input().split())

        ans = 0.0
        for k in range(1, m + 1):
            ans += k * ((k / m) ** n - ((k - 1) / m) ** n)

        return "{:.12f}".format(ans)

    return solve()

# provided sample
assert run("6 1\n") == "3.500000000000", "sample"

# minimum size
assert run("1 1\n") == "1.000000000000", "single face, single roll"

# single-face die
assert run("1 100000\n") == "1.000000000000", "maximum always equals 1"

# small hand-checkable case
assert run("2 2\n") == "1.750000000000", "enumerable probability check"

# another boundary-style case
out = float(run("2 1\n"))
assert abs(out - 1.5) < 1e-12, "ordinary average of a two-faced die"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1.000000000000` | Smallest possible input |
| `1 100000` | `1.000000000000` | Degenerate die with one face |
| `2 2` | `1.750000000000` | Correct conversion from cumulative probabilities |
| `2 1` | `1.500000000000` | Single-roll behavior |

## Edge Cases

Consider the input

```
1 100000
```

The loop runs only for `k = 1`.

$$(1/1)^{100000}=1, \qquad (0/1)^{100000}=0.$$

The probability that the maximum equals `1` is `1`, so the contribution is

$$1 \cdot 1 = 1.$$

The algorithm outputs exactly `1`.

Consider the input

```
6 1
```

For every `k`, the probability difference becomes

$$\frac{k}{6}-\frac{k-1}{6} = \frac16.$$

Every face contributes with equal probability, producing the standard average of a fair die. The output is `3.5`.

Consider the input

```
2 2
```

The cumulative probabilities are

$$P(\max \le 1)=\left(\frac12\right)^2=\frac14,$$

$$P(\max \le 2)=1.$$

Subtracting consecutive values yields probabilities `1/4` and `3/4` for maxima `1` and `2`. Summing weighted contributions gives `1.75`, exactly matching the true distribution of the maximum.
