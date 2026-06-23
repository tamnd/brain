---
title: "CF 105262B - Re-Indexing"
description: "We are given a book where each chapter has two attributes: a unique title and a unique starting page number. In a correct book, the chapters would be ordered by increasing starting page number, since that represents the actual reading order."
date: "2026-06-24T02:31:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105262
codeforces_index: "B"
codeforces_contest_name: "Game of Coders 3.0"
rating: 0
weight: 105262
solve_time_s: 49
verified: true
draft: false
---

[CF 105262B - Re-Indexing](https://codeforces.com/problemset/problem/105262/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a book where each chapter has two attributes: a unique title and a unique starting page number. In a correct book, the chapters would be ordered by increasing starting page number, since that represents the actual reading order.

However, the provided table of contents is shuffled. The key point is that nothing about the chapters themselves is corrupted. Each chapter still points to the correct starting page, and all chapters are present exactly once. Only their order in the list is wrong.

For each query, we are told the title of a chapter that Eddard has just finished reading. We must determine which chapter comes immediately after it in the correct ordering by starting page. If the finished chapter is the last one in reading order, we output that there is no next chapter.

The input size is large: up to 10^5 chapters overall and up to 10^5 queries per test case. This immediately rules out any solution that scans all chapters per query. Even O(nq) would reach 10^10 operations in the worst case, which is far beyond a 1 second limit. We need preprocessing that allows each query to be answered in constant time.

A subtle edge case appears when the finished chapter is the one with the largest starting page. In that case, there is no valid successor, and we must print a special message. Another edge case is when chapters are given in completely arbitrary order, meaning we cannot assume any partial ordering from input.

## Approaches

A direct approach is to reconstruct the correct reading order for every query. For each query, we could scan all chapters, find the chapter’s page, and then scan again to find the next larger page. This works logically, because the next chapter is simply the smallest page strictly greater than the current one. However, each query would cost O(n), giving O(nq) total time, which is too slow when both n and q can be 10^5.

The key observation is that the structure never changes. The correct order is determined entirely by sorting chapters by their starting page. Once we sort them once, every chapter has a fixed successor. This transforms the problem into a mapping problem: for each chapter title, we want to know the next title in the sorted list.

We can precompute a dictionary from chapter title to its position in the sorted array. Then answering a query becomes a constant-time lookup followed by a neighbor check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal (sort + hash map) | O(n log n + n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read all chapters into a list of pairs (page, title or title, page). We store both because sorting must be done by page, but queries are by title. This separation is essential since titles are not ordered in any meaningful way.
2. Sort the list of chapters by starting page in ascending order. This reconstructs the true reading order of the book, since pages strictly define order and are unique.
3. Build a dictionary mapping each chapter title to its index in the sorted list. This allows us to jump directly from a query string to its position in the ordered sequence.
4. For each query title, retrieve its index in O(1) using the dictionary.
5. If the index is not the last position in the sorted list, output the title at index + 1. Otherwise output "No More Chapters".

The critical idea is that once ordering is fixed globally, each query becomes a local neighbor lookup rather than a search problem.

### Why it works

Sorting by page number produces the unique correct total order of chapters because page numbers are distinct and define a strict total ordering. The dictionary ensures that every chapter title is associated with exactly one position in this order. Since the successor relation in a sorted array is well-defined and stable, the answer to each query is exactly the next element in this fixed sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        chapters = []

        for _ in range(n):
            s, p = input().split()
            p = int(p)
            chapters.append((p, s))

        chapters.sort()  # sort by page

        pos = {}
        for i, (p, s) in enumerate(chapters):
            pos[s] = i

        for _ in range(q):
            c = input().strip()
            i = pos[c]
            if i == n - 1:
                out.append("No More Chapters")
            else:
                out.append(chapters[i + 1][1])

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first reconstructs the correct ordering by sorting chapters on their starting page. The dictionary `pos` is crucial because it eliminates repeated scanning during queries. Each query becomes a direct index lookup.

A common implementation mistake is forgetting to strip input strings for queries, which can lead to mismatched dictionary keys. Another is accidentally sorting by title instead of page due to tuple ordering confusion; ensuring the tuple is `(page, title)` avoids this.

## Worked Examples

### Example 1

Input:

```
3 3
Chapter2 43
Chapter3 60
Chapter1 1
Chapter1
Chapter2
Chapter3
```

Sorted chapters become:

| Step | Chapters (sorted by page) | Query | Index | Answer |
| --- | --- | --- | --- | --- |
| 1 | (1, Chapter1), (43, Chapter2), (60, Chapter3) | Chapter1 | 0 | Chapter2 |
| 2 | same | Chapter2 | 1 | Chapter3 |
| 3 | same | Chapter3 | 2 | No More Chapters |

This confirms that once ordering is fixed, answers are simple adjacency checks.

### Example 2

Input:

```
3 1
SecondChapter 4
FirstChapter 1
ThirdChapter 24
FirstChapter
```

Sorted order:

| Step | Chapters | Query | Index | Answer |
| --- | --- | --- | --- | --- |
| 1 | (1, FirstChapter), (4, SecondChapter), (24, ThirdChapter) | FirstChapter | 0 | SecondChapter |

This demonstrates that the input order is irrelevant and only page ordering matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Sorting dominates, each query is O(1) |
| Space | O(n) | Storage for chapter list and position map |

The constraints allow up to 10^5 total chapters, so an O(n log n) preprocessing step is comfortably within limits. Query handling is linear in q overall, which is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        chapters = []

        for _ in range(n):
            s, p = input().split()
            chapters.append((int(p), s))

        chapters.sort()
        pos = {s: i for i, (_, s) in enumerate(chapters)}

        for _ in range(q):
            c = input().strip()
            i = pos[c]
            if i == n - 1:
                out.append("No More Chapters")
            else:
                out.append(chapters[i + 1][1])

    return "\n".join(out)

# provided sample-like test
assert run("""1
3 3
Chapter2 43
Chapter3 60
Chapter1 1
Chapter1
Chapter2
Chapter3
""") == """Chapter2
Chapter3
No More Chapters"""

# boundary: single chapter
assert run("""1
1 2
Only 10
Only
Only
""") == """No More Chapters
No More Chapters"""

# already sorted
assert run("""1
3 2
A 1
B 2
C 3
A
B
""") == """B
C"""

# reverse order input
assert run("""1
3 2
C 3
B 2
A 1
A
C
""") == """B
No More Chapters"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single chapter | No More Chapters twice | last-element handling |
| already sorted | B, C | correctness when input is already ordered |
| reverse order | B, No More Chapters | full reordering correctness |

## Edge Cases

One edge case is when there is only one chapter. After sorting, that chapter is both first and last. The dictionary still maps it to index 0, and since `n - 1 == 0`, every query correctly returns "No More Chapters".

Another edge case is when the input order is reverse sorted by page. Sorting still restores the correct order because page numbers define a strict total order. The adjacency logic remains valid since successor is always index + 1 in the sorted array.

A final edge case is repeated queries for the same chapter. Since we do not modify any state, each query independently resolves via the same dictionary lookup, ensuring consistent output regardless of repetition.
