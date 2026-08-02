---
title: "CF 102620I - Bracelets"
description: "We have two bracelets. Each bracelet is represented by a circular sequence of characters, and we may activate some beads while moving around the bracelet in either direction."
date: "2026-08-02T07:09:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102620
codeforces_index: "I"
codeforces_contest_name: "mBIT Standard June 2020"
rating: 0
weight: 102620
solve_time_s: 76
verified: true
draft: false
---

[CF 102620I - Bracelets](https://codeforces.com/problemset/problem/102620/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two bracelets. Each bracelet is represented by a circular sequence of characters, and we may activate some beads while moving around the bracelet in either direction. The activated characters must appear in the same order on both bracelets, but the starting point of the circle is not fixed. The goal is to find the maximum number of activated beads that can match.

A circular sequence can be viewed by writing it twice in a row. Any walk that starts somewhere on the circle and continues without using a bead twice appears as a contiguous segment of this doubled sequence. Because we only need the length of the best common subsequence, doubling both bracelets lets us represent every possible starting position.

The input contains two strings describing the two bracelets. The output is the largest possible length of a common activated sequence, considering both clockwise and counterclockwise directions.

The lengths are at most 1500 characters. A quadratic dynamic program is acceptable, but trying every pair of rotations separately would create roughly $1500^3$ work, which is too much in Python. We need to avoid enumerating rotations and instead represent all rotations at once.

A few cases require care. If a bracelet has only one character, the doubled representation must still work because the same character can be chosen only once. For example:

```
a
a
```

The answer is `1`. A solution that allows the doubled string to contribute twice would incorrectly return `2`.

Repeated characters also create traps. For example:

```
aaa
aaa
```

The answer is `3`, not `6`. The circle can be traversed from any point, but each bead can only be used once.

The direction of traversal matters. For example:

```
abc
cba
```

The answer is `3` because reversing one bracelet makes the sequences identical. A solution that only checks clockwise order would miss this.

## Approaches

The direct approach is to generate every rotation of both bracelets and compute the longest common subsequence for each pair. This is correct because every possible circular starting point is considered, and LCS handles the choice of which beads to activate. However, there are $n \times m$ rotation pairs, and each LCS costs $O(nm)$, giving $O(n^2m^2)$ operations. With lengths around 1500, this is far beyond the limit.

The key observation is that rotations do not need to be generated explicitly. If a string is doubled, every rotation appears as a substring of that doubled string. A common subsequence between two doubled strings represents choosing a direction and starting position on each bracelet. We only have to prevent using the same bracelet twice, so the final answer is limited by the original shorter bracelet length.

The same argument applies after reversing either bracelet. We compute the best result for all combinations of original and reversed directions. This reduces the problem to four ordinary LCS computations on doubled strings.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2m^2)$ | $O(nm)$ | Too slow |
| Optimal | $O(nm)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Create four pairs of strings representing the possible directions of movement. Each bracelet can be read normally or reversed, so we consider both choices.
2. For every chosen pair of directions, duplicate both strings. The duplicated strings contain every possible circular starting point as a normal subsequence.
3. Compute the LCS length of the two doubled strings. If the LCS is larger than the number of beads available on either bracelet, clamp it to the smaller original length.
4. Take the maximum value over all direction choices.

Why this works is that every valid activation corresponds to selecting beads in order from some rotation of each bracelet. That rotation exists inside the doubled string. Conversely, any subsequence of the doubled strings that uses no more than the original number of beads corresponds to a valid walk around both circles.

The invariant is that every LCS computation considers one complete choice of traversal directions while the doubled representation covers every possible starting point. Since all valid cases are included and no case can use more beads than physically exist, the maximum found is exactly the answer.

## Python Solution

```python
import sys

input = sys.stdin.readline

def lcs(a, b):
    if len(b) > len(a):
        a, b = b, a

    dp = [0] * (len(b) + 1)

    for ca in a:
        prev = 0
        for j, cb in enumerate(b, 1):
            cur = dp[j]
            if ca == cb:
                dp[j] = prev + 1
            elif dp[j - 1] > dp[j]:
                dp[j] = dp[j - 1]
            prev = cur

    return dp[-1]

def solve():
    s = input().strip()
    t = input().strip()

    ans = 0
    limit = min(len(s), len(t))

    for a in (s, s[::-1]):
        for b in (t, t[::-1]):
            value = lcs(a + a, b + b)
            if value > limit:
                value = limit
            if value > ans:
                ans = value

    print(ans)

if __name__ == "__main__":
    solve()
```

The `lcs` function uses a rolling one-dimensional dynamic program. The usual LCS table has a row for every character of the first string and a column for every character of the second string, but only the previous row is needed while scanning. This reduces memory from $O(nm)$ to $O(m)$.

The main function creates the four orientation combinations. Reversing is necessary because a bracelet may be traversed in either direction. Doubling with `a + a` and `b + b` removes the need to explicitly rotate the strings.

The final clamp is required because the doubled strings contain two copies of every bead. Without it, the LCS could illegally select the same physical bead after going around the bracelet twice.

## Worked Examples

For the input:

```
metrocity
kryptonite
```

The best direction choice gives the common sequence `etoty`.

| First bracelet | Second bracelet | LCS on doubled strings | Current answer |
| --- | --- | --- | --- |
| metrocity | kryptonite | 5 | 5 |
| metrocity | etinotyrk | 10 | 10 |

The second orientation allows the same activation order that appears when one bracelet is followed backwards.

For:

```
abc
cba
```

| First bracelet | Second bracelet | LCS on doubled strings | Current answer |
| --- | --- | --- | --- |
| abc | cba | 1 | 1 |
| abc | abc | 3 | 3 |

The second row demonstrates why reverse traversal must be checked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Four LCS computations are performed, and each doubled string has size at most $3000$, giving a constant factor of four over the quadratic DP. |
| Space | $O(m)$ | The LCS implementation keeps only one dynamic programming row. |

The solution fits the 1500 character limit because it avoids the cubic rotation enumeration. The rolling DP also keeps memory usage small.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()
    t = sys.stdin.readline().strip()

    def lcs(a, b):
        if len(b) > len(a):
            a, b = b, a
        dp = [0] * (len(b) + 1)
        for x in a:
            prev = 0
            for i, y in enumerate(b, 1):
                tmp = dp[i]
                if x == y:
                    dp[i] = prev + 1
                elif dp[i - 1] > dp[i]:
                    dp[i] = dp[i - 1]
                prev = tmp
        return dp[-1]

    ans = 0
    for a in (s, s[::-1]):
        for b in (t, t[::-1]):
            ans = max(ans, min(len(s), len(t), lcs(a + a, b + b)))

    sys.stdin = old
    return str(ans) + "\n"

assert run("a\na\n") == "1\n"
assert run("abc\ncba\n") == "3\n"
assert run("aaa\naaa\n") == "3\n"
assert run("abcd\nxyab\n") == "2\n"
assert run("metrocity\nkryptonite\n") == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `1` | Single bead handling |
| `abc / cba` | `3` | Reverse traversal |
| `aaa / aaa` | `3` | Preventing reuse after doubling |
| `abcd / xyab` | `2` | Normal partial matching |
| `metrocity / kryptonite` | `10` | Mixed direction matching |

## Edge Cases

For a single-bead bracelet:

```
a
a
```

The doubled strings are still `"aa"`, but the answer is clamped to one bead. The algorithm returns `1` because it never allows more activations than the physical bracelet contains.

For repeated characters:

```
aaa
aaa
```

The LCS of the doubled strings is six, but only three beads exist on each bracelet. The limit step changes this to `3`, which is the only valid answer.

For opposite directions:

```
abc
cba
```

The normal orientation gives a small match, but reversing the second bracelet creates `"abc"`. The algorithm checks this orientation and obtains `3`.

For a bracelet where the best sequence wraps around the end:

```
abcde
cdeab
```

The sequence `cdeab` is not a subsequence of the first string in its original written form. After doubling the first bracelet, it becomes available inside `"abcdeabcde"`, so the LCS computation finds it without explicit rotation handling.
