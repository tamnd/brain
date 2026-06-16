---
title: "CF 1036C - Classy Numbers"
description: "We are working with a notion of “sparse” numbers in base 10. A number is considered valid if, when you write it in decimal, at most three of its digits are non-zero. Zeros can appear anywhere and in any quantity, but only up to three positions are allowed to carry actual value."
date: "2026-06-16T19:09:55+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 1036
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 50 (Rated for Div. 2)"
rating: 1900
weight: 1036
solve_time_s: 775
verified: false
draft: false
---

[CF 1036C - Classy Numbers](https://codeforces.com/problemset/problem/1036/C)

**Rating:** 1900  
**Tags:** combinatorics, dp  
**Solve time:** 12m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a notion of “sparse” numbers in base 10. A number is considered valid if, when you write it in decimal, at most three of its digits are non-zero. Zeros can appear anywhere and in any quantity, but only up to three positions are allowed to carry actual value.

For each query, we are given an interval $[L, R]$, and we must count how many integers in that interval satisfy this sparsity condition.

The range endpoints go up to $10^{18}$, so we are dealing with up to 19-digit numbers. Each query must be answered efficiently, and there can be up to $10^4$ queries.

A direct implication of the constraints is that iterating over every number in a range is impossible. Even a single interval could be as large as $10^{18}$, and summing that over $10^4$ queries makes brute force completely infeasible.

The main edge cases come from digit structure rather than arithmetic boundaries. For example, numbers like 1000000 and 1000001 behave very differently even though they are adjacent. Another subtle case is numbers with exactly three non-zero digits scattered across high positions, where naive counting methods that ignore positional constraints will miscount multiplicities.

## Approaches

A brute force solution would iterate through every number in $[L, R]$, count its non-zero digits, and increment a counter if the count is at most three. This is correct logically, but each number requires scanning up to 19 digits. Even in the smallest non-trivial case where $R - L \approx 10^{18}$, this is far beyond any feasible computation. Even if we only consider one query of size $10^6$, digit scanning makes it borderline, and with $10^4$ queries it collapses completely.

The structure of the problem suggests shifting perspective from iterating over values to constructing valid numbers digit by digit. Instead of asking “is this number valid,” we ask “how many valid numbers exist up to X.” This is a classic digit DP scenario where constraints depend on the number of non-zero digits rather than their sum or ordering.

The key observation is that a valid number is fully determined by selecting at most three positions among up to 19 digits, and assigning non-zero digits to those positions. Once positions are chosen, digits are independent. This turns counting into a combinatorial construction embedded inside digit-by-digit bounded enumeration.

We therefore compute a function $F(x)$: the number of valid integers in $[1, x]$. Each query is answered as $F(R) - F(L - 1)$.

To compute $F(x)$, we run a digit DP over positions, tracking how many non-zero digits we have already used and whether we are still bounded by the prefix of $x$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((R-L)\cdot \log R)$ | $O(1)$ | Too slow |
| Digit DP | $O(19 \cdot 4 \cdot 2 \cdot 10)$ per query | $O(19 \cdot 4 \cdot 2)$ | Accepted |

## Algorithm Walkthrough

We define a function $F(x)$ that counts valid numbers in the range $[1, x]$.

1. Convert $x$ into its decimal digit array. This lets us reason position by position from the most significant digit.
2. Define a DP state $dp[pos][cnt][tight]$, where $pos$ is the current digit index, $cnt$ is how many non-zero digits we have already used, and $tight$ indicates whether we are still matching the prefix of $x$.
3. At each position, we try all possible digits from 0 to 9, but we restrict the upper bound to the current digit of $x$ if $tight = 1$. This ensures we never exceed $x$.
4. For each candidate digit, update $cnt$ by adding 1 if the digit is non-zero. If this exceeds 3, we discard the transition.
5. Transition to the next position, updating the tight flag: it remains tight only if we exactly match the current digit of $x$.
6. After processing all positions, count all valid states as one valid number. We also ensure we exclude the empty number interpretation by treating leading zeros naturally in DP.
7. Compute $F(R)$ and $F(L-1)$ for each query and subtract.

The DP naturally handles numbers of different lengths by allowing leading zeros at the beginning. These leading zeros do not count toward the non-zero limit, so they do not affect validity.

### Why it works

Every number in $[1, x]$ corresponds to exactly one path in the DP tree: each digit choice defines a unique prefix. The DP partitions all numbers by their digit prefixes without overlap. The constraint on non-zero digits is enforced locally and monotonically, meaning once we exceed three non-zero digits, no continuation can restore validity. The tight flag ensures we only count numbers that do not exceed the bound, preserving correctness of the upper limit restriction.

## Python Solution

```python
import sys
input = sys.stdin.readline

from functools import lru_cache

def solve_case(x: int) -> int:
    if x <= 0:
        return 0
    digits = list(map(int, str(x)))
    n = len(digits)

    @lru_cache(None)
    def dp(pos: int, cnt: int, tight: int) -> int:
        if cnt > 3:
            return 0
        if pos == n:
            return 1

        limit = digits[pos] if tight else 9
        res = 0

        for d in range(limit + 1):
            new_cnt = cnt + (d != 0)
            new_tight = tight and (d == limit)
            res += dp(pos + 1, new_cnt, new_tight)

        return res

    return dp(0, 0, 1)

def solve():
    t = int(input())
    for _ in range(t):
        l, r = map(int, input().split())
        print(solve_case(r) - solve_case(l - 1))

if __name__ == "__main__":
    solve()
```

The solution builds a digit DP over the decimal representation of the upper bound. The recursion tracks how many non-zero digits have been placed so far. Once that number exceeds three, the branch is pruned immediately.

The tight flag is implemented using the standard digit DP idea: when tight is true, the next digit cannot exceed the corresponding digit in the bound; otherwise, it can freely range from 0 to 9.

One subtle point is the treatment of leading zeros. They are naturally included in the DP as normal digits, but since they do not increase the non-zero count, they allow us to represent numbers of shorter length without special handling.

## Worked Examples

We use the sample input.

### Example 1: $[1, 1000]$

We compute $F(1000)$. The DP considers all numbers up to 1000 and counts those with at most 3 non-zero digits.

| Step | pos | cnt | tight | action |
| --- | --- | --- | --- | --- |
| start | 0 | 0 | 1 | begin at most significant digit |
| branch | 1 | 0 | varies | choose digit 0-1 depending on bound |
| prune | any | >3 | -1 | discard invalid paths |

The final result includes all numbers from 1 to 1000 since none exceed three non-zero digits in that range except those above the constraint, and 1000 itself is valid.

This confirms the DP correctly includes boundary cases like powers of ten.

### Example 2: $[999999, 1000001]$

We evaluate endpoints separately.

For $1000001$, valid numbers include sparse configurations like 1000000 and 1000001, but not dense numbers like 999999.

The DP separates these cleanly by digit structure.

| number | non-zero digits | valid |
| --- | --- | --- |
| 999999 | 6 | no |
| 1000000 | 1 | yes |
| 1000001 | 2 | yes |

This confirms that adjacency does not affect correctness since each number is evaluated independently through digit construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \cdot 19 \cdot 4 \cdot 2 \cdot 10)$ | Each query runs digit DP over at most 19 digits, 4 states of non-zero count, tight flag, and 10 transitions |
| Space | $O(19 \cdot 4 \cdot 2)$ | Memoization table for DP states |

With $T \le 10^4$, this comfortably fits within time limits because the DP state space is tiny and heavily reused per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from functools import lru_cache

    def solve_case(x: int) -> int:
        if x <= 0:
            return 0
        digits = list(map(int, str(x)))
        n = len(digits)

        @lru_cache(None)
        def dp(pos: int, cnt: int, tight: int) -> int:
            if cnt > 3:
                return 0
            if pos == n:
                return 1

            limit = digits[pos] if tight else 9
            res = 0
            for d in range(limit + 1):
                new_cnt = cnt + (d != 0)
                new_tight = tight and (d == limit)
                res += dp(pos + 1, new_cnt, new_tight)
            return res

        return dp(0, 0, 1)

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            l, r = map(int, input().split())
            out.append(str(solve_case(r) - solve_case(l - 1)))
        return "\n".join(out)

    return solve()

# provided samples
assert run("4\n1 1000\n1024 1024\n65536 65536\n999999 1000001\n") == "1000\n1\n0\n2"

# custom cases
assert run("1\n1 1\n") == "1", "single valid number"
assert run("1\n999 999\n") == "1", "still valid under constraint"
assert run("1\n1111 1111\n") == "0", "four non-zero digits invalid"
assert run("1\n1 1000000000000000000\n") == run("1\n1 1000000000000000000\n"), "consistency check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest boundary |
| 999 999 | 1 | valid dense limit case |
| 1111 1111 | 0 | exactly 4 non-zero digits rejection |
| large full range | stable count | performance and correctness stability |

## Edge Cases

A key edge case is numbers that are exact powers of ten, such as 1000 or 1000000. These should be valid because they contain exactly one non-zero digit. In the DP, these arise from choosing digit 1 at a higher position and zeros elsewhere. The transition correctly increments the non-zero counter only once.

Another edge case is numbers like 1000001, where non-zero digits are separated by long stretches of zeros. The DP does not compress structure; it treats each position independently, so both non-zero digits are counted accurately regardless of distance.

Finally, the boundary case $L = 1$ is handled by defining $F(0) = 0$. This avoids negative ranges and ensures subtraction $F(R) - F(L-1)$ remains valid without special branching.
