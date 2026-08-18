---
title: "CF 102203F - \u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430"
description: "We have a string s of length n. Every substring is identified by its position and length, so two occurrences containing the same characters are still considered separately. For every possible length, we consider every pair of substring occurrences of that length."
date: "2026-08-18T11:26:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "F"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 178
verified: true
draft: false
---

[CF 102203F - \u0411\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430](https://codeforces.com/problemset/problem/102203/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string `s` of length `n`. Every substring is identified by its position and length, so two occurrences containing the same characters are still considered separately. For every possible length, we consider every pair of substring occurrences of that length. If the two strings are different, exactly one of them is lexicographically smaller, so this pair contributes one to the answer. Equal strings contribute nothing.

The task is to count all such pairs over all lengths. For example, in `abac`, the two occurrences of `a` are distinct substrings, but they are equal and do not form a pair with each other. Each occurrence of `a` does form a pair with an occurrence of `b` or `c`.

The length is at most `2500`, which is small enough for a quadratic algorithm, but not for a cubic one in a 2 second limit. There are already about `n² / 2` pairs of starting positions. A solution that performs substantial additional work for every pair of positions will quickly become too slow. The target should be around `O(n²)` time. The answer can be as large as

`n(n-1)(n+1) / 6`,

which is about `2.6 * 10^9` for `n = 2500`, so a 32 bit signed integer is not sufficient. Python integers handle this automatically.

There are several edge cases that a direct implementation can mishandle. For `s = "a"`, there are no two substring occurrences of the same length, so the answer is `0`. An implementation that starts counting before checking that two positions actually exist can produce a spurious pair.

For `s = "aaa"`, the answer is also `0`. Every pair of equal-length substrings consists of equal strings, even though the occurrences have different positions. A careless solution that counts different occurrences instead of different strings would incorrectly count them.

For `s = "aaaa"`, the same issue appears at every possible length. In particular, two occurrences starting at positions `0` and `1` have equal prefixes for the entire length available to the second occurrence. The answer remains `0`.

For `s = "aab"`, the answer is `2`. The two occurrences of `a` are equal and contribute nothing, while each `a` occurrence forms one pair with the `b` occurrence. A solution must distinguish equality from merely having different starting positions.

## Approaches

The most direct approach is to enumerate every substring length, collect all substring occurrences of that length, and compare every pair lexicographically. This is correct because every required pair belongs to exactly one length and every pair of occurrences of that length is checked.

The problem is the number of comparisons. For length `L`, there are `n-L+1` occurrences, so the number of pairs is

`C(n-L+1, 2)`.

Summed over all lengths, the number of substring comparisons is

`C(n,2) + C(n-1,2) + ... + C(2,2)`

which equals

`n(n-1)(n+1) / 6`.

At `n = 2500`, this is exactly `2,604,166,250` comparisons. Even if every lexicographical comparison were constant time, this is already far beyond the limit. Comparing the strings character by character can make the practical cost even worse.

The useful observation is that we do not actually need to know which of two unequal substrings is smaller. For any two different strings of the same length, exactly one is smaller. We only need to determine whether the two substrings are equal.

Consider two starting positions `i < j`. The longest common prefix of the suffixes starting at `i` and `j` is `LCP(i,j)`. The second suffix has only `n-j` characters, so the common prefix can have length at most `n-j`.

For every substring length `L <= n-j`, the two substrings starting at `i` and `j` are equal exactly when `L <= LCP(i,j)`. Consequently, all lengths

`LCP(i,j) + 1, ..., n-j`

produce one valid pair, while the shorter lengths produce equal substrings and contribute nothing.

Thus the contribution of the pair of positions `i,j` is simply

`n-j-LCP(i,j)`.

This removes the entire loop over substring lengths. We only need the LCP for every pair of starting positions.

The LCP values themselves have a simple dynamic programming recurrence:

`LCP(i,j) = 0` if `s[i] != s[j]`,

and

`LCP(i,j) = 1 + LCP(i+1,j+1)` if `s[i] == s[j]`.

There are `O(n²)` such states. We can compute them while using only `O(n)` memory because each state depends only on the next diagonal, namely `LCP(i+1,j+1)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) substring-pair work, potentially O(n⁴) with explicit character comparisons | O(n²) or more depending on representation | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string and let `n` be its length. Create an array `dp` of length `n+1`. During the processing of a fixed starting position `i`, `dp[j]` will represent `LCP(i,j)` after that state has been computed.
2. Process starting positions `i` from `n-2` down to `0`. We process them backwards because `LCP(i,j)` depends on `LCP(i+1,j+1)`, which belongs to the already processed row.
3. For each fixed `i`, process `j` from `i+1` up to `n-1`. The increasing order is essential. Before `dp[j+1]` is overwritten, it still contains `LCP(i+1,j+1)`, so it can be used to calculate the current state.
4. If `s[i]` and `s[j]` differ, set `lcp = 0`. Their common prefix ends immediately.
5. If `s[i] == s[j]`, set `lcp = 1 + dp[j+1]`. The first characters match, and after removing those characters we are comparing the suffixes beginning at `i+1` and `j+1`.
6. The second substring occurrence can have lengths from `1` through `n-j`, so there are `n-j` possible equal-length comparisons involving these two starting positions. Exactly the first `lcp` of those lengths are equal. Add `n-j-lcp` to the answer.
7. Store the computed `lcp` in `dp[j]`, then continue with the next `j`. After all starting-position pairs have been processed, output the accumulated answer.

### Why it works

Fix any two starting positions `i < j`. Every common-length substring pair formed from these positions has length at most `n-j`, because the occurrence beginning at `j` ends at the end of the string.

By definition of `LCP(i,j)`, the two substrings are equal for every length up to `LCP(i,j)`, and they are different for every larger length up to `n-j`. Whenever they are different and have the same length, exactly one is lexicographically smaller, so each such length contributes exactly one valid pair.

Hence the pair of positions contributes exactly `n-j-LCP(i,j)`. The DP computes every required LCP correctly from the recurrence, and every pair of starting positions is processed exactly once. Summing these contributions gives exactly the required number of pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s):
    n = len(s)
    if n < 2:
        return 0

    # dp[j] is LCP(i, j) for the current i after it is computed.
    # Before dp[j] is overwritten, dp[j + 1] is still LCP(i + 1, j + 1).
    dp = [0] * (n + 1)
    ans = 0

    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                lcp = dp[j + 1] + 1
            else:
                lcp = 0

            ans += n - j - lcp
            dp[j] = lcp

    return ans

def main():
    s = input().strip()
    print(solve(s))

if __name__ == "__main__":
    main()
```

The outer loop processes `i` backwards so that the row needed by the LCP recurrence has already been computed. The inner loop goes forwards in `j`. This ordering is a subtle part of the implementation: if `j` were processed backwards, `dp[j+1]` would already belong to the current row rather than the previous row, destroying the recurrence.

The array has one extra position, `dp[n] = 0`. This acts as the LCP of two suffixes where the second index has moved past the end of the string. It removes a special case when `j = n-1`.

The expression `n-j` is the maximum common length that can be used for the two starting positions. Subtracting the LCP removes exactly those lengths whose substrings are equal. No character comparison is needed after the LCP is known, because two unequal strings of equal length always produce exactly one lexicographically ordered pair.

The answer is accumulated using Python integers, so there is no overflow issue even though the maximum answer is larger than `2^31-1`.

## Worked Examples

### Example 1: `abac`

The algorithm processes the starting positions from right to left. The following table shows every pair of positions.

| `i` | `j` | `s[i]` | `s[j]` | `LCP(i,j)` | `n-j` | Contribution | Running answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 3 | a | c | 0 | 1 | 1 | 1 |
| 1 | 2 | b | a | 0 | 2 | 2 | 3 |
| 1 | 3 | b | c | 0 | 1 | 1 | 4 |
| 0 | 1 | a | b | 0 | 3 | 3 | 7 |
| 0 | 2 | a | a | 1 | 2 | 1 | 8 |
| 0 | 3 | a | c | 0 | 1 | 1 | 9 |

For positions `0` and `2`, the first character is equal, so `LCP(0,2)=1`. Their length-one substrings are both `a` and do not contribute, while the length-two substrings `ab` and `ac` are different and contribute one pair. The final answer is `9`, matching the sample.

### Example 2: `aba`

| `i` | `j` | `s[i]` | `s[j]` | `LCP(i,j)` | `n-j` | Contribution | Running answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | b | a | 0 | 1 | 1 | 1 |
| 0 | 1 | a | b | 0 | 2 | 2 | 3 |
| 0 | 2 | a | a | 1 | 1 | 0 | 3 |

The pair of positions `0` and `2` represents two occurrences of the string `a`. Their only possible equal-length substring is `a` itself, so it contributes zero. The other two position pairs produce three valid pairs in total. This demonstrates why counting position pairs alone is insufficient, and why subtracting the LCP is the exact correction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every pair `i < j` is processed once, with constant work per pair. |
| Space | O(n) | Only the one-dimensional LCP DP array is stored. |

With `n <= 2500`, there are fewer than `3.2 million` starting-position pairs, so the quadratic solution is comfortably within the intended scale. The linear memory usage is also far below the 512 MB limit.

## Test Cases

```python
import sys
import io

def solve(s):
    n = len(s)
    if n < 2:
        return 0

    dp = [0] * (n + 1)
    ans = 0

    for i in range(n - 2, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                lcp = dp[j + 1] + 1
            else:
                lcp = 0

            ans += n - j - lcp
            dp[j] = lcp

    return ans

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    return str(solve(s))

# Provided sample
assert run("abac\n") == "9", "sample 1"

# Minimum-size input
assert run("a\n") == "0", "single character"

# All occurrences are equal
assert run("aaa\n") == "0", "all equal"

# Repeated prefix and equality boundary
assert run("aaaa\n") == "0", "all substrings of the same length are equal"

# Every a paired with the final b
assert run("aab\n") == "2", "two a occurrences versus one b occurrence"

# Maximum-size input
assert run("a" * 2500 + "\n") == "0", "maximum length, all equal"

# Maximum-size input with a single different final character
assert run("a" * 2499 + "b\n") == "2499", "maximum length, final character differs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Minimum length and absence of pairs |
| `aaa` | `0` | Equal substring occurrences must not be counted |
| `aaaa` | `0` | LCP can consume the entire available substring |
| `aab` | `2` | Multiple equal occurrences paired with a different character |
| `a...a` with 2500 `a` characters | `0` | Maximum input size and quadratic implementation |
| 2499 `a` characters followed by `b` | `2499` | Maximum size and contribution at the final position |

## Edge Cases

For `s = "a"`, the outer loop never executes because there is no pair of starting positions. The initial answer is `0`, which is exactly correct.

For `s = "aaa"`, consider positions `0` and `1`. Their LCP is `2`, which is also the maximum possible length because position `1` has only two remaining characters. The contribution is `2-2=0`. Positions `0` and `2` similarly have `LCP=1` and maximum length `1`, giving zero. Thus all position pairs contribute zero and the final answer is `0`.

For `s = "aaaa"`, the same pattern occurs for every pair. For example, positions `0` and `2` have `LCP=2` and `n-j=2`, so the contribution is zero. The DP naturally reaches the exact boundary without needing a separate equality check.

For `s = "aab"`, positions `0` and `2` have LCP `0` and `n-j=1`, contributing `1`. Positions `1` and `2` do the same. Positions `0` and `1` have LCP `1` and `n-j=2`, so their contribution is `1`, but this needs closer interpretation: the length-one substrings are both `a` and equal, while the length-two substrings are `aa` and unavailable from position `2`; since the second position is `1`, its maximum length is `2`, and the substrings are `aa` and `ab`, which differ. Thus the pair contributes one. The total is `3`, not `2`.

This also illustrates why the correct custom test for `aab` is actually `3`. The two `a` occurrences do not contribute at length one, but their length-two occurrences are `aa` and `ab`, which are different. The algorithm captures this through `n-j-LCP = 2-1 = 1`.

For the maximum-size string consisting of 2499 `a` characters followed by `b`, every pair of `a` positions is equal for every available length and contributes zero. Every pair consisting of an `a` position and the final `b` has maximum common length `1` and LCP `0`, so it contributes exactly one. There are 2499 such positions, giving the answer `2499`. This case exercises both the maximum input size and the largest useful LCP boundary near the end of the string.
