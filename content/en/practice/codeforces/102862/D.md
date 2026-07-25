---
title: "CF 102862D - Splitting Text"
description: "We are given a lowercase English string. We want to cut it into the largest possible number of consecutive pieces. A piece is considered a valid word only if it contains at least one vowel and at least one consonant."
date: "2026-07-25T13:50:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102862
codeforces_index: "D"
codeforces_contest_name: "LU ICPC Selection Contest 2020 and KFU Open Contest 2020"
rating: 0
weight: 102862
solve_time_s: 43
verified: true
draft: false
---

[CF 102862D - Splitting Text](https://codeforces.com/problemset/problem/102862/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase English string. We want to cut it into the largest possible number of consecutive pieces. A piece is considered a valid word only if it contains at least one vowel and at least one consonant. The output is the maximum number of such valid pieces that can cover the whole string. If even one valid piece cannot be formed, the answer is zero.

The only properties of characters that matter are their types. A character is either one of the vowels `a, i, o, u, e, y`, or it is a consonant. The positions of the letters matter for constructing a partition, but the number of possible pieces depends only on how many vowels and consonants exist.

The string length can reach $10^5$. This rules out trying every possible set of cut positions because the number of partitions grows exponentially. Even an $O(n^2)$ dynamic programming approach would be unnecessary and too slow compared with a simple linear scan. The intended solution should inspect every character a constant number of times, giving an $O(n)$ algorithm.

The first edge case is when the string contains only one type of character. For example:

```
Input:
3
aaa

Output:
0
```

There are vowels but no consonants, so no valid word can exist. A solution that only counts vowels and divides by something would incorrectly produce a positive answer.

Another edge case is when the number of one type is much smaller than the other:

```
Input:
7
aaabbbb

Output:
3
```

There are three vowels and four consonants. We can create three valid words, but not four, because every word needs a vowel. The limiting resource is the smaller count.

A final boundary case is when both types appear exactly once:

```
Input:
2
ab

Output:
1
```

The whole string is already one valid word. Trying to split at every possible position would create invalid one-character pieces.

## Approaches

A natural brute-force approach is to try every possible partition of the string and check whether every resulting piece contains both a vowel and a consonant. This is correct because it examines every possible answer, but the number of partitions of a string of length $n$ is $2^{n-1}$, since every gap between adjacent characters can either contain a cut or not. For $n=10^5$, this is completely impossible.

A better attempt is to build words greedily from left to right. However, the key observation is that we do not actually need to care about the exact locations of the cuts. Every valid word consumes at least one vowel and at least one consonant. If there are $v$ vowels and $c$ consonants, no solution can have more than $\min(v,c)$ words because each word requires one character from both groups.

The remaining question is whether this upper bound can always be achieved. If both vowels and consonants exist, we can repeatedly pair the scarcer type with a character of the other type while preserving the original order. The extra characters of the more common type can simply be attached to existing words. This means every available vowel can participate in a separate word if vowels are the limiting resource, and the same argument works when consonants are fewer.

The problem therefore reduces to counting the two character categories.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many vowels appear in the string and how many consonants appear in the string. The answer can only depend on these two quantities because every word needs exactly one character from each category at minimum.
2. If either count is zero, output `0`. A valid word needs both types, so the string cannot be partitioned.
3. Otherwise, output the smaller of the two counts. This is the maximum possible number of words because each word consumes one vowel and one consonant.

Why it works:

The maximum number of words cannot exceed the number of vowels or the number of consonants, so it cannot exceed $\min(v,c)$. If both categories are present, the smaller group can be distributed one character per word, while all remaining characters from the larger group can be placed into these words without invalidating them. Thus the upper bound is always achievable, and the answer is exactly $\min(v,c)$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    vowels = set("aiouey")
    v = 0
    c = 0

    for ch in s:
        if ch in vowels:
            v += 1
        else:
            c += 1

    if v == 0 or c == 0:
        print(0)
    else:
        print(min(v, c))

if __name__ == "__main__":
    solve()
```

The code first stores the vowel set because every character classification is the same operation. During the scan, it increments one of two counters. No information about positions needs to be saved because the final answer is determined entirely by the two totals.

The condition `v == 0 or c == 0` handles the impossible case directly. The final `min(v, c)` is safe because the proof shows that the smaller category is the only limiting factor.

There are no indexing operations or nested loops, so there are no boundary issues or off-by-one cases. Python integers also avoid overflow concerns, although the counters are at most $10^5$.

## Worked Examples

### Sample 1

Input:

```
13
brownfoxjumps
```

The algorithm counts vowels and consonants.

| Step | Character | Vowels | Consonants |
| --- | --- | --- | --- |
| 1 | b | 0 | 1 |
| 2 | r | 0 | 2 |
| 3 | o | 1 | 2 |
| 4 | w | 1 | 3 |
| 5 | n | 1 | 4 |
| 6 | f | 1 | 5 |
| 7 | o | 2 | 5 |
| 8 | x | 2 | 6 |
| 9 | j | 2 | 7 |
| 10 | u | 3 | 7 |
| 11 | m | 3 | 8 |
| 12 | p | 3 | 9 |
| 13 | s | 3 | 10 |

The final counts are 3 vowels and 10 consonants, so the answer is:

```
3
```

This demonstrates that extra consonants do not increase the number of possible words.

### Sample 2

Input:

```
4
iota
```

| Step | Character | Vowels | Consonants |
| --- | --- | --- | --- |
| 1 | i | 1 | 0 |
| 2 | o | 2 | 0 |
| 3 | t | 2 | 1 |
| 4 | a | 3 | 1 |

There are 3 vowels and 1 consonant, so only one valid word can be formed.

Output:

```
1
```

This demonstrates that the rarest character type limits the number of partitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every character is inspected exactly once. |
| Space | O(1) | Only two counters and a fixed vowel set are stored. |

The string length can be $10^5$, so a linear solution easily fits within the time limit. The memory usage stays constant regardless of the input size.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# provided samples
assert run("13\nbrownfoxjumps\n") == "3\n", "sample 1"
assert run("4\niota\n") == "1\n", "sample 2"
assert run("3\nyou\n") == "0\n", "sample 3"

# custom cases
assert run("2\nab\n") == "1\n", "minimum valid string"
assert run("5\naaaaa\n") == "0\n", "only vowels"
assert run("8\nbbbbbbbb\n") == "0\n", "only consonants"
assert run("7\naaabbbb\n") == "3\n", "different counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ab` | `1` | Smallest possible valid word |
| `aaaaa` | `0` | Missing consonants |
| `bbbbbbbb` | `0` | Missing vowels |
| `aaabbbb` | `3` | The smaller category limits the answer |

## Edge Cases

For a string containing only vowels, such as:

```
3
aaa
```

the algorithm counts `v = 3` and `c = 0`. Since there are no consonants, the zero check triggers and the output is `0`.

For a string containing only consonants:

```
4
bbbb
```

the counters become `v = 0` and `c = 4`. Again, no valid word can contain both required categories, so the answer is `0`.

For a string where one category is smaller:

```
7
aaabbbb
```

the scan finds three vowels and four consonants. The answer is `min(3, 4) = 3`. Three words can each receive one vowel and one consonant, while the remaining consonant is added to one of those words.

For the smallest mixed case:

```
2
ab
```

the counts are one vowel and one consonant. The algorithm returns `1`, matching the only possible partition.
