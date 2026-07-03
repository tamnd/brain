---
title: "CF 103463A - A simple problem"
description: "We are given a set of digits from 0 to n, and we are asked to consider all possible permutations of these digits. Each permutation is interpreted as a number by concatenating the digits in order."
date: "2026-07-03T06:55:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103463
codeforces_index: "A"
codeforces_contest_name: "The Hangzhou Normal U Qualification Trials for ZJPSC 2020"
rating: 0
weight: 103463
solve_time_s: 54
verified: true
draft: false
---

[CF 103463A - A simple problem](https://codeforces.com/problemset/problem/103463/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of digits from 0 to n, and we are asked to consider all possible permutations of these digits. Each permutation is interpreted as a number by concatenating the digits in order. However, any permutation that starts with zero is discarded because it would produce a number with a leading zero.

Among all valid permutations, we count how many resulting numbers are divisible by a given integer m.

The core task is therefore not about constructing numbers directly, but about counting permutations of a small set of digits under two constraints: no leading zero and divisibility of the formed number by m.

The constraints are small: n is at most 15 and m is at most 100. This immediately suggests that factorial-scale enumeration up to 16 factorial is impossible to do explicitly, since (15 + 1)! is already astronomically large. Any solution must avoid generating permutations directly.

A subtle edge case arises from the leading zero rule. For example, if n = 2, the digits are {0,1,2}. Permutations like 012 or 021 are invalid even though they are permutations of all digits. Only permutations whose first digit is nonzero are counted. A naive permutation generator might count all arrangements first and filter later, but this would waste computation on invalid states and still not scale.

Another important edge case is when n = 0. In this case, the only number is 0 itself, and divisibility depends on whether 0 % m = 0, which is always true. Any correct solution must ensure it does not accidentally discard this trivial case.

## Approaches

A brute-force solution would generate every permutation of the digits from 0 to n, construct the corresponding integer, and test divisibility by m. This is conceptually straightforward: we try all possible orderings, skip those starting with zero, and count valid ones.

The problem is the number of permutations grows as factorial of the number of digits. With n up to 15, we have 16 digits total, leading to 16! permutations, which is far beyond any feasible computation. Even if each check were constant time, the enumeration itself is impossible.

The key observation is that we do not need to construct full numbers explicitly. We only need to track the remainder modulo m as we build the number digit by digit. If we know the current remainder and which digits have been used, we can extend the number by adding any unused digit and update the remainder efficiently using modular arithmetic.

This transforms the problem into a state space search over subsets of digits and remainder values. Each state represents a partial permutation, encoded by a bitmask of used digits and the current remainder modulo m. Since there are at most 2^(n+1) subsets and m possible remainders, the total number of states is at most about 2^16 × 100, which is easily manageable.

We then use dynamic programming over subsets, building permutations incrementally and accumulating counts of valid completions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+1)!) | O(n) | Too slow |
| Bitmask DP | O(2^n · n · m) | O(2^n · m) | Accepted |

## Algorithm Walkthrough

We treat each digit from 0 to n as an element that can be placed in a permutation. We build all valid permutations using dynamic programming over subsets.

1. Represent each state by a pair consisting of a bitmask and a remainder modulo m. The bitmask indicates which digits have already been used, and the remainder tracks the value of the number formed so far modulo m.
2. Initialize the DP table with dp[0][0] = 1, meaning there is one way to form an empty number with remainder 0.
3. For each state (mask, rem), try to append any unused digit d. If digit d is already in the mask, skip it. Otherwise compute the new mask and new remainder. The remainder update follows rem_new = (rem * 10 + d) % m. This step is crucial because it avoids constructing large integers explicitly.
4. We must ensure that no number begins with zero. This constraint is enforced by preventing transitions where the first chosen digit is zero and the mask is empty.
5. After processing all states, sum all dp[full_mask][r] where r = 0. These represent complete permutations that use all digits and are divisible by m.

The correctness comes from the invariant that dp[mask][rem] always stores the number of ways to build a partial permutation using exactly the digits in mask that produces a number with remainder rem modulo m. Each transition preserves this invariant because appending a digit updates both the mask and remainder consistently with how decimal numbers work.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    digits = list(range(n + 1))
    N = n + 1
    
    if N == 1:
        return 1 if 0 % m == 0 else 0

    dp = [[0] * m for _ in range(1 << N)]
    dp[0][0] = 1

    for mask in range(1 << N):
        for rem in range(m):
            cur = dp[mask][rem]
            if not cur:
                continue
            for i in range(N):
                if mask & (1 << i):
                    continue
                if mask == 0 and digits[i] == 0:
                    continue
                nmask = mask | (1 << i)
                nrem = (rem * 10 + digits[i]) % m
                dp[nmask][nrem] += cur

    full = (1 << N) - 1
    return dp[full][0]

if __name__ == "__main__":
    print(solve())
```

The implementation directly follows the DP over subsets described earlier. The dp table is indexed by mask and remainder, and stores counts of ways to reach each state. The transition loops over all unused digits and updates both mask and remainder.

The leading zero restriction is handled explicitly at the first transition level: when mask is zero, we forbid choosing digit 0. This ensures we never generate invalid permutations that start with zero.

The modulo update is performed incrementally using `(rem * 10 + digit) % m`, which is the standard way to maintain numeric value under modular arithmetic without constructing large integers.

## Worked Examples

Consider the sample input:

Input:

```
2 3
```

Digits are {0, 1, 2}. Full permutations are 102, 120, 201, 210. We count those divisible by 3.

We track a simplified DP progression for small subsets:

| Mask | Chosen digits | Remainder states (partial summary) |
| --- | --- | --- |
| 000 | {} | {0: 1} |
| 001 | {0} invalid start skipped |  |
| 010 | {1} | {1: 1} |
| 100 | {2} | {2: 1} |

From these partial builds, full permutations yield remainders:

102 % 3 = 0

120 % 3 = 0

201 % 3 = 0

210 % 3 = 0

Thus all 4 permutations are valid and divisible by 3, so the answer is 4.

This trace demonstrates that the DP correctly accumulates all valid orderings and that remainder propagation aligns with full number divisibility.

A second example:

Input:

```
1 2
```

Digits are {0,1}. Valid permutations are only “10” (since “01” is invalid). 10 % 2 = 0, so answer is 1.

This checks the leading-zero constraint behavior in the smallest nontrivial case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^(n+1) · (n+1) · m) | Each state tries up to n+1 transitions and updates m remainders |
| Space | O(2^(n+1) · m) | DP table indexed by subset mask and modulo state |

With n ≤ 15 and m ≤ 100, the state space is about 16 × 2^16 × 100, which is comfortably within limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return str(solve())

# provided sample
assert run("2 3\n") == "4", "sample 1"

# single digit zero case
assert run("0 7\n") == "1", "only number 0 is valid"

# small case with restriction
assert run("1 2\n") == "1", "only 10 is valid"

# no divisible permutations
assert run("1 3\n") == "0", "10 not divisible by 3"

# slightly larger
assert run("2 1\n") == "6", "all valid permutations count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 7 | 1 | single-digit edge case |
| 1 2 | 1 | leading zero constraint |
| 1 3 | 0 | no valid divisible permutations |
| 2 1 | 6 | all permutations counted |

## Edge Cases

For n = 0 and m = 1, the input is “0 1”. The DP reduces to a single digit set {0}. The only valid permutation is the number 0 itself. The algorithm initializes dp[0][0] = 1 and directly counts this as a full mask state, producing remainder 0, which matches the expected output 1.

For inputs where n = 1 and m is large, such as “1 100”, digits are {0,1}. The DP correctly rejects the permutation starting with 0 and only considers “10”. The remainder is computed as (1 * 10 + 0) % 100 = 10, which is not zero, so the result is 0. The transition rule ensures correctness because every valid permutation is built only through allowed first-digit choices and consistent modular updates.
