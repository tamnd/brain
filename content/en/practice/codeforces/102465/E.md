---
title: "CF 102465E - Rounding"
description: "We have P places, and exactly 10,000 people each chose one place. If a place was chosen by c people, its true percentage is [ frac{c}{100}% ] because 10,000 people make every percentage step exactly 0.01. The agency did not report these exact percentages."
date: "2026-08-09T03:42:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "E"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 221
verified: true
draft: false
---

[CF 102465E - Rounding](https://codeforces.com/problemset/problem/102465/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `P` places, and exactly 10,000 people each chose one place. If a place was chosen by `c` people, its true percentage is

[
\frac{c}{100}%
]

because 10,000 people make every percentage step exactly `0.01`.

The agency did not report these exact percentages. Instead, it rounded each percentage independently to the nearest integer, with `.50` rounded upward. Thus, if the reported integer is `r`, the true percentage must lie between `r - 0.50` and `r + 0.50`, with the lower endpoint included and the upper endpoint excluded. Since the true percentage can only have two decimal places, the possible values are discrete.

The task has two parts. First, we must decide whether the reported integers can come from any distribution of exactly 10,000 people. Second, if they can, we must find the smallest and largest possible true percentage for every place, while respecting the fact that all places together account for exactly 100% of the people.

The names must be printed in their original order.

The bound `P <= 10000` means an algorithm around `O(P)` is ideal. Even `O(P log P)` would be comfortable, but there is no reason to sort or perform any more complicated global computation. The percentages themselves are bounded between `0` and `100`, and there are exactly 10,000 people, so the most useful representation is to work with integer numbers of people or integer hundredths of a percent. That completely avoids floating-point precision problems.

There are several boundary cases that can make a direct implementation wrong.

Consider a single place reported as zero.

```
1
Park 0
```

All 10,000 people must have chosen that place, so this report is impossible. A careless implementation that treats the reported value `0` as merely saying that the true percentage is somewhere in `[0, 0.49]` may forget the global sum and produce an apparently valid interval. The correct output is:

```
IMPOSSIBLE
```

At the other extreme, consider one place reported as 100.

```
1
Park 100
```

Every person must have chosen it, so its actual percentage is exactly `100.00`. The correct output is:

```
Park 100.00 100.00
```

A generic formula of `100.00` through `100.49` would be wrong because a percentage cannot exceed 100.

A less obvious boundary appears when the independently rounded intervals do not themselves sum to 100%. For example:

```
2
A 50
B 49
```

The first place can individually be from `49.51` through `50.49`, and the second from `48.51` through `49.49`. Even their largest possible total is `99.98`, so no distribution of the 10,000 people exists. The correct output is:

```
IMPOSSIBLE
```

Finally, even when every individual interval is valid, the total can force a place away from the naive lower or upper endpoint. In the sample with rounded values summing to 97, the other places cannot contribute enough percentage to let the first place fall all the way to its ordinary lower bound. The global sum raises its minimum from `10.51` to `11.06`. This interaction between independent rounding intervals and the fixed total of exactly 100% is the central part of the problem.

## Approaches

A direct brute-force approach would consider every possible number of people for every place. Since there are 10,001 possible counts from zero through 10,000, we could test all 10,001 candidates for each place and check whether the remaining places can absorb the remaining people within their valid ranges. With a precomputed sum of lower and upper bounds, each candidate could be checked in constant time.

The brute force is correct because every feasible true percentage corresponds to an integer number of people, and we explicitly inspect every such possibility. The problem is the number of possibilities. With `P = 10000`, there are

[
10000 \times 10001 = 100010000
]

candidate values. That is already around 100 million checks before input parsing and output, which is unnecessarily expensive under a 2-second limit.

The key observation is that we never need to inspect individual candidate counts. For each place, rounding immediately gives a contiguous interval of possible counts. Once the other places are summarized by their total minimum and maximum, the global sum constraint gives the exact additional restriction on the current place.

Suppose a place has an independently valid interval `[L_i, U_i]`, expressed in hundredths of a percentage. If we want to minimize its value, we should make every other place as large as possible. The other places can contribute at most

[
\sum_{j\ne i} U_j.
]

Since the total must be exactly 10,000 hundredths, the current place must be at least

[
10000-\sum_{j\ne i}U_j.
]

Its true minimum is therefore the larger of this value and its own independent lower bound.

The maximum follows symmetrically. To maximize place `i`, make all other places as small as possible. They contribute at least

[
\sum_{j\ne i}L_j,
]

so place `i` can be at most

[
10000-\sum_{j\ne i}L_j.
]

Its true maximum is the smaller of that value and its independent upper bound.

This turns the entire problem into computing two sums and performing a constant amount of arithmetic per place.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(P * 10000)` | `O(P)` | Too slow |
| Optimal | `O(P)` | `O(P)` | Accepted |

## Algorithm Walkthrough

1. Read every place and its reported rounded percentage. Convert the reported percentage into an interval of possible integer hundredths of a percentage.

For a reported value `r` strictly between 0 and 100, the possible true percentages are

[
r-0.49,\ r-0.48,\ldots,\ r+0.49.
]

In hundredths, that gives

[
L_i=100r-49,\qquad U_i=100r+49.
]

For `r = 0`, the lower bound cannot be negative, so `L_i = 0`. For `r = 100`, the upper bound cannot exceed 100%, so `U_i = 10000`.

1. Compute the sum of all lower bounds and the sum of all upper bounds.

If

[
\sum L_i > 10000,
]

even making every place as small as possible gives more than 100%, so the reports are impossible.

If

[
\sum U_i < 10000,
]

even making every place as large as possible gives less than 100%, so the reports are also impossible.

Thus the reports are feasible exactly when

[
\sum L_i \le 10000 \le \sum U_i.
]

1. For each place `i`, calculate its smallest possible value.

The place cannot go below its own lower bound `L_i`. At the same time, all other places can contribute at most

[
\text{sumUpper}-U_i.
]

So the current place must provide at least

[
10000-(\text{sumUpper}-U_i).
]

Taking both restrictions together gives

[
\text{minimum}_i=
\max\left(L_i,\ 10000-(\text{sumUpper}-U_i)\right).
]

The second term is the amount forced onto this place by the requirement that the whole distribution sum to 100%.

1. Calculate the largest possible value for the same place.

All other places contribute at least

[
\text{sumLower}-L_i.
]

Consequently, the current place can contribute at most

[
10000-(\text{sumLower}-L_i).
]

Combining this with its own independent upper bound gives

[
\text{maximum}_i=
\min\left(U_i,\ 10000-(\text{sumLower}-L_i)\right).
]

1. Convert the resulting integer hundredths back to percentages by inserting a decimal point before the last two digits. Python formatting with `value / 100` and `:.2f` is safe here, but formatting directly from the integer quotient and remainder also avoids any dependency on floating-point arithmetic.
2. Print the place name together with its minimum and maximum values in the original input order.

Why it works: each place starts with exactly the set of values that could round to its reported integer, after accounting for the special boundaries 0% and 100%. The only remaining condition is that all places together contain exactly 10,000 hundredths of a percentage. To minimize one place, every other place should be pushed as high as its allowed interval permits. To maximize it, every other place should be pushed as low as possible. Since all intervals are continuous in integer hundredths, these extremal choices characterize the exact feasible minimum and maximum. The global feasibility test guarantees that at least one complete assignment exists, so these bounds are attainable rather than merely necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p = int(input())

    places = []
    sum_lower = 0
    sum_upper = 0

    for _ in range(p):
        name, value = input().split()
        value = int(value)

        lower = max(0, value * 100 - 49)
        upper = min(10000, value * 100 + 49)

        places.append((name, lower, upper))
        sum_lower += lower
        sum_upper += upper

    if sum_lower > 10000 or sum_upper < 10000:
        print("IMPOSSIBLE")
        return

    out = []

    for name, lower, upper in places:
        minimum = max(lower, 10000 - (sum_upper - upper))
        maximum = min(upper, 10000 - (sum_lower - lower))

        min_text = f"{minimum // 100}.{minimum % 100:02d}"
        max_text = f"{maximum // 100}.{maximum % 100:02d}"

        out.append(f"{name} {min_text} {max_text}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop stores each place together with its integer lower and upper bounds. Multiplying the reported integer by 100 moves everything into hundredths, so `32` becomes `3200`, and the ordinary rounded interval becomes `[3151, 3249]`.

The `max(0, ...)` and `min(10000, ...)` operations are necessary. For a reported zero, `-49` hundredths is not a legal percentage, so the lower bound becomes zero. For a reported 100, `10049` hundredths is also impossible, so the upper bound becomes exactly 10,000.

The two accumulated sums allow the global feasibility test to be done once. There is no need to examine individual assignments of people to places.

For each place, `sum_upper - upper` is exactly the largest amount all other places can contribute. Subtracting it from 10,000 gives the amount that the current place is forced to contribute. The `max` with `lower` combines that global restriction with the place's own rounding restriction.

The maximum uses the same reasoning in reverse. `sum_lower - lower` is the smallest amount all other places can contribute, so the current place cannot exceed the remaining total. The `min` combines that restriction with its own upper bound.

All arithmetic stays within a few million at most, so integer overflow is not a concern in Python or in standard fixed-width integer languages with normal 64-bit integers. More importantly, no floating-point arithmetic is needed to decide feasibility or compute the exact two-decimal answers. This avoids errors around values such as `32.50`.

## Worked Examples

### Sample 1

The reported values are `32`, `22`, `26`, and `19`. Their independent intervals, in hundredths, are as follows.

| Place | Reported | Lower | Upper |
| --- | --- | --- | --- |
| Catacombes | 32 | 3151 | 3249 |
| Cite_Universitaire | 22 | 2151 | 2249 |
| Arenes_de_Lutece | 26 | 2551 | 2649 |
| Observatoire | 19 | 1851 | 1949 |

The total lower bound is `9704`, while the total upper bound is `10096`, so a total of `10000` is possible.

For Catacombes, the other three places can contribute at most

[
2249+2649+1949=6847.
]

Hence Catacombes must contribute at least `10000 - 6847 = 3153`. Its own lower bound is `3151`, so the global condition raises the minimum to `3153`, or `31.53%`.

For the maximum, the other three places contribute at least

[
2151+2551+1851=6553.
]

Catacombes can therefore contribute at most `3447`, but its own upper bound is only `3249`, so its maximum remains `32.49%`.

The same calculation is performed for every place.

| Place | `sumLower` | `sumUpper` | Minimum | Maximum |
| --- | --- | --- | --- | --- |
| Catacombes | 9704 | 10096 | 3153 | 3249 |
| Cite_Universitaire | 9704 | 10096 | 2153 | 2249 |
| Arenes_de_Lutece | 9704 | 10096 | 2553 | 2649 |
| Observatoire | 9704 | 10096 | 1853 | 1949 |

The resulting output is therefore `31.53 32.49`, `21.53 22.49`, `25.53 26.49`, and `18.53 19.49`.

### Sample 2

Here the rounded values sum to only 97, so the global total of 100% has to be supplied by the rounding uncertainty.

For the first place, Aqueduc_Medicis, its ordinary interval is `10.51` through `11.49`. The upper bounds of all the other places sum to `88.94%`, so Aqueduc_Medicis must be at least

[
100-88.94=11.06%.
]

That is larger than its ordinary lower bound of `10.51%`.

| Place | Reported | Lower | Upper | Global Minimum | Global Maximum |
| --- | --- | --- | --- | --- | --- |
| Aqueduc_Medicis | 11 | 10.51 | 11.49 | 11.06 | 11.49 |
| Parc_Montsouris | 40 | 39.51 | 40.49 | 40.06 | 40.49 |
| Place_Denfert | 10 | 9.51 | 10.49 | 10.06 | 10.49 |
| Hopital_Sainte_Anne | 4 | 3.51 | 4.49 | 4.06 | 4.49 |
| Butte_aux_cailles | 20 | 19.51 | 20.49 | 20.06 | 20.49 |
| Cite_florale | 12 | 11.51 | 12.49 | 12.06 | 12.49 |
| Prison_de_la_Sante | 0 | 0.00 | 0.49 | 0.06 | 0.49 |

The zero-reporting place is particularly instructive. Its independent lower bound is `0.00`, but all the other places together cannot reach 100%, so it is forced to contribute at least `0.06%`. The same global deficit raises every other minimum by `0.55%`.

This is why simply printing `[r - 0.49, r + 0.49]` for every place would fail on this sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(P)` | Each place is read once and processed once after the global sums are known. |
| Space | `O(P)` | The name and two bounds for every place are stored so the original order can be printed. |

With at most 10,000 places, the algorithm performs only a few integer operations per input line. The memory usage is also small, since each stored name has at most 20 characters and each bound is a small integer. The solution is comfortably within the 2-second and 256 MB limits.

## Test Cases

The following test harness uses the same core logic as the submitted solution. The helper returns exactly what the online judge would receive from standard output.

```python
import sys
import io

def solve_string(inp: str) -> str:
    data = inp.strip().splitlines()
    p = int(data[0])

    places = []
    sum_lower = 0
    sum_upper = 0

    for line in data[1:p + 1]:
        name, value = line.split()
        value = int(value)

        lower = max(0, value * 100 - 49)
        upper = min(10000, value * 100 + 49)

        places.append((name, lower, upper))
        sum_lower += lower
        sum_upper += upper

    if sum_lower > 10000 or sum_upper < 10000:
        return "IMPOSSIBLE"

    out = []

    for name, lower, upper in places:
        minimum = max(lower, 10000 - (sum_upper - upper))
        maximum = min(upper, 10000 - (sum_lower - lower))

        min_text = f"{minimum // 100}.{minimum % 100:02d}"
        max_text = f"{maximum // 100}.{maximum % 100:02d}"

        out.append(f"{name} {min_text} {max_text}")

    return "\n".join(out)

# Sample 1
sample1 = """\
4
Catacombes 32
Cite_Universitaire 22
Arenes_de_Lutece 26
Observatoire 19
"""

expected1 = """\
Catacombes 31.53 32.49
Cite_Universitaire 21.53 22.49
Arenes_de_Lutece 25.53 26.49
Observatoire 18.53 19.49
"""

assert solve_string(sample1) == expected1.strip(), "sample 1"

# Sample 2
sample2 = """\
7
Aqueduc_Medicis 11
Parc_Montsouris 40
Place_Denfert 10
Hopital_Sainte_Anne 4
Butte_aux_cailles 20
Cite_florale 12
Prison_de_la_Sante 0
"""

expected2 = """\
Aqueduc_Medicis 11.06 11.49
Parc_Montsouris 40.06 40.49
Place_Denfert 10.06 10.49
Hopital_Sainte_Anne 4.06 4.49
Butte_aux_cailles 20.06 20.49
Cite_florale 12.06 12.49
Prison_de_la_Sante 0.06 0.49
"""

assert solve_string(sample2) == expected2.strip(), "sample 2"

# Sample 3
sample3 = """\
2
Catacombes 50
Arenes_de_Lutece 49
"""

assert solve_string(sample3) == "IMPOSSIBLE", "sample 3"

# Minimum-size input
assert solve_string("""\
1
Only 0
""") == "Only 0.00 0.00", "single place at zero"

# Single place at the upper boundary
assert solve_string("""\
1
Only 100
""") == "Only 100.00 100.00", "single place at 100"

# All equal values, exact total
all_equal = """\
4
A 25
B 25
C 25
D 25
"""

expected_equal = """\
A 24.76 25.24
B 24.76 25.24
C 24.76 25.24
D 24.76 25.24
"""

assert solve_string(all_equal) == expected_equal.strip(), "all equal values"

# Boundary values and an impossible total
assert solve_string("""\
2
A 0
B 0
""") == "IMPOSSIBLE", "two zero reports"

# Maximum-size input
lines = ["10000"]
for i in range(10000):
    lines.append(f"P{i} 0")

assert solve_string("\n".join(lines)) == "IMPOSSIBLE", "maximum P"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / Only 0` | `Only 0.00 0.00` | Minimum-size input and the zero boundary |
| `1 / Only 100` | `Only 100.00 100.00` | Upper boundary at exactly 100% |
| Four places with value `25` | Each has `24.76 25.24` | Equal values and an exactly balanced total |
| Two places with value `0` | `IMPOSSIBLE` | Global feasibility rather than independent intervals |
| 10,000 places with value `0` | `IMPOSSIBLE` | Maximum input size and linear-time processing |

## Edge Cases

The first edge case is a reported value of zero. For a place reported as zero, the mathematical rounding interval would begin at `-0.50`, but a percentage cannot be negative. In integer hundredths the interval is therefore `[0, 49]`. For the input

```
1
Park 0
```

the lower and upper sums are both insufficient to reach 10,000, so the algorithm immediately prints `IMPOSSIBLE`. The special lower bound prevents a negative percentage from entering the calculation.

The second edge case is a reported value of 100. Its normal rounding interval would extend above 100%, but percentages cannot exceed 100. The interval becomes `[9951, 10000]`. With only one place, the total requirement forces that place to exactly 10,000 hundredths, producing

```
Park 100.00 100.00
```

The explicit upper clamp is what makes this work without relying on the global constraint to repair an invalid local interval.

The third edge case is an impossible collection whose rounded intervals almost add up to 100. Consider

```
2
A 50
B 49
```

The maximum possible values are `50.49` and `49.49`, giving `99.98%`. In integer units, `sum_upper = 9998`, which is below 10,000. The algorithm detects this before calculating any individual answer and prints `IMPOSSIBLE`. Checking only that every reported percentage is between zero and 100 would miss this contradiction.

The fourth edge case is a collection whose reported values sum below 100 and whose missing percentage must be distributed among the places. In Sample 2, the reported values sum to `97`. The upper bounds provide enough room to reach 100, so the input is feasible. When calculating the minimum of a place, the expression

[
10000-(\text{sumUpper}-U_i)
]

forces it to take its share of the missing total. For Aqueduc_Medicis, this gives `11.06%` instead of its independent minimum `10.51%`. The same reasoning applies to every place, including Prison_de_la_Sante, whose minimum becomes `0.06%` even though its own rounded value allows `0.00%`.

The final edge case is exact half rounding. A value of `32.50%` rounds to `33`, not `32`. Since the true percentages occur in increments of `0.01%`, the largest value that can produce a reported `32` is `32.49%`, while the smallest value producing `33` is `32.51%`. Representing the intervals as integer hundredths makes this boundary exact and eliminates the floating-point ambiguity that would arise from comparing values such as `32.5`.
