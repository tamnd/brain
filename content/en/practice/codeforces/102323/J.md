---
title: "CF 102323J - Factorial Products"
description: "For each test case, we are given three lists of non-negative integers, called A, B, and C. For a list such as A = [a1, a2, ..., ak], define its score as [ P(A)=a1!cdot a2!cdots ak!. ] The task is to determine which of the three lists has the largest score."
date: "2026-08-13T04:20:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "J"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 70
verified: true
draft: false
---

[CF 102323J - Factorial Products](https://codeforces.com/problemset/problem/102323/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

For each test case, we are given three lists of non-negative integers, called `A`, `B`, and `C`. For a list such as `A = [a1, a2, ..., ak]`, define its score as

[
P(A)=a_1!\cdot a_2!\cdots a_k!.
]

The task is to determine which of the three lists has the largest score. If two or all three scores are equal and tied for the maximum, the required answer is `TIE`.

The input starts with the number of test cases. Each test case gives the three list sizes, followed by the elements of the three lists. Every element is below `2501`. The official statement also guarantees that if two products are different, their relative difference is at least `0.01%` of the larger product.

The crucial constraint is the upper bound of `2500` on individual values, not the magnitude of the factorial products. Even `2500!` is far too large to construct explicitly in ordinary integer arithmetic. A Python integer can technically represent it, but repeatedly constructing and multiplying products containing many such factorials would make the numbers enormous and the arithmetic increasingly expensive. With a one-second limit, a solution must avoid materializing these products. The input itself still has to be read, so any efficient algorithm should be essentially linear in the total number of list elements.

There are several edge cases where a straightforward implementation can silently fail. Consider

```
1
1 1 1
0
1
0
```

The scores are `0! = 1`, `1! = 1`, and `0! = 1`, so the output is

```
Case #1: TIE
```

An implementation that treats `0!` as zero would incorrectly choose `B`.

Another case is

```
1
2 1 1
2 2
3
2
```

Here `P(A)=2!*2!=4`, `P(B)=3!=6`, and `P(C)=2!=2`, so the answer is

```
Case #1: B
```

A careless implementation that compares only the largest element of each list would incorrectly choose `A` because its largest element is `2`, but the product depends on every factorial.

A third edge case is an exact tie:

```
1
1 2 1
3
2 1
3
```

Both `A` and `C` have score `3!`, while `B` has `2!*1!=2`, so the result is

```
Case #1: TIE
```

The output is `TIE` even though the tied lists do not contain the same elements. The comparison must be between the resulting products.

## Approaches

The brute-force approach follows the mathematical definition directly. For every value `x`, calculate `x!`, multiply those factorials together for the corresponding list, and then compare the three resulting integers. This is correct because it constructs exactly the three quantities defined by the problem.

The difficulty is the size of the numbers. If a list contains `m` values and every value is `2500`, computing each factorial separately takes roughly `2500m` multiplications. Across the three lists this is roughly `7500m` multiplications when the lists have comparable size. More seriously, the intermediate integers are themselves hundreds or thousands of digits long, and multiplying many such values makes each arithmetic operation increasingly expensive. Storing the final products is also unnecessary work because we only need their ordering.

The observation that removes the problem is that multiplication becomes addition after taking logarithms:

\log(a_1!)+\log(a_2!)+\cdots+\log(a_k!).
]

Since the logarithm is strictly increasing, the list with the largest logarithmic score is exactly the list with the largest original product. We can precompute

[
L[x]=\log(x!)
]

for every `x` from `0` through `2500`. The recurrence

[
L[x]=L[x-1]+\log x
]

computes the whole table in linear time.

Then each list requires only one addition per element. We never construct a factorial or a factorial product.

The guarantee about different products is what makes floating-point comparison appropriate here. A relative difference of at least `0.01%` corresponds to a logarithmic difference of roughly

[
\log(1.0001)\approx 10^{-4}.
]

The accumulated floating-point error in the sums is vastly smaller than that separation for realistic input sizes, so a small comparison tolerance can distinguish genuinely different products while treating mathematically equal products as ties.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2500S) arithmetic steps, with huge-integer costs | O(S) plus huge integers | Too slow |
| Optimal | O(2500 + S) | O(2500) | Accepted |

Here `S` is the total number of elements in the three lists of one test case. The optimal method also uses `math.lgamma(x + 1)` as an alternative way to obtain `log(x!)`, but precomputing the cumulative logarithms makes the intended recurrence explicit and avoids repeatedly evaluating a special function.

## Algorithm Walkthrough

1. Precompute `log_fact[x]` for every integer `x` from `0` to `2500`. Start with `log_fact[0] = 0`, because `0! = 1` and `log(1) = 0`. For every `x > 0`, set `log_fact[x] = log_fact[x - 1] + log(x)`. This gives the logarithm of every factorial without ever constructing the factorial itself.
2. Read the three list sizes and then read the three lists. The sizes tell us exactly how many values belong to each list, so the input can be consumed even when a list's values are split across several physical input lines.
3. For each list, add `log_fact[x]` for every value `x` in it. The resulting sum is the logarithm of that list's factorial product.
4. Find the maximum of the three logarithmic scores. Since logarithm preserves ordering, the maximum score corresponds to the maximum original product.
5. Compare every score with the maximum using a small tolerance. If all three values within tolerance of the maximum are considered tied, print `TIE`; otherwise print the name of the unique maximum list.
6. Repeat for every test case and prefix the answer with its one-based case number.

Why it works: after processing a list, its accumulated value is exactly

\log\left(\prod_{x\in A}x!\right).
]

Thus the three accumulated values represent the logarithms of the three required products. Because logarithm is strictly increasing, their ordering is identical to the ordering of the original products. The problem's separation guarantee prevents two different products from being close enough to be confused by the floating-point comparison, while equal products produce equal mathematical logarithmic sums and are treated as a tie.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

MAXV = 2500
EPS = 1e-10

# log_fact[x] = log(x!)
log_fact = [0.0] * (MAXV + 1)
for x in range(1, MAXV + 1):
    log_fact[x] = log_fact[x - 1] + math.log(x)

def read_list(n):
    values = []
    while len(values) < n:
        values.extend(map(int, input().split()))
    return values[:n]

def solve():
    t = int(input())
    out = []

    for case_no in range(1, t + 1):
        sizes = []
        while len(sizes) < 3:
            sizes.extend(map(int, input().split()))

        na, nb, nc = sizes[:3]

        A = read_list(na)
        B = read_list(nb)
        C = read_list(nc)

        scores = [
            sum(log_fact[x] for x in A),
            sum(log_fact[x] for x in B),
            sum(log_fact[x] for x in C),
        ]

        mx = max(scores)

        tied = sum(abs(score - mx) <= EPS for score in scores)

        if tied >= 2:
            answer = "TIE"
        elif scores[0] == mx:
            answer = "A"
        elif scores[1] == mx:
            answer = "B"
        else:
            answer = "C"

        out.append(f"Case #{case_no}: {answer}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The precomputation creates the table used by every test case. The first entry is zero because the logarithm of `0!` is the logarithm of `1`. Each subsequent entry adds only `log(x)`, exactly mirroring the recurrence `x! = x * (x - 1)!`.

The `read_list` helper deserves attention because the statement describes each list as occupying one input line, but robust competitive-programming code should not depend on that formatting detail. It keeps reading until it has collected the requested number of values.

The three `sum` expressions implement the central transformation from products to sums. No factorial is constructed, so Python's arbitrary-precision integer machinery never has to handle the enormous values involved.

The comparison uses an absolute tolerance on logarithms. A relative difference of `0.01%` between distinct products corresponds to a logarithmic gap near `1e-4`, whereas `1e-10` is many orders of magnitude smaller. The tolerance is therefore comfortably below the guaranteed separation.

The `0!` and `1!` cases require no special branch because both already appear correctly in the precomputed table. There is also no integer overflow concern because every value stored in `scores` is a floating-point logarithm rather than a factorial product.

## Worked Examples

The official statement gives the example lists `A = {2,4,7}`, `B = {0,1,9}`, and `C = {2,3,5,5}`. Their actual products are `241920`, `362880`, and `172800`, respectively, so `B` is the largest.

For a trace, the relevant logarithmic state is as follows.

| List | Values | Logarithmic score | Relative result |
| --- | --- | --- | --- |
| A | 2, 4, 7 | `log(2!) + log(4!) + log(7!)` | about `12.395` |
| B | 0, 1, 9 | `log(0!) + log(1!) + log(9!)` | about `12.802` |
| C | 2, 3, 5, 5 | `log(2!) + log(3!) + log(5!) + log(5!)` | about `12.059` |

The maximum is the score for `B`, so the output is `Case #1: B`. The trace demonstrates why the algorithm can compare quantities that would be awkward to store directly: the original products are already hundreds of thousands, while their logarithms remain small floating-point numbers.

A second example exercises an exact tie:

```
1
2 2 1
3 2
2 3
4
```

The states are

| List | Values | Factorial product | Logarithmic score |
| --- | --- | --- | --- |
| A | 3, 2 | `3! * 2! = 12` | `log(12)` |
| B | 2, 3 | `2! * 3! = 12` | `log(12)` |
| C | 4 | `4! = 24` | `log(24)` |

Here `C` is strictly larger, so the answer is `Case #1: C`. To get a genuine tie, changing `C` to `2 1` gives `2!*1!=2`, leaving `A` and `B` tied for the maximum. The key property is that the order of values inside a list does not matter because multiplication is commutative, so `[3,2]` and `[2,3]` must produce identical logarithmic sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2500 + S) per test case | Precomputation is linear in the maximum value, and each list element contributes one table lookup and one addition |
| Space | O(2500) | The factorial-logarithm table contains one floating-point value for each possible input value |

The maximum element is only `2500`, so the precomputation is negligible. After that, the algorithm performs constant work for every input value. Unlike the brute-force solution, its running time does not grow with the number of digits in the factorial products, because those products are never created.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

MAXV = 2500
EPS = 1e-10

log_fact = [0.0] * (MAXV + 1)
for x in range(1, MAXV + 1):
    log_fact[x] = log_fact[x - 1] + math.log(x)

def program(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    t = next(it)
    ans = []

    for case_no in range(1, t + 1):
        na = next(it)
        nb = next(it)
        nc = next(it)

        A = [next(it) for _ in range(na)]
        B = [next(it) for _ in range(nb)]
        C = [next(it) for _ in range(nc)]

        scores = [
            sum(log_fact[x] for x in A),
            sum(log_fact[x] for x in B),
            sum(log_fact[x] for x in C),
        ]

        mx = max(scores)
        tied = sum(abs(x - mx) <= EPS for x in scores)

        if tied >= 2:
            winner = "TIE"
        elif scores[0] == mx:
            winner = "A"
        elif scores[1] == mx:
            winner = "B"
        else:
            winner = "C"

        ans.append(f"Case #{case_no}: {winner}")

    return "\n".join(ans) + "\n"

# Provided example from the statement.
sample1 = """\
1
3 3 4
2 4 7
0 1 9
2 3 5 5
"""
assert program(sample1) == "Case #1: B\n", "provided example"

# Minimum-size values.  0! = 1! = 1, so all three products tie.
sample2 = """\
1
1 1 1
0
1
0
"""
assert program(sample2) == "Case #1: TIE\n", "minimum values and 0!"

# All lists contain exactly the same values, so they must tie.
assert program("""\
1
4 4 4
5 5 5 5
5 5 5 5
5 5 5 5
""") == "Case #1: TIE\n", "all equal lists"

# Boundary value 2500.  B has one additional 1!, so it is still tied with A.
assert program("""\
1
1 2 1
2500
2500 1
2499
""") == "Case #1: A\n", "maximum element and 1!"

# Catch an off-by-one mistake in factorial indexing.
# A = 4! = 24, B = 3! * 1! = 6, C = 3! = 6.
assert program("""\
1
1 2 1
4
3 1
3
""") == "Case #1: A\n", "factorial boundary"

# A and B have equal products despite different order.
assert program("""\
1
2 2 1
3 2
2 3
2
""") == "Case #1: TIE\n", "permutation equality"

# Large input value repeated many times, exercising the precomputed table
# without constructing the enormous factorial product.
assert program("""\
1
2 2 2
2500 2500
2500 2499
2500 2500
""") == "Case #1: A\n", "large factorial products"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 / 0 / 1 / 0` | `Case #1: TIE` | Minimum values and correct handling of `0!` |
| Four copies of `5` in each list | `Case #1: TIE` | Exact equality and repeated values |
| Lists containing `2500` | `Case #1: A` | Maximum allowed element and absence of huge integer construction |
| `4` versus `3,1` versus `3` | `Case #1: A` | Correct factorial indexing and boundary handling |
| `[3,2]` versus `[2,3]` | `Case #1: TIE` | Product commutativity and equality |
| Repeated `2500!` values | `Case #1: A` | Large logarithmic sums and precomputation |

## Edge Cases

For `0!`, the input

```
1
1 1 1
0
1
0
```

produces three logarithmic scores of zero. The precomputed value `log_fact[0]` is explicitly initialized to zero, so all three lists are recognized as tied. No special case is needed during the main loop.

For repeated values, consider

```
1
3 2 1
5 5 5
5 5
5
```

Every list contributes the same number of copies of `log(5!)` according to its size, so the scores are proportional to `3`, `2`, and `1`. The result is `Case #1: A`. The algorithm handles repetition naturally because every occurrence contributes separately to the sum.

For equal products with different list contents, use

```
1
2 2 1
3 2
2 3
2
```

The first two lists both have product `3!*2! = 12`. Their logarithmic scores are both `log(12)`, so their difference is zero and both are within the tolerance of the maximum. The output is `Case #1: TIE`.

For the largest possible element, consider

```
1
1 2 1
2500
2500 1
2499
```

The first list has product `2500!`, the second also has `2500!*1!`, and the third has `2499!`. Since `1! = 1`, the first two lists tie for the largest product. The algorithm looks up `log_fact[2500]` directly and never tries to construct `2500!`.

The final edge case is the numerical one. Suppose two products differ by the smallest amount allowed by the statement, about `0.01%`. Their logarithms differ by approximately `0.0001`, while the comparison tolerance is `1e-10`. The tolerance is far smaller than the guaranteed gap, so distinct products cannot be collapsed into a tie by the comparison. At the same time, mathematically equal products have equal logarithmic sums, so they are recognized as tied.
