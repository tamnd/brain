---
title: "CF 103999A - String String"
description: "We are given two strings, a longer text string and a shorter pattern string. The task is to determine how many times the pattern appears inside the text as a contiguous substring."
date: "2026-07-02T05:38:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103999
codeforces_index: "A"
codeforces_contest_name: "FMI No Stress 11"
rating: 0
weight: 103999
solve_time_s: 43
verified: true
draft: false
---

[CF 103999A - String String](https://codeforces.com/problemset/problem/103999/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, a longer text string and a shorter pattern string. The task is to determine how many times the pattern appears inside the text as a contiguous substring. Every occurrence is counted, including overlaps, so if the pattern can start at multiple adjacent positions in the text, all of them contribute to the answer.

The input is simply two lines, one containing the text and one containing the pattern. The output is a single integer representing the number of starting positions in the text where the pattern matches completely.

The key constraint that drives the solution is that the strings can be large, potentially up to around 10^5 characters in typical competitive programming settings. A naive approach that compares the pattern against the text at every possible starting position would lead to about O(nm) character comparisons in the worst case, which becomes too slow when both strings are large and similar in length.

A few edge cases tend to break careless implementations. One is when the pattern is identical to the text, where the correct answer is exactly one, but implementations that mishandle bounds or indexing may overcount or miss it entirely. Another is when the pattern has repeated structure, such as "aaaa" inside "aaaaaaaa", where overlapping matches are frequent and brute force solutions may degrade to quadratic behavior. A third is when the pattern has length one, where every character match in the text is a valid occurrence, and off-by-one errors in loop bounds are common.

## Approaches

The most direct way to solve the problem is to try aligning the pattern at every possible starting position in the text and compare character by character. For each index i in the text, we check whether the substring starting at i matches the pattern fully. This is correct because it exhaustively tests all candidate positions where a match could begin.

However, this approach performs m comparisons per starting position, where m is the pattern length. Since there are n possible starting positions, the total work is proportional to n times m. In worst-case inputs like a text of repeated characters and a pattern of repeated characters, every comparison sequence proceeds almost entirely before failing, producing quadratic behavior.

The improvement comes from recognizing that repeated comparisons between overlapping shifts of the pattern are wasteful. When we fail at a mismatch after having matched a prefix of the pattern, that prefix information can be reused. The structure that captures exactly how prefixes of a string overlap with its suffixes is the prefix function used in the Knuth-Morris-Pratt algorithm. Once this prefix structure is precomputed for the pattern, we can scan the text in a single pass while maintaining how much of the pattern has already matched. Each character in the text is processed once, and the pattern pointer only moves forward or falls back using precomputed fallback links.

This turns repeated re-computation of matches into a linear-time state machine traversal over the text.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| KMP (prefix function) | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

We solve the problem using the KMP string matching framework.

1. Compute a prefix function for the pattern string. For each position in the pattern, this value represents the length of the longest proper prefix that is also a suffix ending at that position. This structure tells us where we can resume matching if a mismatch occurs without re-checking characters from scratch.
2. Initialize a pointer j = 0, representing how many characters of the pattern are currently matched against the text.
3. Iterate over each character in the text from left to right. For each character, attempt to extend the current match.
4. If the current text character matches the pattern character at position j, increment j by one. This extends the current partial match because the prefix condition is preserved.
5. If a mismatch occurs and j is not zero, fall back using the prefix function: set j to the prefix function value at j − 1, and try matching again. This step reuses the longest valid prefix that could still align with the current suffix of the processed text.
6. Repeat the fallback process until either j becomes zero or a match is possible. If j is zero and the current character still does not match, move on to the next text character.
7. Whenever j reaches the full length of the pattern, we have found one occurrence. Increment the answer, and reset j to the prefix function value at the last position of the pattern so that overlapping matches are naturally handled.

The reason this works is that at every point in the scan, j represents the length of the longest prefix of the pattern that matches a suffix of the text ending at the current position. The prefix function guarantees that when a mismatch happens, we transition to the next best possible prefix without losing correctness or missing any valid alignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def prefix_function(p):
    n = len(p)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]
        if p[i] == p[j]:
            j += 1
        pi[i] = j
    return pi

def count_occurrences(s, p):
    if not p or not s:
        return 0

    pi = prefix_function(p)
    j = 0
    ans = 0

    for i in range(len(s)):
        while j > 0 and s[i] != p[j]:
            j = pi[j - 1]
        if s[i] == p[j]:
            j += 1

        if j == len(p):
            ans += 1
            j = pi[j - 1]

    return ans

def main():
    s = input().strip()
    p = input().strip()
    print(count_occurrences(s, p))

if __name__ == "__main__":
    main()
```

The solution separates preprocessing and scanning. The prefix function computation builds the fallback structure for the pattern. During the scan, the variable j tracks how much of the pattern is currently matched. The while-loop inside the scan is the core of the KMP transition logic, ensuring that mismatches trigger controlled fallback rather than restarting comparisons from scratch.

A subtle implementation detail is the reset after a full match. Instead of setting j to zero, we reuse the prefix function value at the last matched position. This is what enables overlapping matches to be counted correctly without re-scanning characters.

## Worked Examples

### Example 1

Input:

```
ababababa
aba
```

| i | s[i] | j before | action | j after | matches |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 0 | match | 1 | 0 |
| 1 | b | 1 | match | 2 | 0 |
| 2 | a | 2 | full match | 1 | 1 |
| 3 | b | 1 | match | 2 | 1 |
| 4 | a | 2 | full match | 1 | 2 |
| 5 | b | 1 | match | 2 | 2 |
| 6 | a | 2 | full match | 1 | 3 |
| 7 | b | 1 | match | 2 | 3 |
| 8 | a | 2 | full match | 1 | 4 |

Output:

```
4
```

This trace shows how overlapping occurrences are naturally handled because after each full match, the prefix function keeps partial structure alive instead of resetting completely.

### Example 2

Input:

```
aaaaa
aaa
```

| i | s[i] | j before | action | j after | matches |
| --- | --- | --- | --- | --- | --- |
| 0 | a | 0 | match | 1 | 0 |
| 1 | a | 1 | match | 2 | 0 |
| 2 | a | 2 | full match | 2 | 1 |
| 3 | a | 2 | full match | 2 | 2 |
| 4 | a | 2 | full match | 2 | 3 |

Output:

```
3
```

This example demonstrates maximum overlap, where every shift still produces a valid match. The prefix fallback ensures we do not restart from zero after each match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Prefix function is linear in pattern size, and scanning the text processes each character once with amortized constant fallback work |
| Space | O(m) | Prefix array stores one integer per pattern character |

The linear complexity fits comfortably within typical constraints of up to 100,000 characters, where naive quadratic approaches would be infeasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def prefix_function(p):
        n = len(p)
        pi = [0] * n
        j = 0
        for i in range(1, n):
            while j > 0 and p[i] != p[j]:
                j = pi[j - 1]
            if p[i] == p[j]:
                j += 1
            pi[i] = j
        return pi

    def solve():
        s = sys.stdin.readline().strip()
        p = sys.stdin.readline().strip()
        if not p or not s:
            return 0
        pi = prefix_function(p)
        j = 0
        ans = 0
        for i in range(len(s)):
            while j > 0 and s[i] != p[j]:
                j = pi[j - 1]
            if s[i] == p[j]:
                j += 1
            if j == len(p):
                ans += 1
                j = pi[j - 1]
        return ans

    return str(solve())

# provided samples
assert run("ababababa\naba\n") == "4"
assert run("aaaaa\naaa\n") == "3"

# custom cases
assert run("abc\nabc\n") == "1", "exact match"
assert run("abc\nb\n") == "1", "single char match"
assert run("aaaaa\nb\n") == "0", "no match"
assert run("aaaaaa\naaa\n") == "4", "heavy overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `abc / abc` | 1 | full equality case |
| `abc / b` | 1 | single-character alignment |
| `aaaaa / b` | 0 | no-match path |
| `aaaaaa / aaa` | 4 | dense overlapping matches |

## Edge Cases

One important edge case is when the pattern is exactly one character long. In this case, every matching character in the text should count as an occurrence. The algorithm handles this naturally because each match immediately triggers a full match condition and resets correctly using the prefix array, which is zero throughout.

Another edge case is a pattern that does not appear anywhere in the text. The pointer j will repeatedly fall back to zero, and no match event is ever triggered, so the answer remains zero.

A third case is maximal overlap, such as a text of repeated identical characters and a pattern that is shorter but also repeated. In this situation, after each match the prefix function keeps j non-zero, allowing the scan to continue efficiently without restarting, and ensuring every valid starting position is counted exactly once.
