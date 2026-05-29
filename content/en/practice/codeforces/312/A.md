---
title: "CF 312A - Whose sentence is it?"
description: "Each input line represents a sentence from a chat log, and the task is to classify who likely said it based on simple pattern clues at the beginning and end of the string. A sentence is attributed to Freda if it ends with the substring \"lala.\"."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 312
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 185 (Div. 2)"
rating: 1100
weight: 312
solve_time_s: 193
verified: false
draft: false
---

[CF 312A - Whose sentence is it?](https://codeforces.com/problemset/problem/312/A)

**Rating:** 1100  
**Tags:** implementation, strings  
**Solve time:** 3m 13s  
**Verified:** no  

## Solution
## Problem Understanding

Each input line represents a sentence from a chat log, and the task is to classify who likely said it based on simple pattern clues at the beginning and end of the string.

A sentence is attributed to Freda if it ends with the substring `"lala."`. A sentence is attributed to Rainbow if it begins with the substring `"miao."`. If both conditions appear together in the same sentence, or neither condition is satisfied, the sentence is considered unrecognizable.

The output is one label per sentence. The classification is strictly based on prefix and suffix matching, not on any deeper parsing or tokenization.

The constraints are small, with at most 10 sentences and each sentence length up to 100 characters. This immediately rules out any concern about efficiency. Even repeated string scans per sentence are negligible. The main risk is implementation detail errors: confusing prefix versus substring checks, or accidentally matching partial words instead of exact boundary-aligned substrings.

A subtle edge case appears when both markers are present in one string. For example, a sentence like `"miao.lala."` contains both patterns, but it must not be classified as either Freda or Rainbow. Another tricky case is when spacing interferes with matching. `"miao ."` is not valid Rainbow speech because the dot is not directly attached to `"miao"`.

## Approaches

A brute-force approach would, for each sentence, try to search for the substrings `"miao."` anywhere in the string and `"lala."` anywhere in the string, and then apply rules based on whether they appear. This is already sufficient given constraints, but careless substring searching can lead to incorrect classifications because the problem is not about occurrence anywhere, but about strict position: prefix for Rainbow and suffix for Freda.

The correct simplification comes from observing that both checks are constant-time operations on bounded-length strings. We do not need any search algorithm at all. We only need to inspect the first five characters for `"miao."` and the last five characters for `"lala."`, provided the string is long enough.

This reduces the problem to fixed-position comparisons using direct slicing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive substring search anywhere | O(n·L) | O(1) | Accepted but error-prone |
| Fixed prefix/suffix check | O(n·L) | O(1) | Accepted |

Here $n \le 10$, $L \le 100$, so both are trivially fast, but only the fixed-position approach matches the intended interpretation.

## Algorithm Walkthrough

1. Read all sentences from input.
2. For each sentence, check whether it starts with `"miao."`. This determines a potential Rainbow classification. The check must be anchored at position 0, since prefix position is part of the definition.
3. For each sentence, check whether it ends with `"lala."`. This determines a potential Freda classification. This must use the last five characters of the string.
4. If both conditions are true, output `"OMG>.< I don't know!"` because the sentence is ambiguous.
5. If only the prefix condition is true, output `"Rainbow's"`.
6. If only the suffix condition is true, output `"Freda's"`.
7. Otherwise, output `"OMG>.< I don't know!"`.

### Why it works

The classification rules define two independent predicates on a string: one depends only on the prefix, the other only on the suffix. Since neither predicate depends on internal structure, checking only the fixed boundary segments preserves all necessary information. Any sentence that satisfies a condition must match exactly at those positions, so no information is lost by ignoring the rest of the string. The final decision is just a logical combination of two boolean values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def classify(s: str) -> str:
    s = s.rstrip('\n')
    is_rainbow = s.startswith("miao.")
    is_freda = s.endswith("lala.")

    if is_rainbow and is_freda:
        return "OMG>.< I don't know!"
    if is_rainbow:
        return "Rainbow's"
    if is_freda:
        return "Freda's"
    return "OMG>.< I don't know!"

def main():
    n = int(input())
    for _ in range(n):
        s = input().rstrip('\n')
        print(classify(s))

if __name__ == "__main__":
    main()
```

The implementation relies on Python’s `startswith` and `endswith`, which directly encode the fixed-position checks required by the problem. Using them avoids manual slicing errors and handles short strings safely without index issues.

The classification logic is ordered so that the ambiguous case is detected first. This matters because a sentence satisfying both conditions must not fall into either single-label branch.

## Worked Examples

### Example 1

Input sentences:

```
miao.lala.
miao.
lala.
hello miao.
```

| Sentence | startswith("miao.") | endswith("lala.") | Decision |
| --- | --- | --- | --- |
| miao.lala. | True | True | ambiguous |
| miao. | True | False | Rainbow's |
| lala. | False | True | Freda's |
| hello miao. | False | False | unknown |

This trace shows how each sentence is independently classified by boundary checks only, confirming that internal occurrences like `"hello miao."` do not count as valid prefix matches.

### Example 2 (given sample excerpt)

Input:

```
miao .
wow, welcome.
miao.lala.
miao.
miao .
```

| Sentence | startswith("miao.") | endswith("lala.") | Decision |
| --- | --- | --- | --- |
| miao . | False | False | unknown |
| wow, welcome. | False | False | unknown |
| miao.lala. | True | True | ambiguous |
| miao. | True | False | Rainbow's |
| miao . | False | False | unknown |

This example highlights the importance of exact matching: `"miao ."` is not valid because of the space between `"miao"` and `"."`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · L) | Each sentence is scanned once for prefix and suffix checks, with L ≤ 100 |
| Space | O(1) | No additional data structures proportional to input size are used |

Given $n \le 10$, the runtime is effectively constant, and the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def classify(s: str) -> str:
        s = s.rstrip('\n')
        is_rainbow = s.startswith("miao.")
        is_freda = s.endswith("lala.")

        if is_rainbow and is_freda:
            return "OMG>.< I don't know!"
        if is_rainbow:
            return "Rainbow's"
        if is_freda:
            return "Freda's"
        return "OMG>.< I don't know!"

    n = int(sys.stdin.readline())
    out = []
    for _ in range(n):
        out.append(classify(sys.stdin.readline()))
    return "\n".join(out)

# provided sample
assert run("""5
I will go to play with you lala.
wow, welcome.
miao.lala.
miao.
miao .
""") == """Freda's
OMG>.< I don't know!
OMG>.< I don't know!
Rainbow's
OMG>.< I don't know!"""

# minimum size
assert run("""1
miao.lala.""") == "OMG>.< I don't know!"

# only freda
assert run("""1
hello lala.""") == "Freda's"

# only rainbow
assert run("""1
miao.hi""") == "Rainbow's"

# neither
assert run("""1
hello world""") == "OMG>.< I don't know!"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| miao.lala. | ambiguous | both prefix and suffix condition |
| hello lala. | Freda's | suffix-only detection |
| miao.hi | Rainbow's | prefix-only detection |
| hello world | unknown | no pattern match |

## Edge Cases

### Case: both markers present

Input:

```
miao.lala.
```

Here `startswith("miao.")` is true and `endswith("lala.")` is also true. The algorithm evaluates both booleans before branching. The first condition in the decision logic detects the overlap and immediately returns the ambiguous output. This prevents misclassification into either single-author category.

### Case: spacing breaks prefix

Input:

```
miao .
```

`startswith("miao.")` returns false because the string contains a space between `"miao"` and `"."`. Even though visually similar, the exact substring does not match. Since suffix check is also false, the final output is unknown.

### Case: suffix only match

Input:

```
hello lala.
```

`endswith("lala.")` is true while prefix is false. The decision flow reaches the Freda branch, confirming that suffix alignment alone is sufficient for classification.
