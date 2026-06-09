---
title: "CF 1791A - Codeforces Checking"
description: "We are given a very small decision problem repeated multiple times. Each test case provides a single lowercase English letter, and we must decide whether that letter belongs to a fixed reference string, namely “codeforces”."
date: "2026-06-09T10:28:36+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1791
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 849 (Div. 4)"
rating: 800
weight: 1791
solve_time_s: 63
verified: true
draft: false
---

[CF 1791A - Codeforces Checking](https://codeforces.com/problemset/problem/1791/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small decision problem repeated multiple times. Each test case provides a single lowercase English letter, and we must decide whether that letter belongs to a fixed reference string, namely “codeforces”.

So the task is not about constructing or modifying strings, but about membership: we are effectively checking whether a character is contained in a predefined set of characters.

The input size is extremely small, with at most 26 test cases. That immediately rules out any need for optimization beyond constant time per query. Even a repeated scan of a short string is sufficient.

The only subtle mistakes that can happen here come from treating the problem as positional rather than membership-based. For example, someone might incorrectly assume only specific indices matter without realizing duplicates are irrelevant. Another possible mistake is forgetting that membership checks must be case-sensitive; uppercase letters are never part of the valid set.

A concrete failure case would be interpreting the string incorrectly as ordered matching:

Input:

```
1
c
```

Correct output:

```
YES
```

A buggy approach might check whether the character is at a specific index in the string rather than anywhere in it, and incorrectly reject it unless it matches a chosen position.

## Approaches

A direct way to solve the problem is to treat the string “codeforces” as a list of characters and, for each query, scan through it to see whether the given character matches any position. Since the reference string has length 10, this takes constant time per test case, but still involves repeated iteration.

This brute-force method is already sufficient because the input limits are tiny. However, the structure of the problem makes it even simpler: membership in a small fixed set can be precomputed once, and each query becomes a constant-time lookup.

The key observation is that we do not care about order or frequency, only whether the character exists in a known set. That allows us to replace scanning with a direct membership test using a set or boolean array indexed by character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(10 · t) | O(1) | Accepted |
| Set Lookup | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Construct a data structure containing all distinct characters from the string “codeforces”. This can be a set of characters. The purpose is to enable constant-time membership queries.
2. Read the number of test cases t.
3. For each test case, read the character c. We treat it as a single-element string or character.
4. Check whether c exists in the precomputed set. If it does, output “YES”; otherwise, output “NO”.
5. Repeat until all test cases are processed.

The reasoning behind precomputing the set is that the reference string never changes. Any repeated scanning would redundantly recompute the same information.

### Why it works

The algorithm relies on the invariant that the set always contains exactly the characters present in “codeforces” and nothing else. Each query is independent, and the membership test is equivalent to checking whether c is an element of that fixed set. Since set membership is exact and lossless, no false positives or false negatives can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = "codeforces"
    allowed = set(s)

    t = int(input())
    out = []

    for _ in range(t):
        c = input().strip()
        if c in allowed:
            out.append("YES")
        else:
            out.append("NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution precomputes a set from the string once, which avoids repeated linear scans. Each query then becomes a constant-time hash lookup. Using `strip()` ensures we correctly remove the newline character without affecting the letter itself.

The output is accumulated in a list and printed at once, which avoids repeated I/O overhead inside the loop.

## Worked Examples

### Example 1

Input:

```
5
a
c
d
x
o
```

| Step | Input c | Set contains c? | Output |
| --- | --- | --- | --- |
| 1 | a | No | NO |
| 2 | c | Yes | YES |
| 3 | d | Yes | YES |
| 4 | x | No | NO |
| 5 | o | Yes | YES |

This trace shows direct membership evaluation against the fixed character set. Each decision is independent and requires no state beyond the precomputed set.

### Example 2

Input:

```
3
f
z
e
```

| Step | Input c | Set contains c? | Output |
| --- | --- | --- | --- |
| 1 | f | Yes | YES |
| 2 | z | No | NO |
| 3 | e | Yes | YES |

This confirms that letters outside the string are correctly rejected, while all valid letters are accepted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant-time set lookup |
| Space | O(1) | The set has at most 10 characters |

The constraints are small enough that even a less optimal O(10·t) scan would pass easily. The chosen solution is simpler and avoids repeated traversal, ensuring clean and predictable performance within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys

    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""10
a
b
c
d
e
f
g
h
i
j
""") == """NO
NO
YES
YES
YES
YES
NO
NO
NO
NO"""

# custom cases
assert run("""1
c
""") == "YES", "single valid char"

assert run("""1
z
""") == "NO", "invalid char"

assert run("""3
o
c
x
""") == """YES
YES
NO""", "mixed membership"

assert run("""5
d
e
f
g
h
""") == """YES
YES
YES
NO
NO""", "boundary mix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single c | YES | minimal positive case |
| single z | NO | minimal negative case |
| o c x | YES YES NO | mixed membership logic |
| d e f g h | YES YES YES NO NO | multiple contiguous valid + invalid transitions |

## Edge Cases

One edge case is a character that is not in the English alphabetic range expected by intuition, such as ‘z’. The algorithm handles this correctly because membership is purely set-based. For input `z`, the set lookup fails and the output is “NO”.

Another edge case is repeated valid characters across multiple test cases. For input:

```
3
c
c
c
```

each lookup is independent. The set does not change, so every query returns “YES”, confirming that there is no state leakage between test cases.

Finally, a boundary case is the smallest possible input size:

```
1
a
```

Since ‘a’ is not in “codeforces”, the set check correctly returns “NO”, showing that the algorithm does not assume any default positivity.
