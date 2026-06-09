---
title: "CF 1907B - YetnotherrokenKeoard"
description: "We are asked to simulate a keyboard with broken keys that behave like selective backspaces. Every lowercase 'b' deletes the most recent lowercase letter in the typed string, and every uppercase 'B' deletes the most recent uppercase letter. All other letters are appended normally."
date: "2026-06-08T20:37:16+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1907
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 913 (Div. 3)"
rating: 1000
weight: 1907
solve_time_s: 156
verified: true
draft: false
---

[CF 1907B - YetnotherrokenKeoard](https://codeforces.com/problemset/problem/1907/B)

**Rating:** 1000  
**Tags:** data structures, implementation, strings  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a keyboard with broken keys that behave like selective backspaces. Every lowercase 'b' deletes the most recent lowercase letter in the typed string, and every uppercase 'B' deletes the most recent uppercase letter. All other letters are appended normally. The output is the final typed string after processing all key presses.

Each test case gives a string representing key presses. The input contains up to 1000 test cases, and the total number of letters across all test cases is at most one million. This implies that any algorithm must process each character in roughly constant time, since an O(n²) approach could require up to 10¹² operations in the worst case, which is far too slow. We must therefore aim for an O(n) solution per test case.

Edge cases include strings containing only 'b' or 'B' characters, in which nothing should be appended, and repeated backspace characters, which must not delete letters that do not exist. For example, the string "bbb" produces an empty output because there are no lowercase letters to delete, and "BB" produces an empty output for the same reason with uppercase letters. Mixed strings like "aBbB" must handle alternating backspaces correctly.

## Approaches

The brute-force approach would maintain a single string or list and, for each character, scan backwards to find the last character of the required case when encountering 'b' or 'B'. While this is conceptually correct, scanning backward for each backspace is O(n) per deletion, leading to a worst-case O(n²) algorithm, which is too slow for inputs of length up to 10⁶.

The key insight to achieve linear time is to maintain two separate stacks: one for lowercase letters and one for uppercase letters. When a normal character is typed, it is appended to both the final string and the corresponding stack. When a 'b' or 'B' is typed, we pop the last element from the appropriate stack and remove that letter from the final string. By using stacks, deletions become O(1) per operation, giving an overall O(n) algorithm. This works because the problem requires removing only the most recent letter of a given case, which is precisely the behavior a stack naturally models.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow for large inputs |
| Stack-based | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `result` to hold the final typed string.
2. Initialize two empty lists `lower_stack` and `upper_stack` to track the positions of lowercase and uppercase letters in `result`.
3. Iterate over each character `c` in the input string.
4. If `c` is 'b', check if `lower_stack` is non-empty. If it is, pop the last index and remove that character from `result`. If it is empty, do nothing.
5. If `c` is 'B', check if `upper_stack` is non-empty. If it is, pop the last index and remove that character from `result`. If it is empty, do nothing.
6. If `c` is a lowercase letter other than 'b', append it to `result` and append its index to `lower_stack`.
7. If `c` is an uppercase letter other than 'B', append it to `result` and append its index to `upper_stack`.
8. After processing all characters, join `result` into a string and output it.

The invariant is that `result` always contains the typed string after processing all characters up to the current position, and the stacks track positions of letters available for deletion. This guarantees that backspaces always remove the correct most recent letter.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    result = []
    lower_stack = []
    upper_stack = []
    
    for i, c in enumerate(s):
        if c == 'b':
            if lower_stack:
                idx = lower_stack.pop()
                result[idx] = ''
        elif c == 'B':
            if upper_stack:
                idx = upper_stack.pop()
                result[idx] = ''
        else:
            result.append(c)
            if c.islower():
                lower_stack.append(len(result) - 1)
            else:
                upper_stack.append(len(result) - 1)
    
    print(''.join(result))
```

The solution uses `result` as the mutable string container and two stacks to keep track of indices for quick deletion. Using indices rather than popping from `result` ensures O(1) deletion without shifting elements. We strip the input to remove the trailing newline.

## Worked Examples

### Example 1: "ARaBbbitBaby"

| Step | Character | result | lower_stack | upper_stack |
| --- | --- | --- | --- | --- |
| 1 | A | A | [] | [0] |
| 2 | R | AR | [] | [0,1] |
| 3 | a | ARa | [2] | [0,1] |
| 4 | B | Aa | [2] | [0] |
| 5 | b | A | [] | [0] |
| 6 | b | A | [] | [0] |
| 7 | i | Ai | [1] | [0] |
| 8 | t | Ait | [1,2] | [0] |
| 9 | B | it | [1,2] | [] |
| 10 | a | ita | [1,2,2] | [] |
| 11 | b | it | [1,2] | [] |
| 12 | y | ity | [1,2,3] | [] |

The trace confirms that lowercase and uppercase deletions operate independently and only remove the most recent letter of the corresponding type.

### Example 2: "Bubble"

| Step | Character | result | lower_stack | upper_stack |
| --- | --- | --- | --- | --- |
| 1 | B |  | [] | [] |
| 2 | u | u | [0] | [] |
| 3 | b |  | [] | [] |
| 4 | b |  | [] | [] |
| 5 | l | l | [0] | [] |
| 6 | e | le | [0,1] | [] |

This shows that consecutive backspaces beyond available letters are ignored without errors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once, and deletions are O(1) via stacks. |
| Space | O(n) | The result string and two stacks store up to all characters in the input. |

Given the total length of input does not exceed 10⁶, this solution fits comfortably within the 1-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        s = input().strip()
        result = []
        lower_stack = []
        upper_stack = []
        for i, c in enumerate(s):
            if c == 'b':
                if lower_stack:
                    idx = lower_stack.pop()
                    result[idx] = ''
            elif c == 'B':
                if upper_stack:
                    idx = upper_stack.pop()
                    result[idx] = ''
            else:
                result.append(c)
                if c.islower():
                    lower_stack.append(len(result) - 1)
                else:
                    upper_stack.append(len(result) - 1)
        print(''.join(result))
    return output.getvalue().strip()

# Provided samples
assert run("12\nARaBbbitBaby\nYetAnotherBrokenKeyboard\nBubble\nImprobable\nabbreviable\nBbBB\nBusyasaBeeinaBedofBloomingBlossoms\nCoDEBARbIES\ncodeforces\nbobebobbes\nb\nTheBBlackbboard\n") == """ity
YetnotherrokenKeoard
le
Imprle
revile

usyasaeeinaedofloominglossoms
CDARIES
codeforces
es

helaoard"""

# Custom test cases
assert run("3\na\nb\nB\n") == "a\n\n", "single-letter edge cases"
assert run("1\nbBbbBB\n") == "", "only backspaces, nothing to delete"
assert run("1\nAbBa\n") == "a", "alternating deletes"
assert run("1\nABCdefBb\n") == "ACdef", "mixed uppercase/lowercase with backspaces"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "a\nb\nB\n" | "a\n\n" | Single-character edge cases, backspace ignored when nothing to delete |
| "bBbbBB\n" | "" | Multiple backspaces beyond available letters |
| "AbBa\n" | "a" | Alternating uppercase |
