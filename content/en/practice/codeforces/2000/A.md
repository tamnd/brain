---
title: "CF 2000A - Primary Task"
description: "We are given a list of integers written on a board, and one of them might be a corrupted representation of a number of the form $10^x$ where $x ge 2$. The corruption happens because the exponentiation symbol '^' was lost."
date: "2026-06-08T14:11:27+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 800
weight: 2000
solve_time_s: 157
verified: true
draft: false
---

[CF 2000A - Primary Task](https://codeforces.com/problemset/problem/2000/A)

**Rating:** 800  
**Tags:** implementation, math, strings  
**Solve time:** 2m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers written on a board, and one of them might be a corrupted representation of a number of the form $10^x$ where $x \ge 2$. The corruption happens because the exponentiation symbol '^' was lost. For instance, $10^5$ may have been written as $105$ and $10^{19}$ as $1019$. Our task is to determine, for each number on the board, whether it could be the corrupted version of such a power of ten. If it could be, we print "YES"; otherwise, we print "NO".

The input size allows up to 10,000 integers, each not exceeding 10,000. This upper bound is small, which immediately suggests that we can precompute all potential valid numbers and perform a simple membership check for each integer, rather than doing complex arithmetic transformations. The problem's subtlety lies in correctly interpreting what counts as a corrupted $10^x$: the number must start with 10 and then have the digits of the exponent concatenated directly, not any arbitrary digits. For example, 1010 could correspond to $10^{10}$, but 100 or 1023 cannot.

Edge cases that might trip up a naive solution include numbers like 100 (which is $10^2$) - since $x \ge 2$, the corruption could produce 102, but not 100. Similarly, numbers like 1002 should be interpreted carefully: it represents $10^2$ with '2' appended as exponent, but 1002 itself does not correspond to a valid corrupted form since the exponent would need to be 2 but the digits don't match. Small numbers, numbers with multiple leading zeros, and numbers close to the 10,000 limit are potential pitfalls.

## Approaches

A brute-force approach would attempt to reconstruct $10^x$ for all $x \ge 2$, convert them into strings, simulate the corruption by removing the '^' symbol, and then compare each corrupted number with the input list. While this is feasible for a single integer, doing this for 10,000 integers and potentially very large exponents would be inefficient. Specifically, checking all $x$ up to, say, 1,000,000 is unnecessary because our integers are bounded by 10,000.

The key observation is that the maximum integer on the board is 10,000, which means the largest $10^x$ that could produce a corrupted number within this range is $10^2 = 100$ up to $10^4 = 10000$. More generally, if we enumerate $x$ from 2 upwards and form the corrupted numbers by concatenating "10" and the digits of $x$, we can precompute all possible valid numbers that fit within the 1 to 10,000 range. Then for each input number, we simply check if it exists in this precomputed set. This reduces the problem to a constant-time lookup per number and is trivially fast.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check each x for each a) | O(t * max_x) | O(1) | Too slow if max_x large |
| Precompute valid corrupted numbers | O(max_x + t) | O(max_x) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty set to store all numbers that could be corrupted forms of $10^x$ with $x \ge 2$ and the resulting number ≤ 10,000. We use a set for O(1) membership checks.
2. Iterate $x$ starting from 2, convert $x$ to a string, and concatenate it with "10" to simulate the corrupted number. Convert this concatenated string back to an integer.
3. If the resulting integer is greater than 10,000, break the loop, because larger $x$ only produces larger numbers, which are outside the input bounds.
4. Add each valid integer to the set.
5. For each input integer, check if it exists in the precomputed set. If it does, print "YES"; otherwise, print "NO".

This works because the corruption is deterministic: a valid number must always start with "10" followed by digits representing the exponent. By precomputing all possibilities within the input constraints, we guarantee correctness and avoid unnecessary calculations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
numbers = [int(input()) for _ in range(t)]

valid_set = set()
x = 2
while True:
    corrupted = int("10" + str(x))
    if corrupted > 10000:
        break
    valid_set.add(corrupted)
    x += 1

for a in numbers:
    if a in valid_set:
        print("YES")
    else:
        print("NO")
```

We first read all inputs into a list. The precomputation loop builds the set of all valid corrupted numbers by concatenating "10" with each exponent starting from 2 until the resulting number exceeds 10,000. During the final loop, we leverage the O(1) lookup of the set to determine membership efficiently.

## Worked Examples

Using Sample 1:

Input:

```
7
100
1010
101
105
2033
1019
1002
```

Precomputed set: {102, 103, 104, 105, 106, 107, 108, 109, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024}

| Input a | Is in set? | Output |
| --- | --- | --- |
| 100 | No | NO |
| 1010 | Yes | YES |
| 101 | No | NO |
| 105 | Yes | YES |
| 2033 | No | NO |
| 1019 | Yes | YES |
| 1002 | No | NO |

This confirms the algorithm correctly identifies valid corrupted numbers and ignores others.

Another example:

Input:

```
3
102
103
1100
```

| Input a | Is in set? | Output |
| --- | --- | --- |
| 102 | Yes | YES |
| 103 | Yes | YES |
| 1100 | No | NO |

This demonstrates correctness for the lower boundary of the exponent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t + max_x) | Precomputation loops over x until corrupted > 10000; checking t numbers is O(1) each |
| Space | O(max_x) | Set stores all valid corrupted numbers; max_x ≈ 100 |

With t ≤ 10^4 and integers ≤ 10^4, precomputing at most a few dozen numbers and checking membership is extremely fast. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    numbers = [int(input()) for _ in range(t)]
    
    valid_set = set()
    x = 2
    while True:
        corrupted = int("10" + str(x))
        if corrupted > 10000:
            break
        valid_set.add(corrupted)
        x += 1
    
    for a in numbers:
        if a in valid_set:
            print("YES")
        else:
            print("NO")
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided sample
assert run("7\n100\n1010\n101\n105\n2033\n1019\n1002\n") == "NO\nYES\nNO\nYES\nNO\nYES\nNO", "Sample 1"

# Custom tests
assert run("3\n102\n103\n1100\n") == "YES\nYES\nNO", "Lower boundary exponents"
assert run("5\n100\n101\n104\n109\n1015\n") == "NO\nNO\nYES\nYES\nYES", "Mix of valid and invalid"
assert run("1\n10000\n") == "NO", "Maximum value edge"
assert run("1\n1010\n") == "YES", "Direct match"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n102\n103\n1100 | YES\nYES\nNO | Lower boundary exponents |
| 5\n100\n101\n104\n109\n1015 | NO\nNO\nYES\nYES\nYES | Mix of valid and invalid |
| 1\n10000 | NO | Upper boundary number, outside valid corrupted forms |
| 1\n1010 | YES | Direct match to a corrupted power of ten |

## Edge Cases

For the smallest possible exponent, x = 2, the corrupted number is 102. The algorithm includes 102 in the set, ensuring that input '102' is correctly identified as "YES". For numbers just above the 10,000 limit, such as 10002, the precomputation loop stops before including them, so the algorithm correctly returns "NO". The set-based lookup guarantees that repeated numbers or unordered inputs do not affect correctness. The deterministic formation of corrupted numbers ensures no valid number is omitted.
