---
title: "CF 104349D - Yet another permutation problem"
description: "We are given two permutations of the same set of numbers from 1 to n. Each player owns one array, and in a move a player is allowed to delete any single element from their own array."
date: "2026-07-01T18:15:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104349
codeforces_index: "D"
codeforces_contest_name: "TheForces Round #13 (Boombastic-Forces)"
rating: 0
weight: 104349
solve_time_s: 82
verified: false
draft: false
---

[CF 104349D - Yet another permutation problem](https://codeforces.com/problemset/problem/104349/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two permutations of the same set of numbers from 1 to n. Each player owns one array, and in a move a player is allowed to delete any single element from their own array. After each deletion, both arrays effectively shrink, and the relative order of remaining elements is preserved.

The game ends when both arrays become identical as sequences, meaning they have the same length and match at every position. Both players act optimally, and the task is to determine the minimum total number of deletion moves required across both arrays to reach this identical state.

A useful way to interpret the process is that we are trying to find a common subsequence that both arrays can be reduced to, since deletions only remove elements while preserving order. The final identical array must therefore be a sequence that appears as a subsequence in both permutations. The game ends when both sides have deleted everything except that common subsequence.

The answer is therefore driven by the longest sequence we can keep unchanged in both arrays while maintaining positional consistency.

The constraints are strong: n can be up to 100000 and summed across test cases up to 100000. This immediately rules out any quadratic or even n log squared approaches per test case. Any solution must be essentially linear or linearithmic.

A naive but tempting idea is to simulate deletions or try all possible final subsequences. That fails because the number of subsequences is exponential. Another common incorrect attempt is to greedily match positions without considering global consistency, which breaks when relative ordering constraints conflict across the two permutations.

For example, if A = [1, 2, 3, 4] and B = [2, 1, 4, 3], one might greedily try to match equal positions or early matches, but any local decision ignores that only a globally consistent subsequence can survive deletions in both arrays.

## Approaches

The key perspective shift is to stop thinking in terms of deletions and instead think in terms of what we can preserve simultaneously.

Since both arrays are permutations, each value appears exactly once in each array. This allows us to encode one permutation as a position map over the other. Concretely, if we fix array A, we can map each value x to its index in A. Then array B becomes a sequence of indices according to where its values appear in A.

This transforms the problem into a classic structure: we now want the longest increasing subsequence of that transformed array. Any increasing subsequence corresponds to values appearing in the same relative order in both permutations, which is exactly what is required for a common subsequence that can survive deletions.

Once we compute the LIS length, say L, that represents the maximum number of elements that can remain in both arrays in identical order. Since both arrays must end up exactly equal to that preserved sequence, each array must delete n − L elements. The total number of deletions across both players is therefore 2(n − L).

The brute-force approach would try all subsequences of A and check whether it appears in B in the same order, which is exponential. The LIS reduction compresses the entire compatibility condition into a single sequence optimization problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all subsequences) | O(2^n · n) | O(n) | Too slow |
| Optimal (LIS via position mapping) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed test case by test case.

1. Build a position array pos such that pos[x] is the index of value x in permutation A. This lets us translate values into their relative ordering in A.
2. Transform permutation B into an array T where T[i] = pos[B[i]]. Now T represents B expressed in the coordinate system of A.
3. Compute the length of the longest increasing subsequence of T using a standard patience sorting technique with a tails array. Each element is inserted using binary search.
4. Let L be the LIS length. The final answer is 2 * (n − L).

The reason step 3 is valid is that any increasing subsequence in T corresponds to indices in A that are increasing, meaning the corresponding values appear in the same order in both A and B.

### Why it works

The LIS on the transformed sequence captures exactly the largest set of elements that can be kept without violating order in either permutation. Because each number is unique in both arrays, preserving order in A is equivalent to requiring increasing indices in A, and matching order in B is guaranteed by construction of T. Every deletion reduces the arrays symmetrically until only this maximal consistent structure remains.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_left

def lis_length(arr):
    tails = []
    for x in arr:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        A = list(map(int, input().split()))
        B = list(map(int, input().split()))
        
        pos = [0] * (n + 1)
        for i, v in enumerate(A):
            pos[v] = i
        
        T = [pos[v] for v in B]
        L = lis_length(T)
        out.append(str(2 * (n - L)))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by constructing the position map for A, which is essential for converting the second permutation into a comparable numeric sequence. The transformation into T is the key reduction step, and it must be done carefully since any mistake here breaks the ordering logic.

The LIS function uses a greedy tails array with binary search. The invariant is that tails[i] stores the smallest possible ending value of an increasing subsequence of length i+1. This ensures optimal extension possibilities.

Finally, the answer computation directly reflects that both arrays must delete all elements not in the chosen common subsequence.

## Worked Examples

### Example 1

Input:

A = [1, 2, 3, 4], B = [2, 1, 4, 3]

Position map from A:

1→0, 2→1, 3→2, 4→3

Transformed B:

T = [1, 0, 3, 2]

LIS computation:

| Step | x | tails |
| --- | --- | --- |
| 1 | 1 | [1] |
| 2 | 0 | [0] |
| 3 | 3 | [0, 3] |
| 4 | 2 | [0, 2] |

L = 2

Answer = 2 * (4 − 2) = 4

This shows that only two elements can be preserved in consistent order across both permutations.

### Example 2

Input:

A = [4, 2, 3, 1], B = [4, 3, 2, 1]

Position map from A:

4→0, 2→1, 3→2, 1→3

Transformed B:

T = [0, 2, 1, 3]

LIS:

| Step | x | tails |
| --- | --- | --- |
| 1 | 0 | [0] |
| 2 | 2 | [0, 2] |
| 3 | 1 | [0, 1] |
| 4 | 3 | [0, 1, 3] |

L = 3

Answer = 2 * (4 − 3) = 2

This demonstrates that even when both permutations are heavily mixed, a long consistent subsequence can still exist if relative structure aligns partially.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | LIS computation uses binary search for each element |
| Space | O(n) | position array and transformed sequence |

The total n across test cases is at most 100000, so the solution comfortably fits within time limits. The logarithmic factor is small enough to handle efficiently.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from bisect import bisect_left

    def lis_length(arr):
        tails = []
        for x in arr:
            i = bisect_left(tails, x)
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            A = list(map(int, input().split()))
            B = list(map(int, input().split()))
            pos = [0] * (n + 1)
            for i, v in enumerate(A):
                pos[v] = i
            T = [pos[v] for v in B]
            L = lis_length(T)
            out.append(str(2 * (n - L)))
        return "\n".join(out)

    return solve()

# provided sample
assert run("""3
4
1 2 3 4
2 1 4 3
4
1 2 3 4
1 2 4 3
5
4 2 3 5 1
4 5 1 3 2
""") == """4
2
4"""

# custom: already identical
assert run("""1
3
1 2 3
1 2 3
""") == "0"

# custom: reversed
assert run("""1
4
1 2 3 4
4 3 2 1
""") == "6"

# custom: alternating structure
assert run("""1
6
1 3 5 2 4 6
1 2 3 4 5 6
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical permutations | 0 | no deletions needed |
| reversed permutation | 6 | minimal LIS = 1 |
| mixed alternating case | 4 | partial ordering consistency |

## Edge Cases

A fully identical pair of permutations produces a transformed sequence that is strictly increasing, so LIS equals n and the answer becomes zero. The algorithm naturally handles this because every element extends the tails array without replacement.

A fully reversed permutation produces a strictly decreasing transformed sequence, so LIS is always 1. The code correctly replaces tails entries repeatedly and ends with length 1, yielding 2(n − 1).

Small n cases such as n = 1 or n = 2 are handled without special logic because LIS computation and position mapping both degrade safely: with n = 1, T has one element and LIS is 1, giving zero deletions as expected.
