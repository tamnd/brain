---
title: "CF 102783G - Hyper Chocolate Cubes"
description: "Felix receives hypercubes of chocolate with sizes corresponding to powers of a chosen side length w. The available pieces have weights: 1, w, w², w³, ..., w¹⁰⁰."
date: "2026-07-27T20:01:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102783
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 2"
rating: 0
weight: 102783
solve_time_s: 77
verified: true
draft: false
---

[CF 102783G - Hyper Chocolate Cubes](https://codeforces.com/problemset/problem/102783/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Felix receives hypercubes of chocolate with sizes corresponding to powers of a chosen side length `w`. The available pieces have weights:

`1, w, w², w³, ..., w¹⁰⁰`.

For each package weight `x`, we need to determine whether Felix can place some of these hypercubes on either side of a balance scale so that the two sides become equal, with the package on one side.

Putting a chocolate piece on the same side as the package subtracts its value from the package's effective weight, while putting it on the opposite side adds its value. Since every available hypercube can be used at most once, the question becomes whether `x` can be written as a sum of powers of `w` where every coefficient is one of:

`-1, 0, 1`.

The input contains up to 20 package weights, each at most `10^9`. A direct search over subsets is impossible because there are 101 possible powers of `w`, giving far more combinations than can be explored. Even restricting ourselves to the useful powers would still leave an exponential search space, so the solution has to exploit the structure of powers.

The important property is that powers of `w` form a positional number system. Instead of choosing pieces globally, we can decide the coefficient of each power from the smallest power upward. Once the coefficient of `w^i` is fixed, the remaining value must be divisible by `w^(i+1)`, which lets us reduce the problem one digit at a time.

The tricky cases come from values that look close to representable but require an invalid digit. For example, with `w = 5`, the value `2` cannot be created:

```
1
5
25
```

The possible signed combinations near this range are `-5, -4, -1, 0, 1, 4, 5`, so the answer is `NO`. A naive approach that only checks normal base-5 digits might incorrectly assume every digit can be adjusted.

Another edge case is when the remainder is `w - 1`. For example, with `w = 5` and `x = 4`, the correct representation is:

`5 - 1 = 4`.

The first digit is actually `-1`, not `4`. Any approach that only allows digits `0` through `w-1` will fail here.

A small example:

```
Input
1 5
4

Output
YES
```

The package can be balanced by placing the `5` cube on one side and the single cube on the other side.

## Approaches

The brute-force approach is to try every possible assignment of the available hypercubes. Each power can have three states: unused, placed with the package, or placed against the package. If we consider all 101 powers, this gives `3^101` possibilities, which is astronomically large. Even though only powers up to `10^9` matter numerically, the search space is still exponential and cannot work.

The useful observation is that this is exactly a balanced positional representation problem. In a normal base-`w` representation, every digit must be between `0` and `w-1`. Here, every digit can instead be `-1`, `0`, or `1`. We only need to inspect the current remainder modulo `w`.

Suppose the current value is `x`. The coefficient of the `1`-power determines the remainder when dividing by `w`. If `x % w` is zero, the current digit must be zero. If the remainder is one, we use a positive one. If the remainder is `w-1`, we use a negative one because subtracting one makes the value divisible by `w`.

After removing that digit, we divide by `w` and solve the same problem for the next power. If a remainder appears that cannot be represented by `-1`, `0`, or `1`, the answer is impossible.

The brute-force works because it tries every valid placement, but fails because it ignores the positional structure. The greedy digit-by-digit process succeeds because every decision is forced by divisibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^101) | O(101) | Too slow |
| Optimal | O(100) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read each package weight and repeatedly examine its remainder when divided by `w`. The lowest power `w^0` is the only power that affects the remainder modulo `w`, so it must be decided first.
2. If the remainder is zero, assign coefficient `0` to the current power. The current value is already divisible by `w`, so no cube of this size is needed.
3. If the remainder is one, assign coefficient `1`. Taking one cube of the current size removes the extra remainder.
4. If the remainder is `w - 1`, assign coefficient `-1`. This is the same as adding one to the next digit because `-1 ≡ w-1 (mod w)`, and it makes the remaining value divisible by `w`.
5. If the remainder is anything else, no valid coefficient exists for the current power, so the answer is `NO`.
6. Divide the remaining value by `w` and continue with the next power. The process stops when the value becomes zero.

Why it works:

At every step, the current value must be expressed as:

`current = digit + w * remaining`

where `digit` is one of `-1`, `0`, or `1`. The chosen digit is the only possible one that makes `current - digit` divisible by `w`. After removing it, the remaining problem is identical but shifted one power higher. Since every digit decision preserves equivalence with the original balance problem, reaching zero means we found a valid arrangement, while encountering an impossible remainder proves that no arrangement exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(x, w):
    while x > 0:
        r = x % w

        if r == 0:
            digit = 0
        elif r == 1:
            digit = 1
        elif r == w - 1:
            digit = -1
        else:
            return False

        x = (x - digit) // w

    return True

def solve():
    n, w = map(int, input().split())

    ans = []
    for _ in range(n):
        x = int(input())
        ans.append("YES" if possible(x, w) else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `possible` function performs the balanced-base conversion. The variable `x` always represents the part of the package weight that has not yet been handled by smaller powers.

The remainder check is the core of the implementation. The three valid cases correspond exactly to the three possible coefficients of the current power. The line `x = (x - digit) // w` first removes the chosen coefficient and then moves to the next power.

There is no need to explicitly generate the powers of `w`. The repeated division naturally walks through the same positions. Since all inputs are at most `10^9`, fewer than 100 iterations are needed.

## Worked Examples

### Example 1

Input:

```
4 5
25
26
29
32
```

For `w = 5`, the process looks like this:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 25 | 0 | 0 | 5 |
| 5 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

The number `25` is exactly `5²`, so one square hypercube balances it.

For `26`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 26 | 1 | 1 | 5 |
| 5 | 0 | 0 | 1 |
| 1 | 1 | 1 | 0 |

This corresponds to `25 + 1`.

For `29`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 29 | 4 | -1 | 6 |
| 6 | 1 | 1 | 1 |
| 1 | 1 | 1 | 0 |

The representation is `25 + 5 - 1`.

For `32`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 32 | 2 | invalid | - |

The remainder cannot be represented, so the answer is `NO`.

### Example 2

Input:

```
3 3
1
2
5
```

For `w = 3`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |

`1` is directly available.

For `2`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 2 | 2 | -1 | 1 |
| 1 | 1 | 1 | 0 |

The representation is `3 - 1`.

For `5`:

| Value | Remainder | Chosen digit | New value |
| --- | --- | --- | --- |
| 5 | 2 | -1 | 2 |
| 2 | 2 | -1 | 1 |
| 1 | 1 | 1 | 0 |

The representation is `9 - 3 - 1`, but since only powers up to 100 are available, this is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(100n) | Each number is divided by `w` until it becomes zero. |
| Space | O(1) | Only a few integer variables are stored. |

The maximum input size is only 20 values, so this logarithmic conversion is easily within the limits. The algorithm never explores combinations of cubes, which is the source of the exponential difficulty in the brute-force approach.

## Test Cases

```python
import sys
import io

def possible(x, w):
    while x > 0:
        r = x % w
        if r == 0:
            digit = 0
        elif r == 1:
            digit = 1
        elif r == w - 1:
            digit = -1
        else:
            return False
        x = (x - digit) // w
    return True

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, w = map(int, sys.stdin.readline().split())
    res = []
    for _ in range(n):
        x = int(sys.stdin.readline())
        res.append("YES" if possible(x, w) else "NO")
    return "\n".join(res)

assert run("""4 5
25
26
29
32
""") == """YES
YES
YES
NO""", "sample 1"

assert run("""3 3
1
2
5
""") == """YES
YES
YES""", "balanced ternary"

assert run("""1 5
2
""") == "NO", "invalid remainder"

assert run("""1 2
1000000000
""") == "YES", "large binary case"

assert run("""3 10
1
9
11
""") == """YES
YES
YES""", "decimal balanced representation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 5 / 25 26 29 32` | `YES YES YES NO` | Official sample behavior and invalid digit detection |
| `3 3 / 1 2 5` | `YES YES YES` | Balanced ternary style representations |
| `1 5 / 2` | `NO` | Rejects impossible remainders |
| `1 2 / 1000000000` | `YES` | Large values and repeated division |
| `3 10 / 1 9 11` | `YES YES YES` | Boundary remainders including `w-1` |

## Edge Cases

When the remainder is neither `0`, `1`, nor `w-1`, the algorithm immediately rejects the value. For example:

```
Input
1 5
2
```

The first remainder is `2`. The current digit would need to be `2`, but a single cube can only contribute `-1`, `0`, or `1` at this position. The algorithm returns `NO`.

When the remainder is `w-1`, the solution must use a negative digit. For example:

```
Input
1 5
4
```

The first remainder is `4`, so we choose digit `-1`:

`4 - (-1) = 5`

After dividing by `5`, the remaining value is `1`, which is handled by choosing digit `1`. The representation is `5 - 1`, so the answer is `YES`.

The maximum values are also safe. For example:

```
Input
1 2
1000000000
```

The algorithm only performs binary reductions. It finishes after about 30 iterations, far below the available 100 powers, and correctly determines whether the signed representation exists.
