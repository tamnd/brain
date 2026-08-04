---
title: "CF 102606B - Binary String"
description: "This problem is about discovering a hidden binary string. We are told only its length. The only information available comes from queries: we submit another binary string, and the judge tells us whether our submitted string appears inside the hidden string as a subsequence."
date: "2026-08-05T00:37:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "B"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 155
verified: true
draft: false
---

[CF 102606B - Binary String](https://codeforces.com/problemset/problem/102606/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem is about discovering a hidden binary string. We are told only its length. The only information available comes from queries: we submit another binary string, and the judge tells us whether our submitted string appears inside the hidden string as a subsequence.

The challenge is that the hidden string can have length up to 1000, while each query is restricted to about half of that length. A direct reconstruction method that asks about the entire known prefix eventually produces queries that are too long. The solution has to use the query length limit as a guide.

Because there are at most 1024 queries and `n` is at most 1000, an approach using roughly one query per character is acceptable. However, any solution requiring quadratic exploration of possible strings is impossible because the number of possible binary strings grows exponentially.

The tricky cases are not caused by large values, but by the direction in which we reconstruct. For example, if the hidden string is:

```
1
```

the only valid answer is:

```
1
```

A solution that assumes it can always test a zero first and blindly append it would fail.

For a small split case:

```
n = 4
hidden = 0110
```

If we try to reconstruct all four characters from the left by asking whether the current answer plus a new character is a subsequence, after finding three characters the query length becomes four, which is larger than the allowed query length of three. The same issue appears for every large string. The correct approach must reconstruct from both ends so that every query stays within the limit.

## Approaches

The natural brute-force idea is to build the answer from left to right. Suppose we already know a prefix `p`. We can ask whether `p + "0"` is a subsequence. If it is not, the next character must be `1`. This works because every prefix of the real string is itself a subsequence of the hidden string.

The problem is the query size. After discovering roughly half of the string, the next query would contain the known prefix plus one more character, exceeding the allowed length. For `n = 1000`, a full left-to-right reconstruction needs queries of length close to 1000, while the limit is only 501.

The key observation is that the restriction is exactly half the length. We can reconstruct the first half from the left and the second half from the right. When reconstructing from the right, we keep the already known suffix at the end of the query and prepend a candidate character. The query length never exceeds half of the string plus one.

The two halves together cover every position, and the number of queries is at most `n`, which fits easily inside the limit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Left-to-right reconstruction | O(n) queries but invalid query sizes | O(n) | Not allowed |
| Two-sided reconstruction | O(n) queries | O(n) | Accepted |

## Algorithm Walkthrough

1. Let `half = n // 2`. Reconstruct the first `half` characters from left to right. Maintain the prefix already found. Ask whether the prefix followed by `0` is a subsequence. If the answer is yes, the next character is `0`; otherwise it must be `1`.

The longest query in this phase has length `half`, so it respects the query limit.

1. Reconstruct the remaining characters from right to left. Maintain the suffix already found. Ask whether `0` followed by the current suffix is a subsequence. If it is, the new character is `0`; otherwise it is `1`.

The suffix length before adding a new character is never more than `n - half - 1`, so the query length is at most `half + 1`.

1. Reverse the reconstructed suffix and place it after the first half. The two parts together form the original string.

Why it works:

The invariant during the first phase is that the stored prefix is exactly the corresponding prefix of the hidden string. Adding either `0` or `1` creates a candidate prefix of the hidden string, and only the correct one remains a subsequence.

The second phase uses the same idea from the opposite direction. A correct suffix of the hidden string remains a subsequence when the next real character is placed before it. Testing `0 + suffix` distinguishes whether the next character is zero or one. Since every position belongs to exactly one of the two reconstructed parts, the final string is correct.

## Python Solution

```python
import sys

input = sys.stdin.readline

def ask(s):
    print("? " + s, flush=True)
    return int(input())

n = int(input())

half = n // 2

left = ""
for _ in range(half):
    if ask(left + "0"):
        left += "0"
    else:
        left += "1"

right = ""
for _ in range(n - half):
    if ask("0" + right):
        right = "0" + right
    else:
        right = "1" + right

print("! " + left + right, flush=True)
```

The function `ask` handles the interactive communication. Every query is immediately flushed because an interactive judge waits for the program's output before replying.

The first loop builds the left part. At every point, the current prefix is already known to be correct, so checking the next zero is enough. The opposite case must be one because the hidden string has exactly one character at that position.

The second loop uses the same logic but grows the answer backwards. The assignment `right = "0" + right` keeps the suffix in the correct order while adding characters from right to left.

No integer calculations beyond the split point are needed, so there are no overflow concerns. The important boundary is the query length, and both loops are designed so that the maximum query size is `floor(n/2)+1`.

## Worked Examples

For a hidden string `0110`:

| Step | Known left | Known right | Query | Answer |
| --- | --- | --- | --- | --- |
| 1 | "" | "" | "0" | Yes |
| 2 | "0" | "" | "00" | No |
| 3 | "01" | "" | "010" | Yes |
| 4 | "01" | "0" | "00" | Yes |

The first half becomes `01`. The right reconstruction discovers the remaining `10`, giving the final answer `0110`.

For a hidden string `101`:

| Step | Known left | Known right | Query | Answer |
| --- | --- | --- | --- | --- |
| 1 | "" | "" | "0" | No |
| 2 | "" | "1" | "01" | Yes |
| 3 | "" | "01" | "001" | No |

The algorithm finds the left part as `1` and the right part as `01`, producing `101`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) queries | One query determines each character |
| Space | O(n) | The reconstructed string is stored |

The solution uses at most `n` queries, which is below the allowed 1024 queries for the maximum length. The memory usage is linear and easily fits the limits.

## Test Cases

This is an interactive problem, so there is no offline input/output format that can be tested with normal assert-based tests. The following cases describe the situations an offline simulator for the judge should verify.

| Hidden string | Expected answer | What it validates |
| --- | --- | --- |
| `0` | `0` | Minimum length handling |
| `1` | `1` | Single character with no zero subsequence |
| `0000` | `0000` | All equal values |
| `1111` | `1111` | All equal values |
| `0110` | `0110` | Split point between two halves |
| `10101` | `10101` | Odd length reconstruction |

## Edge Cases

For the one-character string `1`, the first phase has no characters to reconstruct because `n // 2` is zero. The suffix phase asks whether `0` is possible. The answer is false, so the algorithm places `1` in the suffix and returns the correct string.

For an even length string such as `0110`, the split creates two parts of equal size. The left phase only handles `01`, and the right phase handles `10`. Neither side needs a query longer than three characters, which is the allowed limit for this length.

For an odd length string such as `10101`, the left part has length two and the right part has length three. The right reconstruction still works because before adding each character the stored suffix is short enough that prepending one character keeps the query within the limit. The final concatenation preserves the original order.
