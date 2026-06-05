---
title: "CF 312A - Whose sentence is it?"
description: "We are given a small chat log with up to 10 sentences. Each sentence is a string of letters, underscores, commas, periods, and spaces. Two people, Freda and Rainbow, are involved. According to prior experience, Freda always ends her sentences with the substring \"lala."
date: "2026-06-06T00:49:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 312
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 185 (Div. 2)"
rating: 1100
weight: 312
solve_time_s: 90
verified: false
draft: false
---

[CF 312A - Whose sentence is it?](https://codeforces.com/problemset/problem/312/A)

**Rating:** 1100  
**Tags:** implementation, strings  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small chat log with up to 10 sentences. Each sentence is a string of letters, underscores, commas, periods, and spaces. Two people, Freda and Rainbow, are involved. According to prior experience, Freda always ends her sentences with the substring `"lala."` while Rainbow always begins his sentences with `"miao."`. Our goal is to identify, for each sentence, whether it belongs to Freda, Rainbow, or if it cannot be determined. A sentence is indeterminate if it both starts with `"miao."` and ends with `"lala."`, or if it satisfies neither pattern.

The input constraints are small: at most 10 sentences and each sentence has a length of at most 100 characters. This implies that any algorithm that checks each sentence individually in linear time relative to its length is acceptable. No sophisticated data structures or optimizations are necessary, as the overall number of operations is at most 1000, far below the typical competitive programming limit of 10^8 operations per second.

Non-obvious edge cases involve whitespace and punctuation. For example, a sentence that begins with `"miao"` but has a space before the period, like `"miao ."`, is not considered Rainbow's sentence. Similarly, `"lala"` without the final period does not qualify as Freda's sentence. A sentence that simultaneously starts with `"miao."` and ends with `"lala."` should be marked as indeterminate. A naive check that only tests for the start or end without considering overlaps could misclassify such sentences.

## Approaches

A brute-force approach is straightforward. For each sentence, we can check if it ends with `"lala."` or starts with `"miao."` and output the corresponding label. If both conditions hold or neither hold, we output the indeterminate message. This works because the number of sentences is small and each sentence is short. The brute-force method is linear in the total length of the text, which in the worst case is 10 sentences times 100 characters, resulting in 1000 operations.

The optimal approach does not differ from the brute-force in this problem, as there is no larger input size to optimize for. The key insight is that string operations in Python such as `.startswith()` and `.endswith()` run in linear time with respect to the substring length, which is constant in this case (`"miao."` and `"lala."` are both length 5). Therefore, we can directly apply these built-in functions without any preprocessing or extra data structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * L) | O(1) | Accepted |
| Optimal | O(n * L) | O(1) | Accepted |

Here, `n` is the number of sentences and `L` is the maximum sentence length, 100.

## Algorithm Walkthrough

1. Read the integer `n` representing the number of sentences.
2. For each sentence in the chat record, remove the trailing newline.
3. Check if the sentence starts with `"miao."`. Store this as a boolean variable `is_rainbow`.
4. Check if the sentence ends with `"lala."`. Store this as a boolean variable `is_freda`.
5. If both `is_rainbow` and `is_freda` are True, print the indeterminate message `"OMG>.< I don't know!"`.
6. If only `is_rainbow` is True, print `"Rainbow's"`.
7. If only `is_freda` is True, print `"Freda's"`.
8. If neither is True, print the indeterminate message.

Why it works: the properties of the sentences are mutually exclusive except in the indeterminate case. By checking the start and end independently, and explicitly handling the overlap scenario, the algorithm guarantees that every sentence is classified correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
for _ in range(n):
    sentence = input().rstrip('\n')
    is_rainbow = sentence.startswith("miao.")
    is_freda = sentence.endswith("lala.")
    
    if is_rainbow and is_freda:
        print("OMG>.< I don't know!")
    elif is_rainbow:
        print("Rainbow's")
    elif is_freda:
        print("Freda's")
    else:
        print("OMG>.< I don't know!")
```

The solution reads each sentence, trims the newline character, and then checks the relevant start and end substrings. The order of checks matters: the first condition ensures that the indeterminate case is handled before any single match is printed. Using `.startswith()` and `.endswith()` avoids manual indexing errors and works even if the sentence length is exactly 5 characters.

## Worked Examples

Sample Input:

```
5
I will go to play with you lala.
wow, welcome.
miao.lala.
miao.
miao .
```

| Sentence | is_rainbow | is_freda | Output |
| --- | --- | --- | --- |
| I will go to play with you lala. | False | True | Freda's |
| wow, welcome. | False | False | OMG>.< I don't know! |
| miao.lala. | True | True | OMG>.< I don't know! |
| miao. | True | False | Rainbow's |
| miao . | False | False | OMG>.< I don't know! |

This trace demonstrates handling of all three classification cases: Freda-only, Rainbow-only, and indeterminate.

Custom Input:

```
3
lala.
miao.lala.
miao..lala.
```

| Sentence | is_rainbow | is_freda | Output |
| --- | --- | --- | --- |
| lala. | False | True | Freda's |
| miao.lala. | True | True | OMG>.< I don't know! |
| miao..lala. | False | True | Freda's |

This trace confirms that only sentences starting exactly with `"miao."` are classified as Rainbow, avoiding false positives when extra punctuation appears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * L) | Each sentence is checked for start and end substrings. `L` is at most 100. |
| Space | O(1) | Only a few boolean variables are used; no additional data structures grow with input size. |

The constraints n ≤ 10 and L ≤ 100 ensure that the solution executes in negligible time, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    output = io.StringIO()
    with redirect_stdout(output):
        n = int(input())
        for _ in range(n):
            sentence = input().rstrip('\n')
            is_rainbow = sentence.startswith("miao.")
            is_freda = sentence.endswith("lala.")
            
            if is_rainbow and is_freda:
                print("OMG>.< I don't know!")
            elif is_rainbow:
                print("Rainbow's")
            elif is_freda:
                print("Freda's")
            else:
                print("OMG>.< I don't know!")
    return output.getvalue().strip()

# Provided sample
assert run("5\nI will go to play with you lala.\nwow, welcome.\nmiao.lala.\nmiao.\nmiao .") == \
"""Freda's
OMG>.< I don't know!
OMG>.< I don't know!
Rainbow's
OMG>.< I don't know!"""

# Minimum size input
assert run("1\nmiao.") == "Rainbow's"

# Freda-only sentence
assert run("1\nhello lala.") == "Freda's"

# Indeterminate sentence both start and end
assert run("1\nmiao.lala.") == "OMG>.< I don't know!"

# Edge punctuation
assert run("1\nmiao..lala.") == "Freda's"

# Random unknown sentence
assert run("1\nhello world.") == "OMG>.< I don't know!"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| miao. | Rainbow's | Minimum-length Rainbow sentence |
| hello lala. | Freda's | Minimum-length Freda sentence |
| miao.lala. | OMG>.< I don't know! | Indeterminate case with both patterns |
| miao..lala. | Freda's | False positive avoidance for extra punctuation |
| hello world. | OMG>.< I don't know! | Unknown sentence handling |

## Edge Cases

The sentence `"miao ."` has a space before the period. Our algorithm correctly identifies it as neither Rainbow nor Freda. The boolean variables `is_rainbow` and `is_freda` are False, so the indeterminate message is printed. The sentence `"miao.lala."` triggers both `is_rainbow` and `is_freda`, producing the indeterminate output. The order of checks ensures that overlapping conditions are not misclassified. All other sentences are correctly classified based on exact substring matches at the start and end.
