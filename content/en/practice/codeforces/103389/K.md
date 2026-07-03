---
title: "CF 103389K - \u97f3\u4e50\u6e38\u620f"
description: "The task is essentially about processing a stream of text tokens and extracting a very specific character statistic from them. Instead of performing any structural parsing or transformation, we read all input strings and focus only on occurrences of the hyphen character -."
date: "2026-07-03T12:14:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103389
codeforces_index: "K"
codeforces_contest_name: "2021\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 103389
solve_time_s: 41
verified: true
draft: false
---

[CF 103389K - \u97f3\u4e50\u6e38\u620f](https://codeforces.com/problemset/problem/103389/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially about processing a stream of text tokens and extracting a very specific character statistic from them. Instead of performing any structural parsing or transformation, we read all input strings and focus only on occurrences of the hyphen character `-`. Every time this character appears in any token, it contributes one unit to the final answer.

You can think of the input as a sequence of whitespace-separated strings, possibly spanning multiple lines, and the output is a single integer representing how many hyphens appear across all of them combined. No grouping, no ordering, and no interpretation of the strings matters beyond character inspection.

Even though the official description is minimal, the implied constraints are standard for Codeforces string-processing tasks. The input size can easily reach hundreds of thousands or millions of characters in total. That immediately rules out any repeated rescanning or inefficient concatenation strategies. A solution must process the input in a single pass, inspecting each character exactly once.

A subtle edge case arises from how input is terminated and structured. Since reading is typically done via token-based input or full stream reading until EOF, implementations that assume a fixed number of strings or lines can fail silently when the input length varies. Another edge case is the absence of any hyphens at all, where the correct output is simply zero, and implementations must ensure they still produce output even if no matching characters are found.

## Approaches

The brute-force interpretation is straightforward. We read all strings into memory, then for each string, we iterate over every character and increment a counter whenever we encounter `-`. This is correct because it directly mirrors the definition of the task. The cost of this approach is proportional to the total number of characters across all strings. If we denote that total length as N, the runtime is O(N), which is already optimal in terms of asymptotic complexity.

There is no meaningful algorithmic optimization beyond this, because every character must be examined at least once to determine whether it is a hyphen. Any attempt to skip scanning or batch process characters would still implicitly touch each character, so the theoretical lower bound remains linear.

The only practical refinement is in how input is read. Using Python’s standard input methods efficiently ensures we do not incur overhead from repeated function calls or string concatenations. The optimal solution is therefore not about reducing complexity, but about implementing the linear scan in the most direct and efficient way possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan per string | O(N) | O(1) to O(N) | Accepted |
| Single-pass stream scan | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read input from standard input as a continuous stream of whitespace-separated tokens. This ensures we correctly handle any mixture of line breaks and spaces without making assumptions about formatting.
2. Initialize a counter to zero. This counter will accumulate the total number of hyphens encountered across all tokens.
3. Iterate over each token obtained from the input. Each token is treated independently, but processed identically.
4. For each token, iterate through every character and check whether it equals `-`. If it does, increment the counter by one. This direct character check avoids any unnecessary preprocessing or conversions.
5. After all tokens have been processed, output the final value of the counter.

The key idea is that the problem reduces entirely to character counting under streaming input, so correctness depends only on ensuring that no character is skipped and no character is double-counted.

### Why it works

The algorithm maintains a simple invariant: after processing k tokens, the counter equals the number of hyphens appearing in exactly those k tokens. Each token is fully scanned once, and every character is evaluated exactly once. Since the input is partitioned into disjoint tokens and all tokens are covered, the final counter necessarily equals the total number of hyphens in the entire input.

## Python Solution

```python
import sys
input = sys.stdin.readline

data = sys.stdin.read().split()

ans = 0
for token in data:
    for ch in token:
        if ch == '-':
            ans += 1

print(ans)
```

The solution reads the entire input at once using `sys.stdin.read()`, which avoids overhead from per-line reading. Splitting into tokens ensures that all whitespace-separated strings are handled uniformly.

The nested loop structure is intentional and minimal. The outer loop iterates over tokens, while the inner loop inspects each character. The condition `ch == '-'` is the only logic required, and the counter accumulates results without any auxiliary storage.

A common implementation mistake here is using repeated `input()` calls in a loop, which can be slower and risk missing EOF conditions. Another subtle issue is forgetting to process all characters in a token if one attempts to optimize by using string methods incorrectly. The presented solution avoids both pitfalls by sticking to direct iteration.

## Worked Examples

Consider an input where tokens are mixed across lines:

Input:

```
a-b c--d
e-f
```

We process token by token.

| Token | Characters processed | Hyphens found | Counter |
| --- | --- | --- | --- |
| a-b | a, -, b | 1 | 1 |
| c--d | c, -, -, d | 2 | 3 |
| e-f | e, -, f | 1 | 4 |

The final output is 4. This trace shows that line breaks do not matter, only token boundaries and characters inside them.

Now consider a case with no hyphens:

Input:

```
abc def ghi
```

| Token | Characters processed | Hyphens found | Counter |
| --- | --- | --- | --- |
| abc | a, b, c | 0 | 0 |
| def | d, e, f | 0 | 0 |
| ghi | g, h, i | 0 | 0 |

The final result is 0, confirming correct handling of empty matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Every character in every token is checked exactly once |
| Space | O(1) | Only a single counter is stored, input is streamed |

The algorithm fits easily within typical constraints for string problems. Even for inputs with millions of characters, a single linear scan in Python is sufficient under standard time limits, since each operation is a simple character comparison.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    ans = 0
    for token in data:
        for ch in token:
            if ch == '-':
                ans += 1
    return str(ans)

# constructed cases

# case 1: mixed hyphens
assert run("a-b c--d e-f") == "4", "mixed hyphens"

# case 2: no hyphens
assert run("abc def ghi") == "0", "no hyphens"

# case 3: all hyphens
assert run("--- --") == "5", "all hyphens"

# case 4: single character
assert run("-") == "1", "single hyphen"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a-b c--d e-f | 4 | mixed distribution across tokens |
| abc def ghi | 0 | absence of target character |
| --- -- | 5 | dense consecutive hyphens |
| - | 1 | minimal input case |

## Edge Cases

A key edge case is when the input contains no tokens at all. In that situation, `sys.stdin.read().split()` returns an empty list, and the loop never executes. The counter remains at its initialized value of zero, which is correct because there are no characters and therefore no hyphens.

Another case is extremely large contiguous strings without whitespace. Since the algorithm processes each character independently, it still performs correctly. For example, input like `a---b---c` is treated as a single token, and the scan counts all hyphens directly, producing the correct total.

A final edge case is irregular whitespace, such as multiple spaces or newlines between tokens. Because splitting collapses all whitespace uniformly, the grouping of tokens is irrelevant to the correctness of the count.
