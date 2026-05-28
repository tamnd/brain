---
title: "CF 172A - Phone Code"
description: "We are given a list of phone numbers from friends in a city. Each phone number is a string of digits, and all numbers have the same length. The task is to find the city phone code, which Polycarpus defines as the longest common prefix shared by all these numbers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 172
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2012 - Qualification Round"
rating: 800
weight: 172
solve_time_s: 180
verified: true
draft: false
---

[CF 172A - Phone Code](https://codeforces.com/problemset/problem/172/A)

**Rating:** 800  
**Tags:** *special, brute force, implementation  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of phone numbers from friends in a city. Each phone number is a string of digits, and all numbers have the same length. The task is to find the city phone code, which Polycarpus defines as the longest common prefix shared by all these numbers. In other words, the city code is the sequence of digits at the start of every number before the first mismatch occurs. The output is the length of this prefix, not the prefix itself.

The constraints tell us there can be up to 30,000 numbers, each up to 20 digits long. This means any solution that compares every number character by character is feasible because the total comparisons are at most 30,000 times 20, which is 600,000 operations-comfortably within a 2-second limit. The guarantees that all numbers are the same length and distinct remove ambiguity, but we need to handle the possibility that the numbers share no common prefix at all. For example, if the numbers are `123` and `987`, the correct output is 0. A naive approach that assumes the first character always matches could silently produce the wrong answer.

Another edge case is when all numbers are identical except the last character. For example, `5550`, `5551`, `5552`. The longest common prefix is `555`, of length 3. A careless implementation might overcount or undercount if it doesn't correctly check character equality across all numbers.

## Approaches

The most straightforward approach is brute force. Take the first number as a reference, then iterate over each character index and compare that character with the corresponding character in all other numbers. Stop at the first mismatch. This approach works because we only compare characters until a mismatch is found. In the worst case, every character of every number matches, so we perform `n * length` comparisons, which is manageable given the constraints.

A slightly more structured way is to use a pairwise reduction. Start with the first number as the current prefix, and then iteratively shorten it by comparing it with each subsequent number until it matches the beginning of that number. This technique avoids repeatedly checking characters we already know differ at earlier positions, though for these small lengths the performance gain is minimal.

The key insight is that since the strings are short (up to 20 digits), we can safely compare character by character across all numbers without worrying about efficiency. The structure of the problem - fixed-length strings, guaranteed digit content, and small maximum length - makes the brute force approach essentially optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (compare each character across all strings) | O(n * m), m = string length | O(1) | Accepted |
| Iterative prefix reduction | O(n * m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of friends `n` and the list of phone numbers. All numbers have equal length `m`.
2. Take the first phone number as the initial reference prefix.
3. Initialize a variable `prefix_length` to the total length `m`. This represents the maximum possible prefix.
4. Iterate over the remaining phone numbers.
5. For each number, iterate character by character from the beginning up to the current `prefix_length`.
6. Compare characters at the same position with the reference number. If a mismatch occurs, reduce `prefix_length` to the index of the mismatch and break out of the inner loop.
7. Continue to the next number, further reducing `prefix_length` if necessary.
8. After processing all numbers, `prefix_length` holds the length of the longest common prefix. Print it.

The invariant is that after processing each number, `prefix_length` always reflects the longest prefix shared by all numbers processed so far. No character beyond `prefix_length` can be part of a valid common prefix, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
numbers = [input().strip() for _ in range(n)]

prefix_length = len(numbers[0])

for num in numbers[1:]:
    for i in range(prefix_length):
        if num[i] != numbers[0][i]:
            prefix_length = i
            break

print(prefix_length)
```

We first read all input numbers and strip newline characters. We assume the first number has the maximal possible prefix. For each subsequent number, we only check up to `prefix_length` because any character beyond it cannot be part of the common prefix. The loop breaks immediately on a mismatch, preventing unnecessary comparisons. Finally, we print the length of the prefix, which is exactly what the problem asks.

## Worked Examples

### Sample Input 1

```
4
00209
00219
00999
00909
```

| num | i | numbers[0][i] | num[i] | prefix_length update |
| --- | --- | --- | --- | --- |
| 00219 | 0 | 0 | 0 | 5 |
| 00219 | 1 | 0 | 0 | 5 |
| 00219 | 2 | 2 | 2 | 5 |
| 00219 | 3 | 0 | 1 | 3 |
| 00999 | 0 | 0 | 0 | 3 |
| 00999 | 1 | 0 | 0 | 3 |
| 00999 | 2 | 2 | 9 | 2 |
| 00909 | 0 | 0 | 0 | 2 |
| 00909 | 1 | 0 | 0 | 2 |

After all numbers, `prefix_length` = 2, matching the expected output.

### Sample Input 2

```
2
123
987
```

| num | i | numbers[0][i] | num[i] | prefix_length update |
| --- | --- | --- | --- | --- |
| 987 | 0 | 1 | 9 | 0 |

No characters match, so `prefix_length` = 0.

These traces confirm that the algorithm stops correctly at the first mismatch and maintains the correct prefix length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m) | We compare each character of each number up to the current prefix length; n is up to 30,000, m up to 20, giving at most 600,000 comparisons. |
| Space | O(n * m) | We store all input strings. No additional significant space is used. |

The total operations are well under the 2-second time limit and the memory usage fits within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    numbers = [input().strip() for _ in range(n)]
    prefix_length = len(numbers[0])
    for num in numbers[1:]:
        for i in range(prefix_length):
            if num[i] != numbers[0][i]:
                prefix_length = i
                break
    return str(prefix_length)

# Provided samples
assert run("4\n00209\n00219\n00999\n00909\n") == "2", "sample 1"
assert run("2\n123\n987\n") == "0", "sample 2"

# Custom cases
assert run("3\n5550\n5551\n5552\n") == "3", "common prefix just before last digit"
assert run("2\n1\n1\n") == "1", "single-digit identical numbers"
assert run("3\n12345678901234567890\n12345678901234567891\n12345678901234567892\n") == "19", "max length numbers differing at last digit"
assert run("2\n99999\n99999\n") == "5", "all numbers identical"
assert run("2\n0000\n1111\n") == "0", "no common prefix at all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5550, 5551, 5552 | 3 | Handles mismatch at last digit correctly |
| 1, 1 | 1 | Single-digit edge case |
| long numbers differing at last digit | 19 | Max-length input boundary handling |
| identical numbers | 5 | Entire string matches |
| 0000, 1111 | 0 | No common prefix |

## Edge Cases

If all numbers are identical except the last character, the algorithm correctly stops comparison at the first mismatch for each number. For example, `5550`, `5551`, `5552` results in `prefix_length` = 3. For completely non-overlapping numbers like `123` and `987`, the algorithm detects the mismatch immediately at the first character and sets `prefix_length` = 0. For single-digit numbers, the algorithm handles both matching and non-matching scenarios naturally, returning either 1 or 0. All edge cases are correctly handled by the character-by-character comparison loop with early break on mismatch.
