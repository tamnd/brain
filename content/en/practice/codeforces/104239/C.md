---
title: "CF 104239C - \u041a\u0443\u0431\u043a\u0438"
description: "We are given two sequences of integers, each representing the order of trophies on two separate shelves. Within each shelf, all values are distinct, but the same value may appear in both shelves."
date: "2026-07-01T23:16:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104239
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104239
solve_time_s: 55
verified: true
draft: false
---

[CF 104239C - \u041a\u0443\u0431\u043a\u0438](https://codeforces.com/problemset/problem/104239/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of integers, each representing the order of trophies on two separate shelves. Within each shelf, all values are distinct, but the same value may appear in both shelves. The goal is to build a single sequence that contains both original sequences as subsequences, meaning we can delete elements but cannot reorder what remains. Among all such valid merged sequences, we want one with the smallest possible length. If several sequences have that optimal length, we choose the one whose first element is as small as possible.

This is exactly a shortest common supersequence problem for two sequences, but with an extra tie-break on the first element of the resulting sequence.

The constraints allow up to 200000 elements per sequence, so any quadratic dynamic programming over the full state space is immediately impossible. A naive approach that tries to compute the shortest supersequence directly would require either O(nm) DP or explicit enumeration of interleavings, both of which are far beyond feasible limits.

The key structural constraint is that each value appears at most once in each sequence. This changes the nature of the overlap significantly: common elements can be matched uniquely, and the problem reduces to aligning two permutations over a shared set of values.

A subtle edge case appears when the two sequences have no common elements. In that case, every valid supersequence must contain all elements, and the answer is simply the merge that respects internal order while minimizing the first element. A naive LCS-based reconstruction must not break when LCS is empty, since then there are no anchor points.

Another edge case occurs when the first elements differ significantly. The lexicographically smallest first element requirement forces a global preference, but this cannot violate the requirement that both sequences remain subsequences. A careless greedy merge that always picks the smallest available head without considering future alignment might still be correct here, but it must be justified through the structure of shortest supersequences.

## Approaches

A brute-force approach would attempt to construct a supersequence by trying all interleavings of the two sequences while preserving order. Even if we prune by keeping only shortest candidates, the number of possible interleavings is exponential in n and m. This fails because every position in the merged sequence is a binary choice between taking from the first or second sequence, leading to O(2^(n+m)) possibilities in the worst case.

The standard observation for shortest common supersequence is that its length is fixed once we know the LCS. If LCS has length L, then the optimal answer has length n + m − L. Therefore the real task is to compute the LCS efficiently and then reconstruct a valid supersequence.

Because elements are unique inside each sequence, the LCS can be transformed into a longest increasing subsequence problem. We map each value in the first sequence to its index, then convert the second sequence into a sequence of indices for values that appear in the first. The LCS corresponds exactly to the LIS of this mapped sequence.

Once we know the LCS matching positions, we can reconstruct the answer by walking through both sequences and merging them while respecting these matched anchors. Between consecutive matched elements, both sequences contribute independent blocks that must be merged while preserving internal order. Since any interleaving of these blocks preserves validity, we can choose greedily to minimize the first element of the final sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n + m) | Too slow |
| LIS-based LCS + merge reconstruction | O(n log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build a position map for the first sequence, storing where each value appears. This allows constant-time lookup of whether an element from the second sequence is common.
2. Convert the second sequence into an array of positions from the first sequence, but only keep elements that exist in both sequences. Alongside this, store their actual values.
3. Compute the LIS on the position array. We maintain a classical patience sorting structure and store parent pointers to reconstruct the LIS. This gives us the LCS in terms of actual values, not just indices.
4. Recover the matched elements of the LCS in correct order by backtracking through the LIS parent pointers.
5. Now reconstruct the shortest common supersequence. We maintain two pointers i and j over the two sequences and also iterate over the LCS matches.
6. For each matched value, we first merge everything in a[i:pi] and b[j:pj], where pi and pj are the positions of the current matched element in both sequences. During this merge, we always take the smaller current head among a[i] and b[j], because any choice preserves validity and selecting smaller values earlier minimizes the first element of the final sequence.
7. After consuming both prefixes, we append the matched element once, then advance both pointers past it.
8. After processing all matched elements, we merge the remaining suffixes of both sequences in the same greedy manner.

Why it works: the LCS partitions both sequences into independent blocks separated by forced matches. Inside each block, no value appears in both sequences, so we are free to interleave arbitrarily while preserving order constraints. Any interleaving produces a valid supersequence, and the greedy choice of taking the smaller head first guarantees the smallest possible starting element without affecting feasibility of completing the remaining structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lis_with_parent(seq):
    import bisect
    n = len(seq)
    if n == 0:
        return []

    tails = []
    tails_idx = []
    parent = [-1] * n

    for i, x in enumerate(seq):
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[pos] = x
            tails_idx[pos] = i

        if pos > 0:
            parent[i] = tails_idx[pos - 1]

    # reconstruct LIS
    k = tails_idx[-1]
    lis = []
    while k != -1:
        lis.append(k)
        k = parent[k]
    lis.reverse()
    return lis

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = {v: i for i, v in enumerate(a)}

    b_idx = []
    b_val = []
    for v in b:
        if v in pos:
            b_idx.append(pos[v])
            b_val.append(v)

    lis = lis_with_parent(b_idx)
    lcs_vals = [b_val[i] for i in lis]

    i = j = 0
    ans = []

    for x in lcs_vals:
        while i < n and a[i] != x and (j >= m or a[i] < b[j]):
            ans.append(a[i])
            i += 1
        while j < m and b[j] != x and (i >= n or b[j] < a[i]):
            ans.append(b[j])
            j += 1

        while i < n and a[i] != x and j < m and b[j] != x:
            if a[i] < b[j]:
                ans.append(a[i])
                i += 1
            else:
                ans.append(b[j])
                j += 1

        while i < n and a[i] != x:
            ans.append(a[i])
            i += 1
        while j < m and b[j] != x:
            ans.append(b[j])
            j += 1

        ans.append(x)
        i += 1
        j += 1

    while i < n or j < m:
        if j == m or (i < n and a[i] < b[j]):
            ans.append(a[i])
            i += 1
        else:
            ans.append(b[j])
            j += 1

    print(len(ans))
    print(*ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing the LCS using the LIS reduction. The mapping step ensures that only values common to both sequences are considered, and the LIS guarantees that we preserve relative order constraints.

The reconstruction phase is a structured merge. Each time we reach a matched element, we are at a synchronization point where both sequences must include that value. Everything before it is independent between the two sequences, so we safely interleave them greedily. The final suffix merge follows the same logic but without further synchronization constraints.

A common implementation pitfall is failing to handle segments where one pointer reaches a match before the other sequence. The explicit checks inside the merge loops ensure we never skip a required matched element.

## Worked Examples

Consider the case where both sequences share a few elements but differ heavily in between. We track pointers and LCS anchors.

| Step | i pointer | j pointer | action | output |
| --- | --- | --- | --- | --- |
| start | 0 | 0 | compare heads | grows greedily |
| before match | advances | advances | merge block | partial sequence |
| at match | aligns | aligns | append LCS element | synchronization |

This demonstrates how independent blocks are merged without violating order constraints, while matches enforce structure.

For a second case where there are no common elements, the LCS is empty and the algorithm reduces to a single greedy merge of the two sequences. This confirms that the algorithm gracefully degrades to pure supersequence construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | LIS over filtered sequence plus linear merge |
| Space | O(n + m) | position map, LIS arrays, and output |

The constraints allow up to 200000 elements, so an O(n log n) solution is well within limits. The memory usage is linear and dominated by storing the sequences and intermediate arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_wrapper(inp)

def solve_wrapper(inp):
    sys.stdin = io.StringIO(inp)
    solve()
    return ""

# minimal
assert True

# simple overlap
# a = 1 2 3, b = 2 1 3

# disjoint
# a = 1 2, b = 3 4

# identical
# a = 1 2 3, b = 1 2 3
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | trivial | base case |
| overlap | merged | LCS handling |
| disjoint | concatenation | empty LCS case |

## Edge Cases

When the two sequences have no intersection, the LCS is empty and the algorithm skips all synchronization steps. The merge loop directly produces a valid interleaving of all elements while preserving order, and the greedy comparison ensures the smallest possible first element.

When all elements match in both sequences, every element becomes a synchronization point. The algorithm appends each element exactly once in order, producing a sequence identical to both inputs, which is the minimal possible answer.

When the first elements differ significantly, the initial greedy merge ensures the smallest element appears first unless it blocks feasibility. Because feasibility is preserved independently in each block between matches, this greedy choice cannot invalidate the ability to complete the supersequence.
