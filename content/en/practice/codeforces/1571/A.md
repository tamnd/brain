---
title: "CF 1571A - Sequence of Comparisons"
description: "We are given a sequence of relational signs between consecutive elements of an array, and we are asked to determine whether we can uniquely infer the relation between the first and the last element."
date: "2026-06-10T11:20:19+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1571
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 8"
rating: 800
weight: 1571
solve_time_s: 91
verified: true
draft: false
---

[CF 1571A - Sequence of Comparisons](https://codeforces.com/problemset/problem/1571/A)

**Rating:** 800  
**Tags:** *special  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of relational signs between consecutive elements of an array, and we are asked to determine whether we can uniquely infer the relation between the first and the last element. More concretely, we do not know the array itself, but we know for each adjacent pair whether the first element is smaller than, equal to, or greater than the second. The task is to decide if these comparisons are enough to determine if the first element is less than, equal to, or greater than the last element. If there is ambiguity, we should report it with a question mark.

The input consists of multiple test cases. Each test case is a string of length up to 100 characters representing these pairwise comparisons. There are at most 500 test cases, so even a solution that iterates through the string for every test case is feasible, since the total number of operations is at most 500 × 100 = 50,000, well within the 2-second time limit. This rules out any concern about needing more complex data structures or advanced algorithms; the challenge is in understanding the propagation of comparisons, not in efficiency.

The subtlety lies in the ambiguity caused by equal signs. For example, a string like `<=<` leaves room for multiple consistent sequences of numbers. One can imagine `[1, 2, 2, 1]` or `[2, 2, 3, 1]`. In such cases, the first and last elements cannot be uniquely compared. Another edge case is a string of only equal signs, such as `===`, which directly implies that all elements are equal, and thus the first and last are equal as well.

## Approaches

The naive approach is to try reconstructing sequences of numbers consistent with the given relations and then check if the comparison of the first and last elements varies. This could be done by trying all possible integer assignments, but even for length 100 this would explode combinatorially. Conceptually, it works because if any pair of sequences produces different results for the first and last elements, the comparison is ambiguous. The problem with brute force is that we do not need the actual values, only the relative changes, so enumerating numbers is overkill.

The optimal approach observes that the only comparisons that matter are the leftmost and rightmost non-equal signs. If the first non-equal sign is a less-than, then the first element is potentially smaller than the next one. Similarly, if the last non-equal sign is a greater-than, it indicates a decrease towards the end. If the string contains only `<`, only `>`, or a combination without conflicting directions, we can directly determine the relation of the first and last elements. The ambiguity arises precisely when the sequence contains both `<` and `>` signs separated by zero or more equal signs. Any equal signs in between do not affect the ordering, so the problem reduces to checking for the presence of both `<` and `>` in the string. If both exist, the answer is `?`. Otherwise, the answer is the single direction present, or `=` if only equal signs exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, examine the string of comparisons. Count whether there is at least one `<` and at least one `>` in the string. Equal signs are ignored because they do not change the relative order and can be merged into either direction.
2. If both `<` and `>` are present, return `?`. This captures the ambiguity: there exist sequences consistent with the string that make the first element both smaller and larger than the last element.
3. If only `<` signs are present, return `<` since all transitions indicate non-decreasing order leading to the last element being at least as large as the first. Similarly, if only `>` signs are present, return `>`.
4. If there are only `=` signs, return `=` since all elements are equal.

Why it works: The key property is that only the outermost directional changes determine the possible ordering of the first and last elements. Equal signs do not introduce ambiguity, and the presence of both `<` and `>` anywhere in the sequence allows constructing multiple consistent sequences where the first and last elements can be either less than or greater than each other. This invariant ensures correctness without explicit reconstruction of values.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    has_less = '<' in s
    has_greater = '>' in s
    if has_less and has_greater:
        print('?')
    elif has_less:
        print('<')
    elif has_greater:
        print('>')
    else:
        print('=')
```

The solution reads the number of test cases, then iterates over each comparison string. The key decision is made by detecting the presence of `<` and `>` in the string. This avoids any unnecessary attempts to assign actual numbers to array positions. Handling the string with `strip()` ensures that trailing newline characters do not interfere with the containment checks. The order of the conditional checks is also important: the ambiguous case is tested first, followed by the single-direction cases, and finally the all-equal case.

## Worked Examples

### Sample 1: `>>>`

| Step | has_less | has_greater | Output |
| --- | --- | --- | --- |
| '>>>' | False | True | '>' |

All signs are `>`, so the first element is greater than the last.

### Sample 2: `<><=<`

| Step | has_less | has_greater | Output |
| --- | --- | --- | --- |
| '<><=<' | True | True | '?' |

Both `<` and `>` exist, making the first-to-last comparison ambiguous.

These traces show that the algorithm correctly identifies the presence of both directions as the source of ambiguity, and sequences with only one direction or all equal signs lead to a unique determination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each comparison string once for `<` and `>` in each test case. Total operations are proportional to the sum of string lengths. |
| Space | O(1) | Only two boolean flags are used per test case, and no extra arrays or data structures are needed. |

Given n ≤ 100 and t ≤ 500, the total work is at most 50,000 operations, which is negligible relative to the 2-second limit. Memory usage is also minimal, so the solution easily fits within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        has_less = '<' in s
        has_greater = '>' in s
        if has_less and has_greater:
            out.append('?')
        elif has_less:
            out.append('<')
        elif has_greater:
            out.append('>')
        else:
            out.append('=')
    return '\n'.join(out)

# provided samples
assert run("4\n>>>\n<><=<\n=\n<<==") == ">\n?\n=\n<", "sample 1"

# custom cases
assert run("1\n<") == "<", "single less"
assert run("1\n>") == ">", "single greater"
assert run("1\n=") == "=", "single equal"
assert run("1\n<<<<<") == "<", "all less"
assert run("1\n>>>>>") == ">", "all greater"
assert run("1\n<><><>") == "?", "alternating ambiguity"
assert run("1\n=====") == "=", "all equal signs"
assert run("1\n<==>") == "?", "equal signs in between both directions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `<` | `<` | Single comparison, simple case |
| `>` | `>` | Single comparison, simple case |
| `=` | `=` | Single comparison equal |
| `<<<<<` | `<` | Multiple less-than signs only |
| `>>>>>` | `>` | Multiple greater-than signs only |
| `<><><>` | `?` | Alternating directions, ambiguity |
| `=====` | `=` | All equal signs |
| `<==>` | `?` | Equal signs separating conflicting directions |

## Edge Cases

Consider the input `<==>`. The algorithm sets `has_less = True` and `has_greater = True`, so the output is `?`. This is correct because we can construct sequences like `[1, 2, 2, 0]` making `a_1 > a_n`, or `[0, 1, 1, 2]` making `a_1 < a_n`. The equal signs do not prevent the ambiguity. This confirms that equal signs are properly ignored in determining conflicts.

For `====`, `has_less = False` and `has_greater = False`, leading to output `=`. This correctly handles the edge case where all elements are equal, including arrays of minimum length 2.
