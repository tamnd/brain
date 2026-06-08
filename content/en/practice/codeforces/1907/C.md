---
title: "CF 1907C - Removal of Unattractive Pairs"
description: "We are given a string of lowercase letters, and we can repeatedly remove pairs of adjacent letters if they are different. The goal is to reduce the string to its minimum possible length."
date: "2026-06-08T20:36:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 1907
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 913 (Div. 3)"
rating: 1200
weight: 1907
solve_time_s: 137
verified: false
draft: false
---

[CF 1907C - Removal of Unattractive Pairs](https://codeforces.com/problemset/problem/1907/C)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, math, strings  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase letters, and we can repeatedly remove pairs of adjacent letters if they are different. The goal is to reduce the string to its minimum possible length. The input consists of multiple test cases, each with a string of up to 200,000 characters, and the total length across all test cases does not exceed 200,000.

This means our solution must be linear in the length of each string, because any quadratic approach would perform up to $n^2 \approx 4 \cdot 10^{10}$ operations in the worst case, which is far beyond the 1-second time limit. Each removal affects only adjacent characters, so the problem has a strong local property, suggesting a greedy or stack-based approach.

Edge cases include strings that are already composed of repeating characters, strings with alternating characters, and very short strings of length 1 or 2. For example, the string `"aa"` cannot be reduced at all, yielding a minimum length of 2, while `"ab"` can be fully removed, resulting in 0. Careless implementations that remove characters in an arbitrary order may fail to reach the minimum because the order of removals affects which letters remain.

## Approaches

The brute-force approach would repeatedly scan the string from left to right, removing the first pair of different adjacent characters encountered, and then restarting. This process is correct because every allowed operation reduces the string by exactly two characters, but it is extremely slow: each pass can take $O(n)$ and there may be up to $O(n/2)$ removals, yielding a worst-case complexity of $O(n^2)$. For $n = 2 \cdot 10^5$, this is far too slow.

The key insight for an optimal approach is to notice that removal operations only depend on the last unmatched character when scanning the string. This naturally leads to a stack-based greedy solution: traverse the string from left to right, pushing characters onto a stack. When the current character is different from the top of the stack, they form a removable pair, so pop the top instead of pushing. This ensures that every pair removal is applied immediately when possible, and the final stack length represents the minimal string length.

The brute-force works because it only removes valid pairs, but fails when the string is long due to repeated rescans. The observation that we can maintain a stack to handle local decisions reduces the time complexity to $O(n)$ because each character is pushed and popped at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Stack-based Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty stack. This will store characters that have not yet been removed.
2. Iterate over each character `c` in the string.
3. If the stack is not empty and the top character differs from `c`, pop the stack. This represents removing the adjacent pair.
4. Otherwise, push `c` onto the stack. This means `c` could not be removed with the previous character.
5. After iterating through the string, the stack contains all characters that could not be paired and removed. The minimal length of the string is the size of the stack.

Why it works: At each step, the stack maintains a correct partial solution for the prefix of the string. Each pop corresponds to a valid removal of adjacent differing characters, and no pair is missed because the stack only compares with the most recent unmatched character. Since removals are local and independent beyond adjacency, this greedy choice is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    
    stack = []
    for c in s:
        if stack and stack[-1] != c:
            stack.pop()
        else:
            stack.append(c)
    print(len(stack))
```

Explanation: We use fast I/O to handle large inputs. Each character is pushed onto the stack if it cannot form a removable pair with the top. The stack’s final length is printed for each test case. Using `strip()` ensures no newline interferes with character comparison. Boundary issues are avoided because an empty stack is correctly checked before popping.

## Worked Examples

### Example 1: `"aabc"`

| Step | Stack | Action |
| --- | --- | --- |
| 'a' | ['a'] | push 'a' |
| 'a' | ['a','a'] | push 'a' |
| 'b' | ['a'] | 'b' != 'a', pop |
| 'c' | [] | 'c' != 'a', pop |
| Final stack length: 0 |  |  |

This demonstrates that the greedy approach can remove non-adjacent characters indirectly by resolving pairs in the correct order.

### Example 2: `"abaca"`

| Step | Stack | Action |
| --- | --- | --- |
| 'a' | ['a'] | push |
| 'b' | [] | pop, 'b' != 'a' |
| 'a' | ['a'] | push |
| 'c' | [] | pop, 'c' != 'a' |
| 'a' | ['a'] | push |
| Final stack length: 1 |  |  |

This shows that when
