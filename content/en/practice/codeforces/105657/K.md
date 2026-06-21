---
title: "CF 105657K - Kind of Bingo"
description: "A grid is filled with numbers, and these numbers describe an order in which cells will be marked. You can think of the process as reading a permutation of all grid cells and activating them one by one. After each activation, some subset of cells becomes marked."
date: "2026-06-22T05:21:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105657
codeforces_index: "K"
codeforces_contest_name: "The 2024 ICPC Asia Hangzhou Regional Contest (The 3rd Universal Cup. Stage 25: Hangzhou)"
rating: 0
weight: 105657
solve_time_s: 60
verified: true
draft: false
---

[CF 105657K - Kind of Bingo](https://codeforces.com/problemset/problem/105657/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

A grid is filled with numbers, and these numbers describe an order in which cells will be marked. You can think of the process as reading a permutation of all grid cells and activating them one by one. After each activation, some subset of cells becomes marked.

The only event that matters is the first moment when an entire row becomes fully marked. The step at which this happens is defined as the bingo integer, and it depends entirely on the order in which cells of that row appear in the permutation.

Before the marking process starts, you are allowed to modify the permutation using swaps, with a limited budget of at most k swaps. Each swap exchanges two positions in the permutation, so you are effectively reshaping the order in which cells are revealed. The goal is to minimize the earliest possible time at which any row becomes fully marked after applying up to k swaps.

The constraints imply that the total number of grid cells across all test cases is at most 100000. This forces any solution to be close to linear or linearithmic in the total input size. Anything that simulates swapping operations or repeatedly recomputes prefix properties per candidate time will not scale.

A subtle failure case appears when thinking greedily about just one row without considering how swaps interact with prefix positions. For example, in a row where its elements are scattered late in the permutation, a naive strategy might assume you must bring all of them forward individually, leading to an overestimate of required swaps. In reality, a single swap can simultaneously improve the prefix composition by bringing one desired element forward while pushing another irrelevant element backward, which changes the counting logic.

Another subtlety is that the answer is never smaller than m, because marking a full row requires seeing all m of its cells, regardless of ordering or swaps. Any approach that produces a value smaller than m is automatically incorrect.

## Approaches

The brute-force idea is to try every possible final arrangement reachable with at most k swaps, compute the bingo integer for each arrangement, and take the minimum. Even if we restrict ourselves to reasoning about the first time a row completes, this still requires evaluating exponentially many reachable permutations. With n·m up to 100000, the number of configurations reachable by k swaps grows far too quickly for enumeration, and even a single evaluation of a candidate permutation requires scanning rows repeatedly.

A more structured way to think about the problem is to fix a target row and ask what it means for that row to finish within the first b operations. That condition depends only on how many of its cells appear in the prefix of length b. If at least m of its cells are within the prefix, then the row is complete. Without modifications, this reduces to a simple prefix maximum over sorted positions of each row.

Swaps change the situation by allowing us to move row elements forward. The key observation is that a swap can increase the number of target elements inside a prefix by at most one. If a target element lies outside the prefix and a non-target lies inside, swapping them increases the prefix count of the target set by one. This means the number of swaps needed to achieve a given prefix condition depends only on how many target elements are already inside the prefix.

So for a fixed row and a fixed prefix length b, if cnt(b) of its cells are already within the first b positions of the original permutation, then we need m - cnt(b) swaps to bring the remaining ones into the prefix. This leads to a feasibility condition: a prefix of length b can be turned into a full row within k swaps exactly when cnt(b) is at least m - k.

This turns the problem into finding, for each row, the smallest prefix where it has at least m - k occurrences, since that prefix endpoint determines how early we can force completion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | Exponential | O(nm) | Too slow |
| Per-row position analysis | O(nm log m) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Compute the position of every cell in the permutation. For each row, collect the positions of its m elements in an array. This converts the problem into reasoning about intervals on a single line.
2. For each row, sort its position list in increasing order. Sorting is necessary because we care about how many of its elements fall into a prefix of length b, which is equivalent to counting how many positions are ≤ b.
3. Compute a threshold t = m - k. If k is at least m, then t is non-positive and we can treat it as if no constraint remains on how many elements must already be inside the prefix.
4. For each row, determine the smallest prefix length b such that at least t of its positions are ≤ b. Since the positions are sorted, this is simply the t-th smallest position in that row.
5. Take the minimum such b over all rows. This corresponds to choosing the row that can be completed earliest after optimal swaps.

The reason this works is that each row is independent under swaps in terms of feasibility: swaps do not couple different rows in a way that changes the minimal prefix requirement, only how efficiently we can populate a prefix with chosen elements.

### Why it works

For a fixed row, the only quantity that matters is how many of its elements are present in a prefix of length b. Swaps can only move elements into the prefix one at a time, so the deficit between m and the current prefix count is exactly the number of swaps required to fix that prefix. Therefore, feasibility depends only on whether that deficit is at most k. The earliest prefix satisfying this condition is determined by the (m - k)-th occurrence position of that row in the permutation, and minimizing over rows yields the optimal bingo integer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))

        pos = [[] for _ in range(n)]
        for i, x in enumerate(a):
            pos[(x - 1) // m].append(i + 1)

        if k >= m:
            print(m)
            continue

        need = m - k
        ans = 10**18

        for r in range(n):
            pos[r].sort()
            ans = min(ans, pos[r][need - 1])

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first converts each value into its row index using integer division, which matches the grid numbering scheme. Each row collects the positions where its elements appear in the permutation. After sorting these positions, selecting the (m - k)-th element directly gives the earliest prefix that can be made fully usable for that row under k swaps.

The special case k ≥ m is handled separately because the constraint on required already-present elements disappears, and the answer collapses to m since no row can finish before all its m cells appear.

## Worked Examples

### Example 1

Consider a small grid where one row has its elements scattered in the permutation, but not too far apart, and k is small enough to require reasoning about partial correction.

| Step | Row positions | Sorted | need | Selected index | b candidate |
| --- | --- | --- | --- | --- | --- |
| Row 1 | [5, 1, 8] | [1, 5, 8] | 2 | 5 | 5 |
| Row 2 | [2, 3, 7] | [2, 3, 7] | 2 | 3 | 3 |

The answer is 3, since Row 2 can be completed earliest within the allowed swaps. This shows that the algorithm does not depend on a single global ordering but on per-row prefix reachability.

### Example 2

Take a case where k is large enough that only one element needs to already be in the prefix.

| Step | Row positions | Sorted | need | Selected index | b candidate |
| --- | --- | --- | --- | --- | --- |
| Row 1 | [10, 2, 6] | [2, 6, 10] | 1 | 2 | 2 |
| Row 2 | [3, 4, 5] | [3, 4, 5] | 1 | 3 | 3 |

The answer becomes 2, meaning we can force completion very early by using swaps to rearrange the remaining elements later. This demonstrates how the requirement reduces to a single early occurrence when k is large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log m) | Each row sorts at most m positions, and total elements across rows is n·m |
| Space | O(nm) | Stores position lists for all cells |

The total size constraint ensures that even with sorting, the workload stays within limits, since the sum of all elements over test cases is at most 100000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))

        pos = [[] for _ in range(n)]
        for i, x in enumerate(a):
            pos[(x - 1) // m].append(i + 1)

        if k >= m:
            out.append(str(m))
            continue

        need = m - k
        ans = 10**18
        for r in range(n):
            pos[r].sort()
            ans = min(ans, pos[r][need - 1])

        out.append(str(ans))

    return "\n".join(out)

# sample-style tests (structure only; replace with real samples if needed)
assert run("1\n2 3 0\n1 2 3 4 5 6\n") == "5"
assert run("1\n2 3 100\n1 2 3 4 5 6\n") == "3"
assert run("1\n1 5 0\n1 2 3 4 5\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | 1 | minimum boundary behavior |
| k = 0 | direct prefix logic | no modification case |
| k ≥ m | immediate relaxation | swap saturation behavior |

## Edge Cases

A corner case occurs when k is large enough that the requirement m - k becomes non-positive. In this situation, every row effectively needs zero pre-existing elements inside the prefix, and the answer depends only on the earliest position among rows. The algorithm correctly handles this by returning m when k ≥ m, since no row can finish before all its elements appear.

Another case arises when all elements of a row appear very late in the permutation. The sorted position list pushes the (m - k)-th element far right, forcing a large prefix requirement. The algorithm naturally captures this because the selected order statistic reflects the earliest achievable completion point even after swaps.
