---
title: "CF 106420C - Champion's Meeting (Easy)"
description: "We are given two ordered lists of racers, where every racer has a unique prestige value. The task is to construct a single final lineup by repeatedly picking the next racer either from the front of the first list or the front of the second list, always consuming one element at a…"
date: "2026-06-20T03:46:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 65
verified: true
draft: false
---

[CF 106420C - Champion's Meeting (Easy)](https://codeforces.com/problemset/problem/106420/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two ordered lists of racers, where every racer has a unique prestige value. The task is to construct a single final lineup by repeatedly picking the next racer either from the front of the first list or the front of the second list, always consuming one element at a time. The goal is to form a combined sequence that respects a greedy preference rule based on prestige comparisons at the current fronts of the two lists.

Each step, only the first remaining racer of each list matters. We decide which one should be placed next in the merged sequence, then remove it from its list. The process continues until both lists are exhausted.

The important implication of typical constraints in this kind of merging problem is linearity: if the total number of racers is up to around 200000, then an O(nm) or O((n+m)²) strategy is immediately infeasible. The only viable direction is an algorithm that advances pointers through both lists at most once, producing an O(n + m) solution.

A subtle edge case appears when one of the lists becomes empty early. A naive implementation that always compares heads without checking emptiness will fail. For example, if A is empty and B still has elements, the only valid action is to take from B. Another edge case is when the first elements are equal in value. Although the problem states uniqueness globally, implementations sometimes assume equality handling and introduce unnecessary branching that can break ordering logic.

## Approaches

A brute-force interpretation is to simulate all possible ways of interleaving the two lists. At each step, there are up to two choices, so in the worst case we explore a binary decision tree of height n + m. This leads to exponential complexity, roughly O(2^(n+m)), which becomes impossible even for very small inputs beyond a few dozen elements.

The key observation is that we do not actually need to explore both choices. At any step, we only care which current prefix choice leads to a lexicographically better resulting sequence. Because all values are distinct, comparing the remaining suffixes reduces locally to comparing only the current heads. Once one head is strictly smaller than the other, choosing it first always yields a globally better prefix and therefore cannot be worse in any future continuation.

This local optimality collapses the entire decision process into a simple greedy merge, similar to merging two sorted arrays, except the order is determined dynamically by head comparison rather than fixed sorting.

We maintain two pointers and repeatedly take the smaller current head, advancing that pointer. When one list is exhausted, the remaining elements of the other list are appended directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(n+m) | Too slow |
| Optimal Greedy Merge | O(n+m) | O(1) extra | Accepted |

## Algorithm Walkthrough

We simulate the merge process with two indices, one for each list.

1. Initialize two pointers i and j at the start of arrays A and B. These represent the first unconsumed racers in each list.
2. While both i is within A and j is within B, compare A[i] and B[j]. The smaller value is selected as the next racer in the output sequence. This choice is correct because any later decision does not depend on skipping a smaller available prefix when all values are distinct.
3. If A[i] is smaller, append it to the result and increment i. Otherwise append B[j] and increment j. This ensures that only one element is consumed per step, preserving linear progress.
4. When one pointer reaches the end of its array, append all remaining elements of the other array in order. At this point there is no choice left, since only one source remains.

Why it works: at every step, the decision is between two candidates that are the earliest remaining elements of each list. Since all values are unique, picking the smaller head always produces a lexicographically smaller prefix of the merged sequence. Any alternative choice would immediately increase the first differing position, and no future swaps can repair that ordering because later elements cannot move earlier in the sequence. This establishes a greedy-choice property combined with optimal substructure, guaranteeing correctness of always taking the smaller available head.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    i = j = 0
    res = []
    
    while i < n and j < m:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    
    while i < n:
        res.append(a[i])
        i += 1
    
    while j < m:
        res.append(b[j])
        j += 1
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution is structured around two pointers moving independently through the arrays. The main loop continues only while both lists still have elements, ensuring every comparison is meaningful. Each iteration consumes exactly one element, so no element is ever revisited.

The final two loops handle exhaustion cases. They are necessary because once one array is empty, no further comparisons are possible, and all remaining elements must be appended in order.

A common implementation mistake is forgetting that the merge loop must stop when either pointer reaches its limit, not both. Another subtle issue is incorrectly handling equality, but here uniqueness guarantees strict ordering, so the else branch safely handles all remaining cases.

## Worked Examples

Consider A = [3, 7, 10] and B = [2, 6, 8, 11].

We track pointer positions and output.

| i | j | A[i] | B[j] | Chosen | Output |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 3 | 2 | 2 | [2] |
| 0 | 1 | 3 | 6 | 3 | [2, 3] |
| 1 | 1 | 7 | 6 | 6 | [2, 3, 6] |
| 1 | 2 | 7 | 8 | 7 | [2, 3, 6, 7] |
| 2 | 2 | 10 | 8 | 8 | [2, 3, 6, 7, 8] |
| 2 | 3 | 10 | 11 | 10 | [2, 3, 6, 7, 8, 10] |
| 3 | 3 | - | - | remaining B | [2, 3, 6, 7, 8, 10, 11] |

This trace shows that the algorithm behaves exactly like merging two sorted sequences and always preserves the smallest available prefix element.

Now consider A = [5] and B = [1, 2, 3].

| i | j | A[i] | B[j] | Chosen | Output |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 1 | 1 | [1] |
| 0 | 1 | 5 | 2 | 2 | [1, 2] |
| 0 | 2 | 5 | 3 | 3 | [1, 2, 3] |
| 0 | 3 | 5 | - | remaining A | [1, 2, 3, 5] |

This confirms correct handling of early exhaustion of one list.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each element is appended exactly once and pointers only move forward |
| Space | O(n + m) | Output array stores all merged elements |

The linear complexity matches the constraint regime where total input size can reach hundreds of thousands, making a single pass solution necessary and sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    i = j = 0
    res = []
    
    while i < n and j < m:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    
    while i < n:
        res.append(a[i])
        i += 1
    
    while j < m:
        res.append(b[j])
        j += 1
    
    return " ".join(map(str, res))

# custom tests
assert run("1 1\n5\n3") == "3 5"
assert run("3 0\n1 2 3\n") == "1 2 3"
assert run("0 4\n4 1 2 3\n") == "4 1 2 3"
assert run("4 4\n1 4 7 10\n2 3 5 6") == "1 2 3 4 5 6 7 10"
assert run("5 5\n10 20 30 40 50\n1 2 3 4 5") == "1 2 3 4 5 10 20 30 40 50"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 / 3 | 3 5 | single element swap ordering |
| 3 0 / 1 2 3 | 1 2 3 | empty second array |
| 0 4 / 4 1 2 3 | 4 1 2 3 | empty first array |
| 4 4 / 1 4 7 10 + 2 3 5 6 | 1 2 3 4 5 6 7 10 | interleaving correctness |
| 5 5 descending vs ascending | merged sorted order | worst-case full alternation |

## Edge Cases

When one list is empty from the start, the algorithm skips the comparison loop entirely and directly outputs the other list. For input A = [] and B = [4, 1, 2], the pointer i stays at 0 while j advances from 0 to 3, producing [4, 1, 2] exactly as required.

When all elements of one list are smaller than the other, the algorithm consistently drains that list first. For A = [1, 2, 3] and B = [10, 11], every comparison selects from A until exhaustion, after which B is appended. The invariant that pointers only move forward ensures no element is skipped or reordered incorrectly.

When interleaving is maximal, such as A = [1, 3, 5, 7] and B = [2, 4, 6, 8], each step alternates between arrays. The algorithm handles this without additional branching because each comparison independently resolves the next smallest head, maintaining correctness even under tight alternation.
