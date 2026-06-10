---
title: "CF 1532C - Uniform String"
description: "For each test case, we must build a string of length n using only the first k lowercase letters, namely 'a', 'b', ..., up to the k-th letter. Every one of these k letters must appear at least once."
date: "2026-06-10T16:39:41+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1532
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Practice 7"
rating: 0
weight: 1532
solve_time_s: 165
verified: false
draft: false
---

[CF 1532C - Uniform String](https://codeforces.com/problemset/problem/1532/C)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 2m 45s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case, we must build a string of length `n` using only the first `k` lowercase letters, namely `'a'`, `'b'`, ..., up to the `k`-th letter.

Every one of these `k` letters must appear at least once. Among all valid strings, we want to maximize the frequency of the least frequent letter. If multiple strings achieve that optimum value, any of them may be printed.

The constraints are tiny. The string length never exceeds `100`, and there are at most `100` test cases. Even a relatively inefficient construction would fit comfortably within the limits. The real challenge is understanding what distribution of letters maximizes the minimum frequency.

The objective is a balancing problem. If one letter appears much more often than the others, those extra occurrences do not help the minimum frequency. To maximize the smallest count, we want the occurrences of the `k` letters to be distributed as evenly as possible.

One easy mistake is to place every required letter once and then fill the remaining positions with `'a'`.

For example:

```
n = 7, k = 3
```

A careless construction might produce:

```
abcaaaa
```

The frequencies are:

```
a = 5
b = 1
c = 1
```

The minimum frequency is only `1`, while it is possible to achieve `2` by distributing the extra positions more evenly.

Another edge case is when `n = k`.

```
n = 4, k = 4
```

Every letter must appear exactly once, so the answer is simply a permutation of:

```
abcd
```

The maximum possible minimum frequency is `1`.

A third edge case occurs when `k = 1`.

```
n = 6, k = 1
```

Only the letter `'a'` may be used. The answer must be:

```
aaaaaa
```

The minimum frequency is `6`, which is also the maximum possible value.

## Approaches

A brute-force viewpoint is to think about all possible distributions of `n` positions among the first `k` letters. For each distribution, we could check whether every letter appears at least once and compute the minimum frequency. The number of possible strings is roughly `k^n`, which becomes enormous even for moderate values. This approach is completely impractical.

The key observation is that the order of letters does not affect the minimum frequency. Only the counts matter.

Suppose the frequencies are:

```
c1, c2, ..., ck
```

Their sum is `n`.

To maximize the smallest frequency, we should make these counts as equal as possible. If one letter exceeds another by at least two, moving one occurrence from the larger group to the smaller group increases the minimum frequency or keeps it unchanged while making the distribution more balanced.

The most balanced distribution is obtained by repeatedly cycling through the first `k` letters:

```
abcabcabc...
```

Whenever we place a new character, we give one more occurrence to the next letter in the cycle. After `n` placements, every letter count differs from every other count by at most one.

This immediately achieves the optimal distribution, because no valid solution can make every frequency exceed `⌊n/k⌋`, and the cyclic construction gives each letter either `⌊n/k⌋` or `⌈n/k⌉` occurrences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(kⁿ) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty string builder.
2. For each position `i` from `0` to `n - 1`, choose the character corresponding to `i % k`.
3. Append that character to the answer.
4. After processing all `n` positions, output the constructed string.

The modulo operation cycles through:

```
0, 1, 2, ..., k-1, 0, 1, 2, ...
```

which corresponds to:

```
a, b, c, ..., repeated
```

As a result, the frequencies stay as balanced as possible.

### Why it works

The construction distributes the `n` positions among the `k` letters in round-robin fashion. After all positions are assigned, every letter appears either `⌊n/k⌋` times or `⌈n/k⌉` times.

No valid solution can make the minimum frequency exceed `⌊n/k⌋`, because the total number of characters is only `n`. Our construction achieves exactly that bound for every letter. Since the minimum frequency is as large as theoretically possible, the produced string is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())

        ans = []
        for i in range(n):
            ans.append(chr(ord('a') + (i % k)))

        print("".join(ans))

solve()
```

The implementation directly follows the round-robin idea.

The expression:

```
i % k
```

selects which of the first `k` letters should be used at position `i`.

The character is generated by shifting from `'a'`:

```
chr(ord('a') + (i % k))
```

Because every position is processed exactly once, the running time is linear in the string length.

There are no tricky boundary conditions. When `k = 1`, the modulo is always zero, producing only `'a'`. When `n = k`, each letter appears exactly once before the cycle could repeat.

## Worked Examples

### Example 1

Input:

```
n = 7, k = 3
```

| i | i % k | Character | Current String |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 1 | b | ab |
| 2 | 2 | c | abc |
| 3 | 0 | a | abca |
| 4 | 1 | b | abcab |
| 5 | 2 | c | abcabc |
| 6 | 0 | a | abcabca |

Output:

```
abcabca
```

The frequencies are:

```
a = 3
b = 2
c = 2
```

The minimum frequency is `2`, which is optimal.

### Example 2

Input:

```
n = 6, k = 2
```

| i | i % k | Character | Current String |
| --- | --- | --- | --- |
| 0 | 0 | a | a |
| 1 | 1 | b | ab |
| 2 | 0 | a | aba |
| 3 | 1 | b | abab |
| 4 | 0 | a | ababa |
| 5 | 1 | b | ababab |

Output:

```
ababab
```

The frequencies are:

```
a = 3
b = 3
```

This demonstrates the perfectly balanced case where `n` is divisible by `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each position is generated once |
| Space | O(n) | The answer string is stored before printing |

Since `n ≤ 100`, the total amount of work is tiny. The solution easily fits within any reasonable time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        ans = []
        for i in range(n):
            ans.append(chr(ord('a') + (i % k)))

        out.append("".join(ans))

    return "\n".join(out)

# provided sample
assert run("3\n7 3\n4 4\n6 2\n") == "abcabca\nabcd\nababab"

# minimum size
assert run("1\n1 1\n") == "a"

# k = 1
assert run("1\n6 1\n") == "aaaaaa"

# n = k
assert run("1\n5 5\n") == "abcde"

# near maximum values
assert run("1\n26 26\n") == "abcdefghijklmnopqrstuvwxyz"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `a` | Smallest valid instance |
| `6 1` | `aaaaaa` | Single-letter alphabet |
| `5 5` | `abcde` | Every letter used exactly once |
| `26 26` | `abcdefghijklmnopqrstuvwxyz` | Largest alphabet size |

## Edge Cases

Consider:

```
1
4 4
```

The algorithm generates:

```
abcd
```

Each letter appears exactly once. Since all four required letters must be present and the string length is also four, no letter can appear more than once. The minimum frequency is correctly `1`.

Consider:

```
1
6 1
```

The modulo sequence is:

```
0 0 0 0 0 0
```

The generated string is:

```
aaaaaa
```

Only `'a'` is allowed, so this is the unique valid answer. The minimum frequency equals `6`.

Consider:

```
1
7 3
```

The algorithm produces:

```
abcabca
```

The frequencies become:

```
a = 3
b = 2
c = 2
```

All counts differ by at most one. Any attempt to increase the minimum frequency above `2` would require at least three occurrences of every letter, which would need `9` total characters. Since only `7` positions exist, the obtained minimum frequency is optimal.
