---
title: "CF 1582C - Grandma Capa Knits a Scarf"
description: "We are given a string of lowercase English letters, and the task is to transform it into a palindrome by erasing as few letters as possible."
date: "2026-06-10T10:02:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 1200
weight: 1582
solve_time_s: 344
verified: false
draft: false
---

[CF 1582C - Grandma Capa Knits a Scarf](https://codeforces.com/problemset/problem/1582/C)

**Rating:** 1200  
**Tags:** brute force, data structures, greedy, strings, two pointers  
**Solve time:** 5m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase English letters, and the task is to transform it into a palindrome by erasing as few letters as possible. There is one catch: we are allowed to choose only one letter type to erase, but we can remove as many occurrences of that letter as we like. The goal is to find the minimum number of deletions to achieve a palindrome under this restriction, or report that it is impossible.

For input, we get multiple test cases. Each test case gives the string length `n` and the string `s`. The output for each case is a single integer: the minimum number of deletions or `-1` if no choice of letter allows forming a palindrome.

The constraints are meaningful for our algorithm design. `n` can be up to 10^5 and the total sum of `n` across all test cases is 2 × 10^5. This immediately rules out any O(n²) algorithm per test case, because in the worst case we would perform 10^10 operations. Therefore, our solution must operate roughly in O(n) per test case.

Non-obvious edge cases include:

- The string is already a palindrome. For example, `abba` should return `0`.
- The string has all identical letters, like `aaaaa`, where no deletions are necessary.
- The string cannot become a palindrome no matter which letter we pick, e.g., `xyzxyz`. A naive approach might try random deletions and incorrectly conclude it is possible.

## Approaches

The brute-force approach is to consider all possible sequences of deletions for all letters. For each letter `c`, try removing some occurrences to make `s` a palindrome. We can implement this with a two-pointer method: start with pointers at the beginning and end of the string. If the characters are equal, move both pointers inward. If they are different, we can try removing either one only if it matches the chosen letter `c`. The brute-force fails because checking all letters for all mismatched positions in the naive way would take O(n²) per string.

The key insight is that the two-pointer approach works efficiently if we fix the letter `c` we are allowed to remove. For a fixed `c`, we can scan the string from both ends in O(n). Whenever the left and right characters differ, if one of them is `c`, we delete it and move the pointer; otherwise, we cannot form a palindrome with this choice of `c`. Repeating this for all 26 letters gives a worst-case O(26 × n) = O(n) algorithm, which is acceptable.

This observation reduces the problem from exponential possibilities of deletions to a linear scan per candidate letter. We also need to check the case where we delete nothing at all if the string is already a palindrome.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all deletions) | O(n²) | O(1) | Too slow |
| Two-pointer per candidate letter | O(26 × n) ≈ O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. Loop over each test case.
2. For each test case, read `n` and the string `s`. Initialize a variable `best` to store the minimum deletions found, starting with infinity.
3. Iterate over all lowercase letters `c` from `'a'` to `'z'`. For each `c`, try to make a palindrome using `c` as the only deletable letter.
4. Initialize two pointers, `l = 0` and `r = n - 1`, and a counter `deletions = 0`. These pointers track the current substring under consideration.
5. While `l < r`:

- If `s[l] == s[r]`, increment `l` and decrement `r`.
- If `s[l] != s[r]`:

- If `s[l] == c`, increment `l` and `deletions += 1`.
- Else if `s[r] == c`, decrement `r` and `deletions += 1`.
- Else, break and mark this letter as impossible.
6. If the pointers cross without contradiction, update `best` with the minimum of `best` and `deletions`.
7. After trying all letters, if `best` is still infinity, output `-1`. Otherwise, output `best`.

Why it works: At every step, we are forced to either match characters or remove the allowed letter. The two-pointer invariant ensures we always consider the outermost characters, so we never make unnecessary deletions. Trying all letters guarantees we find the global minimum deletions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_deletions_to_palindrome(s):
    n = len(s)
    best = float('inf')
    for c in set(s):
        l, r = 0, n - 1
        deletions = 0
        possible = True
        while l < r:
            if s[l] == s[r]:
                l += 1
                r -= 1
            elif s[l] == c:
                l += 1
                deletions += 1
            elif s[r] == c:
                r -= 1
                deletions += 1
            else:
                possible = False
                break
        if possible:
            best = min(best, deletions)
    return -1 if best == float('inf') else best

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    print(min_deletions_to_palindrome(s))
```

The solution uses fast I/O and handles multiple test cases. We iterate only over letters present in the string to minimize unnecessary checks. The two-pointer logic carefully handles edge characters and counts deletions exactly when the allowed letter is removed.

## Worked Examples

### Example 1

Input: `"abcaacab"`

| l | r | s[l] | s[r] | Action | deletions |
| --- | --- | --- | --- | --- | --- |
| 0 | 7 | a | b | remove b? no, remove a? yes | 1 |
| 1 | 7 | b | b | match | 1 |
| 2 | 6 | c | a | remove a? yes | 2 |
| 2 | 5 | c | c | match | 2 |
| 3 | 4 | a | a | match | 2 |

Output: `2`. Demonstrates that careful deletion leads to palindrome.

### Example 2

Input: `"xyzxyz"`

No letter choice allows making palindrome. Output: `-1`. Demonstrates impossible case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 * n) ≈ O(n) | Two-pointer scan for each distinct letter |
| Space | O(1) | Only counters and pointers |

This fits comfortably under the 1-second limit for n up to 10^5 and total sum 2 × 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided samples
assert run("5\n8\nabcaacab\n6\nxyzxyz\n4\nabba\n8\nrprarlap\n10\nkhyyhhyhky\n") == "2\n-1\n0\n3\n2"

# custom cases
assert run("1\n1\na\n") == "0", "single character"
assert run("1\n5\naabaa\n") == "0", "already palindrome"
assert run("1\n5\nabcde\n") == "-1", "impossible case"
assert run("1\n6\naabaaa\n") == "1", "erase middle b"
assert run("1\n4\nabab\n") == "1", "erase a to get b-b palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | single character string |
| `aabaa` | `0` | already palindrome |
| `abcde` | `-1` | impossible |
| `aabaaa` | `1` | minimal deletion middle |
| `abab` | `1` | choice of letter to erase |

## Edge Cases

For a string of length 1, `s = "a"`, the algorithm sets `best = inf` initially. Iterating over `c = 'a'` results in pointers crossing immediately with zero deletions. Output is `0`.

For `s = "xyzxyz"`, choosing any letter results in an irreconcilable mismatch somewhere. The two-pointer scan breaks early, leaving `best = inf`, returning `-1`. This correctly identifies impossible cases without over-deleting.

For `s = "aabaaa"`, choosing `c = 'b'`, the algorithm deletes `b` at index 2, pointers then meet with a palindrome `aaaaa`. Output is `1`. This demonstrates the minimal deletion logic.

This editorial ensures a reader can re-derive the solution: the critical step
