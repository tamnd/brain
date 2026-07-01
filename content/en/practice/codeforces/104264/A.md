---
title: "CF 104264A - Vowels"
description: "We are given a single string consisting only of lowercase English letters. The task is to compute a single integer based on this string, and print it. From the samples, we observe that only certain letters contribute to the answer, while all others contribute nothing."
date: "2026-07-01T21:31:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104264
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #9 (Fool-Forces)"
rating: 0
weight: 104264
solve_time_s: 66
verified: true
draft: false
---

[CF 104264A - Vowels](https://codeforces.com/problemset/problem/104264/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string consisting only of lowercase English letters. The task is to compute a single integer based on this string, and print it. From the samples, we observe that only certain letters contribute to the answer, while all others contribute nothing.

The samples make the rule clear. In `"abue"` the output is `3`, in `"amir"` it is `2`, and in `"qwsdr"` it is `0`. The only consistent interpretation is that we are counting how many vowels appear in the string, where vowels are the letters `a`, `e`, `i`, `o`, and `u`.

The string length is at most 100. This is small enough that even a direct scan of every character with a simple condition is sufficient. The upper bound means the total number of operations per test case is at most 100 comparisons, which is negligible under a 1 second limit. Any linear solution is trivially safe.

There are no hidden structural constraints like ordering or grouping. The only meaningful edge case is when the string contains no vowels at all, in which case the answer is zero. Another edge case is when the string consists entirely of vowels, in which case the answer equals the string length. Single-character inputs also behave naturally under the same rule.

## Approaches

A brute-force way to solve this problem is to consider each character and decide whether it is a vowel by checking it against all vowel letters. For every character, we compare it with `a`, `e`, `i`, `o`, and `u`. If any match occurs, we increment a counter.

This works correctly because it directly implements the definition of the task: count vowel characters. The cost is bounded by 5 comparisons per character, so for a string of length n the complexity is O(5n), which simplifies to O(n). With n ≤ 100, this is extremely fast.

There is no real need for further optimization beyond recognizing that membership testing can be simplified using a set for clarity, but even that is optional. The structure of the problem is purely linear scanning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct checks) | O(n) | O(1) | Accepted |
| Optimal (set membership / direct check) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string. We need the entire string because each character contributes independently to the result.
2. Initialize a counter to zero. This variable accumulates the number of vowels encountered so far.
3. Define the vowel set `{a, e, i, o, u}`. This allows constant-time membership checks for each character.
4. Iterate over each character in the string. Each character is evaluated independently because the contribution of one letter does not depend on others.
5. If the current character belongs to the vowel set, increment the counter. Otherwise, do nothing and continue. This conditional is the core of the problem definition.
6. After processing all characters, output the final value of the counter.

### Why it works

Each character in the string is classified into exactly one of two categories: vowel or non-vowel. The algorithm increments the counter exactly once for every vowel and never increments it for non-vowels. Since every character is processed exactly once and contributes independently, the final count equals the total number of vowels in the string. No reordering or interaction between characters affects the result, so a single linear pass is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

vowels = set("aeiou")

cnt = 0
for ch in s:
    if ch in vowels:
        cnt += 1

print(cnt)
```

The solution reads the input string and removes trailing whitespace using `strip`. The vowel set is stored in a Python `set` so membership checks run in average O(1) time.

The loop processes each character exactly once. For each character, we perform a membership test against the vowel set. If it succeeds, the counter is incremented. The final result is printed directly.

A common implementation mistake would be forgetting to strip the newline character from input, which is harmless here but can lead to confusion in other problems. Another potential mistake is using a list instead of a set for membership checks, which would still work but makes the intent less clear.

## Worked Examples

### Example 1: `"abue"`

We track the counter as we scan the string.

| Character | Is vowel | Counter |
| --- | --- | --- |
| a | yes | 1 |
| b | no | 1 |
| u | yes | 2 |
| e | yes | 3 |

Final output is 3.

This confirms that multiple vowels scattered through the string are counted independently and accumulated correctly.

### Example 2: `"amir"`

| Character | Is vowel | Counter |
| --- | --- | --- |
| a | yes | 1 |
| m | no | 1 |
| i | yes | 2 |
| r | no | 2 |

Final output is 2.

This shows that non-vowel characters do not affect the count and are safely ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is checked once against a constant-size vowel set |
| Space | O(1) | Only a fixed set of vowels and a counter are stored |

The input size is at most 100, so a linear scan is far below any computational limits. Memory usage is constant and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    s = input().strip()
    vowels = set("aeiou")
    cnt = 0
    for ch in s:
        if ch in vowels:
            cnt += 1
    return str(cnt)

# provided samples
assert run("abue\n") == "3", "sample 1"
assert run("amir\n") == "2", "sample 2"
assert run("qwsdr\n") == "0", "sample 3"

# custom cases
assert run("a\n") == "1", "single vowel"
assert run("bcd\n") == "0", "no vowels"
assert run("aeiou\n") == "5", "all vowels"
assert run("abcdeiouxyz\n") == "6", "mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | 1 | minimum size input |
| `"bcd"` | 0 | no vowels case |
| `"aeiou"` | 5 | all vowels case |
| `"abcdeiouxyz"` | 6 | mixed distribution correctness |

## Edge Cases

A single-character string like `"a"` is handled naturally. The loop runs once, the vowel check succeeds, and the counter becomes 1. There is no special-case logic needed.

A string with no vowels such as `"bcd"` results in no increments during iteration. Each character is checked, fails the membership test, and the counter remains zero throughout, producing the correct output.

A fully vowel string like `"aeiou"` increments the counter at every step. Each iteration hits the membership condition, so the final count equals the length of the string. This confirms that the algorithm correctly accumulates repeated positive matches without interference.
