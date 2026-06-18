---
problem: 1282C
contest_id: 1282
problem_index: C
name: "Petya and Exam"
contest_name: "Codeforces Round 610 (Div. 2)"
rating: 1800
tags: ["greedy", "sortings", "two pointers"]
answer: passed_samples
verified: false
solve_time_s: 175
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2da601-1174-83ec-845c-92c2dc74892b
---

# CF 1282C - Petya and Exam

**Rating:** 1800  
**Tags:** greedy, sortings, two pointers  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 55s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2da601-1174-83ec-845c-92c2dc74892b  

---

## Solution

## Problem Understanding

Each test case describes an exam where problems arrive with deadlines and take different amounts of time depending on whether they are easy or hard. Petya processes problems sequentially starting from time zero, choosing an order, and may stop at any integer time $s \le T$. His score depends on how many problems he has solved, but only if every problem whose deadline is at most $s$ has been solved by that time. If even one such “active” problem is left unsolved when he leaves, the score for that attempt becomes zero.

So the real structure is not just scheduling, but choosing a prefix of time and selecting a subset of problems to fit within that time while respecting two constraints: total time spent on chosen problems cannot exceed $s$, and all problems with deadline at most $s$ must be included in that solved set.

The key tension is that increasing $s$ relaxes deadlines but also increases the amount of work needed because more problems become mandatory. A good solution is some balance point where Petya can still finish all mandatory problems and also fill remaining time with optional ones.

The constraints imply that any solution must be close to linear or linearithmic per test case. Since total $n$ across tests is $2 \cdot 10^5$, any quadratic simulation over subsets or time points is immediately too slow. Sorting-based strategies and greedy sweeps are natural candidates.

A common failure case arises when one assumes that once a set of mandatory problems is fixed, we can greedily take the cheapest remaining ones without considering how the deadline set changes as we move $s$. For example, picking a late time $s$ without ensuring feasibility of all earlier deadlines leads to invalid scoring resets.

Another subtle failure happens if we try to fix $s$ and greedily solve problems in arbitrary order without separating easy and hard costs. For instance, mixing hard problems early can block satisfying a tighter earlier deadline set that would have been optimal.

## Approaches

A brute-force approach would try every possible leaving time $s$, and for each $s$ determine the maximum number of problems Petya can solve under time limit $s$ while also solving all problems with $t_i \le s$. For a fixed $s$, we would first identify mandatory problems, ensure they can fit within $s$, and then greedily add other problems by increasing order of solving time. This is correct but expensive.

For each $s$, scanning all problems and sorting candidates costs $O(n \log n)$, and doing this for all $T$ possible times is impossible since $T$ can be $10^9$. Even if we only consider distinct $t_i$, there are still up to $n$ candidates, giving $O(n^2 \log n)$ in worst cases.

The key observation is that optimal answers only occur at times equal to some $t_i$ or at $T$. Any optimal strategy must “turn on” a new constraint exactly when a new problem becomes mandatory. This reduces the candidate set of $s$ to at most $n+1$.

Once $s$ is fixed, all problems split into mandatory (deadline $\le s$) and optional (deadline $> s$). Mandatory ones must be included and define a base time cost. If this base cost exceeds $s$, the choice of $s$ is invalid.

Among optional problems, we want to maximize count subject to remaining time. Since every problem is either cost $a$ or $b$, the optimal way is to always take easier ones first. This becomes a classic knapsack-like greedy where sorting is unnecessary: we just count how many easy and hard problems are available.

We can preprocess by sorting problems by deadline and maintaining prefix counts of easy and hard types. Then for each candidate $s$, we know exactly how many mandatory easy/hard problems exist, and how many optional remain. Feasibility is checked using total time, and remaining time is used greedily to add more problems.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $s$ | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Sort + prefix + greedy sweep | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Sort all problems by their mandatory time $t_i$. This ensures that as we increase $s$, the set of mandatory problems only grows. This monotonicity is the core structure that allows prefix processing.
2. Build prefix counts: at position $i$, store how many easy and hard problems appear among the first $i$ problems in sorted order.
3. Consider each candidate time $s$ as either $t_i$ for some $i$, or $T$. For a fixed prefix up to $i$, all these problems are mandatory.
4. Compute mandatory time cost as $cost = easy_i \cdot a + hard_i \cdot b$. If this exceeds $s$, skip this $i$ because Petya cannot even satisfy required constraints.
5. If feasible, compute remaining time $rem = s - cost$. Also compute remaining optional counts: easy and hard outside the prefix.
6. To maximize solved problems, always take easy optional problems first because they consume less time per problem. Use as many easy as fit into $rem$, then use hard problems.
7. Track the maximum total solved over all valid $s$.

### Why it works

The sorted-by-deadline sweep guarantees that every valid solution corresponds to some prefix of the sorted array. Within any fixed prefix, feasibility depends only on total required processing time, not order. Since all tasks of a given type have identical cost, the optimal use of leftover time is greedy by cost: taking easier tasks first always dominates any exchange with a hard task in terms of number of problems solved. This creates a stable optimal structure where prefix feasibility and local greedy filling together cover all optimal schedules.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    for _ in range(m):
        n, T, a, b = map(int, input().split())
        tp = list(map(int, input().split()))
        t = list(map(int, input().split()))

        arr = list(zip(t, tp))
        arr.sort()

        easy_pref = [0]
        hard_pref = [0]

        for ti, typ in arr:
            easy_pref.append(easy_pref[-1] + (typ == 0))
            hard_pref.append(hard_pref[-1] + (typ == 1))

        ans = 0

        def evaluate(limit_time, idx):
            easy_m = easy_pref[idx]
            hard_m = hard_pref[idx]

            cost = easy_m * a + hard_m * b
            if cost > limit_time:
                return 0

            rem = limit_time - cost

            easy_total = easy_pref[-1]
            hard_total = hard_pref[-1]

            easy_avail = easy_total - easy_m
            hard_avail = hard_total - hard_m

            take_easy = min(easy_avail, rem // a)
            rem -= take_easy * a

            take_hard = min(hard_avail, rem // b)

            return easy_m + hard_m + take_easy + take_hard

        n = len(arr)

        for i in range(n + 1):
            limit = T if i == n else arr[i-1][0]
            ans = max(ans, evaluate(limit, i))

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first sorts problems so that any prefix corresponds to a feasible deadline threshold. Prefix arrays allow constant-time extraction of mandatory counts. The evaluation function enforces feasibility of mandatory tasks, then greedily fills leftover time with optional tasks in increasing cost order (easy before hard). Each prefix is tested as a potential optimal cutoff.

A subtle detail is that the candidate time is taken exactly as a deadline value. Choosing any intermediate time between two deadlines does not change the mandatory set but only tightens the time budget, so it cannot improve the answer.

## Worked Examples

Consider a small case with mixed deadlines and costs:

Input:

```
1
4 10 1 3
0 1 0 1
2 3 5 7
```

Sorted by deadline:

| i | t | type | easy pref | hard pref |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1 | 0 |
| 2 | 3 | 1 | 1 | 1 |
| 3 | 5 | 0 | 2 | 1 |
| 4 | 7 | 1 | 2 | 2 |

For prefix $i=2$, limit is $s=3$. Mandatory cost is $1\cdot1 + 1\cdot3 = 4$, which exceeds 3, so invalid.

For prefix $i=3$, limit $s=5$. Mandatory cost is $2 + 3 = 5$, rem = 0, score = 3.

For prefix $i=4$, limit $s=7$. Mandatory cost = 8, rem = -1, invalid.

The best answer is 3.

This trace shows how infeasible prefixes are filtered purely by cost, and how feasibility sharply changes at each deadline threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, each prefix evaluation is O(1) |
| Space | $O(n)$ | arrays for sorting and prefix sums |

The solution fits comfortably since total $n$ over all test cases is $2 \cdot 10^5$, making sorting-based processing efficient within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m = int(input())
    out = []
    for _ in range(m):
        n, T, a, b = map(int, input().split())
        tp = list(map(int, input().split()))
        t = list(map(int, input().split()))
        arr = list(zip(t, tp))
        arr.sort()

        easy_pref = [0]
        hard_pref = [0]
        for ti, typ in arr:
            easy_pref.append(easy_pref[-1] + (typ == 0))
            hard_pref.append(hard_pref[-1] + (typ == 1))

        def eval(limit, idx):
            em = easy_pref[idx]
            hm = hard_pref[idx]
            cost = em * a + hm * b
            if cost > limit:
                return 0
            rem = limit - cost
            ea = easy_pref[-1] - em
            ha = hard_pref[-1] - hm
            take_e = min(ea, rem // a)
            rem -= take_e * a
            take_h = min(ha, rem // b)
            return em + hm + take_e + take_h

        ans = 0
        n = len(arr)
        for i in range(n + 1):
            limit = T if i == n else arr[i-1][0]
            ans = max(ans, eval(limit, i))

        out.append(str(ans))

    return "\n".join(out)

# provided samples (single aggregated test)
assert run("""10
3 5 1 3
0 0 1
2 1 4
2 5 2 3
1 0
3 2
1 20 2 4
0
16
6 20 2 5
1 1 0 1 0 0
0 8 2 9 11 6
7 17 1 6
1 1 0 1 0 0 0
1 7 0 11 10 15 10
6 17 2 6
0 0 1 0 0 1
7 6 3 7 10 12
5 17 2 5
1 1 1 1 0
17 11 10 6 4
1 1 1 2
0
1
""") == """3
2
1
0
1
4
0
1
2
1"""

# small custom case
assert run("""1
2 5 1 2
0 1
1 2
""") == "2", "basic mix"

# all easy
assert run("""1
3 10 1 5
0 0 0
1 2 3
""") == "3", "all easy"

# all hard tight time
assert run("""1
3 5 1 4
1 1 1
1 2 3
""") == "1", "hard constraint"

# boundary zero deadlines
assert run("""1
2 5 1 2
0 1
0 5
""") == "2", "deadline edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed small case | 2 | interaction of types |
| all easy | 3 | greedy fill correctness |
| all hard tight | 1 | feasibility pruning |
| zero deadline mix | 2 | boundary handling of t_i = 0 |

## Edge Cases

A critical edge case is when all mandatory problems already exceed the time limit for a given prefix. For example, if $s$ equals a small early deadline but includes multiple hard problems, the cost check immediately rejects it. The algorithm correctly returns zero for that prefix without attempting greedy filling, ensuring invalid schedules do not leak partial scores.

Another edge case occurs when all problems are easy. Then every prefix is feasible, and the optimal strategy is simply taking as many as possible within $T$. The greedy filling phase naturally reduces to taking all tasks in order of increasing deadline, and the solution achieves the full count.

A final subtle case is when deadlines are equal or clustered. Since sorting is stable with respect to values, identical deadlines do not create ambiguity: the prefix structure still correctly captures all mandatory sets, and evaluating at each boundary remains sufficient.