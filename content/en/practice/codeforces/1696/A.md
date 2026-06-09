---
title: "CF 1696A - NIT orz!"
description: "We are given an array of integers and a number $z$. We are allowed to repeatedly pick any element $ai$ and perform two bitwise operations: update $ai$ to $ai operatorname{or} z$ and simultaneously update $z$ to $ai operatorname{and} z$."
date: "2026-06-09T22:33:06+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1696
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 21"
rating: 800
weight: 1696
solve_time_s: 123
verified: true
draft: false
---

[CF 1696A - NIT orz!](https://codeforces.com/problemset/problem/1696/A)

**Rating:** 800  
**Tags:** bitmasks, greedy  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a number $z$. We are allowed to repeatedly pick any element $a_i$ and perform two bitwise operations: update $a_i$ to $a_i \operatorname{or} z$ and simultaneously update $z$ to $a_i \operatorname{and} z$. The goal is to determine the maximum value that any element in the array can reach after applying these operations any number of times.

The array represents the initial values we can manipulate, and $z$ is a value that propagates its bits selectively into array elements through OR operations while losing bits through AND operations. The problem is essentially about understanding how bits can flow from $z$ to array elements and which operations will produce the largest number.

The constraints are moderate: each array has at most 2000 elements, and the sum of $n$ across all test cases is at most $10^4$. This means a quadratic algorithm per test case is feasible, but an algorithm that simulates an unbounded number of operations is risky. Edge cases include arrays of size 1, cases where $z$ is zero, and arrays where all elements are equal to $z$. A naive implementation that applies the operation blindly until convergence might get stuck or do unnecessary operations. For instance, if $a = [7]$ and $z = 3$, repeatedly applying the operation does not increase the maximum beyond 7, and careless loops could overcomplicate the calculation.

## Approaches

A brute-force approach would attempt to apply the operation on every element repeatedly until no changes occur. This is correct because every application either increases $a_i$ or decreases $z$, so it eventually stabilizes. However, in the worst case, $z$ could have up to 30 bits, and for each element we might try all combinations of bit transfers. With $n = 2000$, this could result in millions of operations, making the brute-force slow.

The key insight is that the order of operations does not matter if our goal is only the maximum element. Every operation $a_i = a_i \operatorname{or} z$ can only increase $a_i$, and $z = a_i \operatorname{and} z$ can only decrease $z$. Therefore, the maximum value that any element can reach is achieved by choosing the element that maximizes $a_i \operatorname{or} z$ in a single step. Applying multiple operations on different elements cannot yield a higher value for the maximum element than the best single OR operation.

This reduces the problem to computing $\max(a_i \operatorname{or} z)$ over all $i$, which is linear in the size of the array. This approach is efficient and fits comfortably within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 2^30) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. Each test case is independent, so we process them sequentially.
2. For each test case, read $n$ and $z$, followed by the array $a$ of length $n$. These values define the problem instance.
3. Initialize a variable `max_val` to zero. This will track the maximum achievable value across all array elements.
4. Iterate over each element $a_i$ in the array.
5. Compute `candidate = a_i | z`. This represents the value $a_i$ would achieve if we applied the operation once with the current $z$. This single operation is sufficient to consider because no combination of multiple operations produces a higher maximum than the largest OR result.
6. Update `max_val` to be the maximum of its current value and `candidate`.
7. After processing all elements, print `max_val` as the result for the test case.

Why it works: the OR operation is monotone with respect to each element, and the AND operation on $z$ only reduces bits in subsequent operations. Therefore, the highest achievable value in a single step represents the maximum possible value across any sequence of operations. No sequence of multiple operations can surpass this maximum because `a_i | z` already sets all bits that could be transferred from $z$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, z = map(int, input().split())
    a = list(map(int, input().split()))
    max_val = 0
    for x in a:
        max_val = max(max_val, x | z)
    print(max_val)
```

The code follows the algorithm precisely. Reading input with `sys.stdin.readline` ensures fast input for large arrays. The OR operation is computed for each element independently, and `max_val` keeps track of the global maximum. This avoids unnecessary operations on `z` since its decreasing value never produces a higher maximum. Off-by-one errors are avoided because the array is zero-indexed internally, even though the problem uses one-indexing.

## Worked Examples

For the input:

```
2 3
3 4
```

| a_i | a_i | z | a_i | candidate = a_i | z | max_val |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 4 | 4 | 3 | 4 | 7 | 3 | 7 |

The maximum value is 7.

For the input:

```
5 5
0 2 4 6 8
```

| a_i | a_i | z | a_i | candidate = a_i | z | max_val |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 0 | 5 | 5 | 5 |
| 2 | 2 | 5 | 2 | 7 | 5 | 7 |
| 4 | 4 | 5 | 4 | 5 | 5 | 7 |
| 6 | 6 | 5 | 6 | 7 | 5 | 7 |
| 8 | 8 | 5 | 8 | 13 | 5 | 13 |

The maximum value is 13, confirming the algorithm correctly selects the best OR.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with a single OR operation. |
| Space | O(n) | We store the array `a` for each test case. |

Given that the sum of $n$ across all test cases does not exceed $10^4$, the solution runs efficiently within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, z = map(int, input().split())
        a = list(map(int, input().split()))
        max_val = 0
        for x in a:
            max_val = max(max_val, x | z)
        print(max_val)
    return output.getvalue().strip()

# provided samples
assert run("5\n2 3\n3 4\n5 5\n0 2 4 6 8\n1 9\n10\n5 7\n7 15 30 29 27\n3 39548743\n10293834 10284344 13635445") == "7\n13\n11\n31\n48234367", "sample 1"

# custom cases
assert run("1\n1 0\n0") == "0", "single element zero"
assert run("1\n3 0\n1 2 4") == "4", "z zero, pick max element"
assert run("1\n4 15\n0 0 0 0") == "15", "all zeros, z non-zero"
assert run("1\n5 31\n1 2 4 8 16") == "31", "z maximum, spreads to any element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0\n0 | 0 | Single-element array, z=0 |
| 3 0\n1 2 4 | 4 | z=0 does not increase any element, picks max a_i |
| 4 15\n0 0 0 0 | 15 | z transfers all bits to any element |
| 5 31\n1 2 4 8 16 | 31 | Maximum z combines with any a_i for largest value |

## Edge Cases

When `z` is zero, the OR operation does not change any element, so the answer is simply the maximum of the original array. For example, if `a = [1, 2, 4]` and `z = 0`, each `a_i | z` equals `a_i`, giving a maximum of 4. When all elements are zero and `z` is non-zero, the maximum becomes exactly `z` because any element OR z equals z. If `z` is already larger than all array elements, applying it
