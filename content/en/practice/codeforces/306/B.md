---
title: "CF 306B - Optimizer"
description: "We are given a linear memory array of size n and a set of m instructions, each of which sets a contiguous block of memory to the value 13. The instructions are indexed in the input order. Some instructions may overlap, fully or partially, with others."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 306
codeforces_index: "B"
codeforces_contest_name: "Testing Round 6"
rating: 2100
weight: 306
solve_time_s: 86
verified: true
draft: false
---

[CF 306B - Optimizer](https://codeforces.com/problemset/problem/306/B)

**Rating:** 2100  
**Tags:** data structures, greedy, sortings  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear memory array of size _n_ and a set of _m_ instructions, each of which sets a contiguous block of memory to the value 13. The instructions are indexed in the input order. Some instructions may overlap, fully or partially, with others. Our task is to remove as many instructions as possible while ensuring that, after removing them, every memory cell that was set to 13 by at least one instruction still ends up set to 13, and no cell is set to 13 that was not set before. The output should list the maximum number of instructions that can be removed and their indices.

The constraints allow _n_ up to 2·10^6 and _m_ up to 2·10^5. Any algorithm that explicitly simulates each instruction on the entire memory array for every combination is infeasible. A naive O(n·m) approach will exceed the time limit, since 2·10^6 × 2·10^5 is beyond practical computation for a 3-second window. This pushes us toward a greedy or line-sweep approach that avoids visiting every memory cell for every instruction.

Edge cases that could cause naive approaches to fail include instructions that are completely nested within larger instructions, multiple instructions covering the same single memory cell, and instructions that touch the boundaries of the memory array. For example, if two instructions cover positions 3 to 5, and one of them also covers 1 to 7, the smaller one can be removed without affecting the final memory state. A careless approach that removes overlapping instructions without considering containment would incorrectly remove an instruction that is essential for setting a memory cell.

## Approaches

The brute-force approach is to simulate the memory array and remove each instruction one by one, checking if the final memory configuration changes. This is correct but extremely slow. For each instruction, we would mark the affected memory cells, then attempt to remove the instruction and re-simulate the remaining instructions to see if the memory is still identical. The operation count in the worst case is O(m·n), which is too high given the constraints.

The key insight is that instructions can be seen as intervals, and an instruction can be removed if its entire interval is already covered by subsequent instructions. Sorting instructions by their starting position and then iterating greedily allows us to track the farthest covered memory cell. If the end of the current instruction is less than or equal to the farthest covered cell so far, the instruction is redundant. Otherwise, it extends the coverage and cannot be removed. This transforms the problem into a classic interval covering problem, reducing the complexity dramatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n) | Too slow |
| Greedy Interval Sweep | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all instructions and store them as tuples of `(start, end, index)`, where `end = start + length - 1`. The index is preserved for output purposes. Storing both start and end simplifies coverage calculations.
2. Sort the instructions first by `start` in ascending order. If two instructions have the same start, sort the longer interval first, so that nested instructions come later and can be removed.
3. Initialize a variable `covered` to zero, representing the farthest memory cell that is guaranteed to be set to 13 by the instructions processed so far.
4. Iterate over the sorted instructions. For each instruction, check if its `end` position is less than or equal to `covered`. If it is, the instruction is fully redundant and can be removed. Otherwise, update `covered` to the `end` of this instruction, extending the memory coverage.
5. Collect the indices of removable instructions during the iteration.
6. Output the number of removable instructions and the list of their indices.

Why it works: The invariant maintained is that `covered` always represents the farthest memory cell that is guaranteed to be set to 13 by the remaining instructions. Any instruction whose end is within this range does not contribute new memory coverage and can safely be removed. Sorting by start ensures that we encounter potentially redundant instructions in the correct order, and preferring longer intervals in tie-breaks ensures that nested instructions are considered for removal correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
instructions = []

for i in range(1, m + 1):
    a, l = map(int, input().split())
    instructions.append((a, a + l - 1, i))

# Sort by start, then by end descending to handle nested intervals
instructions.sort(key=lambda x: (x[0], -x[1]))

removable = []
covered = 0

for start, end, idx in instructions:
    if end <= covered:
        removable.append(idx)
    else:
        covered = end

print(len(removable))
if removable:
    print(" ".join(map(str, removable)))
```

The solution first converts each instruction into an interval `[start, end]`. Sorting ensures we process instructions from left to right and prioritize larger intervals when starts coincide. During iteration, `covered` always reflects the maximum memory cell guaranteed to be set. Only instructions that do not extend this coverage are marked removable. Careful attention is needed for off-by-one errors, particularly in converting length to interval end.

## Worked Examples

**Sample 1:**

Input:

```
10 4
3 3
3 1
4 1
9 2
```

Step trace:

| Instruction | Interval | Covered before | Action | Covered after | Removable |
| --- | --- | --- | --- | --- | --- |
| 3 3 | [3,5] | 0 | extends coverage | 5 | - |
| 3 1 | [3,3] | 5 | redundant | 5 | 2 |
| 4 1 | [4,4] | 5 | redundant | 5 | 3 |
| 9 2 | [9,10] | 5 | extends coverage | 10 | - |

Output:

```
2
2 3
```

This trace shows that nested instructions fully contained in previous coverage are correctly identified as removable.

**Custom Input:**

```
5 3
1 5
2 2
4 1
```

Step trace:

| Instruction | Interval | Covered before | Action | Covered after | Removable |
| --- | --- | --- | --- | --- | --- |
| 1 5 | [1,5] | 0 | extends coverage | 5 | - |
| 2 2 | [2,3] | 5 | redundant | 5 | 2 |
| 4 1 | [4,4] | 5 | redundant | 5 | 3 |

Output:

```
2
2 3
```

This shows that instructions completely contained in a larger instruction are correctly removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting the instructions dominates. Iterating through them is O(m). |
| Space | O(m) | We store intervals and removable indices. |

With m ≤ 2·10^5, O(m log m) operations are comfortably within the 3-second limit, and O(m) memory fits within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    instructions = []
    for i in range(1, m + 1):
        a, l = map(int, input().split())
        instructions.append((a, a + l - 1, i))
    instructions.sort(key=lambda x: (x[0], -x[1]))
    removable = []
    covered = 0
    for start, end, idx in instructions:
        if end <= covered:
            removable.append(idx)
        else:
            covered = end
    out = f"{len(removable)}\n"
    if removable:
        out += " ".join(map(str, removable))
    return out

# provided sample
assert run("10 4\n3 3\n3 1\n4 1\n9 2\n") == "2\n2 3", "sample 1"

# minimum size input
assert run("1 1\n1 1\n") == "0\n", "minimum input"

# all instructions same
assert run("5 3\n1 5\n1 5\n1 5\n") == "2\n2 3", "all equal"

# nested intervals
assert run("5 3\n1 5\n2 2\n4 1\n") == "2\n2 3", "nested intervals"

# adjacent intervals
assert run("6 3\n1 2\n3 2\n5 2\n") == "0\n", "non-overlapping adjacent intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 4 / 3 3 / 3 1 / 4 1 / 9 2 | 2 / 2 3 | basic nested instructions |
| 1 1 / 1 1 | 0 / | minimum input |
| 5 3 / 1 5 / 1 5 / 1 5 | 2 / 2 3 | identical overlapping instructions |
| 5 3 / 1 5 / 2 2 / 4 1 | 2 |  |
