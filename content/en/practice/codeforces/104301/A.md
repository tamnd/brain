---
title: "CF 104301A - Reading Books"
description: "We are given multiple independent scenarios. In each scenario, a reader has a sequence of reading amounts over days and a list of book lengths. Each day contributes a certain number of pages that can be used to progress through books in order."
date: "2026-07-01T20:17:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104301
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #10 (TEN-Forces)"
rating: 0
weight: 104301
solve_time_s: 281
verified: false
draft: false
---

[CF 104301A - Reading Books](https://codeforces.com/problemset/problem/104301/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple independent scenarios. In each scenario, a reader has a sequence of reading amounts over days and a list of book lengths. Each day contributes a certain number of pages that can be used to progress through books in order. Once enough pages have been accumulated to fully cover a book, that book is considered finished forever.

For each day, we must report how many books have been completely finished after processing that day’s reading progress.

The key point is that books are consumed in order, and partial progress carries over across days. The answer after each day is not independent, it depends on all previous days.

The constraints are tight. The total number of days and books across all test cases is up to $2 \cdot 10^5$. This immediately rules out any solution that recomputes progress from scratch for each day or scans the book list repeatedly. A naive simulation that checks all books per day would degrade to $O(nm)$ in the worst case, which is far beyond acceptable.

A few subtle edge cases matter. One is when a single day provides enough pages to finish multiple books at once. Another is when books are extremely small, causing rapid consumption, or extremely large, causing no progress for many days. A naive solution that only subtracts from the current book without looping correctly over multiple finished books will fail on cases like:

Input:

```
1
3 3
10 10 10
5 5 20
```

Correct behavior:

Day 1 finishes 1 book, Day 2 finishes 2 books, Day 3 finishes 3 books.

A buggy approach might stop after finishing one book per day, missing chained completions.

## Approaches

The brute-force idea is straightforward: maintain a pointer to the current book and remaining pages needed. For each day, add that day’s pages and repeatedly subtract book sizes while possible. This is correct but requires care in implementation. The worst case happens when each day finishes only one book and we repeatedly touch many entries across days, but even then each book is removed once, so total work is $O(n + m)$. However, a naive nested approach that restarts scanning from the beginning each time or repeatedly searches for the next unfinished book would become quadratic.

The key observation is that each book is finished exactly once, and once finished, it never needs to be revisited. This means we can maintain a single pointer into the book list and a running counter of accumulated pages. Each book is processed at most once across the entire test case, so amortized complexity becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation with rescanning | $O(nm)$ | $O(1)$ | Too slow |
| Two-pointer cumulative simulation | $O(n + m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain two variables: a pointer into the book array and a running sum of pages collected so far.

1. Initialize a pointer `i = 0` pointing to the first book and a variable `cur = 0` storing accumulated pages.
2. For each day in order, add the day’s reading amount to `cur`. This represents total unread pages carried forward.
3. While `cur` is large enough to fully cover the current book (`cur >= b[i]`) and we still have books left, subtract the book size from `cur` and move `i` forward. Each subtraction corresponds to finishing one book.
4. After processing all possible completions for the day, output `i`, which is the number of books fully finished so far.

The crucial idea is that the pointer only moves forward. We never revisit a book, because once its pages are subtracted, it is permanently completed.

### Why it works

At any moment, `cur` represents leftover pages that have not yet been assigned to incomplete work. Each time we finish a book, we remove exactly its page count, ensuring that `cur` always reflects remaining partial progress toward the next unfinished book. Since books are processed in order and never revisited, the pointer `i` is monotone increasing. This guarantees correctness and prevents double counting or skipping.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    i = 0
    cur = 0
    res = []
    
    for x in a:
        cur += x
        
        while i < m and cur >= b[i]:
            cur -= b[i]
            i += 1
        
        res.append(str(i))
    
    print(" ".join(res))
```

The code follows the algorithm directly. The variable `cur` accumulates pages across days. The pointer `i` tracks how many books are fully completed. The inner loop removes all books that can be completed with the current accumulated pages, ensuring chained completions are handled correctly.

A common implementation pitfall is forgetting the `while` loop and replacing it with a single `if`, which would incorrectly allow only one book per day to be completed.

## Worked Examples

### Example 1

Input:

```
n=4, m=3
a = [7, 5, 2, 1]
b = [6, 8, 9]
```

| Day | Added pages | Cur before | Book 1 | Book 2 | Book 3 | Books finished |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 7 | 6 consumed | 1 left | - | 1 |
| 2 | 5 | 6 | 8 not enough | - | - | 1 |
| 3 | 2 | 8 | 2+6 = 10 → finish book 2 | - | - | 2 |
| 4 | 1 | 1 | cannot finish | - | - | 2 |

Output:

```
1 1 2 2
```

This trace shows that leftover pages accumulate across days and are reused efficiently when they become sufficient.

### Example 2

Input:

```
n=5, m=6
a = [7, 12, 23, 15, 29]
b = [10, 9, 6, 8, 13, 1]
```

| Day | Cur after add | Books finished this day | Total |
| --- | --- | --- | --- |
| 1 | 7 | none | 0 |
| 2 | 19 | 10, 9 | 2 |
| 3 | 23 | 6, 8, 13 | 5 |
| 4 | 15 | none (partial) | 5 |
| 5 | 44 | 1 | 6 |

Output:

```
2 3 5 5 6
```

This demonstrates multiple chained completions in a single day and shows why the inner loop is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ per test case | Each book is processed exactly once by pointer `i`, and each day is processed once |
| Space | $O(1)$ extra | Only pointers and counters are used beyond input storage |

The total input size across test cases is $2 \cdot 10^5$, so linear time processing per test case aggregate is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out_lines = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        i = 0
        cur = 0
        res = []
        for x in a:
            cur += x
            while i < m and cur >= b[i]:
                cur -= b[i]
                i += 1
            res.append(str(i))
        out_lines.append(" ".join(res))
    
    return "\n".join(out_lines)

# provided sample
assert run("""2
4 3
7 5 2 1
6 8 9
5 6
7 12 23 15 29
10 9 6 8 13 1
""") == """1 1 2 2
2 3 5 6 6"""

# minimum size
assert run("""1
1 1
5
10
""") == "0"

# immediate completion chain
assert run("""1
3 3
10 10 10
5 5 5
""") == "1 2 3"

# no progress case
assert run("""1
4 2
1 1 1 1
10 10
""") == "0 0 0 0"

# large accumulation single day
assert run("""1
2 3
100
10 20 30
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum size | 0 | no books completed |
| chain completion | 1 2 3 | multiple books in one flow |
| no progress | 0s | large books block progress |
| single large day | 3 | full consumption in one step |

## Edge Cases

A key edge case is when multiple books are finished in a single day. The algorithm handles this via the `while` loop, which keeps consuming books as long as accumulated pages are sufficient. For example:

Input:

```
1
1 3
100
10 20 30
```

Execution starts with `cur = 100`. The loop removes 10, then 20, then 30, finishing all three books in one step and leaving `cur = 40`. The pointer reaches the end, so output is `3`.

Another edge case is when books are too large to ever be completed during a day. The pointer does not move, and `cur` simply accumulates. This ensures correctness without unnecessary operations, since no subtraction happens until feasibility is reached.
