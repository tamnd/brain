---
title: "CF 102346H - Hour for a Run"
description: "The track contains N equally spaced signs, and Vinicius plans to run exactly V complete laps. Since one lap passes all N signs, the entire training consists of V N sign passages."
date: "2026-08-13T01:27:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 65
verified: true
draft: false
---

[CF 102346H - Hour for a Run](https://codeforces.com/problemset/problem/102346/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The track contains `N` equally spaced signs, and Vinicius plans to run exactly `V` complete laps. Since one lap passes all `N` signs, the entire training consists of `V * N` sign passages.

For each percentage from 10% through 90%, we need the smallest integer number of signs whose corresponding fraction of the complete training is at least that percentage. The output contains nine values, in order for 10%, 20%, ..., 90%.

For example, with `V = 3` and `N = 17`, the training has `51` sign passages. For 30%, the required value is the smallest integer at least `0.30 * 51 = 15.3`, namely `16`. The word "at least" is what makes rounding upward necessary.

Both `V` and `N` are at most `10^4`, so the total number of sign passages can reach `10^8`. A solution that scans every sign passage can consequently perform around one hundred million iterations. That is much more work than necessary for a problem whose answer consists of only nine numbers. The structure of the calculation lets us solve it in constant time, regardless of the size of the training.

The main edge cases come from rounding. With input `1 1`, the entire training has one sign passage. Every positive percentage from 10% through 90% requires reaching that only sign, so the correct output is `1 1 1 1 1 1 1 1 1`. A careless implementation using integer floor division would produce zero for every percentage.

Another useful boundary case is `3 11`. The total is `33`, and 30% is `9.9`, so the answer must be `10`, not `9`. The complete output is `4 7 10 14 17 20 24 27 30`. Direct integer division without a ceiling operation silently fails at values such as `9.9`.

An exact-divisibility case behaves differently. With input `10 10`, the total is `100`, so every requested percentage is an integer number of signs. The output is `10 20 30 40 50 60 70 80 90`. A ceiling formula must preserve an exact integer instead of adding an unnecessary extra sign.

## Approaches

A direct approach is to simulate the training sign by sign. There are `V * N` sign passages in total. For every percentage, we could keep increasing the number of passed signs until the fraction of the total training reaches the desired percentage. This is correct because the first position at which the threshold is reached is exactly the minimum number of signs Vinicius must count.

The problem is that the maximum training contains `10^4 * 10^4 = 10^8` sign passages. A simulation can therefore require up to `10^8` iterations, and doing separate scans for several percentages would make the approach even more wasteful. Even though `10^8` is not mathematically impossible, it is unnecessary and gives the solution a much less comfortable performance margin.

The key observation is that the number of signs for one complete training is known immediately: `V * N`. If we want at least `k * 10%` of the training, the required real-valued number of signs is

`(V * N * k) / 10`

where `k` ranges from 1 to 9.

The answer must be an integer number of signs, and it must be large enough to reach the threshold. That means we need the ceiling of this value. For positive integers, the ceiling of `x / 10` can be computed as `(x + 9) // 10`. Thus each of the nine answers can be obtained directly, with no simulation.

The brute-force works because it searches for the first sign count satisfying each percentage condition, but fails because the search space can contain `10^8` positions. The observation that every threshold is simply a fixed fraction of the known total lets us replace the search with nine arithmetic calculations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(VN) | O(1) | Too slow and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `V` and `N`, where `V * N` is the total number of signs passed during the complete training.
2. Compute `total = V * N`. This gives us the denominator for every percentage calculation, so there is no reason to simulate individual laps or signs.
3. For each `k` from `1` through `9`, compute `total * k`. Dividing this quantity by `10` gives the exact number of signs corresponding to `10k%` of the training.
4. Round that value upward using `(total * k + 9) // 10`. Rounding upward is required because the runner needs to have completed at least the requested percentage. If the exact value is already an integer, ordinary integer division still returns that exact value.
5. Print the nine calculated values separated by spaces, preserving the order from 10% to 90%.

Why it works: for any requested percentage `10k%`, the runner must have passed at least `(V * N * k) / 10` signs. Since the number of passed signs is an integer, the smallest valid count is exactly the ceiling of that fraction. The expression `(x + 9) // 10` computes that ceiling for every positive integer `x`, so each generated answer is both sufficient and minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

V, N = map(int, input().split())

total = V * N

answer = [(total * k + 9) // 10 for k in range(1, 10)]

print(*answer)
```

The first line reads the two quantities describing the training. There is only one test case, so after reading the input the program can immediately perform the calculation.

`total = V * N` represents the number of sign passages in all planned laps. Since every lap contains exactly `N` equally spaced signs, multiplying the number of laps by the number of signs per lap gives the full training length in the units relevant to the problem.

The list comprehension evaluates the nine requested percentages. For `k = 1`, it calculates the 10% threshold; for `k = 2`, it calculates 20%; and so on through `k = 9`.

The expression `(total * k + 9) // 10` is the integer-only ceiling operation. Using `total * k // 10` would be wrong whenever the threshold is not an integer, because floor division would round downward and could leave the runner below the requested percentage.

Python integers automatically handle values larger than fixed-width machine integers, so there is no overflow concern. Even here, `V * N` is at most `10^8`, and multiplying it by `9` gives at most `9 * 10^8`, which also fits comfortably in a standard 32-bit signed integer.

## Worked Examples

### Sample 1

For `V = 3` and `N = 17`, there are `51` sign passages in the complete training.

| k | Percentage | total * k | Ceiling | Answer |
| --- | --- | --- | --- | --- |
| 1 | 10% | 51 | 6 | 6 |
| 2 | 20% | 102 | 11 | 11 |
| 3 | 30% | 153 | 16 | 16 |
| 4 | 40% | 204 | 21 | 21 |
| 5 | 50% | 255 | 26 | 26 |
| 6 | 60% | 306 | 31 | 31 |
| 7 | 70% | 357 | 36 | 36 |
| 8 | 80% | 408 | 41 | 41 |
| 9 | 90% | 459 | 46 | 46 |

For 30%, the exact threshold is `153 / 10 = 15.3`, so 15 signs are insufficient and the answer must be 16. The same ceiling rule applies independently to all nine percentages.

### Sample 2

For `V = 5` and `N = 17`, the total training contains `85` sign passages.

| k | Percentage | total * k | Ceiling | Answer |
| --- | --- | --- | --- | --- |
| 1 | 10% | 85 | 9 | 9 |
| 2 | 20% | 170 | 17 | 17 |
| 3 | 30% | 255 | 26 | 26 |
| 4 | 40% | 340 | 34 | 34 |
| 5 | 50% | 425 | 43 | 43 |
| 6 | 60% | 510 | 51 | 51 |
| 7 | 70% | 595 | 60 | 60 |
| 8 | 80% | 680 | 68 | 68 |
| 9 | 90% | 765 | 77 | 77 |

The 10% threshold is `8.5`, so the runner needs 9 signs. In contrast, the 20% threshold is exactly `17`, so the answer remains 17 rather than becoming 18. This demonstrates why a ceiling calculation is preferable to simply adding one after division.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Exactly nine percentage calculations are performed |
| Space | O(1) | Only the total and nine output values are stored |

The constraints allow up to `10^8` sign passages, but the optimal solution never iterates over those passages. It performs a fixed nine calculations, so its running time is independent of `V * N` and easily fits the available resources.

## Test Cases

```python
import io
import sys

def solve(inp: str) -> str:
    input_stream = io.StringIO(inp)
    V, N = map(int, input_stream.readline().split())

    total = V * N
    answer = [(total * k + 9) // 10 for k in range(1, 10)]

    return " ".join(map(str, answer))

# Provided samples
assert solve("3 17\n") == "6 11 16 21 26 31 36 41 46", "sample 1"
assert solve("5 17\n") == "9 17 26 34 43 51 60 68 77", "sample 2"
assert solve("3 11\n") == "4 7 10 14 17 20 24 27 30", "sample 3"

# Minimum-size input
assert solve("1 1\n") == "1 1 1 1 1 1 1 1 1", "minimum values"

# Maximum-size input
assert solve("10000 10000\n") == (
    "10000000 20000000 30000000 40000000 50000000 "
    "60000000 70000000 80000000 90000000"
), "maximum values"

# Exact divisibility at every requested percentage
assert solve("10 10\n") == "10 20 30 40 50 60 70 80 90", "exact percentages"

# Fractional thresholds that require rounding upward
assert solve("1 7\n") == "1 2 3 3 4 5 6 7 7", "ceiling boundaries"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1 1 1 1 1 1 1 1 1` | Minimum values and the fact that every positive percentage needs the only sign |
| `10000 10000` | `10000000 20000000 30000000 40000000 50000000 60000000 70000000 80000000 90000000` | Maximum values and large arithmetic |
| `10 10` | `10 20 30 40 50 60 70 80 90` | Exact divisibility without adding an unnecessary sign |
| `1 7` | `1 2 3 3 4 5 6 7 7` | Fractional thresholds and ceiling behavior |

## Edge Cases

For the minimum input `1 1`, the total is `1`. For every `k` from 1 to 9, the expression becomes `(k + 9) // 10`, which is 1 for all nine values. The output is therefore `1 1 1 1 1 1 1 1 1`. A floor-based implementation would incorrectly print zero because `k // 10` is zero for these values.

For the boundary input `3 11`, the total is `33`. The 30% threshold is `99 / 10 = 9.9`, so the calculation `(99 + 9) // 10 = 10` correctly rounds upward. The full output is `4 7 10 14 17 20 24 27 30`. This catches the common mistake of using `total * k // 10`, which would produce 9 for the third value.

For the exact-divisibility input `10 10`, the total is `100`. At 20%, for example, the threshold is exactly `20`, and `(200 + 9) // 10` equals `20`, not `21`. The same holds for every requested percentage, giving `10 20 30 40 50 60 70 80 90`. The `+9` in the ceiling formula only compensates for a nonzero remainder, while exact multiples remain unchanged.

For the maximum input `10000 10000`, the total is `100,000,000`. The 90% threshold is `90,000,000`, and all arithmetic remains exact. The algorithm performs the same nine iterations as it does for the minimum input, so increasing the training from one sign passage to one hundred million does not increase the number of algorithmic steps.
