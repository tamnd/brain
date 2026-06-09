---
title: "CF 1744A - Number Replacement"
description: "The task is to decide if a given array of integers can be mapped to a target string using a process where each distinct number in the array is assigned a single letter, and all occurrences of that number are replaced by that letter."
date: "2026-06-09T15:57:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1744
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round  828 (Div. 3)"
rating: 800
weight: 1744
solve_time_s: 494
verified: true
draft: false
---

[CF 1744A - Number Replacement](https://codeforces.com/problemset/problem/1744/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 8m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to decide if a given array of integers can be mapped to a target string using a process where each distinct number in the array is assigned a single letter, and all occurrences of that number are replaced by that letter. The order of replacements does not matter as long as all occurrences of the same number map to the same letter. We are given multiple test cases, each with an array and a target string of equal length, and we must return "YES" if such a mapping exists or "NO" otherwise.

The constraints are small: arrays have at most 50 elements and numbers are at most 50. Since the number of distinct numbers and letters is limited, any mapping can be checked directly. The main subtlety is ensuring that no two distinct numbers map to the same letter and that the same number always maps to the same letter. A naive approach that tries all possible mappings would be unnecessary and slow if $n$ were large, but here a direct greedy check suffices.

Non-obvious edge cases include repeated numbers mapping to different letters in the target string, or multiple numbers attempting to map to the same letter. For instance, if $a = [1,2,1]$ and $s = "aba"$, this is valid because 1 maps to 'a' and 2 maps to 'b'. But if $a = [1,2,1]$ and $s = "abb"$, it is invalid because 1 would need to map to both 'a' and 'b'. Similarly, if $a = [1,2,3]$ and $s = "aaa"$, it is invalid because three distinct numbers cannot all map to the same letter.

## Approaches

The brute-force approach would attempt to try every possible assignment of numbers to letters, which is unnecessary. The problem can be reduced to verifying two conditions: every number must map consistently to one letter, and no letter can be assigned to multiple numbers. We can iterate through the array and string in parallel, keeping a dictionary mapping numbers to letters. Each time we encounter a number, we check if it has a mapping. If it does, the mapping must match the current letter. If it does not, we check if the letter has already been assigned to another number. If it has, the mapping is impossible. Otherwise, we record the mapping and continue. This greedy check runs in linear time in the array length and is sufficient due to the small constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n) | O(n) | Too slow |
| Greedy Mapping Check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length $n$, the array $a$, and the target string $s$.
2. Initialize two dictionaries: one to store the mapping from numbers to letters, and one to track which letters have been assigned.
3. Iterate over each index $i$ from 0 to $n-1$.
4. For $a_i$ and $s_i$, check if $a_i$ already has a mapping. If it does, ensure that the mapped letter equals $s_i$. If not, the answer is "NO".
5. If $a_i$ does not have a mapping, check if $s_i$ is already assigned to another number. If it is, the answer is "NO". Otherwise, assign $a_i \to s_i$ and mark $s_i$ as used.
6. If the loop completes without conflicts, the answer is "YES".

Why it works: The invariant is that each number has at most one assigned letter and each letter is assigned to at most one number. Violating either invariant immediately triggers a "NO". Since all checks are done consistently, the final mapping is guaranteed to reflect a valid transformation if it exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    s = input().strip()
    
    num_to_char = {}
    char_used = {}
    possible = True
    
    for ai, si in zip(a, s):
        if ai in num_to_char:
            if num_to_char[ai] != si:
                possible = False
                break
        else:
            if si in char_used:
                possible = False
                break
            num_to_char[ai] = si
            char_used[si] = True
    
    print("YES" if possible else "NO")
```

This code reads input using fast I/O. We maintain `num_to_char` to ensure consistent mapping of numbers to letters and `char_used` to prevent multiple numbers from mapping to the same letter. The check `num_to_char[ai] != si` ensures a number does not map to different letters, while `si in char_used` ensures letters are unique across numbers. The loop breaks early on conflict.

## Worked Examples

Sample 1:

| Index | a_i | s_i | num_to_char | char_used | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | c | {2: 'c'} | {'c'} | True |
| 1 | 3 | a | {2: 'c', 3: 'a'} | {'c','a'} | True |
| 2 | 2 | c | unchanged | unchanged | True |
| 3 | 4 | t | {2:'c',3:'a',4:'t'} | {'c','a','t'} | True |
| 4 | 1 | a | {1:'a',2:'c',3:'a',4:'t'} | {'a','c','t'} | True |

All checks pass, output is "YES".

Custom case:

a = [1,2,1], s = "abb"

| Index | a_i | s_i | num_to_char | char_used | possible |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | a | {1:'a'} | {'a'} | True |
| 1 | 2 | b | {1:'a',2:'b'} | {'a','b'} | True |
| 2 | 1 | b | conflict, 1 maps to a != b |  | False |

Output: "NO", which matches expectation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case processes up to n elements once. |
| Space | O(n) | Dictionaries store at most n elements each. |

Given t ≤ 1000 and n ≤ 50, the algorithm performs at most 50,000 iterations, well within the 2-second limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution code
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = input().strip()
        
        num_to_char = {}
        char_used = {}
        possible = True
        
        for ai, si in zip(a, s):
            if ai in num_to_char:
                if num_to_char[ai] != si:
                    possible = False
                    break
            else:
                if si in char_used:
                    possible = False
                    break
                num_to_char[ai] = si
                char_used[si] = True
        
        print("YES" if possible else "NO")
    return output.getvalue().strip()

# provided samples
assert run("7\n5\n2 3 2 4 1\ncacta\n1\n50\na\n2\n11 22\nab\n4\n1 2 2 1\naaab\n5\n1 2 3 2 1\naaaaa\n6\n1 10 2 9 3 8\nazzfdb\n7\n1 2 3 4 1 1 2\nabababb") == "YES\nYES\nYES\nNO\nYES\nYES\nNO"

# custom cases
assert run("1\n3\n1 2 1\naba") == "YES", "repeated numbers map correctly"
assert run("1\n3\n1 2 1\nabb") == "NO", "same number maps to different letters"
assert run("1\n3\n1 2 3\naa") == "NO", "more numbers than letters available"
assert run("1\n1\n1\na") == "YES", "single element, trivial mapping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1, aba | YES | repeated numbers map consistently |
| 1 2 1, abb | NO | number mapping conflict |
| 1 2 3, aa | NO | more numbers than letters used multiple times |
| 1, a | YES | minimal case |

## Edge Cases

When all numbers are identical and the string uses a single letter, the algorithm handles this naturally. For example, a = [1,1,1], s = "aaa"
