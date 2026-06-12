---
title: "CF 918A - Eleven"
description: "We are asked to generate a string of length n consisting only of the letter 'O' in uppercase and lowercase, following a rule based on the Fibonacci sequence. The positions in the string that correspond to Fibonacci numbers (1, 2, 3, 5, 8, ..."
date: "2026-06-12T09:50:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 918
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 459 (Div. 2)"
rating: 800
weight: 918
solve_time_s: 157
verified: true
draft: false
---

[CF 918A - Eleven](https://codeforces.com/problemset/problem/918/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 2m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to generate a string of length _n_ consisting only of the letter 'O' in uppercase and lowercase, following a rule based on the Fibonacci sequence. The positions in the string that correspond to Fibonacci numbers (1, 2, 3, 5, 8, ...) should be uppercase 'O', and all other positions should be lowercase 'o'. Positions are counted starting from 1.

The input is a single integer _n_, which can be as small as 1 and as large as 1000. This means that any solution with linear or near-linear time complexity will run comfortably within the 1-second time limit. There is no concern for integer overflow because Fibonacci numbers below 1000 fit within standard integers.

A subtle edge case occurs when the Fibonacci sequence has repeated numbers at the beginning. By definition, the first two Fibonacci numbers are both 1, so position 1 should be considered a Fibonacci position, and we should not mistakenly mark it twice or skip it. Another edge case is when _n_ is itself a Fibonacci number, for example _n_ = 8. We need to include this last position as uppercase.

A careless implementation could generate the Fibonacci sequence without checking bounds and might overshoot _n_, causing either an index error or extra characters. It is crucial to only mark positions within the range 1 to _n_.

## Approaches

The most straightforward approach is to compute the Fibonacci sequence up to _n_, store all the Fibonacci numbers in a list, and then iterate through positions 1 to _n_. At each position, we check if it is in the list of Fibonacci numbers. If it is, we append 'O' to the string, otherwise 'o'. This approach works because we explicitly know which positions are Fibonacci, and we only need to consider numbers up to _n_. The complexity is acceptable for _n_ ≤ 1000, but checking membership in a list repeatedly is linear in the size of the list, which is slightly inefficient.

We can optimize this by using a set instead of a list to store Fibonacci numbers. Set membership is O(1), so we reduce the overhead of checking each position. The rest of the algorithm remains the same. This is a minor optimization for this problem size but demonstrates good practice for larger _n_.

The brute-force works because it explicitly constructs the Fibonacci numbers and checks each position, but it fails in efficiency when the sequence grows large. The observation that Fibonacci positions can be stored in a set allows O(1) checks per position and streamlines the solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (list check) | O(n * m) where m is number of Fibonacci numbers ≤ n | O(m) | Accepted for n ≤ 1000 |
| Optimal (set check) | O(n) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the input integer _n_. This gives the length of the string to generate.
2. Initialize the first two Fibonacci numbers, f1 and f2, both equal to 1. These represent the first positions to mark as uppercase 'O'.
3. Generate all Fibonacci numbers less than or equal to _n_. Start from f1 and f2, and iteratively compute f_next = f1 + f2. Add each Fibonacci number to a set for O(1) membership checks. Stop once f_next > n.
4. Initialize an empty list `name` to build the resulting string. Iterating over positions i from 1 to _n_, check if i is in the Fibonacci set. If it is, append 'O' to the list; otherwise, append 'o'.
5. Join the list into a single string and print the result.

The key property that guarantees correctness is that the set contains all Fibonacci numbers up to _n_, and we iterate through exactly the positions 1 to _n_. By checking each position against this set, we ensure that every Fibonacci position is uppercase and all other positions are lowercase.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

# Generate Fibonacci numbers up to n
fib_set = set()
a, b = 1, 1
while a <= n:
    fib_set.add(a)
    a, b = b, a + b

# Build the name
name = []
for i in range(1, n + 1):
    if i in fib_set:
        name.append('O')
    else:
        name.append('o')

print(''.join(name))
```

The solution first reads the integer _n_. The Fibonacci numbers are generated in a loop, and each number is added to a set to allow constant-time lookups. Using a list `name` ensures efficient string construction. The final join operation produces the output string in one pass. Using a set avoids repeated linear scans and off-by-one errors because all indices are properly constrained to 1 through _n_.

## Worked Examples

### Sample 1

Input: 8

| i | Fibonacci? | name |
| --- | --- | --- |
| 1 | Yes | O |
| 2 | Yes | O |
| 3 | Yes | O |
| 4 | No | o |
| 5 | Yes | O |
| 6 | No | o |
| 7 | No | o |
| 8 | Yes | O |

Output: OOOoOooO

This trace confirms that positions 1, 2, 3, 5, 8 are correctly marked as uppercase 'O' and all others as lowercase 'o'.

### Custom Input

Input: 1

| i | Fibonacci? | name |
| --- | --- | --- |
| 1 | Yes | O |

Output: O

This edge case demonstrates handling of the smallest possible input. The algorithm correctly marks the first position as 'O'.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Generating Fibonacci numbers up to n takes O(log n) steps, iterating through positions 1 to n is O(n) |
| Space | O(n) | The set of Fibonacci numbers and the output list both take O(n) space in the worst case |

With n ≤ 1000, this solution comfortably fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    fib_set = set()
    a, b = 1, 1
    while a <= n:
        fib_set.add(a)
        a, b = b, a + b
    name = []
    for i in range(1, n + 1):
        name.append('O' if i in fib_set else 'o')
    return ''.join(name)

# provided sample
assert run("8\n") == "OOOoOooO", "sample 1"

# custom cases
assert run("1\n") == "O", "minimum size"
assert run("2\n") == "OO", "two positions, both Fibonacci"
assert run("10\n") == "OOOoOooOoo", "n larger, check proper Fibonacci positions"
assert run("13\n") == "OOOoOooOooOooO", "n equal to a Fibonacci number"
assert run("1000\n")[0:10] == "OOOoOooOoo", "first ten characters correctness for large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | O | Minimum input handled correctly |
| 2 | OO | First two Fibonacci numbers included |
| 10 | OOOoOooOoo | Correct Fibonacci marking within a larger string |
| 13 | OOOoOooOooOooO | Handles n equal to a Fibonacci number |
| 1000 | OOOoOooOoo... | Correctness for large n |

## Edge Cases

For the smallest input, n = 1, the algorithm generates Fibonacci numbers {1}. Iterating through position 1, it finds it in the set, appends 'O', and prints "O". This confirms that edge positions at the start of the string are handled correctly. For n equal to a Fibonacci number, such as n = 13, the last position is included because the Fibonacci set generation stops only when a > n. All positions less than or equal to n are correctly accounted for. The algorithm handles repeated Fibonacci numbers at the start (1, 1) naturally because the set ignores duplicates, ensuring position 1 is uppercase without duplication issues.
