---
title: "CF 1140A - Detective Book"
description: "Ivan’s detective book is structured such that each page introduces a mystery, and the solution to that mystery is revealed on a later page. Concretely, we have a list of integers where the $i$-th integer $ai$ tells us the page that resolves the mystery introduced on page $i$."
date: "2026-06-12T03:45:51+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1140
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 62 (Rated for Div. 2)"
rating: 1000
weight: 1140
solve_time_s: 81
verified: true
draft: false
---

[CF 1140A - Detective Book](https://codeforces.com/problemset/problem/1140/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

Ivan’s detective book is structured such that each page introduces a mystery, and the solution to that mystery is revealed on a later page. Concretely, we have a list of integers where the $i$-th integer $a_i$ tells us the page that resolves the mystery introduced on page $i$. Ivan reads sequentially, starting from the first unread page each day, but he cannot stop in the middle of a “mystery chain.” He reads until every mystery he has encountered has been resolved. The task is to determine how many days it takes him to finish the book.

The input is small enough that $n$ can go up to $10^4$, so algorithms up to $O(n)$ or $O(n \log n)$ will run comfortably within the 2-second time limit. Quadratic algorithms that repeatedly traverse the book in full could reach $10^8$ operations, which risks timing out.

Edge cases can be subtle. For instance, if all mysteries are explained immediately on the same page, Ivan reads one page per day. For $n=5$ with $a = [1,2,3,4,5]$, each day is a single page, producing 5 days. A careless approach that assumes Ivan always reads multiple pages per day would produce a wrong answer here. Another tricky case is when the last page explains all previous mysteries, e.g., $a = [5,5,5,5,5]$; Ivan must read all five pages in one day.

## Approaches

The brute-force approach simulates Ivan’s reading explicitly. Start at page 1 and keep reading sequentially, stopping only when every mystery encountered is resolved. Count each stopping point as a new day. This method is correct because it directly follows the reading rules, but it can be inefficient if implemented naively with repeated checks for unresolved mysteries. The worst-case complexity can reach $O(n^2)$ when each page references a faraway page, since each day may require scanning from the start of the unread pages to check all previous mysteries.

The key observation for an optimal approach is that for each day, Ivan will read from the first unread page until the farthest page required by any mystery in that day. Formally, while iterating through pages in order, maintain the farthest page $max_page$ that needs to be read to resolve all mysteries encountered so far. Ivan stops when the current page index exceeds $max_page$. Increment the day count, then continue from the next unread page. This works because the stopping condition is exactly when all mysteries in the current contiguous segment are resolved. This reduces the algorithm to a single linear pass through the pages, giving $O(n)$ time complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(1) | Too slow for large n |
| Max Page Tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `days` to 0. This will count how many reading sessions Ivan has.
2. Set a pointer `i` at 0, representing the current unread page index.
3. While `i < n`:

1. Initialize `max_page` to `a[i] - 1` because we need zero-based indexing.
2. Initialize a pointer `j = i` to track pages within the current day.
3. While `j <= max_page`:

1. Update `max_page = max(max_page, a[j] - 1)`. This ensures Ivan continues reading until all mysteries for the current day are resolved.
2. Increment `j` by 1.
4. Increment `days` by 1 since Ivan has finished one day’s reading.
5. Move `i` to `j`, the next unread page.
4. Print `days`.

Why it works: the algorithm maintains the invariant that `max_page` is always the furthest page Ivan must read to resolve all mysteries he has encountered so far. By extending `max_page` whenever a later page requires reading further, the algorithm ensures no unresolved mystery is left at the end of the day. Each page is visited exactly once, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

days = 0
i = 0
while i < n:
    max_page = a[i] - 1
    j = i
    while j <= max_page:
        max_page = max(max_page, a[j] - 1)
        j += 1
    days += 1
    i = j

print(days)
```

The outer loop advances the start of the next day, while the inner loop stretches to the farthest unresolved mystery. Subtle points include adjusting `a[i]` to zero-based indexing and updating `max_page` before incrementing `j`.

## Worked Examples

**Sample Input 1:**

```
9
1 3 3 6 7 6 8 8 9
```

| i | j | max_page | Action |
| --- | --- | --- | --- |
| 0 | 0 | 0 | read page 1, max_page = 0, stop day, days=1 |
| 1 | 1 | 2 | read pages 2,3; max_page updates to 2; j=3, stop day, days=2 |
| 3 | 3 | 7 | read pages 4-8, max_page extends to 7; j=8, stop day, days=3 |
| 8 | 8 | 8 | read page 9, max_page=8, j=9, stop day, days=4 |

The trace shows the algorithm correctly extends reading to include all unresolved mysteries per day.

**Edge Case Input:**

```
5
5 5 5 5 5
```

| i | j | max_page | Action |
| --- | --- | --- | --- |
| 0 | 0 | 4 | read pages 1-5, extend max_page to 4, j=5, stop day, days=1 |

All pages are read in one day because the last page resolves all mysteries. The algorithm correctly captures this.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each page is processed exactly once. The inner while loop only progresses j forward, never revisiting pages. |
| Space | O(n) | Storing the array `a`. Extra variables use O(1) space. |

With n up to 10^4, O(n) operations are well within the 2-second limit, and memory usage stays below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    days = 0
    i = 0
    while i < n:
        max_page = a[i] - 1
        j = i
        while j <= max_page:
            max_page = max(max_page, a[j] - 1)
            j += 1
        days += 1
        i = j
    return str(days)

# Provided sample
assert run("9\n1 3 3 6 7 6 8 8 9\n") == "4", "sample 1"

# Minimum input
assert run("1\n1\n") == "1", "single page"

# All explained immediately
assert run("5\n1 2 3 4 5\n") == "5", "all pages self-explained"

# All explained at the last page
assert run("5\n5 5 5 5 5\n") == "1", "all explained on last page"

# Sequential chunks
assert run("6\n2 2 4 4 6 6\n") == "3", "two-page chains"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | single page book |
| 1 2 3 4 5 | 5 | each page explains itself, one per day |
| 5 5 5 5 5 | 1 | last page explains all, one day |
| 2 2 4 4 6 6 | 3 | chains of multiple pages correctly counted |

## Edge Cases

For the scenario where all mysteries are resolved on the same page, the algorithm correctly identifies that reading must continue until that page. With `a = [5,5,5,5,5]`, `i=0`, `j=0`, and `max_page=4`. The inner loop iterates j from 0 to 4, reading all pages in one day. The invariant `j <= max_page` ensures no day ends prematurely. Similarly, for pages that explain themselves, the algorithm handles single-page days by setting `max_page = a[i]-1`, so the day ends immediately. These traces confirm the algorithm handles both extremes correctly.
