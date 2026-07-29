---
title: "CF 102769A - A Greeting from Qinhuangdao"
description: "The problem describes a collection of red and blue balls. There are r red balls and b blue balls, and two balls are selected uniformly at random without replacement."
date: "2026-07-30T04:20:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102769
codeforces_index: "A"
codeforces_contest_name: "2020 China Collegiate Programming Contest Qinhuangdao Site"
rating: 0
weight: 102769
solve_time_s: 61
verified: true
draft: false
---

[CF 102769A - A Greeting from Qinhuangdao](https://codeforces.com/problemset/problem/102769/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a collection of red and blue balls. There are `r` red balls and `b` blue balls, and two balls are selected uniformly at random without replacement. We need to compute the probability that both selected balls are red, then print that probability as a reduced fraction. The output format also requires a case number before each answer.

The total number of ways to choose two balls from all available balls is the number of pairs among `r + b` objects, which is `C(r+b, 2)`. The favorable choices are pairs containing only red balls, which gives `C(r, 2)`. The required probability is the ratio between these two quantities.

The constraints are small: each color count is at most 100 and there are at most 10 test cases. This means even direct combinatorial calculations are easily fast enough. There is no need for advanced probability techniques or large precomputation. The main challenge is not performance but avoiding mistakes when reducing the fraction and handling special values correctly.

A few cases are easy to mishandle. When there is only one red ball, choosing two red balls is impossible. For input:

```
1
1 5
```

the answer is `Case #1: 0/1`. A careless implementation might calculate `1 * 0 / 2 = 0` correctly but forget that the reduced denominator must still be positive and nonzero.

Another case is when all balls are red. For input:

```
1
5 0
```

the probability is exactly 1 because every possible pair is red. The reduced answer must be `1/1`, not something like `10/10`.

The last common mistake is using ordered selections instead of unordered pairs. For example:

```
1
2 1
```

There is one favorable pair, the two red balls, and three total pairs. The answer is `1/3`. Counting ordered draws gives `2 / 6`, which is mathematically equal but requires proper reduction before output.

## Approaches

The direct approach is to count the number of possible pairs and the number of successful pairs. Since choosing two objects ignores order, the total number of selections is:

$$\binom{r+b}{2}=\frac{(r+b)(r+b-1)}{2}$$

and the successful selections are:

$$\binom{r}{2}=\frac{r(r-1)}{2}$$

The probability is the first value divided by the second. This method is already optimal because the input values are tiny. A brute-force simulation could try every pair of balls, check whether both are red, and count the results. That would still be correct, but it creates unnecessary work. With 200 balls, checking all pairs means about 20,000 operations per test case, which is acceptable here but ignores the mathematical structure.

The observation that all pairs are equally likely lets us replace simulation with counting. Once we know the number of favorable pairs and total pairs, the probability is just a fraction. We only need to divide the numerator and denominator by their greatest common divisor to produce the required irreducible form.

The brute-force works because it directly models every possible selection, but the counting formula works because every pair has identical probability and the number of possible pairs has a closed form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r+b)^2) | O(1) | Accepted for these limits, but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and process each pair of ball counts independently.
2. Compute the number of successful selections. Two red balls can be chosen in `r * (r - 1) / 2` ways because the order of the chosen balls does not matter.
3. Compute the total number of possible selections. Any two balls among all `r + b` balls can be chosen, giving `(r + b) * (r + b - 1) / 2` possibilities.
4. Find the greatest common divisor of the favorable count and total count. Divide both values by this gcd so the fraction is reduced.
5. Print the reduced fraction using the required case numbering format.

The division by the gcd is necessary because the problem asks for an irreducible fraction. The probability itself does not change when numerator and denominator are divided by the same value.

Why it works: every possible pair of balls has the same probability of being selected. The numerator counts exactly the pairs that contain two red balls, while the denominator counts every possible pair. Their ratio is exactly the required probability. Reducing by the greatest common divisor only changes the representation of the fraction, not its value, so the final output is mathematically equivalent and irreducible.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for case in range(1, t + 1):
        r, b = map(int, input().split())

        numerator = r * (r - 1) // 2
        denominator = (r + b) * (r + b - 1) // 2

        g = gcd(numerator, denominator)
        numerator //= g
        denominator //= g

        ans.append(f"Case #{case}: {numerator}/{denominator}")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution follows the counting approach directly. `numerator` stores the number of successful choices, and `denominator` stores all possible choices.

The multiplication is done before division because the combination formula requires the product of the two consecutive values. The values are small enough that integer overflow is not a concern in Python.

The gcd operation also handles the special cases naturally. If the numerator is zero, the gcd of zero and the denominator is the denominator itself, so the result becomes `0/1`. If the numerator and denominator are equal, the gcd reduces the fraction to `1/1`.

## Worked Examples

For input:

```
1
2 1
```

the execution is:

| Step | r | b | Red pairs | Total pairs | gcd | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 2 | 1 | 1 | 3 | 1 | 1/3 |
| Reduced | 2 | 1 | 1 | 3 | 1 | 1/3 |

There is exactly one pair containing two red balls, while the three possible pairs are `{red, red}`, `{red, blue}`, and `{red, blue}`. The calculation confirms that the probability is `1/3`.

For input:

```
1
8 8
```

the execution is:

| Step | r | b | Red pairs | Total pairs | gcd | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 8 | 8 | 28 | 120 | 4 | 7/30 |
| Reduced | 8 | 8 | 7 | 30 | 1 | 7/30 |

The fraction reduction step is visible here. The raw probability is `28/120`, but dividing by the gcd gives the required irreducible form `7/30`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case uses a fixed number of arithmetic operations and one gcd computation |
| Space | O(1) | Only a few integer variables are stored besides the output list |

With at most 10 test cases and values no larger than 100, this solution runs far below the limits.

## Test Cases

```python
import sys
import io
from math import gcd

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for case in range(1, t + 1):
        r, b = map(int, input().split())

        num = r * (r - 1) // 2
        den = (r + b) * (r + b - 1) // 2

        g = gcd(num, den)
        out.append(f"Case #{case}: {num // g}/{den // g}")

    print("\n".join(out))

assert run("""3
1 1
2 1
8 8
""") == """Case #1: 0/1
Case #2: 1/3
Case #3: 7/30
""", "samples"

assert run("""1
1 100
""") == """Case #1: 0/1
""", "one red ball"

assert run("""1
100 0
""") == """Case #1: 1/1
""", "all red balls"

assert run("""1
3 3
""") == """Case #1: 1/5
""", "balanced small case"

assert run("""1
100 100
""") == """Case #1: 99/398
""", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100` | `0/1` | No possible pair of red balls |
| `100 0` | `1/1` | Probability of certainty |
| `3 3` | `1/5` | Fraction reduction with equal colors |
| `100 100` | `99/398` | Maximum allowed values |

## Edge Cases

For the case with only one red ball:

```
1
1 5
```

the algorithm computes `1 * 0 / 2 = 0` successful pairs. The total number of pairs is positive, so the fraction becomes `0/6`, and gcd reduction changes it to `0/1`.

For the case where every ball is red:

```
1
5 0
```

the favorable count and total count are both `10`. The gcd is `10`, producing `1/1`. This avoids printing an unreduced probability.

For the case where order is incorrectly counted:

```
1
2 1
```

the correct model counts unordered pairs. There is one successful pair and three total pairs. The algorithm never distinguishes between drawing the first red then the second red and drawing the second red then the first red, so it matches the selection process described by the problem.
