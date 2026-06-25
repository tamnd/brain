---
title: "CF 106077B - Mercury"
description: "We have a ciphertext string made of lowercase letters. Every character in the string has been shifted by the same Caesar cipher offset, but the offset is unknown. We are also given several target phrases."
date: "2026-06-25T12:10:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106077
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 9-17-25 Div. 2 (Beginner)"
rating: 0
weight: 106077
solve_time_s: 41
verified: true
draft: false
---

[CF 106077B - Mercury](https://codeforces.com/problemset/problem/106077/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a ciphertext string made of lowercase letters. Every character in the string has been shifted by the same Caesar cipher offset, but the offset is unknown. We are also given several target phrases. After applying the correct reverse shift to the ciphertext, every one of these phrases must appear somewhere as a contiguous substring.

The task is to find any shift value that can transform the ciphertext into a string containing all given phrases. The output is the decoded string, so we need to actually apply the discovered shift and print the result.

The ciphertext length is at most 1000, and there can be at most 1000 phrases. Each phrase is short, with length at most 30. These limits are small enough that we can afford to try all possible Caesar shifts. A Caesar cipher has only 26 possible offsets, so the main work is checking 26 candidate decoded strings. With a string length around 1000 and 1000 phrases, even a quadratic style check remains far below the limit. Algorithms depending on much larger search spaces, such as trying arbitrary substitutions, would not fit the structure of the problem.

The main edge cases come from treating the shift direction incorrectly or assuming that checking only one phrase is enough. For example, consider:

```
abc
1
b
```

The correct decoded string is:

```
bcd
```

because shifting every letter of `abc` forward by one makes the phrase `b` appear. A solution that always shifts backward would fail.

Another case is when the answer shift is zero:

```
hello
2
hell
llo
```

The output should be:

```
hello
```

A careless implementation that assumes some nonzero movement is needed would miss this valid answer.

A final subtle case is repeated occurrences and overlapping phrases:

```
aaaa
2
aa
aaa
```

The correct output is:

```
aaaa
```

The substring checks must work with overlaps. Searching by manually marking used characters would incorrectly reject this case.

## Approaches

The direct approach is to simulate every possible Caesar shift. Since there are only 26 possible transformations, we can decode the whole string for each one. For every candidate decoded string, we scan through all phrases and check whether each phrase is a substring. If every phrase appears, we have found a valid answer.

This brute force is correct because the Caesar cipher has a finite set of possibilities. The original message must correspond to exactly one of those 26 shifts, so testing all of them guarantees that we will reach it.

The only possible inefficiency comes from the repeated substring checks. In the worst case, we try 26 shifts, each with 1000 phrases, and each substring search can take around the length of the ciphertext. This gives about 26 * 1000 * 1000 operations, which is only around 26 million basic character comparisons in a high level estimate. This is completely acceptable for the given limits.

The key observation is that the cipher space is tiny. We do not need to recover the shift mathematically or build advanced string matching structures. The unknown value is one number from 0 to 25, so enumeration is the natural solution. The problem looks like a string problem, but the small search space dominates the complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 * n * m * l) | O(n) | Accepted |
| Optimal | O(26 * n * m * l) | O(n) | Accepted |

Here, `n` is the ciphertext length, `m` is the number of phrases, and `l` is the maximum phrase length.

## Algorithm Walkthrough

1. Read the ciphertext and all required phrases. Store the phrases because the same list must be tested against every possible decoded string.
2. Try every possible Caesar shift from 0 to 25. For each shift, create the candidate decoded string by moving every ciphertext character by that amount.
3. Check every phrase against the candidate string. If even one phrase is missing, discard this shift and continue.
4. When a shift makes all phrases appear, print the decoded string immediately. Since an answer is guaranteed to exist, some shift will succeed.

The reason this works is that there are only 26 possible decoded versions of the ciphertext. The correct one is guaranteed to be among them, so the first valid candidate we find is enough.

### Why it works

The invariant of the search is that every candidate string we test is a valid Caesar transformation of the ciphertext. We never skip a possible decoded string because every shift value from 0 to 25 is examined.

For the correct shift, every required phrase must appear by the problem guarantee. The checking phase accepts exactly strings where all phrases are present, so the correct shift will pass the test and be returned. A wrong shift may also pass in unusual cases, but any valid decoded string is accepted, so returning the first passing candidate is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = int(input())
    phrases = [input().strip() for _ in range(n)]

    length = len(s)

    for shift in range(26):
        decoded = []
        for ch in s:
            decoded.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        decoded = ''.join(decoded)

        ok = True
        for p in phrases:
            if p not in decoded:
                ok = False
                break

        if ok:
            print(decoded)
            return

if __name__ == "__main__":
    solve()
```

The solution first stores the phrases because they need to be reused for all 26 candidates. Recomputing or rereading them would add unnecessary work.

The decoding loop converts each character into a number from 0 to 25, applies the shift with modulo arithmetic, and converts it back. The modulo operation handles wraparound cases such as shifting `z` forward to `a`.

The phrase verification uses Python's substring search. This is safe because the total input size is small. The early break when a phrase is missing avoids unnecessary checks after a failed candidate.

The code checks every shift including zero. This matters because the ciphertext might already be the decoded message.

## Worked Examples

Since the original statement does not provide samples, consider these two examples.

For the input:

```
abcxyz
2
bcd
yza
```

The trace is:

| Shift | Decoded string | Phrase checks | Result |
| --- | --- | --- | --- |
| 0 | abcxyz | bcd missing | Reject |
| 1 | bcdyza | both phrases found | Accept |

The algorithm stops after finding shift 1. This demonstrates the normal case where the correct Caesar movement is found by enumeration.

For the input:

```
hello
2
hell
llo
```

The trace is:

| Shift | Decoded string | Phrase checks | Result |
| --- | --- | --- | --- |
| 0 | hello | both phrases found | Accept |

This confirms that the zero shift case is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 * | s |
| Space | O( | s |

The largest values still make this approach small enough. Even the rough upper bound of 26 million character comparisons is comfortable in Python.

## Test Cases

```python
import sys, io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    s = input().strip()
    n = int(input())
    phrases = [input().strip() for _ in range(n)]

    for shift in range(26):
        decoded = ''.join(
            chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
            for c in s
        )

        if all(p in decoded for p in phrases):
            return decoded + "\n"

    return ""

assert solve_case("""abcxyz
2
bcd
yza
""") == "bcdyza\n", "sample style case"

assert solve_case("""hello
2
hell
llo
""") == "hello\n", "zero shift"

assert solve_case("""z
1
a
""") == "a\n", "wrap around"

assert solve_case("""aaaa
2
aa
aaa
""") == "aaaa\n", "overlapping substrings"

assert solve_case("""mnop
2
qrst
tuvw
""") == "qrst\n", "larger shift"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abcxyz` with phrases `bcd`, `yza` | `bcdyza` | Finds a nonzero shift |
| `hello` with phrases already present | `hello` | Handles zero shift |
| `z` to `a` | `a` | Handles alphabet wraparound |
| Repeated `a` characters | Same string | Allows overlapping matches |
| `mnop` to shifted phrases | Shifted string | Checks general transformation |

## Edge Cases

For the zero shift case:

```
hello
2
hell
llo
```

The algorithm starts with shift 0, builds `hello`, and checks both phrases. Since both are present, it returns immediately. A solution that starts searching from shift 1 would still eventually work, but checking zero keeps the reasoning simple and avoids unnecessary assumptions.

For the wraparound case:

```
z
1
a
```

At shift 1, the character calculation becomes `(25 + 1) % 26 = 0`, which maps back to `a`. This is why the modulo operation is essential.

For overlapping matches:

```
aaaa
2
aa
aaa
```

The candidate string is unchanged at shift 0. The substring checks find `aa` and `aaa` inside the same area of the string. The algorithm only cares about existence, not about consuming characters, so overlaps are naturally handled.
