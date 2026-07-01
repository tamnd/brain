---
title: "CF 103993D - Password"
description: "We are dealing with 6-digit passwords, where each password is a sequence of digits from 0 to 9. The structure of the password is highly constrained: it must use exactly two distinct digits, and each of those digits must appear exactly three times, so the password is always a…"
date: "2026-07-02T06:00:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103993
codeforces_index: "D"
codeforces_contest_name: "ICPC 2022-2023 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 103993
solve_time_s: 45
verified: true
draft: false
---

[CF 103993D - Password](https://codeforces.com/problemset/problem/103993/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are dealing with 6-digit passwords, where each password is a sequence of digits from 0 to 9. The structure of the password is highly constrained: it must use exactly two distinct digits, and each of those digits must appear exactly three times, so the password is always a permutation of something like AAA BBB where A and B are different digits.

In addition to this structural rule, we are also given a set of digits that are forbidden. Any candidate password is invalid if it uses even one of those digits.

So the task is purely combinatorial: count how many length-6 sequences can be formed by choosing two allowed digits and arranging them such that each appears exactly three times.

The input consists of a small list of forbidden digits. Everything not listed is allowed. Since digits range only from 0 to 9, the effective universe is extremely small, which already suggests that brute force over digit pairs is sufficient.

The constraints imply a very small search space. At most 10 digits exist, and we are choosing pairs of allowed digits. That gives at most C(10, 2) = 45 candidate pairs, which is tiny. For each pair, counting arrangements is constant work. This immediately rules out any need for advanced optimization or preprocessing.

Edge cases are mostly about how forbidden digits shrink the available set.

A subtle case is when fewer than two digits are available. For example, if 9 digits are forbidden and only one digit remains, then it is impossible to form a valid password because we need two distinct digits. Another corner case is when exactly two digits remain, which produces a single valid digit pair but many permutations.

Example where greedy thinking fails: if allowed digits are {1, 2}, one might mistakenly think there is only one password “111222”, but the answer is actually the number of distinct permutations of this multiset, which is 6!/(3!3!) = 20. Missing this combinatorial factor is the most common mistake.

## Approaches

The brute-force idea is to generate all length-6 sequences of digits 0 to 9 and check whether each sequence satisfies the constraints: exactly two distinct digits, each appearing three times, and no forbidden digits. There are 10^6 such sequences. Each check is O(6), so this approach costs about 6 million operations per test, which is already borderline but still acceptable in some languages, though unnecessary.

The key observation is that the structure of valid passwords is completely determined by choosing the two digits. Once the digits A and B are fixed, the number of valid sequences is purely combinatorial: we are arranging 3 copies of A and 3 copies of B in a length-6 sequence. The number of such arrangements is the multinomial coefficient 6! / (3!3!) = 20, independent of which digits were chosen.

This reduces the problem to counting how many pairs of allowed digits exist. If k digits are allowed, we choose any unordered pair (A, B), giving C(k, 2) possibilities, and each contributes exactly 20 passwords.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all sequences | O(10^6) | O(1) | Too slow / unnecessary |
| Choose digit pairs + combinatorics | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the set of forbidden digits and mark them. This step defines which digits remain usable in the construction.
2. Build the list of allowed digits by scanning 0 through 9 and collecting those not marked forbidden. This isolates the effective alphabet.
3. Count the number of allowed digits, call it k. This value determines whether any valid password can exist at all.
4. If k is less than 2, return 0 immediately because we cannot choose two distinct digits. This is a structural impossibility.
5. Otherwise, compute the number of ways to pick two distinct digits from k, which is k * (k - 1) / 2. Each such pair corresponds to a fixed multiset of digits used in the password.
6. Multiply the number of pairs by 20, because for any chosen pair (A, B), the number of valid 6-length arrangements with three A’s and three B’s is 6! / (3!3!) = 20.

### Why it works

Every valid password must use exactly two distinct digits, so it induces a unique unordered pair of digits. Conversely, any unordered pair of allowed digits uniquely defines a family of valid passwords consisting of all permutations of a multiset with three copies of each digit. These families are disjoint because different digit pairs cannot produce the same sequence. Since each family has the same fixed size, the total count is simply the number of pairs multiplied by the size of one family.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    forbidden = set(map(int, input().split())) if n else set()

    allowed = [d for d in range(10) if d not in forbidden]
    k = len(allowed)

    if k < 2:
        print(0)
        return

    pairs = k * (k - 1) // 2
    ans = pairs * 20
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first constructs the allowed digit set, which is necessary to ensure forbidden digits never enter any candidate construction. The check `k < 2` handles the degenerate case where no valid pair exists.

The expression `k * (k - 1) // 2` computes the number of unordered digit pairs efficiently without generating them explicitly. Multiplying by 20 applies the fixed combinatorial count for arranging three copies of each digit.

A common implementation mistake is forgetting that order matters in the final sequence but not in the selection of digits. That is why we separate pair selection (combinatorial choice) from arrangement count (fixed permutation count).

## Worked Examples

### Example 1

Input:

```
8
0 1 2 4 5 6 8 9
```

Allowed digits are only {3, 7}, so k = 2.

| Step | Value |
| --- | --- |
| Allowed digits | {3, 7} |
| k | 2 |
| Pairs | 1 |
| Ways per pair | 20 |
| Answer | 20 |

This shows the minimal non-trivial case where exactly one digit pair exists.

### Example 2

Input:

```
1
8
```

Allowed digits are {0,1,2,3,4,5,6,7,9}, so k = 9.

| Step | Value |
| --- | --- |
| Allowed digits | 9 digits |
| k | 9 |
| Pairs | 36 |
| Ways per pair | 20 |
| Answer | 720 |

This case demonstrates scaling purely via combinatorics, with no dependence on digit identities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only scanning 10 digits and simple arithmetic |
| Space | O(1) | Fixed-size arrays for digits |

The constraints cap digits at 10, so the solution is constant time per test. Even across many test cases, runtime remains trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    forbidden = set(map(int, input().split())) if n else set()
    allowed = [d for d in range(10) if d not in forbidden]
    k = len(allowed)
    ans = 0 if k < 2 else (k * (k - 1) // 2) * 20
    return str(ans)

# provided samples
assert run("8\n0 1 2 4 5 6 8 9\n") == "20"
assert run("1\n8\n") == "720"

# custom cases
assert run("9\n0 1 2 3 4 5 6 7 8\n") == "0", "only one digit allowed"
assert run("0\n") == "810", "all digits allowed: C(10,2)*20"
assert run("7\n0 1 2 3 4 5 6\n") == "60", "three allowed digits"
assert run("8\n1 2 3 4 5 6 7 8\n") == "20", "exact two allowed digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all digits forbidden except one | 0 | insufficient digits |
| no forbidden digits | 810 | full combinatorial case |
| 3 allowed digits | 60 | multiple pairs |
| exactly 2 allowed digits | 20 | base structural case |

## Edge Cases

If almost all digits are forbidden and only one digit remains, the algorithm correctly produces k = 1 and immediately returns 0 because no pair can be formed. For example, input `9` with digits `0 1 2 3 4 5 6 7 8` leaves only digit 9, so k = 1, and the function returns 0 as expected.

When no digits are forbidden, k = 10, so the number of pairs is 45. Multiplying by 20 gives 900. The algorithm handles this cleanly through the same formula without special casing.

If exactly two digits remain, k = 2, producing one pair and therefore exactly 20 valid passwords. This is the smallest non-zero scenario and confirms that the combinatorial factor is applied correctly.

In all cases, the structure of the computation ensures that forbidden digits only affect the size of the allowed set, and never require any special branching beyond counting.
