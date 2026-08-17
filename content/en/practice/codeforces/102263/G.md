---
title: "CF 102263G - Card Game"
description: "Both players start with the same set of cards, containing every integer from 1 through n. During the n turns, every card is used exactly once by each player because chosen cards are removed."
date: "2026-08-17T20:02:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "G"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 126
verified: true
draft: false
---

[CF 102263G - Card Game](https://codeforces.com/problemset/problem/102263/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

Both players start with the same set of cards, containing every integer from 1 through `n`. During the `n` turns, every card is used exactly once by each player because chosen cards are removed. The two players effectively produce independent random permutations of the cards, and turn `i` compares the cards occupying position `i` in those permutations.

Ehab earns points whenever his card is larger than Zeyad's card. If Ehab plays `k` against a smaller card, he receives exactly `k` points. Equal cards give no points.

The input contains only `n`, with `1 <= n <= 10^6`. The large upper bound rules out anything quadratic in `n`. Even an `O(n^2)` computation would require `10^12` iterations at the maximum size, far beyond what a normal competitive programming time limit can support. We need to reduce the entire game to a constant amount of arithmetic.

The first edge case is `n = 1`. Both players have only card `1`, so they must play it against each other and nobody scores. The correct output is `0`.

The second edge case is a small deck such as `n = 2`. Ehab has cards `1` and `2`. Card `1` can never score, while card `2` scores exactly when it is paired with `1`. Since the opponent's card paired with `2` is equally likely to be `1` or `2`, its expected contribution is `2 * 1/2 = 1`. Thus the correct answer is `1`. A careless solution that assumes every card always scores against something smaller would incorrectly count `1 + 2 = 3`.

A third subtle case is equality. When both players choose the same number, neither player receives points. Since every card appears exactly once in each deck, equality is possible in the random pairing. Any formula that counts all opponents with value at most `k` instead of strictly less than `k` introduces an error.

## Approaches

A direct approach can calculate the expected contribution of every Ehab card separately. For a card `k`, we could inspect all `n` possible cards that Zeyad might play against it, determine whether `k` wins, and average the resulting scores. Doing this for all `k` requires exactly `n^2` pair checks. At `n = 10^6`, that is `10^12` operations, so even though the calculation is mathematically correct, it is far too slow.

We can do much better by looking at one card in isolation. Because Zeyad's deck is a uniformly random permutation, the card paired with Ehab's card `k` is uniformly distributed among all `n` cards. There are exactly `k - 1` cards smaller than `k`, and Ehab scores `k` precisely when one of those cards is paired with him.

So the probability that card `k` scores is simply

n k−1 ​ .

Its expected contribution is consequently

k n k−1 ​ .

Linearity of expectation now removes the need to reason about dependencies between different turns. We can add the expected contribution of every Ehab card even though the events involving different cards are not independent.

The total expectation is

E= k=1 ∑ n ​ k n k−1 ​ = n 1 ​ k=1 ∑ n ​ (k 2 −k).

Using the standard sums

k=1 ∑ n ​ k 2 = 6 n(n+1)(2n+1) ​

and

k=1 ∑ n ​ k= 2 n(n+1) ​ ,

we obtain

E= n 1 ​ ( 6 n(n+1)(2n+1) ​ − 2 n(n+1) ​ ).

Factoring and simplifying gives

E= 3 n 2 −1 ​ .

Thus the entire random game can be replaced by one constant-time formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, which determines the complete set of cards in both decks.
2. Consider an arbitrary Ehab card `k`. The opponent's card paired with it is uniformly distributed over all `n` possible cards because the two random permutations are independent.
3. Count the cards that let Ehab score with `k`. Exactly `k - 1` cards have values smaller than `k`, so the probability of scoring with this card is `(k - 1) / n`.
4. Multiply that probability by the number of points earned when the card scores. The expected contribution of `k` is `k * (k - 1) / n`.
5. Sum these contributions over every `k` from `1` through `n`. By linearity of expectation, we may add expected contributions without requiring the individual turns to be independent.
6. Simplify the resulting sum to obtain `(n² - 1) / 3`, then print it as a real number.

### Why it works

For every fixed card `k`, exactly `k - 1` of the opponent's `n` cards cause Ehab to score `k` points. Since every possible opponent card is equally likely to be paired with `k`, its expected contribution is exactly `k(k-1)/n`. Every card in Ehab's deck is used exactly once, so the total score is the sum of these individual contributions. Linearity of expectation guarantees that this sum equals the expected total score regardless of any dependence between the pairings. Algebra reduces that sum to `(n² - 1)/3`, so the algorithm computes the exact expectation.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline
n = int(input())
answer = (n * n - 1) / 3.0print(f"{answer:.10f}")
```

The input contains only one integer, so there is no need for additional data structures or repeated test-case handling.

The expression `n * n - 1` comes directly from the simplified expectation. Python integers have arbitrary precision, so there is no integer overflow even at `n = 10^6`.

The division by `3.0` produces a floating-point result suitable for the required output tolerance. Printing ten digits after the decimal point gives considerably more precision than the required `10^-6`.

The subtraction must happen before division. For `n = 1`, the expression becomes `(1 * 1 - 1) / 3 = 0`, correctly handling the smallest possible deck.

## Worked Examples

The first sample corresponds to `n = 3`.

| Card `k` | Smaller opponent cards | Scoring probability | Expected contribution |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 1 | 1/3 | 2/3 |
| 3 | 2 | 2/3 | 2 |

Adding the contributions gives

0+ 3 2 ​ +2= 3 8 ​ =2.6666666667.

This demonstrates that the largest card contributes most of the expected score, while the smallest card contributes nothing because it cannot beat any card.

The second sample corresponds to `n = 7`.

| Card `k` | Smaller opponent cards | Scoring probability | Expected contribution |
| --- | --- | --- | --- |
| 1 | 0 | 0/7 | 0 |
| 2 | 1 | 1/7 | 2/7 |
| 3 | 2 | 2/7 | 6/7 |
| 4 | 3 | 3/7 | 12/7 |
| 5 | 4 | 4/7 | 20/7 |
| 6 | 5 | 5/7 | 30/7 |
| 7 | 6 | 6/7 | 42/7 |

The sum is

7 2+6+12+20+30+42 ​ = 7 112 ​ =16.

The simplified formula gives the same result immediately:

3 7 2 −1 ​ = 3 48 ​ =16.

The table also makes the probability interpretation concrete. For card `7`, any of the other six cards makes Ehab score, while playing against another `7` produces no points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations are performed. |
| Space | O(1) | Only `n` and the resulting value are stored. |

The maximum `n` is `10^6`, but the algorithm does not iterate over the cards at all. Its running time and memory usage stay constant regardless of `n`, making it comfortably suitable for the given constraint.

## Test Cases

```python
Python# helper: run solution on input string, return output stringimport sysimport io
def solve(inp: str) -> str:    data = inp.strip().split()    n = int(data[0])    answer = (n * n - 1) / 3.0    return f"{answer:.10f}\n"
def run(inp: str) -> str:    return solve(inp)
# provided samplesassert run("3\n") == "2.6666666667\n", "sample 1"assert run("7\n") == "16.0000000000\n", "sample 2"
# minimum-size inputassert run("1\n") == "0.0000000000\n", "only equal cards"
# n = 2, catches incorrect handling of equalityassert run("2\n") == "1.0000000000\n", "two-card deck"
# n = 4, checks the formula on a small nontrivial caseassert run("4\n") == "5.0000000000\n", "small general case"
# maximum-size inputassert run("1000000\n") == "333333333333.0000000000\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0.0000000000` | Minimum deck and equality |
| `2` | `1.0000000000` | Strictly smaller opponent condition |
| `4` | `5.0000000000` | General formula on a small deck |
| `1000000` | `333333333333.0000000000` | Maximum boundary and arithmetic range |

## Edge Cases

For `n = 1`, the input is simply `1`. The only possible pairing is card `1` against card `1`. Since equal cards do not score, the expected result is `0`. The formula produces `(1² - 1) / 3 = 0`, so there is no special case required.

For `n = 2`, the cards are `1` and `2`. Card `1` has zero smaller cards, giving an expected contribution of `0`. Card `2` has one smaller opponent out of two possible opponents, so its contribution is `2 * 1/2 = 1`. The final answer is `1`. This catches implementations that accidentally treat equality as a win.

For `n = 3`, the contributions are `0`, `2/3`, and `2`, giving `8/3 = 2.6666666667`. This checks the transition from integer to fractional expected values and catches off-by-one errors in the count of smaller cards.

For `n = 10^6`, the formula gives

3 10 12 −1 ​ =333333333333.

The result is large, but Python's arbitrary-precision integers handle the intermediate multiplication exactly. No loop, array, or simulation is needed even at the maximum input size.
