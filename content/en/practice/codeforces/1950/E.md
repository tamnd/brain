---
title: "CF 1950E - Nearly Shortest Repeating Substring"
description: "We are given a string s of length n. We want to find the smallest possible length L such that there exists a pattern string k of length L, repeated exactly n / L times, producing a string c of length n, and c differs from s in at most one position."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "number-theory", "strings"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 1500
weight: 1950
solve_time_s: 82
verified: true
draft: false
---

[CF 1950E - Nearly Shortest Repeating Substring](https://codeforces.com/problemset/problem/1950/E)

**Rating:** 1500  
**Tags:** brute force, implementation, number theory, strings  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string `s` of length `n`. We want to find the smallest possible length `L` such that there exists a pattern string `k` of length `L`, repeated exactly `n / L` times, producing a string `c` of length `n`, and `c` differs from `s` in at most one position.

In other words, after changing at most one character of `s`, the resulting string must become perfectly periodic with period length `L`. Among all valid periods, we need the shortest one.

The key observation from the statement is that the repeated string must cover the entire string length, so the candidate period length must divide `n`.

The total length across all test cases is at most `2 · 10^5`. This is large enough that comparing every possible pattern against every possible substring naively can become expensive. An algorithm around `O(n · d(n))`, where `d(n)` is the number of divisors, is completely safe because even the largest numbers below `2 · 10^5` have relatively few divisors. An `O(n²)` approach is too slow in the worst case.

Several edge cases are easy to mishandle.

Consider:

```
n = 4
s = abaa
```

The answer is `1`, because `"aaaa"` differs in exactly one position. A solution that only checks whether the original string is already periodic would incorrectly reject period `1`.

Consider:

```
n = 4
s = abba
```

The answer is `4`. Neither period `1` nor period `2` can be fixed with a single character change. A solution that greedily chooses the most frequent character in each residue class may incorrectly conclude that period `2` works.

Consider:

```
n = 6
s = aaabaa
```

The answer is `1`. The string differs from `"aaaaaa"` in exactly one position. This case shows that a single bad character may appear anywhere, not necessarily inside the first period block.

Another subtle case is:

```
n = 8
s = ababcbab
```

Period `2` does not work. The mismatch appears in several comparisons involving the same wrong character. Counting pairwise disagreements instead of counting actual character changes can overestimate the required modifications.

## Approaches

A natural brute-force approach is to try every divisor `L` of `n`, generate every possible period string of length `L`, and check whether repeating it matches `s` with at most one mismatch.

The problem is that there are exponentially many possible period strings. Even restricting ourselves to period strings appearing inside `s` does not immediately help. The search space becomes enormous.

We need to exploit the fact that only one character may be wrong.

Suppose we fix a candidate period length `L`. Every position `i` belongs to residue class `i mod L`. In a perfectly periodic string, all characters in the same residue class must be equal.

For example, with `L = 3`:

```
positions: 0 1 2 3 4 5 6 7 8
residues : 0 1 2 0 1 2 0 1 2
```

Each residue class must contain a single repeated character.

If the entire string can be repaired with at most one modification, then after grouping positions by residue class, all but possibly one position already agree with the final periodic pattern.

The crucial observation is that if at most one character is wrong, then the correct period string must be equal to one of the existing blocks of length `L`.

Why?

Assume the final periodic string uses period `k`. Since only one position in the whole string is wrong, every block except possibly one is identical to `k`. Thus some block of the original string must already equal `k`.

This immediately reduces the search space. For a fixed divisor `L`, we only need to test period candidates taken from existing blocks of length `L`.

There are `n / L` blocks. Testing all of them naively would be too expensive, but because only one block can contain the erroneous character, it is enough to check the first two blocks.

If a valid period exists, then all correct blocks equal the true period. At most one block differs. Among the first two blocks, at least one must be correct.

So for each divisor `L`, we test:

```
candidate = first block
candidate = second block (if it exists)
```

For each candidate, we compare the repeated pattern against the whole string and count mismatches. If the mismatch count is at most one, then `L` is valid.

This turns the problem into checking a small number of candidates for every divisor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in period length | O(L) | Too slow |
| Optimal | O(n · d(n)) | O(L) | Accepted |

## Algorithm Walkthrough

1. Enumerate all divisors `L` of `n` in increasing order.
2. For each divisor, split the string into blocks of length `L`.
3. Construct a candidate period using the first block.
4. Compare the repeated candidate against the entire string and count mismatches.
5. If the mismatch count is at most one, return `L` immediately because divisors are processed in increasing order.
6. Otherwise, if there is more than one block, construct a second candidate using the second block.
7. Compare this second candidate against the entire string.
8. If the mismatch count is at most one, return `L`.
9. Continue with the next divisor.
10. If no smaller divisor works, `L = n` always works because the string itself can be used as the period.

### Why it works

Assume some divisor `L` is valid. Let `k` be the true period of the repaired string.

Since only one character in the entire string may be incorrect, at most one block of length `L` differs from `k`. Every other block is exactly equal to `k`.

Among the first two blocks, at least one cannot be the corrupted block. Therefore at least one of them equals the true period `k`.

When the algorithm tests that block as a candidate, the repeated candidate is exactly the repaired string. Its mismatch count against the original string is at most one, so the algorithm accepts `L`.

Conversely, if the algorithm accepts a candidate, then repeating that candidate produces a string differing from `s` in at most one position. This is exactly the condition required by the problem.

Since divisors are processed in increasing order, the first accepted divisor is the minimum possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def works(s, n, d, pat):
    mism = 0
    for i in range(n):
        if s[i] != pat[i % d]:
            mism += 1
            if mism > 1:
                return False
    return True

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        divisors = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                divisors.append(i)
                if i * i != n:
                    divisors.append(n // i)
            i += 1

        divisors.sort()

        answer = n

        for d in divisors:
            block_cnt = n // d

            cand1 = s[:d]
            if works(s, n, d, cand1):
                answer = d
                break

            if block_cnt > 1:
                cand2 = s[d:2 * d]
                if works(s, n, d, cand2):
                    answer = d
                    break

        print(answer)

solve()
```

The helper function `works` checks whether a candidate period can generate a string differing from `s` in at most one position. Instead of explicitly building the repeated string, it compares character `s[i]` with `pat[i % d]`. This avoids extra memory and keeps the check linear.

The divisor generation uses the standard square-root enumeration. Each divisor pair is added together, then the list is sorted so periods are tested from smallest to largest.

For each divisor, the algorithm only examines the first two blocks. This is the key optimization. The correctness argument shows that if a valid period exists, one of these two blocks must equal the true period.

The early exit inside `works` is important. Once more than one mismatch appears, that candidate can never become valid, so there is no reason to continue scanning the string.

## Worked Examples

### Example 1

Input:

```
4
abaa
```

Candidate divisors are `1, 2, 4`.

| d | Candidate | Mismatches | Valid |
| --- | --- | --- | --- |
| 1 | a | 1 | Yes |

The repeated string is `"aaaa"`. It differs from `"abaa"` only at position 2, so the answer is `1`.

This example demonstrates why we must allow one modification. The string is not originally periodic with period `1`, but it becomes periodic after fixing a single character.

### Example 2

Input:

```
8
hshahaha
```

Divisors are `1, 2, 4, 8`.

| d | Candidate | Mismatches | Valid |
| --- | --- | --- | --- |
| 1 | h | 3 | No |
| 2 | hs | 4 | No |
| 2 | ha | 1 | Yes |

The second block `"ha"` is the correct period.

Repeating it gives:

```
hahahaha
```

which differs from the original string in exactly one position.

This trace illustrates why checking only the first block is insufficient. The corrupted character may lie inside the first block, making the second block the correct period.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · d(n)) | Each divisor performs at most two full scans of the string |
| Space | O(d(n)) | Storage for the divisor list |

For every divisor, we test at most two candidates, and each test scans the string once. The number of divisors of any integer up to `2 · 10^5` is small, so the total work remains comfortably within the limits. The memory usage is negligible compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    def works(s, n, d, pat):
        mism = 0
        for i in range(n):
            if s[i] != pat[i % d]:
                mism += 1
                if mism > 1:
                    return False
        return True

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        divs = []
        i = 1
        while i * i <= n:
            if n % i == 0:
                divs.append(i)
                if i * i != n:
                    divs.append(n // i)
            i += 1

        divs.sort()

        for d in divs:
            if works(s, n, d, s[:d]):
                ans.append(str(d))
                break

            if n // d > 1 and works(s, n, d, s[d:2*d]):
                ans.append(str(d))
                break

    print("\n".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old
    return out.getvalue()

# provided sample
assert run(
"""5
4
abaa
4
abba
13
slavicgslavic
8
hshahaha
20
stormflamestornflame
"""
) == """1
4
13
2
10
"""

# minimum size
assert run(
"""1
1
a
"""
) == """1
"""

# all equal
assert run(
"""1
6
aaaaaa
"""
) == """1
"""

# one wrong character in otherwise period-1 string
assert run(
"""1
6
aaabaa
"""
) == """1
"""

# first block corrupted, second block is correct
assert run(
"""1
8
hshahaha
"""
) == """2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, s=a` | `1` | Smallest possible input |
| `aaaaaa` | `1` | Already perfectly periodic |
| `aaabaa` | `1` | Single incorrect character anywhere in string |
| `hshahaha` | `2` | Correct period comes from second block |

## Edge Cases

Consider:

```
1
4
abaa
```

For divisor `1`, the candidate period is `"a"`. Repeating it produces `"aaaa"`. The mismatch count is exactly one. The algorithm immediately returns `1`.

This verifies that we correctly handle strings that become periodic after a single modification.

Consider:

```
1
4
abba
```

For divisor `1`, the mismatch count exceeds one. For divisor `2`, both candidates `"ab"` and `"ba"` produce more than one mismatch. Only divisor `4` succeeds.

The algorithm returns `4`, showing that it does not mistakenly accept a shorter period simply because some residue classes look similar.

Consider:

```
1
8
hshahaha
```

The first block is `"hs"` and the second block is `"ha"`. The true period is `"ha"`, but the first block contains the corrupted character. Testing only the first block would fail. The algorithm also tests the second block, finds only one mismatch, and correctly returns `2`.

This is exactly the situation that motivates checking both of the first two blocks.

Consider:

```
1
6
aaabaa
```

For divisor `1`, the repeated string `"aaaaaa"` differs in exactly one position. The algorithm counts mismatches globally rather than counting disagreements between residue classes, so the answer is correctly reported as `1`. This avoids overcounting the effect of a single bad character.
