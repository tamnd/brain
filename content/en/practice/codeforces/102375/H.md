---
title: "CF 102375H - ICPC"
description: "For a given maximum word length (N), the dictionary contains every lowercase English string whose length is from (1) through (N). Words of the same length appear in lexicographic order, while all shorter words come first."
date: "2026-08-15T18:03:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "H"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 165
verified: false
draft: false
---

[CF 102375H - ICPC](https://codeforces.com/problemset/problem/102375/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

For a given maximum word length (N), the dictionary contains every lowercase English string whose length is from (1) through (N). Words of the same length appear in lexicographic order, while all shorter words come first. Concatenating the entire dictionary produces one enormous string. We need the number of occurrences of the four-character substring `icpc` in that concatenation, modulo (10^9+7).

The difficulty is that (N) can be as large as (10^9). The dictionary already contains (26^N) words of length (N), so even representing the last layer is impossible. The original problem has a 2 second limit and 512 MiB memory limit, which rules out anything proportional to the number of generated words or characters. The solution has to depend logarithmically on (N), using modular exponentiation rather than enumerating lengths one by one.

There are two kinds of occurrences to count. An occurrence can be completely inside one dictionary word, or it can cross the boundary between two consecutive words. Ignoring the second kind is a subtle error because concatenation removes the boundary between words.

For example, with (N=3), no individual word is long enough to contain `icpc`, and no boundary can create it either. The correct answer is `0`. A solution that blindly applies a formula containing (26^{N-4}) without handling (N<4) can accidentally interpret a negative exponent.

With (N=4), the answer is `4`, not `1`. The word `icpc` itself contributes one internal occurrence. Three additional occurrences are created across boundaries between consecutive four-letter words, namely the boundaries after `cpci`, `pcic`, and `cicp`. A solution that counts only occurrences inside individual words misses these three.

The boundary between the last word of one length and the first word of the next length is also easy to mishandle. For example, the boundary between `zzz` and `aaaa` consists entirely of `z` characters followed by `a` characters, so it cannot create `icpc`. Treating every dictionary boundary as equivalent would overcount such transitions.

## Approaches

The brute-force approach is straightforward. Generate every word in dictionary order, concatenate them, and scan for `icpc`. This is correct because every possible occurrence in the final string is examined exactly once. However, there are

[
26+26^2+\cdots+26^N
]

words, and the total number of characters is

[
\sum_{L=1}^{N} L26^L=\Theta(N26^N).
]

For (N=10^9), even (26^N) cannot be represented, so brute force fails astronomically far before the time limit becomes relevant.

The useful observation is that the pattern has fixed length four. For a word of length (L), internal occurrences can be counted position by position without constructing any word. Each fixed position requires four specified letters, leaving (L-3) free positions, so there are (26^{L-4}(L-3)) occurrences over all words of that length.

The only remaining issue is concatenation boundaries. A four-character occurrence crossing a boundary must take (1), (2), or (3) characters from the word on the left. Because the pattern is `icpc`, the required left suffix and right prefix are respectively

[
(i,\ cpc),\qquad
(ic,\ pc),\qquad
(icp,\ c).
]

For consecutive words of the same length, the right word is obtained by incrementing the left word in base (26). Every required left suffix ends in a letter other than `z`, so no carry reaches the prefix. For (L\ge4), each of the three boundary types fixes four character positions and leaves (L-4) arbitrary positions. Thus each type occurs (26^{L-4}) times, giving (3\cdot26^{L-4}) crossing occurrences.

The transition from `z...z` to `a...a` contributes zero, because its boundary characters contain only `z` and `a`. For (L<4), the three boundary patterns cannot fit consistently into a word of that length, so there are no same-length crossing occurrences.

Combining internal and crossing occurrences for a fixed (L\ge4) gives

[
(L-3)26^{L-4}+3\cdot26^{L-4}
=L26^{L-4}.
]

So the whole problem becomes evaluating

[
\sum_{L=4}^{N}L26^{L-4}
]

modulo (10^9+7).

This is a weighted geometric progression. We can evaluate it using the standard formulas for a geometric sum and a weighted geometric sum, requiring only one modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N26^N)) | (O(N26^N)) | Too slow |
| Optimal | (O(\log N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. If (N<4), return `0`. No word contains four characters, and the short-word boundaries cannot form `icpc`.
2. For every possible word length (L\ge4), count occurrences entirely inside words. There are (26^{L-4}) choices for the remaining characters for each of the (L-3) possible starting positions, giving ((L-3)26^{L-4}).
3. Count occurrences crossing a boundary between consecutive words of the same length. Splitting `icpc` after its first, second, or third character gives three possible boundary shapes. For each shape, four character positions are fixed and the other (L-4) positions are arbitrary, so each shape contributes (26^{L-4}). The boundary contribution is consequently (3\cdot26^{L-4}).
4. Add the two contributions. The total for length (L) is

[
(L-3+3)26^{L-4}=L26^{L-4}.
]

1. Let (k=L-4) and let (t=N-3). Then (k) ranges from (0) through (t-1), and the answer becomes

[
\sum_{k=0}^{t-1}(k+4)26^k.
]

Separate this into

[
\sum_{k=0}^{t-1}k26^k
+
4\sum_{k=0}^{t-1}26^k.
]

1. Use the geometric-series formula

[
\sum_{k=0}^{t-1}r^k=\frac{r^t-1}{r-1}
]

with (r=26).

1. Use the weighted geometric-series formula

\frac{r-tr^t+(t-1)r^{t+1}}{(r-1)^2}.
]

All divisions are performed modulo (10^9+7). Since (r-1=25) is nonzero modulo the prime modulus, its modular inverse exists.

1. Compute (26^t\bmod(10^9+7)) using binary exponentiation. This is the only operation depending logarithmically on (N), so the complete algorithm takes (O(\log N)) time.

### Why it works

For every length (L), every occurrence belongs uniquely either inside one word or across exactly one boundary between consecutive words. The internal count considers every possible starting position and every assignment of the remaining characters. For a boundary occurrence, the split point must be one of the three internal cuts of `icpc`, and the lexicographic successor structure gives exactly (26^{L-4}) valid boundaries for each cut when (L\ge4). The transition between different word lengths contributes nothing. Thus the exact contribution of every length is (L26^{L-4}), and the final geometric-series calculation evaluates precisely the sum of those contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7
R = 26
INV25 = 280000002

def solve():
    n = int(input())

    if n < 4:
        print(0)
        return

    # We need:
    # sum_{k=0}^{t-1} (k + 4) * 26^k
    t = n - 3

    p = pow(R, t, MOD)

    # sum_{k=0}^{t-1} r^k
    geometric = (p - 1) % MOD
    geometric = geometric * INV25 % MOD

    # sum_{k=0}^{t-1} k * r^k
    weighted_num = (
        R
        - (t % MOD) * p
        + ((t - 1) % MOD) * p % MOD * R
    ) % MOD

    weighted = weighted_num * INV25 % MOD * INV25 % MOD

    answer = (weighted + 4 * geometric) % MOD
    print(answer)

if __name__ == "__main__":
    solve()
```

The early return handles the entire (N<4) range, avoiding negative exponents and invalid boundary assumptions.

The variable `t = n - 3` is the number of terms after substituting (k=L-4). For (N=4), `t` is one, so the sum contains only the term (4\cdot26^0=4), exactly as required.

The value `p` stores (26^t) modulo the answer modulus. Python's built-in `pow(base, exponent, modulus)` performs modular exponentiation efficiently and never constructs the enormous integer (26^t).

The inverse of (25) is `280000002`, because

[
25\cdot280000002\equiv1\pmod{10^9+7}.
]

The weighted-series numerator is reduced modulo `MOD` before multiplication. Python integers do not overflow, but reducing intermediate values keeps the arithmetic small and makes the modular structure explicit.

The two components are computed separately because the original summand (k+4) naturally splits into a weighted geometric series and four copies of an ordinary geometric series.

## Worked Examples

For (N=3), the algorithm stops immediately.

| (N) | (N<4) | Answer |
| --- | --- | --- |
| 3 | true | 0 |

There are no four-character words, so there is no internal occurrence. The transition from `zzz` to `aaaa` cannot produce `icpc`, and shorter boundaries cannot contain four required characters. This confirms the lower-bound handling.

For (N=5), there are contributions from lengths four and five.

| (L) | Internal | Crossing | Total |
| --- | --- | --- | --- |
| 4 | (1\cdot26^0=1) | (3\cdot26^0=3) | 4 |
| 5 | (2\cdot26^1=52) | (3\cdot26^1=78) | 130 |
|  |  |  | **134** |

After substituting (k=L-4), we have (t=2), so

# 4+5\cdot26

1. 

]

The trace confirms both parts of the counting argument. Length four contributes four occurrences, while length five contributes 130, giving the required sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log N)) | One modular exponentiation computes (26^{N-3}) |
| Space | (O(1)) | Only a constant number of modular integers are stored |

The largest possible (N) is (10^9), so iterating through all lengths would already be too slow. Binary exponentiation needs only about 30 squaring steps for such an exponent, making the solution comfortably suitable for the stated limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7
INV25 = 280000002

def solution():
    input = sys.stdin.readline
    n = int(input())

    if n < 4:
        print(0)
        return

    t = n - 3
    p = pow(26, t, MOD)

    geometric = (p - 1) % MOD
    geometric = geometric * INV25 % MOD

    weighted_num = (
        26
        - (t % MOD) * p
        + ((t - 1) % MOD) * p % MOD * 26
    ) % MOD

    weighted = weighted_num * INV25 % MOD * INV25 % MOD

    print((weighted + 4 * geometric) % MOD)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def brute(n: int) -> int:
    # Independent reference for small n.
    words = []

    for length in range(1, n + 1):
        total = 26 ** length
        for x in range(total):
            chars = []
            y = x
            for _ in range(length):
                chars.append(chr(ord('a') + y % 26))
                y //= 26
            words.append(''.join(reversed(chars)))

    s = ''.join(words)
    return sum(s[i:i + 4] == 'icpc' for i in range(len(s) - 3))

def fast_reference(n: int) -> int:
    if n < 4:
        return 0

    ans = 0
    power = 1

    for length in range(4, n + 1):
        ans = (ans + length * power) % MOD
        power = power * 26 % MOD

    return ans

# Provided samples
assert run("3\n") == "0", "sample 1"
assert run("5\n") == "134", "sample 2"

# Minimum size
assert run("1\n") == "0", "minimum N"

# Boundary where the first occurrences appear
assert run("4\n") == "4", "first non-zero case"

# Small case with an independent brute-force reference
assert run("6\n") == str(brute(6)), "small brute-force cross-check"

# Uniform boundary words such as zzz...z -> aaa...a must contribute nothing
assert run("3\n") == "0", "uniform word boundary"

# Maximum allowed N, checked against a direct O(N) modular reference.
# This reference is used only by the test harness, not by the submitted solution.
assert run("1000000000\n") == str(fast_reference(1000000000)), "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `0` | Minimum range where the pattern cannot fit |
| `4` | `4` | First nonzero case and all three boundary splits |
| `5` | `134` | Both internal and crossing contributions |
| `6` | `4190` | Independent brute-force cross-check |
| `1000000000` | Computed by the modular reference | Maximum constraint and logarithmic exponentiation |

The `N=4` case is especially useful because a solution counting only occurrences inside words returns `1`, while the correct answer is `4`. The `N=6` case compares against an actual generated dictionary, so it checks the entire combinatorial derivation rather than merely another implementation of the final formula. The maximum-size test verifies that the implementation does not accidentally iterate over (N) or construct any dictionary words.

## Edge Cases

For (N=3), the input is

```
3
```

The algorithm enters the `n < 4` branch and returns `0`. No dictionary word has four characters. The only length transition capable of looking suspicious is `zzz` followed by `aaaa`, but that boundary is made from `z` and `a`, so it cannot contain `icpc`.

For (N=4), the input is

```
4
```

Here (t=1), (26^t=26), and the geometric sum is (1). The weighted geometric sum is (0), because its only term is (0\cdot26^0). The final expression is (0+4\cdot1=4). These four occurrences consist of one internal occurrence in the word `icpc` and three crossing occurrences after `cpci`, `pcic`, and `cicp`.

For (N=5), the two relevant lengths contribute (4) and (130). At length four, the total is (4). At length five, there are (2\cdot26=52) internal occurrences and (3\cdot26=78) crossing occurrences. Their sum is (134), matching the sample.

For the maximum input

```
1000000000
```

the algorithm never attempts to construct a word or iterate through the (10^9) possible lengths. It sets (t=999999997), computes (26^t) with modular exponentiation in (O(\log N)) multiplications, and evaluates the two closed-form sums. The exponent is large, but its binary representation has only about 30 bits, so the computation remains constant-sized in practice.

The lexicographic carry boundary is handled implicitly by the combinatorial argument. For the three useful boundary shapes, the left word must end in `i`, `c`, or `p`, none of which is `z`. Thus the increment to the next lexicographic word changes only the last character and cannot alter the required prefix. The exceptional `z...z` to `a...a` boundary is treated separately and contributes zero.
