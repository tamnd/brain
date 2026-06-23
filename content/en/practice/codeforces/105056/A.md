---
title: "CF 105056A - Potential Odoo Email"
description: "We are given a single string that is supposed to represent an email-like identifier, and we need to decide whether it matches a very specific pattern used by a fictional group of addresses. A valid string must consist of two parts separated by a single '@' character."
date: "2026-06-23T12:11:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105056
codeforces_index: "A"
codeforces_contest_name: "International Odoo Programming Contest 2024"
rating: 0
weight: 105056
solve_time_s: 71
verified: false
draft: false
---

[CF 105056A - Potential Odoo Email](https://codeforces.com/problemset/problem/105056/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single string that is supposed to represent an email-like identifier, and we need to decide whether it matches a very specific pattern used by a fictional group of addresses.

A valid string must consist of two parts separated by a single '@' character. The part before the '@' is a username made only of lowercase English letters. The part after the '@' must be the literal text "odoo". After that domain, there is no additional suffix, no extra dots, and no characters allowed.

So the task reduces to checking both structure and exact content: one '@', a left side that is non-empty and purely alphabetic lowercase, and a right side that is exactly four characters long and equals "odoo".

The input size is at most 50 characters, so even a straightforward scan or split is trivial in terms of performance. Any approach that runs in linear time over the string is sufficient.

The most common failure cases come from subtle formatting violations. A string might contain multiple '@' symbols, which immediately invalidates it. Another common issue is accepting domains that merely contain "odoo" but are not exactly equal, such as "odoocom" or "odoo." or "odoo123". Finally, uppercase letters or digits in the username should be rejected even if everything else matches.

Examples clarify these edge cases:

Input: `palm@odoocom`

Output: `no`

Even though the substring "odoo" appears, the domain is longer than required.

Input: `im_not_an_email`

Output: `no`

There is no '@' separator at all, so the structure is invalid.

## Approaches

A brute-force way to solve this is to try interpreting the string as an email by scanning every position as a potential '@' split point. For each candidate split, we would validate the left substring for lowercase letters and compare the right substring to "odoo". This works because the constraints are tiny, but it introduces unnecessary overhead since we only need to find one separator and validate it directly.

A cleaner approach is to locate the single '@' character first. If it does not exist or appears more than once, we immediately reject the string. Once the split point is known, we validate the left side by checking character types and ensuring it is not empty. Then we verify the right side is exactly "odoo" and nothing else.

The key insight is that the structure is rigid enough that we do not need any backtracking or guessing. There is exactly one valid decomposition if the string is valid at all, so direct parsing is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force split checks | O(n²) worst case | O(1) | Accepted |
| Single split validation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string E.
2. Count how many times '@' appears in E. If it is not exactly one, return "no". The format requires a single separator, so multiple or zero occurrences immediately break the structure.
3. Split E into two parts at the '@' position: left and right.
4. Check that the left part is non-empty and consists only of lowercase English letters from 'a' to 'z'. Any digit, uppercase letter, or underscore invalidates it.
5. Check that the right part is exactly the string "odoo". Any deviation in length or character content invalidates it.
6. If all checks pass, output "yes", otherwise output "no".

### Why it works

The validation enforces a unique structural decomposition of the string. Since there is exactly one valid position for '@', once that position is fixed, both halves are independently constrained with no ambiguity. The left side condition ensures no illegal characters leak into the username, and the right side equality check enforces a strict domain match. Because every invalid format violates at least one of these independent constraints, no invalid string can pass all checks simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

if s.count('@') != 1:
    print("no")
    sys.exit(0)

left, right = s.split('@')

if not left or right != "odoo":
    print("no")
    sys.exit(0)

for c in left:
    if not ('a' <= c <= 'z'):
        print("no")
        sys.exit(0)

print("yes")
```

The code begins by reading the string and immediately enforces the single '@' constraint, which removes all structurally invalid cases early.

After splitting, it validates the right side using direct string comparison, which is both simpler and safer than character-by-character checks since the target is fixed.

The left side is validated character by character to ensure only lowercase letters are present and that it is not empty. This explicit loop avoids corner cases like empty usernames or invalid symbols that would otherwise slip through a naive prefix check.

## Worked Examples

### Example 1: valid case

Input: `abc@odoo`

| Step | Left | Right | '@' count | Decision |
| --- | --- | --- | --- | --- |
| Read | abc@odoo | - | 1 | continue |
| Split | abc | odoo | 1 | continue |
| Validate left | abc | odoo | 1 | valid letters |
| Validate right | abc | odoo | 1 | matches odoo |

Output: yes

This confirms the full pipeline accepts a cleanly structured string with correct domain and lowercase username.

### Example 2: invalid domain

Input: `palm@odoocom`

| Step | Left | Right | '@' count | Decision |
| --- | --- | --- | --- | --- |
| Read | palm@odoocom | - | 1 | continue |
| Split | palm | odoocom | 1 | continue |
| Validate left | palm | odoocom | 1 | valid letters |
| Validate right | palm | odoocom | 1 | mismatch |

Output: no

This demonstrates that partial matches of the domain are rejected because equality, not substring matching, is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single scan for '@' and one pass over left side |
| Space | O(1) | only a few substrings and variables are stored |

The input size is bounded by 50, so this linear scan is effectively constant time in practice and easily fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        s = input().strip()
        if s.count('@') != 1:
            print("no")
        else:
            left, right = s.split('@')
            if not left or right != "odoo":
                print("no")
            else:
                ok = True
                for c in left:
                    if not ('a' <= c <= 'z'):
                        ok = False
                        break
                print("yes" if ok else "no")
    return out.getvalue().strip()

# provided samples
assert run("[email protected]") == "yes", "sample 1"
assert run("palm@odoocom") == "no", "sample 2"
assert run("im_not_an_email") == "no", "sample 3"

# custom cases
assert run("@odoo") == "no", "empty username"
assert run("abc@odoo@odoo") == "no", "multiple @"
assert run("ABC@odoo") == "no", "uppercase letters"
assert run("a@odoo") == "yes", "minimum valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| @odoo | no | empty username rejection |
| abc@odoo@odoo | no | multiple '@' handling |
| ABC@odoo | no | lowercase enforcement |
| a@odoo | yes | minimum valid structure |

## Edge Cases

One important edge case is an empty username. For input `@odoo`, the split produces an empty left part. The algorithm explicitly checks `if not left`, so it correctly rejects it before any character validation is attempted.

Another edge case is multiple separators, such as `abc@odoo@odoo`. Since the initial check requires exactly one '@', this input is rejected immediately without ambiguity in splitting, preventing accidental acceptance of malformed structures.

A third case is case sensitivity in the username, for example `ABC@odoo`. After splitting, the loop over the left side detects characters outside the range `'a'` to `'z'`, and the string is rejected.
