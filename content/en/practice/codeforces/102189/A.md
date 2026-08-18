---
title: "CF 102189A - \u041e\u0432\u043e\u0449\u0438"
description: "The dish contains two vegetables. The first contributes X mood units for every gram, and there are A grams of it. The second contributes Y mood units per gram, and there are B grams. The total mood change is simply the sum of the contributions from both vegetables: A X + B Y."
date: "2026-08-19T06:16:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102189
codeforces_index: "A"
codeforces_contest_name: "12-\u0439 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0432 \u0410\u0431\u0430\u043a\u0430\u043d\u0435"
rating: 0
weight: 102189
solve_time_s: 469
verified: true
draft: false
---

[CF 102189A - \u041e\u0432\u043e\u0449\u0438](https://codeforces.com/problemset/problem/102189/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The dish contains two vegetables. The first contributes `X` mood units for every gram, and there are `A` grams of it. The second contributes `Y` mood units per gram, and there are `B` grams. The total mood change is simply the sum of the contributions from both vegetables:

`A * X + B * Y`.

The first input line gives the amounts `A` and `B`, while the second gives the per-gram mood changes `X` and `Y`. The required output is one integer, the total change in mood after eating the entire dish. A negative answer means the mood decreases, while a positive answer means it increases.

The quantities `A` and `B` are at most `30000`, and `X` and `Y` lie between `-30000` and `30000`. Even the largest absolute contribution from one vegetable is `30000 * 30000 = 900000000`, so the total absolute result is at most `1800000000`. This fits in a signed 32-bit integer, although Python integers have no overflow problem anyway. More importantly, the constraints do not require any iteration, search, dynamic programming, or graph algorithm. A constant number of arithmetic operations is enough.

The main edge cases come from signed values rather than from the sizes of the inputs. For example, with

```
2 3
2 -1
```

the answer is `2 * 2 + 3 * (-1) = 1`. A careless implementation that treats `Y = -1` as a positive magnitude would produce `7`, losing the fact that the second vegetable decreases mood.

A second case is when both mood changes are negative:

```
1 1
-30000 -30000
```

The correct answer is `-60000`. The multiplication must preserve the signs of `X` and `Y`; taking absolute values before calculating would give the wrong result.

Zero is also a valid mood change. For

```
30000 30000
0 30000
```

the correct answer is `900000000`. The first vegetable contributes nothing, even though its amount is nonzero. Any implementation that assumes every vegetable changes mood would mishandle this case.

Finally, the largest values can produce a result close to the integer boundary:

```
30000 30000
30000 30000
```

The correct answer is `1800000000`. The calculation must be performed using an integer type capable of representing the full result.

## Approaches

A direct brute-force interpretation would process every gram separately. We could add `X` to the answer `A` times and then add `Y` to it `B` times. This is correct because every gram contributes independently, so after all grams have been processed the accumulator contains exactly the total mood change.

The problem is that this performs `A + B` additions. With both amounts equal to `30000`, that is `60000` iterations. In this particular problem, 60000 operations are still small enough to run comfortably within the one-second limit, so this brute-force version would actually be accepted. It is nevertheless unnecessary work and obscures the simple mathematical structure of the problem.

The key observation is that all `A` grams of the first vegetable have exactly the same contribution, `X`. Instead of adding `X` repeatedly, we can combine those identical contributions into the product `A * X`. The same reasoning gives `B * Y` for the second vegetable. Since the dish contains only these two kinds of vegetables, adding the two products gives the complete answer.

This turns the entire computation into two multiplications and one addition. The brute-force works because it explicitly sums every individual contribution, but fails to exploit the fact that many consecutive contributions are identical. Recognizing that repetition lets us replace the repeated additions with multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(A + B) | O(1) | Accepted, but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `A` and `B`, the amounts of the two vegetables. These values determine how many grams of each type contribute to the final mood change.
2. Read `X` and `Y`, the mood change caused by one gram of each vegetable. They may be positive, zero, or negative, so their signs must be preserved.
3. Compute `A * X`. This combines the identical contribution of all grams of the first vegetable into one multiplication.
4. Compute `B * Y` for the second vegetable for the same reason.
5. Add the two products and print the result. The two products account for every gram in the dish, so their sum is exactly the total mood change.

### Why it works

The contribution of the first vegetable is the sum of `X` repeated `A` times, which is exactly `A * X`. Similarly, the contribution of the second vegetable is `B * Y`. Every gram belongs to one of these two groups, so the total contribution is exactly `A * X + B * Y`. The algorithm computes this expression directly, meaning it cannot omit a gram or count one twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())
    X, Y = map(int, input().split())

    print(A * X + B * Y)

if __name__ == "__main__":
    solve()
```

The first input operation reads the two amounts, and the second reads the two per-gram mood changes. `map(int, ...)` is sufficient because all four values are integers, including negative values.

The expression `A * X + B * Y` is the complete mathematical solution. There are no loops, arrays, recursion, or special cases because ordinary signed integer arithmetic already handles positive, negative, and zero contributions correctly.

The order of operations is also straightforward. Each amount is multiplied by its corresponding per-gram effect before the two independent contributions are added. Python's arbitrary-precision integers make overflow impossible for these constraints, although the maximum result is already small enough to fit in a signed 32-bit integer.

## Worked Examples

### Sample 1

The input is:

```
2 3
2 -1
```

The algorithm computes the contribution from each vegetable separately.

| A | B | X | Y | A * X | B * Y | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | 2 | -1 | 4 | -3 | 1 |

The first vegetable raises the mood by `4`, while the second lowers it by `3`. Their combined effect is `1`.

### Sample 2

The input is:

```
1 1
1 -2
```

| A | B | X | Y | A * X | B * Y | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | -2 | 1 | -2 | -1 |

Each vegetable appears in exactly one gram. The first increases the mood by `1`, the second decreases it by `2`, giving a final change of `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs a fixed number of arithmetic operations. |
| Space | O(1) | Only the four input values and one result are stored. |

The constraints allow an extremely small constant-time solution. Even at the maximum values, the computation consists of only two multiplications and one addition, so both the time and memory limits are easily satisfied.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    A, B = map(int, input().split())
    X, Y = map(int, input().split())
    print(A * X + B * Y)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("2 3\n2 -1\n") == "1\n", "sample 1"
assert run("1 1\n1 -2\n") == "-1\n", "sample 2"

# Minimum amounts, both positive contributions
assert run("1 1\n1 1\n") == "2\n", "minimum-size positive case"

# Maximum amounts and maximum positive effects
assert run("30000 30000\n30000 30000\n") == "1800000000\n", "maximum values"

# Maximum amounts and maximum negative effects
assert run("30000 30000\n-30000 -30000\n") == "-1800000000\n", "minimum result"

# Zero contribution and mixed signs
assert run("30000 1\n0 -30000\n") == "-30000\n", "zero and negative contribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `2` | Minimum amounts and ordinary positive contributions |
| `30000 30000 / 30000 30000` | `1800000000` | Maximum bounds and largest positive result |
| `30000 30000 / -30000 -30000` | `-1800000000` | Negative values and the most negative result |
| `30000 1 / 0 -30000` | `-30000` | Zero contribution and mixed signs |

## Edge Cases

When one vegetable decreases mood, its contribution must remain negative. For

```
2 3
2 -1
```

the first product is `4` and the second is `-3`, so the result is `1`. The algorithm never takes an absolute value or otherwise changes the sign, so the negative effect is handled naturally.

When both effects are negative, the same formula still applies. For

```
1 1
-30000 -30000
```

the products are `-30000` and `-30000`, producing `-60000`. There is no separate branch for negative values because integer multiplication already applies the correct sign.

A zero effect is another case that requires no special branch. With

```
30000 30000
0 30000
```

the first product is `0`, and the second is `900000000`. The result is `900000000`. The algorithm correctly treats the first vegetable as having no influence on mood.

At the maximum positive boundary,

```
30000 30000
30000 30000
```

the products are both `900000000`, giving `1800000000`. The calculation uses the full input values without any off-by-one adjustment, because `A` grams contribute exactly `A` copies of `X`.

The same boundary works for the negative extreme:

```
30000 30000
-30000 -30000
```

Both products are `-900000000`, so the answer is `-1800000000`. This confirms that the implementation preserves signs and handles the complete permitted numeric range.
