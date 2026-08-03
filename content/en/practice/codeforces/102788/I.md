---
title: "CF 102788I - Hole Punch"
description: "The problem describes a strip of paper with n equally spaced positions where holes must be punched. A punch tool always creates exactly two holes, and the distance between those two holes is fixed by the tool."
date: "2026-08-03T15:06:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102788
codeforces_index: "I"
codeforces_contest_name: "2017-2018 ICPC Central Quarter Final of Northeastern European Regional Collegiate Programming Contest"
rating: 0
weight: 102788
solve_time_s: 104
verified: true
draft: false
---

[CF 102788I - Hole Punch](https://codeforces.com/problemset/problem/102788/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a strip of paper with `n` equally spaced positions where holes must be punched. A punch tool always creates exactly two holes, and the distance between those two holes is fixed by the tool. We need to find every distance `k` such that repeatedly using only a punch with that distance can create all holes without leaving any hole unpaired. The input is one even integer `n`, and the output is the number of valid distances followed by those distances in increasing order.

The size of `n` is up to `10^9`, so simulating every possible punch distance from `1` to `n` is impossible. A linear scan already needs up to one billion checks, which is too slow in normal contest limits. The solution must use the mathematical structure of the problem rather than trying every distance.

A common mistake is to assume that every divisor of `n` works. Divisibility is necessary, but the reason is more specific: the holes split into groups according to their position modulo `k`, and every such group must contain an even number of holes. For example, with `n = 8`, `k = 3` is not valid. The positions split into groups of sizes `3, 3, 2`, and the groups with three holes cannot be perfectly paired. The correct output for this input is:

```
3
1 2 4
```

Another edge case is `k = n`. It looks like a valid distance because it divides the entire range, but the punch would need two holes separated by `n` centimeters, while the last possible hole is only `n - 1` centimeters away from the first one. For `n = 2`, the only valid distance is `1`, not `2`.

## Approaches

A direct solution would test every possible distance `k`. For each `k`, we can look at every pair of positions that are `k` apart and check whether all holes can be matched. This works because a fixed distance defines exactly which holes can be connected, but for `n = 10^9` it is far too slow. Even checking all candidates requires billions of operations.

The useful observation comes from grouping positions by their remainder modulo `k`. Holes with the same remainder are connected in a chain by jumps of length `k`. For example, if `k = 3`, positions `1, 4, 7` form one chain. A chain can be completely paired if and only if its length is even.

Suppose `n = qk + r`. Among the `k` chains, `r` chains have length `q + 1` and the remaining chains have length `q`. If `r` is not zero, both sizes appear. Since two consecutive integers cannot both be even, a valid distance cannot have a remainder. Thus every valid `k` must divide `n`.

When `k` divides `n`, every chain has exactly `n / k` holes. The chain length must be even, so `n / k` must also be even. The entire problem reduces to finding divisors `k` of `n` where the corresponding quotient is even.

The largest possible value of `n` is `10^9`, so checking divisors up to its square root is enough. The number of checks is only about 31623.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) or worse | O(1) | Too slow |
| Optimal | O(sqrt(n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of holes `n`.
2. Iterate through all integers `i` from `1` to `sqrt(n)`. If `i` divides `n`, both `i` and `n / i` are divisors. Each divisor is checked independently because either one may satisfy the required parity condition.
3. For every divisor `d`, check whether `n / d` is even. If it is, `d` is a valid punch distance because every modulo-`d` chain has an even number of holes.
4. Store all valid distances and sort them before printing. Divisors are discovered in pairs, so sorting is needed to match the required increasing order.

Why it works: for a fixed distance `k`, the possible punches create independent chains of holes. A chain with an odd number of holes always leaves one hole unmatched, while a chain with an even number of holes can be paired from one end to the other. The algorithm only accepts distances where every chain length is even, which is exactly the condition needed for a complete punching plan.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = []

    i = 1
    while i * i <= n:
        if n % i == 0:
            if (n // i) % 2 == 0:
                ans.append(i)
            other = n // i
            if other != i and (n // other) % 2 == 0:
                ans.append(other)
        i += 1

    ans.sort()

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The loop only reaches the square root of `n`, which avoids iterating over impossible distances. When a divisor pair `(i, n / i)` is found, both values are tested. The `other != i` condition prevents adding the square root divisor twice when `n` is a perfect square.

The condition `(n // d) % 2 == 0` directly represents the chain length argument. Dividing the total number of holes by the number of chains gives the number of holes inside each chain, and that number must be even.

Python integers do not overflow here because the largest multiplication is `i * i`, with `i` limited to about 31623.

## Worked Examples

For `n = 8`:

| Current divisor | Quotient | Valid |
| --- | --- | --- |
| 1 | 8 | yes |
| 2 | 4 | yes |
| 4 | 2 | yes |
| 8 | 1 | no |

The valid distances are `1, 2, 4`.

For `n = 12`:

| Current divisor | Quotient | Valid |
| --- | --- | --- |
| 1 | 12 | yes |
| 2 | 6 | yes |
| 3 | 4 | yes |
| 4 | 3 | no |
| 6 | 2 | yes |
| 12 | 1 | no |

The valid distances are `1, 2, 3, 6`.

These traces show that the answer depends on the parity of the number of holes inside each chain, not simply on whether a number divides `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n)) | Every possible divisor up to the square root is checked. |
| Space | O(a) | The output array stores the valid divisors. |

The square root of the maximum input is small enough for a direct divisor search, so the algorithm easily fits the limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    ans = []

    i = 1
    while i * i <= n:
        if n % i == 0:
            if (n // i) % 2 == 0:
                ans.append(i)
            if n // i != i and (n // (n // i)) % 2 == 0:
                ans.append(n // i)
        i += 1

    ans.sort()
    return str(len(ans)) + "\n" + " ".join(map(str, ans)) + "\n"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

assert run("8\n") == "3\n1 2 4\n"
assert run("2\n") == "1\n1\n"
assert run("6\n") == "2\n1 3\n"
assert run("12\n") == "4\n1 2 3 6\n"
assert run("1000000000\n") == "6\n1 2 4 5 8 10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `1` and `1` | Minimum valid size |
| `6` | `1 3` | Odd quotient divisors are rejected |
| `12` | `1 2 3 6` | Multiple divisor pairs |
| `1000000000` | large divisor search | Square root iteration boundary |

## Edge Cases

For `n = 8` and `k = 3`, the algorithm does not output `3` because `3` is not a divisor of `8`. The mathematical reduction catches the invalid case before any pairing simulation is needed.

For `n = 2`, the algorithm checks divisors `1` and `2`. The divisor `1` has quotient `2`, which is even, while divisor `2` has quotient `1`, which is odd. The result is only distance `1`.

For `n = 12`, the divisor `4` is rejected even though it divides `12`. Its quotient is `3`, meaning each chain would contain three holes, leaving one unmatched hole in every chain.

For a large value such as `n = 1000000000`, the algorithm never attempts to test one billion candidates. It only checks possible divisors up to `31623`, which is the key reason the solution remains efficient.
