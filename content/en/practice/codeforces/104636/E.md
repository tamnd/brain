---
title: "CF 104636E - YES or YES?"
description: "We are given multiple independent test cases. Each test case consists of a very short string of exactly three characters. The task is to decide whether this string represents the word “YES” when we ignore letter case."
date: "2026-06-29T17:06:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104636
codeforces_index: "E"
codeforces_contest_name: "\u041c\u0438\u0441\u0438\u0441 2023 \u043e\u0441\u0435\u043d\u044c - \u043c\u0430\u0441\u0441\u0438\u0432\u044b, \u0441\u0442\u0440\u043e\u043a\u0438"
rating: 0
weight: 104636
solve_time_s: 73
verified: true
draft: false
---

[CF 104636E - YES or YES?](https://codeforces.com/problemset/problem/104636/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. Each test case consists of a very short string of exactly three characters. The task is to decide whether this string represents the word “YES” when we ignore letter case. Any mixture of uppercase and lowercase letters is allowed, so all variants like “yes”, “YeS”, or “YEs” should be accepted.

The output is also per test case. For each input string, we print a confirmation if it matches “YES” under case-insensitive comparison, otherwise we reject it.

The constraints are extremely small: each string has length three and there are at most 1000 test cases. This means even the most direct character-by-character processing is trivial in terms of performance. Any solution that does constant work per test case is sufficient, and even slightly wasteful approaches like converting strings repeatedly or comparing against multiple variants will still pass comfortably.

There are no tricky hidden edge cases in terms of length or structure, since every input is guaranteed to be exactly three alphabetic characters. The only subtlety is case normalization. A naive comparison like checking equality against the literal string "YES" without adjusting case would fail for valid inputs like "yes" or "yEs". Another potential mistake is partially checking letters, for example comparing only the first character or using lexicographic tricks that assume uniform casing.

A representative failure case is:

Input:

```
yEs
```

Correct output:

```
YES
```

A naive implementation that checks `s == "YES"` would incorrectly print NO, since the cases differ even though the letters match conceptually.

## Approaches

The brute-force way to think about this problem is to enumerate all valid representations of the word “YES” with mixed case. Since each of the three characters can independently be uppercase or lowercase, there are $2^3 = 8$ possible variants:

YES, YEs, YeS, Yes, yES, yEs, yeS, yes.

We could store this set and check membership for each query. This is correct and runs in constant time per test case, but it is unnecessarily indirect for such a small transformation problem. It also introduces avoidable overhead in building or storing the set.

A cleaner observation is that all valid strings become identical after applying a single normalization step: converting every character to the same case. If we convert the input string to either lowercase or uppercase, then every valid variant becomes exactly "yes" or "YES". This reduces the problem to a single string comparison.

So instead of handling multiple patterns, we reduce each test case to:

convert s to lowercase, then compare with "yes".

This is the key simplification: the structure of the target word is fixed, and case is the only source of variation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate all variants | O(1) per test | O(1) | Accepted |
| Normalize case and compare | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. This defines how many independent checks we will perform.
2. For each test case, read the 3-character string. No preprocessing is needed since length is fixed.
3. Convert the string into a normalized form, typically lowercase. This removes all case distinctions so that logically identical strings map to the same representation.
4. Compare the normalized string with the target “yes”. If they match exactly, the input must be some case variation of “YES”, so we output “YES”.
5. Otherwise, output “NO”.

### Why it works

The algorithm relies on the fact that case conversion is a many-to-one mapping that preserves letter identity while removing formatting differences. Every valid input string is composed of the same letters as “YES” in some order of casing, so after normalization they all collapse to a single canonical form. Any string that differs in letters cannot become “yes” after normalization, so it will never produce a false positive.

This creates a clean invariant: after step 3, the string equals “yes” if and only if the original string is a case permutation of “YES”.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        if s.lower() == "yes":
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution processes each test case independently. The `.lower()` call is the only transformation applied, ensuring uniform comparison. Stripping is necessary to remove the newline character from input; forgetting this is a common source of incorrect comparisons.

The print statements use uppercase output, but any case is acceptable per the problem statement. The logic itself is strictly based on normalized equality.

## Worked Examples

We trace a few representative inputs from the sample.

### Example 1

Input:

```
YES
yES
Noo
```

| s | s.lower() | comparison with "yes" | output |
| --- | --- | --- | --- |
| YES | yes | equal | YES |
| yES | yes | equal | YES |
| Noo | noo | not equal | NO |

This shows that case variations collapse correctly, while letter mismatches remain distinct.

### Example 2

Input:

```
Yes
YeS
XES
```

| s | s.lower() | comparison with "yes" | output |
| --- | --- | --- | --- |
| Yes | yes | equal | YES |
| YeS | yes | equal | YES |
| XES | xes | not equal | NO |

This demonstrates that even a single wrong character breaks the equality after normalization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant-time lowercase conversion and comparison |
| Space | O(1) | No extra storage proportional to input size is required |

The solution easily fits within limits because even in the worst case of 1000 test cases, the total number of character operations is only a few thousand.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        s = sys.stdin.readline().strip()
        if s.lower() == "yes":
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output) + ("\n" if output else "")

# provided samples
assert run("10\nYES\nyES\nyes\nYes\nYeS\nNoo\norZ\nyEz\nYas\nXES\n") == \
"YES\nYES\nYES\nYES\nYES\nNO\nNO\nNO\nNO\nNO\n"

# custom cases
assert run("3\nyes\nYES\nYeS\n") == "YES\nYES\nYES\n", "all valid forms"
assert run("2\nabc\nyes\n") == "NO\nYES\n", "mixed validity"
assert run("2\nYeS\nYES\n") == "YES\nYES\n", "uppercase variants"
assert run("1\nXyZ\n") == "NO\n", "completely different string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all case variants | YES YES YES | normalization correctness |
| mixed strings | NO YES | rejection vs acceptance |
| uppercase variants | YES YES | full-case handling |
| unrelated string | NO | false positive prevention |

## Edge Cases

One edge case is when the input is already correctly formatted but mixed case, such as “YeS”. The algorithm converts it to “yes” and matches successfully. The trace is:

Input: “YeS” → lowercase becomes “yes” → equals target → output YES.

Another edge case is a completely unrelated string like “XyZ”. After normalization it becomes “xyz”, which does not match “yes”, so it correctly produces NO.

There are no structural edge cases involving length or empty input because the problem guarantees fixed-length strings, so correctness depends entirely on character matching after normalization.
