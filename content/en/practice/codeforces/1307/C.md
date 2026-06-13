---
title: "CF 1307C - Cow and Message"
description: "We are given a string of lowercase English letters. A message is any subsequence whose chosen indices form an arithmetic progression. The progression can have any positive difference, including the special case of length one. The task is not to find the message itself."
date: "2026-06-11T17:36:57+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 1307
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 621 (Div. 1 + Div. 2)"
rating: 1500
weight: 1307
solve_time_s: 793
verified: true
draft: false
---

[CF 1307C - Cow and Message](https://codeforces.com/problemset/problem/1307/C)

**Rating:** 1500  
**Tags:** brute force, dp, math, strings  
**Solve time:** 13m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of lowercase English letters. A message is any subsequence whose chosen indices form an arithmetic progression. The progression can have any positive difference, including the special case of length one.

The task is not to find the message itself. Instead, we must determine how many times the most frequent hidden message appears.

At first glance this looks like a subsequence problem with arithmetic progressions, which suggests something complicated. The crucial observation is that we only need the maximum frequency over all hidden strings, not the identity of the string.

The string length can reach $10^5$. Any solution that explicitly enumerates arithmetic progressions, subsequences, or candidate messages is immediately impossible. Even $O(n^2)$ is too large. We need something close to linear time.

A few edge cases are easy to miss.

Consider:

```
a
```

The only hidden message is `"a"`, which occurs once. The answer is:

```
1
```

A solution that only counts messages of length at least two would incorrectly return zero.

Consider:

```
aaaa
```

The message `"a"` occurs four times. The message `"aa"` occurs $\binom{4}{2}=6$ times. The answer is:

```
6
```

A solution that only tracks single letters would miss that a two-letter message can occur more often.

Consider:

```
abab
```

The message `"ab"` occurs four times:

$$(1,2),(1,4),(3,4),(3,2\text{ is invalid because order matters})$$

More systematically, every earlier `a` can pair with every later `b`. The answer comes from ordered pairs of letters, not necessarily equal letters.

The key lesson is that the maximum frequency may come either from a one-letter string or from a two-letter string.

## Approaches

A brute-force approach would try to enumerate hidden messages and count their occurrences. Even restricting ourselves to arithmetic progressions does not help. There are exponentially many subsequences, and the number of arithmetic progressions inside a string of length $10^5$ is enormous. This is completely infeasible.

The breakthrough comes from understanding a theorem hidden inside the problem.

Suppose a hidden message has length at least three. Every occurrence of that message contains a first character and a last character. If we forget the middle characters, each occurrence maps to an occurrence of a two-letter message formed by those endpoints.

This mapping is injective. Different occurrences of the longer message produce different endpoint pairs. That means the number of occurrences of any message of length at least three cannot exceed the number of occurrences of some two-letter message.

As a result, the most frequent hidden message must have length one or length two.

Now the problem becomes much simpler.

For length one, we only need the frequency of each character.

For length two, we need to count, for every ordered pair of letters $(a,b)$, how many pairs of indices $i<j$ satisfy:

$$s_i=a,\quad s_j=b.$$

There are only 26 lowercase letters, so there are only $26^2=676$ ordered pairs.

We can process the string from left to right. When we see a character $c$, every previously seen character $x$ creates new occurrences of the pair $(x,c)$.

This leads to a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(26n)$ | $O(26^2)$ | Accepted |

## Algorithm Walkthrough

1. Maintain an array `cnt[26]` where `cnt[x]` is the number of times letter `x` has appeared so far.
2. Maintain a matrix `pairs[26][26]` where `pairs[x][y]` stores the number of occurrences of the two-letter message consisting of letter `x` followed by letter `y`.
3. Scan the string from left to right.
4. Suppose the current character is `c`.
5. For every letter `x` from `a` to `z`, add `cnt[x]` to `pairs[x][c]`.

Every previous occurrence of `x` can be paired with the current occurrence of `c`, producing one new occurrence of the message `xc`.
6. Increase `cnt[c]` by one.
7. After processing the whole string, the answer is the maximum value among all entries of `cnt` and all entries of `pairs`.

### Why it works

For single-letter messages, `cnt[c]` is exactly the number of occurrences of that message.

For two-letter messages, every valid occurrence corresponds to a pair of positions $i<j$. When position $j$ is processed, position $i$ has already been counted inside `cnt`. The algorithm adds exactly one contribution for that pair and never counts it again.

The remaining question is why longer messages can be ignored. Let a message $t$ of length at least three start with letter $a$ and end with letter $b$. Every occurrence of $t$ determines a unique occurrence of the two-letter message $ab$ using the first and last chosen positions. Distinct occurrences of $t$ produce distinct endpoint pairs. Hence:

$$\text{occurrences}(t) \le \text{occurrences}(ab).$$

So no message of length at least three can beat the best one-letter or two-letter message. The algorithm checks all such candidates, therefore the maximum it returns is the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

cnt = [0] * 26
pairs = [[0] * 26 for _ in range(26)]

for ch in s:
    c = ord(ch) - ord('a')

    for x in range(26):
        pairs[x][c] += cnt[x]

    cnt[c] += 1

ans = max(cnt)

for i in range(26):
    for j in range(26):
        ans = max(ans, pairs[i][j])

print(ans)
```

The array `cnt` tracks all one-letter messages. The matrix `pairs` tracks all two-letter messages.

The update order matters. We must first add contributions from previously seen characters and only then increment the count of the current character. Otherwise a character could incorrectly pair with itself at the same position.

All counts fit comfortably inside 64-bit integers. In the worst case, a two-letter message can occur about:

$$\binom{10^5}{2} \approx 5 \times 10^9,$$

which is much larger than 32-bit limits. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
aaabb
```

Processing trace:

| Position | Character | cnt[a] before | cnt[b] before | pairs[a][a] | pairs[a][b] |
| --- | --- | --- | --- | --- | --- |
| 1 | a | 0 | 0 | 0 | 0 |
| 2 | a | 1 | 0 | 1 | 0 |
| 3 | a | 2 | 0 | 3 | 0 |
| 4 | b | 3 | 0 | 3 | 3 |
| 5 | b | 3 | 1 | 3 | 6 |

Final values:

| Message | Count |
| --- | --- |
| a | 3 |
| b | 2 |
| aa | 3 |
| ab | 6 |
| bb | 1 |

The maximum is 6, which matches the sample answer.

### Example 2

Input:

```
abc
```

Processing trace:

| Position | Character | New pair contributions |
| --- | --- | --- |
| 1 | a | none |
| 2 | b | ab += 1 |
| 3 | c | ac += 1, bc += 1 |

Final counts:

| Message | Count |
| --- | --- |
| a | 1 |
| b | 1 |
| c | 1 |
| ab | 1 |
| ac | 1 |
| bc | 1 |

Every hidden message occurs at most once, so the answer is 1.

This example demonstrates that the algorithm naturally handles strings with all distinct letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(26n)$ | For each character we iterate through all 26 letters |
| Space | $O(26^2)$ | The pair-count matrix has 676 entries |

Since $26$ is a constant, the running time is effectively linear in the string length. For $n=10^5$, the algorithm performs roughly 2.6 million updates, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = sys.stdin.readline().strip()

    cnt = [0] * 26
    pairs = [[0] * 26 for _ in range(26)

    ]

    for ch in s:
        c = ord(ch) - ord('a')

        for x in range(26):
            pairs[x][c] += cnt[x]

        cnt[c] += 1

    ans = max(cnt)

    for i in range(26):
        for j in range(26):
            ans = max(ans, pairs[i][j])

    return str(ans)

# provided sample
assert solve("aaabb\n") == "6"

# minimum size
assert solve("a\n") == "1"

# all equal
assert solve("aaaa\n") == "6"

# distinct letters
assert solve("abc\n") == "1"

# alternating pattern
assert solve("abab\n") == "3"

# large repetition structure
assert solve("aabb\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `1` | Minimum size string |
| `aaaa` | `6` | Two-letter message beats single-letter message |
| `abc` | `1` | No repeated message |
| `abab` | `3` | Ordered pair counting |
| `aabb` | `4` | Cross-group pair accumulation |

## Edge Cases

Consider:

```
a
```

The array `cnt` becomes `[1,0,...]`. No pair counts are created. The maximum value is 1, which is correct.

Consider:

```
aaaa
```

The updates generate:

$$pairs[a][a] = 1+2+3 = 6.$$

The single-letter count is only 4. The algorithm correctly returns 6.

Consider:

```
abab
```

When the second `b` is processed, there are already two `a` characters before it, so two new `ab` occurrences are added. The final value of `pairs[a][b]` becomes 3, corresponding to the pairs:

$$(1,2),\ (1,4),\ (3,4).$$

The algorithm counts each valid ordered pair exactly once.

Consider:

```
abcdefghijklmnopqrstuvwxyz
```

Every character appears once. Every two-letter message appears at most once. The maximum among all stored values remains 1, which is the correct answer.
