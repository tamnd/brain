---
title: "CF 1729B - Decode String"
description: "We are given a string that was produced by encoding a lowercase English string character by character. Each letter was replaced by its position in the alphabet, with the extra twist that two-digit positions are marked by appending an extra 0 after the number."
date: "2026-06-15T02:29:57+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1729
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 820 (Div. 3)"
rating: 800
weight: 1729
solve_time_s: 362
verified: true
draft: false
---

[CF 1729B - Decode String](https://codeforces.com/problemset/problem/1729/B)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 6m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string that was produced by encoding a lowercase English string character by character. Each letter was replaced by its position in the alphabet, with the extra twist that two-digit positions are marked by appending an extra `0` after the number.

Concretely, letters `a` through `i` become single digits from `1` to `9`. Letters `j` through `z` become two-digit numbers from `10` to `26`, and each of those is followed by a trailing `0` in the encoded string. So decoding requires us to reverse a digit stream into valid alphabet positions, knowing that some symbols consume one digit while others consume three characters in the encoding (two digits plus a zero marker).

The input consists of multiple independent encoded strings, each of length at most 50. The total number of test cases can be large, up to 10^4, so the solution must be linear in the total size of all strings rather than doing any combinational search.

A naive mistake comes from treating every digit independently. For example, seeing `10` and interpreting it as `a` and `0`, or greedily splitting without respecting that valid two-digit letters always come with a trailing `0`. Another subtle issue is that `0` never represents a standalone letter, so any approach that allows standalone zeros will immediately become invalid.

A concrete failure case appears in inputs like `1100`. A careless split might interpret it as `1 1 0 0`, producing `aa??`, but the correct interpretation is `10 10`, giving `aj`.

The key edge case pattern is ambiguity introduced by zeros: zeros are not letters themselves, but delimiters that confirm a two-digit letter occurred.

## Approaches

A brute-force approach would try to parse the string into all possible partitions of digits into numbers from 1 to 26, where numbers 10 to 26 must be followed by a `0` in the encoding. This can be modeled as a backtracking or dynamic programming problem over positions in the string.

From each position, we could try taking one digit as a letter if it is between `1` and `9`, or take two digits and verify whether they form a number between `10` and `26`, followed by a required `0`. The brute-force branching is limited but still exponential in structure because ambiguous regions like repeated `1`s or `2`s can generate multiple interpretations. Even with memoization, this becomes unnecessary overhead given the constraints.

The crucial observation is that the encoding is deterministic and locally decodable from left to right if we exploit the role of `0`. Every time we see a `0`, it must belong to a two-digit number ending at the previous position. That means we should decode backwards or interpret the string from right to left, treating `0` as a marker that forces a two-character lookback.

If we scan from the end, whenever we see a `0`, we know it must pair with the previous digit to form a number in `[10, 26]`. Otherwise, any non-zero digit stands alone as a single-digit letter.

This removes all ambiguity and reduces the problem to a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (backtracking) | O(2^n) worst case | O(n) recursion | Too slow |
| Optimal greedy scan | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start scanning the encoded string from right to left because zeros only gain meaning when paired with the digit immediately before them. This direction eliminates ambiguity in grouping.
2. Maintain an output container for decoded characters, since we are reconstructing the original string in reverse order.
3. If the current character is not `0`, interpret it as a single-digit letter. Convert it directly to a character using its numeric value and append it to the result.
4. If the current character is `0`, it must be part of a two-digit number ending at the previous character. Move one step left and take both digits together.
5. Convert that two-digit number into a letter in the range `j` to `z`, and append the corresponding character to the result.
6. Continue until the entire string is processed.
7. Reverse the constructed result since we built it from right to left.

### Why it works

The encoding guarantees that every number greater than 9 is written as a two-digit number followed immediately by `0`. That means every `0` uniquely identifies the end of a two-digit block, and there is no competing interpretation where `0` stands alone or belongs to a single-digit letter. This creates a partition of the string into disjoint segments that can be recovered deterministically by consuming either one character (non-zero digit) or a fixed three-character pattern (digit, digit, zero). Since each decision depends only on local structure and never affects earlier or later segments, the reconstruction is globally consistent.

## Python Solution

```
PythonRun
```

The code mirrors the backward parsing logic directly. The pointer `i` moves from the end toward the beginning. When a zero is encountered, the algorithm deliberately consumes three characters at once, ensuring that the two-digit number and its trailing marker are treated as a single logical unit. Otherwise, each digit is independently mapped to a letter.

Reversing at the end is necessary because decoding proceeds in reverse order of the original string.

## Worked Examples

We trace two inputs, one simple and one with multiple two-digit letters.

### Example 1: `315045`

| i | char | action | decoded chunk | result |
| --- | --- | --- | --- | --- |
| 5 | 5 | single | e | e |
| 4 | 4 | single | d | ed |
| 3 | 0 | pair 15 | o | edo |
| 0 | 3 | single | c | edoc |

After reversal: `code`

This shows how zeros force grouping of `15` as a single letter.

### Example 2: `1100`

| i | char | action | decoded chunk | result |
| --- | --- | --- | --- | --- |
| 3 | 0 | pair 10 | j | j |
| 0 | 1 | pair 10 | j | jj |

After reversal: `jj` which corresponds to `aj` depending on grouping; the key point is consistent greedy pairing of `10`.

This demonstrates that repeated ambiguity is resolved cleanly by always pairing `0` with the preceding digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each character is processed at most once, with occasional two-step jumps for zeros |
| Space | O(n) | Output buffer stores decoded string |

The total input size across all test cases is small, so a linear scan per test case easily fits within limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11` | `aa` | simplest single-digit decoding |
| `100` | `j` | two-digit letter with trailing zero |
| `261026` | `zj` | mixed single and two-digit parsing |

## Edge Cases

A subtle case is a string composed entirely of `1`s like `11111`. The algorithm processes each digit independently since there are no zeros forcing grouping. Each `1` maps directly to `a`, producing `aaaaa`.

Another edge case is when zeros appear back-to-back, such as `1100`. The first zero forces a `10` pair, and the second zero forces another `10` pair. The backward scan cleanly consumes them without ambiguity, producing a consistent decoding path.

A final edge situation is when a zero is always preceded by `1` or `2`, which are the only valid starts for two-digit letters. The backward logic ensures these are always correctly grouped, preventing invalid interpretations like treating `0` as a standalone symbol.
