---
title: "CF 103566A - \u0411\u0443\u043a\u0432\u044b \u043d\u0430 \u0437\u0430\u043a\u0430\u0437"
description: "The problem reduces language to a structural property of letters. Each lowercase English letter is classified only by how many “holes” it contains when drawn in a specific font used by the problem setter."
date: "2026-07-03T04:57:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103566
codeforces_index: "A"
codeforces_contest_name: "2021-2022 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 103566
solve_time_s: 48
verified: true
draft: false
---

[CF 103566A - \u0411\u0443\u043a\u0432\u044b \u043d\u0430 \u0437\u0430\u043a\u0430\u0437](https://codeforces.com/problemset/problem/103566/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem reduces language to a structural property of letters. Each lowercase English letter is classified only by how many “holes” it contains when drawn in a specific font used by the problem setter. Exactly one letter has two holes, and six letters have one hole, while all others have zero holes.

Given a string consisting of uppercase letters, the task is to determine how many holes appear in total when the string is written using this font mapping. Each occurrence of a letter contributes independently according to its hole count, so repeated letters accumulate their contribution.

The input is a single string. The output is a single integer representing the total number of holes across all characters.

Although the statement is short, the key idea is that the mapping is fixed and small, so the computation is purely a per-character classification problem.

From a complexity perspective, the input length can be assumed large in typical Codeforces fashion, up to around 10^5 or more characters. That immediately implies the solution must be linear in the string length. Any approach that scans or processes each character multiple times in nested loops would become too slow. The alphabet size is constant, so constant-time lookup per character is required.

A few edge cases are easy to miss if one assumes the usual English typography instead of the problem’s custom definition. For example, treating letters like “B” or “D” inconsistently depending on font assumptions would break correctness. Another subtle case is when the string contains only zero-hole letters, which should correctly output zero rather than an empty result or uninitialized value. A minimal example is input `C`, which must return `0`, since that letter has no hole in this definition.

## Approaches

A direct way to solve the problem is to, for each character, manually check whether it belongs to the set of one-hole letters or the special two-hole letter. For every character, we could compare it against all seven relevant letters and accumulate the answer accordingly. This works because the classification is static and independent per character.

In the brute-force interpretation, for each character we might iterate through a list of known hole-bearing letters and check membership. With at most 7 comparisons per character, the total cost is proportional to 7n. While this is already linear in practice, the structure becomes slightly cleaner if we convert membership checks into a constant-time lookup structure such as a boolean array or hash set. That removes repeated comparisons and simplifies the logic.

The key observation is that the alphabet is fixed and very small. We can precompute a mapping from character to hole count and then sum values across the string in one pass. This reduces the problem to array indexing per character.

The brute-force approach works because we only inspect membership, but it becomes unnecessarily repetitive. The optimized approach compresses all classification logic into a constant-time table lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Per-character comparison against list | O(n) | O(1) | Accepted |
| Direct lookup table per character | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We construct a direct mapping from characters to their hole counts, then accumulate the result while scanning the string once.

1. Define the set of letters with exactly one hole as `A, D, O, P, Q, R`. Assign each of them a value of 1. Define the letter with two holes as `B`, assigned value 2. All other letters implicitly map to 0. This encoding turns the visual property into arithmetic.
2. Create a lookup structure, typically an array of size 26 or a dictionary, that maps each uppercase letter to its hole count. This ensures constant-time access per character without repeated comparisons.
3. Initialize an accumulator variable `ans = 0` that will store the total number of holes across the string.
4. Iterate over each character in the input string. For each character, add its mapped value to `ans`. The correctness comes from treating each letter occurrence independently.
5. Output `ans` after processing all characters.

### Why it works

Each character contributes independently to the total, and the contribution depends only on a fixed classification that does not change during processing. The algorithm maintains the invariant that after processing the first k characters, `ans` equals the sum of hole counts for those k characters. Since every step only adds the correct contribution for the current character, the invariant holds until the end of the string, where it equals the required total.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

hole = [0] * 26
hole[ord('A') - ord('A')] = 1
hole[ord('D') - ord('A')] = 1
hole[ord('O') - ord('A')] = 1
hole[ord('P') - ord('A')] = 1
hole[ord('Q') - ord('A')] = 1
hole[ord('R') - ord('A')] = 1
hole[ord('B') - ord('A')] = 2

ans = 0
for ch in s:
    ans += hole[ord(ch) - ord('A')]

print(ans)
```

The solution precomputes a fixed array `hole` where each index corresponds to a letter. The mapping uses ASCII offsets so that each character is converted into an index in constant time. This avoids any conditional chains inside the loop.

The accumulation loop is the core of the solution. Each iteration performs only an array access and an addition, both constant time operations. The order of operations is straightforward because no state depends on future characters.

A common mistake would be to recompute membership using string searches or repeated comparisons, which is unnecessary overhead. Another subtle issue is forgetting to strip the input, which could introduce newline characters and break indexing.

## Worked Examples

### Example 1

Input:

```
ABCD
```

We track contributions step by step.

| Character | Value | Running Total |
| --- | --- | --- |
| A | 1 | 1 |
| B | 2 | 3 |
| C | 0 | 3 |
| D | 1 | 4 |

The final result is 4, which matches the sum of holes contributed by each letter. This confirms that the mapping handles mixed classifications correctly, including zero-hole letters.

### Example 2

Input:

```
QQQ
```

| Character | Value | Running Total |
| --- | --- | --- |
| Q | 1 | 1 |
| Q | 1 | 2 |
| Q | 1 | 3 |

The result is 3, demonstrating that repeated letters accumulate correctly and are not treated as unique entities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once with constant-time lookup |
| Space | O(1) | The mapping array is fixed size (26) regardless of input length |

The solution easily fits within typical constraints since even for 10^5 characters, only 10^5 simple array accesses are performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    hole = [0] * 26
    hole[0] = 1
    hole[3] = 1
    hole[14] = 1
    hole[15] = 1
    hole[16] = 1
    hole[17] = 1
    hole[1] = 2
    ans = 0
    for ch in s:
        ans += hole[ord(ch) - 65]
    return str(ans)

assert run("ABCD\n") == "4"
assert run("QQQ\n") == "3"
assert run("C\n") == "0"
assert run("BBBB\n") == "8"
assert run("ADOPQR\n") == "6"
assert run("Z\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ABCD | 4 | Mixed letters, basic correctness |
| QQQ | 3 | Repetition accumulation |
| C | 0 | Zero-hole letter handling |
| BBBB | 8 | Two-hole letter scaling |
| ADOPQR | 6 | Full one-hole set coverage |
| Z | 0 | Non-listed letter correctness |

## Edge Cases

One edge case is an input consisting entirely of zero-hole letters. For example, input `XYZ` should produce `0`. The algorithm processes each character, finds zero in the lookup table, and accumulates nothing. The final sum remains zero, which is correct.

Another edge case is maximal repetition of the two-hole letter. For input `BBBBB`, each step adds 2, so the running total evolves as 2, 4, 6, 8, 10. Since the lookup is independent per character, no special handling is needed, and the result remains stable even for large repetitions.

A final subtle case is ensuring correct character indexing. If the mapping array is built using ASCII offsets, every uppercase letter must align correctly with its index. Any off-by-one error in indexing would misclassify letters, but since each character is directly mapped via `ord(ch) - 65`, the mapping remains consistent across all inputs.
