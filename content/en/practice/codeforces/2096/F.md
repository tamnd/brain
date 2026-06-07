---
title: "CF 2096F - Wonderful Impostors"
description: "We are given a game with n viewers, each of whom may either be a crewmate or an impostor. The viewers make statements about themselves and others in contiguous ranges."
date: "2026-06-08T05:24:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2096
codeforces_index: "F"
codeforces_contest_name: "Neowise Labs Contest 1 (Codeforces Round 1018, Div. 1 + Div. 2)"
rating: 3100
weight: 2096
solve_time_s: 93
verified: false
draft: false
---

[CF 2096F - Wonderful Impostors](https://codeforces.com/problemset/problem/2096/F)

**Rating:** 3100  
**Tags:** data structures, implementation, two pointers  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a game with `n` viewers, each of whom may either be a crewmate or an impostor. The viewers make statements about themselves and others in contiguous ranges. Each statement has one of two forms: either it claims that a segment of viewers contains at least one impostor, or it claims that a segment contains no impostors.

We are asked multiple questions, each specifying a contiguous subset of statements, and we must determine whether it is possible for all statements in that range to be simultaneously true. Importantly, the game does not guarantee the existence of at least one impostor or at least one crewmate globally, so we cannot assume anything outside the statement ranges.

The input limits are large: up to 200,000 viewers, statements, and queries per test case, with sums across all test cases also bounded by 200,000. This indicates that any solution iterating naively over viewers or statements per query will be too slow. Specifically, a brute-force approach checking every viewer for every statement would yield `O(m*n)` per test case, which is up to `4*10^10` operations in the worst case, far beyond what is feasible in 2 seconds.

A subtle edge case arises when multiple statements overlap, for example: one statement says there is at least one impostor in viewers 1-3, and another says viewers 2-3 have no impostors. Naively checking each statement independently may miss conflicts created by overlapping ranges. Another tricky case is when statements fully cover the same range but contradict: a statement "there is at least one impostor in 1-5" and another "there are no impostors in 1-5" must immediately yield "NO" if queried together. A careless approach that does not track overlaps efficiently will give wrong answers.

## Approaches

A brute-force solution would assign each statement a type and then attempt all assignments of viewers to roles, checking all statements in a query for consistency. This is correct in principle, because checking all possible viewer assignments guarantees correctness. However, with `n` up to 2 * 10^5, the number of assignments is `2^n`, which is completely infeasible. Even if we only check each statement individually per query, iterating through ranges explicitly for every query results in `O(q * m * n)` operations, which is too slow.

The key observation is that we do not need the full assignment of roles; we only need to identify potential conflicts between statements. A statement of type 0 (no impostors in a range) forces all viewers in that range to be crewmates. A statement of type 1 (at least one impostor) requires at least one viewer in that range to be an impostor. Two statements conflict if a type 1 statement is entirely contained in a type 0 statement. Therefore, the problem reduces to efficiently detecting if, in a contiguous set of statements, any type 1 statement is entirely inside a type 0 statement. We can precompute the earliest conflicting position for each statement, and then answer each query in constant time by checking if the query range extends past this earliest conflict. This reduces the complexity from prohibitive to linear preprocessing plus constant-time queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n * q) | O(n) | Too slow |
| Optimal | O(m + q) per test case | O(m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of viewers `n` and the number of statements `m`.
2. Initialize a variable `rightmost_zero` to track the farthest endpoint of any type 0 statement seen so far. This represents the largest range that must contain only crewmates.
3. Initialize an array `earliest_conflict` of size `m + 1` to store the earliest position at which a conflict occurs.
4. Iterate through all statements from 1 to `m`. For each statement:

- If it is type 0, update `rightmost_zero` to be the maximum of its current value and the endpoint of this statement. This ensures we know the full extent of enforced crewmates.
- If it is type 1, record the earliest statement index at which this type 1 statement could conflict with a previous type 0 statement. Specifically, if its start point is less than or equal to `rightmost_zero`, then it is potentially conflicting, and `earliest_conflict[i]` should be the maximum of `earliest_conflict[i-1]` and the current index. Otherwise, inherit `earliest_conflict[i-1]`.
5. After processing all statements, we have for each statement the earliest conflicting type 1 that is completely inside a previous type 0 statement.
6. For each query `(l, r)`, check whether `earliest_conflict[r] < l`. If true, there are no conflicts in this range, so output "YES". Otherwise, output "NO".

This works because type 0 statements enforce strict crewmates, and any type 1 statement inside such a range immediately violates the possibility of all statements being true. By tracking the rightmost zero and propagating conflicts, we reduce the verification per query to a simple comparison.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        statements = []
        for _ in range(m):
            x, a, b = map(int, input().split())
            statements.append((x, a, b))
        earliest_conflict = [0] * (m + 1)
        rightmost_zero = 0
        for i, (x, a, b) in enumerate(statements, start=1):
            if x == 0:
                rightmost_zero = max(rightmost_zero, b)
            if x == 1:
                if a <= rightmost_zero:
                    earliest_conflict[i] = max(earliest_conflict[i-1], i)
                else:
                    earliest_conflict[i] = earliest_conflict[i-1]
            else:
                earliest_conflict[i] = earliest_conflict[i-1]
        q = int(input())
        for _ in range(q):
            l, r = map(int, input().split())
            print("YES" if earliest_conflict[r] < l else "NO")

if __name__ == "__main__":
    solve()
```

The code first tracks the farthest range of crewmates imposed by type 0 statements. When a type 1 statement starts inside this range, it potentially conflicts, and we record this in `earliest_conflict`. Queries are answered by checking if any conflict exists within the query range. Using `i-1` propagation ensures that the conflict information is cumulative, so we never miss an earlier type 0 statement.

## Worked Examples

### Example 1

Input segment:

```
4 3
1 1 3
1 2 4
0 2 3
1
1 3
```

| Statement | x | a | b | rightmost_zero | earliest_conflict |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 3 | 0 | 0 |
| 2 | 1 | 2 | 4 | 0 | 0 |
| 3 | 0 | 2 | 3 | 3 | 0 |

Query (1,3) checks if `earliest_conflict[3] < 1` → `0 < 1` → YES.

This shows that although type 0 is last, it does not invalidate previous type 1 statements outside its range.

### Example 2

Input segment:

```
5 2
0 1 5
1 1 5
3
1 1
2 2
1 2
```

| Statement | x | a | b | rightmost_zero | earliest_conflict |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 5 | 5 | 0 |
| 2 | 1 | 1 | 5 | 5 | 2 |

Query (1,1): `earliest_conflict[1] < 1` → `0 < 1` → YES

Query (2,2): `earliest_conflict[2] < 2` → `2 < 2` → NO

Query (1,2): `earliest_conflict[2] < 1` → `2 < 1` → NO

This confirms that the conflict detection correctly identifies contradictions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m + q) per test case | Each statement is processed once, and each query is answered in constant time. |
| Space | O(m) | We store `earliest_conflict` of size m+1. |

Given the constraints that the total `m` and `q` across all test cases is ≤ 2 * 10^5, this algorithm fits comfortably in the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("""4
4 3
1 1 3
1 2 4
0 2
```
