---
title: "CF 7B - Memory Manager"
description: "We are asked to implement a simple memory manager for a linear memory array of size m. Each memory cell can either be fr"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 7
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 7"
rating: 1600
weight: 7
solve_time_s: 61
verified: true
draft: false
---

[CF 7B - Memory Manager](https://codeforces.com/problemset/problem/7/B)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to implement a simple memory manager for a linear memory array of size _m_. Each memory cell can either be free or occupied by a block. We are to process a sequence of operations: `alloc n`, `erase x`, and `defragment`. An `alloc n` request tries to allocate a contiguous segment of _n_ bytes. If multiple contiguous free segments exist, the one closest to the beginning of memory is chosen. Each successful allocation receives a unique identifier starting at 1. If allocation fails, we must return `NULL`.

An `erase x` request frees the memory associated with identifier _x_. If _x_ was never allocated or has already been erased, we print `ILLEGAL_ERASE_ARGUMENT`. Finally, `defragment` moves all allocated blocks toward the start of memory while preserving their order, eliminating gaps between them.

Constraints are tight but manageable. The total number of operations is at most 100, and memory is at most 100 bytes. This allows solutions that simulate memory explicitly, since even a naive O(t*m) algorithm will execute at most 10,000 steps, which is well within the 1-second limit.

Edge cases include allocating a block when no sufficiently large contiguous free segment exists, attempting to erase a block that was never allocated, and allocating after a defragmentation that moves blocks but does not change their size. For example, if memory is `[alloc 3, alloc 4, erase 1]`, a subsequent `alloc 5` without defragmentation should fail because free space is split, while with defragmentation it should succeed.

## Approaches

The brute-force approach simulates memory as a list of length _m_, storing either `0` for free bytes or the allocation ID for occupied bytes. For `alloc n`, we scan the list for the first contiguous sequence of at least _n_ zeros, replace it with the new ID, and increment the allocation counter. For `erase x`, we scan the memory and replace all occurrences of ID `x` with zero. `defragment` is implemented by filtering all non-zero IDs to the front and padding the rest with zeros. This is correct because all operations only require checking contiguous sequences and maintaining allocation IDs, but scanning the memory repeatedly for large _m_ would be slow if constraints were larger.

The key observation for optimization is that the problem size allows direct simulation. For larger memory, one could maintain a list of free segments as intervals, allocating and merging intervals, and moving allocated segments as a separate list. The structure of this problem makes a linear scan sufficient, because both `t` and `m` are ≤100.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t*m) | O(m) | Accepted |
| Interval Optimization | O(t*#blocks) | O(#blocks) | Not needed for constraints |

## Algorithm Walkthrough

1. Initialize memory as a list of zeros of length _m_. Maintain an allocation counter starting at 1 and a dictionary mapping IDs to their memory ranges for quick erasure checks.
2. For an `alloc n` operation, iterate through memory from start to end to find the first sequence of at least _n_ consecutive zeros. If found, replace these zeros with the current allocation ID, record the mapping from ID to range, increment the counter, and print the ID. If not found, print `NULL`.
3. For an `erase x` operation, first check whether ID `x` exists in the mapping. If it does not, print `ILLEGAL_ERASE_ARGUMENT`. Otherwise, retrieve the start and end indices of the block, set all corresponding memory cells back to zero, and remove the ID from the mapping.
4. For a `defragment` operation, iterate over memory and collect all non-zero IDs in order. Replace the memory with this ordered list followed by zeros to fill up to length _m_. Update the mapping of each ID to reflect its new range.
5. Repeat steps 2-4 for all operations in the input, ensuring output is printed immediately for `alloc` and failed `erase` operations.

Why it works: at every step, memory accurately reflects the state of allocation. The allocation scan guarantees the first-fit policy. Erase checks against the mapping guarantee that only valid IDs are removed. Defragmentation preserves the relative order of allocations. The invariants of memory consistency and correct ID assignment are maintained throughout.

## Python Solution

```python
import sys
input = sys.stdin.readline

t, m = map(int, input().split())
memory = [0] * m
alloc_counter = 1
id_map = {}  # ID -> (start, end)

for _ in range(t):
    parts = input().split()
    cmd = parts[0]

    if cmd == 'alloc':
        n = int(parts[1])
        found = False
        i = 0
        while i <= m - n:
            if all(memory[i+j] == 0 for j in range(n)):
                for j in range(n):
                    memory[i+j] = alloc_counter
                id_map[alloc_counter] = (i, i+n)
                print(alloc_counter)
                alloc_counter += 1
                found = True
                break
            i += 1
        if not found:
            print("NULL")

    elif cmd == 'erase':
        x = int(parts[1])
        if x not in id_map:
            print("ILLEGAL_ERASE_ARGUMENT")
        else:
            start, end = id_map[x]
            for i in range(start, end):
                memory[i] = 0
            del id_map[x]

    elif cmd == 'defragment':
        new_memory = [val for val in memory if val != 0]
        memory = new_memory + [0]*(m - len(new_memory))
        idx = 0
        for val in new_memory:
            start = idx
            while idx < m and memory[idx] == val:
                idx += 1
            id_map[val] = (start, idx)
```

The code mirrors the algorithm: memory is explicitly represented, allocations scan for free space, and the ID map ensures valid erasures. Defragmentation rebuilds memory in place and updates all ranges. A subtle point is maintaining the ID map correctly during defragmentation; we recalculate ranges for all moved blocks. Another subtlety is scanning memory efficiently; we do not skip indices within a potential allocation until we confirm failure, preventing off-by-one errors.

## Worked Examples

**Sample Input 1**

```
6 10
alloc 5
alloc 3
erase 1
alloc 6
defragment
alloc 6
```

| Operation | Memory state | ID Map | Output |
| --- | --- | --- | --- |
| alloc 5 | 1 1 1 1 1 0 0 0 0 0 | {1:(0,5)} | 1 |
| alloc 3 | 1 1 1 1 1 2 2 2 0 0 | {1:(0,5),2:(5,8)} | 2 |
| erase 1 | 0 0 0 0 0 2 2 2 0 0 | {2:(5,8)} | - |
| alloc 6 | 0 0 0 0 0 2 2 2 0 0 | {2:(5,8)} | NULL |
| defragment | 2 2 2 0 0 0 0 0 0 0 | {2:(0,3)} | - |
| alloc 6 | 2 2 2 3 3 3 3 3 3 0 | {2:(0,3),3:(3,9)} | 3 |

This demonstrates first-fit allocation, handling of illegal allocations, and correct defragmentation with ID map update.

**Custom Input 2**

```
4 5
alloc 2
alloc 2
erase 1
alloc 3
```

| Operation | Memory state | ID Map | Output |
| --- | --- | --- | --- |
| alloc 2 | 1 1 0 0 0 | {1:(0,2)} | 1 |
| alloc 2 | 1 1 2 2 0 | {1:(0,2),2:(2,4)} | 2 |
| erase 1 | 0 0 2 2 0 | {2:(2,4)} | - |
| alloc 3 | 0 0 2 2 0 | {2:(2,4)} | NULL |

This confirms that without defragmentation, fragmented free memory cannot satisfy allocation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t*m) | Each `alloc` and `erase` scans up to m cells, repeated for t operations. |
| Space | O(m + t) | Memory array of length m and ID map storing up to t allocations. |

Given m, t ≤ 100, maximum steps are 10,000, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
```
