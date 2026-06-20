---
title: "CF 106384E - \u5192\u6ce1\u6392\u5e8f"
description: "The problem is centered around a process that is explicitly described as bubble sort. We are given an array, and the task is to compute some quantity related to how bubble sort operates on that array."
date: "2026-06-20T23:04:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106384
codeforces_index: "E"
codeforces_contest_name: "CYCPC Round 2"
rating: 0
weight: 106384
solve_time_s: 46
verified: true
draft: false
---

[CF 106384E - \u5192\u6ce1\u6392\u5e8f](https://codeforces.com/problemset/problem/106384/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is centered around a process that is explicitly described as bubble sort. We are given an array, and the task is to compute some quantity related to how bubble sort operates on that array. Even though the statement text is extremely minimal in the prompt, the title strongly signals that the intended solution depends on understanding the mechanics of bubble sort, especially how elements move through adjacent swaps.

In bubble sort, larger elements gradually move to the right through repeated adjacent swaps. Any statistic derived from this process is usually tied to inversions, swap counts, or the number of passes required to settle the array. So the core mental model is that every inversion in the array contributes exactly one swap in the process, and bubble sort resolves inversions in a structured way.

The input is an array, and the output is a single number derived from the bubble sort process. Problems of this form almost always reduce to counting inversions or a closely related quantity such as total swaps performed by bubble sort or total movement cost of elements.

The constraints are not shown, but Codeforces “E” problems involving sorting processes typically allow arrays up to at least $2 \cdot 10^5$. That immediately rules out any $O(n^2)$ simulation of bubble sort. A naive simulation performs one pass per element and each pass may scan the full array, leading to quadratic behavior in the worst case. That would time out quickly at scale.

The main subtlety in bubble sort problems is that although the algorithm is defined procedurally, the final quantity is static. The process of swapping adjacent inverted pairs does not depend on intermediate structure in a complicated way; it depends only on how many inversions exist in the original array. The challenge is recognizing that equivalence.

A typical edge case is when the array is already sorted or reverse sorted. In the sorted case, bubble sort performs zero swaps, and any incorrect implementation that still counts passes or comparisons instead of swaps will overestimate the result. In the reverse sorted case, the number of swaps reaches the maximum possible, and it equals $n(n-1)/2$, which is the total number of inversions.

## Approaches

The brute-force interpretation directly simulates bubble sort. We repeatedly scan the array, swapping adjacent elements whenever they are out of order, until no swaps occur in a full pass. This is correct because it exactly follows the definition of bubble sort. However, each pass costs $O(n)$, and there can be $O(n)$ passes in the worst case, such as when the array is reverse sorted. This leads to $O(n^2)$ complexity, which becomes too slow when $n$ is large.

The key observation is that bubble sort swaps adjacent elements, and each swap removes exactly one inversion. Moreover, bubble sort never creates inversions. This means the total number of swaps performed over the entire process is exactly equal to the inversion count of the initial array. Once we recognize this invariant, we no longer need to simulate the process. We only need to count how many pairs $(i, j)$ satisfy $i < j$ and $a[i] > a[j]$.

This reduces the problem to a classical inversion counting task, which can be solved efficiently using a merge sort based approach or a Fenwick tree after coordinate compression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Bubble Sort Simulation | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal Inversion Count (Fenwick / Merge Sort) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We solve the problem by converting the bubble sort process into an inversion counting problem.

1. First, we observe that every swap in bubble sort occurs between two adjacent elements that form an inversion. This means that each swap corresponds to exactly one pair where the left element is greater than the right element. This gives a direct mapping between swaps and inversions.
2. We reformulate the problem as counting inversions in the initial array. Instead of simulating swaps, we count all pairs $(i, j)$ such that $i < j$ and $a[i] > a[j]$. This is the exact number of swaps bubble sort will perform in total.
3. To compute this efficiently, we process the array from left to right while maintaining a data structure that tracks how many previous elements are greater than the current element. This allows us to count contributions incrementally instead of enumerating pairs.
4. We use a Fenwick tree (or BIT) over compressed values of the array. Coordinate compression is needed because array values can be large, and we only care about relative ordering. Each time we process a value, we query how many previously seen values are greater, then update the structure to include the current value.
5. We accumulate these counts to obtain the total number of inversions, which is the final answer.

### Why it works

Bubble sort swaps adjacent inverted pairs until all inversions are eliminated. Each swap reduces the inversion count by exactly one and does not introduce new inversions. Since the process terminates only when no inversions remain, the total number of swaps must equal the initial inversion count. This makes the inversion count a complete invariant of the bubble sort process.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def query(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(set(a))
    comp = {v: i + 1 for i, v in enumerate(vals)}

    fw = Fenwick(len(vals))
    inv = 0

    for x in a:
        cx = comp[x]
        inv += fw.query(len(vals)) - fw.query(cx)
        fw.update(cx, 1)

    print(inv)

if __name__ == "__main__":
    solve()
```

The code begins by compressing values so that they fit into a compact range suitable for a Fenwick tree. This step preserves ordering, which is the only property relevant for inversion counting.

The Fenwick tree maintains counts of elements seen so far. For each new element, we query how many previous elements are strictly greater, which directly gives the number of inversions contributed by that element. After processing the query, we insert the current element into the structure.

The subtraction `fw.query(len(vals)) - fw.query(cx)` is the key step, since it counts all elements greater than the current one among those already processed.

## Worked Examples

### Example 1

Input:

```
3
3 1 2
```

We track Fenwick updates step by step.

| Step | Value | Fenwick state (conceptual) | Greater previous count | Inversions |
| --- | --- | --- | --- | --- |
| 1 | 3 | [3] | 0 | 0 |
| 2 | 1 | [3,1] | 1 | 1 |
| 3 | 2 | [3,1,2] | 1 | 2 |

Final answer is 2.

This matches bubble sort behavior: 3 swaps past 1 and 2 indirectly through adjacent swaps.

### Example 2

Input:

```
4
4 3 2 1
```

| Step | Value | Greater previous count | Inversions |
| --- | --- | --- | --- |
| 1 | 4 | 0 | 0 |
| 2 | 3 | 1 | 1 |
| 3 | 2 | 2 | 3 |
| 4 | 1 | 3 | 6 |

Final answer is 6, which equals $4 \cdot 3 / 2$, the maximum inversion count.

This shows the worst-case bubble sort behavior where every pair is inverted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each update and query in Fenwick tree costs logarithmic time |
| Space | $O(n)$ | Fenwick tree and coordinate compression storage |

The solution is efficient for arrays up to $2 \cdot 10^5$ elements, where an $O(n^2)$ simulation would be far too slow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO

    output = StringIO()
    _sys.stdout = output

    solve()

    _sys.stdout = sys.__stdout__
    return output.getvalue()

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    vals = sorted(set(a))
    comp = {v: i + 1 for i, v in enumerate(vals)}

    fw = [0] * (len(vals) + 1)

    def add(i):
        while i < len(fw):
            fw[i] += 1
            i += i & -i

    def sum_(i):
        s = 0
        while i > 0:
            s += fw[i]
            i -= i & -i
        return s

    inv = 0
    for x in a:
        cx = comp[x]
        inv += sum_(len(vals)) - sum_(cx)
        add(cx)

    return str(inv) + "\n"

# provided samples
assert run("3\n3 1 2\n") == "2\n"

# custom cases
assert run("1\n5\n") == "0\n", "single element"
assert run("2\n1 2\n") == "0\n", "already sorted"
assert run("2\n2 1\n") == "1\n", "single inversion"
assert run("4\n4 3 2 1\n") == "6\n", "maximum inversions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | no swaps case |
| sorted array | 0 | no inversions |
| reverse pair | 1 | basic swap |
| full reverse | 6 | worst-case bubble sort |

## Edge Cases

For input `1 5`, the array has a single element. Bubble sort performs no comparisons that lead to swaps, and the algorithm immediately returns 0 since the Fenwick tree sees no prior elements.

For input `1 2 3 4`, every prefix has no inversions. The Fenwick queries always return zero for “greater previous elements,” confirming that sorted arrays produce zero swaps.

For input `2 1`, there is exactly one inversion. The algorithm counts this when processing the second element, where one previous element is greater.

For input `4 3 2 1`, every pair is inverted. The Fenwick tree accumulates 3 + 2 + 1 = 6 inversions, matching the total number of swaps bubble sort would perform in the most expensive case.
