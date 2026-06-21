---
title: "CF 105981C - Echoes of the Runes"
description: "We are given an array of integers and asked a very specific question about its order: whether it can be transformed into a nondecreasing sequence using at most one swap of two elements."
date: "2026-06-21T21:44:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105981
codeforces_index: "C"
codeforces_contest_name: "The 2025 Hunan University Programming Contest"
rating: 0
weight: 105981
solve_time_s: 230
verified: true
draft: false
---

[CF 105981C - Echoes of the Runes](https://codeforces.com/problemset/problem/105981/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked a very specific question about its order: whether it can be transformed into a nondecreasing sequence using at most one swap of two elements. A swap is allowed between any two positions, not necessarily adjacent, and we are allowed to choose not to swap at all if the array is already sorted.

The input represents a single sequence, and the output is a binary decision. We either confirm that the array can be made sorted with zero or one swap, or we reject it.

The constraint n ≤ 1000 is small enough that even O(n²) reasoning would pass comfortably. That already suggests that we are not expected to simulate complex transformations or perform multi-layer optimization. The structure of the task is global consistency checking rather than incremental processing.

A subtle case appears when duplicates exist. For example, in an array like `[1, 3, 2, 2, 3]`, multiple correct swaps may exist, but only one specific swap matters. A careless approach that only checks “number of inversions” would fail, because inversions do not directly encode whether a single swap can fix global ordering. The correct criterion depends on exact positional mismatches with the sorted version.

Another failure case is assuming that if there are few inversions, a swap always fixes them. For example, `[3, 1, 2]` has multiple inversions, but no single swap makes it sorted.

The real difficulty is not computational, but identifying what structure “one swap away from sorted” imposes on the permutation.

## Approaches

A brute-force approach tries every possible pair of indices i and j, swaps them, and checks whether the resulting array is sorted. This is correct because it directly follows the problem statement. However, each check costs O(n), and there are O(n²) swaps, giving O(n³) total time. With n = 1000, this reaches about 10⁹ operations, which is borderline but still too slow in Python.

We improve this by avoiding repeated simulation. The key observation is that a sorted array differs from the original only at positions where elements are misplaced relative to the sorted order. If we sort the array and compare it position by position with the original, all correct positions match, and incorrect ones mark exactly where structure breaks.

If more than two positions differ, a single swap cannot fix all mismatches because one swap can only correct exactly two positions. If exactly two positions differ, we can test whether swapping those two elements in the original array produces the sorted array.

This reduces the problem to a single comparison against the sorted version.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force swap simulation | O(n³) | O(1) | Too slow |
| Compare with sorted array | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reduce the problem by comparing the original array to its sorted form and reasoning about mismatch structure.

1. Build a sorted copy of the array. This represents the target configuration we want to reach. Sorting costs O(n log n), which is easily fast enough.
2. Compare the original array and the sorted array index by index and collect all indices where they differ. These positions represent exactly where the current ordering disagrees with a valid sorted ordering.
3. If there are zero mismatched positions, the array is already sorted, so no swap is needed.
4. If there are more than two mismatched positions, it is impossible to fix the array with a single swap because one swap can affect at most two positions in a permutation.
5. If there are exactly two mismatched positions i and j, attempt swapping a[i] and a[j] in the original array and verify whether the array becomes equal to the sorted array. If it does, the answer is positive, otherwise it is not fixable with one swap.

Why it works: a sorted array is a fixed target permutation. Any single swap modifies exactly two positions in a way that changes their values. Therefore, the set of mismatches must either be empty or consist of exactly two positions that can be corrected simultaneously by swapping those two elements. Any larger mismatch set cannot be resolved with a single transposition, because one swap cannot simultaneously repair more than two incorrect positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    b = sorted(a)
    
    diff = []
    for i in range(n):
        if a[i] != b[i]:
            diff.append(i)
    
    if len(diff) == 0:
        print("Sorted")
        return
    
    if len(diff) != 2:
        print("Failed")
        return
    
    i, j = diff
    a[i], a[j] = a[j], a[i]
    
    if a == b:
        print("Sorted")
    else:
        print("Failed")

if __name__ == "__main__":
    solve()
```

The solution constructs the sorted target and uses it as a reference for structural comparison. The diff list isolates exactly where the permutation deviates. The final swap test is necessary because having exactly two mismatches does not guarantee that swapping them fixes ordering unless their values align correctly.

## Worked Examples

Consider input `[1, 3, 2]`. The sorted array is `[1, 2, 3]`. The mismatches occur at positions 1 and 2. Swapping them produces `[1, 2, 3]`, so the output is valid.

| Step | Array | Sorted | Diff positions |
| --- | --- | --- | --- |
| Initial | 1 3 2 | 1 2 3 | [1, 2] |
| After swap | 1 2 3 | 1 2 3 | [] |

This confirms the case where a single swap fixes the permutation.

Now consider `[3, 1, 2]`. The sorted array is `[1, 2, 3]`. All positions differ, so the diff size is 3, which immediately makes it impossible.

| Step | Array | Sorted | Diff positions |
| --- | --- | --- | --- |
| Initial | 3 1 2 | 1 2 3 | [0, 1, 2] |

The algorithm rejects without attempting swaps, which matches the structural limitation of a single transposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; comparison is linear |
| Space | O(n) | Storage for sorted copy and diff list |

The constraints n ≤ 1000 make this trivial to execute within limits. Even repeated sorting across test cases would remain efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# already sorted
assert run("5\n1 2 3 4 5\n") == "Sorted"

# one swap fixes
assert run("3\n1 3 2\n") == "Sorted"

# cannot fix
assert run("3\n3 1 2\n") == "Failed"

# duplicates case
assert run("5\n1 3 2 2 3\n") == "Sorted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already sorted array | Sorted | zero swaps case |
| single correct swap | Sorted | exactly two mismatches |
| fully inconsistent order | Failed | more than two mismatches |
| array with duplicates | Sorted | correctness under equal values |

## Edge Cases

A key edge case is when the array is already sorted. For input `[1, 2, 3]`, the diff list is empty, and the algorithm immediately accepts without attempting swaps, which avoids unnecessary mutation and guarantees correctness.

Another important case is when exactly two mismatches exist but swapping them does not fix ordering due to value misalignment. For example `[1, 4, 3, 2]` sorted becomes `[1, 2, 3, 4]`. The diff indices are three positions, so it is rejected immediately, avoiding a misleading partial fix attempt.

Duplicates do not break the logic because comparison is value-based rather than index-based. Even if multiple valid sorted permutations exist, the sorted array provides a canonical target, and mismatch detection remains stable.
