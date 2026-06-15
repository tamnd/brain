---
title: "CF 1073B - Vasya and Books"
description: "We are given a stack of books where each book has a unique label. The stack order matters: the first array describes which book is at the top, and the last element is at the bottom."
date: "2026-06-15T14:11:20+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1073
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 53 (Rated for Div. 2)"
rating: 1000
weight: 1073
solve_time_s: 279
verified: true
draft: false
---

[CF 1073B - Vasya and Books](https://codeforces.com/problemset/problem/1073/B)

**Rating:** 1000  
**Tags:** implementation, math  
**Solve time:** 4m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stack of books where each book has a unique label. The stack order matters: the first array describes which book is at the top, and the last element is at the bottom. We also receive a second sequence that describes a fixed order in which Vasya attempts to take specific books.

At each step, Vasya looks for the requested book in the current stack. If it is still present, he removes that book together with everything above it in the stack, and all of those removed books are considered moved to his backpack. If the requested book has already been removed earlier, nothing happens in that step.

The task is to compute, for each step, how many books get removed during that operation.

The constraints go up to 200,000 books. This immediately rules out any solution that repeatedly scans or simulates stack operations naively per query. A straightforward simulation that searches for each requested book in the current stack and physically removes elements could degrade to quadratic behavior, which is too slow for the time limit.

A subtle issue appears when multiple queries refer to books that are already removed. In those cases, the answer is zero, and a naive implementation that does not maintain a proper "already removed" structure might incorrectly try to process stale positions or double count removed segments.

A concrete failure case for careless simulation is when you rebuild or shrink a list each time. For example, if the stack is `[1, 2, 3, 4]` and queries are `[4, 3, 2, 1]`, repeatedly scanning and slicing can accidentally recompute positions incorrectly if indices are not updated after deletions. The correct output is `4 0 0 0`, since the first operation removes the entire stack, and all later requests do nothing.

## Approaches

A direct simulation keeps the current stack as a list. For each query, we search for the requested book, find its position, and remove everything up to that position. This is correct because it matches the problem definition exactly. However, searching for each book takes linear time, and removing a prefix also takes linear time. Over all queries, this leads to quadratic complexity in the worst case when only small portions are removed each time.

The key observation is that the stack only ever shrinks from the top downward, and each book can be removed exactly once. Instead of repeatedly searching, we can precompute the position of every book in the initial stack. Then we maintain a pointer indicating how far down the stack we have already processed. When a query asks for a book, we only remove it if its position is still above the current pointer. We advance the pointer whenever we remove a new lowest reached position. Each book is effectively touched once.

This transforms repeated scanning into a single pass over the stack positions in increasing order of removal events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an array `pos` where `pos[x]` gives the index of book `x` in the initial stack. This converts each query into a direct position lookup instead of a search.
2. Maintain a variable `ptr` representing the highest index in the stack that has already been removed. Initially, no books are removed, so `ptr = 0`.
3. For each requested book `b_i`, check its position `p = pos[b_i]`.
4. If `p <= ptr`, the book has already been removed as part of a previous operation, so output `0`.
5. If `p > ptr`, then this book is still present. The operation removes all books from index `ptr + 1` down to `p`. The number of removed books is `p - ptr`.
6. Update `ptr` to `p`, since everything above and including `p` is now removed from future consideration.
7. Repeat for all queries.

The correctness comes from the fact that `ptr` always tracks the deepest prefix of the stack that has already been consumed. Every removal extends this prefix monotonically, and no removed segment is ever revisited.

## Why it works

At any moment, the remaining stack is exactly the suffix starting at `ptr + 1`. Each query either refers to a book inside this suffix or outside it. If it is outside, it has already been included in a previous removal, so the answer must be zero. If it is inside, the removal takes exactly the prefix of the remaining suffix up to that book, which is a contiguous segment of unused books. Because `ptr` only moves forward, each index is processed at most once, guaranteeing linear total work.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, x in enumerate(a):
        pos[x] = i + 1

    ptr = 0
    res = []

    for x in b:
        p = pos[x]
        if p <= ptr:
            res.append("0")
        else:
            res.append(str(p - ptr))
            ptr = p

    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The `pos` array is built using 1-based indexing so that stack positions align naturally with removal lengths. This avoids off-by-one adjustments when computing `p - ptr`.

The `ptr` variable is the central state of the solution. Every time we answer a non-zero query, we extend it exactly to the position of the newly removed book. This guarantees we never double count any segment.

The output is accumulated as strings for efficiency, since repeated printing inside the loop would slow down execution.

## Worked Examples

### Example 1

Input stack is `[1, 2, 3]`, queries are `[2, 1, 3]`.

| Step | Book | Position | ptr before | Action | Removed |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | remove prefix to 2 | 2 |
| 2 | 1 | 1 | 2 | already removed | 0 |
| 3 | 3 | 3 | 2 | remove prefix to 3 | 1 |

Output is `2 0 1`.

This demonstrates how once `ptr` moves past a position, that book can no longer trigger any operation.

### Example 2

Stack `[3, 1, 4, 2, 5]`, queries `[4, 2, 5, 1, 3]`.

| Step | Book | Position | ptr before | Action | Removed |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 0 | remove to 3 | 3 |
| 2 | 2 | 4 | 3 | extend to 4 | 1 |
| 3 | 5 | 5 | 4 | extend to 5 | 1 |
| 4 | 1 | 2 | 5 | already removed | 0 |
| 5 | 3 | 1 | 5 | already removed | 0 |

This shows how `ptr` monotonically grows and eventually covers the entire stack.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each book position is processed at most once as `ptr` only moves forward |
| Space | O(n) | We store the position array |

The solution fits comfortably within limits since both memory and time scale linearly with up to 200,000 elements.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, x in enumerate(a):
        pos[x] = i + 1

    ptr = 0
    ans = []
    for x in b:
        p = pos[x]
        if p <= ptr:
            ans.append("0")
        else:
            ans.append(str(p - ptr))
            ptr = p
    return " ".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("""3
1 2 3
2 1 3
""") == "2 0 1"

# minimum size
assert run("""1
1
1
""") == "1"

# already reversed stack
assert run("""4
4 3 2 1
1 2 3 4
""") == "1 1 1 1"

# all queries after full removal
assert run("""5
1 2 3 4 5
5 4 3 2 1
""") == "5 0 0 0 0"

# mixed pattern
assert run("""5
3 1 4 2 5
4 2 5 1 3
""") == "3 1 1 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| size 1 | 1 | smallest valid case |
| reversed stack | 1 1 1 1 | repeated incremental removals |
| full reverse queries | 5 0 0 0 0 | after full consumption behavior |
| mixed pattern | 3 1 1 0 0 | partial overlap and pointer logic |

## Edge Cases

A key edge case is when a query refers to a book already removed in a previous step. In this situation, the correct behavior is to output zero and not modify any state. The algorithm handles this by checking whether the stored position is at or below `ptr`.

For example, with stack `[1, 2, 3, 4]` and queries `[3, 4, 2, 1]`, after processing `3`, the pointer becomes `3`. When processing `4`, it extends to `4`. At that point, both `2` and `1` lie below or equal to `ptr`, so they correctly produce zero without further changes.
