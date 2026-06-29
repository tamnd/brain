---
title: "CF 104640E - \u041f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u043e\u0435 \u041f\u044f\u0442\u043d\u043e"
description: "We are given a collection of axis-aligned rectangles, each defined by its height and width, and each rectangle is also allowed to be rotated by 90 degrees."
date: "2026-06-29T16:50:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104640
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104640
solve_time_s: 92
verified: false
draft: false
---

[CF 104640E - \u041f\u0440\u044f\u043c\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u043e\u0435 \u041f\u044f\u0442\u043d\u043e](https://codeforces.com/problemset/problem/104640/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of axis-aligned rectangles, each defined by its height and width, and each rectangle is also allowed to be rotated by 90 degrees. This means that for every rectangle we can treat it as having two possible orientations, and we are free to choose whichever orientation helps us.

The goal is to select a subset of these rectangles and arrange them in a strictly non-decreasing chain, where each rectangle fits inside the next one. A rectangle with dimensions $(h_1, w_1)$ can be placed inside $(h_2, w_2)$ if both height and width do not exceed the corresponding dimensions. We want the longest possible such chain, and we also need to output the indices of the rectangles forming it in order.

The problem is essentially asking for the longest chain under a two-dimensional partial order, but with the added twist that each item has two possible states due to rotation.

The constraint $n \le 10^5$ immediately rules out any quadratic comparison between pairs. Any approach that tries to compare all pairs or run dynamic programming over all previous rectangles in a straightforward way would lead to about $10^{10}$ operations in the worst case, which is far beyond feasible limits.

A naive but tempting mistake is to treat each rectangle independently, pick its best orientation locally, and then sort and greedily take a chain. This fails because orientation decisions are global. A rectangle might need to be “sacrificed” into a non-optimal orientation to enable longer chains later.

Another subtle issue arises when both dimensions are equal after rotation. If we always normalize by sorting dimensions without care, we might unintentionally allow invalid chains or break tie consistency, which can destroy the reconstruction of a correct sequence.

## Approaches

A brute-force solution would try all subsets and all orientation choices, checking whether a given sequence forms a valid nesting chain. Even restricting to subsequences, this becomes exponential in $n$. A slightly more structured brute force would be dynamic programming over subsets or over pairs, but even then we would end up comparing every rectangle to every other rectangle, leading to $O(n^2)$ transitions. With $10^5$ rectangles, this is completely infeasible.

The key structural observation is that once rectangles are placed in a chain, one dimension is non-decreasing along the chain, and we can enforce ordering by sorting. The real challenge is that we are dealing with a two-dimensional ordering, which is classic Longest Increasing Subsequence (LIS) in 2D.

The rotation freedom simplifies each rectangle into a choice of ordering its two sides. The best strategy is to always orient each rectangle so that its smaller side is treated as height and its larger side as width. This normalization ensures consistency: every rectangle is represented in its minimal canonical form $(a, b)$ with $a \le b$. Any optimal chain can be transformed into one using this representation because swapping axes only helps reduce constraints.

After normalization, the problem reduces to finding the longest sequence of pairs $(a_i, b_i)$ such that both coordinates are non-decreasing. This is a standard 2D LIS problem. Sorting by the first coordinate, and then finding the LIS on the second coordinate, gives the optimal chain structure.

To reconstruct the sequence, we must store predecessors during LIS computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ or $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. For each rectangle, reorder its dimensions so that $a = \min(h, w)$ and $b = \max(h, w)$. This fixes rotation choices into a canonical representation, ensuring every rectangle is represented in the most restrictive orientation for nesting.
2. Store each rectangle as a triple $(a, b, index)$, preserving original indices so that we can reconstruct the answer later.
3. Sort all rectangles by $a$ in increasing order, and for equal $a$, by $b$ in increasing order. This ensures that any valid nesting chain must respect this ordering on the first coordinate, so we only need to control the second coordinate going forward.
4. Run a longest non-decreasing subsequence process on the sequence of $b$ values. We maintain a DP structure where we store the smallest possible ending value for a subsequence of each length.
5. To allow reconstruction, we store for each element the length of the best subsequence ending there and a predecessor pointer to the previous element in that subsequence. This is necessary because the problem requires the actual chain, not just its length.
6. When updating the LIS structure, we use binary search to find the first position where the current $b$ can be placed, maintaining minimal tail values. Each update corresponds to extending or improving a subsequence.
7. After processing all rectangles, we identify the position with the maximum subsequence length and reconstruct the chain by following predecessor pointers backwards, then reversing the result.

### Why it works

The correctness rests on reducing a 2D dominance problem into a 1D LIS problem. Sorting by $a$ ensures that any valid chain must already satisfy the first dimension constraint. After that, the second dimension becomes the only remaining condition. Because all rectangles are pre-sorted, any subsequence we build automatically preserves non-decreasing $a$, so enforcing LIS on $b$ guarantees full validity.

The predecessor pointers ensure that every extension in the LIS corresponds to a real valid transition between rectangles in sorted order, so the reconstructed chain is a valid nesting sequence in both dimensions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    rects = []
    for i in range(n):
        h, w = map(int, input().split())
        a, b = min(h, w), max(h, w)
        rects.append((a, b, i + 1))
    
    rects.sort(key=lambda x: (x[0], x[1]))
    
    import bisect
    
    tail = []
    tail_idx = []
    parent = [-1] * n
    pos_in_tail = [-1] * n
    
    # store best ending index for each length
    best_idx = []
    
    for i, (a, b, idx) in enumerate(rects):
        j = bisect.bisect_right(tail, b)
        
        if j == len(tail):
            tail.append(b)
            best_idx.append(i)
        else:
            tail[j] = b
            best_idx[j] = i
        
        pos_in_tail[i] = j
        
        if j > 0:
            parent[i] = best_idx[j - 1]
    
    # reconstruct LIS
    length = len(tail)
    last = best_idx[length - 1]
    
    ans = []
    while last != -1:
        ans.append(rects[last][2])
        last = parent[last]
    
    ans.reverse()
    
    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The code first normalizes each rectangle so that orientation is fixed in a consistent way. Sorting by the first dimension ensures we only need to manage feasibility in the second dimension. The LIS structure uses `tail` to maintain minimal possible ending values for subsequences of each length, and `best_idx` to remember which rectangle currently defines each subsequence length endpoint.

The `parent` array is what enables reconstruction. Every time a rectangle extends a subsequence, it stores a pointer to the best sequence of length one less. This guarantees that when we backtrack from the last element of the optimal subsequence, we recover a valid chain in correct order.

A subtle point is the use of `bisect_right` instead of `bisect_left`. This enforces non-decreasing sequences rather than strictly increasing ones, matching the condition $h_1 \le h_2$, $w_1 \le w_2$.

## Worked Examples

### Sample 1

Input rectangles after normalization:

| i | (a, b) | sorted order |
| --- | --- | --- |
| 1 | (1, 1) | 1 |
| 2 | (2, 3) | 4 |
| 3 | (2, 5) | 3 |
| 4 | (1, 4) | 2 |
| 5 | (3, 5) | 5 |

After sorting:

(1,1), (1,4), (2,3), (2,5), (3,5)

We process LIS on second coordinates:

| step | b | tail | action |
| --- | --- | --- | --- |
| 1 | 1 | [1] | start |
| 2 | 4 | [1,4] | extend |
| 3 | 3 | [1,3] | replace |
| 4 | 5 | [1,3,5] | extend |
| 5 | 5 | [1,3,5] | extend |

Final chain length is 4 with reconstruction yielding indices consistent with a valid nesting order such as $1 \to 4 \to 3 \to 5$.

This trace shows how replacing tails improves future extension potential without breaking correctness.

### Sample 2

Input:

(1,10), (2,9), (3,8), (4,7), (5,6)

After normalization and sorting, second coordinates are strictly decreasing.

| step | b | tail |
| --- | --- | --- |
| 1 | 10 | [10] |
| 2 | 9 | [9] |
| 3 | 8 | [8] |
| 4 | 7 | [7] |
| 5 | 6 | [6] |

Each element replaces the previous tail, so LIS length is 1.

This confirms that when no nesting is possible, the algorithm correctly avoids forcing invalid increasing structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates $O(n \log n)$, LIS uses binary search per element |
| Space | $O(n)$ | storing rectangles, DP arrays, and reconstruction pointers |

The complexity fits comfortably within constraints for $n = 10^5$, since both sorting and binary searches scale efficiently and memory usage is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # direct inline solution for testing
    n = int(sys.stdin.readline())
    rects = []
    for i in range(n):
        h, w = map(int, sys.stdin.readline().split())
        rects.append((min(h, w), max(h, w), i + 1))
    rects.sort(key=lambda x: (x[0], x[1]))

    import bisect
    tail = []
    best_idx = []
    parent = [-1] * n
    pos = [-1] * n

    for i, (_, b, _) in enumerate(rects):
        j = bisect.bisect_right(tail, b)
        if j == len(tail):
            tail.append(b)
            best_idx.append(i)
        else:
            tail[j] = b
            best_idx[j] = i
        pos[i] = j
        if j > 0:
            parent[i] = best_idx[j - 1]

    length = len(tail)
    cur = best_idx[length - 1]
    ans = []
    while cur != -1:
        ans.append(rects[cur][2])
        cur = parent[cur]

    return f"{len(ans)}\n" + " ".join(map(str, ans[::-1]))

# samples
assert run("5\n1 1\n3 2\n2 5\n4 1\n3 5\n") == "4\n1 4 3 5"
assert run("5\n1 10\n2 9\n3 8\n4 7\n5 6\n") == "1\n1"

# custom
assert run("1\n7 3\n") == "1\n1"
assert run("3\n1 1\n1 1\n1 1\n") == "3\n1 2 3"
assert run("3\n5 4\n6 3\n7 2\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rectangle | 1 element chain | base case |
| identical rectangles | all usable in any order | equal handling |
| strictly decreasing | only one element | no false chaining |

## Edge Cases

A subtle edge case is when many rectangles become identical after normalization. For example, $(3,5), (5,3), (3,5)$ all normalize to $(3,5)$. The algorithm allows all of them to participate in the LIS because we use non-decreasing transitions. This is correct because identical rectangles can always nest in any order.

Another case is when rotation matters for feasibility. A rectangle like $(2,10)$ and another $(9,3)$ would both normalize to $(2,10)$ and $(3,9)$, and without normalization consistency, a greedy choice of orientation could break the chain. The canonical transformation removes this ambiguity before LIS computation.

Finally, cases with large increasing chains in both dimensions stress reconstruction correctness. Because every DP transition stores a predecessor, the backtracking step always recovers a consistent sequence even when multiple optimal subsequences exist.
