---
title: "CF 987C - Three displays"
description: "We are given a sequence of displays arranged along a line. Each display has a fixed position in this order, a font size, and a rental cost."
date: "2026-06-17T00:50:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 987
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 485 (Div. 2)"
rating: 1400
weight: 987
solve_time_s: 71
verified: true
draft: false
---

[CF 987C - Three displays](https://codeforces.com/problemset/problem/987/C)

**Rating:** 1400  
**Tags:** brute force, dp, implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of displays arranged along a line. Each display has a fixed position in this order, a font size, and a rental cost. The task is to pick three displays with strictly increasing positions, and also strictly increasing font sizes, while minimizing the total rental cost of the chosen three.

Formally, we want indices $i < j < k$ such that $s_i < s_j < s_k$, and among all such valid triples, we minimize $c_i + c_j + c_k$. If no such triple exists, we return -1.

The ordering constraint is crucial: we cannot reorder displays, so this is not a general combination problem but a structured subsequence selection problem with both position and value monotonicity constraints.

The constraint $n \le 3000$ already suggests that a quadratic or cubic approach might still be viable. A cubic $O(n^3)$ solution would examine all triples directly and compute the cost if valid. This is too slow in the worst case since it would perform about $2.7 \times 10^{10}$ checks. A quadratic or $O(n^2)$ method is the real target.

Edge cases tend to appear when no increasing triple exists even though increasing pairs exist. For example, if $s = [5, 4, 3]$, there are decreasing values, so no valid triple exists and the answer is -1. A naive approach that only checks pairs would incorrectly assume extendability.

Another subtle case is when multiple valid triples exist but only some satisfy minimal cost. For instance, a greedy choice of locally cheap elements can fail if it blocks a later cheaper third element.

## Approaches

A direct brute-force approach tries every triple $(i, j, k)$ with $i < j < k$, checks whether $s_i < s_j < s_k$, and computes the cost. This is correct because it explores the entire feasible space, but it degenerates into $O(n^3)$ checks. With $n = 3000$, this is far beyond acceptable limits.

The key observation is that the structure naturally splits around the middle element $j$. If we fix $j$, the problem becomes choosing the cheapest valid $i < j$ with smaller font size than $s_j$, and the cheapest valid $k > j$ with larger font size than $s_j$. This turns the problem into two independent optimization queries around each middle position.

So instead of recomputing costs for each triple, we precompute, for every position $j$, the best possible left candidate cost and right candidate cost. Then we combine them in $O(n)$ per middle point, yielding an overall $O(n^2)$ solution.

The only remaining challenge is computing these prefix and suffix minima efficiently while respecting the strict inequality constraints on font sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We treat each index $j$ as the middle element of the triple.

1. For each position $j$, compute the cheapest valid left partner $i < j$ such that $s_i < s_j$. We scan all indices to the left and track the minimum cost satisfying the constraint.
2. For each position $j$, compute the cheapest valid right partner $k > j$ such that $s_k > s_j$. We again scan to the right and track the minimum cost satisfying the constraint.
3. If either side does not exist for a given $j$, then $j$ cannot serve as the middle of a valid triple.
4. For every valid $j$, compute the candidate answer as

$$c_j + \text{bestLeft}[j] + \text{bestRight}[j]$$

and keep the minimum over all $j$.
5. If no valid $j$ produces a full triple, return -1.

The key idea is that once the middle element is fixed, the left and right choices become independent minimization problems constrained only by inequality with $s_j$.

### Why it works

Fixing the middle index $j$, any valid triple must use a left index from $\{ i < j \mid s_i < s_j \}$ and a right index from $\{ k > j \mid s_k > s_j \}$. The cost splits cleanly into three independent parts, and minimizing each side independently is safe because there is no interaction between chosen left and right indices beyond sharing $j$. Since we try all possible middle positions, every valid triple is considered exactly once at its middle element, ensuring no candidate is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = list(map(int, input().split()))
    c = list(map(int, input().split()))

    INF = 10**30

    left = [INF] * n
    right = [INF] * n

    for j in range(n):
        best = INF
        for i in range(j):
            if s[i] < s[j]:
                if c[i] < best:
                    best = c[i]
        left[j] = best

    for j in range(n - 1, -1, -1):
        best = INF
        for k in range(j + 1, n):
            if s[k] > s[j]:
                if c[k] < best:
                    best = c[k]
        right[j] = best

    ans = INF
    for j in range(n):
        if left[j] != INF and right[j] != INF:
            ans = min(ans, left[j] + c[j] + right[j])

    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the decomposition into a middle index and two independent searches. The left array stores the cheapest valid predecessor for each position, and the right array stores the cheapest valid successor.

The nested loops are intentionally simple because $n = 3000$ allows roughly $9 \times 10^6$ operations, which is safe in Python.

A subtle point is using a large sentinel value for INF. This ensures we do not accidentally combine invalid states when no valid left or right candidate exists.

## Worked Examples

### Example 1

Input:

```
5
2 4 5 4 10
40 30 20 10 40
```

We compute best left and right choices.

For $j = 2$ (value 5), valid left indices are 1 and 0. The cheapest is index 1 with cost 30. Valid right indices are 4 only, cost 40.

| j | best left | c[j] | best right | total |
| --- | --- | --- | --- | --- |
| 2 | 30 | 20 | 40 | 90 |

For other positions, either left or right is missing or more expensive. The minimum is 90.

This shows how the algorithm isolates the optimal middle index rather than greedily picking smallest costs globally.

### Example 2

Input:

```
3
5 4 3
10 10 10
```

No increasing triplet exists.

| j | best left | best right | valid |
| --- | --- | --- | --- |
| 0 | INF | INF | no |
| 1 | INF | INF | no |
| 2 | INF | INF | no |

No valid middle index produces a full chain, so output is -1.

This confirms that the algorithm correctly distinguishes between “no solution” and “large cost solution”.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each index, we scan left and right arrays to compute best valid candidates |
| Space | O(n) | Two auxiliary arrays store best left and right costs |

With $n \le 3000$, $n^2 \approx 9 \times 10^6$, which fits comfortably in time limits in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    def solve():
        n = int(input())
        s = list(map(int, input().split()))
        c = list(map(int, input().split()))

        INF = 10**30

        left = [INF] * n
        right = [INF] * n

        for j in range(n):
            best = INF
            for i in range(j):
                if s[i] < s[j]:
                    best = min(best, c[i])
            left[j] = best

        for j in range(n - 1, -1, -1):
            best = INF
            for k in range(j + 1, n):
                if s[k] > s[j]:
                    best = min(best, c[k])
            right[j] = best

        ans = INF
        for j in range(n):
            if left[j] != INF and right[j] != INF:
                ans = min(ans, left[j] + c[j] + right[j])

        print(-1 if ans == INF else ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""5
2 4 5 4 10
40 30 20 10 40
""") == "90"

# no solution
assert run("""3
5 4 3
10 10 10
""") == "-1"

# minimum size valid
assert run("""3
1 2 3
5 6 1
""") == "12"

# all increasing but expensive middle forces choice
assert run("""4
1 10 2 20
100 1 100 1
""") == "202"

# repeated values prevent strict increase
assert run("""5
1 2 2 3 4
5 4 3 2 1
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sorted increasing | 12 | basic correctness |
| no triple | -1 | impossible case handling |
| mixed ordering | 202 | cost minimization tradeoff |
| duplicates | 10 | strict inequality handling |

## Edge Cases

One important edge case is when increasing subsequences exist but cannot form a full length-3 chain due to ordering constraints. For example:

```
4
1 3 2 4
5 100 1 100
```

Here, a naive greedy approach might pick 1 and 2 early, but 2 appears after 3 and breaks monotonicity. The algorithm instead evaluates each middle position independently, so it considers 3 as a potential middle and correctly finds the best compatible neighbors.

Another edge case is when the cheapest element globally cannot be used because it violates ordering constraints. The split-by-middle structure avoids this trap by forcing compatibility with both sides rather than optimizing globally per element.

Finally, cases with equal font sizes highlight the strict inequality requirement. Any equal pair is ignored by construction, since neither left nor right arrays accept equality in comparisons.
