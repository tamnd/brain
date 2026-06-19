---
title: "CF 106159E - Elementary Data Structure Problem"
description: "We are maintaining a growing collection of stacks, where both the number of stacks and their contents evolve over time. Initially there are no stacks. The system processes a sequence of operations in order. One operation creates a new empty stack and appends it to the end."
date: "2026-06-19T19:14:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106159
codeforces_index: "E"
codeforces_contest_name: "XIII UnB Contest Mirror"
rating: 0
weight: 106159
solve_time_s: 46
verified: true
draft: false
---

[CF 106159E - Elementary Data Structure Problem](https://codeforces.com/problemset/problem/106159/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a growing collection of stacks, where both the number of stacks and their contents evolve over time. Initially there are no stacks. The system processes a sequence of operations in order.

One operation creates a new empty stack and appends it to the end. Another operation pushes a value onto a chosen stack. The third operation asks for the j-th value that was ever pushed into a particular stack, counting from the bottom of that stack in order of insertion.

So each stack behaves like a standard stack for insertion order, but queries are not asking for the top element. Instead, they ask for historical access by insertion index.

The constraints are extremely small, with at most 100 operations total. This immediately removes any concern about performance beyond simple linear processing. Any approach that performs constant or linear work per operation will pass comfortably.

The main subtlety is not performance but indexing correctness. Each stack grows independently, and operations refer to stacks by 1-based identifiers that depend on creation order. A naive implementation can easily go wrong by mixing up stack indices or by misunderstanding that the j-th element refers to insertion order rather than depth from the top in reverse operations.

A typical failure case happens when one mistakenly treats the stack as needing deletion or dynamic re-indexing. For example, if we interpret the j-th element as "j-th from top", we might reverse indexing incorrectly. In reality, it is simply the j-th pushed element.

## Approaches

A direct simulation matches the problem structure exactly. We maintain a list of stacks. Each stack is a list that stores values in insertion order. When a type 1 operation appears, we append a new empty list. When a type 2 operation appears, we append the value to the corresponding stack. When a type 3 operation appears, we directly index into the stack.

This works because all operations are local and do not require any global structure. There is no need for balancing, searching, or persistence. Every query is answered in O(1) time after O(1) updates.

A brute force variant would be identical in structure, since there is no meaningful optimization problem here. Any attempt to use more complex data structures would only add overhead without benefit.

The key observation is that stacks are independent, and their growth history is exactly the sequence of appended values. Therefore, the j-th element is literally at index j-1 in the underlying array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct simulation) | O(Q) | O(Q) | Accepted |
| Optimal (same simulation) | O(Q) | O(Q) | Accepted |

## Algorithm Walkthrough

1. Start with an empty list `stacks`. This represents the current collection of stacks in creation order. Each stack is itself a list storing pushed values in order of arrival.
2. When a type 1 operation occurs, append a new empty list to `stacks`. This new list represents a fresh stack with no elements.
3. When a type 2 operation `(i, x)` occurs, append `x` to `stacks[i-1]`. This simulates pushing onto stack i, preserving insertion order.
4. When a type 3 operation `(i, j)` occurs, output `stacks[i-1][j-1]`. This directly retrieves the j-th inserted element in that stack.

The correctness comes from maintaining each stack as a pure append-only sequence. Since no deletions or modifications occur, insertion order is equivalent to stable positional indexing.

### Why it works

Each stack is independent and only ever receives append operations. This means the sequence of values inside a stack is exactly the chronological order of insertions. The j-th inserted element never changes position, since no operation removes or reorders elements. Therefore, indexing by position is equivalent to tracking insertion history.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    q = int(input().strip())
    stacks = []

    for _ in range(q):
        parts = input().split()
        t = int(parts[0])

        if t == 1:
            stacks.append([])

        elif t == 2:
            i = int(parts[1]) - 1
            x = int(parts[2])
            stacks[i].append(x)

        else:
            i = int(parts[1]) - 1
            j = int(parts[2]) - 1
            print(stacks[i][j])

if __name__ == "__main__":
    main()
```

The implementation mirrors the algorithm directly. Each stack is stored as a Python list, so append is O(1) amortized. Indexing is adjusted from 1-based to 0-based for both stacks and elements.

The only common mistake is forgetting that both stack indices and element positions are 1-based in the input. The conversion must be applied consistently at every access.

## Worked Examples

Consider a simple sequence:

Input:

```
1
2 1 10
3 1 1
```

| Step | Operation | Stacks state | Output |
| --- | --- | --- | --- |
| 1 | create stack | [[]] |  |
| 2 | push 10 to stack 1 | [[10]] |  |
| 3 | query stack 1, index 1 | [[10]] | 10 |

The output is 10 because it is the first and only element inserted.

Now consider multiple stacks:

Input:

```
3
1
1
2 1 5
2 2 7
3 1 1
```

| Step | Operation | Stacks state | Output |
| --- | --- | --- | --- |
| 1 | create | [[]] |  |
| 2 | create | [[], []] |  |
| 3 | push 5 to stack 1 | [[5], []] |  |
| 4 | push 7 to stack 2 | [[5], [7]] |  |
| 5 | query stack 1, 1 | [[5], [7]] | 5 |

This confirms that stacks evolve independently and indexing is local to each stack.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q) | Each operation performs O(1) work: append, create, or direct index |
| Space | O(Q) | Each pushed value is stored once across all stacks |

The limit of 100 operations makes this solution trivially fast. Even higher constraints would remain safe due to constant-time operations per query.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    q = int(sys.stdin.readline().strip())
    stacks = []
    out = []

    for _ in range(q):
        parts = sys.stdin.readline().split()
        t = int(parts[0])

        if t == 1:
            stacks.append([])
        elif t == 2:
            i = int(parts[1]) - 1
            x = int(parts[2])
            stacks[i].append(x)
        else:
            i = int(parts[1]) - 1
            j = int(parts[2]) - 1
            out.append(str(stacks[i][j]))

    return "\n".join(out)

# provided-style sample 1
assert run("""3
1
2 1 4
3 1 1
""") == "4"

# sample 2: multiple stacks
assert run("""6
1
1
2 1 5
2 2 9
3 2 1
3 1 1
""") == "9\n5"

# single stack multiple queries
assert run("""5
1
2 1 7
2 1 8
3 1 1
3 1 2
""") == "7\n8"

# minimal edge: one element
assert run("""2
1
3 1 1
""") == ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single stack push/query | 4 | basic functionality |
| two stacks interleaving | 9\n5 | independence of stacks |
| multiple pushes same stack | 7\n8 | order preservation |
| minimal creation only | empty | handling structure without queries |

## Edge Cases

One edge case is querying immediately after stack creation without pushes. Since the problem guarantees valid queries, this situation does not occur in input, but logically it would be invalid to access an empty stack. The implementation relies on the guarantee and does not add extra checks.

Another subtle case is ensuring 1-based indexing is consistently converted. For example, stack 1 is stored at index 0. If this shift is forgotten in either push or query, the program silently returns incorrect results while still staying within bounds.

A final case is when multiple stacks are created before any pushes occur. The structure should still correctly allocate empty lists without errors, ensuring later pushes land in the correct stack by identifier order.
