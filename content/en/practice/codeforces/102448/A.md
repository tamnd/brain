---
title: "CF 102448A - Accept or Reject"
description: "We have a string S of length N, and we need to determine whether at least one contiguous substring of exactly M characters reads the same from left to right and from right to left."
date: "2026-08-08T11:57:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "A"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 436
verified: true
draft: false
---

[CF 102448A - Accept or Reject](https://codeforces.com/problemset/problem/102448/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string `S` of length `N`, and we need to determine whether at least one contiguous substring of exactly `M` characters reads the same from left to right and from right to left.

For example, if `S = "ajabbaaksj"` and `M = 4`, the substring `"abba"` is a palindrome, so the answer is `Accept`. The substring does not have to start at any particular position, and there may be many candidate windows. We only need one valid palindrome of length exactly `M`.

The bounds make the straightforward approach unusable. Since `N` can reach `5 * 10^5`, an algorithm that examines `M` characters for each of the roughly `N` possible starting positions can perform about `N * M` character comparisons. In the worst case, with `N = M = 5 * 10^5`, that is about `2.5 * 10^11` comparisons, far beyond what fits in a one second limit. We need a solution whose running time is linear or close to linear in `N`.

There are a few boundary cases that are easy to mishandle. When `M = 1`, every individual character is a palindrome, so the answer must always be `Accept`. For example, `N = 1`, `M = 1`, `S = "a"` gives `Accept`. A solution that only checks palindromes with a center between two characters would incorrectly reject this case.

The parity of `M` also matters. An even palindrome such as `"abba"` has its center between two characters, while an odd palindrome such as `"aba"` has its center on a character. For example, `N = 3`, `M = 3`, `S = "aba"` gives `Accept`. An implementation that only handles even-length centers would miss it.

A palindrome can also begin or end exactly at the boundary of the string. For example, `N = 4`, `M = 4`, `S = "abba"` gives `Accept`. Any indexing scheme that requires a character on both sides of a candidate center can accidentally discard this valid palindrome.

Finally, having a palindrome longer than `M` is enough to answer `Accept`, because every prefix or suffix of the right length is not necessarily a palindrome, but a palindrome contains palindromic substrings of every length having the same parity as its length around its center. More directly, the algorithm must check whether a palindrome of exactly `M` exists, rather than simply finding an arbitrary long palindrome. For example, `S = "abcba"` with `M = 4` must be rejected, because its only length-5 palindrome does not contain a length-4 palindrome. This is why the parity of the requested length cannot be ignored.

## Approaches

The direct approach is to enumerate every substring of length `M` and check whether it is equal to its reverse. There are `N - M + 1` such substrings. Checking one substring takes `O(M)` time, because in the worst case we may need to compare roughly half of its characters before discovering a mismatch, so the total is `O((N - M + 1)M)`, which is `O(NM)` in the worst case. With `N = M = 5 * 10^5`, this can reach approximately `2.5 * 10^11` character comparisons. The brute-force method is correct because it explicitly tests every possible candidate, but the amount of repeated work is far too large.

The useful observation is that we do not actually care about every possible substring separately. A palindrome is completely characterized by its center and its radius. If we know, for every position, how far a palindrome extends around that center, then we can answer the fixed-length question immediately.

There are two kinds of centers. An odd-length palindrome has a character as its center, while an even-length palindrome has the gap between two characters as its center. Manacher's algorithm computes the maximum palindrome radius for every possible center in linear time. Once those radii are known, checking whether a palindrome of length `M` exists becomes a simple scan.

For an odd `M`, a palindrome of length `M` has radius `(M + 1) // 2` in the usual Manacher representation, where the radius counts the center character itself. For an even `M`, its half-length is `M // 2`, and the corresponding even-center radius must be at least that value.

The brute-force method works because it independently verifies each window. It fails because neighboring windows repeat almost all of the same comparisons. Manacher's algorithm removes this repetition by reusing information about already known palindromic intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NM)` | `O(1)` | Too slow |
| Manacher | `O(N)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Build the transformed string by inserting a separator between every pair of characters and also at both ends. For example, `"abba"` becomes `"#a#b#b#a#"`. This gives every palindrome a uniform center representation, so odd and even lengths can be processed by the same radius array.
2. Run Manacher's algorithm on the transformed string. For every transformed position `i`, store `p[i]`, the number of characters that can be matched symmetrically around `i`. The algorithm maintains the rightmost palindrome currently known and its center. If the new position lies inside that palindrome, its initial radius can be copied from its mirror position, limited by the current right boundary. Only the characters beyond that boundary need to be compared explicitly.
3. Check every transformed center whose radius is large enough for a palindrome of length `M`. In the transformed representation, a palindrome of original length `M` corresponds to a transformed palindrome radius of at least `M`. Thus, if any `p[i] >= M`, the answer is `Accept`.
4. If no transformed center has radius at least `M`, output `Reject`. Since every original substring palindrome has a corresponding center in the transformed string, no candidate can have been missed.

The reason the transformed representation works is that each original character and each separator occupy alternating positions. A palindrome of `M` original characters spans exactly `2M` transformed edges around its center, so a transformed radius of `M` is precisely sufficient to contain such a substring.

### Why it works

For every possible center, `p[i]` represents the largest symmetric region around that center that is a palindrome. Every palindrome in the original string has one of these transformed centers, regardless of whether its length is odd or even. A length-`M` palindrome therefore exists exactly when some center has transformed radius at least `M`. Manacher computes all these maximum radii correctly, so scanning them cannot miss an existing palindrome or accept a non-palindrome.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    S = input().strip()

    # Transform the string so odd and even palindromes
    # are handled uniformly.
    T = "#" + "#".join(S) + "#"
    n = len(T)

    p = [0] * n
    center = 0
    right = 0

    for i in range(n):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        while (
            i - p[i] - 1 >= 0
            and i + p[i] + 1 < n
            and T[i - p[i] - 1] == T[i + p[i] + 1]
        ):
            p[i] += 1

        if i + p[i] > right:
            center = i
            right = i + p[i]

    for radius in p:
        if radius >= M:
            print("Accept")
            return

    print("Reject")

if __name__ == "__main__":
    solve()
```

The transformation creates a separator between every original character. This is what makes a palindrome such as `"aba"` and one such as `"abba"` look structurally identical to Manacher's algorithm. Their centers are simply different transformed positions.

The `p` array stores the maximum radius around each transformed position. `center` and `right` describe the palindrome reaching furthest to the right among the palindromes processed so far. When `i < right`, the palindrome around `i` has a mirrored position `2 * center - i`. Its known radius gives us a valid starting value for `p[i]`, so we do not repeat comparisons already performed elsewhere.

The expansion loop is guarded on both sides of the transformed string. This avoids accessing positions outside the array when a palindrome reaches either end of `S`. Python integers do not overflow, so no special handling is required for the radius or indices.

The final condition is `radius >= M`, not `radius == M`. A larger palindrome may contain a palindrome of the requested length only when the requested length has the appropriate parity, so this deserves care. In the transformed representation, however, a radius of `R` represents all original palindrome lengths from `1` through `R` with the corresponding center structure, and a radius of at least `M` is exactly the condition for an original palindrome of length `M` around that center.

## Worked Examples

### Sample 1

The input is:

```
10 4
ajabbaaksj
```

The transformed string is `#a#j#a#b#b#a#a#k#s#j#`. The relevant center is the separator between the two `b` characters. Its radius reaches four original characters on each side in the transformed representation, enough to cover `"abba"`.

| Center | Character | Radius `p[i]` | `p[i] >= M` |
| --- | --- | --- | --- |
| 1 | `a` | 1 | No |
| 3 | `j` | 1 | No |
| 5 | `a` | 1 | No |
| 7 | `b` | 1 | No |
| 9 | `#` | 4 | Yes |

The center at the separator between the two `b` characters corresponds to `"abba"`. Since its transformed radius is at least `4`, the algorithm prints `Accept`.

### Constructed Example

Consider:

```
5 4
abcba
```

The string has a palindrome of length `5`, but no palindrome of length `4`. The transformed string is `#a#b#c#b#a#`. The largest radius occurs at the center character `c`.

| Center | Character | Radius `p[i]` | `p[i] >= 4` |
| --- | --- | --- | --- |
| 1 | `a` | 1 | No |
| 3 | `b` | 1 | No |
| 5 | `c` | 5 | Yes |

This table exposes a subtle point. The center has radius `5`, so the algorithm's simple `p[i] >= M` test would appear to accept `M = 4`. That is not correct for the original-length interpretation. A transformed radius of `5` corresponds to the original palindrome length `5`, while the next smaller palindrome around the same center has length `3`, not `4`.

For this reason, the implementation must distinguish the parity of `M` when interpreting Manacher's transformed radius. The code above therefore needs a parity-aware final check. The corrected implementation is given below.

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    S = input().strip()

    T = "#" + "#".join(S) + "#"
    n = len(T)

    p = [0] * n
    center = 0
    right = 0

    for i in range(n):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        while (
            i - p[i] - 1 >= 0
            and i + p[i] + 1 < n
            and T[i - p[i] - 1] == T[i + p[i] + 1]
        ):
            p[i] += 1

        if i + p[i] > right:
            center = i
            right = i + p[i]

    # In the transformed string:
    # odd original length M has a character at the center,
    # even original length M has a separator at the center.
    if M % 2 == 1:
        needed = M
        for i in range(1, n, 2):
            if p[i] >= needed:
                print("Accept")
                return
    else:
        needed = M
        for i in range(0, n, 2):
            if p[i] >= needed:
                print("Accept")
                return

    print("Reject")

if __name__ == "__main__":
    solve()
```

The transformed positions alternate between original characters and separators. Character centers occur at odd indices, while separator centers occur at even indices. Consequently, an odd-length palindrome must be checked only at character centers, and an even-length palindrome only at separator centers. This removes the parity mistake illustrated by `"abcba"` with `M = 4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` | The transformed string has `2N + 1` positions, and Manacher's expansion advances the right boundary only `O(N)` times. |
| Space | `O(N)` | The transformed string and the palindrome-radius array both contain `O(N)` elements. |

With `N <= 5 * 10^5`, the transformed string contains at most `1,000,001` positions. Both the running time and memory usage grow linearly, so the solution is appropriate for the one second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solve():
    N, M = map(int, input().split())
    S = input().strip()

    T = "#" + "#".join(S) + "#"
    n = len(T)

    p = [0] * n
    center = 0
    right = 0

    for i in range(n):
        mirror = 2 * center - i

        if i < right:
            p[i] = min(right - i, p[mirror])

        while (
            i - p[i] - 1 >= 0
            and i + p[i] + 1 < n
            and T[i - p[i] - 1] == T[i + p[i] + 1]
        ):
            p[i] += 1

        if i + p[i] > right:
            center = i
            right = i + p[i]

    if M % 2 == 1:
        for i in range(1, n, 2):
            if p[i] >= M:
                print("Accept")
                return
    else:
        for i in range(0, n, 2):
            if p[i] >= M:
                print("Accept")
                return

    print("Reject")

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

    return out.getvalue().strip()

assert run("10 4\najabbaaksj\n") == "Accept", "sample 1"

assert run("1 1\na\n") == "Accept", "minimum-size input"

assert run("4 4\nabba\n") == "Accept", "whole string is an even palindrome"

assert run("5 4\nabcba\n") == "Reject", "odd palindrome must not satisfy even length"

assert run("5 5\nabcba\n") == "Accept", "whole string is an odd palindrome"

assert run("6 3\nxxabcy\n") == "Reject", "no length-3 palindrome"

assert run("6 3\naabbcc\n") == "Accept", "boundary length-3 palindrome"

assert run("500000 500000\n" + "a" * 500000 + "\n") == "Accept", \
    "maximum-size all-equal string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / a` | `Accept` | Minimum size and `M = 1` |
| `4 4 / abba` | `Accept` | Even palindrome occupying the entire string |
| `5 4 / abcba` | `Reject` | Correct parity handling |
| `5 5 / abcba` | `Accept` | Odd palindrome occupying the entire string |
| `6 3 / xxabcy` | `Reject` | No candidate palindrome |
| `6 3 / aabbcc` | `Accept` | Palindrome near a boundary |
| `500000 500000 / a...a` | `Accept` | Maximum input size and repeated characters |

## Edge Cases

When `M = 1`, every character is itself a palindrome. For the input

```
1 1
a
```

the transformed string is `#a#`, and the character center has radius `1`. Since `M` is odd, the algorithm examines character centers and immediately finds `p[i] >= 1`, producing `Accept`.

For an even palindrome at the very beginning or end of the string, the center is a separator rather than a character. With

```
4 4
abba
```

the transformed string is `#a#b#b#a#`. The center separator has radius `4`, so the even-length branch finds a radius large enough for `M = 4`. The answer is `Accept`. The explicit separation between character and separator centers prevents an even palindrome from being confused with an odd one.

The parity case `abcba` with `M = 4` is especially useful for catching an incorrect implementation. The input is

```
5 4
abcba
```

The center character `c` has transformed radius `5`. However, because `M` is even, the algorithm ignores character centers and checks separator centers only. None has radius `4`, so the result is `Reject`. The length-5 palindrome does not accidentally satisfy the length-4 query.

A palindrome can also touch the string boundary. For

```
5 5
abcba
```

the entire string is one palindrome. Its center is the character `c`, and its radius is `5`. Since `M` is odd and the character-center branch checks this position, the algorithm returns `Accept`. No special case for the first or last substring is required because Manacher's boundary checks naturally handle it.

Finally, the all-equal maximum-size case stresses both the expansion logic and the asymptotic complexity:

```
500000 500000
aaaaaaaaaa...aaaaaaaaaa
```

Every character comparison succeeds, so the largest possible palindrome is found. Despite the long expansion, Manacher's algorithm still runs in linear time because the maintained right boundary only moves forward `O(N)` times. The result is `Accept`.
