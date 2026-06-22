---
title: "CF 105586A - \u6f14\u594f\u6625\u65e5\u5f71"
description: "We are given a short playlist of songs represented as strings. Each string is a single program item in an original concert schedule. The task simulates a simple rule applied while reading this schedule from top to bottom."
date: "2026-06-22T14:44:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105586
codeforces_index: "A"
codeforces_contest_name: "\u201c\u534e\u4e3a\u676f\u201d 2024 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u65b0\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u51b3\u8d5b\uff09"
rating: 0
weight: 105586
solve_time_s: 49
verified: true
draft: false
---

[CF 105586A - \u6f14\u594f\u6625\u65e5\u5f71](https://codeforces.com/problemset/problem/105586/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short playlist of songs represented as strings. Each string is a single program item in an original concert schedule.

The task simulates a simple rule applied while reading this schedule from top to bottom. Every time the performer sees the exact string `"Tomori"`, she immediately inserts an extra song `"Haruhikage"` right after it in the final output. All other strings are copied unchanged and keep their original order.

So the output is not just a copy of the input list. It is a transformed list where some entries expand into two consecutive entries depending on their value.

The input size is very small, with at most 100 strings and each string having length at most 20. This removes any concern about performance optimizations beyond straightforward linear processing. A single pass over the input is sufficient.

The only subtlety is that matching must be exact and case-sensitive. Strings like `"TOMORI"` or `"tomori"` do not trigger insertion. A naive approach that attempts case-insensitive comparison or substring matching would silently produce incorrect output.

A second corner case is when `"Tomori"` appears consecutively. In that situation, each occurrence independently triggers an insertion, so multiple `"Haruhikage"` lines may appear in sequence.

## Approaches

A direct way to think about the problem is to construct the final list explicitly. We read all strings into an array, then iterate through it and append each string to a result list. Whenever we encounter `"Tomori"`, we also append `"Haruhikage"` immediately after it.

This approach is already optimal in structure. The brute-force interpretation would be to repeatedly rebuild or insert into a growing list using operations that shift elements, such as inserting into the middle of an array. That leads to unnecessary overhead: each insertion into an array-based structure can cost O(n), and in the worst case where every element is `"Tomori"`, we would perform O(n) insertions, resulting in O(n^2) behavior.

The key observation is that we never need to modify the structure in the middle. We only need to emit output in a streaming fashion. This turns the problem into a single linear scan where each input element contributes either one or two output elements.

The structure of the problem guarantees independence between elements. Each line can be processed without knowledge of future or past values, which eliminates any need for complex data structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (insert into array/list repeatedly) | O(n^2) | O(n) | Unnecessary but works for small n |
| Optimal (single pass append/output) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, which indicates how many strings follow.
2. For each of the next `n` lines, read the string `s`.
3. Immediately output `s`.
4. If `s` is exactly equal to `"Tomori"`, output an additional line `"Haruhikage"` right after it.

The reasoning behind immediate output is that the transformation depends only on the current element. There is no dependency on future elements, so delaying processing provides no benefit.

### Why it works

The algorithm maintains a simple invariant: after processing the i-th input string, the output contains exactly the transformed version of the first i strings according to the rule, and nothing else. Since each string is handled independently and order is preserved, concatenating all local transformations produces the correct global result. No reordering or buffering is required because the transformation never changes relative order, only inserts a fixed string after specific matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

for _ in range(n):
    s = input().strip()
    print(s)
    if s == "Tomori":
        print("Haruhikage")
```

The implementation follows the algorithm directly. Input is processed line by line using fast I/O. Each string is stripped of trailing newline characters to ensure exact comparison. The conditional check is a direct equality test, which enforces case sensitivity.

The key implementation detail is printing immediately rather than storing results. While storing in a list would also work, it is unnecessary given the small constraints and the simplicity of streaming output.

## Worked Examples

### Example 1

Input:

```
3
Tomori
Neko
Tomori
```

We process each string sequentially.

| Step | Input String | Output So Far |
| --- | --- | --- |
| 1 | Tomori | Tomori Haruhikage |
| 2 | Neko | Tomori Haruhikage Neko |
| 3 | Tomori | Tomori Haruhikage Neko Tomori Haruhikage |

The first and third strings trigger the insertion rule, so `"Haruhikage"` appears twice in the output.

This demonstrates that each occurrence is handled independently, without any shared state between steps.

### Example 2

Input:

```
4
TOMORI
Tomori
Tomo
Haruhikage
```

| Step | Input String | Output So Far |
| --- | --- | --- |
| 1 | TOMORI | TOMORI |
| 2 | Tomori | TOMORI Tomori Haruhikage |
| 3 | Tomo | TOMORI Tomori Haruhikage Tomo |
| 4 | Haruhikage | TOMORI Tomori Haruhikage Tomo Haruhikage |

Only the exact `"Tomori"` matches trigger insertion. This confirms that substring matches and case variations are ignored correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is read once and processed with O(1) comparison and output operations |
| Space | O(1) auxiliary | No additional data structures are required beyond the current input string |

The linear scan is easily sufficient for n up to 100, and even scales comfortably far beyond the problem constraints. Memory usage remains constant aside from input buffering.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n = int(sys.stdin.readline().strip())
        for _ in range(n):
            s = sys.stdin.readline().strip()
            print(s)
            if s == "Tomori":
                print("Haruhikage")
    return out.getvalue().strip()

# provided sample-style tests
assert run("3\nTomori\nNeko\nTomori\n") == "Tomori\nHaruhikage\nNeko\nTomori\nHaruhikage"

# single non-trigger case
assert run("2\nNeko\nRikki\n") == "Neko\nRikki"

# case sensitivity check
assert run("3\nTOMORI\nTomori\ntomori\n") == "TOMORI\nTomori\nHaruhikage\ntomori"

# consecutive triggers
assert run("2\nTomori\nTomori\n") == "Tomori\nHaruhikage\nTomori\nHaruhikage"

# minimum case
assert run("1\nTomori\n") == "Tomori\nHaruhikage"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 lines mixed | expanded with inserts | basic transformation correctness |
| no Tomori | unchanged output | baseline pass-through behavior |
| case variants | only exact match triggers | case sensitivity |
| consecutive Tomori | repeated insertion handling | independence of events |
| single element | minimal boundary case | correctness at n=1 |

## Edge Cases

One important case is when there are no matching strings at all. For example, if the input is:

```
2
Neko
Rikki
```

the algorithm simply prints each line once and performs no insertions. Since the condition is never satisfied, no extra output appears, and the output is identical to the input sequence.

Another case is consecutive `"Tomori"` entries:

```
2
Tomori
Tomori
```

The algorithm processes the first `"Tomori"` and immediately prints `"Haruhikage"`, then processes the second independently and does the same again. There is no interaction between the two steps, so the result correctly contains two inserted lines.

A third case is strings that visually resemble the trigger but differ in case:

```
1
TOMORI
```

Since comparison is exact, the condition fails and no extra output is produced. This confirms that the equality check is strict and does not rely on pattern matching or normalization.
