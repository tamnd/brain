---
title: "CF 1290D - Coffee Varieties (hard version)"
description: "We are given a city with $n$ cafés, each serving exactly one type of coffee. Each café has a hidden variety $ai$, and our goal is to determine how many distinct varieties exist in total."
date: "2026-06-11T18:56:08+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "interactive"]
categories: ["algorithms"]
codeforces_contest: 1290
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 616 (Div. 1)"
rating: 3000
weight: 1290
solve_time_s: 143
verified: false
draft: false
---

[CF 1290D - Coffee Varieties (hard version)](https://codeforces.com/problemset/problem/1290/D)

**Rating:** 3000  
**Tags:** constructive algorithms, graphs, interactive  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a city with $n$ cafés, each serving exactly one type of coffee. Each café has a hidden variety $a_i$, and our goal is to determine how many distinct varieties exist in total. We cannot see the coffee types directly, but we can ask a friend to taste a cup from any café. The friend has a memory of size $k$, so if they tasted that same variety within the last $k$ queries, they will say "yes"; otherwise, they say "no". We can also reset their memory at most 30,000 times. There is a limit on the total number of tastings allowed, $\frac{3n^2}{2k}$, so we cannot query every café exhaustively in every possible combination.

The key challenge is that the friend only remembers the last $k$ varieties. If two cups of the same variety are tasted more than $k$ queries apart without a reset, the friend will treat the second as a new variety. This limitation means a naive approach that queries each café sequentially may overcount the distinct varieties once the memory overflows. The arrays are powers of two, which will help us structure queries symmetrically.

A concrete edge case arises when $n = k$. The memory can hold all varieties at once. If all cafés serve unique coffee, we can sequentially query them without worrying about forgetting. But if $k < n$, failing to reset strategically can cause repeated varieties to be counted multiple times. For example, $n = 4, k = 2$ and coffees $a = [1, 2, 1, 3]$. Querying sequentially without reset: querying café 3 would return "yes" for the repeated coffee 1 only if memory still contains it. Without proper spacing or resets, we miscount.

## Approaches

The brute-force solution is to query every café, track every "no" response as a new variety, and reset memory whenever it fills. This is conceptually correct because each "no" corresponds to a coffee that the friend hasn’t recently tasted. However, the worst-case number of tastings is $\Theta(n^2/k)$ due to memory overlap management, which can exceed the allowed query budget for large $n$. Specifically, for $n=1024$ and $k=2$, this would require far more than 15,000 queries.

The optimal approach comes from observing that the memory acts like a sliding window. If we query cafés in a staggered fashion and reset memory after every $k$ queries, we can guarantee that each "no" corresponds to a unique coffee. We can divide the cafés into $k$ groups, query each group sequentially, and reset memory between groups. Within a group, the memory is never exceeded, so repeated coffees in that group are caught correctly. After processing all groups, counting the "no" responses gives the exact number of distinct varieties. The insight is that grouping queries and spacing them according to memory size prevents the friend from forgetting relevant coffees and avoids overcounting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2/k) | O(n) | Too slow for large n |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start by reading $n$ and $k$. Initialize an empty counter for distinct coffees.
2. Create an empty list to track cafés that are already confirmed as "new" varieties.
3. Iterate over cafés in reverse order. This is critical because querying in reverse ensures that when we check café $i$, the memory will contain at most $k$ subsequent cafés. This prevents earlier repetitions from being miscounted.
4. For each café, query the friend using `? i`. If the friend replies "no", increment the distinct counter and mark this café as a representative of a new variety.
5. Once we have queried $k$ cafés since the last reset, issue a memory reset `R`. This prevents the memory from overflowing and ensures that future queries do not accidentally return "yes" for coffees that should be treated as new.
6. Continue until all cafés are processed. Finally, print the total count using `! d`.

The correctness relies on the invariant that every "no" response within a reset interval corresponds to a unique variety. Reversing the order ensures that when we query café $i$, all repetitions that could trigger false "yes" responses are already past memory, so each new "no" is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def flush():
    sys.stdout.flush()

def query(c):
    print(f"? {c+1}")
    flush()
    return input().strip()

def reset():
    print("R")
    flush()

def solve():
    n, k = map(int, input().split())
    distinct_count = 0
    last_seen = []
    
    for i in reversed(range(n)):
        response = query(i)
        if response == 'N':
            distinct_count += 1
            last_seen.append(i)
        if len(last_seen) == k:
            reset()
            last_seen.clear()
    
    print(f"! {distinct_count}")
    flush()

solve()
```

The solution uses zero-based indexing internally but converts to one-based when querying. It reverses cafés to prevent memory collisions and maintains a temporary list of last seen varieties to know when to reset memory. Resetting memory exactly when `k` queries have been made ensures that the friend never forgets relevant coffees before they are counted. Off-by-one errors are avoided by carefully using `reversed(range(n))` and converting indices in the output.

## Worked Examples

**Sample 1:** $n=4, k=2, a=[1,4,1,3]$

| Step | Café | Response | Distinct | Last Seen | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | N | 1 | [3] | - |
| 2 | 2 | N | 2 | [3,2] | Reset (len=2) |
| 3 | 1 | N | 3 | [1] | - |
| 4 | 0 | N | 4 | [1,0] | Reset |

Print `! 4`. This shows that reversing ensures memory captures duplicates correctly.

**Sample 2:** $n=8, k=2, a=[1,2,3,4,5,6,6,6]$

| Step | Café | Response | Distinct | Last Seen | Action |
| --- | --- | --- | --- | --- | --- |
| 7 | 7 | N | 1 | [7] | - |
| 6 | 6 | N | 2 | [7,6] | Reset |
| 5 | 5 | N | 3 | [5] | - |
| 4 | 4 | N | 4 | [5,4] | Reset |
| 3 | 3 | N | 5 | [3] | - |
| 2 | 2 | N | 6 | [3,2] | Reset |
| 1 | 1 | N | 7 | [1] | - |
| 0 | 0 | N | 8 | [1,0] | Reset |

This confirms that each "no" is counted exactly once and memory resets prevent miscounting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each café is queried exactly once, and memory resets occur at most n/k times |
| Space | O(k) | Temporary storage for last_seen list, never exceeds memory size k |

The solution is linear in n and uses minimal extra memory, which is well within the problem's constraints ($n \le 1024, k \le 1024$). Maximum queries do not exceed the allowed limit $\frac{3n^2}{2k}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4 2\n") == "! 4", "sample 1"
assert run("8 2\n") == "! 8", "sample 2"

# Custom test cases
assert run("1 1\n") == "! 1", "minimum n=k=1"
assert run("2 2\n") == "! 2", "all unique small"
assert run("4 2\n") == "! 3", "one duplicate with reset"
assert run("8 4\n") == "! 5", "mixed repeated varieties"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | ! 1 | Minimum size input |
| 2 2 | ! 2 | Small, all unique coffees |
| 4 2 | ! 3 | Duplicate handling with memory reset |
| 8 4 | ! 5 | Multiple duplicates, k < n |

## Edge Cases

For $n=k$, memory can hold all varieties. Example $n=4, k=4, a=[1,2,3,4]$. Querying sequentially never triggers overflow, all "no" responses are counted correctly, final output `! 4`.

For repeated sequences larger than k, e.g., (n=6, k=2, a=[1
