---
title: "CF 1335B - Construct the String"
description: "For each test case we have to build a lowercase string of length n. The condition is that every contiguous segment of length a must contain exactly b different letters. Any valid string is acceptable. The numbers describe a sliding window condition. If we look at positions 1..."
date: "2026-06-11T15:56:55+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1335
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 634 (Div. 3)"
rating: 900
weight: 1335
solve_time_s: 124
verified: false
draft: false
---

[CF 1335B - Construct the String](https://codeforces.com/problemset/problem/1335/B)

**Rating:** 900  
**Tags:** constructive algorithms  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case we have to build a lowercase string of length `n`. The condition is that every contiguous segment of length `a` must contain exactly `b` different letters. Any valid string is acceptable.

The numbers describe a sliding window condition. If we look at positions `1...a`, then `2...a+1`, then `3...a+2`, every such window must have the same number of distinct characters. We are free to choose the letters themselves.

The total sum of all values of `n` is at most 2000, so even quadratic algorithms would fit comfortably. The challenge is not performance but discovering a simple construction. Since the alphabet has only 26 lowercase letters and `b ≤ a`, a valid answer always exists.

Several edge cases are easy to mishandle.

Suppose `a = 1` and `b = 1`.

```
1
6 1 1
```

Every substring of length one contains exactly one distinct character, so any string works. A correct output is

```
aaaaaa
```

A careless solution that tries to cycle through several letters would still work, but it misses the fact that only one letter is needed.

Another interesting case is when `a = b`.

```
1
5 5 5
```

The only substring of length five must contain five distinct characters. One possible answer is

```
abcde
```

Using fewer than five letters would violate the requirement.

A more subtle example is

```
1
7 5 3
```

A string such as

```
abcabca
```

works because every window of length five contains only the letters `a`, `b`, and `c`. If we instead used

```
abcdeab
```

the first window would contain five distinct letters, which is incorrect.

## Approaches

A brute-force strategy would try to construct the string character by character. For every new position we could test all 26 letters and check whether every affected substring of length `a` still has exactly `b` distinct characters. Since each verification examines up to `a` characters, the amount of work grows quickly. In larger versions of the problem this approach becomes unattractive because the search space itself is enormous.

The key observation is that we do not need to satisfy every window independently. If we create a repeating pattern whose set of characters already contains exactly `b` different letters, then every length-`a` window will inherit the same set.

Take the first `b` letters of the alphabet and repeat them cyclically:

```
abcabcabc...
```

Since `b ≤ a`, any consecutive block of length `a` sees only those `b` letters, and each of them appears somewhere inside the block because the period is exactly `b`. The sliding windows automatically satisfy the condition.

The brute-force works because it checks the requirement directly, but fails because it searches unnecessarily. The observation that the answer can be periodic reduces the problem to a straightforward construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in n | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, prepare the first `b` lowercase letters: `"abc..."`.
2. Build the answer one position at a time.
3. At position `i`, place the character whose index is `i mod b`.

This creates a repeating pattern of length `b`.
4. Continue until the string reaches length `n`.
5. Output the constructed string.

### Why it works

The repeating block contains exactly `b` distinct letters. Since its period is also `b`, every group of `b` consecutive positions contains all these letters. A window of length `a` is at least as long as `b`, so every such window contains each of the `b` letters at least once. No additional letters ever appear, because only those first `b` characters are used. Hence every substring of length `a` contains exactly `b` distinct characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
ans = []

for _ in range(t):
    n, a, b = map(int, input().split())
    cur = []

    for i in range(n):
        cur.append(chr(ord('a') + (i % b)))

    ans.append("".join(cur))

print("\n".join(ans))
```

The solution processes test cases independently.

The expression `i % b` determines which character of the repeating block should be used. Position `0` gets `'a'`, position `1` gets `'b'`, and so on. After reaching the `b`-th letter, the pattern starts again.

The variable `a` does not appear in the code. That may look suspicious at first, but the proof above explains why the only requirement is that `b ≤ a`. Once the period is `b`, every window of length `a` automatically contains all `b` letters.

Using a list and `"".join()` avoids repeated string concatenation and keeps the implementation efficient.

## Worked Examples

Consider the sample case

```
7 5 3
```

The repeating block is `"abc"`.

| Position i | i mod b | Character | String so far |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 1 | b | ab |
| 2 | 2 | c | abc |
| 3 | 0 | a | abca |
| 4 | 1 | b | abcab |
| 5 | 2 | c | abcabc |
| 6 | 0 | a | abcabca |

The final answer is

```
abcabca
```

The windows

```
abcab
bcabc
cabca
```

all contain exactly three distinct letters.

Now consider

```
5 5 1
```

| Position i | i mod b | Character | String so far |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 0 | a | aa |
| 2 | 0 | a | aaa |
| 3 | 0 | a | aaaa |
| 4 | 0 | a | aaaaa |

The output becomes

```
aaaaa
```

The only length-five window contains one distinct letter, which matches the requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is generated once |
| Space | O(n) | The answer string is stored explicitly |

Since the sum of all values of `n` does not exceed 2000, the running time is tiny compared with the limits. Memory usage is also negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, a, b = map(int, input().split())
        cur = []

        for i in range(n):
            cur.append(chr(ord('a') + (i % b)))

        ans.append("".join(cur))

    return "\n".join(ans)

# provided sample
assert run(
"""4
7 5 3
6 1 1
6 6 1
5 2 2
"""
) == "abcabca\naaaaaa\naaaaaa\nababa"

# minimum size
assert run(
"""1
1 1 1
"""
) == "a"

# all values equal
assert run(
"""1
5 5 5
"""
) == "abcde"

# single distinct letter
assert run(
"""1
8 4 1
"""
) == "aaaaaaaa"

# maximum length pattern
assert run(
"""1
10 10 3
"""
) == "abcabcabca"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `a` | Minimum constraints |
| `5 5 5` | `abcde` | Case where all letters must be distinct |
| `8 4 1` | `aaaaaaaa` | Single repeated letter |
| `10 10 3` | `abcabcabca` | Repetition over many positions |

## Edge Cases

Consider

```
1
6 1 1
```

The algorithm uses `i mod 1`, which is always zero. Every position receives `'a'`, producing

```
aaaaaa
```

Every substring of length one contains one distinct letter, so the condition is satisfied.

Now consider

```
1
5 5 5
```

The indices modulo five are

```
0, 1, 2, 3, 4
```

which gives

```
abcde
```

The only window of length five contains exactly five different letters.

Finally, consider

```
1
7 5 3
```

The generated string is

```
abcabca
```

Its windows are

```
abcab
bcabc
cabca
```

Each window contains the same set `{a, b, c}`. Since no other letters appear and none of these three letters disappear from any window, the requirement holds throughout the string.
