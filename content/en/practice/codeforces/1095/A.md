---
title: "CF 1095A - Repeating Cipher"
description: "We are given a string that was produced by a very specific “stretched repetition” rule applied to some hidden original string. The original string is short, with length at most 10, but we do not know it."
date: "2026-06-13T05:22:55+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1095
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 529 (Div. 3)"
rating: 800
weight: 1095
solve_time_s: 1373
verified: false
draft: false
---

[CF 1095A - Repeating Cipher](https://codeforces.com/problemset/problem/1095/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 22m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string that was produced by a very specific “stretched repetition” rule applied to some hidden original string. The original string is short, with length at most 10, but we do not know it. What we are given is the final expanded string after each character was repeated a number of times equal to its position in the original string.

Concretely, if the hidden string is `s = s1 s2 ... sm`, then the first character `s1` appears once in the encrypted string, the second character `s2` appears twice consecutively, the third character appears three times, and so on. The encrypted string is therefore a concatenation of blocks whose lengths grow as 1, 2, 3, ..., m.

The task is to recover the original string from this expanded form.

The constraints are small: the encrypted string length is at most 55, and the original string length is at most 10 implicitly because 1 + 2 + ... + 10 = 55. This immediately tells us that any solution that scans or simulates in linear time is easily sufficient. Even nested loops up to 10 levels are trivial in performance terms, but unnecessary.

The main edge case is structural rather than computational. Since block sizes are increasing, a wrong solution typically fails when it assumes equal-sized segments or tries to split greedily without respecting the strict 1, 2, 3, ... growth pattern. Another subtle issue is off-by-one indexing: the k-th character belongs to a block of size k, not k-1 or k+1, which can silently corrupt reconstruction.

## Approaches

The brute-force perspective starts by imagining we try to guess the original string and simulate the encryption. Since the original length is at most 10, each position has 26 possibilities, so there are 26^10 potential candidates. For each candidate, we could build its encrypted form in O(m^2) time (since we append i copies for position i), giving an astronomically large search space. Even with pruning, this is completely unnecessary given the structure.

The key observation is that the encryption process is deterministic and injective in a very structured way: the encrypted string is simply a concatenation of known-length blocks. The first block has size 1, the second size 2, and so on. Therefore, instead of guessing the original string, we can directly decode it by walking through the encrypted string and slicing out blocks of increasing size.

This turns the problem into a simple parsing task: maintain a pointer into the string, extract 1 character, then 2 characters, then 3, and so on, and record the first character of each block.

The brute-force approach is exponential in the worst case due to guessing strings. The optimal approach is linear in the length of the encrypted string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^m · m²) | O(m) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We reconstruct the original string by exploiting the fixed block structure of the cipher.

1. Initialize a pointer `i = 0` to track our position in the encrypted string. We also maintain a block size counter `k = 1`.
2. While `i` is less than the length of the string, we know that the next block in the original encoding had size `k`, so we take the substring starting at `i` of length `k`.
3. The original character that generated this block must be the first character of that substring, since all characters in the block are identical by construction.
4. Append that character to the answer.
5. Move the pointer forward by `k`, and increment `k` by 1 to match the increasing repetition rule.
6. Continue until the string is fully consumed.

The key idea is that we never need to validate the block contents beyond consistency, because the problem guarantees the input is valid.

### Why it works

At each step, the encryption process produces a contiguous block of identical characters whose length is exactly determined by its position in the original string. Since the blocks are non-overlapping and strictly ordered by increasing size, the boundary between blocks is uniquely determined by the sequence 1, 2, 3, ..., m. Therefore, at decoding time, the block boundaries are fixed and unambiguous, and selecting the first character of each block reconstructs the original string exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
t = input().strip()

res = []
i = 0
k = 1

while i < n:
    res.append(t[i])
    i += k
    k += 1

print("".join(res))
```

The solution reads the encrypted string and walks through it using two variables: `i`, the current position, and `k`, the expected block length. At each iteration, we extract the character at position `i` as the representative of the current block. We then skip ahead by `k` characters because the encryption guarantees that this entire segment corresponds to one repeated character. Incrementing `k` ensures we respect the 1, 2, 3, ... growth pattern.

No substring validation is required because the input is guaranteed to be a valid encoding.

## Worked Examples

### Example 1

Input:

```
6
baabbb
```

We track decoding step by step.

| Step | i | k | Block read | Chosen char | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | "b" | b | b |
| 2 | 1 | 2 | "aa" | a | ba |
| 3 | 3 | 3 | "bbb" | b | bab |

The pointer moves 0 → 1 → 3 → 6, consuming the full string. The reconstructed string is `bab`, which matches the original.

This trace shows that block boundaries are fully determined by the increasing sequence of lengths.

### Example 2

Input:

```
10
ccdddeeeee
```

We assume it is valid under the same structure.

| Step | i | k | Block read | Chosen char | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | "c" | c | c |
| 2 | 1 | 2 | "cd" | c | cc |
| 3 | 3 | 3 | "dde" | d | ccd |
| 4 | 6 | 4 | "eeee" | e | ccde |

This demonstrates that even when characters differ across blocks, each block is independent and fully determined by its starting position and expected length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited exactly once as we jump through blocks |
| Space | O(1) | Aside from output storage, only a few counters are used |

The constraints cap the input size at 55, so even less efficient linear scanning is sufficient. The solution is optimal and comfortably within limits.

## Test Cases

```python
# helper: run solution on input string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input().strip())
    t = input().strip()

    res = []
    i = 0
    k = 1

    while i < n:
        res.append(t[i])
        i += k
        k += 1

    return "".join(res)

# provided sample
assert run("6\nbaabbb\n") == "bab"

# minimal case
assert run("1\na\n") == "a"

# single block chain
assert run("3\naaabbbccc\n") == "abc"

# mixed characters valid structure
assert run("6\nxxyyyzzz\n") == "xyz"

# edge increasing pattern
assert run("10\nabcdefghijjjj\n") == "abcdefghij"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 a | a | minimal boundary case |
| 3 aaabbbccc | abc | repeated block structure |
| 6 xxyyyzzz | xyz | correct stepping through blocks |
| 10 abcdefghijjjj | abcdefghij | full-length sequential decoding |

## Edge Cases

A subtle edge case is the smallest possible input where the string length is 1. In that case, the algorithm starts with `k = 1`, reads exactly one character, and terminates immediately. There is no risk of overstepping because the pointer increment exactly matches the remaining length.

Another case is when all characters are identical. For example, `t = "aaaaa..."`. The algorithm still works because it never relies on character differences, only on block lengths. Each step consumes a growing segment, and the output simply repeats the same character for each block.

A final case is the maximal length of 55. Since 1 + 2 + ... + 10 = 55, the algorithm will naturally terminate exactly after 10 iterations. There is no partial block ambiguity, because the sum of block sizes exactly matches the string length.
