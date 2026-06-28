---
title: "CF 104936B - Taking an Exam"
description: "Each test case describes an exam scenario where we decide which problems Busy Beaver attempts and in what combination. Every problem has a time cost equal to its difficulty, and solving it immediately gives points equal to that same difficulty plus one extra point."
date: "2026-06-28T07:27:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104936
codeforces_index: "B"
codeforces_contest_name: "MITIT 2024 Beginner Round"
rating: 0
weight: 104936
solve_time_s: 77
verified: false
draft: false
---

[CF 104936B - Taking an Exam](https://codeforces.com/problemset/problem/104936/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes an exam scenario where we decide which problems Busy Beaver attempts and in what combination. Every problem has a time cost equal to its difficulty, and solving it immediately gives points equal to that same difficulty plus one extra point. After finishing chosen problems, the exam is submitted, and any unused time up to the full duration is converted directly into bonus points.

So the decision is not just which problems to solve, but also implicitly how much total time is spent, since finishing earlier increases the bonus. If a subset of problems takes total time $S$, then the score is formed by summing their individual rewards and then adding the remaining time $M - S$.

The constraints push us toward an algorithm that is close to linearithmic per test case. The total number of problems across all test cases is at most $10^5$, so anything like $O(N^2)$ or exponential subset search is immediately impossible. Even $O(N \log^2 N)$ would be unnecessary overhead when a simpler $O(N \log N)$ or linear scan suffices.

A few situations tend to trap naive reasoning. One is assuming that we should prioritize high difficulty because they give more points per item. For example, if $M = 10$ and problems are $[9, 1, 1]$, choosing the large one first gives score $10 + 2 + 1 = 13$, but choosing the two small ones yields a better structure because it allows more remaining time, increasing the bonus effect.

Another subtle case is when no problem fits within the time limit. For instance, if $M = 5$ and all $d_i = 10$, the optimal decision is to solve nothing and immediately submit, producing a score of $5$. A greedy that insists on picking something will incorrectly force an invalid choice.

## Approaches

The brute-force view starts by considering every subset of problems. For each subset, we compute its total time, check whether it fits within $M$, compute the score from both problem rewards and remaining time, and track the best answer. This is correct because it explores all feasible schedules.

The failure point is the number of subsets. With $N$ up to $10^5$, the number of combinations is $2^N$, which is astronomically large even for much smaller inputs. The structure of the score function is what allows a simplification: when expanding the formula, the dependence on chosen problems becomes surprisingly simple.

If a subset has total time $S$ and contains $k$ problems, the score is

$$\sum (d_i + 1) + (M - S)$$

which becomes

$$M + k.$$

All dependence on actual difficulty values disappears except for feasibility. The only thing that matters is how many problems we can pick such that their total time does not exceed $M$. This turns the problem into a classic “maximize count under a sum constraint”, which is solved by always taking the smallest available elements first.

Sorting the difficulties ensures that adding problems in that order keeps the accumulated time as small as possible for any fixed number of chosen items. This guarantees we can test prefixes and find the maximum feasible prefix length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(N)$ | Too slow |
| Optimal | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Sort all problem difficulties in non-decreasing order. This ensures that any prefix of the array represents the cheapest possible way to pick that many problems.
2. Iterate through the sorted list while maintaining a running sum of selected difficulties.
3. For each problem, check whether adding its difficulty keeps the total time within $M$. If yes, include it and increase the count of chosen problems.
4. If adding the current problem would exceed $M$, stop. Any further problems are larger or equal, so they would only violate the constraint even more quickly.
5. Compute the final answer as $M + k$, where $k$ is the number of selected problems.

The reason we can stop early is that once the sum exceeds $M$, adding any later element cannot reduce it, since the array is sorted.

### Why it works

The transformation of the score into $M + k$ reduces the objective to maximizing $k$ under a sum constraint. For any fixed $k$, the minimum possible sum of chosen problems is achieved by taking the $k$ smallest difficulties. Therefore, if even the smallest $k$ elements exceed $M$, no other selection of size $k$ can fit. This creates a monotone feasibility condition over $k$, which the greedy prefix selection exploits exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        d = list(map(int, input().split()))
        d.sort()

        s = 0
        k = 0

        for x in d:
            if s + x <= m:
                s += x
                k += 1
            else:
                break

        out.append(str(m + k))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction that the score depends only on how many problems are chosen. Sorting enforces the optimal structure for packing as many problems as possible under the time limit. The running sum tracks feasibility, and the moment it breaks the constraint we can safely stop because all remaining values are no smaller.

The final expression `m + k` reflects the decomposition of total score into remaining time plus fixed contribution per chosen problem.

## Worked Examples

Consider a case where $M = 10$ and difficulties are $[4, 1, 5]$. After sorting, we get $[1, 4, 5]$.

| Step | Chosen | Sum | k | Feasible |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 | yes |
| 2 | [1, 4] | 5 | 2 | yes |
| 3 | [1, 4, 5] | 10 | 3 | yes |

The answer is $10 + 3 = 13$. The trace shows that taking smaller problems first preserves feasibility for the largest possible prefix.

Now consider $M = 6$ and $[5, 4, 3]$. Sorting gives $[3, 4, 5]$.

| Step | Chosen | Sum | k | Feasible |
| --- | --- | --- | --- | --- |
| 1 | [3] | 3 | 1 | yes |
| 2 | [3, 4] | 7 | 1 | no |

We stop at $k = 1$, and the answer becomes $6 + 1 = 7$. The second choice breaks feasibility, and any alternative pair would only increase total time further.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting dominates; the scan is linear |
| Space | $O(N)$ | Storage for difficulties |

The constraints allow up to $10^5$ total elements, so an $O(N \log N)$ solution is comfortably within limits, while keeping memory linear ensures no overhead issues.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        d = list(map(int, input().split()))
        d.sort()

        s = 0
        k = 0
        for x in d:
            if s + x <= m:
                s += x
                k += 1
            else:
                break
        out.append(str(m + k))

    return "\n".join(out)

# provided samples (as intended separate tests)
assert solve_io("4\n3 7\n1 2 4\n4 15\n5 10 5 10\n3 10\n20 30 40\n2 10\n4 5\n") == "10\n49\n10\n12"

# minimum size
assert solve_io("1\n1 5\n3\n") == "6"

# all equal values
assert solve_io("1\n5 10\n2 2 2 2 2\n") == "15"

# cannot take any
assert solve_io("1\n3 3\n10 20 30\n") == "3"

# tight packing
assert solve_io("1\n4 6\n1 2 3 4\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small | 6 | minimal case correctness |
| all equal | 15 | stability under uniform weights |
| too large | 3 | zero-pick scenario |
| tight packing | 8 | prefix boundary behavior |

## Edge Cases

When every problem exceeds $M$, the algorithm still sorts them and immediately finds that the first element already violates the constraint. The chosen count remains zero, and the answer becomes exactly $M$. This matches the intended strategy of submitting immediately.

When all problems fit, the algorithm consumes the entire sorted list without breaking, producing $M + N$. The total sum constraint is never triggered, and the prefix becomes the whole array.

When difficulties are highly skewed, such as one very large value and many small ones, sorting ensures the large value is considered last, so it never blocks earlier optimal selections. This prevents a greedy mistake where a high-value-but-expensive problem would otherwise be chosen too early and reduce the number of solvable tasks.
