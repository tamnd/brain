---
title: "CF 264A - Escape from Stones"
description: "We start with a segment representing Liss’s current safe region, initially the interval from 0 to 1. Stones fall one after another, and each stone always lands exactly at the midpoint of Liss’s current interval."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 1200
weight: 264
solve_time_s: 65
verified: true
draft: false
---

[CF 264A - Escape from Stones](https://codeforces.com/problemset/problem/264/A)

**Rating:** 1200  
**Tags:** constructive algorithms, data structures, implementation, two pointers  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a segment representing Liss’s current safe region, initially the interval from 0 to 1. Stones fall one after another, and each stone always lands exactly at the midpoint of Liss’s current interval. After each impact, Liss reacts by discarding either the left half or the right half of her current interval, depending on the instruction character, which is either “l” or “r”.

The key hidden object in this problem is not the interval itself but the order in which the split points appear. Every time a stone falls, it introduces a new point (the midpoint at that moment). After all operations, we want to know the relative ordering of these points from left to right.

The input is a string of length n, describing a sequence of left or right decisions. The output is a permutation of numbers from 1 to n, representing the order of stone indices when their final positions are sorted on the real line.

The constraint n up to 10^6 immediately rules out any simulation that recomputes positions as floating-point intervals or maintains explicit real-valued coordinates. Any O(n log n) sorting is borderline but still acceptable, while O(n^2) interval updates or naive insertion into arrays is too slow.

A subtle issue arises from naive interval simulation using floating point numbers. Even though the process seems geometric, floating point precision will fail for n around 10^6. Two different stones can end up extremely close, and sorting them becomes unstable. Another issue is repeatedly inserting into a list representing positions, which leads to quadratic behavior.

## Approaches

A direct simulation tracks the current interval and assigns each new stone a numeric coordinate equal to the midpoint. After processing all stones, we sort by coordinates. This is conceptually correct because each stone’s position is well-defined by the recursive halving process. However, computing exact coordinates quickly becomes problematic.

At step i, the interval has size 2^{-i}, so coordinates become rational numbers with denominators growing exponentially. Storing them exactly requires big integers or fractions. Even if we use Python’s fractions, each operation adds overhead proportional to number size, leading to roughly O(n^2) behavior in practice.

The key observation is that we never need the absolute coordinates. We only need relative order. Each new stone is always inserted exactly at the midpoint of the current interval, which means it splits the current order into two parts: everything that went left stays on the left side of the new point, and everything that went right stays on the right side. This is exactly an incremental construction of a binary search tree in insertion order, where each node is inserted at the root of the current interval.

Instead of computing coordinates, we simulate ordering using a structure that maintains the current left boundary and right boundary in terms of "ranked insertion positions". A clean way to see it is that each position corresponds to a segment, and each insertion splits a segment into two. If we maintain a balanced structure of positions, each operation becomes O(1) amortized by placing the new element immediately next to a known boundary.

The most standard reduction is to maintain a linked structure using two arrays, left and right pointers, and insert each new stone between existing endpoints determined by previous decisions. The construction becomes equivalent to building a sequence where each character inserts a new index either just before or just after the current pivot.

This transforms the problem into maintaining a dynamic sequence with insertions at the current position, which is efficiently handled by keeping arrays of neighbors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (geometry + sort) | O(n log n) to O(n^2) | O(n) | Too slow / unsafe |
| Optimal (linked insertion simulation) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We interpret the process as maintaining an evolving ordered sequence of stone indices. We keep track of the current "center" position, which corresponds to the most recently inserted midpoint. Each new stone is inserted either immediately to the left or immediately to the right of the current center, depending on the instruction.

1. We initialize a sequence structure with a single element representing the first stone. This stone is placed at the center of the ordering because it is the first midpoint.
2. We maintain two arrays, left and right, that act as a doubly linked list over stone indices. Each new stone will be inserted next to the current center node.
3. We also maintain a pointer cur that tracks the most recently inserted stone, which is the current midpoint of the interval in the geometric interpretation.
4. For each next stone i from 2 to n, we read the instruction character. If it is “l”, we insert i immediately to the left of cur, updating pointers so that i becomes the new neighbor between cur’s left neighbor and cur. If it is “r”, we insert i immediately to the right of cur in the same way.
5. After insertion, we update cur to be i, because each new midpoint becomes the reference point for the next split.
6. After processing all stones, we traverse from the leftmost node using the linked structure and output indices in order.

The reason this works is that every step preserves the invariant that the linked list order matches the geometric order of midpoints induced by the interval splitting process. Each insertion corresponds exactly to splitting the current segment at its midpoint, and all earlier points remain consistently ordered relative to this split.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    if n == 0:
        return

    # arrays for doubly linked list
    left = [-1] * (n + 1)
    right = [-1] * (n + 1)

    # first stone is index 1
    cur = 1

    # start with a single node
    head = 1
    tail = 1

    for i in range(2, n + 1):
        if s[i - 2] == 'l':
            # insert i to the left of cur
            prev = left[cur]

            left[i] = prev
            right[i] = cur

            left[cur] = i

            if prev != -1:
                right[prev] = i
            else:
                head = i

        else:
            # insert i to the right of cur
            nxt = right[cur]

            right[i] = nxt
            left[i] = cur

            right[cur] = i

            if nxt != -1:
                left[nxt] = i
            else:
                tail = i

        cur = i

    # traverse from head
    res = []
    x = head
    while x != -1:
        res.append(str(x))
        x = right[x]

    sys.stdout.write("\n".join(res))

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on maintaining local adjacency updates rather than computing any geometric position. The `left` and `right` arrays encode a doubly linked list over indices. Each insertion modifies only constant many pointers, so no shifting or scanning is required.

The pointer `cur` is crucial: it represents the most recent midpoint, which is always the anchor for the next split. Updating `cur = i` after each insertion preserves the structure of the process.

Care must be taken when inserting at boundaries. If we insert to the left of the current head, we must update `head`. Similarly, inserting to the right of the tail updates `tail`. These cases correspond to extending the sequence outward.

## Worked Examples

### Example 1

Input:

```
llrlr
```

We track insertion order step by step.

| Step | i | s[i] | cur before | operation | head |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | - | - | start | 1 |
| 2 | 2 | l | 1 | insert left of 1 | 2 |
| 3 | 3 | l | 2 | insert left of 2 | 3 |
| 4 | 4 | r | 3 | insert right of 3 | 3 |
| 5 | 5 | l | 4 | insert left of 4 | 3 |

Final linked order traversal gives:

3 5 4 2 1

This matches the required output, confirming that repeated left insertions build a reversed prefix while right insertions re-anchor locally.

### Example 2

Input:

```
lrrl
```

| Step | i | s[i] | cur | operation | sequence (conceptual) |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | - | - | start | [1] |
| 2 | 2 | l | 1 | insert left | [2, 1] |
| 3 | 3 | r | 2 | insert right | [2, 3, 1] |
| 4 | 4 | r | 3 | insert right | [2, 3, 4, 1] |

Final output:

2 3 4 1

This demonstrates that right insertions extend the structure outward while preserving relative order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each stone is inserted once with O(1) pointer updates and one final traversal |
| Space | O(n) | Storage for left/right pointers for all stones |

The solution comfortably fits within limits since n can reach 10^6, and the algorithm performs only linear work with no sorting or heavy arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    old = sys.stdout
    sys.stdout = output
    try:
        solve()
    finally:
        sys.stdout = old
    return output.getvalue().strip()

# provided sample
assert run("llrlr\n") == "3\n5\n4\n2\n1"

# minimum size
assert run("l\n") == "1"

# simple right chain
assert run("rrrr\n") == "1\n2\n3\n4"

# alternating pattern
assert run("lrlr\n") == "2\n4\n3\n1"

# all left
assert run("llll\n") == "4\n3\n2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| l | 1 | minimum case |
| rrrr | 1 2 3 4 | monotone growth |
| lrlr | 2 4 3 1 | alternating structure |
| llll | 4 3 2 1 | full reversal behavior |

## Edge Cases

A single-character input like “l” or “r” never triggers any insertion logic. The algorithm returns just `[1]`, which is correct because only one stone exists and it trivially occupies the only position.

A fully left-skewed input such as “llll” repeatedly inserts each new stone to the left of the current center. Each insertion updates the head, and traversal naturally produces a reversed sequence. The linked list ensures no element is lost or overwritten, so the final order becomes 4 3 2 1 for n = 4.

A fully right-skewed input such as “rrrr” always appends to the right of the current tail. The head remains fixed at 1, and the final traversal produces 1 2 3 4, matching the intuitive idea that each new midpoint expands the interval to the right side.
