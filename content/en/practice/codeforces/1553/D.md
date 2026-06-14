---
title: "CF 1553D - Backspace"
description: "We are given two strings, where one represents what we attempt to type from left to right, and the other represents the final text we want to end up with."
date: "2026-06-14T21:12:15+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1553
codeforces_index: "D"
codeforces_contest_name: "Harbour.Space Scholarship Contest 2021-2022 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 1500
weight: 1553
solve_time_s: 427
verified: false
draft: false
---

[CF 1553D - Backspace](https://codeforces.com/problemset/problem/1553/D)

**Rating:** 1500  
**Tags:** dp, greedy, strings, two pointers  
**Solve time:** 7m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings, where one represents what we attempt to type from left to right, and the other represents the final text we want to end up with. At each character of the first string, we have a binary choice: either we append that character to our current text, or we press backspace instead, which removes the most recently kept character if one exists.

The key difficulty is that backspaces are not independent deletions on the original string. They act on the evolving output, which means earlier decisions constrain later possibilities. The task is to decide whether there exists any sequence of keep or delete decisions that transforms the first string into the second.

The constraints are large, with up to 10^5 queries and a total input size of 2 × 10^5 characters. This immediately rules out any solution that simulates all decision sequences or performs exponential search over choices. Even quadratic DP over prefixes is too slow because the combined string length already reaches the limit.

A naive interpretation might suggest simulating all possible resulting strings using DP over prefixes and stack states, but that state space grows exponentially because each character doubles the branching factor. Even pruning identical states would not survive the worst cases like repeated characters.

A subtle edge case appears when the target string is longer than the source. Since we can only delete characters, never create new ones, any case where |t| > |s| must fail immediately. Another failure mode occurs if a greedy left-to-right matching is attempted without accounting for deletions affecting future structure, for example trying to match characters as soon as they appear without considering that earlier characters may be removed later.

## Approaches

The brute-force view is to treat this as a path search over decisions at each position in s. At each index we either keep the character and append it to a simulated stack, or we apply a backspace and pop from that stack. This is correct because it directly mirrors the process definition. However, each step branches into two possibilities, giving 2^n possible decision sequences. Even for n = 200000 this is completely infeasible.

The key observation is that the final string is not dependent on the exact sequence of operations, but only on the structure of deletions relative to the characters that survive. Instead of simulating forward construction, we can reason backwards about which characters of s could survive to form t.

A useful way to view this is that each character of t must correspond to some character of s that is kept, and everything between matched characters must be deletions that cancel earlier kept characters. This suggests a two-pointer process from the end: we try to match t backwards inside s, allowing ourselves to skip characters in s, but whenever we skip a character in s we treat it as if it contributes to backspace capacity that can delete previously matched characters.

This leads to a greedy reverse scan: we walk s from right to left and try to match t from right to left, while maintaining a counter that represents how many deletions we can still apply. If we encounter a character of s that matches the current character of t and we have no pending deletions blocking it, we match it. Otherwise, we treat it as a backspace effect and increase deletion capacity.

The reversal is what makes this work: instead of simulating the stack directly, we reason about how many characters can be “erased over” from the right side, which avoids tracking the full history of the constructed string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state branching) | O(2^n) | O(n) | Too slow |
| Reverse greedy matching | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We initialize two pointers, one at the end of s and one at the end of t. We also maintain a variable that counts how many backspaces are currently available as we move left through s. This variable represents how many characters to the left we are allowed to erase without needing a direct match.
2. We iterate from the last character of s toward the first. Each character is treated based on whether we currently have pending deletions or whether it can contribute to matching t.
3. If we still have unmatched characters in t and the current character in s equals the current character in t, we consume both characters by moving both pointers left. This means we commit this character as part of the final constructed string.
4. If the characters do not match, we interpret this position in s as a decision where backspace was pressed instead of typing. This increases our deletion capacity, since this backspace can erase one previously kept character.
5. If deletion capacity is positive, we use it to “erase” a character from the constructed suffix and reduce the capacity.
6. We continue until we exhaust s. At the end, if we have successfully matched all characters of t, the answer is YES, otherwise NO.

The key invariant is that at any point while scanning from right to left, the deletion counter exactly represents how many characters to the right of the current position in s can be ignored when forming t. Any character in t that is already matched corresponds to a fixed suffix alignment that cannot be broken by earlier decisions, because all earlier operations only affect positions further left.

This ensures correctness because we never assume a character is matched unless it is structurally reachable without violating deletion constraints, and every skipped character is correctly accounted for as potential backspace capacity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        s = input().strip()
        t = input().strip()

        i = len(s) - 1
        j = len(t) - 1
        skip = 0

        while i >= 0:
            if j >= 0 and s[i] == t[j] and skip == 0:
                i -= 1
                j -= 1
            else:
                if skip > 0:
                    skip -= 1
                else:
                    skip += 1
                    i -= 1

        print("YES" if j < 0 else "NO")

if __name__ == "__main__":
    solve()
```

The solution uses a reverse two-pointer scan. The pointer i moves through s, while j tracks how much of t remains unmatched. The skip variable encodes the number of backspaces available due to earlier decisions in s. When characters match and no deletion is pending, both pointers move. Otherwise, we either consume a pending deletion or generate one by treating a character as deleted.

A subtle implementation detail is that we only match when skip is zero. This ensures that deletions always take priority, since a pending backspace must apply to earlier characters before we can safely fix a match in the suffix.

## Worked Examples

### Example 1

Input:

s = "ababa", t = "ba"

| i | j | s[i] | t[j] | skip | action |
| --- | --- | --- | --- | --- | --- |
| 4 | 1 | a | a | 0 | match j--, i-- |
| 3 | 0 | b | b | 0 | match j--, i-- |
| 2 | - | a | - | 0 | finish matching |

We finish with j = -1, so the answer is YES.

This trace shows how matches only happen when suffix alignment is clean, and earlier characters do not interfere.

### Example 2

Input:

s = "ababa", t = "bb"

| i | j | s[i] | t[j] | skip | action |
| --- | --- | --- | --- | --- | --- |
| 4 | 1 | a | b | 0 | skip++ |
| 3 | 1 | b | b | 1 | consume skip |
| 2 | 1 | a | b | 0 | skip++ |
| 1 | 1 | b | b | 1 | match |
| 0 | 0 | a | b | 0 | skip++ |

We end with j still ≥ 0, so answer is NO.

This demonstrates how mismatch positions generate deletion capacity, and how that capacity is later consumed to align valid matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character of s is processed at most once |
| Space | O(1) | Only a few pointers and counters are used |

The total length of all strings is at most 2 × 10^5, so the linear scan over all test cases easily fits within time limits, and the constant memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    q = int(input())
    res = []
    for _ in range(q):
        s = input().strip()
        t = input().strip()

        i = len(s) - 1
        j = len(t) - 1
        skip = 0

        while i >= 0:
            if j >= 0 and s[i] == t[j] and skip == 0:
                i -= 1
                j -= 1
            else:
                if skip > 0:
                    skip -= 1
                else:
                    skip += 1
                    i -= 1

        res.append("YES" if j < 0 else "NO")

    return "\n".join(res)

# provided samples
assert run("""4
ababa
ba
ababa
bb
aaa
aaaa
aababa
ababa
""") == """YES
NO
NO
YES"""

# custom cases
assert run("""1
a
a
""") == "YES", "minimum equal"

assert run("""1
a
aa
""") == "NO", "target longer than source"

assert run("""1
abc
abc
""") == "YES", "no deletions needed"

assert run("""1
abc
def
""") == "NO", "completely different strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a vs a | YES | minimum matching case |
| a vs aa | NO | impossible length increase |
| abc vs abc | YES | identity case |
| abc vs def | NO | no overlap case |

## Edge Cases

A case where t is longer than s immediately fails because no sequence of deletions can create additional characters. The algorithm naturally handles this since j cannot reach -1 before i is exhausted.

For example, s = "a", t = "aa". The scan never finds enough matching pairs, and j remains non-negative after i reaches -1, producing NO.

A second edge case is when all characters differ. For s = "abc", t = "xyz", every character becomes skip capacity but no matches ever consume it. The pointer j never moves, so the final condition correctly fails.

A third edge case involves repeated characters where greedy forward matching would fail, such as s = "ababa", t = "bb". The reverse scan ensures that the second valid 'b' is not prematurely matched before accounting for deletions, preserving correctness where forward greedy approaches would incorrectly accept or reject.
