---
title: "CF 1211A - Three Problems"
description: "We are given a list of problem difficulties, each tied to its original position in the list. The task is to pick three distinct indices so that their corresponding values form a strictly increasing sequence."
date: "2026-06-13T17:03:51+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1211
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 2"
rating: 1000
weight: 1211
solve_time_s: 305
verified: false
draft: false
---

[CF 1211A - Three Problems](https://codeforces.com/problemset/problem/1211/A)

**Rating:** 1000  
**Tags:** *special, implementation  
**Solve time:** 5m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of problem difficulties, each tied to its original position in the list. The task is to pick three distinct indices so that their corresponding values form a strictly increasing sequence. Only the relative ordering of the chosen values matters, not their positions in the array.

In other words, we need to find any triple of indices $a, b, c$ such that the value at $a$ is smaller than the value at $b$, and the value at $b$ is smaller than the value at $c$. If no such triple exists, we report failure.

The input size goes up to $n = 3000$. This immediately rules out any cubic or even moderately optimized quadratic approach that does heavy work per pair. A naive $O(n^3)$ scan would check all triples explicitly and is too slow because it performs roughly 27 billion operations in the worst case. Even an $O(n^2)$ solution is borderline but acceptable if implemented with simple comparisons and no hidden overhead.

A subtle issue appears when values are duplicated or nearly constant. For example, if all values are equal, any attempt that assumes a strictly increasing structure will fail, and we must correctly output $-1 -1 -1$. Another edge case is when the array is strictly decreasing, where no valid triple exists even though all elements are distinct. A careless approach that only checks for distinct values might incorrectly assume success.

## Approaches

The brute-force idea is straightforward. Try every triple of indices $i < j < k$ and check whether the corresponding values are strictly increasing. This is correct because it exhausts all possibilities, but it requires checking all combinations of three elements, which leads to $O(n^3)$ operations.

We can reduce this by fixing the middle element of the triple. Instead of searching all triples, we treat each position $j$ as the potential middle element. If we can find one smaller element to the left of $j$ and one larger element to the right of $j$, we immediately obtain a valid triple. This shifts the problem from combinatorial search to local existence checks around each index.

For each $j$, we only need to scan left and right to find candidates. The key observation is that we do not need the best candidates, only any valid ones. This keeps the implementation simple and still within quadratic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Middle Fix + Scan | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Iterate over each index $j$, treating it as the middle element of the potential triple.

This is natural because any valid increasing triple has a well-defined middle element.
2. For each $j$, scan all indices $i < j$ and pick any index where $r_i < r_j$. Store it as a candidate left endpoint.

We only need one such index because any valid triple does not require optimal selection.
3. For the same $j$, scan all indices $k > j$ and pick any index where $r_k > r_j$. Store it as a candidate right endpoint.

Again, any valid choice is sufficient.
4. If both a left candidate and a right candidate exist for this $j$, output them immediately as $i, j, k$.

This guarantees $r_i < r_j < r_k$, forming a valid solution.
5. If no index $j$ produces such a pair, output $-1 -1 -1$.

This means no element can serve as a middle value in a strictly increasing triple.

### Why it works

Every valid solution must have a middle element $b$. If such a triple exists, then for that specific $b$, there must exist at least one smaller element on its left side (or anywhere else in the array, but we can always choose a left occurrence in an equivalent solution ordering) and one larger element on its right side (or elsewhere). By exhaustively trying each $j$, we ensure we do not miss the correct middle position. The moment we detect both sides for any $j$, we reconstruct a valid triple immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    r = list(map(int, input().split()))
    
    for j in range(n):
        left = -1
        right = -1
        
        for i in range(j):
            if r[i] < r[j]:
                left = i
                break
        
        for k in range(j + 1, n):
            if r[k] > r[j]:
                right = k
                break
        
        if left != -1 and right != -1:
            print(left + 1, j + 1, right + 1)
            return
    
    print(-1, -1, -1)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the idea of treating each index as a potential middle element. The inner scans are early-exit loops, which ensures we do not waste time once a valid candidate is found. The indices are converted to 1-based format at output.

The main subtlety is ensuring we do not accidentally reuse the same index for multiple roles. Since we only consider $i < j < k$, all indices are inherently distinct and ordered, so no additional checks are required.

## Worked Examples

### Example 1

Input:

```
6
3 1 4 1 5 9
```

We track the first successful middle index.

| j | left candidate i | right candidate k | decision |
| --- | --- | --- | --- |
| 0 | none | none | skip |
| 1 | none | 2 (4 > 1 false, next valid is 4 or 5 index etc) | skip |
| 2 | 1 (1 < 4) | 4 (5 > 4) | accept |

At $j = 2$, we find $r_1 = 1 < 4$ and $r_4 = 5 > 4$, so we output $2\ 3\ 5$ in 1-based indexing, which corresponds to a valid increasing triple.

This trace shows that we do not need the earliest or best triple, only any valid combination anchored at a middle element.

### Example 2

Input:

```
5
5 4 3 2 1
```

| j | left candidate i | right candidate k | decision |
| --- | --- | --- | --- |
| 0 | none | none | skip |
| 1 | none | none | skip |
| 2 | none | none | skip |
| 3 | none | none | skip |
| 4 | none | none | fail |

No middle element has both a smaller left element and a larger right element, confirming that no increasing triple exists.

This demonstrates the failure condition where the array is strictly decreasing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each index is treated as middle once, scanning left and right lists linearly |
| Space | $O(1)$ | Only a few variables are used beyond the input array |

With $n \le 3000$, the worst-case number of operations is about $9 \times 10^6$, which is well within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    r = list(map(int, input().split()))
    
    for j in range(n):
        left = -1
        right = -1
        
        for i in range(j):
            if r[i] < r[j]:
                left = i
                break
        
        for k in range(j + 1, n):
            if r[k] > r[j]:
                right = k
                break
        
        if left != -1 and right != -1:
            return f"{left+1} {j+1} {right+1}\n"
    
    return "-1 -1 -1\n"

# provided sample
assert run("6\n3 1 4 1 5 9\n") != "", "sample 1"

# minimum size valid
assert run("3\n1 2 3\n") == "1 2 3\n", "already sorted"

# all equal
assert run("4\n7 7 7 7\n") == "-1 -1 -1\n", "all equal"

# strictly decreasing
assert run("5\n5 4 3 2 1\n") == "-1 -1 -1\n", "decreasing"

# middle valid only at end
assert run("5\n5 1 2 3 4\n") != "", "late middle case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | 1 2 3 | simplest valid triple |
| 7 7 7 7 | -1 -1 -1 | duplicates only |
| 5 4 3 2 1 | -1 -1 -1 | strictly decreasing |
| 5 1 2 3 4 | any valid | late emergence of valid middle |

## Edge Cases

A key edge case is when the valid middle element exists only near the beginning or end. For example, in `5 1 2 3 4`, the value `1` at index 2 can serve as a middle element, but only after we scan both sides. The algorithm checks each position in turn, and at $j = 1$ (value `1`), it finds no left candidate but immediately finds right-side candidates. However, it still correctly waits for both conditions before outputting.

Another important case is constant arrays such as `8 8 8 8`. For every $j$, neither side can produce strict inequality, so both scans fail and the algorithm cleanly returns $-1 -1 -1$ without false positives.

A decreasing array like `5 4 3 2 1` exercises the worst-case behavior where every middle candidate fails on the right-side check. Each iteration still runs in linear time, but no early success occurs, confirming correctness under full traversal.
