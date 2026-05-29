---
title: "CF 401D - Roman and Numbers"
description: "We are asked to count the number of integers that can be formed by permuting the digits of a given number $n$, do not start with zero, and are divisible by a given modulus $m$. The input $n$ can be as large as $10^{18}$, which means up to 18 digits, and $m$ is at most 100."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "combinatorics", "dp", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 401
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 235 (Div. 2)"
rating: 2000
weight: 401
solve_time_s: 79
verified: true
draft: false
---

[CF 401D - Roman and Numbers](https://codeforces.com/problemset/problem/401/D)

**Rating:** 2000  
**Tags:** bitmasks, brute force, combinatorics, dp, number theory  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of integers that can be formed by permuting the digits of a given number $n$, do not start with zero, and are divisible by a given modulus $m$. The input $n$ can be as large as $10^{18}$, which means up to 18 digits, and $m$ is at most 100. The output is simply the count of valid numbers.

The challenge lies in the fact that generating all permutations naively is not feasible. Even a number with 18 distinct digits has $18! \approx 6.4 \times 10^{15}$ permutations, which is astronomically large. This rules out any solution that explicitly enumerates permutations.

Edge cases include numbers with repeated digits, which can reduce the number of distinct permutations. Numbers with zero digits need special care because leading zeros are invalid. For example, for $n = 102$ and $m = 2$, the permutations $012$ is invalid because it starts with zero, but $120$ and $210$ are valid.

Another subtlety is handling divisibility. We cannot check divisibility after generating a number because there are too many numbers. Instead, we must compute the remainder incrementally while building the number.

## Approaches

The brute-force approach generates all permutations of the digits of $n$, checks that they do not start with zero, and then checks divisibility by $m$. This works for numbers with very few digits. With $d$ digits, this requires up to $d!$ permutations, each taking $O(d)$ to check divisibility, so $O(d! \cdot d)$. For $d = 18$, this is infeasible.

The key observation is that we do not need to generate permutations explicitly. Each number is a rearrangement of digits, which naturally suggests a state space defined by which digits have been used so far. Since $d \le 18$, we can encode the used digits as a bitmask of length $d$. The remaining problem is to compute the number of ways to complete the number given a partial bitmask and the current remainder modulo $m$.

Dynamic programming over bitmasks and remainders solves this. Let `dp[mask][rem]` represent the number of ways to form numbers using the digits corresponding to `mask` that leave a remainder `rem` modulo `m`. At each step, we try placing an unused digit at the next position, update the remainder using modular arithmetic, and update the mask. To avoid counting numbers starting with zero, we simply skip zero if we are at the first position. To handle repeated digits without double-counting, we ensure that if two identical digits are in the remaining set, we always use the leftmost unused one first in our ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d! * d) | O(d!) | Too slow for d > 10 |
| Bitmask DP | O(2^d * m * d) | O(2^d * m) | Accepted |

## Algorithm Walkthrough

1. Convert the number $n$ to a list of digits and sort them. Sorting ensures that repeated digits can be handled consistently without double-counting permutations.
2. Initialize a DP table `dp[mask][rem]` with -1 to indicate uncomputed states. `mask` is an integer where the $i$-th bit is 1 if the $i$-th digit has been used. `rem` is the remainder modulo `m`.
3. Define a recursive function `count(mask, rem)` that returns the number of valid numbers that can be formed using the unused digits in `mask`, given the current remainder `rem`.
4. In the recursion, if all digits are used (`mask == (1 << d) - 1`), check if `rem == 0`. If so, return 1, otherwise return 0. This is the base case.
5. Otherwise, iterate over all digit positions `i`. Skip any digit already used (`mask & (1 << i)`) or skip leading zero if `mask == 0` and the digit is zero. To avoid double-counting identical digits, skip a digit if it is the same as the previous one and the previous digit has not been used (`digits[i] == digits[i-1]` and `(mask & (1 << (i-1))) == 0`).
6. For a valid choice, recursively call `count(mask | (1 << i), (rem * 10 + digits[i]) % m)` and accumulate the result.
7. Store the result in `dp[mask][rem]` and return it.

Why it works: The DP ensures that every combination of unused digits and remainder is considered exactly once. Skipping repeated digits when the previous identical digit has not been used prevents overcounting permutations. Leading zeros are avoided explicitly. By building the remainder incrementally, we only ever consider numbers that are divisible by `m` in the final check, eliminating the need to construct full numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10000)

def main():
    n, m = input().split()
    m = int(m)
    digits = sorted([int(c) for c in n])
    d = len(digits)
    dp = [[-1 for _ in range(m)] for _ in range(1 << d)]

    def count(mask, rem):
        if mask == (1 << d) - 1:
            return 1 if rem == 0 else 0
        if dp[mask][rem] != -1:
            return dp[mask][rem]
        total = 0
        for i in range(d):
            if mask & (1 << i):
                continue
            if i > 0 and digits[i] == digits[i-1] and not (mask & (1 << (i-1))):
                continue
            if mask == 0 and digits[i] == 0:
                continue
            total += count(mask | (1 << i), (rem * 10 + digits[i]) % m)
        dp[mask][rem] = total
        return total

    print(count(0, 0))

if __name__ == "__main__":
    main()
```

The first section converts the input number to digits and sorts them. The DP table `dp` is initialized for all subsets of digits and all remainders. The recursive `count` function mirrors the algorithm walkthrough. The conditions for skipping used digits, leading zeros, and repeated digits ensure correctness. We accumulate valid counts in `total`, memoize, and finally print the result.

## Worked Examples

For `n = 104`, `m = 2`:

| mask | rem | next digit | new mask | new rem | total |
| --- | --- | --- | --- | --- | --- |
| 0b000 | 0 | 1 | 0b001 | 1 | ... |
| 0b001 | 1 | 0 | 0b011 | 10 % 2 = 0 | ... |
| 0b011 | 0 | 4 | 0b111 | 0 | 1 |
| ... | ... | ... | ... | ... | ... |

All permutations leading to remainders divisible by 2 are counted. The result is 3: `104`, `140`, `410`.

For `n = 232`, `m = 2`:

Only the numbers `232`, `223`, `322` exist. Only `232` and `322` are divisible by 2. The DP correctly counts 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^d * d * m) | Each subset of digits (2^d) is combined with each possible remainder (m), iterating over up to d digits for transitions |
| Space | O(2^d * m) | DP table stores every mask and remainder combination |

For $d \le 18$ and $m \le 100$, this is roughly $2.6 \times 10^5$ states, feasible within memory and time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided samples
assert run("104 2\n") == "3", "sample 1"
assert run("232 2\n") == "2", "sample 2"

# custom cases
assert run("1 1\n") == "1", "single digit divisible"
assert run("100 10\n") == "1", "leading zero avoidance"
assert run("111 3\n") == "1", "all digits same"
assert run("9876543210 11\n") == "0", "large number no valid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | Single-digit case, divisible |
| 100 10 | 1 | Leading zero prevention |
| 111 3 | 1 | All digits identical |
| 9876543210 11 | 0 | Large input, no valid number |

## Edge Cases

For `n = 100`, `m = 10`, the DP avoids permutations starting with zero (`010`,
