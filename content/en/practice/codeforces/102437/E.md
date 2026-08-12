---
title: "CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b"
description: "We have two orders, each represented by a string of length (n). The (i)-th character describes the article number of the (i)-th box in the stack. We need to determine whether the current order (s) can be transformed into the previous order (t)."
date: "2026-08-12T07:59:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 836
verified: false
draft: false
---

[CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b](https://codeforces.com/problemset/problem/102437/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We have two orders, each represented by a string of length (n). The (i)-th character describes the article number of the (i)-th box in the stack. We need to determine whether the current order (s) can be transformed into the previous order (t).

The allowed transformation has two independent parts. First, every letter is shifted by the same Caesar shift (d), cyclically modulo 26. Second, the stack can be rotated, meaning that a prefix of (s) is moved from the top to the bottom. If the rotation amount is (k), the resulting order is

[
s[k:] + s[].
]

After both operations, the resulting string must equal (t). We have to output any valid pair ((k,d)), or report `Impossible`.

The length can be as large as (200,000). An algorithm that examines every rotation and compares all (n) characters would perform up to (n^2 = 40,000,000,000) character comparisons in the worst case, which is far beyond what is practical. We need a solution whose work is essentially linear in the string length.

There are several edge cases that can break a straightforward implementation. The first is (n=1). There is no meaningful rotation to search for, but a Caesar shift may still be necessary. For example,

```
1
z
a
```

is solvable with (k=0), because shifting `z` backward by 25 gives `a`. An implementation that assumes there are adjacent characters to inspect would fail on this case.

Another edge case is wraparound in the alphabet. For example,

```
1
a
z
```

is also solvable. The required shift can be represented as (d=1), because shifting `z` backward by 1 gives `y`, while shifting `a` backward by 1 gives `z`. The arithmetic must be performed modulo 26 rather than using ordinary integer differences.

A third issue is rotation across the end of the string. Consider

```
5
abcde
bcdea
```

Rotating `bcdea` by (4) positions produces `abcde`, so the correct answer exists with (k=4) and (d=0). A search that only checks ordinary substrings of `s` and forgets the cyclic boundary would miss this solution.

Finally, repeated characters can make several rotations valid. For example,

```
4
aaaa
aaaa
```

has every rotation as a valid rotation, and (d=0) works for all of them. The algorithm must accept the first valid candidate rather than relying on uniqueness.

## Approaches

The direct solution is to try every possible rotation (k). For each rotation, we would compare every character of the rotated (s) with the corresponding character of (t). The first pair of positions determines the Caesar shift, and then every remaining position must have exactly the same shift modulo 26. This method is correct because it explicitly checks every possible transformation.

The problem is the amount of repeated work. There are (n) rotations, and checking one rotation takes (O(n)) time. At (n=200,000), the worst case reaches (200,000^2=40,000,000,000) character checks. The brute force is conceptually simple, but its quadratic behavior rules it out.

The useful observation is that a Caesar shift does not change the difference between neighboring letters. If `x` is changed to `x-d` and `y` is changed to `y-d`, then their difference remains

[
(y-d)-(x-d)=y-x \pmod {26}.
]

So instead of comparing the original letters, we can compare the cyclic sequence of differences between consecutive letters.

For a string (x), define

(x[(i+1)\bmod n]-x[i])\bmod 26.
]

This sequence has exactly (n) elements because it also contains the difference from the last character back to the first.

Suppose rotating (s) by (k) positions gives the correct arrangement before the Caesar shift. Its cyclic difference sequence is simply the cyclic difference sequence of (s), starting at position (k). The Caesar shift then changes no differences at all. Consequently, a valid rotation exists exactly when the cyclic difference sequence of (t) occurs as a cyclic rotation of the cyclic difference sequence of (s).

Finding one cyclic sequence inside another is a standard string matching problem. We can concatenate the difference sequence of (s) with itself and use the Knuth-Morris-Pratt algorithm to find the difference sequence of (t) in (O(n)) time. Once a matching starting position (k) is found, the Caesar shift is determined by the first character:

[
d=(s[k]-t[0])\bmod 26.
]

The difference representation solves the rotation problem, while KMP makes the search linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Convert every character of (s) and (t) into its numerical value from 0 to 25. This lets us perform all Caesar-shift arithmetic with ordinary modular arithmetic.
2. Build the cyclic difference array `ds` for (s). For every position (i), store the difference from (s[i]) to (s[(i+1)\bmod n]), modulo 26. Build `dt` for (t) in exactly the same way.
3. Construct the KMP prefix function for `dt`. The prefix function tells us how much of the pattern is still usable after a mismatch, so the search never has to restart from the beginning.
4. Search for `dt` inside `ds + ds`. A rotation of a cyclic array corresponds to a contiguous segment of its doubled version. We only accept a match starting at an index smaller than (n), because those are exactly the (n) possible rotations.
5. If there is no such match, print `Impossible`. Matching cyclic differences is necessary for a valid transformation, so no Caesar shift can repair a missing rotation.
6. If the match starts at (k), calculate

[
d=(s[k]-t[0])\bmod 26.
]

The rotated string begins with `s[k]`. Shifting that character backward by (d) must produce `t[0]`, so this equation gives exactly the required Caesar shift.

1. Print `Success`, followed by (k) and (d). The value produced by modulo 26 lies between 0 and 25, which satisfies the required range (-26<d<26).

### Why it works

The central invariant is that two strings differ only by a uniform Caesar shift if and only if their corresponding cyclic differences are equal. A Caesar shift cancels when two neighboring characters are subtracted, so it cannot affect the difference array.

A rotation by (k) simply changes the starting point of the cyclic difference array. Searching `dt` inside `ds + ds` therefore finds exactly the rotations whose relative character structure matches that of (t). Once such a rotation is found, every adjacent difference agrees, so the difference between the rotated (s) and (t) is constant across the entire cycle. That constant is precisely the Caesar shift computed from the first character. Thus every reported pair ((k,d)) produces (t), and if a valid pair exists, its rotation must appear in the KMP search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_diff(s):
    n = len(s)
    if n == 1:
        return []
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

    ds = build_diff(s)
    dt = build_diff(t)

    pi = prefix_function(dt)

    j = 0
    doubled = ds + ds

    for i, value in enumerate(doubled):
        while j > 0 and value != dt[j]:
            j = pi[j - 1]

        if value == dt[j]:
            j += 1

        if j == n:
            start = i - n + 1

            if start < n:
                d = (ord(s[start]) - ord(t[0])) % 26
                print("Success")
                print(start, d)
                return

            j = pi[j - 1]

    print("Impossible")

if __name__ == "__main__":
    solve()
```

The `build_diff` function converts a string into its cyclic difference sequence. The expression `(i + 1) % n` handles the final-to-first edge, which is necessary because rotations are cyclic rather than ordinary substring operations.

The (n=1) case is handled separately because its difference sequence would be empty. There is only one possible rotation, (k=0), and the Caesar shift can be obtained directly from the two characters.

The prefix function is computed only for `dt`. During the KMP search, `ds + ds` represents every cyclic rotation of `ds` as a normal contiguous segment. The first (n) possible starting positions correspond exactly to (k=0,\ldots,n-1).

When KMP reaches `j == n`, the entire target difference sequence has matched. The expression `i - n + 1` gives the beginning of that match. We reject starts at or beyond (n), because those are duplicate matches created by doubling the array.

Finally, `d = (ord(s[start]) - ord(t[0])) % 26` follows directly from the direction of the Caesar operation. If the rotated character is `c`, shifting it backward by (d) gives `c-d`, so we need `c-d = t[0] (mod 26)`. Rearranging gives the expression used in the code.

Python integers have arbitrary precision, so there is no overflow issue. All indices stay within (2n), and every character conversion is constant time.

## Worked Examples

### Sample 1

The input is

```
3
abc
fde
```

The cyclic differences are as follows.

| String | Difference sequence |
| --- | --- |
| `t = abc` | `[1, 1, 24]` |
| `s = fde` | `[24, 1, 1]` |

Doubling the difference sequence of `s` gives `[24, 1, 1, 24, 1, 1]`. The target sequence `[1, 1, 24]` first occurs at position (1).

| KMP state | Value | Pattern position | Result |
| --- | --- | --- | --- |
| start | 24 | 0 | mismatch |
| after index 1 | 1 | 1 | match |
| after index 2 | 1 | 2 | match |
| after index 3 | 24 | 3 | full match |

Thus (k=1). Rotating `fde` by one position gives `def`. Its first character is `d`, while the target starts with `a`, so

[
d=(d-a)\bmod26=3.
]

Shifting `def` backward by 3 gives `abc`, so the algorithm prints `Success`, `1 3`.

### Sample 2

The input is

```
3
abc
aba
```

The cyclic differences are

| String | Difference sequence |
| --- | --- |
| `t = abc` | `[1, 1, 24]` |
| `s = aba` | `[25, 25, 0]` |

The doubled sequence of `s` is `[25, 25, 0, 25, 25, 0]`, which contains no occurrence of `[1, 1, 24]`.

| Search position | Current difference | Target progress |
| --- | --- | --- |
| 0 | 25 | 0 |
| 1 | 25 | 0 |
| 2 | 0 | 0 |
| 3 | 25 | 0 |
| 4 | 25 | 0 |
| 5 | 0 | 0 |

No rotation has the same relative character changes as `t`, so there is no Caesar shift that can make the strings equal. The answer is `Impossible`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Building both difference arrays, constructing KMP's prefix function, and searching the doubled array each take linear time. |
| Space | (O(n)) | The difference arrays, doubled sequence, and prefix function all require linear memory. |

With (n\le200,000), the algorithm performs only a constant number of linear passes over the input. Its memory usage is also linear, so it is suitable for the stated constraints.

## Test Cases

The success output is not unique, so a robust test harness should verify the returned transformation instead of comparing the complete output string literally. The following test code does that while still checking the exact `Impossible` samples.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    n = int(data[0])
    t = data[1]
    s = data[2]

    def build_diff(x):
        if n == 1:
            return []
        return [
            (ord(x[(i + 1) % n]) - ord(x[i])) % 26
            for i in range(n)
        ]

    if n == 1:
        d = (ord(s[0]) - ord(t[0])) % 26
        return f"Success\n0 {d}\n"

    ds = build_diff(s)
    dt = build_diff(t)

    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and dt[i] != dt[j]:
            j = pi[j - 1]
        if dt[i] == dt[j]:
            j += 1
        pi[i] = j

    j = 0
    for i, value in enumerate(ds + ds):
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

def run(inp: str) -> str:
    return solve_data(inp)

def valid_output(inp: str, out: str) -> bool:
    data = inp.strip().split()
    n = int(data[0])
    t = data[1]
    s = data[2]

    lines = out.strip().split()

    if lines[0] == "Impossible":
        return len(lines) == 1

    if lines[0] != "Success" or len(lines) != 3:
        return False

    k = int(lines[1])
    d = int(lines[2])

    if not (0 <= k < n and -26 < d < 26):
        return False

    rotated = s[k:] + s[:k]

    transformed = "".join(
        chr((ord(c) - ord('a') - d) % 26 + ord('a'))
        for c in rotated
    )

    return transformed == t

# Provided samples.
assert run("""3
abc
fde
""") == "Success\n1 3\n"

assert run("""3
abc
aba
""") == "Impossible\n"

assert valid_output(
    """1
z
a
""",
    run("""1
z
a
""")
)

# Minimum-size, no transformation needed.
assert valid_output(
    """1
a
a
""",
    run("""1
a
a
""")
)

# All characters equal, with a non-zero Caesar shift.
assert valid_output(
    """4
zzzz
aaaa
""",
    run("""4
zzzz
aaaa
""")
)

# Rotation by n - 1, exercising the cyclic boundary.
assert valid_output(
    """5
abcde
bcdea
""",
    run("""5
abcde
bcdea
""")
)

# Maximum-size input, all characters equal.
n = 200000
max_case = f"{n}\n" + "a" * n + "\n" + "a" * n + "\n"
assert valid_output(max_case, run(max_case))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / a` | `Success`, (k=0,d=0) | Minimum size and empty difference sequence |
| `4 / zzzz / aaaa` | `Success`, any rotation and (d=1) | All-equal strings and modular Caesar arithmetic |
| `5 / abcde / bcdea` | `Success`, (k=4,d=0) | Rotation wrapping around the end |
| (n=200000), all `a` | `Success`, (k=0,d=0) | Maximum input size and linear performance |

## Edge Cases

For (n=1), the difference arrays contain no elements, so KMP is not meaningful. Consider

```
1
z
a
```

There is only one possible rotation, (k=0). The required shift is

[
(z-a)\bmod26=25.
]

The algorithm returns `Success`, `0 25`. This is equivalent to the sample's `0 -25` because the Caesar shift is cyclic modulo 26, and both values represent the same transformation.

For alphabet wraparound, consider

```
1
a
z
```

The algorithm computes

[
(a-z)\bmod26=1.
]

Shifting `a` backward by 1 produces `z`, so `Success 0 1` is valid. The modulo operation prevents a negative raw difference from being treated as an invalid shift.

For a rotation that crosses the end of the string, consider

```
5
abcde
bcdea
```

The cyclic difference sequence of `s` is searched in `ds + ds`. The target starts at position (4), corresponding to the rotation

# \texttt{a}+\texttt{bcde}

\texttt{abcde}.
]

KMP finds (k=4), and the first characters already agree, so (d=0).

For repeated characters, consider

```
4
aaaa
aaaa
```

Every cyclic difference is zero, so every rotation matches. KMP accepts the first one, (k=0), and the first characters give (d=0). There is no need to distinguish between multiple valid answers because the problem accepts any one of them.

The most subtle correctness case is when the difference sequences match but the strings do not initially have the same first character. For example,

```
3
abc
def
```

The cyclic difference sequence of both strings is `[1, 1, 24]`, so (k=0) is a valid structural match. The first-character difference gives

[
d=(d-a)\bmod26=3.
]

Shifting `def` backward by 3 produces `abc`. This demonstrates why matching differences alone is not the final step, but it reduces the remaining work to determining one global Caesar shift.
