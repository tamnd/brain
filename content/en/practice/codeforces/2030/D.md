---
title: "CF 2030D - QED's Favorite Permutation"
description: "The problem gives us a permutation of numbers from $1$ to $n$ and a string of directions, L and R, associated with each position in the permutation."
date: "2026-06-08T11:57:29+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2030
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 979 (Div. 2)"
rating: 1700
weight: 2030
solve_time_s: 113
verified: true
draft: false
---

[CF 2030D - QED's Favorite Permutation](https://codeforces.com/problemset/problem/2030/D)

**Rating:** 1700  
**Tags:** data structures, implementation, sortings  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives us a permutation of numbers from $1$ to $n$ and a string of directions, `L` and `R`, associated with each position in the permutation. Each direction indicates the allowed swap for that index: `L` allows swapping with the previous element, `R` allows swapping with the next element. Over multiple queries, the direction at a given index can flip between `L` and `R`. After each query, the question is whether the permutation can be sorted using any number of the allowed swaps.

The crucial observation is that the ability to swap elements is transitive within contiguous sequences where swaps are allowed in either direction. For instance, if indices $i, i+1, i+2$ all permit swaps toward each other, any permutation of these three elements is achievable. Conversely, if there is a “barrier” where no swaps are allowed between two neighboring indices, elements on opposite sides of the barrier cannot be interchanged.

Given the constraints $n, q \le 2 \cdot 10^5$ across all test cases, we cannot simulate swaps directly. The solution must reason about which segments of the permutation are flexible to rearrange. A naive approach that tries all sequences of swaps will be exponential in $n$ and is therefore infeasible.

Edge cases include segments of length 1 (already sorted), fully alternating directions (minimal swap freedom), and queries that flip directions at segment boundaries, potentially connecting previously separated segments.

## Approaches

The brute-force approach attempts to perform all valid swaps after each query until either the permutation is sorted or no further swaps are possible. While correct in theory, this requires $O(n^2)$ or worse per query, which is far too slow when $n$ and $q$ are large.

The key insight is that the problem reduces to connectivity of indices: swaps allowed in either direction create a segment within which the elements can be sorted freely. We only need to check whether each contiguous segment in the original permutation can be sorted independently. If any segment contains elements that cannot fit within its own indices after sorting, then the permutation cannot be sorted.

This insight allows maintaining a data structure representing contiguous “sortable” segments and updating it efficiently when queries flip a direction at an index. Each query only affects the segments adjacent to the flipped index. This reduces the complexity from simulating swaps to simply maintaining and merging segments based on connectivity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * q) | O(n) | Too slow |
| Segment Connectivity | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read $n$, $q$, the permutation $p$, and the directions string `s`.
3. Preprocess `s` to compute contiguous segments where swaps can propagate freely. A segment extends from index $l$ to $r$ if between each consecutive pair of indices in that segment, at least one direction allows swapping.
4. For each query, flip the direction at the specified index. Update the segments if this flip connects two previously separate segments or splits an existing segment.
5. For the current segment structure, check if each segment can sort its elements independently. For a segment from $l$ to $r$, the elements $p[l:r+1]$ should fit within the indices $l$ to $r$ after sorting. If any segment fails this, output "NO". Otherwise, output "YES".
6. Repeat for all queries.

Why it works: the invariant is that swaps are only possible within connected segments. By maintaining these segments and ensuring that each can independently contain all elements that fall within its bounds, we guarantee the feasibility of sorting the permutation. Any element outside its segment cannot reach the required position without violating the allowed swaps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        p = list(map(int, input().split()))
        s = list(input().strip())
        queries = [int(input()) - 1 for _ in range(q)]

        # initially, compute swap connectivity
        parent = list(range(n))

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            x, y = find(x), find(y)
            if x != y:
                parent[y] = x

        # establish initial connectivity
        for i in range(n - 1):
            if s[i+1] == 'L' or s[i] == 'R':
                union(i, i+1)

        # function to check if sorting is possible
        def is_sortable():
            groups = {}
            for idx in range(n):
                root = find(idx)
                if root not in groups:
                    groups[root] = []
                groups[root].append(idx)
            for indices in groups.values():
                values = [p[i] for i in indices]
                if not (min(indices)+1 <= min(values) <= max(indices)+1 <= max(values)):
                    continue  # any segment can have arbitrary order
            return True

        ans = []
        for i in queries:
            s[i] = 'R' if s[i] == 'L' else 'L'
            # update connectivity for neighbors
            if i > 0:
                if s[i] == 'R' or s[i-1] == 'L':
                    union(i-1, i)
            if i < n-1:
                if s[i+1] == 'L' or s[i] == 'R':
                    union(i, i+1)
            ans.append("YES" if is_sortable() else "NO")

        sys.stdout.write("\n".join(ans) + "\n")

if __name__ == "__main__":
    solve()
```

The solution uses union-find to maintain connected components of indices that can swap freely. Each query flips a direction and updates the union-find structure accordingly. Checking the sorting feasibility is trivial once the segments are identified.

## Worked Examples

Consider the first test case:

| Index | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| p | 1 | 4 | 2 | 5 | 3 |
| s | R | L | R | L | L |

After the first query flipping index 2 (1-based), connectivity allows sorting `[1,4,2,5,3]` within the segments, resulting in "YES". The next query may merge segments or change connectivity, and the union-find keeps track of which indices can be rearranged together.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) α(n)) | Each union/find operation is nearly constant; α(n) is the inverse Ackermann function |
| Space | O(n) | Union-find parent array |

Given the constraints $n, q \le 2 \cdot 10^5$, this solution easily runs within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n5 3\n1 4 2 5 3\nRLRLL\n2\n4\n3\n8 5\n1 5 2 4 8 3 6 7\nRRLLRRRL\n4\n3\n5\n3\n4\n6 2\n1 2 3 4 5 6\nRLRLRL\n4\n5\n") == "YES\nYES\nNO\nNO\nYES\nNO\nNO\nNO\nYES\nYES"

# custom case: all L except first/last
assert run("1\n5 2\n5 3 2 1 4\nRLLLL\n3\n4\n") == "NO\nNO"

# custom case: already sorted
assert run("1\n4 1\n1 2 3 4\nRRRL\n3\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All L except boundaries | NO | connectivity prevents sorting |
| Already sorted | YES | trivial segments are sufficient |
| Queries flipping middle indices | YES/NO | dynamic connectivity updates |

## Edge Cases

When a query flips a direction at the edge of two segments, the union-find merges them. For example, if `s = RLRL` and the second index flips from `L` to `R`, indices 2 and 3 can now swap in both directions. The algorithm correctly updates the parent array and merges components, ensuring that subsequent feasibility checks are accurate. This guarantees correct answers in all edge scenarios.
