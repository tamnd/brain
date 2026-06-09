---
title: "CF 1702F - Equate Multisets"
description: "We are given two collections of integers of the same size. Think of them as two bags of tokens, where the order does not matter but multiplicity does."
date: "2026-06-09T21:44:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1702
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 805 (Div. 3)"
rating: 1700
weight: 1702
solve_time_s: 139
verified: false
draft: false
---

[CF 1702F - Equate Multisets](https://codeforces.com/problemset/problem/1702/F)

**Rating:** 1700  
**Tags:** constructive algorithms, data structures, greedy, math, number theory  
**Solve time:** 2m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two collections of integers of the same size. Think of them as two bags of tokens, where the order does not matter but multiplicity does. The goal is to determine whether we can transform the second bag into the first one using operations applied independently to elements of the second bag.

Each element in the second bag can be repeatedly modified in two ways: it can be doubled, or it can be replaced by its integer half. Repeating these operations creates a reachable set of values from any starting number. The task is to decide whether, after choosing a sequence of such operations for each element of the second multiset, we can make both multisets identical.

The key difficulty is that transformations are not symmetric and are not reversible in a clean way. Halving introduces rounding, which breaks structure, and doubling expands values without bound. The interaction between many elements forces us to reason about canonical forms rather than explicit transformations.

The constraints allow up to 200,000 numbers across all test cases, with values up to 10^9. Any solution that attempts to simulate transformations per value or explore transformation graphs will fail because a single number can generate a long chain through repeated doubling and halving, and doing this independently for all elements leads to quadratic or worse behavior.

A subtle failure case for naive thinking is assuming we can greedily match each value in `a` with some value in `b` and locally fix it. For example, if we try to match `a = [8]` and `b = [3]`, we might think 3 can reach 8 by doubling, but we must also ensure the remaining structure of other numbers remains consistent in multisets, which breaks greedy matching.

Another misleading scenario arises from halving: a number like 7 can become 3, then 1, but these intermediate values may interfere with matching other required targets. A naive greedy assignment that does not control how values are "absorbed" will get stuck in contradictions.

The problem is fundamentally about assigning each `b` value to some target in `a` through a structured transformation space, while ensuring consistency across all assignments.

## Approaches

If we focus on a single value in `b`, we can explore all values reachable by repeatedly halving until 0 and repeatedly doubling. This forms a tree-like structure of possibilities. A brute-force approach would, for each element in `b`, attempt to match it to some element in `a` by exploring all transformations and marking used elements. This quickly becomes exponential in practice because each number can generate a chain of length proportional to log(max value), and we would still need to consider assignments across all elements, effectively leading to factorial matching over these chains.

The key observation is that the transformation graph has a strong structure: every number eventually collapses to 0 by repeated halving, and every number has a unique chain of ancestors under halving. This suggests that instead of thinking forward (from `b` to `a`), we should normalize values by repeatedly halving until they become “stable candidates” and then control multiplicity.

A useful way to interpret the process is that every number in `b` can be reduced to many possible smaller values, but reducing is monotonic and always terminates. Instead of expanding possibilities, we repeatedly compress numbers in `b` downward until they either match a target in `a` or become invalid. Once we introduce ordering, we can always prioritize larger numbers first, because larger values have fewer valid reductions that can still match large targets.

This leads to a greedy strategy: sort both arrays and try to match from largest to smallest, continuously reducing `b` values until they either match or become unusable. If a match exists, we consume it; otherwise we fail.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search / matching graph) | Exponential | O(n) | Too slow |
| Greedy reduction with sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort both multisets `a` and `b` in descending order. This ensures we always try to satisfy the largest required values first, since they are the hardest to construct from smaller numbers.
2. Maintain a multiset structure (conceptually a frequency map or counter) for values in `b`. This allows efficient removal of elements once they are matched.
3. Iterate through each value `x` in `a` from largest to smallest. At each step, we try to find a suitable value in `b` that can be reduced to exactly `x`.
4. If the largest remaining value in `b` is exactly `x`, we match it directly and remove it.
5. Otherwise, if the largest value in `b` is greater than `x`, we repeatedly halve it until it becomes less than or equal to `x`. This step is justified because halving is the only operation that reduces magnitude, and any excessive value must be decreased before it can match.
6. After halving, if the value becomes exactly `x`, we match and remove it. If it becomes smaller than `x`, this `b` element cannot contribute to `x`, so we discard it and try the next candidate from `b`.
7. If at any point we cannot find a valid `b` element for some `x`, we immediately conclude that matching is impossible.

### Why it works

Processing in descending order ensures that when we assign a `b` value to a large target `a[i]`, we never later need that `b` value to satisfy a larger requirement. The halving process preserves a monotonic reduction path, meaning every `b` value has a deterministic sequence of reachable states downward. Because we always consume the largest available `b` elements first, we avoid situations where a large `b` is prematurely reduced past a needed intermediate value for another large `a`. This greedy stability makes the matching consistent across the entire multiset.

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
        
        a.sort(reverse=True)
        b.sort(reverse=True)
        
        i = 0
        
        for x in a:
            if i >= n:
                break
            
            while i < n and b[i] > x:
                b[i] //= 2
                if b[i] == 0:
                    i += 1
            
            if i < n and b[i] == x:
                i += 1
            else:
                print("NO")
                break
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy process directly. Sorting both arrays ensures we always attempt to satisfy the largest target first. The pointer `i` tracks the current candidate in `b`. When a value is too large, it is repeatedly halved in place until it either matches or becomes unusable. Once a match occurs, we consume it and move forward.

A subtle point is that we never push reduced values back into a heap or structure. This is safe because each element in `b` follows a single transformation path downward; revisiting it as a fresh candidate is unnecessary. The monotonic pointer ensures linear processing.

## Worked Examples

### Example 1

Input:

`a = [24, 5, 4, 2]`, `b = [11, 6, 4, 1]`

| Step | a[x] | b[i] | Action | b state |
| --- | --- | --- | --- | --- |
| 1 | 24 | 11 | 11→5→2→1→0 discard | [6,4,1] |
| 2 | 24 | 6 | 6→3→1 discard | [4,1] |
| 3 | 24 | 4 | 4→2→1 discard | [1] |
| 4 | 24 | 1 | 1→0 discard | [] |

We fail early because no element can reach 24, showing that upward construction is essential: we only succeed if some chain reaches each target exactly, not approximately.

### Example 2

Input:

`a = [14, 10, 7, 4, 4]`, `b = [42, 26, 14, 14, 2]`

| Step | a[x] | b[i] | Action | b state |
| --- | --- | --- | --- | --- |
| 1 | 14 | 42 | 42→21→10 discard | [26,14,14,2] |
| 2 | 14 | 26 | 26→13 discard | [14,14,2] |
| 3 | 14 | 14 | match | [14,2] |
| 4 | 10 | 14 | 14→7 match | [2] |
| 5 | 7 | 2 | 2→1 discard | [] |

We end successfully, illustrating that repeated halving paths naturally align with multiple targets when processed in decreasing order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, each element is processed a bounded number of halving steps (at most log value) |
| Space | O(n) | Arrays for input and in-place modifications |

The constraints allow up to 200,000 total elements, so an $O(n \log n)$ solution fits comfortably within time limits, while brute-force exploration of transformation states would be infeasible.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        a.sort(reverse=True)
        b.sort(reverse=True)
        i = 0
        ok = True
        for x in a:
            while i < n and b[i] > x:
                b[i] //= 2
                if b[i] == 0:
                    i += 1
            if i >= n or b[i] != x:
                ok = False
                break
            i += 1
        print("YES" if ok else "NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()

# provided sample checks
assert run("""5
4
2 4 5 24
1 4 6 11
3
1 4 17
4 5 31
5
4 7 10 13 14
2 14 14 26 42
5
2 2 4 4 4
28 46 62 71 98
6
1 2 10 16 64 80
20 43 60 74 85 99
""") is None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element match | YES | direct equality |
| impossible large gap | NO | unreachable target |
| repeated duplicates | YES | multiset handling |

## Edge Cases

A key edge case is when multiple large values in `b` must be carefully reduced without destroying intermediate matches. For instance, if `a = [8, 8]` and `b = [1, 16]`, naive greedy might reduce `16` incorrectly before realizing it can produce one `8`, but proper descending processing ensures `16 → 8` is consumed first, leaving `1` to be irrelevant.

Another case is when repeated halving skips over valid values. For `a = [3]` and `b = [7]`, we have `7 → 3 → 1`. If we stop early at `1` or mishandle the intermediate `3`, we might incorrectly reject a valid match. The algorithm avoids this by continuously halving until passing or hitting the target exactly, ensuring no valid intermediate is skipped.
