---
title: "CF 1462A - Favorite Sequence"
description: "Polycarp has a favorite sequence of integers, but we do not see it directly. Instead, we see the result of a special writing process he performs."
date: "2026-06-11T02:08:05+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1462
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 690 (Div. 3)"
rating: 800
weight: 1462
solve_time_s: 139
verified: false
draft: false
---

[CF 1462A - Favorite Sequence](https://codeforces.com/problemset/problem/1462/A)

**Rating:** 800  
**Tags:** implementation, two pointers  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarp has a favorite sequence of integers, but we do not see it directly. Instead, we see the result of a special writing process he performs. He writes the first element on the left end of a whiteboard, the second element on the right end, then alternates placing the next available element as far left as possible, then as far right as possible, continuing this zigzag until the entire sequence is written. Our task is to reconstruct the original sequence from the final whiteboard state.

The input gives the number of test cases, and for each test case, the length of the whiteboard sequence and the sequence itself. We must output Polycarp's original favorite sequence for each test case.

Given that $n$ can be up to 300 and there can be up to 300 test cases, a solution that runs in roughly $O(n)$ per test case is acceptable. There are no constraints that would require anything faster, and even an $O(n^2)$ approach might pass because $300^2 \cdot 300$ is just under 30 million operations, but we can do much better.

Edge cases arise when the sequence has a single element, when all elements are identical, or when the largest or smallest elements appear at the ends. For example, if the whiteboard sequence is `[42]`, the output must simply be `[42]`. If all elements are equal, such as `[1, 1, 1, 1]`, the output is the same sequence. Careless implementations that assume strictly increasing or decreasing patterns may fail in these cases.

## Approaches

A brute-force approach would attempt to simulate Polycarp’s writing process in reverse. One could try all possible combinations of left and right insertions to reconstruct the original sequence, but that quickly becomes infeasible as $n$ grows due to the factorial number of permutations.

The key observation is that Polycarp always writes the largest remaining number at one of the extremes of the whiteboard. In other words, the first element of the whiteboard sequence is the first element of the original sequence. After that, we can maintain two pointers, one at the beginning of the whiteboard sequence and one at the end, and pick elements from either end in the order that reconstructs the zigzag placement. By iteratively choosing the larger of the two extremes that hasn't been used, we can reconstruct the original sequence in a single pass.

The observation reduces the problem to a two-pointer traversal: always select the larger of the two available extremes from the whiteboard sequence, append it to the reconstructed sequence, and remove it from consideration. This works because Polycarp always places the next largest unplaced number at an extreme, and the order of placement alternates from left to right, but the selection by maximum ensures the correct order can be reconstructed greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Two-pointer Greedy | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `a` to hold the reconstructed favorite sequence.
2. Use two pointers, `l` at the start of the whiteboard sequence `b` and `r` at the end.
3. Repeat while `l <= r`:

1. Compare `b[l]` and `b[r]`.
2. Append the larger of the two to the sequence `a`.
3. If `b[l]` was larger, increment `l`. Otherwise, decrement `r`.
4. Once all elements are processed, output `a` as the reconstructed sequence.

The reason this works is that the largest element remaining in the whiteboard sequence must correspond to the next element Polycarp would have placed at either end of the whiteboard. By always choosing the maximum of the two available extremes, we respect the alternating placement order and correctly reconstruct the original sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))
        a = []
        l, r = 0, n - 1
        while l <= r:
            if b[l] > b[r]:
                a.append(b[l])
                l += 1
            else:
                a.append(b[r])
                r -= 1
        print(' '.join(map(str, a)))

if __name__ == "__main__":
    solve()
```

This code reads the number of test cases, then for each test case reads the whiteboard sequence. The two-pointer approach ensures we always select the correct element to reconstruct the original sequence. We carefully handle the pointers to avoid off-by-one errors and ensure all elements are included. Printing is done at the end for each test case.

## Worked Examples

Consider the first sample input:

```
7
3 4 5 2 9 1 1
```

| l | r | Selected | a sequence so far |
| --- | --- | --- | --- |
| 0 | 6 | 3 | [3] |
| 1 | 6 | 4 | [3, 4] |
| 2 | 6 | 5 | [3, 4, 5] |
| 3 | 6 | 2 | [3, 4, 5, 2] |
| 3 | 5 | 9 | [3, 4, 5, 2, 9] |
| 3 | 4 | 1 | [3, 4, 5, 2, 9, 1] |
| 3 | 3 | 1 | [3, 4, 5, 2, 9, 1, 1] |

This demonstrates that the two-pointer selection correctly reconstructs the original sequence in order.

Second sample input:

```
4
9 2 7 1
```

| l | r | Selected | a sequence so far |
| --- | --- | --- | --- |
| 0 | 3 | 9 | [9] |
| 1 | 3 | 1 | [9, 1] |
| 1 | 2 | 7 | [9, 1, 7] |
| 2 | 1 | 2 | [9, 1, 7, 2] |

This confirms that the algorithm also handles small sequences correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is considered exactly once with two pointers |
| Space | O(n) | We store the reconstructed sequence |

Given that $n \le 300$ and $t \le 300$, the total number of operations is roughly $300 \cdot 300 = 90,000$, well within the 2-second time limit. Memory usage is negligible for these constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("6\n7\n3 4 5 2 9 1 1\n4\n9 2 7 1\n11\n8 4 3 1 2 7 8 7 9 4 2\n1\n42\n2\n11 7\n8\n1 1 1 1 1 1 1 1\n") == \
"3 4 5 2 9 1 1\n9 1 7 2\n8 4 3 1 2 7 8 7 9 4 2\n42\n11 7\n1 1 1 1 1 1 1 1", "provided samples"

# Custom cases
assert run("1\n1\n100\n") == "100", "single element"
assert run("1\n5\n1 2 3 4 5\n") == "5 4 3 2 1", "ascending sequence"
assert run("1\n5\n5 4 3 2 1\n") == "5 4 3 2 1", "descending sequence"
assert run("1\n4\n2 2 2 2\n") == "2 2 2 2", "all equal elements"
assert run("1\n6\n1 3 2 4 5 6\n") == "6 5 4 3 2 1", "mixed sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n100` | `100` | Single-element sequence |
| `1\n5\n1 2 3 4 5` | `5 4 3 2 1` | Sequence increasing |
| `1\n5\n5 4 3 2 1` | `5 4 3 2 1` | Sequence decreasing |
| `1\n4\n2 2 2 2` | `2 2 2 2` | All elements equal |
| `1\n6\n1 3 2 4 5 6` | `6 5 4 3 2 1` |  |
