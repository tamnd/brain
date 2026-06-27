---
title: "CF 105129C - LCIS"
description: "We are given two sequences, each a permutation of the same set of integers from 1 to n. The task is to find the length of the longest subsequence that appears in both permutations and is strictly increasing."
date: "2026-06-27T18:52:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "C"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 46
verified: true
draft: false
---

[CF 105129C - LCIS](https://codeforces.com/problemset/problem/105129/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences, each a permutation of the same set of integers from 1 to n. The task is to find the length of the longest subsequence that appears in both permutations and is strictly increasing.

A subsequence means we pick elements without changing their relative order inside each array. Increasing means the values themselves must strictly grow. So we are looking for a sequence of values that respects two constraints at once: it must appear in order inside both permutations, and the chosen values must be increasing.

A useful way to reinterpret the problem is to think of one permutation as defining an order, and the second permutation as a sequence in which we want to extract a longest increasing pattern when projected onto the first ordering.

The constraints allow n up to 100000 per test case with multiple test cases. This immediately rules out any quadratic approach over all pairs of positions. A solution must be close to linear or n log n per test case. Anything like dynamic programming over pairs of indices or checking all subsequences will be too slow.

A naive mistake is to treat this as longest common subsequence first and then enforce increasing order afterward. That would ignore the structure that both arrays are permutations. Another common incorrect approach is computing LIS directly on one permutation using values from the other without correctly mapping positions, which breaks the alignment condition.

## Approaches

The brute-force viewpoint starts from classical longest common subsequence. We could define a DP where dp[i][j] is the answer for prefixes a[1..i] and b[1..j]. That works for general sequences but costs O(n^2) per test case, which is far beyond limits when n is 100000.

The key simplification comes from the fact that both arrays are permutations. This means every value appears exactly once in each array. Instead of thinking about matching positions, we can convert the problem into a single sequence problem.

We fix array b as a reference order. We map each value in a to its position in b. Then we transform a into an array p where p[i] is the index of a[i] inside b. Now any subsequence of a corresponds to a subsequence of p, and the requirement that it is common to both permutations means we are choosing values whose positions in b are increasing. The condition that the chosen values are increasing in value is already automatically satisfied if we select them in order from a subsequence that respects b ordering. This reduces the problem to finding the longest increasing subsequence of the mapped array p.

The entire problem becomes a standard LIS problem on an array of length n, solvable in O(n log n) using a greedy tails array with binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force LCS DP | O(n^2) | O(n^2) | Too slow |
| Position mapping + LIS | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Build an array pos where pos[x] is the index of value x in permutation b. This gives us a fast way to compare ordering in b.
2. Replace each element a[i] by pos[a[i]]. After this transformation, we get a numeric sequence p representing where each element of a appears in b. The problem is now reduced to finding a longest increasing subsequence in p.
3. Maintain an array tails, where tails[len] stores the minimum possible last value of an increasing subsequence of length len found so far. This structure ensures we keep subsequences that are easiest to extend.
4. For each value x in p, find the first position in tails where x could extend or replace an existing tail using binary search. If x is larger than all current tails, we extend the sequence; otherwise we update the appropriate position.
5. The final size of tails is the length of the longest increasing subsequence, which is the answer.

The reason binary search is valid is that tails remains sorted at all times. Each position represents the best possible ending value for a subsequence of that length, so we never lose potential optimal extensions.

### Why it works

Any common increasing subsequence corresponds to a sequence of values whose positions in b are strictly increasing. Since we encode each value by its position in b, we are exactly selecting an increasing subsequence in p. Conversely, any increasing subsequence in p corresponds to values that appear in increasing order in both permutations. The LIS on p therefore captures exactly the LCIS length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, x in enumerate(b):
            pos[x] = i

        p = [pos[x] for x in a]

        tails = []

        for x in p:
            lo, hi = 0, len(tails)
            while lo < hi:
                mid = (lo + hi) // 2
                if tails[mid] < x:
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(tails):
                tails.append(x)
            else:
                tails[lo] = x

        print(len(tails))

if __name__ == "__main__":
    solve()
```

The first part builds the inverse position mapping for b, which is essential because it converts value comparisons into index comparisons. Without this step, we cannot unify the two permutations into a single sequence problem.

The second part constructs p, which is the transformed representation of a in the coordinate system of b. Every later step depends on this reduction.

The LIS implementation uses the standard patience sorting idea. The binary search ensures we maintain optimal tails efficiently, and updating tails instead of storing full sequences keeps memory linear.

## Worked Examples

Consider a simple case where a = [1, 3, 2, 4] and b = [1, 2, 3, 4]. Then pos becomes {1:0, 2:1, 3:2, 4:3}, and p becomes [0, 2, 1, 3].

| Step | x | tails before | action | tails after |
| --- | --- | --- | --- | --- |
| 1 | 0 | [] | append | [0] |
| 2 | 2 | [0] | append | [0, 2] |
| 3 | 1 | [0, 2] | replace index 1 | [0, 1] |
| 4 | 3 | [0, 1] | append | [0, 1, 3] |

Final answer is 3. This corresponds to the subsequence [1, 2, 4].

Now consider a reversed case a = [4, 3, 2, 1], b = [1, 2, 3, 4]. Then p = [3, 2, 1, 0].

| Step | x | tails before | action | tails after |
| --- | --- | --- | --- | --- |
| 1 | 3 | [] | append | [3] |
| 2 | 2 | [3] | replace | [2] |
| 3 | 1 | [2] | replace | [1] |
| 4 | 0 | [1] | replace | [0] |

Final answer is 1, since no increasing structure exists.

The first trace shows how local replacements can improve future extensibility, which is the core mechanism behind LIS. The second shows that strictly decreasing transformed sequences collapse to length one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of n elements is processed with a binary search over tails |
| Space | O(n) | Arrays for position mapping and LIS tails |

The total complexity fits comfortably within limits even for 100000 elements per test case, since log n is small and all operations are linear or near-linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import check_output
    return check_output(["python3", "solution.py"], input=inp.encode()).decode()

# sample-like tests
assert run("1\n1\n1\n1\n") == "1\n"

assert run("1\n4\n1 3 2 4\n1 2 3 4\n") == "3\n"

assert run("1\n4\n4 3 2 1\n1 2 3 4\n") == "1\n"

# identical permutations
assert run("1\n5\n1 2 3 4 5\n1 2 3 4 5\n") == "5\n"

# shifted order
assert run("1\n6\n2 3 4 5 6 1\n1 2 3 4 5 6\n") == "5\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | 1 | minimum boundary |
| identity permutations | n | full match case |
| reversed permutation | 1 | worst ordering collapse |
| cyclic shift | 5 | non-trivial LIS structure |

## Edge Cases

A critical edge case is when one permutation is exactly reversed. In that case, mapping produces a strictly decreasing sequence, and the LIS algorithm must correctly reduce it to length one without any accidental extension. The tails array continuously gets replaced rather than extended, preserving correctness.

Another case is when both permutations are identical. Then pos maps each element to its own index, producing an already increasing sequence, so every element extends tails. The algorithm must not trigger replacements in this case.

A third subtle case is when the best subsequence is not contiguous in either array. The LIS transformation handles this naturally because it operates only on relative ordering in b, not adjacency, ensuring such patterns are still discovered correctly.
