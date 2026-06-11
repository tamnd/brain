---
title: "CF 1136A - Nastya Is Reading a Book"
description: "The book is divided into consecutive chapters. Each chapter occupies a continuous range of pages, and every page belongs to exactly one chapter. Nastya has already read pages 1 through k - 1. Page k is the first page she has not read yet."
date: "2026-06-12T04:00:10+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1136
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 546 (Div. 2)"
rating: 800
weight: 1136
solve_time_s: 78
verified: true
draft: false
---

[CF 1136A - Nastya Is Reading a Book](https://codeforces.com/problemset/problem/1136/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The book is divided into consecutive chapters. Each chapter occupies a continuous range of pages, and every page belongs to exactly one chapter.

Nastya has already read pages `1` through `k - 1`. Page `k` is the first page she has not read yet. We need to determine how many chapters are not completely finished.

A chapter counts as unfinished in two situations. Either Nastya has not started it at all, or she stopped somewhere inside it and did not reach its last page.

The chapter ranges are given in order and do not overlap. Since the chapters cover the book consecutively, once we find the chapter that contains page `k`, every chapter from that point onward is unfinished. Any chapter before that point has already been fully read.

The constraints are very small. There are at most 100 chapters, so even a straightforward scan through all chapters is easily fast enough. We do not need any advanced data structures or searching techniques.

A subtle case occurs when `k` is exactly the first page of a chapter.

Example:

```
3
1 3
4 7
8 10
4
```

Page `4` belongs to the second chapter. The first chapter is completely read, but the second chapter has not been started. The answer is `2`, not `1`.

Another easy-to-miss case is when `k` is the last page of a chapter.

```
3
1 3
4 7
8 10
7
```

The second chapter is still unfinished because page `7` has not been read yet. The answer is `2`.

A careless solution might think that reaching the last page means the chapter is complete, but page `k` itself has not been read.

The smallest possible input also deserves attention.

```
1
1 1
1
```

The only chapter contains page `1`, which has not been read. The correct answer is `1`.

## Approaches

A brute-force interpretation would be to simulate reading page by page. We could determine which pages have been read, then examine every chapter and check whether all pages in that chapter were read. Since each chapter contains at most 100 pages and there are at most 100 chapters, this would require at most about 10,000 page checks. Even that would be accepted under these constraints.

The structure of the problem allows something much simpler.

A chapter is fully read if its last page is strictly smaller than `k`. The moment we encounter a chapter whose range contains page `k`, or whose ending page is at least `k`, that chapter is unfinished. Every later chapter is also unfinished because Nastya never reached it.

This means we only need to find the first chapter whose interval contains page `k`. If that chapter has index `i` (using zero-based indexing), then all chapters from `i` through `n - 1` are unfinished, giving an answer of `n - i`.

A single linear scan is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · pages_per_chapter) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of chapters `n`.
2. Store all chapter intervals `(l, r)`.
3. Read the page number `k`, which is the first unread page.
4. Scan the chapters from left to right.
5. For each chapter, check whether `k` lies inside its page range, meaning `l ≤ k ≤ r`.
6. As soon as such a chapter is found, output the number of remaining chapters, which is `n - current_index`.
7. Stop immediately because all later chapters are also unfinished.

### Why it works

The chapters form consecutive, non-overlapping page ranges. Since page `k` is the first unread page, every page before `k` has already been read.

Any chapter ending before `k` is completely finished. The unique chapter containing `k` is unfinished because page `k` itself has not been read. Every chapter after that one is also unfinished because Nastya never reached those pages.

Thus the answer is exactly the number of chapters starting from the chapter containing `k` through the end of the book.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

chapters = []
for _ in range(n):
    l, r = map(int, input().split())
    chapters.append((l, r))

k = int(input())

for i, (l, r) in enumerate(chapters):
    if l <= k <= r:
        print(n - i)
        break
```

The first part reads and stores the chapter ranges.

After reading `k`, the solution performs a linear scan. Since the intervals are consecutive and non-overlapping, exactly one chapter contains page `k`.

When that chapter is found at position `i`, the answer is `n - i`. This counts the current chapter plus all chapters after it.

The most common implementation mistake is an off-by-one error around page `k`. Remember that page `k` has **not** been read yet. A chapter containing `k` is still unfinished, even if `k` happens to be the chapter's last page.

## Worked Examples

### Sample 1

Input:

```
3
1 3
4 7
8 11
2
```

| Chapter Index | Range | Does it contain k=2? | Answer if found |
| --- | --- | --- | --- |
| 0 | [1, 3] | Yes | 3 - 0 = 3 |

Output:

```
3
```

Page `2` lies inside the first chapter. Since Nastya stopped during that chapter, every chapter remains unfinished.

### Sample 2

Input:

```
3
1 3
4 8
9 12
6
```

| Chapter Index | Range | Does it contain k=6? | Answer if found |
| --- | --- | --- | --- |
| 0 | [1, 3] | No | - |
| 1 | [4, 8] | Yes | 3 - 1 = 2 |

Output:

```
2
```

The first chapter ends before page `6`, so it is fully read. The second chapter contains page `6`, making it unfinished, and the third chapter has not been started.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan through the chapter list |
| Space | O(1) | Aside from storing the input intervals |

With at most 100 chapters, the linear scan performs at most 100 checks. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())

    chapters = []
    for _ in range(n):
        l, r = map(int, input().split())
        chapters.append((l, r))

    k = int(input())

    for i, (l, r) in enumerate(chapters):
        if l <= k <= r:
            return str(n - i) + "\n"

# provided sample
assert run(
"""3
1 3
4 7
8 11
2
"""
) == "3\n", "sample 1"

# minimum size
assert run(
"""1
1 1
1
"""
) == "1\n", "single chapter"

# k at first page of second chapter
assert run(
"""3
1 3
4 7
8 10
4
"""
) == "2\n", "start of chapter"

# k at last page of second chapter
assert run(
"""3
1 3
4 7
8 10
7
"""
) == "2\n", "end page still unread"

# k in final chapter
assert run(
"""4
1 2
3 4
5 6
7 8
8
"""
) == "1\n", "only last chapter remains"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One chapter, page 1 unread | 1 | Minimum-size input |
| k = first page of chapter 2 | 2 | Chapter not yet started |
| k = last page of chapter 2 | 2 | Unread boundary page |
| k in final chapter | 1 | Only one unfinished chapter remains |

## Edge Cases

Consider the case where `k` is exactly the first page of a chapter.

```
3
1 3
4 7
8 10
4
```

The scan checks `[1,3]` and moves on. The next interval `[4,7]` contains `4`, so the answer is `3 - 1 = 2`. The second chapter has not been started, so both the second and third chapters are unfinished.

Now consider `k` being the last page of a chapter.

```
3
1 3
4 7
8 10
7
```

The chapter `[4,7]` contains page `7`. Since page `7` itself has not been read, the chapter is still unfinished. The algorithm correctly returns `2`.

Finally, consider the smallest possible book.

```
1
1 1
1
```

The only chapter contains page `1`, which is the first unread page. The scan finds it immediately and returns `1`. The chapter cannot be considered finished because no pages have been read from it.
