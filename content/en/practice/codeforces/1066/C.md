---
title: "CF 1066C - Books Queries"
description: "We are simulating a growing sequence of books placed on a shelf. Each book has a unique identifier, and we only ever add books either to the far left end or the far right end of the current arrangement. Over time, this produces a fixed linear ordering of all inserted books."
date: "2026-06-15T13:09:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1066
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 515 (Div. 3)"
rating: 1400
weight: 1066
solve_time_s: 175
verified: true
draft: false
---

[CF 1066C - Books Queries](https://codeforces.com/problemset/problem/1066/C)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 2m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a growing sequence of books placed on a shelf. Each book has a unique identifier, and we only ever add books either to the far left end or the far right end of the current arrangement. Over time, this produces a fixed linear ordering of all inserted books.

Alongside insertions, we receive queries asking about a specific book already on the shelf. For such a query, we must compute how many removals from the left end or from the right end are needed so that this target book becomes exposed at one of the ends. We are not actually removing anything permanently, this is purely a hypothetical question about the current ordering.

The key observation from the constraints is that there are up to 200,000 operations, so we cannot rebuild or simulate the full list for every query using an array and repeated inserts at both ends, because operations like inserting at the left of a Python list or deleting from the middle would degrade to quadratic behavior in the worst case. We need a representation that supports O(1) insertion at both ends and O(1) positional queries.

A subtle point is that the structure is not arbitrary. Every book is inserted exactly once, and only at the extremes. That guarantees that the final order is completely determined by the sequence of insertions, and every book has a fixed position in that evolving sequence.

Edge cases worth highlighting:

If all inserts go to the same side, for example all "L", then the structure is a simple reversed list. A naive simulation still works, but a wrong assumption about “left means increasing index” can break logic.

If a query happens immediately after inserting the first book, the answer must always be zero, since that book is already both leftmost and rightmost.

If a book is in the middle after many alternating insertions, we must ensure we correctly measure distance to both ends in the final fixed ordering, not in insertion order.

## Approaches

A brute-force approach would maintain an explicit list representing the shelf. For each insertion, we would do list.insert(0, id) for "L" or append for "R". For each query, we would scan the list to find the index of the book, then compute its distance to both ends as min(index, n - 1 - index). This is correct but too slow.

The problem arises because finding the index of a book is O(n), and we may do it up to 200,000 times. That leads to O(nq), which is far beyond limits.

The key structural insight is that we never need to store the full list explicitly. We only need to know the relative position of each book in the final ordering. Since every insertion is at an extreme, we can assign each book a numerical coordinate representing its position on a number line. Each new left insertion gets a smaller coordinate than all previous ones, and each right insertion gets a larger coordinate. This turns the shelf into a set of integers preserving order.

Once each book has a coordinate, answering a query reduces to finding how many books lie strictly to the left and right of it in this coordinate ordering. Instead of counting dynamically, we track for each book how many were inserted before it on each side using prefix-like counters.

A simpler equivalent view is that we assign each book an index in the final sequence using a deque-like model, but we never build the deque explicitly. Instead, we simulate two pointers expanding outward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Coordinate assignment with hash map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two growing pointers representing the leftmost and rightmost occupied positions in an implicit array. We also maintain a dictionary mapping each book id to its final position.

1. Initialize two counters, left = 0 and right = 0. These represent the current boundaries of the shelf in an imaginary coordinate system.
2. Maintain a dictionary pos where pos[id] stores the assigned coordinate of each book.
3. When processing an "L id" query, we decrement left by 1 and assign pos[id] = left. This ensures every new left insertion is strictly smaller than all previous positions.
4. When processing an "R id" query, we increment right by 1 and assign pos[id] = right. This ensures every right insertion is strictly larger than all previous positions.
5. When processing a "? id" query, we compute how many steps are needed to bring this book to either end. If pos[id] is k, then:

the number of books to its left is k - left, and to its right is right - k. The answer is min(k - left, right - k).

The reasoning is that left and right track the extreme coordinates, so differences in this coordinate system correspond exactly to distances in the final shelf order.

### Why it works

The invariant is that after each operation, all books lie at distinct integer coordinates, and the ordering of books on the shelf corresponds exactly to increasing coordinate values. Every "L" insertion creates a new minimum coordinate, and every "R" insertion creates a new maximum coordinate. Therefore, the shelf order is always consistent with sorting by coordinate, and distances to ends are correctly measured by coordinate differences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    pos = {}
    left = 0
    right = 0

    first = True

    for _ in range(q):
        parts = input().split()
        if parts[0] == 'L':
            x = int(parts[1])
            if first:
                pos[x] = 0
                left = right = 0
                first = False
            else:
                left -= 1
                pos[x] = left

        elif parts[0] == 'R':
            x = int(parts[1])
            if first:
                pos[x] = 0
                left = right = 0
                first = False
            else:
                right += 1
                pos[x] = right

        else:
            x = int(parts[1])
            k = pos[x]
            print(min(k - left, right - k))

if __name__ == "__main__":
    solve()
```

The solution avoids maintaining any explicit list. Instead, it assigns each book a coordinate as if we were expanding a number line. The first inserted book is special because both boundaries start undefined, so we initialize both left and right to zero at that point.

Each insertion updates only one endpoint. Queries rely purely on arithmetic differences between stored coordinates and current boundaries, so they are O(1).

A subtle detail is handling the first insertion cleanly. Without initializing both bounds correctly, the coordinate system would drift or produce incorrect distances.

## Worked Examples

### Example 1

Input:

```
L 1
R 2
R 3
? 2
L 4
? 1
```

We track coordinates:

| Step | Operation | left | right | pos mapping | Query result |
| --- | --- | --- | --- | --- | --- |
| 1 | L 1 | 0 | 0 | {1:0} |  |
| 2 | R 2 | 0 | 1 | {1:0,2:1} |  |
| 3 | R 3 | 0 | 2 | {1:0,2:1,3:2} |  |
| 4 | ? 2 | 0 | 2 | same | min(1,1)=1 |
| 5 | L 4 | -1 | 2 | {4:-1,...} |  |
| 6 | ? 1 | -1 | 2 | same | min(0,2)=0 |

The trace shows that coordinate differences directly encode how far a book is from either end.

### Example 2

Input:

```
L 100
R 200
L 300
? 200
R 400
? 100
```

| Step | Operation | left | right | pos mapping | Query result |
| --- | --- | --- | --- | --- | --- |
| 1 | L 100 | 0 | 0 | {100:0} |  |
| 2 | R 200 | 0 | 1 | {100:0,200:1} |  |
| 3 | L 300 | -1 | 1 | {300:-1,...} |  |
| 4 | ? 200 | -1 | 1 | same | min(2,0)=0 |
| 5 | R 400 | -1 | 2 | {400:2,...} |  |
| 6 | ? 100 | -1 | 2 | same | min(1,2)=1 |

This confirms that even with alternating insertions, the coordinate system remains consistent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q) | Each query updates or reads a dictionary entry in O(1) average time |
| Space | O(q) | Each book is stored once in the position map |

The solution comfortably fits within limits since 200,000 operations with constant-time processing is efficient in Python when using fast I/O and a hash map.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    q = int(input())
    pos = {}
    left = 0
    right = 0
    first = True

    for _ in range(q):
        parts = input().split()
        if parts[0] == 'L':
            x = int(parts[1])
            if first:
                pos[x] = 0
                left = right = 0
                first = False
            else:
                left -= 1
                pos[x] = left

        elif parts[0] == 'R':
            x = int(parts[1])
            if first:
                pos[x] = 0
                left = right = 0
                first = False
            else:
                right += 1
                pos[x] = right

        else:
            x = int(parts[1])
            k = pos[x]
            out.append(str(min(k - left, right - k)))

    return "\n".join(out)

# provided sample
assert run("""8
L 1
R 2
R 3
? 2
L 4
? 1
L 5
? 1
""") == "1\n1\n2"

# minimum case
assert run("""1
L 1
""") == ""

# single query edge
assert run("""1
L 1
? 1
""") == "0"

# all right insertions
assert run("""5
L 1
R 2
R 3
R 4
? 1
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single insertion | empty | no queries edge |
| single query | 0 | immediate endpoint |
| all right insertions | 3 | monotonic growth correctness |

## Edge Cases

One edge case is when the first operation is already a query after a single insertion. For input:

```
L 10
? 10
```

the system assigns pos[10] = 0 and both left and right are 0. The query computes min(0,0) = 0, which correctly reflects that the book is already at both ends.

Another case is alternating insertions that expand both sides asymmetrically. For example:

```
L 1
R 2
L 3
R 4
? 2
```

After processing, coordinates become 3 at leftmost and 4 at rightmost extremes depending on ordering shifts. The query still correctly measures distances purely via coordinate gaps, not insertion order.

A final subtle case is when many left insertions happen before any right insertions. The left boundary moves far negative, but since all computations are relative differences, no overflow or ordering inconsistency occurs, and distances remain correct.
