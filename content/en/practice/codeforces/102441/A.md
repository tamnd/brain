---
title: "CF 102441A - Template for Search"
description: "We are given a pattern containing lowercase letters, ?, and . A lowercase letter must appear literally, ? can represent any one lowercase letter, and can represent any sequence of lowercase letters, including the empty sequence."
date: "2026-08-09T01:31:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "A"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 425
verified: true
draft: false
---

[CF 102441A - Template for Search](https://codeforces.com/problemset/problem/102441/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pattern containing lowercase letters, `?`, and `*`. A lowercase letter must appear literally, `?` can represent any one lowercase letter, and `*` can represent any sequence of lowercase letters, including the empty sequence. We need to choose an actual lowercase string that matches the entire pattern, with the additional requirement that the resulting string is a palindrome. Among all possible choices, we want one with minimum length. If no palindrome can match the pattern, we print `-1`. The empty string counts as a valid palindrome.

The length of the pattern is at most 500. That is small enough for quadratic dynamic programming, but not small enough for enumerating possible output strings. Even an alphabet of only 26 letters gives exponentially many candidates. A cubic algorithm performs around (500^3 = 125) million basic state transitions in the worst case, which is already uncomfortable in Python, so we will go one step further and make the DP quadratic.

There are several cases where a simple greedy construction fails. For `ac?ba`, the two outer `a` characters are compatible, but after matching them we are left with `c?b`, whose ends cannot be made equal. The correct answer is `-1`. A careless algorithm that treats `?` as automatically fixing a mismatch could produce an invalid string.

For `*ac?ba`, the star cannot simply be ignored. The shortest valid palindrome is `abacaba`. The leading star consumes `ab`, while the fixed suffix `ba` produces the mirrored `ab` at the other end. An implementation that always treats `*` as an empty string misses the optimal construction.

For `*`, the answer is the empty string. Since `*` may consume zero characters, there is no reason to output even a single letter. An implementation that assumes every pattern character contributes to the answer would incorrectly output a nonempty string.

For `??`, the answer is `aa`. Both question marks may independently choose `a`, and the two positions must be equal because the final string is a palindrome. A careless implementation might unnecessarily force them to different characters or treat `?` as a literal symbol.

Finally, `a*b` has no solution when `a` and `b` differ. Every string matching this pattern starts with `a` and ends with `b`, while a palindrome must have equal first and last characters. The star cannot change that fact because it lies between the two fixed endpoints.

## Approaches

A direct brute-force solution would enumerate every palindrome of increasing length, check whether it matches the pattern, and stop at the first successful length. If a solution exists, the DP construction below gives one of length at most (2n), so we could restrict the search to that range. A palindrome of length (L) is determined by its first (\lceil L/2\rceil) characters, giving (26^{\lceil L/2\rceil}) candidates.

For (n=500), enumerating lengths from 0 through 1000 examines exactly

1+\frac{52(26^{500}-1)}{25}
]

candidate palindromes. Checking each candidate against the pattern takes linear time, so the total work is on the order of (n26^n). The reason this approach is conceptually correct is simple: every possible palindrome is eventually tested, and the first accepted one has minimum length. The problem is that the search space is astronomically large.

The key observation is that a palindrome gives us a natural way to split the pattern from its two ends. Suppose the current pattern interval is (s[l..r]). If both endpoints are ordinary characters or question marks, they must produce the same character. We can place that character at both ends of the answer and solve the inside interval.

The interesting case is a `*` at one endpoint. Consider a leading `*`. It may consume some string (X). Because the final answer is a palindrome, the corresponding suffix of the answer must be (reverse(X)). The rest of the pattern sits between those two copies. If we decide that a suffix (s[k..r]) is responsible for producing (X), the leading star can produce (reverse(X)), and the middle pattern (s[l+1..k-1]) must produce a palindrome.

For minimizing the length, the best string produced by an arbitrary pattern segment is especially simple. Every ordinary character contributes one character, every `?` contributes one chosen character, and every `*` can contribute nothing. Thus the minimum length of a string matching (s[k..r]) is just the number of non-star characters in that interval.

This turns the star transition into

\min_k
\left(
dp[l+1][k-1]
+
2\cdot count(k,r)
\right),
]

where `count(k,r)` is the number of non-star characters in (s[k..r]). There is also the possibility of making the leading star empty, giving `dp[l+1][r]`.

A direct implementation would try every (k) for every interval, giving (O(n^3)). The expression can be rearranged using prefix counts:

2P[r+1]
+
\left(dp[l+1][k-1]-2P[k]\right),
]

where (P[x]) is the number of non-star characters in the first (x) positions. For fixed (l), the minimum inside the parentheses can be maintained incrementally as (r) grows. The symmetric expression handles a trailing `*`. That removes the extra factor of (n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n26^n)) | (O(n)) | Too slow |
| Direct Interval DP | (O(n^3)) | (O(n^2)) | Conceptually valid, Python-unfriendly |
| Optimized Interval DP | (O(n^2)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Define `dp[l][r]` as the minimum length of a palindrome matching the pattern interval `s[l..r]`. If the interval is empty, its value is zero.
2. Precompute `pref[i]`, the number of non-star characters among `s[0..i-1]`. Then the minimum length of an arbitrary string matching `s[l..r]` is `pref[r+1] - pref[l]`, because stars can always be empty.
3. Process intervals in increasing right endpoint and decreasing left endpoint. This ordering makes `dp[i+1][j]`, `dp[i][j-1]`, and `dp[i+1][j-1]` available whenever they are needed.
4. If the interval consists of one character, a star contributes zero characters, while a letter or `?` contributes one character.
5. If `s[l]` is a star, one option is to make it empty and use `dp[l+1][r]`. The other option is to let it mirror a shortest string produced by some suffix `s[k..r]`. The resulting length is `2 * nonstars(k,r) + dp[l+1][k-1]`.
6. Maintain the minimum value of `dp[l+1][k-1] - 2 * pref[k]` while the right endpoint grows. This makes the best nonempty use of the leading star available in constant time for every interval.
7. If the left endpoint is not a star but `s[r]` is a star, apply the exact same idea from the other direction. Either the trailing star is empty, or it mirrors a shortest string produced by some prefix `s[l..k]`.
8. Maintain the corresponding minimum `2 * pref[k+1] + dp[k+1][r-1]` while the left endpoint moves inward. This gives the best use of a trailing star in constant time.
9. If neither endpoint is a star, they must be able to represent the same character. Two equal letters are compatible, a letter and `?` are compatible, and two `?` characters are compatible. When they are compatible, put the same chosen character on both ends and add two to `dp[l+1][r-1]`.
10. Alongside every DP value, store which transition produced it. For a star split, store the chosen split position `k`. This lets us reconstruct the actual palindrome after the DP finishes.
11. During reconstruction, a leading star split at `k` produces `reverse(T) + middle + T`, where `T` is the shortest string represented by `s[k..r]`. A trailing star produces `T + middle + reverse(T)`. Ordinary matching endpoints produce `c + middle + c`.
12. If `dp[0][n-1]` is infinite, no palindrome matches the pattern, so print `-1`. Otherwise reconstruct the stored decisions.

### Why it works

The invariant is that `dp[l][r]` is exactly the minimum length of a palindrome matching `s[l..r]`. When neither endpoint is a star, a palindrome forces the two endpoints to use the same character, so the ordinary transition considers every possible valid choice. When the left endpoint is a star, every matching palindrome either uses that star for zero characters or consumes a prefix that is the reverse of a string produced by some suffix of the remaining pattern. The latter is exactly what the split transition enumerates. The trailing-star case is symmetric.

For every split, we use the shortest possible string represented by the mirrored pattern segment. Making that segment longer can only add characters to both sides of the palindrome and cannot make the independent middle problem shorter. Thus the minimum-length choice for each split is sufficient. Since every possible use of the outer star is represented by some split, and every non-star endpoint pair is represented by the ordinary transition, the DP considers every feasible structure and takes the shortest one.

The reconstruction follows the same decomposition used by the DP. Every constructed piece is either a character mirrored around a smaller palindrome or a string mirrored around a smaller palindrome, so the result is always a palindrome. The corresponding pattern segments concatenate in the required order, so the result also matches the original pattern.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

# Transition types:
# 1 = skip left star
# 2 = use left star, split at arg[i][j]
# 3 = skip right star
# 4 = use right star, split at arg[i][j]
# 5 = match both endpoints
#
# dp[l][r] = minimum palindrome length matching s[l:r+1]

def solve_template(s):
    n = len(s)

    # pref[i] = number of non-'*' characters in s[:i]
    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (ch != '*')

    dp = [[INF] * n for _ in range(n)]
    kind = [[0] * n for _ in range(n)]
    arg = [[-1] * n for _ in range(n)]

    # For a fixed left endpoint i:
    # left_best[i] =
    # min_{k=i+1..j} dp[i+1][k-1] - 2*pref[k]
    #
    # left_arg[i] stores the k producing that minimum.
    left_best = [INF] * n
    left_arg = [-1] * n

    for j in range(n):
        # For this fixed j, while i decreases:
        # right_best =
        # min_{k=i..j-1} 2*pref[k+1] + dp[k+1][j-1]
        right_best = INF
        right_arg = -1

        for i in range(j, -1, -1):
            if i < j:
                # dp[i+1][j-1], with the empty interval handled explicitly.
                inner = 0 if i + 1 >= j else dp[i + 1][j - 1]

                # Add k = j to the running minimum for a leading star.
                candidate_left = inner - 2 * pref[j]
                if candidate_left < left_best[i]:
                    left_best[i] = candidate_left
                    left_arg[i] = j

                # Add k = i to the running minimum for a trailing star.
                candidate_right = 2 * pref[i + 1] + inner
                if candidate_right < right_best:
                    right_best = candidate_right
                    right_arg = i

            # Single-character interval.
            if i == j:
                if s[i] == '*':
                    dp[i][j] = 0
                    kind[i][j] = 1
                else:
                    dp[i][j] = 1
                    kind[i][j] = 5
                continue

            if s[i] == '*':
                # Option 1: make the left star empty.
                best = dp[i + 1][j]
                best_kind = 1
                best_arg = -1

                # Option 2: mirror a shortest string produced by s[k..j].
                candidate = 2 * pref[j + 1] + left_best[i]
                if candidate < best:
                    best = candidate
                    best_kind = 2
                    best_arg = left_arg[i]

                dp[i][j] = best
                kind[i][j] = best_kind
                arg[i][j] = best_arg

            elif s[j] == '*':
                # Option 1: make the right star empty.
                best = dp[i][j - 1]
                best_kind = 3
                best_arg = -1

                # Option 2: mirror a shortest string produced by s[i..k].
                candidate = right_best - 2 * pref[i]
                if candidate < best:
                    best = candidate
                    best_kind = 4
                    best_arg = right_arg

                dp[i][j] = best
                kind[i][j] = best_kind
                arg[i][j] = best_arg

            else:
                # Neither endpoint is a star.
                a = s[i]
                b = s[j]

                compatible = (
                    a == b or
                    a == '?' or
                    b == '?'
                )

                if compatible:
                    dp[i][j] = 2 + (
                        0 if i + 1 >= j else dp[i + 1][j - 1]
                    )
                    kind[i][j] = 5
                # Otherwise dp[i][j] stays INF.

    if dp[0][n - 1] >= INF:
        return "-1"

    def canonical(l, r):
        """Shortest concrete string matching s[l:r+1]."""
        out = []
        for p in range(l, r + 1):
            if s[p] == '*':
                continue
            if s[p] == '?':
                out.append('a')
            else:
                out.append(s[p])
        return ''.join(out)

    def build(l, r):
        if l > r:
            return ""

        t = kind[l][r]

        if l == r:
            if s[l] == '*':
                return ""
            if s[l] == '?':
                return "a"
            return s[l]

        if t == 1:
            # Left star is empty.
            return build(l + 1, r)

        if t == 2:
            # Left star mirrors the shortest string from k..r.
            k = arg[l][r]
            middle = build(l + 1, k - 1)
            x = canonical(k, r)
            return x[::-1] + middle + x

        if t == 3:
            # Right star is empty.
            return build(l, r - 1)

        if t == 4:
            # Right star mirrors the shortest string from l..k.
            k = arg[l][r]
            middle = build(k + 1, r - 1)
            x = canonical(l, k)
            return x + middle + x[::-1]

        # Ordinary compatible endpoints.
        a = s[l]
        b = s[r]

        if a == '?':
            c = b if b != '?' else 'a'
        else:
            c = a

        return c + build(l + 1, r - 1) + c

    return build(0, n - 1)

def main():
    s = input().strip()
    print(solve_template(s))

if __name__ == "__main__":
    main()
```

The prefix array is the first optimization. `pref[r + 1] - pref[l]` tells us how many actual characters a pattern interval must contribute if all its stars are made empty. This is enough because the split transitions only need the shortest possible string represented by the mirrored interval.

The `left_best` array stores the transformed minimum for every possible leading star. Instead of repeatedly evaluating every split `k`, the code adds the new possibility `k = j` when the right boundary advances. The expression involving `pref` separates the part depending on `j` from the part depending on `k`.

The `right_best` variable performs the symmetric optimization for a trailing star. It is reset for each right endpoint and updated as the left endpoint moves toward zero. At the moment `dp[i][j]` is computed, it contains exactly the best split whose first part starts at or after `i`.

The order of the nested loops is essential. The outer loop increases `j`, while the inner loop decreases `i`. Consequently, `dp[i+1][j]` has already been calculated earlier in the same column, and `dp[i+1][j-1]` was calculated in a previous column.

The reconstruction deliberately uses the shortest concrete string represented by a split interval. A `?` is replaced by `a`, while stars are skipped. Since those characters are mirrored around the recursively constructed middle, the exact choice for `?` does not affect optimality.

No integer overflow is possible in Python. In other languages, a normal integer type is already sufficient because the answer is at most (2n), while the DP uses `INF` only as a sentinel.

## Worked Examples

### Sample 1

The pattern is `*ac?ba`. Number the positions from 0 to 5.

| State `(l,r)` | Pattern interval | Transition | Mirrored string | Middle | Result |
| --- | --- | --- | --- | --- | --- |
| `(0,5)` | `*ac?ba` | Left star split at 4 | `ba` | `aca` | `abacaba` |
| `(1,3)` | `ac?` | Match `a` with `?` | `a` | `c` | `aca` |
| `(2,2)` | `c` | Single character | `c` | empty | `c` |
| empty | empty | Base case | empty | empty | empty |

At the top level, the suffix `ba` is matched by the pattern positions 4 and 5. The leading star consumes its reverse, `ab`. The remaining pattern is `ac?`, whose shortest palindrome is `aca`. Combining them gives `ab + aca + ba = abacaba`. The result matches the pattern because the leading star consumes `ab`, after which `ac?ba` consumes `acaba`.

### Sample 2

The pattern is `ac?ba`.

| State `(l,r)` | Pattern interval | Endpoint comparison | Inner interval | Result |
| --- | --- | --- | --- | --- |
| `(0,4)` | `ac?ba` | `a` and `a` match | `c?b` | depends on inner |
| `(1,3)` | `c?b` | `c` and `b` conflict | `?` | impossible |
| `(0,4)` | `ac?ba` | outer pair cannot be completed | impossible | `-1` |

The outer `a` characters are forced to match each other. Once they are removed, the inner pattern has fixed endpoints `c` and `b`, which cannot become equal. There is no star available to absorb either mismatch, so the entire pattern has no palindromic match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^2)) | There are (O(n^2)) DP states, and the star split minima are maintained incrementally in constant time |
| Space | (O(n^2)) | The DP values and reconstruction choices use quadratic memory |

For (n \le 500), there are only 250,000 DP states. Each state performs constant work after the running minima have been maintained, so the algorithm is easily within the intended bounds. The reconstruction is also linear in the size of the pattern plus the produced answer, and the produced answer has length at most (2n).

## Test Cases

```python
import io
import sys

# The submitted solution is represented by solve_template(s).

INF = 10**9

def solve_template(s):
    n = len(s)

    pref = [0] * (n + 1)
    for i, ch in enumerate(s):
        pref[i + 1] = pref[i] + (ch != '*')

    dp = [[INF] * n for _ in range(n)]
    kind = [[0] * n for _ in range(n)]
    arg = [[-1] * n for _ in range(n)]

    left_best = [INF] * n
    left_arg = [-1] * n

    for j in range(n):
        right_best = INF
        right_arg = -1

        for i in range(j, -1, -1):
            if i < j:
                inner = 0 if i + 1 >= j else dp[i + 1][j - 1]

                candidate_left = inner - 2 * pref[j]
                if candidate_left < left_best[i]:
                    left_best[i] = candidate_left
                    left_arg[i] = j

                candidate_right = 2 * pref[i + 1] + inner
                if candidate_right < right_best:
                    right_best = candidate_right
                    right_arg = i

            if i == j:
                if s[i] == '*':
                    dp[i][j] = 0
                    kind[i][j] = 1
                else:
                    dp[i][j] = 1
                    kind[i][j] = 5
                continue

            if s[i] == '*':
                best = dp[i + 1][j]
                best_kind = 1
                best_arg = -1

                candidate = 2 * pref[j + 1] + left_best[i]
                if candidate < best:
                    best = candidate
                    best_kind = 2
                    best_arg = left_arg[i]

                dp[i][j] = best
                kind[i][j] = best_kind
                arg[i][j] = best_arg

            elif s[j] == '*':
                best = dp[i][j - 1]
                best_kind = 3
                best_arg = -1

                candidate = right_best - 2 * pref[i]
                if candidate < best:
                    best = candidate
                    best_kind = 4
                    best_arg = right_arg

                dp[i][j] = best
                kind[i][j] = best_kind
                arg[i][j] = best_arg

            else:
                a = s[i]
                b = s[j]

                if a == b or a == '?' or b == '?':
                    dp[i][j] = 2 + (
                        0 if i + 1 >= j else dp[i + 1][j - 1]
                    )
                    kind[i][j] = 5

    if dp[0][n - 1] >= INF:
        return "-1"

    def canonical(l, r):
        out = []
        for p in range(l, r + 1):
            if s[p] == '*':
                continue
            out.append('a' if s[p] == '?' else s[p])
        return ''.join(out)

    def build(l, r):
        if l > r:
            return ""

        t = kind[l][r]

        if l == r:
            if s[l] == '*':
                return ""
            return 'a' if s[l] == '?' else s[l]

        if t == 1:
            return build(l + 1, r)

        if t == 2:
            k = arg[l][r]
            x = canonical(k, r)
            return x[::-1] + build(l + 1, k - 1) + x

        if t == 3:
            return build(l, r - 1)

        if t == 4:
            k = arg[l][r]
            x = canonical(l, k)
            return x + build(k + 1, r - 1) + x[::-1]

        a = s[l]
        b = s[r]
        if a == '?':
            c = b if b != '?' else 'a'
        else:
            c = a

        return c + build(l + 1, r - 1) + c

    return build(0, n - 1)

def run(inp: str) -> str:
    return solve_template(inp)

# Provided samples
assert run("*ac?ba") == "abacaba", "sample 1"
assert run("ac?ba") == "-1", "sample 2"

# Minimum-size and empty-palindrome case
assert run("*") == "", "a single star can match the empty string"

# Minimum-size question-mark case
assert run("?") == "a", "a question mark can choose any lowercase letter"

# All-equal values
assert run("aa") == "aa", "two equal fixed endpoints form a palindrome"

# Boundary case with a star and mismatching fixed endpoints
assert run("a*b") == "-1", "a palindrome cannot start with a and end with b"

# Star at the boundary can mirror the fixed prefix
assert run("abc*") == "abccba", "trailing star mirrors abc"

# Maximum-size all-equal input
assert run("a" * 500) == "a" * 500, "maximum-size fixed palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `*` | empty string | Minimum-size pattern and zero-length star |
| `?` | `a` | Single wildcard handling |
| `aa` | `aa` | Equal fixed endpoints |
| `a*b` | `-1` | Impossible fixed endpoint mismatch |
| `abc*` | `abccba` | Boundary star and mirrored prefix |
| `a` repeated 500 times | `a` repeated 500 times | Maximum input size and quadratic DP boundaries |

## Edge Cases

For `ac?ba`, the algorithm first handles the outer `a` and `a` as a compatible pair. The remaining interval is `c?b`. Since neither endpoint is a star and `c` cannot equal `b`, its DP value is infinite. That infinity propagates to the original interval, producing `-1`.

For `*ac?ba`, the leading star has two fundamentally different possibilities. It can be empty, which leaves `ac?ba` and ultimately fails. Or it can mirror a suffix. The optimal split selects the suffix `ba`. Its shortest matching string is exactly `ba`, so the star contributes `ab` on the left. The middle interval `ac?` becomes `aca`, giving `abacaba`.

For `*`, the single-character base case assigns length zero because the star can consume nothing. Reconstruction returns the empty string, and the program prints a blank line. This is the only situation where the answer itself has no characters.

For `??`, the two endpoints are compatible because both are wildcards. The reconstruction chooses `a` for both, producing `aa`. The choice of `a` is arbitrary, but using the same character is required by the palindrome condition.

For `a*b`, the outer characters are `a` and `b`, so the pattern cannot produce a palindrome. The star is internal and cannot alter either endpoint. The DP correctly reaches an impossible interval instead of trying to use the star to repair a mismatch it cannot repair.

For `abc*`, the right endpoint is a star. The optimal transition keeps the fixed prefix `abc` as the string mirrored by the star. The result is `abc + cba = abccba`, which matches `abc*` because the star consumes `cba`. The answer has length six, showing why simply deleting every star is not sufficient.

For the maximum-size input consisting of 500 `a` characters, there are no stars and every mirrored pair is compatible. The DP reduces to the ordinary palindrome recurrence, producing exactly 500 `a` characters. The case exercises the full quadratic state space and both interval boundaries.
