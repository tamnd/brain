---
title: "CF 1926A - Vlad and the Best of Five"
description: "The task is simple: for each string of length five consisting only of the letters A and B, determine which letter occurs more frequently. Each test case provides one such string, and we have multiple test cases to process."
date: "2026-06-08T18:58:51+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1926
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 928 (Div. 4)"
rating: 800
weight: 1926
solve_time_s: 89
verified: true
draft: false
---

[CF 1926A - Vlad and the Best of Five](https://codeforces.com/problemset/problem/1926/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is simple: for each string of length five consisting only of the letters `A` and `B`, determine which letter occurs more frequently. Each test case provides one such string, and we have multiple test cases to process. The output is just the character `A` or `B` for each string, representing the most frequent letter.

The constraints are extremely light. Each string has length exactly five, and the number of test cases is at most 32. This means even a brute-force algorithm that examines every character of every string is trivially fast, because the total number of character inspections in the worst case is 32 times 5, or 160 operations. There is no need for complex optimizations or data structures. Memory usage is negligible as well.

A non-obvious edge case occurs when `A` and `B` appear the same number of times. In a string of length five, this cannot happen exactly because five is odd. Therefore, one letter always strictly dominates. Strings such as `AAAAA` or `BBBBB` represent extreme cases, where the same character fills the entire string. Another subtle case is when there is only one occurrence of the dominant letter, for example `ABBBB`, where counting logic must not miscount.

## Approaches

The naive approach is to iterate through each string and count the occurrences of `A` and `B` using a simple loop. Once both counts are known, compare them and output the letter with the higher count. This works because the string length is constant and very small, so the cost of two separate counters per string is negligible.

The key insight for a slightly more elegant approach is that Python strings support a built-in `count` method, so we can directly call `s.count('A')` and `s.count('B')` for each string. The maximum length is five, so `count` iterates at most five characters internally. This gives the same result with cleaner code. There is no need to optimize further, because the algorithm already runs in constant time for each test case.

The brute-force and the built-in-count approach both run in linear time relative to the string length, but the actual number of operations is so small that they are essentially equivalent in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual count loop | O(5 * t) = O(t) | O(1) | Accepted |
| Python `count` method | O(5 * t) = O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. This tells us how many strings to process.
2. Loop over each test case, reading the string `s` of length five.
3. Count the number of `A` characters in the string using `s.count('A')`. Store it in a variable `a_count`.
4. Count the number of `B` characters using `s.count('B')`, or equivalently compute it as `5 - a_count` since the string length is fixed.
5. Compare `a_count` and `b_count`. If `a_count` is greater, output `A`; otherwise output `B`.
6. Repeat for all test cases.

Why it works: the sum of `A` and `B` counts always equals five, so one count is enough to infer the other. Each string has a unique majority letter because the length is odd, so the comparison in step five always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    a_count = s.count('A')
    b_count = 5 - a_count
    if a_count > b_count:
        print('A')
    else:
        print('B')
```

The solution reads all input lines using fast I/O. The `.strip()` call removes any trailing newline characters. Counting `A` first and subtracting from five to get `B` avoids an unnecessary second call to `count`. The comparison is straightforward because the majority letter is guaranteed by string length. There are no off-by-one risks since we are working with the fixed length of five.

## Worked Examples

**Sample Input 1:** `ABABB`

| Step | `s` | `a_count` | `b_count` | Output |
| --- | --- | --- | --- | --- |
| 1 | ABABB | 2 | 3 | B |

**Sample Input 2:** `AAAAA`

| Step | `s` | `a_count` | `b_count` | Output |
| --- | --- | --- | --- | --- |
| 1 | AAAAA | 5 | 0 | A |

These traces show that the algorithm correctly identifies the majority character in strings where `B` dominates and where `A` dominates. Counting logic is straightforward and the fixed length prevents ambiguous cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each string has length five, so counting operations are constant per string. With up to 32 strings, total time is minimal. |
| Space | O(1) | We store only two counters per string and no extra data structures. |

Given the constraints, this solution completes in negligible time and uses trivial memory, well within the provided limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        s = input().strip()
        a_count = s.count('A')
        b_count = 5 - a_count
        if a_count > b_count:
            output.append('A')
        else:
            output.append('B')
    return "\n".join(output)

# provided sample
assert run("8\nABABB\nABABA\nBBBAB\nAAAAA\nBBBBB\nBABAA\nAAAAB\nBAAAA\n") == "B\nA\nB\nA\nB\nA\nA\nA", "sample 1"

# custom cases
assert run("1\nBBBBB\n") == "B", "all B"
assert run("1\nAAAAA\n") == "A", "all A"
assert run("1\nABBBB\n") == "B", "one A, four B"
assert run("1\nAAABB\n") == "A", "three A, two B"
assert run("1\nBAAAA\n") == "A", "one B, four A"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| BBBBB | B | all characters same, all B |
| AAAAA | A | all characters same, all A |
| ABBBB | B | small majority of B over A |
| AAABB | A | small majority of A over B |
| BAAAA | A | one B at start, majority A |

## Edge Cases

For strings where all characters are the same, like `AAAAA` or `BBBBB`, the algorithm counts five for one letter and zero for the other. The comparison still works and returns the correct letter. For strings with one minority character, such as `ABBBB` or `BAAAA`, the counting still produces the correct majority because the fixed string length guarantees a unique dominant character. No additional handling is necessary.
