---
title: "CF 182D - Common Divisors"
description: "We are given two lowercase strings. A string d is called a divisor of another string s if s can be formed by concatenating d several times in a row. For example, \"ab\" divides \"ababab\" because repeating \"ab\" three times gives the full string."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "hashing", "implementation", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 182
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 117 (Div. 2)"
rating: 1400
weight: 182
solve_time_s: 96
verified: true
draft: false
---

[CF 182D - Common Divisors](https://codeforces.com/problemset/problem/182/D)

**Rating:** 1400  
**Tags:** brute force, hashing, implementation, math, strings  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two lowercase strings. A string `d` is called a divisor of another string `s` if `s` can be formed by concatenating `d` several times in a row.

For example, `"ab"` divides `"ababab"` because repeating `"ab"` three times gives the full string. On the other hand, `"aba"` does not divide `"ababab"` because repeating it never produces the target exactly.

The task is to count how many strings divide both input strings at the same time.

The string lengths are at most `10^5`, which immediately rules out expensive substring generation combined with repeated reconstruction. Anything close to `O(n^2)` character work can become too slow when both strings are large. A solution doing tens of billions of operations will not finish within the time limit. We need something close to linear or `O(n log n)`.

The tricky part is that matching prefixes is not enough. A candidate divisor must repeat perfectly across the entire string.

Consider this input:

```
ababab
abab
```

The common divisor is `"ab"`, not `"abab"`. A careless implementation might only check whether both strings start with the same prefix and accidentally count `"abab"` even though it cannot tile `"ababab"` completely.

Another easy mistake appears when the candidate length does not divide the full string length.

```
aaa
aa
```

The only common divisor is `"a"`.

A naive approach might treat `"aa"` as valid because both strings begin with `"aa"`, but `"aa"` cannot generate `"aaa"` through repetition.

Single-character strings are also important:

```
a
a
```

The answer is `1`, because `"a"` divides both strings.

Different patterns with the same character counts can also break incorrect solutions:

```
abab
abba
```

The answer is `0`.

Both strings contain the same letters, but no repeating base string generates both exactly.

## Approaches

The most direct solution is to try every possible substring as a candidate divisor. For each candidate, we check whether repeating it reconstructs both strings exactly.

Suppose the first string has length `n` and the second has length `m`. In the worst case, there are `O(min(n, m))` candidate lengths. For every candidate, rebuilding and comparing strings costs up to `O(n + m)`.

That gives a total complexity around `O(min(n, m) * (n + m))`.

With lengths near `10^5`, this becomes far too expensive. A worst-case input could require around `10^10` character operations.

The key observation is that a valid divisor length must divide both string lengths.

If a string of length `k` generates a string of length `n`, then `k` must divide `n` exactly. So instead of checking every possible length, we only need to check the common divisors of the two lengths.

For example, if the strings have lengths `8` and `16`, the only possible divisor lengths are common divisors of `8` and `16`, namely `1`, `2`, `4`, and `8`.

That reduces the number of candidates dramatically. The number of divisors of an integer is small, usually at most a few hundred for values around `10^5`.

For each valid length `k`, we take the prefix of length `k` from the first string and verify that repeating it reconstructs both strings.

The verification itself can be done efficiently using repetition and equality comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(min(n,m) × (n+m)) | O(n+m) | Too slow |
| Optimal | O((n+m) × d) | O(n+m) | Accepted |

Here `d` is the number of common divisors of the string lengths, which is very small in practice.

## Algorithm Walkthrough

1. Read the two input strings.
2. Compute their lengths `n` and `m`.
3. Iterate through all integers `k` from `1` to `min(n, m)`.
4. Skip any `k` that does not divide both `n` and `m`.

A repeating block of length `k` can only generate strings whose lengths are multiples of `k`.
5. Take the first `k` characters of the first string as the candidate divisor.
6. Rebuild the first string by repeating the candidate `n // k` times.
7. Rebuild the second string by repeating the candidate `m // k` times.
8. If both rebuilt strings match the originals exactly, increment the answer.
9. Print the final count.

### Why it works

Every valid divisor string must appear as a prefix of both strings, because repetition always starts from the beginning. Its length must also divide both string lengths exactly.

The algorithm checks every possible common divisor length and verifies whether the corresponding prefix truly generates both strings through repetition. No valid divisor can be missed, because every divisor must satisfy these properties. No invalid divisor can be counted, because reconstruction guarantees exact equality with both original strings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s1 = input().strip()
    s2 = input().strip()

    n = len(s1)
    m = len(s2)

    ans = 0

    for k in range(1, min(n, m) + 1):
        if n % k != 0 or m % k != 0:
            continue

        candidate = s1[:k]

        if candidate * (n // k) == s1 and candidate * (m // k) == s2:
            ans += 1

    print(ans)

solve()
```

The loop checks every possible divisor length. The divisibility condition is essential because a repeating block cannot generate a string whose length is not a multiple of the block length.

The candidate divisor is always taken from the prefix of `s1`. Any valid divisor must begin at the start of the string, so checking arbitrary substrings is unnecessary.

The reconstruction step is where correctness is enforced. Even if two strings share the same prefix, the repeated pattern may fail later in the string. Building the repeated string and comparing against the original catches these cases cleanly.

One subtle detail is using `.strip()` when reading input. Without it, the newline character becomes part of the string and breaks all comparisons.

Another easy mistake is forgetting to check both strings separately. A candidate might divide `s1` correctly but fail on `s2`.

## Worked Examples

### Example 1

Input:

```
abcdabcd
abcdabcdabcdabcd
```

| k | Divides both lengths? | Candidate | Rebuild s1 | Rebuild s2 | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | Yes | `"a"` | `"aaaaaaaa"` | `"aaaaaaaaaaaaaaaa"` | No |
| 2 | Yes | `"ab"` | `"abababab"` | `"abababababababab"` | No |
| 4 | Yes | `"abcd"` | `"abcdabcd"` | `"abcdabcdabcdabcd"` | Yes |
| 8 | Yes | `"abcdabcd"` | `"abcdabcd"` | `"abcdabcdabcdabcd"` | Yes |

Answer: `2`

This trace shows why matching prefixes alone is insufficient. `"ab"` appears at the start of both strings but does not tile them correctly.

### Example 2

Input:

```
aaa
aa
```

| k | Divides both lengths? | Candidate | Rebuild s1 | Rebuild s2 | Valid? |
| --- | --- | --- | --- | --- | --- |
| 1 | Yes | `"a"` | `"aaa"` | `"aa"` | Yes |
| 2 | No | - | - | - | Skipped |

Answer: `1`

This example demonstrates why divisor lengths matter. `"aa"` cannot be considered because length `2` does not divide `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) × d) | `d` is the number of common divisor lengths checked |
| Space | O(n+m) | Temporary repeated strings during comparison |

The number of divisors for values up to `10^5` is very small, so the solution easily fits within the time limit. Even with maximum input sizes, the amount of repeated work remains manageable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        s1 = input().strip()
        s2 = input().strip()

        n = len(s1)
        m = len(s2)

        ans = 0

        for k in range(1, min(n, m) + 1):
            if n % k != 0 or m % k != 0:
                continue

            candidate = s1[:k]

            if candidate * (n // k) == s1 and candidate * (m // k) == s2:
                ans += 1

        return str(ans)

    return solve()

# provided sample
assert run("abcdabcd\nabcdabcdabcdabcd\n") == "2", "sample 1"

# minimum-size input
assert run("a\na\n") == "1", "single character strings"

# no common divisors
assert run("abab\nabba\n") == "0", "same letters, different structure"

# repeated same character
assert run("aaaaaa\naaa\n") == "2", "divisors are 'a' and 'aaa'"

# boundary length divisibility
assert run("aaa\naa\n") == "1", "length mismatch prevents 'aa'"

# identical strings
assert run("xyzxyz\nxyzxyz\n") == "2", "divisors are 'xyz' and full string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `1` | Minimum valid input |
| `abab / abba` | `0` | Shared prefixes are not enough |
| `aaaaaa / aaa` | `2` | Multiple valid divisor lengths |
| `aaa / aa` | `1` | Length divisibility condition |
| `xyzxyz / xyzxyz` | `2` | Identical strings with multiple divisors |

## Edge Cases

Consider the input:

```
aaa
aa
```

The algorithm checks `k = 1` and `k = 2`.

For `k = 1`, the candidate is `"a"`. Repeating it produces both original strings exactly, so it is counted.

For `k = 2`, the algorithm skips immediately because `2` does not divide `3`.

This prevents the incorrect inclusion of `"aa"`.

Now consider:

```
abab
abba
```

Possible common divisor lengths are `1`, `2`, and `4`.

For `k = 1`, the candidate is `"a"`. Repeating it gives `"aaaa"` and `"aaaa"`, which fail.

For `k = 2`, the candidate is `"ab"`. Repeating it gives `"abab"` and `"abab"`. The second reconstruction does not match `"abba"`.

For `k = 4`, the candidate is `"abab"`. Repeating it once gives `"abab"` for the first string but `"abab"` does not match `"abba"`.

The answer correctly becomes `0`.

Finally, consider identical strings:

```
abcabc
abcabc
```

The algorithm checks lengths `1`, `2`, `3`, and `6`.

Only `"abc"` and `"abcabc"` reconstruct both strings correctly.

This confirms that the algorithm counts both primitive divisors and the full string itself when valid.
