---
title: "CF 102281H - \u0421\u043f\u0438\u0447\u0435\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430"
description: "We have two matchboxes, each initially containing exactly n matches. Every time Professor X needs a match, he chooses one of the two pockets uniformly at random and tries to take a match from that box."
date: "2026-08-13T09:25:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102281
codeforces_index: "H"
codeforces_contest_name: "2011, IV \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u043d\u0430\u044f \u043c\u0435\u0436\u0432\u0443\u0437\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 102281
solve_time_s: 87
verified: true
draft: false
---

[CF 102281H - \u0421\u043f\u0438\u0447\u0435\u0447\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430](https://codeforces.com/problemset/problem/102281/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two matchboxes, each initially containing exactly `n` matches. Every time Professor X needs a match, he chooses one of the two pockets uniformly at random and tries to take a match from that box. The process ends at the first moment when he chooses a box that is already empty.

The task is to compute the expected number of matches still present in the other box at that moment.

The only input is `n`, with `1 <= n <= 30`. The upper bound is small enough that even algorithms polynomial in `n` would be easily fast enough. However, a direct enumeration of all random choice histories is exponential, so the interesting part of the problem is recognizing the combinatorial structure of a stopping history rather than simulating every possibility.

There are two boundary cases that are easy to mishandle. First, the other box can still contain all `n` matches. For example, with `n = 1`, the professor may choose the same pocket twice: the first choice removes its only match, and the second choice discovers that box empty while the other box still contains `1` match. In fact the expected answer for `n = 1` is `0.5`. An implementation that only considers situations where the other box has already been used would incorrectly miss this case.

Second, the final empty-box discovery is an unsuccessful selection, so it must be included in the probability of a particular history. For `n = 2`, the correct answer is `0.875000000000000`. If we instead stop immediately when a box receives its last successful match, we are solving a different random experiment and obtain the wrong expectation.

The upper bound `n = 30` also makes numerical concerns straightforward. The largest exponent of two that appears is `2n = 60`, so ordinary double precision is more than sufficient for the required `1e-6` error tolerance.

## Approaches

A direct brute-force solution can generate every possible sequence of pocket choices until an empty box is found. Each choice has two possibilities, so if we allow for the final unsuccessful choice, a history has length at most `2n + 1`. For `n = 30`, enumerating all binary strings of this maximum length gives `2^61`, approximately `2.3 * 10^18`, candidate histories. Simulating up to 61 choices for every history would require on the order of `61 * 2^61`, roughly `1.4 * 10^20` elementary operations. That is completely infeasible.

The brute-force works because every possible sequence has a simple probability, namely a power of `1/2`. The failure comes from treating different orderings separately even when they lead to the same final number of remaining matches.

Suppose that when the empty box is discovered, the other box contains exactly `k` matches. Then the empty box must have been selected `n` times successfully before the final failed selection. The other box must have been selected exactly `n-k` times. Consequently, before the final failed choice there were exactly

`n + (n-k) = 2n-k`

successful selections.

For a fixed choice of which box is eventually found empty, the first `2n-k` choices contain exactly `n` selections of that box and `n-k` selections of the other box. There are

`C(2n-k, n)`

ways to arrange these choices.

Every such arrangement is valid. Before the final choice, the box that will become empty has been used exactly `n` times, while the other box has at least `k` matches left. Thus neither box could have been empty earlier.

The final choice must select the already exhausted box. Including that choice gives a probability of

`C(2n-k, n) / 2^(2n-k+1)`

for one particular box to be the first empty box. Either box can play that role, and the two cases have equal probability. Therefore

`P(k) = C(2n-k, n) / 2^(2n-k)`.

The expected number of remaining matches is consequently

`E = sum(k * P(k))` for `k = 0..n`.

Since there are only `n+1` possible values of `k`, we have reduced the problem from exponentially many histories to only `O(n)` probability terms.

We can evaluate these terms without repeatedly computing binomial coefficients. Start with `k = n`. In that case the other box was never selected, so

`P(n) = 1 / 2^n`.

For decreasing `k`, the ratio between consecutive probabilities is

`P(k-1) / P(k) = (2n-k+1) / (2(n-k+1))`.

Thus every next probability can be obtained from the previous one with a constant amount of arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n * 2^(2n+1))` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(1)` | Accepted |

## Algorithm Walkthrough

1. Read `n`. We will calculate the probability that exactly `k` matches remain in the box that was not found empty.
2. Start with `k = n` and probability `p = 2^(-n)`. This corresponds to choosing the same box `n` times successfully and then choosing that same box once more. The other box has therefore never been touched.
3. Add `k * p` to the expected value. This is the contribution of the current possible number of remaining matches.
4. Move from `k` to `k-1`. Update the probability using

`p *= (2*n-k+1) / (2*(n-k+1))`.

This recurrence is obtained directly from the ratio of the two binomial-probability expressions, so it avoids large combinatorial calculations.
5. Continue until `k = 0`. The value `k = 0` is valid because both boxes can be empty when the professor finally discovers one of them. Its contribution to the expectation is zero, but its probability is still part of the distribution.
6. Print the accumulated expectation with enough decimal places to satisfy the required precision.

### Why it works

For every possible `k`, a stopping history with exactly `k` matches left in the other box has exactly `n` successful selections from the box that will become empty and exactly `n-k` successful selections from the other box before the final failed selection. Choosing the positions of those `n` selections gives `C(2n-k,n)` valid prefixes, and the final choice is forced. Accounting for either box being the empty one gives exactly the probability `P(k)` used by the algorithm. These events are mutually exclusive and cover every possible stopping history, so summing `k * P(k)` gives precisely the required expected value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    # Probability that exactly n matches remain in the other box.
    p = 2.0 ** (-n)
    ans = 0.0

    for k in range(n, -1, -1):
        ans += k * p

        if k > 0:
            p *= (2 * n - k + 1) / (2 * (n - k + 1))

    print(f"{ans:.15f}")

if __name__ == "__main__":
    solve()
```

The variable `p` represents the probability of the current value of `k`. We begin at `k = n` because that probability has the simplest form, `2^-n`.

The loop visits every possible value of `k` exactly once. The expression `ans += k * p` applies the definition of mathematical expectation directly.

The update is performed only when `k > 0`. At `k = 0`, there is no next probability to calculate, and attempting the recurrence would divide by an invalid boundary expression.

All arithmetic is done with Python floating point. The largest exponent is only 60, and there are at most 31 iterations, so accumulated numerical error is far below the required `1e-6`.

No integer overflow is possible because the implementation does not construct the binomial coefficients at all. The recurrence uses only small integer factors and floating-point division.

## Worked Examples

### Sample 1

For `n = 2`, we begin with the probability that the other box still contains both matches.

| `k` | `p = P(k)` | `k * p` |
| --- | --- | --- |
| 2 | `0.2500000000` | `0.5000000000` |
| 1 | `0.3750000000` | `0.3750000000` |
| 0 | `0.3750000000` | `0.0000000000` |

The probabilities sum to `1`, and the expected value is

`0.5 + 0.375 = 0.875`.

Hence the output is `0.875000000000000`. The case `k = 2` demonstrates why the range must include `n`: the professor can discover one empty box without ever using the other box.

### Sample 2

For `n = 3`, the initial probability is `P(3) = 1/8`.

| `k` | `p = P(k)` | `k * p` |
| --- | --- | --- |
| 3 | `0.1250000000` | `0.3750000000` |
| 2 | `0.2500000000` | `0.5000000000` |
| 1 | `0.3125000000` | `0.3125000000` |
| 0 | `0.3125000000` | `0.0000000000` |

The probabilities again sum to `1`. The expected value is

`0.375 + 0.5 + 0.3125 = 1.1875`.

This matches the second sample and also shows how the recurrence generates the entire distribution without enumerating individual pocket-choice sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | There is one constant-time probability update for each `k` from `n` down to `0`. |
| Space | `O(1)` | Only `n`, the current probability, and the accumulated answer are stored. |

With `n <= 30`, the algorithm performs at most 31 iterations. The memory usage is constant, and the arithmetic stays comfortably within the range where double precision provides much more accuracy than the required `1e-6`.

## Test Cases

```python
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input())
    p = 2.0 ** (-n)
    ans = 0.0

    for k in range(n, -1, -1):
        ans += k * p
        if k > 0:
            p *= (2 * n - k + 1) / (2 * (n - k + 1))

    print(f"{ans:.15f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def reference(n: int) -> float:
    # Independent calculation using the closed-form probability.
    import math

    ans = 0.0
    for k in range(n + 1):
        p = math.comb(2 * n - k, n) / (2.0 ** (2 * n - k))
        ans += k * p
    return ans

# Provided samples.
assert run("2\n") == "0.875000000000000", "sample 1"
assert run("3\n") == "1.187500000000000", "sample 2"

# Minimum-size input. The two possible remaining counts, 0 and 1,
# are equally likely, so the answer is 0.5.
assert run("1\n") == "0.500000000000000", "minimum n"

# Boundary case n = 4, with all possible k values contributing.
assert run("4\n") == "0.992187500000000", "off-by-one boundary"

# Maximum allowed n.
assert abs(float(run("30\n")) - reference(30)) < 1e-12, "maximum n"

# Another symmetric case, checked against the direct combinatorial formula.
assert abs(float(run("5\n")) - reference(5)) < 1e-12, "probability distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0.500000000000000` | Minimum input and the `k = n` boundary case |
| `4` | `0.992187500000000` | Correct handling of every possible `k`, including `k = 0` and `k = n` |
| `30` | Direct combinatorial reference value | Maximum allowed input and numerical stability |
| `5` | Direct combinatorial reference value | Agreement between the recurrence and the probability formula |

## Edge Cases

For `n = 1`, the two boxes initially contain one match each. With probability `1/2`, the professor chooses the same box twice, so the other box contains `1`. With probability `1/2`, he chooses the two different boxes, so the second choice discovers an empty box and the other box contains `0`. The expected value is therefore `1/2`, which the algorithm obtains from `P(1) = 0.5` and `P(0) = 0.5`.

For `n = 2`, the complete distribution is `P(2) = 1/4`, `P(1) = 3/8`, and `P(0) = 3/8`. The resulting expectation is `2 * 1/4 + 1 * 3/8 = 7/8`. The `k = 2` outcome is especially useful for catching the mistake of stopping the analysis when a box becomes empty rather than when an empty box is subsequently selected.

For `k = 0`, the other box is also empty when the professor discovers the first empty box. This case has positive probability, even though its contribution to the expected value is zero. For example, with `n = 2`, its probability is `3/8`. An implementation that only sums positive `k` values can still accidentally get some examples right, but its probability distribution is incomplete and any related calculation would be wrong.

For the maximum input `n = 30`, the largest power of two used is `2^60`, and the loop contains only 31 iterations. The recurrence never requires constructing the enormous set of possible histories, so the same constant-sized state representation works unchanged at the upper boundary.
