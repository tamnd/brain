---
title: "CF 1585D - Yet Another Sorting Problem"
description: "We are asked to determine whether an array of integers can be sorted using only operations called 3-cycles. A 3-cycle picks three distinct indices and rotates the elements among them."
date: "2026-06-10T09:29:43+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 1585
codeforces_index: "D"
codeforces_contest_name: "Technocup 2022 - Elimination Round 3"
rating: 1900
weight: 1585
solve_time_s: 90
verified: true
draft: false
---

[CF 1585D - Yet Another Sorting Problem](https://codeforces.com/problemset/problem/1585/D)

**Rating:** 1900  
**Tags:** data structures, math  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether an array of integers can be sorted using only operations called 3-cycles. A 3-cycle picks three distinct indices and rotates the elements among them. For example, if our array is `[a, b, c, d]` and we choose indices `1, 2, 3`, after the 3-cycle the array becomes `[c, a, b, d]`. The task is not to explicitly sort the array, but only to decide whether it is possible to sort it this way.

The input consists of multiple test cases. Each test case gives the size of the array and the array itself. Each integer in the array is between 1 and n. Since n can be up to 500,000 and the sum over all test cases is also 500,000, we need a linear or near-linear approach. Any solution that simulates all possible sequences of 3-cycles would be combinatorial and impossible within these constraints.

Subtle edge cases emerge from the parity of permutations. A 3-cycle is an odd permutation in the sense of permutation theory: it can be decomposed into an even number of adjacent swaps. This means that not all permutations can be sorted with 3-cycles alone. For example, `[2, 1]` is impossible because swapping two elements requires a 2-cycle, which cannot be expressed as a single 3-cycle. Arrays with repeated elements, like `[2, 2]`, are trivially sortable because swapping identical numbers has no effect and the array is already sorted.

## Approaches

The brute-force approach is to try all sequences of 3-cycles. For an array of size n, the number of 3-cycles is on the order of n³, and the number of sequences grows exponentially. This is clearly infeasible for n up to 500,000. Even trying to greedily move each element to its sorted position using a 3-cycle would be messy, because 3-cycles can only rotate three elements, and some configurations cannot be resolved by any combination.

The key insight is to look at the permutation of indices induced by sorting. If we number the positions `1..n` and consider where each element must go to achieve the sorted array, we get a permutation of positions. Then the problem reduces to a question from permutation theory: can this permutation be expressed as a product of 3-cycles? This is equivalent to asking whether the permutation is an even permutation. For arrays with distinct elements, any permutation can be expressed as a product of 3-cycles, except for simple two-element swaps. Repeated elements make it easier, because swapping identical elements effectively cancels odd parity, allowing all arrays with duplicates to be sorted.

Thus the optimal approach is:

1. Count duplicates. If there is at least one duplicate, the answer is always YES.
2. Otherwise, compute the parity of the permutation induced by sorting. If the permutation is even, it can be expressed as 3-cycles; if odd, it cannot. Return YES for even, NO for odd.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n³) | O(n) | Too slow |
| Permutation Parity | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. For each test case, read n and the array a.
2. Check if any value in a occurs more than once. If yes, immediately output YES. Repeated elements allow us to fix any odd permutation by swapping duplicates.
3. If all elements are distinct, compute the permutation needed to sort the array. This is done by pairing each element with its index, sorting the pairs by value, and recording the new positions of original indices.
4. Compute the parity of this permutation. Initialize a visited array of size n to mark which positions have been processed. For each unvisited position, follow the cycle it forms until returning to the start. Count the length of each cycle; a cycle of length k contributes k-1 transpositions. Sum over all cycles to determine the total number of transpositions.
5. If the total number of transpositions is even, output YES; otherwise output NO.

Why it works: The algorithm leverages the fact that any permutation can be decomposed into cycles. The parity of a permutation (even or odd number of transpositions) determines whether it can be expressed as a product of 3-cycles. Repeated elements allow adjustment of parity, making all arrays with duplicates sortable. By explicitly counting cycles and transpositions, we determine if sorting is feasible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if len(set(a)) < n:
            print("YES")
            continue
        
        # Compute permutation
        b = sorted((val, i) for i, val in enumerate(a))
        p = [0] * n
        for idx, (_, original_idx) in enumerate(b):
            p[original_idx] = idx
        
        # Count transpositions to compute parity
        visited = [False] * n
        transpositions = 0
        for i in range(n):
            if not visited[i]:
                cycle_len = 0
                j = i
                while not visited[j]:
                    visited[j] = True
                    j = p[j]
                    cycle_len += 1
                transpositions += cycle_len - 1
        
        print("YES" if transpositions % 2 == 0 else "NO")

if __name__ == "__main__":
    solve()
```

The solution first handles duplicates, which immediately guarantee sortability. For distinct elements, the permutation array maps the current indices to their sorted positions. By visiting each cycle in this permutation, we compute how many transpositions are needed. Each cycle of length k requires k-1 transpositions. The sum of these transpositions gives the permutation parity.

## Worked Examples

**Example 1:** `[3, 1, 2]`

| Step | i | visited | j | cycle_len | transpositions |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | [F, F, F] | 0->2->1->0 | 3 | 2 |

Total transpositions = 2 → even → YES.

**Example 2:** `[2, 1]`

| Step | i | visited | j | cycle_len | transpositions |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | [F, F] | 0->1->0 | 2 | 1 |

Total transpositions = 1 → odd → NO.

These examples show the cycle-counting method correctly determines sortability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates; cycle detection is O(n) |
| Space | O(n) | Arrays for permutation and visited flags |

This fits comfortably under the constraints: n ≤ 500,000 and sum n ≤ 500,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("7\n1\n1\n2\n2 2\n2\n2 1\n3\n1 2 3\n3\n2 1 3\n3\n3 1 2\n4\n2 1 4 3\n") == \
"YES\nYES\nNO\nYES\nNO\nYES\nYES", "sample 1"

# Custom cases
assert run("3\n2\n1 2\n3\n3 3 1\n4\n4 3 2 1\n") == "YES\nYES\nYES", "custom cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1` | NO | Odd permutation with distinct elements |
| `3 3 1` | YES | Duplicate allows correction of parity |
| `4 3 2 1` | YES | Even permutation with distinct elements |
| `1 1 1` | YES | All elements equal, trivial |

## Edge Cases

For `[2, 1]`, all elements are distinct and the permutation `(2 1)` is a single transposition, odd parity. The algorithm marks visited[0], follows cycle to 1, back to 0, calculates transpositions = 1 → outputs NO. For `[2, 2]`, a duplicate exists, so the algorithm outputs YES immediately without computing parity. This demonstrates handling of both minimum-size arrays and duplicate edge cases.
