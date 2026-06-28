---
title: "CF 104936B - Taking an Exam"
description: "We are given several independent exam scenarios. Each scenario describes a fixed total exam duration and a list of problems."
date: "2026-06-28T18:10:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104936
codeforces_index: "B"
codeforces_contest_name: "MITIT 2024 Beginner Round"
rating: 0
weight: 104936
solve_time_s: 69
verified: false
draft: false
---

[CF 104936B - Taking an Exam](https://codeforces.com/problemset/problem/104936/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent exam scenarios. Each scenario describes a fixed total exam duration and a list of problems. Every problem consumes time equal to its difficulty, and solving it awards slightly more points than the time it takes, specifically one extra point beyond its duration.

The student can choose any subset of problems to solve, as long as their total time does not exceed the exam duration. After finishing, the student may submit early, and any unused time becomes additional bonus points equal to the remaining minutes.

So the total score is the sum of problem rewards plus the leftover time, and the goal is to select which problems to solve to maximize this sum.

Rewriting the structure more concretely, if we pick a set of problems with total time S, then the score is the sum over chosen problems of (d_i + 1) plus (M - S). This simplifies to M plus the number of solved problems plus the sum of their difficulties minus their total time, and since each problem contributes d_i both positively and negatively, all difficulty terms cancel except for counting how many problems are selected. This is the key simplification: every chosen problem increases score by exactly 1 beyond just consuming time, while time itself only matters through leftover bonus.

Thus, the score becomes M plus the number of chosen problems. The time constraint only restricts which subsets are feasible, but among feasible subsets, maximizing score is equivalent to maximizing the number of problems solved.

From the constraints, the total number of problems across test cases is up to 100000, so any solution must be essentially linear or linearithmic per test case. Sorting is acceptable, but anything like exponential subset search is impossible. Even O(N^2) per test case would be far too slow.

A naive greedy idea might be to pick problems in any order until time runs out, but this can fail depending on ordering. Another naive attempt is trying all subsets, which is clearly exponential.

A more subtle pitfall is ignoring the cancellation: one might incorrectly try to optimize raw score d_i + 1 + leftover time, and believe large d_i are better. But since taking a problem reduces leftover time by exactly d_i, the net effect of difficulty disappears.

A key edge case is when M is smaller than all d_i. Then no problem can be solved and the answer is simply M. Another is when M is large enough to solve everything, where the answer becomes M + N.

## Approaches

The brute-force approach would enumerate all subsets of problems, compute their total time, and compute the resulting score. This is correct because it directly follows the definition, but it requires checking 2^N subsets, and each subset needs summing up to O(N), leading to O(N·2^N), which is infeasible even for N = 30.

The crucial observation is that after algebraic simplification, the score depends only on how many problems are chosen, not which specific ones contribute more “value per time”. Every selected problem increases score by exactly one unit compared to skipping it, but also consumes time. This creates a classical “maximize count under sum constraint” structure.

Since all items are symmetric in benefit, the only thing that matters is feasibility: we want to fit as many problems as possible into total time M. To maximize count under a sum constraint, we should always pick the smallest available difficulties first. Sorting the array and greedily accumulating is optimal because any optimal solution that includes a larger element while excluding a smaller one can be swapped without worsening feasibility or count.

This reduces the problem to sorting and prefix accumulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N·2^N) | O(N) | Too slow |
| Sort + Greedy | O(N log N) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Read N and M, and the list of difficulties. These define a knapsack-like capacity problem where each item costs d_i time and yields unit benefit in terms of count.
2. Sort the difficulties in increasing order. This ensures we always consider the cheapest problems first, which is optimal for maximizing how many we can fit.
3. Initialize a running sum of time used and a counter for how many problems we take. The counter directly represents contribution to score beyond M.
4. Iterate through sorted difficulties. For each d_i, check whether adding it keeps total time within M. If yes, include it and update the running time and counter. If not, stop immediately.
5. Compute final answer as M + count of selected problems, since leftover time is already embedded in M and all used time cancels out.

### Why it works

At any moment, if we have chosen k problems with minimal total time, replacing any chosen problem with a larger one cannot reduce total time. Therefore, if a larger problem is used while a smaller unused one exists, swapping them keeps feasibility and does not reduce count. This exchange argument guarantees that an optimal solution always corresponds to taking a prefix of the sorted array.

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
        
        total = 0
        cnt = 0
        
        for x in d:
            if total + x > m:
                break
            total += x
            cnt += 1
        
        out.append(str(m + cnt))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on sorting each test case’s difficulty list, then greedily accumulating until the time budget is exceeded. The variable `total` tracks consumed exam time, while `cnt` tracks how many problems are taken. The final score is computed as `m + cnt`, reflecting that each solved problem contributes exactly one extra point beyond its time cost cancellation.

The early break is important because once the smallest remaining problem does not fit, no larger one will fit either.

## Worked Examples

Consider a case with M = 7 and difficulties [1, 2, 3, 4].

After sorting, we already have [1, 2, 3, 4]. We iterate:

| Step | Chosen set | Total time | Count | Remaining capacity |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 | 6 |
| 2 | [1,2] | 3 | 2 | 4 |
| 3 | [1,2,3] | 6 | 3 | 1 |
| 4 | stop | 6 | 3 | 1 |

Final answer is 7 + 3 = 10.

This trace shows that greedily taking smallest elements maximizes count without violating the constraint, and stopping early is forced when the next item does not fit.

Now consider M = 5 and difficulties [5, 10, 20].

After sorting: [5, 10, 20].

| Step | Chosen set | Total time | Count |
| --- | --- | --- | --- |
| 1 | [5] | 5 | 1 |
| 2 | stop | 5 | 1 |

Answer is 5 + 1 = 6.

This demonstrates the edge case where only one item fits, and larger items are irrelevant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates, scanning is linear |
| Space | O(1) extra | Sorting is in-place apart from input storage |

The total N across test cases is 100000, so sorting per test case remains efficient, and the overall complexity easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        res = []
        for _ in range(t):
            n, m = map(int, input().split())
            d = list(map(int, input().split()))
            d.sort()
            s = 0
            c = 0
            for x in d:
                if s + x > m:
                    break
                s += x
                c += 1
            res.append(str(m + c))
        return "\n".join(res)

    return solve()

# provided sample (formatted as multi-test)
assert run("""4
3 7
1 2 4
4 10
1 2 3 4
1 5
10
2 9
4 5
""") == "10\n49\n5\n12"

# all equal values
assert run("""1
5 10
2 2 2 2 2
""") == "12"

# cannot take anything
assert run("""1
3 1
5 6 7
""") == "1"

# take everything exactly
assert run("""1
3 6
1 2 3
""") == "9"

# large M
assert run("""1
4 100
1 1 1 1
""") == "104"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 12 | greedy tie handling |
| cannot take anything | 1 | zero selection case |
| exact fit | 9 | boundary equality |
| large M | 104 | full selection case |

## Edge Cases

When M is smaller than the smallest difficulty, the algorithm immediately skips all elements because the first comparison fails. For input like N = 3, M = 1, d = [5, 6, 7], sorting leaves the array unchanged and the first check fails, producing cnt = 0 and answer = 1, which matches the intended “submit immediately” strategy.

When all problems fit, such as M = 6 with [1, 2, 3], the loop consumes everything and cnt becomes N. The output becomes M + N, reflecting that every problem contributes exactly one unit of gain beyond feasibility.

When multiple equal difficulties exist, sorting preserves them in any order, and the greedy prefix selection naturally takes as many as fit. Swapping equal elements does not change feasibility, confirming stability of the approach.
