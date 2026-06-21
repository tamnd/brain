---
title: "CF 105575C - \u732b\u5a18\u9b54\u6cd5"
description: "We are given a single string that encodes a sequence of fixed-size tokens. Each meaningful token is exactly 5 characters long, and the string should be viewed as a concatenation of such 5-character blocks."
date: "2026-06-22T06:21:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105575
codeforces_index: "C"
codeforces_contest_name: "Southeast University 6th Programming Competition Competition (Winter, Novice Group) \u4e1c\u5357\u5927\u5b66\u7b2c\u516d\u5c4a\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u51ac\u5b63\u8d5b\uff08\u65b0\u624b\u7ec4\uff09"
rating: 0
weight: 105575
solve_time_s: 45
verified: true
draft: false
---

[CF 105575C - \u732b\u5a18\u9b54\u6cd5](https://codeforces.com/problemset/problem/105575/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string that encodes a sequence of fixed-size tokens. Each meaningful token is exactly 5 characters long, and the string should be viewed as a concatenation of such 5-character blocks.

Our task is to scan these blocks from left to right and find the first block that exactly matches the pattern `"moew~"`. Once that block is found, we output its position in the block sequence, using 1-based indexing.

So instead of thinking about individual characters, it is more natural to think of the string as being split into chunks of size 5. We are searching for the first chunk equal to a specific target string, and reporting its ordinal position.

The constraints implied by this structure are small enough that a linear scan over blocks is sufficient. Each step examines exactly 5 characters, so even if the string is large, the total work remains proportional to its length.

A subtle failure case appears if someone scans character by character instead of jumping in steps of 5. For example, if the string is `"xxxxxmoew~yyyyy"` and we check every substring of length 5 starting at every index, we may still be correct but we waste effort and risk accidental misalignment assumptions. The correct interpretation requires enforcing alignment to multiples of 5 from the start.

Another edge case is assuming the match always starts at index 0. If the correct block is later, a naive single-check solution would immediately return wrong results.

## Approaches

A direct brute-force interpretation is to check every possible starting position `i` in the string and compare `s[i:i+5]` with `"moew~"`. This is correct because it examines every candidate substring of the right length. However, it is inefficient in structure because it checks overlapping windows that are not valid block boundaries.

In the worst case, this performs about `O(n)` substring comparisons, and each substring comparison costs `O(5)`, so overall it is still linear, but it ignores the stronger structure: valid candidates only occur at indices divisible by 5.

The key observation is that the string is conceptually partitioned into non-overlapping chunks of length 5. Once we accept this, we no longer need to consider every index. We only need to inspect positions `0, 5, 10, 15, ...`, which reduces the problem to a simple block scan. This removes redundancy and makes the intent of the problem match the implementation exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all substrings) | O(n) | O(1) | Accepted |
| Block Scan (step by 5) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the input string as a sequence of fixed-length tokens and iterate over them directly.

1. Start from the first character of the string. This position represents the first 5-character block.
2. Extract the substring of length 5 starting at the current index.
3. Compare this substring with `"moew~"`. If it matches, compute the block number as `i // 5 + 1` and stop.
4. If it does not match, move to the next block by increasing the index by 5.
5. Repeat until a match is found.

The reason we jump by 5 each time is that any valid token boundary must align with multiples of 5. Checking intermediate positions would only produce misaligned substrings that are not meaningful under the problem’s construction.

### Why it works

The correctness comes from the invariant that at every iteration, the index `i` is exactly at the start of a block. Since all valid comparisons must occur at block boundaries, the algorithm never skips a valid candidate. At the same time, it never evaluates invalid offsets, so every checked substring corresponds exactly to one logical token in the input sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    target = "moew~"
    
    i = 0
    while i < len(s):
        if s[i:i+5] == target:
            print(i // 5 + 1)
            return
        i += 5

if __name__ == "__main__":
    solve()
```

The solution reads the input string and iterates in fixed steps of 5. At each step it extracts exactly one token and compares it to the target pattern. Once a match is found, it converts the character index into a block index using integer division.

A common mistake is iterating character by character or using a loop like `for i in range(len(s) - 4)`, which works but loses the structural constraint that only aligned positions matter. The step size of 5 encodes the problem’s intended structure directly.

## Worked Examples

Consider the input:

```
aaaaamoew~xxxxx
```

| i | s[i:i+5] | Match | Block |
| --- | --- | --- | --- |
| 0 | aaaaa | No | - |
| 5 | moew~ | Yes | 2 |

At `i = 5`, we find the match and output `5 // 5 + 1 = 2`.

This shows that the algorithm correctly ignores misaligned substrings and only evaluates valid block positions.

Now consider:

```
moew~abcde
```

| i | s[i:i+5] | Match | Block |
| --- | --- | --- | --- |
| 0 | moew~ | Yes | 1 |

The match occurs immediately at the first block, confirming correct handling of the minimal case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is part of exactly one 5-length check |
| Space | O(1) | Only a few variables are used besides input storage |

The algorithm runs comfortably within limits because each iteration advances by 5 characters, meaning the total number of iterations is `n / 5`. This is linear and efficient even for very large strings.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from contextlib import redirect_stdout
    import io as sio
    
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    s = input().strip()
    target = "moew~"
    i = 0
    while i < len(s):
        if s[i:i+5] == target:
            print(i // 5 + 1)
            return
        i += 5

assert run("moew~") == "1"
assert run("aaaaamoew~xxxxx") == "2"
assert run("xxxxxmoew~") == "2"
assert run("moew~abcde") == "1"
assert run("aaaaabbbbbmoew~") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| moew~ | 1 | minimal input |
| aaaaamoew~xxxxx | 2 | match in middle |
| xxxxxmoew~ | 2 | alignment after offset |
| moew~abcde | 1 | immediate match |
| aaaaabbbbbmoew~ | 3 | deeper position |

## Edge Cases

One important edge case is when the target appears at the very beginning. In this case, `i = 0`, and the algorithm immediately succeeds without any iteration issues. The substring `s[0:5]` matches `"moew~"`, so the output is `1`, which is correct.

Another case is when the match appears at the last possible block. The loop continues stepping by 5 until the final valid index. Since every step preserves alignment, the last block is still checked correctly and no out-of-bounds access occurs because slicing in Python safely truncates.

A third case is when the string length is exactly 5. The algorithm performs one check at `i = 0` and terminates immediately, correctly handling the smallest valid input size without requiring special handling.
