---
title: "CF 1873D - 1D Eraser"
description: "We are given a binary string representing a strip of cells, where each position is either black or white. The only operation allowed is choosing any contiguous segment of fixed length $k$ and repainting all cells in that segment to white."
date: "2026-06-08T23:14:17+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1873
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 898 (Div. 4)"
rating: 800
weight: 1873
solve_time_s: 92
verified: true
draft: false
---

[CF 1873D - 1D Eraser](https://codeforces.com/problemset/problem/1873/D)

**Rating:** 800  
**Tags:** greedy, implementation, two pointers  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing a strip of cells, where each position is either black or white. The only operation allowed is choosing any contiguous segment of fixed length $k$ and repainting all cells in that segment to white. The goal is to eliminate every black cell using as few such segment-repainting operations as possible.

The key observation is that each operation affects a contiguous window of size $k$, and multiple black cells inside that window can be cleared simultaneously. However, operations interact through overlap, so the problem is not about counting black cells, but about how optimally we can place these fixed-length “erasers” to cover all black positions.

The constraints allow up to $2 \cdot 10^5$ total characters across all test cases. This immediately rules out any solution that tries all possible windows for each black cell or simulates each operation naively over the string in quadratic time. An $O(n^2)$ approach would involve scanning or updating overlapping segments repeatedly and would not finish within time limits.

A few subtle edge cases appear in this problem.

If $k = 1$, each operation only clears one cell, so the answer is exactly the number of black cells. A naive sliding window idea might overcomplicate this case.

If the string has no black cells, the answer is zero. Any algorithm that assumes at least one operation is needed would incorrectly output a positive value.

If black cells appear consecutively in long blocks, a greedy method must ensure we do not overcount operations by applying overlapping erasures unnecessarily.

For example, in the string `BBBW` with $k = 3$, one operation at position 0 clears all three black cells. A careless approach that processes each black cell independently might apply multiple overlapping operations and overcount.

## Approaches

A brute-force approach would simulate every possible operation sequence. At each step, we could try choosing any window of size $k$ that covers at least one remaining black cell, apply it, and recurse. While this is correct in principle, the branching factor is large and the state space grows exponentially. Even a greedy variant that repeatedly scans for the best window and updates the string would degrade to $O(n^2)$ in worst cases where each operation only eliminates a small number of new black cells.

The structure of the operation suggests a more direct strategy. When we encounter a black cell, the only meaningful decision is to apply an operation that covers it. Since any operation affects a full segment of length $k$, the optimal choice is to use the leftmost uncovered black cell as an anchor and erase the segment starting there. Any operation that starts earlier or later either fails to cover this cell or wastes coverage on already-clean regions.

This leads to a simple greedy sweep: we move from left to right, and whenever we find a black cell that has not already been covered by a previous operation, we apply an operation starting at that position. This immediately clears that cell and all black cells within the next $k-1$ positions, so we can safely skip ahead.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Greedy Sweep | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process the string from left to right while maintaining how far the last applied operation extends.

1. Initialize a pointer $i = 0$ and a variable $covered = -1$, which tracks the rightmost index cleaned by previous operations.
2. Scan the string from left to right.
3. If $i \leq covered$, the current cell is already white due to a previous operation, so we move to the next index.
4. If $s[i] = 'B'$, this is an uncovered black cell, so we must apply a new operation starting at $i$.
5. Increment the answer counter and set $covered = i + k - 1$, representing the full range cleaned by this operation.
6. Continue scanning.

Each operation is forced at the first uncovered black cell because delaying it or shifting it right would leave this position unhandled.

### Why it works

The algorithm relies on the fact that every operation covers a fixed-length interval. Once we decide to cover the leftmost uncovered black cell at position $i$, any optimal solution must include at least one operation that covers $i$. Among all such operations, starting at $i$ is never worse than starting later because it maximizes coverage to the right while still fixing $i$. This creates a greedy choice property: once we fix the first uncovered black cell, we reduce the problem to a strictly smaller suffix that is independent of earlier decisions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()

    ans = 0
    covered = -1

    for i in range(n):
        if i <= covered:
            continue
        if s[i] == 'B':
            ans += 1
            covered = i + k - 1

    print(ans)
```

The key implementation detail is the `covered` pointer, which avoids explicitly modifying the string. Instead of simulating repainting, we record how far the last operation extends. This prevents unnecessary $O(k)$ updates per operation and keeps the solution linear.

The condition `i <= covered` ensures that we never reconsider positions already handled by a previous eraser. The check for `'B'` guarantees we only trigger operations when necessary.

## Worked Examples

### Example 1

Input: `n = 6, k = 3, s = WBWWWB`

We track the sweep step by step.

| i | s[i] | covered | Action | ans |
| --- | --- | --- | --- | --- |
| 0 | W | -1 | skip | 0 |
| 1 | B | -1 | apply, covered = 3 | 1 |
| 2 | W | 3 | skip | 1 |
| 3 | W | 3 | skip | 1 |
| 4 | W | 3 | skip | 1 |
| 5 | B | 3 | apply, covered = 7 | 2 |

This shows that a single operation can cover multiple nearby black cells, and only uncovered ones trigger new operations.

### Example 2

Input: `n = 5, k = 4, s = BWBWB`

| i | s[i] | covered | Action | ans |
| --- | --- | --- | --- | --- |
| 0 | B | -1 | apply, covered = 3 | 1 |
| 1 | W | 3 | skip | 1 |
| 2 | B | 3 | skip (covered) | 1 |
| 3 | W | 3 | skip | 1 |
| 4 | B | 3 | apply, covered = 7 | 2 |

The second black cell at index 2 is already removed by the first operation, even though it was not explicitly checked.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each position is visited once, and each operation is constant time |
| Space | $O(1)$ | Only a few integer variables are used |

The total input size across test cases is $2 \cdot 10^5$, so a linear scan per test case is sufficient and comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        s = sys.stdin.readline().strip()

        ans = 0
        covered = -1

        for i in range(n):
            if i <= covered:
                continue
            if s[i] == 'B':
                ans += 1
                covered = i + k - 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""8
6 3
WBWWWB
7 3
WWBWBWW
5 4
BWBWB
5 5
BBBBB
8 2
BWBWBBBB
10 2
WBBWBBWBBW
4 1
BBBB
3 2
WWW
""") == """2
1
2
1
4
3
4
0"""

# custom cases
assert run("""1
1 1
B
""") == "1", "single cell"

assert run("""1
5 5
BBBBB
""") == "1", "whole covered in one move"

assert run("""1
6 2
BBBBBB
""") == "3", "tight packing"

assert run("""1
6 3
WBWBWB
""") == "2", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `B, k=1` | 1 | minimal single-cell operation |
| all B, k=n | 1 | full coverage in one move |
| dense blocks, small k | 3 | correct packing behavior |
| alternating pattern | 2 | non-overlapping greedy correctness |

## Edge Cases

When $k = 1$, the algorithm naturally treats each black cell as requiring its own operation. Each uncovered `'B'` increments the answer and sets `covered = i`, so no skipping errors occur.

When there are no black cells, the loop never triggers an operation because the condition `s[i] == 'B'` is never satisfied. The result remains zero.

When black cells overlap heavily within a distance smaller than $k$, the first encountered black cell triggers an operation that automatically covers all of them. For example, `BBBW` with $k = 3$ sets `covered = 2`, skipping the rest without additional operations, which matches the optimal strategy.
