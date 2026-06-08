---
title: "CF 1902A - Binary Imbalance"
description: "We are given a binary string consisting of only '0' and '1' characters. We can perform a specific insertion operation between any two consecutive characters. If the two characters are the same, we insert a '1'. If they are different, we insert a '0'."
date: "2026-06-08T21:07:01+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1902
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 159 (Rated for Div. 2)"
rating: 800
weight: 1902
solve_time_s: 105
verified: true
draft: false
---

[CF 1902A - Binary Imbalance](https://codeforces.com/problemset/problem/1902/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string consisting of only '0' and '1' characters. We can perform a specific insertion operation between any two consecutive characters. If the two characters are the same, we insert a '1'. If they are different, we insert a '0'. The task is to determine whether it is possible, using any number of these operations, to make the number of zeroes strictly larger than the number of ones.

The input has multiple test cases, each with a string of length at most 100. Since the length is small, we can reason carefully about each string without worrying about performance issues for large inputs. A key observation is that the string only grows by insertions, but the type of character inserted is entirely determined by the adjacency pattern. If a string contains no adjacent characters that differ, no zero can ever be inserted. Conversely, if a string contains at least one '01' or '10', we can generate more zeroes.

An important edge case is when the string is entirely '1's. No matter how many insertions we perform, every insertion between equal characters produces another '1', so zeroes cannot outnumber ones. For example, with the input "11", the answer is "NO". Another edge case is a string with a single '0', like "0". Here the string already satisfies the requirement, and no operations are needed.

## Approaches

The brute-force approach is to simulate all possible insertions until either the zero count exceeds the one count or we exhaust all possibilities. Each insertion increases the string length by one, and there are O(n) positions to consider at each step. For n=100, this approach can explode combinatorially, producing millions of potential strings and making it infeasible. It works in principle because it directly models the problem, but it is clearly too slow.

The key insight is that the operation is deterministic based on adjacent characters. If the string already has more zeroes than ones, the answer is trivially "YES". If it has more or equal ones, we only need to check whether there is at least one adjacent pair that differs. A differing pair produces a zero when we insert between them, and inserting it increases the zero count without increasing the one count. Since we can repeat the operation at multiple differing pairs, we can always reach a configuration where zeroes outnumber ones if the string is not all ones.

This observation reduces the problem to a simple check: if the string contains at least one '0', and it is not entirely '1's, then the answer is "YES". If the string is entirely '1's, the answer is "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n^2) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, count the number of zeroes and ones in the string. If zeroes are already greater than ones, immediately output "YES".
2. If the string contains only ones, output "NO" since no operation can ever produce a zero.
3. If there is at least one '0' and the number of zeroes is not greater than ones, check for any position where adjacent characters differ. If such a pair exists, a zero can be inserted to eventually make zeroes exceed ones. Output "YES".
4. Otherwise, output "NO".

Why it works: the deterministic insertion rules guarantee that differing adjacent characters are the only source of additional zeroes. Any sequence of operations cannot reduce zeroes and cannot insert zeroes between equal ones. Therefore, either the string is capable of producing enough zeroes through these insertions, or it is impossible. The check for differing adjacent pairs captures exactly the condition needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    
    zeros = s.count('0')
    ones = s.count('1')
    
    if zeros > ones:
        print("YES")
        continue
    
    if zeros == 0:
        print("NO")
        continue
    
    found_diff_pair = False
    for i in range(n - 1):
        if s[i] != s[i + 1]:
            found_diff_pair = True
            break
    
    if found_diff_pair:
        print("YES")
    else:
        print("NO")
```

The solution first counts zeros and ones. If zeros already dominate, no operations are needed. If the string is all ones, no zero can be inserted. Otherwise, the loop checks for at least one differing adjacent pair, which guarantees the possibility of inserting zeros. We stop at the first occurrence to avoid unnecessary computation.

## Worked Examples

### Example 1: "00"

| Step | zeros | ones | adjacent differs? | Output |
| --- | --- | --- | --- | --- |
| initial | 2 | 0 | No | YES |

Zeros already exceed ones.

### Example 2: "11"

| Step | zeros | ones | adjacent differs? | Output |
| --- | --- | --- | --- | --- |
| initial | 0 | 2 | No | NO |

All ones, no zero can be inserted.

### Example 3: "10"

| Step | zeros | ones | adjacent differs? | Output |
| --- | --- | --- | --- | --- |
| initial | 1 | 1 | Yes | YES |

Differing pair at positions 1-2 allows a zero insertion.

These examples demonstrate that the algorithm correctly handles the trivial yes, trivial no, and the case where insertion creates zero dominance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting zeros and ones and scanning for differing adjacent pairs takes linear time in string length |
| Space | O(1) | Only counters and a few boolean variables are used, no additional data structures |

Given n ≤ 100 and t ≤ 100, the total work is at most 10,000 operations, well within the 2-second time limit.

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
assert run("3\n2\n00\n2\n11\n2\n10\n") == "YES\nNO\nYES", "sample 1"

# custom cases
assert run("2\n1\n0\n1\n1\n") == "YES\nNO", "single character"
assert run("1\n3\n010\n") == "YES", "alternating pattern"
assert run("1\n4\n1111\n") == "NO", "all ones"
assert run("1\n5\n00100\n") == "YES", "already zeros dominate"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-character "0"/"1" | YES / NO | minimal input edge case |
| "010" | YES | differing adjacent pairs produce zeros |
| "1111" | NO | string with all ones cannot produce zeros |
| "00100" | YES | string already satisfies condition |

## Edge Cases

The minimal input edge case with a single '0' confirms that the algorithm does not require any operations to return YES. A single '1' correctly returns NO. A string with all identical characters, like "1111" or "0000", shows that the only decisive factor is the initial counts and the presence of differing adjacent pairs. Alternating patterns like "1010" demonstrate that zero insertions can always shift the balance, and the algorithm detects this correctly through the scan for differing pairs.
