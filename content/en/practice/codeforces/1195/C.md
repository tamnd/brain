---
title: "CF 1195C - Basketball Exercise"
description: "We are given two horizontal lines of students, each line containing the same number of people. Each student has a height, and we want to build a team by selecting students from these two rows under a strict ordering rule: once we start selecting from left to right, we can never…"
date: "2026-06-12T00:13:43+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1195
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 574 (Div. 2)"
rating: 1400
weight: 1195
solve_time_s: 83
verified: true
draft: false
---

[CF 1195C - Basketball Exercise](https://codeforces.com/problemset/problem/1195/C)

**Rating:** 1400  
**Tags:** dp  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two horizontal lines of students, each line containing the same number of people. Each student has a height, and we want to build a team by selecting students from these two rows under a strict ordering rule: once we start selecting from left to right, we can never move backward in index, and we are also forbidden from picking two consecutive students from the same row.

This creates a constrained sequence problem over two parallel arrays. At each step, we choose a next student either from the top or bottom row, but only if their column index is strictly greater than the last chosen student’s index, and the row alternates from the previous pick.

The goal is to maximize the sum of heights of the chosen students.

The constraint $n \le 10^5$ immediately rules out any exponential or quadratic dynamic programming over pairs of positions. Any solution that tries to consider all sequences or all transitions explicitly between all pairs of indices would be too slow. We need a linear or near-linear approach.

A subtle difficulty is that we are not forced to pick adjacent columns. We may skip columns entirely, which means that at every step we are essentially choosing the best future candidate among all valid positions in the opposite row. A naive greedy choice like always picking the taller of the two available next students fails because a locally optimal choice can block access to a better alternating chain later.

A typical failure scenario is when a slightly smaller immediate pick allows access to a much larger future sequence in the other row. For example, choosing a large value early in one row may force you into a sequence of small values later, whereas waiting a bit and switching rows earlier yields a higher total.

This structure suggests that the decision at each row depends on the best continuation starting from future indices, which is a classic signal for dynamic programming over positions.

## Approaches

A brute-force solution would attempt to simulate all valid alternating sequences starting from every possible first choice. From each starting cell, we branch to every valid next cell in the opposite row with a higher index, accumulating sums. This explores an exponentially large state space because from each position we can jump to many future positions in the opposite row, and each of those leads to further branching. Even pruning does not prevent worst-case blowup, since valid sequences can still be extremely numerous.

The key observation is that once we fix that we are currently at column $i$ in one row, the only relevant future choices are in the opposite row at indices greater than $i$. Among all those future choices, we only ever care about the best possible continuation starting from that index. This suggests precomputing optimal suffix values.

Let us define two DP arrays: $dp_1[i]$ is the best sum we can obtain if the last chosen student is at row 1, column $i$. Similarly, $dp_2[i]$ is defined for row 2.

If we are at $dp_1[i]$, the next choice must come from row 2 at some index $j > i$. The best continuation from $j$ is already encoded in $dp_2[j]$. So we want:

$$dp_1[i] = h_{1,i} + \max_{j > i} dp_2[j]$$

and similarly:

$$dp_2[i] = h_{2,i} + \max_{j > i} dp_1[j]$$

This structure allows us to compute DP from right to left while maintaining running suffix maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal DP with suffix maxima | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create two arrays $dp_1$ and $dp_2$, initially filled with zeros. These represent the best achievable sums starting from each position when that position is chosen as the last pick in its row.
2. Also maintain two running variables `best1` and `best2`, representing the maximum value of $dp_1[j]$ and $dp_2[j]$ for all indices $j > i$. These encode the suffix maxima needed for transitions.
3. Traverse indices from right to left, starting from $i = n-1$ down to $0$. This ordering ensures that when we compute state $i$, all states to the right are already known.
4. At each index $i$, compute:

$dp_1[i] = h_{1,i} + best2$ and $dp_2[i] = h_{2,i} + best1$. This directly applies the transition rule using already computed best continuations.
5. After computing both values for index $i$, update `best1` and `best2` using $dp_1[i]$ and $dp_2[i]$. This ensures that future (leftward) states can use the correct suffix information.
6. After processing all indices, the answer is the maximum among all $dp_1[i]$ and $dp_2[i]$, since the first chosen student can start anywhere.

### Why it works

The correctness hinges on the fact that every valid alternating sequence has a well-defined first chosen index and then strictly decreasing sequence of “remaining suffix choices” in terms of DP dependence. At any position $i$, the best continuation after switching rows depends only on optimal continuations starting strictly to the right. By processing from right to left, we guarantee that every suffix choice has already been optimally resolved, so each DP state is computed with complete knowledge of all valid continuations. This ensures that no future improvement can invalidate a computed state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    dp1 = [0] * n
    dp2 = [0] * n

    best1 = 0
    best2 = 0

    for i in range(n - 1, -1, -1):
        dp1[i] = a[i] + best2
        dp2[i] = b[i] + best1

        if dp1[i] > best1:
            best1 = dp1[i]
        if dp2[i] > best2:
            best2 = dp2[i]

    print(max(best1, best2))

if __name__ == "__main__":
    solve()
```

The code directly implements the suffix DP described earlier. The arrays `dp1` and `dp2` store optimal values starting from each index, but in practice we only need them to update suffix maxima. The variables `best1` and `best2` compress the DP table into O(1) memory per row.

The reverse iteration is essential because it guarantees that when we compute position $i$, all states $j > i$ have already been incorporated into the suffix maxima. The final answer takes the best starting point across both rows.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [9, 3, 5, 7, 3]
b = [5, 8, 1, 4, 5]
```

We process from right to left.

| i | dp1[i] | dp2[i] | best1 | best2 |
| --- | --- | --- | --- | --- |
| 4 | 3 + 0 = 3 | 5 + 0 = 5 | 3 | 5 |
| 3 | 7 + 5 = 12 | 4 + 3 = 7 | 12 | 7 |
| 2 | 5 + 7 = 12 | 1 + 12 = 13 | 12 | 13 |
| 1 | 3 + 13 = 16 | 8 + 12 = 20 | 16 | 20 |
| 0 | 9 + 20 = 29 | 5 + 16 = 21 | 29 | 21 |

Final answer is 29.

This trace shows how suffix contributions accumulate: each position benefits from the best continuation on the opposite row strictly to its right.

### Example 2

Input:

```
n = 3
a = [1, 100, 1]
b = [1, 1, 100]
```

| i | dp1[i] | dp2[i] | best1 | best2 |
| --- | --- | --- | --- | --- |
| 2 | 1 + 0 = 1 | 100 + 0 = 100 | 1 | 100 |
| 1 | 100 + 100 = 200 | 1 + 1 = 2 | 200 | 100 |
| 0 | 1 + 100 = 101 | 1 + 200 = 201 | 201 | 101 |

Answer is 201.

This case highlights why greedy fails: picking the 100 early in row 1 allows access to a 100 later in row 2, producing a higher alternating chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once with constant-time transitions |
| Space | O(n) | DP arrays are allocated per row, though they can be compressed further |

The linear complexity is sufficient for $n \le 10^5$, and memory usage stays well within limits since we only store a few arrays of size $n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    dp1 = [0] * n
    dp2 = [0] * n
    best1 = best2 = 0

    for i in range(n - 1, -1, -1):
        dp1[i] = a[i] + best2
        dp2[i] = b[i] + best1
        best1 = max(best1, dp1[i])
        best2 = max(best2, dp2[i])

    return str(max(best1, best2))

# provided sample
assert run("5\n9 3 5 7 3\n5 8 1 4 5\n") == "29"

# minimum size
assert run("1\n10\n20\n") == "20"

# all equal
assert run("4\n5 5 5 5\n5 5 5 5\n") == "20"

# alternating dominance
assert run("3\n1 100 1\n1 1 100\n") == "201"

# increasing only top
assert run("3\n1 2 3\n3 2 1\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | max single pick | base case correctness |
| all equal | full alternating chain | uniform DP behavior |
| mixed peaks | long-range dependency | suffix transitions |
| asymmetric rows | non-greedy optimal path | correctness of DP choice |

## Edge Cases

A key edge case is when the optimal solution starts in the second row rather than the first. The algorithm handles this naturally because it computes both $dp_1[i]$ and $dp_2[i]$ symmetrically and takes the global maximum at the end. For instance, if row 2 has a large value at position 0 and row 1 is weak, the DP still captures it since $dp_2[0]$ can directly contribute to the answer without requiring a prior pick.

Another subtle case is when skipping many indices is necessary to reach a high-value alternation. Since transitions only depend on suffix maxima, skipping is implicitly handled: `best1` and `best2` aggregate the best achievable continuation over all future positions, so the DP does not force adjacency and correctly evaluates sparse optimal sequences.
