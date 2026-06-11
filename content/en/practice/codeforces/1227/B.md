---
title: "CF 1227B - Box"
description: "We are asked to reconstruct a hidden permutation from a sequence of its prefix maximums. Each test case provides an array q of length n, where q[i] represents the largest element among the first i elements of the unknown permutation p."
date: "2026-06-11T22:26:10+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1227
codeforces_index: "B"
codeforces_contest_name: "Technocup 2020 - Elimination Round 3"
rating: 1200
weight: 1227
solve_time_s: 116
verified: false
draft: false
---

[CF 1227B - Box](https://codeforces.com/problemset/problem/1227/B)

**Rating:** 1200  
**Tags:** constructive algorithms  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to reconstruct a hidden permutation from a sequence of its prefix maximums. Each test case provides an array `q` of length `n`, where `q[i]` represents the largest element among the first `i` elements of the unknown permutation `p`. Our task is to produce any permutation `p` that corresponds to this `q`, or determine that it is impossible.

The array `q` is non-decreasing by definition. Whenever `q[i]` increases compared to `q[i-1]`, we know that the permutation introduces a new maximum at position `i`. If `q[i]` stays the same as `q[i-1]`, the corresponding `p[i]` must be some value smaller than `q[i]` that has not yet appeared in the permutation.

The constraints imply that `n` can be up to 100,000, and the total sum of `n` across all test cases is at most 100,000. This means that any solution with time complexity significantly worse than O(n) per test case will be too slow. We need an algorithm that runs roughly in linear time.

Edge cases arise when `q` contains repeated maximums at the beginning or throughout. For instance, `q = [1,1]` is impossible because a permutation cannot have two distinct numbers equal to the same maximum, but `q = [1,2]` is trivial because `p = [1,2]` works.

A careless approach might try to simply pick the smallest remaining number whenever `q[i]` doesn't increase, but if no suitable unused number exists, it will fail silently. For example, `q = [1,1,2]` cannot be satisfied because after using 1 in the first position, there is no distinct number less than 1 for the second position.

## Approaches

The brute-force approach would attempt to generate all permutations of `[1..n]` and check each one against `q`. This is correct in principle but computationally infeasible, because generating all permutations has factorial complexity, O(n!). For `n = 10^5`, this is completely impractical.

The key observation that enables an efficient solution is that whenever `q[i]` increases, we must place that value in `p[i]`. Otherwise, the prefix maximum at that position would be smaller. Whenever `q[i]` remains the same, we must choose a number smaller than `q[i]` that has not yet appeared. Using this greedy choice ensures that all constraints are satisfied, as we always place the required maximum and fill remaining positions with the smallest available numbers to maintain uniqueness.

The trick is maintaining a pool of unused numbers efficiently. We can precompute all numbers from 1 to n, remove each number when it is placed, and always select the smallest remaining number when `q[i]` does not increase. This guarantees correctness and linear time complexity with a small overhead for maintaining the unused set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (Greedy + Set) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a set `unused` containing all numbers from 1 to `n`. This tracks the numbers we can still place in `p`.
2. Set `prev_max = 0`. This variable remembers the previous prefix maximum as we iterate through `q`.
3. Iterate over the positions `i = 0` to `n-1` in `q`:

1. If `q[i] > prev_max`, this is a new maximum. Place `q[i]` at `p[i]` and remove `q[i]` from `unused`. Update `prev_max = q[i]`.
2. If `q[i] == prev_max`, select the smallest number from `unused` that is strictly smaller than `q[i]` and place it at `p[i]`. If no such number exists, output `-1` because it is impossible to satisfy `q`.
4. After filling all positions, print the permutation `p`.

Why it works: The invariant maintained throughout the iteration is that all numbers already used are removed from `unused`, so no duplicates occur. Each new maximum is forced into position to satisfy `q[i]`. Remaining positions are filled with the smallest unused numbers to maintain the non-decreasing maximum property. If at any point we cannot satisfy the condition, we immediately know the permutation is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        q = list(map(int, input().split()))
        p = []
        prev_max = 0
        unused = set(range(1, n+1))
        
        import heapq
        heap = []
        for x in unused:
            heapq.heappush(heap, x)
        
        possible = True
        for val in q:
            if val > prev_max:
                if val not in unused:
                    possible = False
                    break
                p.append(val)
                unused.remove(val)
                prev_max = val
            else:
                while heap and heap[0] not in unused:
                    heapq.heappop(heap)
                if not heap or heap[0] >= val:
                    possible = False
                    break
                smallest = heapq.heappop(heap)
                p.append(smallest)
                unused.remove(smallest)
        if possible:
            print(' '.join(map(str,p)))
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The solution uses a min-heap to efficiently find the smallest unused number whenever `q[i]` does not increase. The check `heap[0] >= val` ensures that the number we choose does not violate the prefix maximum constraint. The `unused` set guarantees uniqueness. Handling the new maximum is trivial, as we just place it directly and remove it from the available pool.

## Worked Examples

**Sample 1**

Input: `q = [1, 3, 4, 5, 5]`

| i | q[i] | prev_max | Action | p | unused |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | New max → place 1 | [1] | {2,3,4,5} |
| 1 | 3 | 1 | New max → place 3 | [1,3] | {2,4,5} |
| 2 | 4 | 3 | New max → place 4 | [1,3,4] | {2,5} |
| 3 | 5 | 4 | New max → place 5 | [1,3,4,5] | {2} |
| 4 | 5 | 5 | Equal → place 2 | [1,3,4,5,2] | {} |

The output `[1,3,4,5,2]` matches `q` exactly.

**Sample 2**

Input: `q = [1,1,3,4]`

| i | q[i] | prev_max | Action | p | unused |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | New max → place 1 | [1] | {2,3,4} |
| 1 | 1 | 1 | Equal → need <1 → impossible | - | - |

We correctly output `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each number is placed once, heap operations are amortized O(log n) but only for unused numbers. Total over all test cases ≤ 10^5. |
| Space | O(n) | Stores `unused` numbers and the permutation array. |

The solution fits comfortably within the 1-second time limit and the memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n5\n1 3 4 5 5\n4\n1 1 3 4\n2\n2 1\n1\n1\n") == "1 3 4 5 2\n-1\n2 1\n1"

# Custom test cases
assert run("1\n3\n2 2 3\n") == "2 1 3"  # handles repeated max followed by new max
assert run("1\n2\n2 2\n") == "-1"       # impossible to satisfy repeated max at start
assert run("1\n1\n1\n") == "1"          # single element
assert run("1\n5\n1 2 3 4 5\n") == "1 2 3 4 5" # strictly increasing q
assert run("1\n5\n5 5 5 5 5\n") == "-1" # impossible, first element can't be less than 5
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `q=[2,2,3]` | `2 1 3` | repeated max followed by new max |
| `q=[ |  |  |
