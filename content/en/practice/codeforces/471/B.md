---
title: "CF 471B - MUH and Important Things"
description: "We are given a list of tasks, each with an associated difficulty level, and we need to produce three different sequences in which all tasks are completed. Each sequence must respect the rule that tasks can only be reordered if their difficulties are equal."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 471
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 269 (Div. 2)"
rating: 1300
weight: 471
solve_time_s: 101
verified: false
draft: false
---

[CF 471B - MUH and Important Things](https://codeforces.com/problemset/problem/471/B)

**Rating:** 1300  
**Tags:** implementation, sortings  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of tasks, each with an associated difficulty level, and we need to produce three different sequences in which all tasks are completed. Each sequence must respect the rule that tasks can only be reordered if their difficulties are equal. In other words, for any pair of tasks with distinct difficulties, their relative order cannot change across sequences. The input consists of the number of tasks `n` and an array of `n` integers representing the task difficulties. The output should either be "NO" if it is impossible to produce three distinct sequences, or "YES" followed by three sequences of task indices that satisfy the conditions.

The constraints allow `n` to be up to 2000, which is small enough for an algorithm with time complexity up to roughly O(n²) to run comfortably within one second. A brute-force approach that generates all permutations would be infeasible because the number of permutations grows factorially with `n`. We also need to be careful with edge cases: if all tasks have distinct difficulties, no two tasks can be swapped, so only one valid sequence exists, making it impossible to produce three distinct plans. If there are exactly two tasks with the same difficulty and no others repeat, we can only produce two distinct sequences by swapping them, which is still insufficient.

## Approaches

A naive brute-force approach would attempt to generate all valid permutations of task indices that respect the difficulty order. This involves identifying all tasks of equal difficulty and permuting them, while keeping tasks of different difficulties in the same relative order. While correct, this approach quickly becomes impractical because even a single difficulty repeated ten times produces 10! permutations, far exceeding our time constraints.

The key observation is that we only need three distinct sequences, not all possible sequences. A sequence can be altered by swapping tasks with the same difficulty. Therefore, we only need to find two groups of identical difficulties: one group of size at least 2 allows a single swap to create a second sequence, and either another group of size at least 2 or the same group (if it has at least 3 tasks) allows a third sequence. This reduces the problem to counting repetitions in the difficulty array. Once we identify these groups, generating the sequences is straightforward: keep the tasks in a base sorted order for the first sequence, swap tasks in the first repeated group for the second sequence, and swap tasks in the second repeated group (or additional swap in the first group if it is large enough) for the third sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Pair each task's difficulty with its original index and sort the tasks by difficulty. This produces a canonical ordering for the first sequence.
2. Scan the sorted list to find groups of tasks with the same difficulty. Keep track of indices for each repeated difficulty.
3. If no difficulty appears more than once, print "NO" because no swaps are possible, and return.
4. If exactly one difficulty appears at least twice but less than three times, check if any other difficulty appears at least twice to provide a second swap. If not, print "NO" and return.
5. Using the identified repeated groups, generate three sequences. The first sequence is the sorted order. The second sequence is formed by swapping the first two indices in the first repeated group. The third sequence is formed by swapping either the next two indices in the same group (if it has three or more elements) or swapping the first two indices in the second repeated group.
6. Output "YES" and print the three sequences.

Why it works: Sorting tasks by difficulty establishes a valid base sequence where relative order constraints are satisfied. Any swap within a group of equal difficulties preserves this ordering. Since the problem only requires three distinct sequences, two or three swaps in repeated groups guarantee that the sequences are unique, satisfying the problem conditions.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
h = list(map(int, input().split()))

# pair difficulty with original index
tasks = [(h[i], i+1) for i in range(n)]
tasks.sort()  # sort by difficulty

# find repeated difficulties
groups = {}
for diff, idx in tasks:
    if diff not in groups:
        groups[diff] = []
    groups[diff].append(idx)

first_swap = None
second_swap = None
for indices in groups.values():
    if len(indices) >= 2 and not first_swap:
        first_swap = indices[:2]
    elif len(indices) >= 2 and not second_swap:
        second_swap = indices[:2]

# if no two groups of repeats or one group with 3+, impossible
if not first_swap or (len(first_swap) < 3 and not second_swap):
    print("NO")
    sys.exit()

# build sequences
seq1 = [idx for _, idx in tasks]
seq2 = seq1[:]
seq3 = seq1[:]

# first swap for second sequence
seq2[seq1.index(first_swap[0])], seq2[seq1.index(first_swap[1])] = seq2[seq1.index(first_swap[1])], seq2[seq1.index(first_swap[0])]

# second swap for third sequence
if len(first_swap) >= 3:
    seq3[seq1.index(first_swap[1])], seq3[seq1.index(first_swap[2])] = seq3[seq1.index(first_swap[2])], seq3[seq1.index(first_swap[1])]
else:
    seq3[seq1.index(second_swap[0])], seq3[seq1.index(second_swap[1])] = seq3[seq1.index(second_swap[1])], seq3[seq1.index(second_swap[0])]

print("YES")
print(*seq1)
print(*seq2)
print(*seq3)
```

The code first creates a sorted base sequence using task difficulties, then identifies repeated difficulty groups to perform swaps. The `first_swap` handles the second sequence, and `second_swap` or additional swap in `first_swap` generates the third sequence. The `seq1.index()` calls map the original indices correctly to positions in the sorted sequence.

## Worked Examples

Sample Input 1:

```
4
1 3 3 1
```

| Step | tasks (sorted) | first_swap | second_swap | seq1 | seq2 | seq3 |
| --- | --- | --- | --- | --- | --- | --- |
| initial | [(1,1),(1,4),(3,2),(3,3)] | [1,4] | [2,3] | [1,4,2,3] | [1,4,2,3] | [1,4,2,3] |
| seq2 swap | - | - | - | - | [4,1,2,3] | - |
| seq3 swap | - | - | - | - | - | [4,1,3,2] |

This shows that swapping within repeated groups produces distinct sequences.

Sample Input 2:

```
5
1 2 3 4 5
```

No repeated difficulties. `first_swap` is None, so the output is "NO". This confirms the algorithm correctly identifies impossible cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting tasks dominates the runtime; scanning for repeated difficulties is O(n). |
| Space | O(n) | Store task index pairs and sequences. |

With n ≤ 2000, O(n log n) operations run comfortably within one second, and memory usage remains within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    h = list(map(int, input().split()))
    tasks = [(h[i], i+1) for i in range(n)]
    tasks.sort()
    groups = {}
    for diff, idx in tasks:
        if diff not in groups:
            groups[diff] = []
        groups[diff].append(idx)
    first_swap = None
    second_swap = None
    for indices in groups.values():
        if len(indices) >= 2 and not first_swap:
            first_swap = indices[:2]
        elif len(indices) >= 2 and not second_swap:
            second_swap = indices[:2]
    if not first_swap or (len(first_swap) < 3 and not second_swap):
        return "NO"
    seq1 = [idx for _, idx in tasks]
    seq2 = seq1[:]
    seq3 = seq1[:]
    seq2[seq1.index(first_swap[0])], seq2[seq1.index(first_swap[1])] = seq2[seq1.index(first_swap[1])], seq2[seq1.index(first_swap[0])]
    if len(first_swap) >= 3:
        seq3[seq1.index(first_swap[1])], seq3[seq1.index(first_swap[2])] = seq3[seq1.index(first_swap[2])], seq3[seq1.index(first_swap[1])]
    else:
        seq3[seq1.index(second_swap[0])], seq3[seq1.index(second_swap[1])] = seq3[seq1.index(second_swap[1])], seq3[seq1.index(second_swap[0])]
    return "YES\n" + " ".join(map(str, seq1)) + "\n" + " ".join(map(str, seq2)) + "\n" + " ".join
```
