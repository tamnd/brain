---
title: "CF 102433E - Rainbow Strings"
description: "We have a lowercase string, and we want to count its subsequences whose chosen characters are all different. A subsequence is determined by the positions we choose, so choosing the first a from aab and choosing the second a are different subsequences, even though both produce…"
date: "2026-08-10T07:40:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102433
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ACM-ICPC Pacific Northwest Regional Contest (Div. 1)"
rating: 0
weight: 102433
solve_time_s: 209
verified: true
draft: false
---

[CF 102433E - Rainbow Strings](https://codeforces.com/problemset/problem/102433/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a lowercase string, and we want to count its subsequences whose chosen characters are all different. A subsequence is determined by the positions we choose, so choosing the first `a` from `aab` and choosing the second `a` are different subsequences, even though both produce the one-character string `a`. The empty subsequence is also valid.

The key question is not really about the order of the letters. Once we decide which positions are selected, their original order automatically gives a subsequence. For a rainbow subsequence, each letter can contribute either zero selected positions or exactly one selected position. That observation turns the problem into a product of independent choices.

The string has length at most `100000`, so an algorithm that examines all subsequences is completely infeasible. There are `2^n` subsequences, which is already astronomically large for `n = 100000`. Even an algorithm with quadratic time, around `10^10` operations at the maximum size, would be far beyond a one-second limit. We need a linear or near-linear solution.

There are several edge cases that can make a careless implementation fail. For `a`, the correct answer is `2`, because we may choose the `a` or choose nothing. An implementation that forgets the empty subsequence would return `1`.

For `aaa`, the answer is `4`. We can choose none of the three positions, or choose exactly one of the three positions. Choosing two positions is invalid because the resulting subsequence contains the same letter twice. A common mistake is to count the different resulting strings instead of the different position choices, which would incorrectly give only `2`, namely the empty string and `a`.

For `aab`, the answer is `6`. The valid subsequences are the empty subsequence, three one-character subsequences, and two valid length-two subsequences containing one `a` and the `b`. The two choices of the `a` are different because they use different positions.

## Approaches

A direct solution would enumerate every subset of positions. For each subset, we could inspect the selected characters and check whether any letter appears twice. This is correct because every subset of positions represents exactly one subsequence. However, there are `2^n` subsets, and checking each subset can itself take up to `O(n)` time. The resulting worst-case complexity is `O(n 2^n)`, with `2^100000` candidate subsequences at the maximum input size. Even generating those candidates is impossible.

The useful observation is that a rainbow subsequence places an extremely simple restriction on each letter independently. Suppose the letter `c` occurs `cnt[c]` times in the original string. In a rainbow subsequence, there are exactly `cnt[c] + 1` possibilities for this letter: choose none of its occurrences, or choose exactly one of its `cnt[c]` occurrences.

These choices are independent between different letters. If we choose one occurrence of `a` and one occurrence of `b`, their positions already determine the order in the subsequence. We do not need to make an additional ordering choice. Thus every combination of per-letter choices produces exactly one valid rainbow subsequence, and every valid rainbow subsequence corresponds to exactly one such combination.

With 26 lowercase letters, the total number is therefore

[
\prod_{c='a'}^{'z'} (cnt[c] + 1).
]

The empty subsequence is naturally included by choosing zero occurrences for every letter.

The brute-force works because a subsequence is completely determined by its selected positions, but it fails because there are exponentially many position subsets. The observation that every letter can independently be selected zero or one time reduces the problem to counting 26 frequencies and multiplying 26 small factors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n 2^n)` | `O(n)` | Too slow |
| Frequency Product | `O(n + 26)` | `O(26)` | Accepted |

## Algorithm Walkthrough

1. Create a frequency array with one entry for each lowercase letter. Scan the string once and increment the frequency corresponding to every character. This gives us the number of possible positions from which each letter can be selected.
2. Initialize the answer to `1`. This represents the single choice where no letter is selected, which is the empty subsequence.
3. For every lowercase letter, multiply the answer by `cnt[c] + 1` and reduce it modulo `11092019`. The factor counts all possibilities for that letter: selecting no occurrence or selecting exactly one of its occurrences.
4. Print the resulting product. Because each letter's choice is independent, the product counts every rainbow subsequence exactly once.

### Why it works

Consider any rainbow subsequence. For every letter, record whether it is absent or, if present, which occurrence of that letter was selected. Since the subsequence contains no repeated letters, this description has exactly one choice for every letter: zero choices if absent, or one of its occurrences if present. Conversely, any collection of these per-letter choices selects at most one position for each letter, so the selected positions always form a rainbow subsequence when read in their original order. Thus there is a one-to-one correspondence between rainbow subsequences and the combinations counted by

[
\prod_c (cnt[c]+1).
]

The multiplication counts exactly the desired objects, including the empty subsequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 11092019

def solve():
    s = input().strip()

    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    ans = 1
    for x in cnt:
        ans = ans * (x + 1) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop builds the frequency array. Since the input contains only lowercase English letters, `ord(ch) - ord('a')` maps every character directly into the range `0` through `25`.

The second loop applies the product formula. Starting with `ans = 1` is necessary because the empty subsequence must be counted. For a letter appearing `x` times, multiplying by `x + 1` accounts for all ways to either omit that letter or select one of its occurrences.

The modulo is applied after every multiplication. Python integers do not overflow, but keeping the value reduced throughout the computation is both natural for the required answer and keeps intermediate values small. There is no off-by-one issue in the frequency factor: if a letter appears once, its factor is `2`, representing "do not select it" and "select its only occurrence"; if it appears zero times, its factor is `1` and it has no effect.

## Worked Examples

### Sample 1: `aab`

The frequency counts are `a = 2` and `b = 1`, while every other letter has frequency zero. The product therefore becomes `(2 + 1)(1 + 1) = 6`.

| Character | Frequency | Factor | Running answer |
| --- | --- | --- | --- |
| `a` | 2 | 3 | 3 |
| `b` | 1 | 2 | 6 |
| `c` through `z` | 0 | 1 each | 6 |

The three choices for `a` are to select neither occurrence, select the first occurrence, or select the second occurrence. The two choices for `b` are to select it or not. Their combinations give six valid subsequences, including the empty one.

### Sample 2: `icpcprogrammingcontest`

The nonzero frequencies are `c = 3`, eight letters with frequency `2`, namely `g`, `i`, `m`, `n`, `o`, `p`, `r`, and `t`, and three letters with frequency `1`, namely `a`, `e`, and `s`.

| Frequency group | Number of letters | Factor per letter | Contribution |
| --- | --- | --- | --- |
| 3 | 1 | 4 | 4 |
| 2 | 8 | 3 | 6561 |
| 1 | 3 | 2 | 8 |
| 0 | 14 | 1 | 1 |

The final answer is

[
4 \times 3^8 \times 2^3 = 209952.
]

The trace demonstrates why the actual positions do not need to be considered after counting frequencies. Every time we choose one occurrence from each selected letter, the original indices automatically establish the subsequence order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + 26)` | One pass counts the characters, then 26 factors are multiplied. |
| Space | `O(26)` | Only the frequency of each lowercase letter is stored. |

With `n` up to `100000`, the algorithm performs only one linear scan of the input followed by 26 constant-size operations. This is easily within the intended limits, unlike any approach that enumerates or compares subsequences.

## Test Cases

```python
import sys
import io

MOD = 11092019

def solution(s):
    cnt = [0] * 26

    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    ans = 1
    for x in cnt:
        ans = ans * (x + 1) % MOD

    return str(ans)

def run(inp: str) -> str:
    return solution(inp.strip())

# Provided samples
assert run("aab") == "6", "sample 1"
assert run("icpcprogrammingcontest") == "209952", "sample 2"

# Minimum-size input
assert run("a") == "2", "single character"

# All characters equal
assert run("aaa") == "4", "three identical characters"

# Every character distinct
assert run("abcdefghijklmnopqrstuvwxyz") == str(pow(2, 26, MOD)), \
    "all 26 letters occur once"

# Maximum-size input
assert run("a" * 100000) == "100001", \
    "100000 identical characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `2` | Minimum input and inclusion of the empty subsequence |
| `aaa` | `4` | Repeated letters and position-based subsequences |
| `abcdefghijklmnopqrstuvwxyz` | `67108864` | All 26 letters occur once, so every subset is rainbow |
| `"a" * 100000` | `100001` | Maximum input size and the repeated-letter boundary case |

For the all-distinct test, every one of the 26 letters can independently be chosen or omitted, so the answer is `2^26 = 67108864`. For the maximum-size all-`a` test, only zero or one of the `100000` positions may be selected, giving `100001`.

## Edge Cases

For the single-character input `a`, the frequency of `a` is `1`, so its factor is `2`. Every other character contributes a factor of `1`. The final answer is `2`, corresponding to the empty subsequence and the subsequence containing the only position.

For `aaa`, the frequency of `a` is `3`, so the answer is `3 + 1 = 4`. The four choices are selecting no `a`, selecting position one, selecting position two, or selecting position three. The algorithm never counts a pair of positions because the single letter has only one selection slot in a rainbow subsequence.

For `aab`, the factors are `3` for `a` and `2` for `b`, producing `6`. This catches the mistake of counting distinct resulting strings rather than distinct position selections. The two subsequences containing `a` and `b` can use either of the two `a` positions, so they must both be counted.

For a string containing every lowercase letter exactly once, every subsequence is automatically rainbow. There are `2^26` subsets of positions, and the product formula gives exactly `2` for each of the 26 letters, producing `2^26`. This checks that the algorithm handles the maximum possible number of distinct letters correctly.

For `100000` copies of `a`, the answer is `100001`. Only one position can be selected because selecting two positions would repeat `a`. The algorithm obtains this directly from the single factor `100000 + 1`, demonstrating that large frequencies do not require dynamic programming over the positions.
