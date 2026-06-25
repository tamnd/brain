---
title: "CF 105974A - Distinct Xor Subsequences"
description: "We are given an array of integers and we consider all possible subsequences formed by choosing any subset of elements while preserving order. For each chosen subsequence, we compute the bitwise XOR of all its elements."
date: "2026-06-25T13:33:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105974
codeforces_index: "A"
codeforces_contest_name: "Introductory Problems: XOR Basis"
rating: 0
weight: 105974
solve_time_s: 48
verified: true
draft: false
---

[CF 105974A - Distinct Xor Subsequences](https://codeforces.com/problemset/problem/105974/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we consider all possible subsequences formed by choosing any subset of elements while preserving order. For each chosen subsequence, we compute the bitwise XOR of all its elements. The task is to determine how many distinct XOR values can be produced across all subsequences.

Although subsequences preserve order, the XOR operation itself ignores order, so what matters is which elements are selected rather than where they appear. Two different subsequences can still produce the same XOR value, and we are asked to count how many unique results are possible.

If the array length is up to around 10^5, any approach that enumerates subsequences directly is impossible. The number of subsequences is 2^n, which already exceeds any feasible computation once n is even moderately large. This immediately rules out any exponential enumeration strategy and pushes us toward a representation of the set of all subset XORs in compressed form.

A common failure case comes from trying to “track all XORs” in a set incrementally. For example, if the array is [1, 2, 3], one might simulate adding elements and updating a set of reachable XORs. This works for small n but doubles the state space at each step in the worst case. With n = 30, this already becomes borderline, and with n = 10^5 it is impossible.

Another subtle issue is duplicate elements. For instance, [5, 5] produces subsequence XORs {0, 5}. A naive implementation that treats occurrences independently without structure may overcount or miss cancellations unless it explicitly handles XOR algebra correctly.

## Approaches

The brute-force idea is straightforward: generate every subsequence, compute its XOR, and insert it into a set. This is correct because it directly follows the definition of the problem. However, the number of subsequences is 2^n, and each XOR computation costs up to O(n), so the total work is on the order of O(n · 2^n). This becomes infeasible already for n around 25.

The key observation is that XOR over subsets forms a linear structure over the binary field. Each number can be interpreted as a vector of bits, and XOR corresponds to vector addition mod 2. The set of all subset XORs is exactly the linear span of the given vectors. Instead of enumerating combinations, we only need to understand the dimension of this span.

This leads to the concept of a linear basis (also called a XOR basis). We maintain a set of independent vectors such that any array element can be represented as a XOR of some basis elements. Every time we insert a new number, we try to reduce it using previously stored basis vectors. If it cannot be reduced to zero, it becomes a new independent direction.

If the final basis has size k, then each subset XOR corresponds to choosing whether to include each basis vector or not, independently. That produces exactly 2^k distinct XOR values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 2^n) | O(2^n) | Too slow |
| Linear Basis | O(n log A) | O(1) to O(log A) | Accepted |

Here A is the maximum value in the array.

## Algorithm Walkthrough

1. Initialize an empty XOR basis structure where each position corresponds to a bit from high to low. This structure will store at most one vector per bit position.
2. Iterate through each number in the array. For the current number, attempt to reduce it using the existing basis. For each bit from highest to lowest, if that bit is set and we already have a basis vector for that bit, XOR the number with that basis vector to eliminate the leading bit. This step progressively simplifies the number while preserving its representability in the span.
3. After reduction, if the number becomes zero, it means it can already be formed from existing basis elements, so it does not increase the dimensionality of the space.
4. If the number is not zero, find its highest set bit and insert it into the basis at that position. This expands the independent set of vectors.
5. After processing all numbers, count how many basis vectors were inserted. Let this count be k.
6. The answer is 2^k, representing all possible XOR combinations of independent directions.

### Why it works

The basis maintains a set of linearly independent XOR vectors. Every inserted vector either lies in the span of existing vectors or increases the dimension by exactly one. Because XOR is addition in a vector space over GF(2), every subset XOR corresponds uniquely to a choice of basis vectors. The number of reachable XOR values is therefore exactly the number of elements in the span, which is 2 raised to its dimension.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    B = [0] * 60  # basis for bits up to 2^59
    rank = 0

    for x in arr:
        v = x
        for b in range(59, -1, -1):
            if (v >> b) & 1:
                if B[b]:
                    v ^= B[b]
                else:
                    B[b] = v
                    rank += 1
                    break

    # number of distinct XOR subsets
    print(1 << rank)

if __name__ == "__main__":
    solve()
```

The solution maintains a fixed-size array `B` where each entry stores a representative vector whose highest bit is at that position. This guarantees that every new insertion either cancels itself out or introduces a new independent direction. The variable `rank` tracks how many such independent directions have been discovered.

The final shift operation `1 << rank` computes 2^rank efficiently. Since rank is at most 60 for standard 64-bit integers, this is safe.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

We process each number and maintain basis vectors.

| Step | x | Reduced x | Basis changes | Rank |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | add 1 | 1 |
| 2 | 2 | 2 | add 2 | 2 |
| 3 | 3 | 0 | no change | 2 |

The third value reduces to zero because 3 = 1 XOR 2. This confirms that it does not increase dimensionality. The final rank is 2, so the number of distinct XORs is 2^2 = 4.

### Example 2

Input:

```
4
5 5 5 5
```

| Step | x | Reduced x | Basis changes | Rank |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | add 5 | 1 |
| 2 | 5 | 0 | no change | 1 |
| 3 | 5 | 0 | no change | 1 |
| 4 | 5 | 0 | no change | 1 |

All repeated elements collapse into zero after the first insertion. Only one independent vector exists, so the answer is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each number is reduced across at most 60 bit positions |
| Space | O(1) | Fixed-size basis array of constant length |

The constraints allow up to 10^5 elements, and each element is processed in at most 60 steps, giving roughly 6 million bit operations, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    B = [0] * 60
    rank = 0

    for x in arr:
        v = x
        for b in range(59, -1, -1):
            if (v >> b) & 1:
                if B[b]:
                    v ^= B[b]
                else:
                    B[b] = v
                    rank += 1
                    break

    return str(1 << rank)

# small cases
assert run("1\n0") == "1"
assert run("2\n1 1") == "2"
assert run("3\n1 2 3") == "4"

# all equal
assert run("5\n7 7 7 7 7") == "2"

# powers of two
assert run("3\n1 2 4") == "8"

# mixed
assert run("4\n1 2 4 7") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element zero | 1 | empty span case |
| duplicates | 2 | cancellation handling |
| independent powers | 8 | full rank growth |
| mixed XOR structure | 8 | basis correctness |

## Edge Cases

A single zero element input such as [0] should produce exactly one distinct XOR value, because the only subsequences are empty and [0], both yielding zero. The algorithm treats zero as immediately reducible and does not increase rank, so the result is 2^0 = 1.

An array where every element is identical, for example [9, 9, 9], also produces only two distinct XORs: zero and the value itself. The first insertion establishes one basis vector, and every subsequent identical value reduces to zero under that basis, preserving rank 1 and producing 2^1 = 2.

A full-rank construction such as [1, 2, 4, 8] ensures that every number becomes an independent basis vector. Each insertion increases rank by one, and the final result 2^4 = 16 matches the fact that all subset XORs are distinct.
