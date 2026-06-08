---
title: "CF 2065A - Skibidus and Amog'u"
description: "We are given a word that is already in its singular form in a very constrained toy language. Every word is constructed from a root string, and the singular form is always created by appending the suffix “us” to that root."
date: "2026-06-08T07:20:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 2065
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1003 (Div. 4)"
rating: 800
weight: 2065
solve_time_s: 276
verified: false
draft: false
---

[CF 2065A - Skibidus and Amog'u](https://codeforces.com/problemset/problem/2065/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, greedy, implementation, strings  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a word that is already in its singular form in a very constrained toy language. Every word is constructed from a root string, and the singular form is always created by appending the suffix “us” to that root. Our task is to reverse this process: remove the singular suffix and convert the remaining root into its plural form by appending “i”.

The input size is extremely small, with each word having length at most 10 and only lowercase English letters. This immediately rules out any need for sophisticated data structures or optimization. Any solution that processes each character a constant number of times is easily sufficient.

A subtle edge case is the minimal root. The word “us” corresponds to an empty root. Removing “us” yields an empty string, and the correct plural becomes “i”. Another corner case is when the root itself ends with letters that resemble the suffix pattern internally, such as “sussus”. Only the final two characters matter; earlier occurrences of “us” must be ignored.

## Approaches

The brute-force interpretation is to try to explicitly parse all possible root splits, but that is unnecessary because the structure of the language is rigid. Every valid input is guaranteed to end with “us”, so the transformation rule is deterministic.

The key observation is that we do not need to search or validate anything. The suffix is fixed, so the root is always obtained by removing the last two characters. Once the root is extracted, constructing the plural is a direct concatenation with “i”.

This reduces the problem from any kind of parsing or pattern matching to a simple string slicing operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force parsing | O(2^n) or unnecessary matching | O(n) | Too slow / unnecessary |
| Direct suffix removal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing a singular noun.
2. Remove the last two characters of the string. This is safe because the problem guarantees the suffix “us” always exists.
3. Treat the remaining prefix as the root of the word.
4. Append the character “i” to the root to form the plural form.
5. Output the resulting string.

The only reasoning step here is that suffix removal is always valid and does not depend on any additional checks.

### Why it works

Every valid word is constructed as root + “us”. Removing the last two characters always reconstructs the original root exactly. Since plural formation is defined independently as root + “i”, the transformation is fully determined and injective, meaning no ambiguity exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    w = input().strip()
    root = w[:-2]
    print(root + "i")
```

After reading each word, we simply slice off the final two characters. This works safely because the guarantee “ends with us” ensures the slice never corrupts the root. We then concatenate “i” to form the plural. The implementation avoids any conditionals or special cases because even the empty root case behaves correctly: “us” becomes “” and then “i”.

## Worked Examples

### Example 1

Input: `"fungus"`

| Step | Value |
| --- | --- |
| original | fungus |
| remove suffix | fung |
| add i | fungi |

This shows a standard case where the root is non-empty and straightforward.

### Example 2

Input: `"us"`

| Step | Value |
| --- | --- |
| original | us |
| remove suffix | "" |
| add i | i |

This demonstrates the edge case of an empty root, confirming that slicing produces an empty string safely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case processes at most 10 characters |
| Space | O(1) | Only temporary string slices are stored |

The constraints are tiny, so linear processing over all test cases is trivial within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        w = sys.stdin.readline().strip()
        out.append(w[:-2] + "i")
    return "\n".join(out)

# provided samples
assert run("""9
us
sus
fungus
cactus
sussus
amogus
chungus
ntarsus
skibidus
""") == """i
si
fungi
cacti
sussi
amogi
chungi
ntarsi
skibidi"""

# custom cases
assert run("""3
us
bonus
us
""") == """i
boni
i"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| us | i | empty root handling |
| bonus | boni | normal suffix removal |
| us/us | i/i | repeated minimal cases |

## Edge Cases

For the input “us”, removing the last two characters produces an empty string. The algorithm correctly handles this without special logic and outputs “i”, matching the required plural form.

For any word that contains internal “us” sequences such as “sussus”, only the final two characters are removed. The root becomes “suss”, and appending “i” gives “sussi”, showing that internal patterns do not affect correctness.
