---
title: "CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b"
description: "We have two strings of the same length, (s) and (t). The string (s) describes the current order of boxes from top to bottom, while (t) describes an earlier order. We may transform (s) in two ways."
date: "2026-08-09T00:22:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 236
verified: false
draft: false
---

[CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b](https://codeforces.com/problemset/problem/102437/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We have two strings of the same length, (s) and (t). The string (s) describes the current order of boxes from top to bottom, while (t) describes an earlier order. We may transform (s) in two ways. First, we can cyclically rotate it by taking its first (k) characters and moving them to the end. Second, every character can be shifted backward by the same Caesar shift (d), with the alphabet wrapping around from `a` to `z`. We need to determine whether some choice of (k) and (d) turns (s) exactly into (t).

The required output is either `Impossible`, or `Success` followed by one valid pair (k,d). The rotation must satisfy (0 \le k < n), while the shift only needs to be an integer between (-25) and (25). Since shifting by 26 changes nothing, it is enough to use a representative from (0) through (25).

The length can reach (200,000), so trying every rotation and comparing all (n) characters would require (O(n^2)) operations, roughly (4\cdot10^{10}) character comparisons in the worst case. That is far beyond what a competitive programming time limit can accommodate. We need an essentially linear solution.

There are several edge cases that can make a direct implementation fail. For (n=1), there are no adjacent pairs of characters, so any single-character strings can be made equal by an appropriate Caesar shift. For example,

```
1
z
a
```

has the answer `Success` with (k=0,d=-25), or equivalently (k=0,d=1) if shifts are represented modulo 26. An implementation that constructs an ordinary adjacent-difference array and assumes it contains at least one element can mishandle this case.

A second issue is the cyclic boundary. Consider

```
3
abc
bca
```

Here (s=\texttt{abc}) rotated left by one position is `bca`, so (k=1,d=0) works. The pair between the last character and the first character is part of the cyclic structure. If we only compare differences between positions (0) and (1), and (1) and (2), we lose information about that boundary and can incorrectly accept rotations that do not actually match.

A third issue is that the Caesar shift wraps around the alphabet. For example,

```
1
a
z
```

is solvable even though the ordinary numerical difference between `a` and `z` is not a useful signed shift in the usual integer sense. Alphabet arithmetic has to be performed modulo 26.

## Approaches

The direct solution is to try every possible rotation (k). For each rotation, we would construct or inspect the resulting string and check whether there is one Caesar shift that converts every character into the corresponding character of (t). The check itself is linear: once the first character determines the required shift, every remaining character must have exactly the same modular difference. Since there are (n) rotations, this takes (O(n^2)) time. With (n=200,000), the worst case is about (40) billion character comparisons, so although the method is correct, it is unusable.

The key observation is that a Caesar shift changes every character by exactly the same amount. Consequently, it does not change the difference between two neighboring characters when those differences are measured modulo 26.

For a string (x), define its cyclic difference sequence by

[
\operatorname{diff}(x)_i=(x_{i+1}-x_i)\bmod 26,
]

where the index after (n-1) wraps back to (0). If we Caesar-shift every character of (x) by the same amount, both characters in every difference receive the same addition, so the difference cancels.

Thus, two strings can differ only by a Caesar shift exactly when their cyclic difference sequences are equal. The rotation operation simply rotates this difference sequence by the same amount. The original problem therefore becomes a pattern matching problem: find the difference sequence of (t) inside two consecutive copies of the difference sequence of (s).

This is precisely the situation where KMP is useful. We build the difference sequence of (t) as the pattern and search for it in `diff_s + diff_s`. A match beginning at position (k) means that rotating (s) left by (k) gives a string whose cyclic differences are identical to those of (t). Once (k) is known, the Caesar shift is determined by the first character.

The reason the difference representation is sufficient is stronger than merely being a necessary condition. If two cyclic strings have the same difference at every neighboring position, choose one corresponding character pair. Every next character is then forced by the difference, so all characters are determined up to one common additive constant modulo 26. That constant is exactly the Caesar shift.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Convert every lowercase letter into a number from (0) to (25). This makes Caesar shifts ordinary arithmetic modulo 26.
2. Build the cyclic difference array `ds` for (s). For every position (i), store the difference from (s[i]) to the next character, wrapping from the last character back to the first. Build the corresponding array `dt` for (t).

These arrays describe the shape of the strings independently of their absolute alphabet positions. A Caesar shift changes absolute positions but leaves every difference unchanged.
3. If (n=1), there is no difference information to compare. The only possible rotation is (k=0), and the required Caesar shift is simply the modular difference between (s[0]) and (t[0]).
4. For (n>1), regard `dt` as a pattern and search for it in `ds + ds`. A cyclic rotation of `ds` is represented by a contiguous segment of this doubled array, exactly as an ordinary cyclic string rotation becomes a substring of two copies.
5. Use the KMP prefix function to find a match in linear time. Only starting positions (0) through (n-1) correspond to distinct rotations, so once a match is found at such a position, that position is the required rotation (k).
6. Recover the Caesar shift from the first character. After rotating (s) left by (k), its first character is `s[k]`. If the Caesar transformation shifts backward by (d), then

[
t[0]\equiv s[k]-d\pmod{26},
]

so

[
d\equiv s[k]-t[0]\pmod{26}.
]

We output this value in the range (0) through (25), which is allowed by the statement.
7. If KMP finds no valid starting position, no rotation has the same cyclic difference sequence as (t). Since equal cyclic differences are necessary for a common Caesar shift, the answer is `Impossible`.

### Why it works

The invariant is the cyclic difference sequence. A Caesar shift adds the same value to every character, so every adjacent modular difference stays unchanged. A rotation only changes where the cyclic sequence starts, so the difference sequence of a rotated (s) is exactly a cyclic rotation of `ds`.

KMP finds precisely whether `dt` occurs as one of those cyclic rotations. If it does at position (k), the two strings have identical differences after rotating (s) by (k). Starting from their first characters, all subsequent characters are then forced to differ by the same constant modulo 26. Choosing that constant as the Caesar shift produces exactly (t). Conversely, any valid transformation must preserve all cyclic differences, so its rotation must appear as a KMP match. The algorithm can therefore find a valid answer whenever one exists and cannot accept an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def differences(s):
    n = len(s)
    return [
        (ord(s[(i + 1) % n]) - ord(s[i])) % 26
        for i in range(n)
    ]

def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m

    for i in range(1, m):
        j = pi[i - 1]

        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    return pi

def solve():
    n = int(input())
    t = input().strip()
    s = input().strip()

    if n == 1:
        d = (ord(s[0]) - ord(t[0])) % 26
        print("Success")
        print(0, d)
        return

    ds = differences(s)
    dt = differences(t)

    pi = prefix_function(dt)

    # We only need 2*n - 1 elements. A match starting at n
    # would be the same cyclic rotation as starting at 0.
    text_length = 2 * n - 1
    j = 0

    for i in range(text_length):
        value = ds[i % n]

        while j > 0 and value != dt[j]:
            j = pi[j - 1]

        if value == dt[j]:
            j += 1

        if j == n:
            k = i - n + 1

            if k < n:
                d = (ord(s[k]) - ord(t[0])) % 26
                print("Success")
                print(k, d)
                return

            j = pi[j - 1]

    print("Impossible")

if __name__ == "__main__":
    solve()
```

The `differences` function constructs the cyclic representation described in the algorithm. The expression `(i + 1) % n` handles the edge from the last character back to the first, which is essential because the rotation is cyclic rather than linear.

The prefix function is standard KMP preprocessing. `pi[i]` stores the length of the longest proper prefix of the pattern that is also a suffix ending at position `i`. When a mismatch occurs, this allows the search to reuse information instead of restarting from the beginning.

The search does not physically construct `ds + ds`. Instead, `ds[i % n]` accesses the corresponding character of the conceptual doubled array. This saves one temporary array and makes the cyclic nature explicit. We iterate through `2*n - 1` positions because every rotation can be represented by a length-(n) segment starting at an index from (0) through (n-1). Starting at (n) would duplicate the rotation starting at (0).

The expression for `d` deserves attention. The transformation is a backward shift, so `t[0]` must equal `s[k] - d` modulo 26. Rearranging gives `d = s[k] - t[0]` modulo 26. Python's `% 26` produces a nonnegative result, so the returned value lies in (0,\ldots,25), all of which satisfy the permitted range.

There is no integer overflow concern because all stored differences are between (0) and (25), while the prefix array contains values between (0) and (n). Python integers also have arbitrary precision.

## Worked Examples

### Sample 1

The input is

```
3
abc
fde
```

The numeric values of `s = fde` are (5,3,4), and those of `t = abc` are (0,1,2). Their cyclic differences are

[
(3-5,4-3,5-4)\bmod26=(24,1,1)
]

for `s`, and

[
(1-0,2-1,0-2)\bmod26=(1,1,24)
]

for `t`.

The search proceeds as follows.

| Search position | Text value | Pattern index before | Pattern index after | Match |
| --- | --- | --- | --- | --- |
| 0 | 24 | 0 | 0 | no |
| 1 | 1 | 0 | 1 | no |
| 2 | 1 | 1 | 2 | no |
| 3 | 24 | 2 | 3 | yes |

The match starts at (k=1). Rotating `fde` left by one position gives `def`. The first character must become `a`, so

[
d=3-0=3.
]

Shifting `def` backward by three gives `abc`, producing `Success` with `1 3`.

This trace demonstrates why the doubled cyclic difference array is sufficient. The match begins exactly where the required rotation begins.

### Sample 2

The input is

```
3
abc
aba
```

The cyclic differences of `t = abc` are

[
(1,1,24).
]

For `s = aba`, they are

[
(1,-1,0)\bmod26=(1,25,0).
]

The search never obtains the complete pattern.

| Search position | Text value | Pattern index before | Pattern index after | Match |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | no |
| 1 | 25 | 1 | 0 | no |
| 2 | 0 | 0 | 0 | no |
| 3 | 1 | 0 | 1 | no |
| 4 | 25 | 1 | 0 | no |

There is no rotation whose difference sequence equals that of `abc`, so no Caesar shift can repair the mismatch. The correct result is `Impossible`.

The example shows why comparing only character counts would not be enough. Both strings contain two `a`-like positions and one other character, but their cyclic order is different, and Caesar shifts cannot change that order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Difference construction, KMP preprocessing, and KMP search each scan (O(n)) elements |
| Space | (O(n)) | The two difference arrays and KMP prefix array each use (O(n)) memory |

With (n\le 200,000), a linear algorithm performs only a few passes over roughly two hundred thousand elements. This is comfortably within the scale expected for the constraint, while the quadratic brute-force approach would require tens of billions of comparisons in the worst case.

## Test Cases

The test harness below deliberately does not compare the program's output with one fixed `k,d`, because the problem allows multiple valid answers. Instead, it parses the answer and checks that applying the reported transformation really produces (t).

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    try:
        n = int(input())
        t = input().strip()
        s = input().strip()

        if n == 1:
            d = (ord(s[0]) - ord(t[0])) % 26
            return f"Success\n0 {d}\n"

        def differences(x):
            return [
                (ord(x[(i + 1) % n]) - ord(x[i])) % 26
                for i in range(n)
            ]

        ds = differences(s)
        dt = differences(t)

        pi = [0] * n

        for i in range(1, n):
            j = pi[i - 1]
            while j > 0 and dt[i] != dt[j]:
                j = pi[j - 1]
            if dt[i] == dt[j]:
                j += 1
            pi[i] = j

        j = 0

        for i in range(2 * n - 1):
            value = ds[i % n]

            while j > 0 and value != dt[j]:
                j = pi[j - 1]

            if value == dt[j]:
                j += 1

            if j == n:
                k = i - n + 1

                if k < n:
                    d = (ord(s[k]) - ord(t[0])) % 26
                    return f"Success\n{k} {d}\n"

                j = pi[j - 1]

        return "Impossible\n"

    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve_data(inp)

def validate(inp: str, output: str) -> bool:
    lines = output.strip().splitlines()

    first = lines[0]
    n, t, s = inp.strip().splitlines()
    n = int(n)

    if first == "Impossible":
        return True

    assert first == "Success"
    k, d = map(int, lines[1].split())

    assert 0 <= k < n
    assert -26 < d < 26

    rotated = s[k:] + s[:k]

    result = ''.join(
        chr((ord(c) - ord('a') - d) % 26 + ord('a'))
        for c in rotated
    )

    return result == t

# Provided sample 1.
x = run("""3
abc
fde
""")
assert validate("""3
abc
fde
""", x), "sample 1"

# Provided sample 2.
x = run("""3
abc
aba
""")
assert x.strip() == "Impossible", "sample 2"

# Provided sample 3.
x = run("""1
z
a
""")
assert validate("""1
z
a
""", x), "sample 3"

# Minimum-size case with no actual character change.
x = run("""1
a
a
""")
assert validate("""1
a
a
""", x), "single character, equal"

# Boundary wraparound: z shifted backward by 25 becomes a.
x = run("""1
a
z
""")
assert validate("""1
a
z
""", x), "single character, alphabet wrap"

# All characters equal. Every rotation is equivalent, and a common
# Caesar shift is the only relevant operation.
x = run("""5
aaaaa
zzzzz
""")
assert validate("""5
aaaaa
zzzzz
""", x), "all equal characters"

# Rotation at the final possible starting position k = n - 1.
x = run("""4
abcd
dabc
""")
assert validate("""4
abcd
dabc
""", x), "last possible rotation"

# Same cyclic differences but a nonzero Caesar shift.
x = run("""5
abcde
efabc
""")
assert validate("""5
abcde
efabc
""", x), "rotation plus Caesar shift"

# Maximum-size input, all equal characters.
n = 200000
inp = f"{n}\n" + ("a" * n) + "\n" + ("z" * n) + "\n"
x = run(inp)
assert validate(inp, x), "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / a` | Any valid `Success` | Minimum size and zero shift |
| `1 / a / z` | Any valid `Success` | Alphabet wraparound |
| `5 / aaaaa / zzzzz` | Any valid `Success` | All cyclic differences equal zero |
| `4 / abcd / dabc` | Any valid `Success` with (k=3) | Boundary rotation (k=n-1) |
| `5 / abcde / efabc` | Any valid `Success` | Rotation combined with Caesar shift |
| (n=200000), all `a` versus all `z` | Any valid `Success` | Maximum input size and linear performance |

## Edge Cases

The single-character case needs separate handling because the cyclic difference array contains only one difference, namely the difference from the character back to itself, which is always zero. More directly, there is only one possible rotation, (k=0), so for

```
1
z
a
```

the required backward shift satisfies (a=z-d\pmod{26}), giving (d=25), which is equivalent to the sample's (d=-25) modulo 26. The implementation returns the valid representative `25`.

The cyclic boundary is handled when constructing differences. For

```
3
abc
bca
```

the difference sequence of `abc` is `(1,1,24)`, while `bca` has `(1,24,1)`. The second sequence is the first one rotated left by one position, so KMP finds (k=1). Ignoring the last-to-first difference would lose exactly the information needed to distinguish these cyclic arrangements.

Alphabet wrapping is handled by `% 26`. For example, shifting `z` backward by 25 gives `a`, even though `ord('z') - ord('a')` is 25 in ordinary integer arithmetic. The modular expression converts the alphabet into a cycle, which is the actual structure of the Caesar cipher.

All-equal strings are another useful stress case. For

```
5
aaaaa
zzzzz
```

every cyclic difference is zero for both strings. Thus every rotation is structurally valid, and only the Caesar shift matters. The algorithm may return (k=0), although any rotation would also be correct.

Finally, a match at (k=n-1) exercises the upper rotation boundary. For

```
4
abcd
dabc
```

the required rotation is exactly three positions. Searching only the first (n-1) positions would miss this valid answer, while searching the full doubled sequence without checking the starting position could count the duplicate rotation at position (n). The implementation searches `2*n-1` positions and accepts only matches with `k < n`, covering every distinct rotation exactly once.
