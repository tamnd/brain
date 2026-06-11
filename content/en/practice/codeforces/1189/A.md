---
title: "CF 1189A - Keanu Reeves"
description: "We are given a binary string, which is a sequence of characters containing only 0 and 1. A string is defined as good if the count of zeros differs from the count of ones."
date: "2026-06-12T00:36:39+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 1189
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 572 (Div. 2)"
rating: 800
weight: 1189
solve_time_s: 174
verified: true
draft: false
---

[CF 1189A - Keanu Reeves](https://codeforces.com/problemset/problem/1189/A)

**Rating:** 800  
**Tags:** strings  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string, which is a sequence of characters containing only `0` and `1`. A string is defined as good if the count of zeros differs from the count of ones. The task is to split the original string into the smallest number of contiguous substrings such that every substring is good. The output must first state the number of substrings, then the substrings themselves, separated by spaces.

The constraints are small: the string length $n$ is at most 100. This allows algorithms that run in $O(n^2)$ comfortably, although a linear solution exists. Since we are dealing with small binary strings, the complexity is dominated more by the simplicity of splitting logic than by processing power.

Non-obvious edge cases include strings that are already good and strings where all characters are identical. For instance, if the input is `111` or `0`, the minimal number of substrings is one because the string itself is already good. Conversely, strings like `10` or `01` are not good, so each character must be split into individual substrings. A careless solution might attempt to always split the string into two halves or to greedily split only when adjacent characters differ, which would fail for `111000` or `1000`.

## Approaches

The brute-force approach would try every possible split of the string into contiguous substrings and check which combination produces only good substrings with minimal count. There are exponentially many splits, specifically $2^{n-1}$, so this is impractical even for $n = 100$.

The key observation is that the property of being good only depends on the counts of `0` and `1`. A string is good if all characters are the same or if it is not perfectly balanced. This reduces the problem: a string that is already good can remain intact. Only perfectly balanced strings with equal numbers of `0` and `1` need to be split. For a binary string, this is equivalent to checking if the string consists of exactly one `0` and one `1` of length two or larger. Therefore, in practice, the minimal number of substrings is almost always one, except when the string has exactly equal numbers of zeros and ones. In that case, we can split the string into two parts: one containing a single `0` or `1` and the rest, which guarantees both substrings are good.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the total number of zeros and ones in the input string. This allows us to determine if the whole string is already good.
2. If the counts are different, the whole string is good. Output `1` followed by the original string.
3. If the counts are equal, we must split. The simplest strategy is to take the first character as one substring and the remainder as the second substring. This guarantees both substrings are good because the first has count one for a single character, and the second has unequal counts after removing one character of either type.
4. Print the number of substrings, which is `1` if the string is good, or `2` if a split was needed, and then print the substrings.

Why it works: By maintaining the counts of zeros and ones, we can immediately determine if the whole string satisfies the good condition. Splitting off a single character when the counts are equal guarantees the resulting substrings are good, since the remainder will now have unequal counts. No other split produces fewer substrings, ensuring minimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

zeros = s.count('0')
ones = s.count('1')

if zeros != ones:
    print(1)
    print(s)
else:
    # counts are equal, split into first character and the rest
    print(2)
    print(s[0], s[1:])
```

The code first counts zeros and ones in the string, which is necessary to determine if the string is good. If the counts differ, the entire string is printed as a single substring. Otherwise, we split at the first character. The use of `s.strip()` ensures we remove any trailing newline from input, avoiding subtle bugs when printing substrings.

## Worked Examples

**Example 1**

Input:

```
1
1
```

| Step | zeros | ones | Condition | Output |
| --- | --- | --- | --- | --- |
| Count | 0 | 1 | 0 != 1 | 1 substring: 1 |

The string is already good, so minimal substrings is one.

**Example 2**

Input:

```
2
10
```

| Step | zeros | ones | Condition | Output |
| --- | --- | --- | --- | --- |
| Count | 1 | 1 | 1 == 1 | Split into '1' and '0' |

Counts are equal, so we split into first character and remainder. Both substrings are good.

**Example 3**

Input:

```
6
100011
```

| Step | zeros | ones | Condition | Output |
| --- | --- | --- | --- | --- |
| Count | 3 | 3 | 3 == 3 | Split into '1' and '00011' |

Splitting the first character ensures remaining substring has unequal zeros and ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting zeros and ones requires a full pass over the string. |
| Space | O(n) | Storing the string and substrings. |

Given $n \le 100$, this linear solution is extremely fast and fits within memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    s = input().strip()
    zeros = s.count('0')
    ones = s.count('1')
    if zeros != ones:
        return f"1\n{s}"
    else:
        return f"2\n{s[0]} {s[1:]}"

# Provided samples
assert run("1\n1\n") == "1\n1", "sample 1"
assert run("2\n10\n") == "2\n1 0", "sample 2"
assert run("6\n100011\n") == "2\n1 00011", "sample 3"

# Custom cases
assert run("3\n000\n") == "1\n000", "all zeros"
assert run("3\n111\n") == "1\n111", "all ones"
assert run("4\n0101\n") == "2\n0 101", "equal zeros and ones"
assert run("5\n00100\n") == "1\n00100", "unequal counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n000 | 1\n000 | String of identical zeros is good |
| 3\n111 | 1\n111 | String of identical ones is good |
| 4\n0101 | 2\n0 101 | Equal number of zeros and ones triggers split |
| 5\n00100 | 1\n00100 | Unequal counts allow single substring |

## Edge Cases

The minimal input `1` with string `1` or `0` is handled correctly: counts differ by default, so no split occurs. Strings of length `2` with equal numbers like `01` or `10` correctly produce two substrings. Strings with all identical characters, such as `000` or `111`, are returned as a single substring. The algorithm guarantees minimal substrings in all scenarios, as the only situation requiring a split is when counts are equal, which cannot be improved further.
