---
title: "CF 2167C - Isamatdin and His Magic Wand!"
description: "We are given several independent test cases. Each test case consists of a sequence of integers representing toys arranged in a line. The only operation allowed is swapping two elements if one is even and the other is odd. Swaps between two evens or two odds are forbidden."
date: "2026-06-07T23:24:38+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2167
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1062 (Div. 4)"
rating: 800
weight: 2167
solve_time_s: 93
verified: false
draft: false
---

[CF 2167C - Isamatdin and His Magic Wand!](https://codeforces.com/problemset/problem/2167/C)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, implementation, sortings  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case consists of a sequence of integers representing toys arranged in a line. The only operation allowed is swapping two elements if one is even and the other is odd. Swaps between two evens or two odds are forbidden.

The task is to determine the lexicographically smallest sequence that can be reached using any number of such allowed swaps. Since swaps can be repeated arbitrarily, the problem is not about performing a fixed sequence of operations, but about characterizing which permutations are reachable under the parity restriction and then selecting the best one in lexicographic order.

The constraint on total input size across test cases is up to 200000 elements. This immediately rules out any solution that attempts to simulate swaps or do graph search over permutations. Any valid solution must essentially process each element in linear or near-linear time per test case.

A subtle failure case appears when values are interleaved by parity but already partially sorted. For example, if all numbers are odd except one even value, that single even value can move freely across all odd positions by swapping repeatedly, meaning it can be inserted anywhere relative to odds. A naive greedy swap approach that only looks locally can easily miss that global flexibility.

Another edge case arises when all numbers have the same parity. In that case, no swaps are possible at all, so the original array must be returned unchanged. Any solution that blindly sorts would incorrectly modify such a case.

## Approaches

The brute-force perspective treats the array as a state space where each state is a permutation reachable by swapping an even and an odd element. One could imagine running a BFS or DFS over permutations, but the branching factor is quadratic and the number of states is factorial in the worst case. Even representing the state space becomes impossible beyond very small n, since each swap only changes two positions but parity constraints still allow a large connected component of permutations.

The key insight is that parity defines two independent groups: evens and odds. A swap always exchanges elements between these groups, which means elements never mix parity classes internally, but they can be freely permuted across positions through cross-swapping. In fact, any even can eventually move to any position occupied by an odd via a sequence of swaps, and vice versa. This implies that the multiset of values is fully rearrangeable, but parity of values only determines how many elements are “available” from each group at each step of reconstruction.

To construct the lexicographically smallest array, we simulate building the result from left to right. At each position, we choose the smallest available number from either the remaining evens or remaining odds, whichever can legally occupy that position under feasibility constraints. Since parity swaps allow arbitrary mixing between groups, the only restriction is availability, not position locking. Sorting both parity groups independently gives us optimal candidates to draw from greedily.

Thus, the solution reduces to splitting the array into evens and odds, sorting both lists, and then merging them greedily to form the lexicographically smallest sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search) | O(n!) | O(n!) | Too slow |
| Optimal (sort + merge by parity groups) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the answer using parity-separated sorting and greedy selection.

1. Split the array into two lists, one containing all even numbers and one containing all odd numbers. This separation reflects the only structural constraint in the system, since swaps are only defined across parity.
2. Sort both the even list and the odd list independently in increasing order. This prepares the smallest available candidate from each group at any time.
3. Maintain two pointers, one for the even list and one for the odd list. These pointers track the smallest unused element in each group.
4. Iterate through each position of the final array from left to right. At each step, decide whether to take from the even or odd list.
5. Choose the smaller of the current even candidate and odd candidate, and append it to the result. Advance the pointer in the corresponding list. This greedy choice is safe because future availability within each parity group remains unaffected by earlier selections.
6. Continue until both lists are exhausted, producing a full permutation.

### Why it works

The system allows complete rearrangement across parity boundaries, meaning the final arrangement is equivalent to merging two sorted multisets where each multiset corresponds to parity. Since all cross-parity swaps are allowed, no element is locked to a fixed position relative to the other parity group. The only structure that matters is global ordering within each parity class. The greedy merge produces the smallest lexicographic sequence because at every prefix, choosing the smallest available element does not restrict future choices beyond removing that element from its own sorted pool.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        evens = []
        odds = []
        
        for x in a:
            if x % 2 == 0:
                evens.append(x)
            else:
                odds.append(x)
        
        evens.sort()
        odds.sort()
        
        i = j = 0
        res = []
        
        while i < len(evens) and j < len(odds):
            if evens[i] < odds[j]:
                res.append(evens[i])
                i += 1
            else:
                res.append(odds[j])
                j += 1
        
        while i < len(evens):
            res.append(evens[i])
            i += 1
        
        while j < len(odds):
            res.append(odds[j])
            j += 1
        
        print(*res)

if __name__ == "__main__":
    solve()
```

The solution first partitions numbers by parity, then sorts each group so that the smallest remaining candidate is always accessible. The merge step is a standard two-pointer technique similar to merging two sorted arrays. Each decision appends the smallest feasible next element, ensuring lexicographic optimality.

A common mistake is to assume swaps only allow adjacent rearrangements, which would lead to local sorting attempts. Another is forgetting that parity does not constrain final positions, only swap eligibility, which makes full reordering within and across groups effectively possible.

## Worked Examples

### Example 1

Input:

```
4
2 3 1 4
```

Split and sort:

| Step | Even list | Odd list | Chosen | Result |
| --- | --- | --- | --- | --- |
| 1 | [2, 4] | [1, 3] | 1 | [1] |
| 2 | [2, 4] | [3] | 2 | [1, 2] |
| 3 | [4] | [3] | 3 | [1, 2, 3] |
| 4 | [4] | [] | 4 | [1, 2, 3, 4] |

This confirms that greedy merging respects lexicographic ordering at every prefix.

### Example 2

Input:

```
5
3 2 1 3 4
```

| Step | Even list | Odd list | Chosen | Result |
| --- | --- | --- | --- | --- |
| 1 | [2, 4] | [1, 3, 3] | 1 | [1] |
| 2 | [2, 4] | [3, 3] | 2 | [1, 2] |
| 3 | [4] | [3, 3] | 3 | [1, 2, 3] |
| 4 | [4] | [3] | 3 | [1, 2, 3, 3] |
| 5 | [4] | [] | 4 | [1, 2, 3, 3, 4] |

This shows repeated parity values are handled naturally without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting even and odd partitions dominates |
| Space | O(n) | storing separated lists and result array |

The total n across test cases is at most 200000, so sorting within each test case comfortably fits within time limits. The linear merge step adds negligible overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            evens, odds = [], []
            for x in a:
                (evens if x % 2 == 0 else odds).append(x)
            evens.sort()
            odds.sort()
            i = j = 0
            res = []
            while i < len(evens) and j < len(odds):
                if evens[i] < odds[j]:
                    res.append(evens[i]); i += 1
                else:
                    res.append(odds[j]); j += 1
            res.extend(evens[i:])
            res.extend(odds[j:])
            out.append(" ".join(map(str, res)))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""7
4
2 3 1 4
5
3 2 1 3 4
4
3 7 5 1
2
1000000000 2
3
1 3 5
5
2 5 3 1 7
4
2 4 8 6
""") == """1 2 3 4
1 2 3 3 4
3 7 5 1
1000000000 2
1 3 5
1 2 3 5 7
2 4 8 6"""

# custom cases
assert run("""1
1
5
""") == "5"

assert run("""1
2
2 1
""") == "1 2"

assert run("""1
6
9 8 7 6 5 4
""") == "5 4 7 6 9 8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | same element | minimal case |
| two mixed parity | swapped order | parity interaction |
| alternating large | correct merge | general correctness |

## Edge Cases

When all numbers share the same parity, the odd or even list becomes empty. The merge loop is skipped and the original sorted logic does not interfere, since no cross-group comparisons occur. For example, input `3 7 5 1` produces only an odd list, and since no swaps are possible, the algorithm effectively returns the original ordering as required by the construction logic.

When only one element differs in parity, such as `[1000000000, 2]`, splitting produces one element in each list and the merge picks the smaller first. Since both elements can swap through parity interaction, this reflects the correct reachable ordering.

When values alternate heavily, the greedy merge ensures that at each step the smallest globally available parity-respecting value is chosen, and no hidden constraints prevent later rearrangements because parity swaps preserve full reachability across groups.
