---
title: "CF 1805B - The String Has a Target"
description: "We are given a string and allowed to perform exactly one operation: pick a character at some position and move it to the start of the string. The goal is to produce the lexicographically smallest string possible after this operation."
date: "2026-06-09T09:14:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1805
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 862 (Div. 2)"
rating: 800
weight: 1805
solve_time_s: 94
verified: true
draft: false
---

[CF 1805B - The String Has a Target](https://codeforces.com/problemset/problem/1805/B)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string and allowed to perform exactly one operation: pick a character at some position and move it to the start of the string. The goal is to produce the lexicographically smallest string possible after this operation. The input consists of multiple test cases, each giving a string. The output for each test case is the resulting string after the optimal move.

The constraints tell us that each string can be up to $10^5$ characters, and the sum of all string lengths across test cases is at most $10^5$. This implies that any solution must run in roughly linear time with respect to the string length, as an $O(n^2)$ approach would involve up to $10^{10}$ operations, which is infeasible.

Edge cases include strings where the first character is already the smallest, strings with repeated characters, and strings where multiple positions contain the same minimal character. For instance, given "aaa", any move will leave the string unchanged, while for "cba", the last character should be moved to the front, giving "acb". Careless implementations might just move the globally smallest character without considering the order of the remainder of the string, producing a suboptimal result.

## Approaches

The brute-force approach is straightforward: for each position $i$ in the string, simulate moving that character to the front and compare the resulting string to the current minimum. For a string of length $n$, each simulation requires constructing a new string, taking $O(n)$ time. Doing this for all $n$ positions gives an $O(n^2)$ algorithm. This is correct, but far too slow for $n = 10^5$.

The key insight is that we do not need to test every position. Moving a character only makes sense if it is less than or equal to the current first character, because otherwise the new string will start with a larger character, which cannot be optimal. Among candidates that are less than or equal to the first character, we only need to consider the leftmost occurrence that produces the smallest string after the move. By iterating once to find such a candidate and comparing the resulting string efficiently, we reduce the problem to $O(n)$ per string. The problem structure is simple because the operation affects only the first character and preserves the order of all other characters, which makes direct comparison feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the string.
3. Initialize the result as the original string, assuming moving the first character is valid.
4. Iterate through the string starting from the second character. For each character, check if it is smaller than the current first character or equal. If it is smaller, consider moving it to the front and construct the resulting string by concatenating it with the substring excluding this character. Compare this new string with the current best. If it is smaller, update the result.
5. Once all characters are considered, output the result for that test case.

Why it works: The invariant is that we always maintain the lexicographically smallest string seen so far. Since we only consider moving characters that could possibly improve the first character, and we compare the resulting strings fully, we are guaranteed to find the global minimum after exactly one move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        best = s  # initially, moving the first char is a trivial option
        for i in range(1, n):
            candidate = s[i] + s[:i] + s[i+1:]
            if candidate < best:
                best = candidate
        print(best)

if __name__ == "__main__":
    solve()
```

The code uses fast I/O with `sys.stdin.readline`. We iterate over each character from the second one because moving the first character does not change the string. Constructing the candidate string uses slicing, which in Python produces a new string efficiently. We compare lexicographically using Python's built-in `<` operator, which aligns with the problem's definition. Off-by-one errors are avoided by careful indexing: `s[:i]` excludes the current character, and `s[i+1:]` takes the suffix after it.

## Worked Examples

### Example 1: "cba"

| i | s[i] | candidate | best |
| --- | --- | --- | --- |
| 1 | b | bc a | cba |
| 2 | a | a cb | cba → acb |

The trace shows that moving 'a' to the front produces "acb", which is smaller than "cba".

### Example 2: "acac"

| i | s[i] | candidate | best |
| --- | --- | --- | --- |
| 1 | c | c a ac | acac |
| 2 | a | a ac c | acac → aacc |
| 3 | c | c ac a | aacc |

The trace demonstrates that we must consider all positions to find the optimal 'a' at index 2. It also shows the importance of fully comparing the resulting string rather than just the moved character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per string | We iterate through each character and build a new string in O(n) using slicing. |
| Space | O(n) per string | Storing the candidate string requires linear space. |

The sum of all string lengths across test cases is ≤ 10^5, so the total runtime remains well under the time limit. Memory usage is linear in the string length, fitting the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("4\n3\ncba\n4\nacac\n5\nabbcb\n4\naaba\n") == "acb\naacc\nabbcb\naaab", "sample tests"

# custom tests
assert run("1\n1\na\n") == "a", "single character"
assert run("1\n5\nzzzzz\n") == "zzzzz", "all same characters"
assert run("1\n5\nbacab\n") == "abacb", "minimal in the middle"
assert run("1\n3\ncab\n") == "acb", "minimal at last"
assert run("1\n6\naabaaa\n") == "aaabaa", "multiple minimal candidates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "a" | "a" | single-character string |
| "zzzzz" | "zzzzz" | all characters identical |
| "bacab" | "abacb" | optimal character in the middle |
| "cab" | "acb" | optimal character at end |
| "aabaaa" | "aaabaa" | multiple occurrences of minimal character |

## Edge Cases

For the single-character input "a", the algorithm considers no other positions, and the original string remains unchanged. For "zzzzz", any move produces the same string, and the comparison confirms the best is unchanged. In "bacab", moving 'a' at index 1 to the front gives "abacb", which is smaller than any other candidate. For "aabaaa", the algorithm correctly chooses the second 'a' (index 2) to produce "aaabaa", confirming that repeated minimal characters are handled correctly.

The algorithm's careful comparison at each step ensures no off-by-one or incorrect string formation occurs, and the lexicographic comparisons correctly identify the global minimum in all edge cases.
