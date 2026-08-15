---
title: "CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b"
description: "We have two strings of length (n). The string (s) describes the current stack of boxes, while (t) describes the previous stack. We may rotate (s) cyclically to the left by some (k), and then apply the same Caesar shift to every character."
date: "2026-08-15T09:19:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102437
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102437
solve_time_s: 486
verified: false
draft: false
---

[CF 102437E - \u041f\u043e\u0445\u043e\u0436\u0438\u0435 \u0437\u0430\u043a\u0430\u0437\u044b](https://codeforces.com/problemset/problem/102437/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We have two strings of length (n). The string (s) describes the current stack of boxes, while (t) describes the previous stack. We may rotate (s) cyclically to the left by some (k), and then apply the same Caesar shift to every character. The task is to find any pair ((k,d)) that transforms (s) into (t), or report that no such pair exists.

For a rotation by (k), the resulting character at position (i) is (s[(i+k)\bmod n]). If the Caesar shift moves every letter backwards by (d), then the required equality is

[
t_i \equiv s_{(i+k)\bmod n}-d \pmod{26}.
]

The length can reach (200,000), and the official limits are 2 seconds and 512 MB. An (O(n^2)) algorithm can perform about (4\cdot10^{10}) character comparisons in the worst case, which is far beyond what fits in the time limit. We need an (O(n)) or (O(n\log n)) solution, and a linear string-matching algorithm is enough.

There are several edge cases that can make a direct implementation misleading. For (n=1), the only possible rotation is (k=0), but any two letters can be converted into each other by a Caesar shift. For example,

```
1
z
a
```

has a valid answer such as `Success` followed by `0 25`. A method that compares adjacent characters would otherwise appear to have no information at all, because a one-character string has no ordinary adjacent pair.

A second edge case is a rotation that crosses the end of the string. For example,

```
5
abcde
cdeab
```

has the answer `Success` with `3 0`. The correct rotation is the first three characters moved to the bottom. An implementation that only checks ordinary substrings of (s), instead of treating the string cyclically, would miss this answer.

Repeated characters create another subtle case. For

```
4
aaaa
zzzz
```

every rotation is valid, and a single Caesar shift is enough. A solution must not assume that a matching rotation is unique.

Finally, the strings can have the same character frequencies while still being impossible to transform. For example,

```
3
abc
aba
```

is impossible. Both strings contain three lowercase letters, but no cyclic rotation of `aba` can become `abc` after one uniform shift. Comparing only character counts would accept this incorrectly.

## Approaches

The direct approach is to try every rotation (k). For each rotation, construct or conceptually inspect

[
s[k],s[k+1],\ldots,s[n-1],s[0],\ldots,s[k-1].
]

The first character determines the only possible Caesar shift. Once that shift is known, we compare every remaining character against the corresponding character of (t). This is correct because for a fixed rotation there is at most one Caesar shift that can make the first characters equal.

The problem is the number of comparisons. In the worst case there are (n) rotations and (n) character checks for each rotation, giving (O(n^2)) time. For (n=200,000), that is about (40) billion comparisons.

The useful observation is that a Caesar shift changes every character by the same amount, so it does not change the differences between consecutive characters. Encode every cyclic adjacent difference by

[
D_i=(x_{i+1}-x_i)\bmod 26,
]

where (x_n=x_0). For example, the differences of `abc` are

[
[1,1,24],
]

because `c` to `a` is (0-2\equiv24\pmod{26}).

Suppose a rotated version of (s) becomes (t) after a Caesar shift. Every adjacent difference in the rotated (s) must then equal the corresponding adjacent difference in (t). A rotation of (s) simply rotates its difference array by the same amount. Thus the original problem becomes a standard cyclic string matching problem: find the difference array of (t) inside two consecutive copies of the difference array of (s).

This observation also works in the other direction. If the difference arrays match under some rotation, then every consecutive pair differs by the same amount in the two strings. Starting from one character, that constant offset propagates through the entire string, so a single Caesar shift exists.

We can find the required rotation using the Knuth-Morris-Pratt algorithm. KMP finds the pattern (D_t) in (D_s+D_s) in linear time, without checking every rotation separately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Difference arrays + KMP | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Convert every character of (s) and (t) into an integer from (0) to (25). Build their cyclic difference arrays. For a string (x), position (i) stores ((x[(i+1)\bmod n]-x[i])\bmod26). The cyclic last-to-first difference is necessary because rotations preserve the edge between the last and first positions as well.
2. Let (A) be the difference array of (s), and (B) the difference array of (t). A left rotation of (s) by (k) rotates (A) left by exactly (k) positions. We therefore need to find (B) as a length-(n) segment beginning at some position (k) in (A+A).
3. Build the KMP prefix function for (B). The prefix function tells us how much of the pattern is still usable after a mismatch, allowing the search to skip comparisons instead of restarting from the beginning.
4. Run KMP over two copies of (A). Whenever a complete occurrence of (B) starts at position (k<n), we have found a rotation that preserves all cyclic differences. We can stop at the first such occurrence.
5. Once (k) is known, compare the first character of the rotated (s), which is (s[k]), with (t[0]). Since the Caesar transformation moves characters backwards by (d),

[
t_0\equiv s_k-d\pmod{26},
]

so

[
d\equiv s_k-t_0\pmod{26}.
]

Choosing the representative from (0) through (25) always satisfies the required range (-26<d<26).

1. If KMP finds no occurrence beginning in the first (n) positions, no rotation has the required cyclic differences, so no valid transformation exists.

### Why it works

The invariant is that a uniform Caesar shift leaves every cyclic adjacent difference unchanged. A valid transformation therefore implies that the difference array of (t) is a rotation of the difference array of (s), so KMP must find it.

Conversely, suppose KMP finds a rotation (k) for which the two difference arrays are identical. Then for every consecutive pair, the difference between the rotated (s) and (t) is the same modulo (26). Hence all corresponding characters differ by one constant value. That constant is exactly the Caesar shift (d) computed from the first character, so applying rotation (k) and that shift transforms (s) into (t).

The case (n=1) follows from the same reasoning. Both difference arrays contain the single value (0), so KMP finds the only possible rotation, and the first-character calculation supplies the required Caesar shift.

## Python Solution

```python
import sys
input = sys.stdin.readline

def differences(s):
    n = len(s)
    a = [ord(c) - 97 for c in s]
    return [(a[(i + 1) % n] - a[i]) % 26 for i in range(n)], a

def prefix_function(p):
    pi = [0] * len(p)
    for i in range(1, len(p)):
        j = pi[i - 1]
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi

def solve():
    n = int(input())
    t = input().strip()
    s = input().strip()

    dt, tv = differences(t)
    ds, sv = differences(s)

    pi = prefix_function(dt)

    j = 0
    rotation = -1

    # We only need starts from 0 through n - 1.
    # Two copies of ds contain every cyclic rotation.
    for i in range(2 * n):
        value = ds[i % n]

        while j > 0 and value != dt[j]:
            j = pi[j - 1]

        if value == dt[j]:
            j += 1

        if j == n:
            start = i - n + 1
            if start < n:
                rotation = start
                break
            j = pi[j - 1]

    if rotation == -1:
        print("Impossible")
        return

    # t[0] = s[rotation] - d (mod 26)
    d = (sv[rotation] - tv[0]) % 26

    print("Success")
    print(rotation, d)

if __name__ == "__main__":
    solve()
```

The `differences` function converts characters to values from (0) to (25) and computes all cyclic differences. The expression `(i + 1) % n` handles the final edge back to the first character, including the (n=1) case.

The prefix function is standard KMP preprocessing. Its indices are always within the pattern, and the `while` loop repeatedly falls back through previously computed prefix lengths. Since every fallback moves `j` to a smaller value, the total work remains linear.

The search iterates through `2 * n` positions and accesses `ds[i % n]`, which represents two copies of the cyclic difference array without allocating another list. A match beginning at `start` corresponds exactly to rotating (s) left by `start`. The `start < n` condition rejects the duplicate occurrences that begin after the first (n) positions.

The Caesar shift is calculated only after a valid rotation is found. We use `(sv[rotation] - tv[0]) % 26`, because the transformation is a backward shift. The resulting value lies in (0,\ldots,25), which is inside the allowed output range. Python integers do not overflow, so no special arithmetic handling is needed.

## Worked Examples

### Sample 1

The input is

```
3
abc
fde
```

For `t = abc`, the cyclic differences are `1, 1, 24`. For `s = fde`, they are `24, 1, 1`.

| Pattern index | `dt` | Search value from `ds + ds` | KMP state |
| --- | --- | --- | --- |
| 0 | 1 | 24 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 24 | 1 | 2 |
| 3 | 1 | 24 | 3 |

The complete pattern begins at search position (1), so the required rotation is (k=1). After rotating `fde` left by one position, we get `def`. The first character changes from `d` to `a`, which requires a backward shift of (3).

| `k` | Rotated `s` | `t[0]` | `s[k] - t[0]` | Result |
| --- | --- | --- | --- | --- |
| 1 | `def` | `a` | (3-0=3) | `Success 1 3` |

The example demonstrates that matching differences identifies the rotation without comparing all characters of every possible rotation.

### Sample 2

The input is

```
3
abc
aba
```

The cyclic differences of `abc` are `1, 1, 24`. The cyclic differences of `aba` are `25, 25, 0`.

| Pattern index | `dt` | Search value from `ds + ds` | KMP state |
| --- | --- | --- | --- |
| 0 | 1 | 25 | 0 |
| 1 | 1 | 25 | 0 |
| 2 | 24 | 0 | 0 |
| 3 | 1 | 25 | 0 |
| 4 | 1 | 25 | 0 |
| 5 | 24 | 0 | 0 |

No complete occurrence of the pattern appears, so there is no valid rotation. Since a Caesar shift cannot change adjacent differences, there is no possible value of (d) that can repair this mismatch.

The output is therefore

```
Impossible
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Difference construction, KMP preprocessing, and the search each take linear time |
| Space | (O(n)) | The two difference arrays and KMP prefix array contain (O(n)) integers |

With (n\le200,000), the algorithm performs only a constant number of linear passes over the input, which is appropriate for the official 2-second limit. The memory consumption is also comfortably below the official 512 MB limit.

## Test Cases

The test harness below does not compare successful answers against one fixed pair ((k,d)), because the problem explicitly allows any valid transformation. Instead, it checks that the reported pair is within range and actually transforms (s) into (t). Impossible cases are compared exactly.

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    t = sys.stdin.readline().strip()
    s = sys.stdin.readline().strip()

    def differences(x):
        values = [ord(c) - 97 for c in x]
        return [
            (values[(i + 1) % n] - values[i]) % 26
            for i in range(n)
        ], values

    def prefix_function(p):
        pi = [0] * len(p)
        for i in range(1, len(p)):
            j = pi[i - 1]
            while j > 0 and p[i] != p[j]:
                j = pi[j - 1]
            if p[i] == p[j]:
                j += 1
            pi[i] = j
        return pi

    dt, tv = differences(t)
    ds, sv = differences(s)

    pi = prefix_function(dt)

    j = 0
    rotation = -1

    for i in range(2 * n):
        value = ds[i % n]

        while j > 0 and value != dt[j]:
            j = pi[j - 1]

        if value == dt[j]:
            j += 1

        if j == n:
            start = i - n + 1
            if start < n:
                rotation = start
                break
            j = pi[j - 1]

    if rotation == -1:
        result = "Impossible\n"
    else:
        d = (sv[rotation] - tv[0]) % 26
        result = f"Success\n{rotation} {d}\n"

    sys.stdin = old_stdin
    return result

def is_valid(inp: str, out: str) -> bool:
    lines = inp.strip().splitlines()
    n = int(lines[0])
    t = lines[1]
    s = lines[2]

    out_lines = out.strip().splitlines()

    if out_lines[0] == "Impossible":
        return False

    assert out_lines[0] == "Success"
    k, d = map(int, out_lines[1].split())

    assert 0 <= k < n
    assert -26 < d < 26

    for i in range(n):
        source = ord(s[(i + k) % n]) - 97
        target = (source - d) % 26
        if target != ord(t[i]) - 97:
            return False

    return True

# Provided samples.
sample1 = """3
abc
fde
"""
assert is_valid(sample1, solve_case(sample1)), "sample 1"

sample2 = """3
abc
aba
"""
assert solve_case(sample2).strip() == "Impossible", "sample 2"

sample3 = """1
z
a
"""
assert is_valid(sample3, solve_case(sample3)), "sample 3"

# Minimum size, where the difference arrays contain only zero.
case1 = """1
a
z
"""
assert is_valid(case1, solve_case(case1)), "minimum size"

# Rotation crosses the end of the string.
case2 = """5
abcde
cdeab
"""
assert is_valid(case2, solve_case(case2)), "wrap-around rotation"

# All characters are equal, and n is at the maximum allowed size.
n = 200000
case3 = f"{n}\n" + "a" * n + "\n" + "z" * n + "\n"
assert is_valid(case3, solve_case(case3)), "maximum size and all equal"

# Almost matching strings, designed to reject a wrong rotation.
case4 = """4
abca
caab
"""
assert solve_case(case4).strip() == "Impossible", "invalid rotation"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / z` | Any valid `Success` | Minimum size and the fact that one character can always be shifted |
| `5 / abcde / cdeab` | Any valid `Success`, with (k=3,d=0) being one answer | Wrap-around rotation and correct rotation direction |
| (n=200000), both strings constant | Any valid `Success` | Maximum input size, repeated characters, and linear performance |
| `4 / abca / caab` | `Impossible` | Rejecting a rotation whose local differences do not match |

## Edge Cases

For (n=1), consider

```
1
z
a
```

The difference array of both strings is `[0]`, because the only position is also its own cyclic successor. KMP immediately finds a match at rotation (k=0). The shift is

[
d=(25-0)\bmod26=25,
]

so the program may print

```
Success
0 25
```

The sample's `0 -25` is another representation accepted by the problem's allowed shift convention. The essential condition is that the reported pair produces the target character.

For a rotation crossing the end, consider

```
5
abcde
cdeab
```

The difference array of `abcde` is `[1,1,1,1,22]`, while the difference array of `cdeab` is `[1,1,22,1,1]`. The second array starts at position (3) of the first array's cyclic sequence, so KMP finds (k=3). The rotated source is `cdeab`, already equal to the target, giving (d=0).

For repeated characters, consider

```
4
aaaa
zzzz
```

Both cyclic difference arrays are `[0,0,0,0]`. KMP finds rotation (0), and the first characters give

[
d=(25-0)\bmod26=25.
]

Every character of `zzzz` shifted backwards by (25) becomes `aaaa`. The fact that all rotations are valid does not cause a problem because the statement permits any valid answer.

For an impossible pair, consider

```
3
abc
aba
```

The target differences are `[1,1,24]`, while the source differences are `[25,25,0]`. No cyclic rotation can turn one sequence into the other, so KMP never reaches a full pattern match. The algorithm prints `Impossible` without attempting to guess a Caesar shift. This is exactly why checking character counts alone would be insufficient.
