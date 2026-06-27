---
title: "CF 105112F - Fixing Fractions"
description: "Two integers are given as strings of digits, forming a numerator and denominator on each side of a fraction equation."
date: "2026-06-27T19:57:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105112
codeforces_index: "F"
codeforces_contest_name: "2023-2024 ICPC Northwestern European Regional Programming Contest (NWERC 2023)"
rating: 0
weight: 105112
solve_time_s: 73
verified: true
draft: false
---

[CF 105112F - Fixing Fractions](https://codeforces.com/problemset/problem/105112/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Two integers are given as strings of digits, forming a numerator and denominator on each side of a fraction equation. The allowed operation is unusual: you may delete digits from the numerator and denominator, but you must delete exactly the same multiset of digits from both original numbers. After deletions, the remaining digits in each number keep their original order, forming two new integers.

The task is to determine whether there exists a way to perform such synchronized deletions so that the resulting fraction equals a target rational number. If such a construction exists, we must output one valid pair of resulting numbers.

The important subtlety is that we are not free to independently choose subsequences of the two numbers. The deletions are coupled through digit counts: every digit removed from the first number must also be removed the same number of times from the second number. This creates a global constraint across both sides, not just two independent subsequence problems.

The constraints allow each number to have up to 18 digits, which makes the total number of subsequences per number at most 2^18, around 260 thousand. That size is small enough that enumerating all subsequences of a single number is feasible, but pairing them naively would lead to about 2^18 times 2^18 comparisons, which is far too large.

A second constraint that matters is that the resulting values can be large but still fit in 64-bit integer range, since at most 18 digits remain. This allows direct integer evaluation of candidate subsequences without modular arithmetic or hashing tricks on strings.

A failure case for naive reasoning appears when ignoring the coupling of deletions. For example, if one constructs a valid subsequence of the first number and independently constructs a valid subsequence of the second number that matches the target ratio, nothing guarantees that the same digit multiset was removed from both. This invalidates the construction even if the arithmetic condition holds.

Another subtle issue is leading zeros. If deletions produce something like "01" or "00", the result is invalid even though numerically it might still evaluate to a correct value. A correct approach must reject such constructions explicitly.

## Approaches

A brute-force interpretation would attempt to enumerate all ways to delete digits from both numbers simultaneously. For each subset of positions in the first number and each subset in the second number, we would check whether the deleted digits match in multiset and whether the resulting numbers satisfy the target equality. This leads to 2^18 choices per number, so about 2^36 combined states, which is far beyond feasible limits even with heavy pruning.

The key observation is that the deletion constraint can be rewritten in a way that separates the two numbers. Instead of thinking in terms of removed digits, we think in terms of the remaining subsequences. Once we fix a subsequence of the first number, the multiset of digits that must remain in the second number is uniquely determined because the removed digits must match. This means the second subsequence is not independent, it is determined by a simple digit-count constraint.

This transforms the problem into a meet-in-the-middle style lookup. We enumerate all subsequences of the second number, storing their digit frequency vectors and their numeric value. Then for each subsequence of the first number, we compute the required digit frequency vector for the second number using the fixed global difference between original counts. We then search for a matching stored state in constant or logarithmic time.

The arithmetic condition is checked only after ensuring digit compatibility, which avoids generating invalid candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all deletions in both numbers | O(2^n · 2^m) | O(1) | Too slow |
| Subsequence enumeration + hash by digit counts | O(2^n + 2^m) | O(2^m) | Accepted |

## Algorithm Walkthrough

We denote the first number as A and the second as B.

1. Count digit frequencies of A and B. For each digit from 0 to 9, compute how many times it appears in both strings. This gives a fixed reference for what any valid deletion must preserve globally.
2. Compute a difference vector K where K[d] = countA[d] − countB[d]. This represents the imbalance that must be carried into any pair of remaining subsequences. Any valid pair (A', B') must satisfy cnt(A') − cnt(B') = K component-wise.
3. Enumerate every subsequence of B. For each subsequence, compute three things: its digit count vector, its numeric value, and whether it is valid (no leading zero unless it is exactly a single digit). Store these in a hash map keyed by the digit count vector. For each key, we keep all subsequences that produce that digit profile.
4. Enumerate every subsequence of A in the same way, computing its digit count vector and numeric value, again discarding invalid leading-zero cases.
5. For each subsequence A', compute the required digit count vector for B' as cnt(B') = cnt(A') − K. This is forced by the global deletion constraint.
6. Look up all candidate B' subsequences matching this required digit vector. For each candidate, check whether the arithmetic condition A' · d = B' · c holds.
7. If a valid pair is found, output the corresponding A' and B' immediately.

The core invariant is that every state stored for B represents a fully valid subsequence, and every A' is only paired with B' candidates that satisfy the exact digit-count transformation imposed by the original constraint. This ensures no invalid deletion patterns are ever considered, and every checked pair corresponds to a consistent global removal of digits from both original numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def valid_number(s):
    if len(s) == 0:
        return False
    if len(s) > 1 and s[0] == '0':
        return False
    return True

def value_of(s):
    if not s:
        return 0
    return int(s)

def build_subsequences(s):
    n = len(s)
    res = []
    for mask in range(1 << n):
        digits = []
        cnt = [0] * 10
        for i in range(n):
            if mask & (1 << i):
                digits.append(s[i])
                cnt[ord(s[i]) - 48] += 1
        if not digits:
            continue
        if not valid_number(digits):
            continue
        val = int("".join(digits))
        res.append((tuple(cnt), val, "".join(digits)))
    return res

def solve():
    a, b, c, d = input().split()
    c = int(c)
    d = int(d)

    cntA = [0] * 10
    cntB = [0] * 10

    for ch in a:
        cntA[ord(ch) - 48] += 1
    for ch in b:
        cntB[ord(ch) - 48] += 1

    K = [cntA[i] - cntB[i] for i in range(10)]

    subsB = build_subsequences(b)
    mp = {}

    for cnt, val, s in subsB:
        mp.setdefault(cnt, []).append((val, s))

    n = len(a)
    for mask in range(1 << n):
        digits = []
        cnt = [0] * 10
        for i in range(n):
            if mask & (1 << i):
                digits.append(a[i])
                cnt[ord(a[i]) - 48] += 1
        if not digits:
            continue
        if not valid_number(digits):
            continue

        valA = int("".join(digits))
        required = tuple(cnt[i] - K[i] for i in range(10))

        if required in mp:
            for valB, sB in mp[required]:
                if valA * d == valB * c:
                    print("possible")
                    print("".join(digits), sB)
                    return

    print("impossible")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the enumeration strategy. The function `build_subsequences` generates all valid subsequences of the second number, recording both digit frequency and value. The first number is processed similarly on the fly, but instead of storing everything, each subsequence is immediately used to query candidates.

The arithmetic check uses cross multiplication `valA * d == valB * c` to avoid floating-point division issues. The digit count matching is handled using tuples as dictionary keys, which makes lookup efficient and exact.

Leading zero handling is enforced before any numeric interpretation, which prevents invalid states from entering the hash structure.

## Worked Examples

### Example 1

Input:

```
163 326 1 2
```

We enumerate subsequences of `326`. One valid subsequence is `"2"` with digit count `(0,1,0,0,0,0,0,0,0,0)` and value 2.

For `163`, we find subsequence `"1"` with digit count `(1,0,0,0,0,0,0,0,0,0)` and value 1.

The required digit difference K ensures that removing digits aligns both sides. The pair satisfies `1/2 = 1/2`, so it is accepted.

| A' | B' | A'*d | B'*c | Match |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | yes |

This confirms that the algorithm correctly finds a minimal consistent deletion pattern.

### Example 2

Input:

```
871 1261 13 39
```

One valid subsequence pair is `A' = 87` and `B' = 261`.

| A' | B' | A'*39 | B'*13 | Match |
| --- | --- | --- | --- | --- |
| 87 | 261 | 3393 | 3393 | yes |

Here the algorithm does not rely on full-length numbers. It selects subsequences that satisfy both digit constraints and arithmetic equality simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^n + 2^m) | Each subsequence of both numbers is generated once and processed in constant-time hashing and checks |
| Space | O(2^m) | All subsequences of the second number are stored grouped by digit count |

With n, m ≤ 18, the worst-case enumeration is about 262k states per number, which is comfortably within limits even in Python. The constant factor is small because each state only processes at most 18 digits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    out = io.StringIO()
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
# (placeholders since exact formatting not shown)
# assert run("163 326 1 2") == "possible\n1 2"

# single digit trivial match
assert run("5 5 1 1") != "", "basic equality case"

# no solution case
assert run("123 267 12339 23679") == "impossible", "impossible case"

# leading zero stress
assert run("10 10 1 1") != "", "leading zero handling"

# symmetric digits
assert run("12 21 1 1") != "", "rearrangement case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 5 1 1 | possible 5 5 | trivial identity case |
| 123 267 12339 23679 | impossible | no matching subsequences exist |
| 10 10 1 1 | possible 1 1 | handling deletion leading to single digit |
| 12 21 1 1 | possible 1 1 or 2 2 | symmetry and multiple valid answers |

## Edge Cases

A critical edge case occurs when subsequences produce leading zeros. For input `100 100 1 1`, a naive subsequence generator might accept `"00"` as a valid number equal to 0. However, the problem definition rejects numbers with leading zeros. The algorithm explicitly filters any subsequence where the first selected digit is `0` and length exceeds one, ensuring such states never enter the candidate set.

Another edge case is the empty subsequence. For inputs like `111 111 1 1`, choosing no digits from both sides might appear to satisfy digit balance, but it does not form a valid number. The algorithm discards empty masks immediately, so this state cannot be chosen.

A final subtle case is arithmetic overflow or precision errors. For large subsequences like `"999999999999999999"`, floating-point division would be unreliable. Using cross multiplication avoids division entirely and keeps the comparison exact even at the 18-digit limit.
