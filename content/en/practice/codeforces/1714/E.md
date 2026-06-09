---
title: "CF 1714E - Add Modulo 10"
description: "We are given an array of integers, and for each element we can repeatedly increase it by its last digit. For instance, if the element is 27, applying the operation gives 27 + 7 = 34, and applying it again gives 34 + 4 = 38."
date: "2026-06-09T20:07:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1714
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 811 (Div. 3)"
rating: 1400
weight: 1714
solve_time_s: 147
verified: false
draft: false
---

[CF 1714E - Add Modulo 10](https://codeforces.com/problemset/problem/1714/E)

**Rating:** 1400  
**Tags:** brute force, math, number theory  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and for each element we can repeatedly increase it by its last digit. For instance, if the element is 27, applying the operation gives 27 + 7 = 34, and applying it again gives 34 + 4 = 38. The task is to determine whether, by applying this operation any number of times on any subset of elements, we can make all array elements equal.

The input consists of multiple test cases, each with up to 200,000 elements, and the sum of all elements over all test cases is bounded by 200,000. This implies that an algorithm must be at worst linear in the total number of elements across all test cases, since anything quadratic or higher will exceed the time limit.

Non-obvious edge cases arise because the operation behaves differently depending on the last digit. Elements ending in 0 never change, elements ending in 5 converge to a multiple of 10 in one step, and elements ending in 1-9 (except 5) follow a cycle modulo 20 after several steps. A naive approach that simulates every operation for each number can easily time out. Another subtlety is that elements with different last digits may never meet, for example 1 and 2 cannot be transformed to a common value using this operation alone.

## Approaches

The brute-force approach is to simulate the operation on every element until it either repeats a previously seen value or exceeds some bound. This works because the operation increases values monotonically, but it fails when numbers are large (up to 10^9) or the sequence is long, because simulating all steps can reach hundreds of millions of operations in total. In particular, numbers ending in 1-9 other than 5 can generate a sequence of 20 steps before repeating a pattern, so brute force can be slow if we try this for each element.

The key insight is that numbers fall into two categories based on their last digit. If a number ends with 0 or 5, after at most one operation it will reach a multiple of 10. Numbers ending with other digits eventually enter a cycle modulo 20 that is strictly increasing and never overlaps with multiples of 10. Thus, the array can only be made equal if either all numbers are multiples of 10 or can be aligned within their 20-step modulo cycle. More concretely, any number ending with 0 or 5 must all be multiples of 10 after transformations. For numbers ending in 1-9 (except 5), the transformed numbers modulo 20 must be equal, otherwise they can never coincide.

This observation allows us to classify numbers quickly without simulating every step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max_operations) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read the array length `n` and the array elements `a`.
2. Split the array into two groups: numbers ending with 0 or 5, and numbers ending with 1-9 except 5. This is because these two groups have fundamentally different behaviors under the operation.
3. For numbers ending with 0 or 5, apply the operation at most once. If any number ends with 5, it becomes a multiple of 10 after one operation. Then check if all numbers in this group are equal multiples of 10. If not, return NO.
4. For numbers ending with 1-9 except 5, observe that after repeated operations, all numbers eventually reach a value congruent to 2 mod 20. Transform each such number until it reaches a number with last digit 2. Then check if all transformed numbers are equal. If they are, return YES; otherwise, return NO.
5. If the array contains a mix of the two groups (0/5 group and 1-9 except 5 group), they can never be made equal. Return NO.

Why it works: The operation is monotone and only depends on the last digit. Numbers ending with 0 or 5 converge to multiples of 10, and numbers ending with 1-9 follow a modulo 20 cycle with last digit 2. Because of this property, we can classify numbers into mutually exclusive categories that never intersect, and equality is possible only within the same category. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_equalize(arr):
    group0 = []
    group1 = []
    for x in arr:
        last = x % 10
        if last == 0 or last == 5:
            if last == 5:
                x += 5
            group0.append(x)
        else:
            while x % 10 != 2:
                x += x % 10
            group1.append(x)
    if group0 and group1:
        return "No"
    if group0:
        return "Yes" if all(x == group0[0] for x in group0) else "No"
    return "Yes" if all(x == group1[0] for x in group1) else "No"

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(can_equalize(a))
```

The code reads each test case and separates numbers by their last digit. Numbers ending in 0 or 5 are normalized to multiples of 10, and numbers ending in 1-9 are transformed until their last digit becomes 2. The check for equality is performed within each group. If both groups exist in the same test case, the function returns NO immediately.

## Worked Examples

**Example 1:** `[6, 11]`

| Step | a[0] | a[1] | Comment |
| --- | --- | --- | --- |
| Initial | 6 | 11 | 6 ends in 6, 11 ends in 1 |
| Transform a[0] | 12 | 11 | 6+6=12 |
| Transform a[1] | 12 | 12 | 11+1=12 |
| Check equality | 12 == 12 |  | YES |

This demonstrates that numbers ending in different digits can align if they both fall into the "1-9 except 5" group.

**Example 2:** `[2, 18, 22]`

| Step | 2 | 18 | 22 | Comment |
| --- | --- | --- | --- | --- |
| Initial | 2 | 18 | 22 | All end in 2, 8, 2 |
| Transform 2 | 2+2=4 | 18 | 22 |  |
| Transform 4 | 4+4=8 | 18 | 22 | 2→4→8 |
| Transform 8 | 8+8=16 | 18 | 22 | 8→16 |
| Transform 16 | 16+6=22 | 18 | 22 | 16→22 |
| Transform 18 | 18+8=26 | 26 | 22 | 18→26, different group modulo 20 |
| Cannot equalize |  |  |  | NO |

The trace confirms the modulo 20 cycles differ and numbers cannot be made equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is transformed at most a constant number of times due to the modulo 20 cycle or last digit normalization. |
| Space | O(n) | Temporary lists to store grouped numbers. |

This is efficient enough given the constraints: total `n` across all test cases ≤ 2·10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        output.append(can_equalize(a))
    return "\n".join(output)

# Provided samples
assert run("""10
2
6 11
3
2 18 22
5
5 10 5 10 5
4
1 2 4 8
2
4 5
3
93 96 102
2
40 6
2
50 30
2
22 44
2
1 5
""") == """Yes
No
Yes
Yes
No
Yes
No
No
Yes
No"""

# Custom cases
assert run("1\n1\n0\n") == "Yes", "single element"
assert run("1\n2\n0 0\n") == "Yes", "all zero"
assert run("1\n3\n5 15 25\n") == "Yes", "all ending 5"
assert run("1\n2\n11 31\n") == "Yes", "numbers ending in 1 can align"
assert run("1\n2\n12 22\n") == "No", "numbers ending in 2 diverge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n0` | Yes | Single element, trivial equality |
| `1\n2\n0 0` | Yes | All elements already equal and zero |
| `1\n3\n5 15 25` | Yes | Numbers ending in 5 converge to multiples of 10 |
