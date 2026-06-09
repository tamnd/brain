---
title: "CF 1780A - Hayato and School"
description: "We are asked to find, in an array of integers, three distinct elements whose sum is odd. The input consists of multiple test cases, each providing the array. The output must indicate whether such a triple exists, and if it does, provide any valid set of three indices."
date: "2026-06-09T11:23:37+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1780
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 846 (Div. 2)"
rating: 800
weight: 1780
solve_time_s: 128
verified: false
draft: false
---

[CF 1780A - Hayato and School](https://codeforces.com/problemset/problem/1780/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find, in an array of integers, three distinct elements whose sum is odd. The input consists of multiple test cases, each providing the array. The output must indicate whether such a triple exists, and if it does, provide any valid set of three indices.

The key property is that an integer is odd if it is not divisible by 2. Therefore, the sum of three numbers is odd if it contains either exactly one odd and two even numbers, or all three are odd. This observation immediately reduces the problem to counting odd and even numbers rather than testing all possible triples.

The constraints are moderate: each array can have up to 300 elements, but the total across all test cases does not exceed 200,000. A brute-force triple enumeration would require checking up to $\binom{300}{3} \approx 4.5 \times 10^6$ sums per test case. This is feasible for a single test case but not across 10,000 test cases, so we need a more clever approach. Additionally, edge cases include arrays containing only even numbers, arrays with fewer than three odd numbers, or arrays with a mixture where careful selection of indices matters.

A naive approach that simply tests the first three elements might fail if, for example, the array is [2, 4, 6, 1]. Picking the first three gives an even sum, but a valid triple exists including the last element. Thus, the algorithm must selectively pick indices based on parity.

## Approaches

The brute-force method iterates over all triples of indices $(i, j, k)$, sums the elements, and checks if the sum is odd. This guarantees correctness because it considers every possibility. The downside is that in the worst case with $n = 300$ and 10,000 test cases, this results in billions of operations, which is too slow.

The optimal approach uses parity. Count the indices of odd and even numbers. If there are at least three odd numbers, selecting any three yields an odd sum. Otherwise, if there is at least one odd and at least two even numbers, selecting one odd and two even also gives an odd sum. If neither condition holds, no valid triple exists. This reduces the problem to simple linear scans and conditional logic, avoiding nested loops entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) per test case | O(1) | Too slow for large inputs |
| Optimal (Parity-based) | O(n) per test case | O(n) for storing indices | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of elements $n$ and the array $a$.
2. Initialize two lists: `odd_indices` and `even_indices` to store positions of odd and even numbers.
3. Iterate over the array with a 1-based index. If the element is odd, append its index to `odd_indices`. If even, append to `even_indices`.
4. Check the length of `odd_indices`. If there are at least three elements, print "YES" and the first three indices from `odd_indices`.
5. Otherwise, check if `odd_indices` has at least one element and `even_indices` has at least two elements. If so, print "YES", the first odd index, and the first two even indices.
6. If neither condition is met, print "NO".

The invariant is that these conditions cover all cases for forming an odd sum from three numbers. Three odd numbers always sum to odd. One odd and two even numbers also sum to odd. Any other combination either results in an even sum or cannot form three distinct indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    odd_indices = []
    even_indices = []
    
    for i, num in enumerate(a, 1):
        if num % 2 == 0:
            even_indices.append(i)
        else:
            odd_indices.append(i)
    
    if len(odd_indices) >= 3:
        print("YES")
        print(odd_indices[0], odd_indices[1], odd_indices[2])
    elif len(odd_indices) >= 1 and len(even_indices) >= 2:
        print("YES")
        print(odd_indices[0], even_indices[0], even_indices[1])
    else:
        print("NO")
```

The code first separates indices by parity, then applies the logic discussed. Using 1-based indexing avoids off-by-one errors. The order of the conditions ensures the algorithm prioritizes selecting three odd numbers before the mixed case. Enumerate with `start=1` aligns array positions with the required output format.

## Worked Examples

### Sample Input 1

```
3
1 1 1
1 1 2 2
1 2 3
```

| Step | odd_indices | even_indices | Output |
| --- | --- | --- | --- |
| Test 1 | [1, 2, 3] | [] | YES 1 2 3 |
| Test 2 | [1, 2] | [3, 4] | YES 1 3 4 |
| Test 3 | [1, 3] | [2] | NO |

This trace demonstrates that the algorithm correctly picks either three odd numbers or one odd and two even numbers. When neither is available, it outputs "NO".

### Sample Input 2

```
5
2 4 6 1
2 2 2
1 3 5
```

| Step | odd_indices | even_indices | Output |
| --- | --- | --- | --- |
| Test 1 | [4] | [1, 2, 3] | YES 4 1 2 |
| Test 2 | [] | [1, 2, 3] | NO |
| Test 3 | [1, 2, 3] | [] | YES 1 2 3 |

This illustrates edge handling: a single odd with two evens produces a valid triple, whereas all-even arrays fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Linear scan to separate indices suffices; constant-time checks follow. |
| Space | O(n) | Storing indices for odd and even numbers requires at most n positions. |

Given the sum of all $n$ does not exceed 200,000, the total operations are well within typical 1-second limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        odd_indices = []
        even_indices = []
        for i, num in enumerate(a, 1):
            if num % 2 == 0:
                even_indices.append(i)
            else:
                odd_indices.append(i)
        if len(odd_indices) >= 3:
            print("YES")
            print(odd_indices[0], odd_indices[1], odd_indices[2])
        elif len(odd_indices) >= 1 and len(even_indices) >= 2:
            print("YES")
            print(odd_indices[0], even_indices[0], even_indices[1])
        else:
            print("NO")
    return output.getvalue().strip()

# provided samples
assert run("6\n3\n1 1 1\n4\n1 1 2 2\n3\n1 2 3\n5\n1 4 5 1 2\n4\n2 6 2 4\n5\n5 6 3 2 1\n") == "YES\n1 2 3\nYES\n1 3 4\nNO\nYES\n1 3 4\nNO\nYES\n1 3 5"

# custom cases
assert run("1\n3\n2 4 6\n") == "NO", "all even"
assert run("1\n3\n1 3 5\n") == "YES\n1 2 3", "all odd"
assert run("1\n4\n1 2 4 6\n") == "YES\n1 2 3", "one odd, enough evens"
assert run("1\n5\n2 2 2 1 3\n") == "YES\n4 1 2", "two odd, enough evens"
assert run("1\n3\n1 2 2\n") == "YES\n1 2 3", "one odd, two evens"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 4 6 | NO | all even numbers fail |
| 1 3 5 | YES 1 2 3 | all odd numbers succeed |
| 1 2 4 6 | YES 1 2 3 | mixed, one odd, enough evens |
| 2 2 2 1 3 | YES 4 1 2 | mixed, two odd, enough evens |
| 1 2 2 | YES 1 2 3 | minimal size with one odd, two evens |

## Edge Cases

Arrays with only even numbers such as
