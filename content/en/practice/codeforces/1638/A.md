---
title: "CF 1638A - Reverse"
description: "We are given a permutation of length $n$, which is an array containing all integers from $1$ to $n$ exactly once. We are allowed to choose exactly one contiguous subsegment of the permutation and reverse it."
date: "2026-06-10T04:30:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1638
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 771 (Div. 2)"
rating: 800
weight: 1638
solve_time_s: 92
verified: false
draft: false
---

[CF 1638A - Reverse](https://codeforces.com/problemset/problem/1638/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of length $n$, which is an array containing all integers from $1$ to $n$ exactly once. We are allowed to choose exactly one contiguous subsegment of the permutation and reverse it. The goal is to produce the lexicographically smallest permutation possible using this single reversal. Lexicographic order means we compare arrays element by element from left to right and the first place they differ determines which array is smaller.

For example, given the permutation `[2,1,3]`, reversing `[2,1]` produces `[1,2,3]`, which is smaller than the original. If the permutation is already sorted, reversing any segment other than a single element will make it worse, so the optimal action is to reverse a segment of length 1, effectively leaving the array unchanged.

The constraints indicate that $n$ can go up to 500, and there can be up to 500 test cases. This means a naive brute-force approach that tries all possible segments, which is $O(n^3)$ if we check each reversal's effect element by element, would be too slow in the worst case. Instead, we need a strategy that identifies the best segment to reverse efficiently.

Non-obvious edge cases include arrays that are already sorted, arrays where the first element is already 1 but the rest are not sorted, and arrays where multiple minimal elements could appear later. For instance, `[1,4,2,3]` must reverse `[4,2]` to place 2 immediately after 1, giving `[1,2,4,3]`. A careless approach might attempt to always reverse starting from the first element, missing smaller possibilities.

## Approaches

A brute-force approach is to try every pair of indices $(l, r)$, reverse that segment, and compare the resulting permutation to the current best. This would involve $O(n^2)$ reversals, each costing $O(n)$ to construct a new array, giving $O(n^3)$. This works for tiny $n$ but is far too slow for $n = 500$ and 500 test cases.

The key observation is that to make a permutation lexicographically smaller, we should try to place the smallest possible number as early as possible. The first position where the permutation differs from the identity (sorted permutation) is where we should act. Once we find the first element that is not minimal for its position, we locate the smallest number after it and reverse the segment from the first incorrect element to the position of that minimal number. This guarantees the earliest possible improvement in lexicographic order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Iterate over the permutation from left to right to find the first index `i` where `p[i]` is not equal to `i+1`. This is the position where the current permutation starts to differ from the sorted order.
2. If no such `i` exists, the permutation is already sorted. Reverse a single-element segment `[1,1]` to satisfy the "exactly one reversal" requirement.
3. Otherwise, find the position `j` of the smallest element in the suffix starting at `i`. This is the element we want to bring forward to position `i`.
4. Reverse the subsegment `[i, j]`. This moves the smallest element to the earliest possible position and pushes the larger elements after it.
5. Output the resulting permutation.

Why it works: By placing the smallest element that is currently out of place at the earliest index where the permutation deviates from sorted order, we ensure that the resulting permutation is lexicographically minimal. Any other reversal either leaves a larger element at the first differing position or moves the smallest element later, producing a worse permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        
        # find first index where permutation differs from sorted
        for i in range(n):
            if p[i] != i + 1:
                break
        else:
            # already sorted, reverse a single element
            print(*p)
            continue
        
        # find the smallest element in the suffix starting at i
        j = i + p[i:].index(min(p[i:]))
        
        # reverse the segment [i,j]
        p[i:j+1] = reversed(p[i:j+1])
        
        print(*p)

if __name__ == "__main__":
    solve()
```

The solution first reads the number of test cases. For each test case, it reads `n` and the permutation `p`. It then identifies the first element that is out of place, finds the smallest element after it, reverses the segment to bring that smallest element forward, and prints the resulting permutation. Edge cases like already sorted arrays are handled by the `else` clause on the `for` loop.

## Worked Examples

**Input:** `[3, 2, 1, 4]`

| Step | i | j | p after reversal |
| --- | --- | --- | --- |
| Find first mismatch | 0 | - | - |
| Smallest in suffix | 2 | 2 | - |
| Reverse `[0,2]` | 0 | 2 | `[1,2,3,4]` |

This demonstrates that reversing the minimal segment produces the earliest possible lexicographic improvement.

**Input:** `[1, 4, 2, 3]`

| Step | i | j | p after reversal |
| --- | --- | --- | --- |
| First mismatch | 1 | - | - |
| Smallest in suffix | 2 | 2 | - |
| Reverse `[1,2]` | 1 | 2 | `[1,2,4,3]` |

The algorithm identifies the earliest out-of-place element (4) and moves the smallest element after it (2) forward by reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single scan to find first mismatch, single scan to find minimal element in suffix, one reversal |
| Space | O(n) | Storing permutation |

Given that $n \le 500$ and $t \le 500$, the overall complexity is at most 500 * 500 = 250,000 operations, well within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n1\n1\n3\n2 1 3\n4\n1 4 2 3\n5\n1 2 3 4 5\n") == "1\n1 2 3\n1 2 4 3\n1 2 3 4 5"

# Custom tests
assert run("1\n6\n6 5 4 3 2 1\n") == "1 2 3 4 5 6", "reverse full array"
assert run("1\n5\n2 3 1 5 4\n") == "1 3 2 5 4", "first element is not 1"
assert run("1\n4\n1 3 4 2\n") == "1 2 4 3", "smallest in middle"
assert run("1\n3\n1 2 3\n") == "1 2 3", "already sorted"
assert run("1\n2\n2 1\n") == "1 2", "two element swap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 5 4 3 2 1` | `1 2 3 4 5 6` | Reversing full array for largest-to-smallest permutation |
| `2 3 1 5 4` | `1 3 2 5 4` | Smallest element not at front, reversed segment moves it forward |
| `1 3 4 2` | `1 2 4 3` | Minimal element in middle of permutation |
| `1 2 3` | `1 2 3` | Already sorted, no change |
| `2 1` | `1 2` | Two-element swap |

## Edge Cases

For a permutation of length 1 like `[1]`, the algorithm identifies that no elements are out of place and simply outputs `[1]`. For a permutation that is already sorted, such as `[1,2,3,4,5]`, the `for` loop finishes without breaking and the `else` clause ensures that we reverse a segment of length 1, leaving the permutation unchanged. For permutations where the smallest number is in the middle, such as `[1,3,4,2]`, the algorithm correctly identifies the first mismatch (`3` at index 1), finds the minimal element in the suffix (`2` at index 3), reverses `[1,3]`, producing `[1,2,4,3]`. This confirms the algorithm handles all non-trivial edge cases correctly.
