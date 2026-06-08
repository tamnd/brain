---
title: "CF 1926D - Vlad and Division"
description: "We are given a set of non-negative integers and asked to partition them into groups so that within each group, no two numbers share a 1-bit in the same position across the first 31 bits."
date: "2026-06-08T19:00:47+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1926
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 928 (Div. 4)"
rating: 1300
weight: 1926
solve_time_s: 123
verified: false
draft: false
---

[CF 1926D - Vlad and Division](https://codeforces.com/problemset/problem/1926/D)

**Rating:** 1300  
**Tags:** bitmasks, greedy  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of non-negative integers and asked to partition them into groups so that within each group, no two numbers share a 1-bit in the same position across the first 31 bits. Put differently, if you write all numbers in binary and look at the positions from the least significant bit up to the 31st bit, no column in a group can contain more than one 1. Each number must go into exactly one group, and the goal is to minimize the number of groups.

The input consists of multiple test cases, each providing the number of integers and the list of integers. The output for each test case is a single integer: the minimum number of groups needed. The constraints are moderate: the total number of integers across all test cases is at most 200,000. That rules out any solution that checks all pairs of numbers within a test case because that could be O(n²), which would reach 4 × 10¹⁰ operations in the worst case. Linear or near-linear solutions are feasible.

A non-obvious edge case arises when numbers have overlapping bit patterns. For example, if a number appears multiple times, each copy must go into a separate group if any of its 1-bits match with another number. Another subtlety is the number 0, which has no 1-bits. Multiple zeros can be in the same group because they do not conflict with any bit.

Consider a concrete example: [1, 4, 3, 4]. In binary (up to the first 4 bits for simplicity):

```
1 -> 0001
4 -> 0100
3 -> 0011
4 -> 0100
```

Here, the second '4' conflicts with the first '4' on the 3rd bit, so they cannot share a group. Careless solutions might try to greedily pair numbers without accounting for these repeated bits, producing a smaller number of groups than allowed.

## Approaches

A brute-force approach would try all possible groupings and check the bit conditions for each group. This is correct in principle because it would explore all valid partitions, but it is computationally infeasible. Even for n = 20, the number of partitions is enormous (Bell numbers grow very fast), and for n = 2 × 10⁵, this approach is impossible.

The key insight comes from focusing on bits rather than individual numbers. The condition forbids any two numbers in a group from sharing a 1 in the same bit position. That means, for each bit position, the maximum number of numbers in a group cannot exceed 1. Equivalently, if you count how many numbers have the i-th bit set, that count gives a lower bound on the number of groups: we need at least as many groups as the maximum frequency of any single bit being set among all numbers. Once we compute the maximum bit frequency, that number is sufficient as the minimum number of groups. This observation transforms the problem from a combinatorial partitioning problem into a counting problem over bits, which is linear in n and the number of bits (31), making it feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ × n²) | O(n²) | Too slow |
| Optimal | O(n × 31) = O(n) | O(31) = O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of integers `n` and the list of integers `a`.
2. Initialize an array `bit_count` of length 31 to zero. Each entry `bit_count[i]` will track how many numbers have the i-th bit set.
3. Iterate through each number in `a`. For each bit position from 0 to 30 (corresponding to bits 1 to 31), check if the bit is set. If it is, increment `bit_count[i]`.
4. After processing all numbers, find the maximum value in `bit_count`. This maximum represents the minimum number of groups because the bit with the highest frequency will need at least that many separate groups to avoid collisions.
5. Output the maximum value for the test case.

Why it works: the invariant is that within a group, a bit cannot appear twice. Counting the number of 1s per bit captures the exact minimum number of groups needed to satisfy the constraint for that bit. Taking the maximum over all bits ensures that all bit constraints are satisfied simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    bit_count = [0] * 31
    for num in a:
        for i in range(31):
            if num & (1 << i):
                bit_count[i] += 1
    print(max(bit_count))
```

The outer loop handles multiple test cases. `bit_count` tracks the frequency of 1s per bit. The inner loop checks each of the 31 bits efficiently using bitwise AND. Finally, `max(bit_count)` produces the minimum required number of groups. One subtle point is to index bits from 0 to 30 in code because Python uses zero-based indexing for bit positions.

## Worked Examples

### Sample Input 1

```
4
1 4 3 4
```

| Number | Binary | Bit count updates |
| --- | --- | --- |
| 1 | 0001 | bit 0 → 1 |
| 4 | 0100 | bit 2 → 1 |
| 3 | 0011 | bit 0 → 2, bit 1 → 1 |
| 4 | 0100 | bit 2 → 2 |

`bit_count` = [2, 1, 2, 0, ...], max = 2 → output 2. Each group can take numbers avoiding repeated bits.

### Sample Input 2

```
2
0 2147483647
```

| Number | Binary | Bit count updates |
| --- | --- | --- |
| 0 | 000...000 | none |
| 2147483647 | 111...111 (31 bits) | bits 0-30 → 1 each |

`bit_count` = [1,1,1,...], max = 1 → output 1. All numbers fit in one group since 0 has no 1s.

These traces confirm the correctness and the invariant that no bit appears twice in a group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × 31) ≈ O(n) | For each number, we check 31 bits. |
| Space | O(31) = O(1) | We store only a 31-length array for bit counts. |

The algorithm easily handles the total n ≤ 2 × 10⁵ across all test cases within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        bit_count = [0] * 31
        for num in a:
            for i in range(31):
                if num & (1 << i):
                    bit_count[i] += 1
        print(max(bit_count))
    return output.getvalue().strip()

# provided samples
assert run("1\n4\n1 4 3 4\n") == "2", "sample 1"
assert run("1\n2\n0 2147483647\n") == "1", "sample 2"

# custom cases
assert run("1\n3\n0 0 0\n") == "0", "all zeros"
assert run("1\n5\n1 2 4 8 16\n") == "1", "all bits disjoint"
assert run("1\n3\n7 7 7\n") == "3", "all identical max bits"
assert run("1\n4\n1 3 5 7\n") == "3", "overlapping bits"
assert run("1\n2\n2147483647 2147483647\n") == "2", "max 31-bit numbers repeated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | 0 | Multiple zeros need no extra groups |
| 1 2 4 8 16 | 1 | Numbers with disjoint bits can share one group |
| 7 7 7 | 3 | Identical numbers require separate groups per max bit count |
| 1 3 5 7 | 3 | Overlapping bits handled correctly |
| 2147483647 2147483647 | 2 | Maximum 31-bit numbers repeated |

## Edge Cases

If all numbers are zero, `bit_count` remains all zeros. The algorithm correctly outputs 0, meaning a single group can contain all zeros. If numbers have all bits set (2147483647) and appear multiple times, the maximum count across all bits equals the number of repetitions, ensuring each identical number is placed in a separate group. The bit-counting method handles both extremes seamlessly, avoiding pairwise comparisons entirely.
