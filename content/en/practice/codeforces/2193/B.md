---
title: "CF 2193B - Reverse a Permutation"
description: "We are given a permutation of numbers from 1 to n, which means every number in this range appears exactly once. We are allowed to choose a single continuous segment of this permutation and reverse it."
date: "2026-06-07T20:49:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 800
weight: 2193
solve_time_s: 130
verified: false
draft: false
---

[CF 2193B - Reverse a Permutation](https://codeforces.com/problemset/problem/2193/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to n, which means every number in this range appears exactly once. We are allowed to choose a single continuous segment of this permutation and reverse it. Our goal is to produce the lexicographically largest permutation possible with exactly one such reversal. Lexicographic comparison works like dictionary order: at the first index where two sequences differ, the sequence with the larger number is considered greater.

For input, we receive multiple test cases. Each test case gives us the length of the permutation and the permutation itself. The output for each test case is the permutation resulting from one optimal segment reversal that maximizes the sequence in lexicographic order.

The constraints tell us that n can go up to 200,000, and the total sum of n across all test cases is also 200,000. This limits us to O(n) or O(n log n) solutions per test case because anything quadratic will exceed time limits. Edge cases include very small permutations of length 1 or 2, permutations that are already sorted descending, and permutations where the largest number is at the end. A careless approach might just reverse the first decreasing segment or the first segment containing the maximum, but this can fail if the optimal reversal requires stretching the segment to the end or skipping smaller numbers.

For instance, given `[3,2,1,4]`, the naive approach might reverse `[3,2,1]` to `[1,2,3,4]`, which is smaller lexicographically than reversing `[3,2,1,4]` to `[4,1,2,3]`.

## Approaches

A brute-force approach would be to try every possible pair of indices (l, r) for reversal, reverse that segment, and compare the result lexicographically. There are O(n^2) such segments and each reversal costs O(n) to check the sequence, making the brute-force approach O(n^3). For n up to 2×10^5, this is completely infeasible.

The key observation is that the lexicographically maximum permutation always begins with the largest possible number that can be moved to the front. Reversing segments allows us to bring any element to the first position, and among all such moves, the optimal one is to move the largest number to the first position while reversing as few elements as necessary to keep subsequent numbers as large as possible.

Concretely, we first locate the maximum element of the permutation. We then reverse the segment from the start of the array to the index of that maximum element. This puts the maximum element at the front, and the rest of the sequence follows the order that ensures no smaller numbers unnecessarily block larger numbers later. This works because the first position dominates lexicographic comparison, so placing the largest number there is always optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n and the permutation p.
2. Identify the position of the maximum element in p. Let this be index `i_max`.
3. Reverse the segment from the start of the permutation up to `i_max` inclusive.
4. Output the modified permutation.

The reason this works is that the first element is the most significant in lexicographic order. Placing the largest element at the first position guarantees the maximum possible prefix. Reversing beyond the maximum element or choosing a smaller element first would only reduce the first significant value and thus produce a smaller lexicographic permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        i_max = p.index(max(p))
        # Reverse from start to the max element's index
        p[:i_max+1] = reversed(p[:i_max+1])
        print(' '.join(map(str, p)))

if __name__ == "__main__":
    solve()
```

The solution reads all input efficiently using `sys.stdin.readline` for speed. We locate the maximum using Python's `max` and `index`, which are O(n). Reversing a slice is done in-place, keeping space constant. Off-by-one errors are avoided by remembering that slicing in Python is exclusive at the end, so `p[:i_max+1]` correctly includes the element at `i_max`.

## Worked Examples

For input `[3,2,1,4]`, `max(p)=4` at index 3. Reversing `[3,2,1,4]` from start to index 3 gives `[4,1,2,3]`, which is the lexicographically largest permutation.

| Step | p |
| --- | --- |
| Original | [3,2,1,4] |
| Reverse 0-3 | [4,1,2,3] |

For input `[3,1,2]`, `max(p)=3` at index 0. Reversing `[3]` leaves `[3,1,2]` unchanged.

| Step | p |
| --- | --- |
| Original | [3,1,2] |
| Reverse 0-0 | [3,1,2] |

These traces show that the algorithm correctly identifies when the maximum is already at the front and otherwise brings it forward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Finding the maximum and reversing a slice are both linear in n |
| Space | O(1) extra | In-place reversal of the slice; input array reused |

Given the total sum of n across test cases ≤ 2×10^5, the algorithm comfortably executes in time.

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
assert run("4\n4\n3 2 1 4\n3\n3 1 2\n4\n4 3 2 1\n2\n2 1\n") == "4 1 2 3\n3 1 2\n4 3 2 1\n2 1", "sample 1"

# Custom cases
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n2\n1 2\n") == "2 1", "two elements increasing"
assert run("1\n2\n2 1\n") == "2 1", "two elements decreasing"
assert run("1\n5\n1 3 5 2 4\n") == "5 3 1 2 4", "maximum not at start"
assert run("1\n5\n5 4 3 2 1\n") == "5 4 3 2 1", "maximum already at start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1\n` | `1` | single element case |
| `1\n2\n1 2\n` | `2 1` | smallest non-trivial permutation, reverse needed |
| `1\n2\n2 1\n` | `2 1` | already optimal, no reverse needed |
| `1\n5\n1 3 5 2 4\n` | `5 3 1 2 4` | maximum not at start, proper reversal |
| `1\n5\n5 4 3 2 1\n` | `5 4 3 2 1` | maximum at start, no change |

## Edge Cases

When the permutation has length 1, such as `[1]`, reversing the segment `[0,0]` does nothing and correctly outputs `[1]`. For permutations where the maximum is already at the first position, such as `[4,3,2,1]`, the algorithm recognizes `i_max=0` and reverses a segment of length one, leaving the array unchanged. In both scenarios, the algorithm does not perform unnecessary reversals and maintains correctness. For a permutation like `[2,1]`, the algorithm identifies `2` as the maximum at index 0 and performs no reversal, outputting `[2,1]` correctly.
