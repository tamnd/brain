---
title: "CF 1760B - Atilla's Favorite Problem"
description: "We are given several lowercase strings. For each string, we want the smallest alphabet that contains every character appearing in that string. The alphabet is always a prefix of the English alphabet."
date: "2026-06-09T14:21:06+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1760
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 835 (Div. 4)"
rating: 800
weight: 1760
solve_time_s: 207
verified: true
draft: false
---

[CF 1760B - Atilla's Favorite Problem](https://codeforces.com/problemset/problem/1760/B)

**Rating:** 800  
**Tags:** greedy, implementation, strings  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several lowercase strings. For each string, we want the smallest alphabet that contains every character appearing in that string.

The alphabet is always a prefix of the English alphabet. An alphabet of size 1 contains only `a`, an alphabet of size 2 contains `a` and `b`, and so on. An alphabet of size 26 contains every lowercase letter.

The question is simply: what is the smallest prefix of the alphabet that still includes all characters used in the string?

A useful way to think about it is to focus on the largest letter present. If a string contains the letter `w`, then any valid alphabet must contain all letters from `a` through `w`. Since `w` is the 23rd letter, the answer must be at least 23. If all other letters are earlier than `w`, then an alphabet of size 23 is already enough.

The constraints are tiny. Each string has length at most 100, and there are at most 1000 test cases. Even an $O(n^2)$ solution would be completely fine here. We only need to scan each string once.

One easy mistake is to count distinct characters instead of finding the largest character.

Consider:

```
1
3
bcf
```

The distinct letters are `{b,c,f}`, which has size 3. A careless solution would output 3. The correct answer is 6 because `f` is the 6th letter, and any alphabet containing `f` must also contain `a` through `e`.

Another mistake is to use the string length.

Consider:

```
1
5
zzzzz
```

The string length is 5, but the answer is 26 because `z` is the 26th letter.

A third mistake is to sort characters and use the number of unique letters.

Consider:

```
1
4
down
```

There are four distinct letters, but the largest is `w`, so the answer is 23.

## Approaches

A brute-force approach would try every alphabet size from 1 to 26. For each size, we would check whether every character of the string belongs to that alphabet. The first valid size would be the answer.

This works because there are only 26 possible alphabet sizes. For a string of length $n$, the complexity is $O(26n)$.

The key observation is that the answer is completely determined by the largest character in the string. If the largest character is `k`, then every smaller character is automatically included in the alphabet of size corresponding to `k`. Any smaller alphabet would miss `k` itself.

That reduces the problem to finding the maximum character and converting it to its position in the alphabet.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n` and the string `s`.
3. Find the largest character in `s`.
4. Convert that character to its alphabet position using:

`ord(max_char) - ord('a') + 1`
5. Output the resulting value.

The reason this works is that an alphabet of size `x` contains exactly the letters from `a` through the `x`-th letter. The largest character appearing in the string is the only character that determines how far this prefix must extend.

### Why it works

Let `c` be the largest character appearing in the string.

Any valid alphabet must contain `c`, so its size must be at least the alphabet position of `c`.

An alphabet whose size equals the position of `c` contains every letter from `a` through `c`. Since no character in the string is larger than `c`, all characters are included.

The minimum valid alphabet size is exactly the position of the largest character.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    ans = ord(max(s)) - ord('a') + 1
    print(ans)
```

The implementation directly follows the observation from the algorithm.

The call to `max(s)` finds the lexicographically largest lowercase letter in the string. Since lowercase letters appear in alphabetical order in the ASCII table, the largest character is also the alphabetically latest character.

The expression

```
ord(max(s)) - ord('a') + 1
```

converts that character into a 1-based alphabet index. For example:

```
ord('a') - ord('a') + 1 = 1
ord('f') - ord('a') + 1 = 6
ord('z') - ord('a') + 1 = 26
```

There are no overflow concerns because all values are tiny. The only subtle point is removing the trailing newline with `.strip()` before processing the string.

## Worked Examples

### Example 1

Input:

```
1
4
down
```

| Step | Current Maximum |
| --- | --- |
| d | d |
| o | o |
| w | w |
| n | w |

The largest character is `w`.

| Character | Position |
| --- | --- |
| w | 23 |

Answer: `23`.

This example shows that the answer depends on the largest character, not on the number of distinct characters.

### Example 2

Input:

```
1
3
bcf
```

| Step | Current Maximum |
| --- | --- |
| b | b |
| c | c |
| f | f |

The largest character is `f`.

| Character | Position |
| --- | --- |
| f | 6 |

Answer: `6`.

This example demonstrates why counting distinct letters would be incorrect. There are only three distinct letters, but the required alphabet size is six.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan of the string |
| Space | O(1) | Only a few variables are used |

Since each string has length at most 100, the running time is extremely small. Even with 1000 test cases, the total work is only about 100,000 character operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()
        out.append(str(ord(max(s)) - ord('a') + 1))

    return "\n".join(out)

# provided sample
assert run(
    "5\n"
    "1\n"
    "a\n"
    "4\n"
    "down\n"
    "10\n"
    "codeforces\n"
    "3\n"
    "bcf\n"
    "5\n"
    "zzzzz\n"
) == "1\n23\n19\n6\n26"

# minimum size
assert run("1\n1\na\n") == "1"

# largest possible letter
assert run("1\n1\nz\n") == "26"

# all characters identical
assert run("1\n5\nmmmmm\n") == "13"

# mixed letters
assert run("1\n6\nabczxy\n") == "26"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1` | Smallest possible answer |
| `z` | `26` | Largest possible answer |
| `mmmmm` | `13` | Repeated characters |
| `abczxy` | `26` | Largest character determines answer |

## Edge Cases

Consider the input:

```
1
1
a
```

The largest character is `a`, whose position is 1. The algorithm outputs 1. This verifies the smallest possible alphabet.

Consider:

```
1
5
zzzzz
```

Every character is `z`. The maximum character is still `z`, whose position is 26. The algorithm outputs 26. Repeated occurrences do not affect the result.

Consider:

```
1
3
bcf
```

The maximum character is `f`. The algorithm outputs 6. This confirms that the answer is not the number of distinct letters.

Consider:

```
1
4
down
```

The maximum character is `w`. The algorithm outputs 23. Even though only four different letters appear, the alphabet must extend through the 23rd letter to include `w`.
