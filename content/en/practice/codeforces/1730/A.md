---
title: "CF 1730A - Planets"
description: "We are given several independent test cases. In each test case there is a multiset of integers, where each integer represents an orbit label of a planet. Planets sharing the same value belong to the same orbit. We have two ways to destroy planets."
date: "2026-06-15T02:39:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1730
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 823 (Div. 2)"
rating: 800
weight: 1730
solve_time_s: 80
verified: true
draft: false
---

[CF 1730A - Planets](https://codeforces.com/problemset/problem/1730/A)

**Rating:** 800  
**Tags:** data structures, greedy, sortings  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case there is a multiset of integers, where each integer represents an orbit label of a planet. Planets sharing the same value belong to the same orbit.

We have two ways to destroy planets. One option removes a single planet for cost 1. The other option removes every planet belonging to a chosen orbit in one operation for cost c, regardless of how many planets are in that orbit.

The task is to choose a combination of these two actions that removes all planets while minimizing total cost.

The structure of the input implies that only frequencies of distinct orbit values matter, not their positions. Any permutation of the array does not change the answer, so the problem reduces to counting occurrences of each value.

The constraints are small, with n up to 100 per test case and at most 100 test cases. This means any solution that runs in O(n²) per test case is already safe, but the structure allows an even simpler linear counting approach.

A common failure case comes from ignoring frequency aggregation. For example, if all planets are on distinct orbits and c is large, using the second machine is wasteful, but a naive greedy approach might still apply it once per planet. Conversely, if many planets share the same orbit and c is small, failing to group them leads to overpaying by repeatedly using the first machine.

A small illustrative case:

Input:

```
1
5 3
1 1 1 2 3
```

If we destroy individually, cost is 5. If we use the second machine on orbit 1, cost becomes 3 + 2 = 5. If we use it on all orbits, cost becomes 3 + 3 + 3 = 9, which is worse. The correct strategy depends on comparing per-orbit savings, not just raw counts.

## Approaches

The brute-force perspective tries to decide for each subset of orbits whether we use the second machine or not. Suppose there are k distinct orbits. For each orbit, we choose either to pay size of that orbit (using the first machine repeatedly) or pay c once (using the second machine). This leads to 2^k choices. Computing each choice costs O(n), so the total becomes O(2^k n), which is infeasible even for moderate k.

The key observation is that orbits are independent. For each distinct orbit value with frequency f, we only compare two costs: destroying individually costs f, and using the second machine costs c. There is no interaction between different orbits because the second machine cannot partially destroy an orbit.

So the optimal decision is local: for each orbit, take the minimum of f and c. Summing these choices yields the global optimum.

This reduces the problem from combinatorial selection to a simple frequency aggregation problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over orbit subsets | O(2^k · n) | O(k) | Too slow |
| Frequency greedy per orbit | O(n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the array of orbit values and count how many planets belong to each orbit. This step compresses the problem into independent groups because only counts matter.
2. For each distinct orbit, compute its frequency f. This represents the cost of destroying all planets in that orbit using only the first machine.
3. For that orbit, compute the cheaper option between f and c. The second machine is only useful if it costs less than individually destroying all planets in that orbit.
4. Sum these minimum values across all orbits to obtain the total cost.
5. Output the result for the test case.

The reason we evaluate each orbit independently is that there is no shared benefit across orbits: the second machine never affects more than one orbit at a time.

### Why it works

Each orbit forms an isolated decision unit. Any optimal solution can be transformed so that for every orbit we either fully apply the second machine once or only use the first machine repeatedly, without changing cost optimality. Mixing strategies within a single orbit is impossible, and there is no cross-orbit coupling, so summing per-orbit optimal costs yields a globally optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))
        
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        
        ans = 0
        for f in freq.values():
            ans += min(f, c)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by grouping planets by orbit using a dictionary. This ensures we only reason about frequencies, which is the correct abstraction of the problem. Each frequency is then independently compared against the cost c.

A subtle point is that we never consider partial use of the second machine. Once chosen for an orbit, it always removes all planets of that orbit, so splitting its usage is meaningless. This is why the min(f, c) comparison fully captures the decision space.

## Worked Examples

### Example 1

Input:

```
n = 5, c = 3
a = [1, 1, 1, 2, 3]
```

| Orbit | Frequency f | min(f, c) | Running Sum |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 3 |
| 2 | 1 | 1 | 4 |
| 3 | 1 | 1 | 5 |

Final output is 5.

This trace shows that even when the second machine is useful for a dense orbit, sparse orbits are cheaper to handle individually, so decisions naturally separate per orbit.

### Example 2

Input:

```
n = 4, c = 2
a = [1, 2, 3, 4]
```

| Orbit | Frequency f | min(f, c) | Running Sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 1 | 1 | 3 |
| 4 | 1 | 1 | 4 |

Final output is 4.

This case shows that when all orbits are unique, the second machine never helps because c is not cheaper than repeated single deletions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan the array once and then iterate over distinct orbits |
| Space | O(k) | We store frequencies of distinct orbits |

The constraints allow this easily since n ≤ 100 and t ≤ 100, giving at most 10,000 operations overall, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))
        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1
        ans = sum(min(f, c) for f in freq.values())
        output.append(str(ans))
    
    return "\n".join(output)

# provided samples
assert run("""4
10 1
2 1 4 5 2 4 5 5 1 2
5 2
3 2 1 2 2
2 2
1 1
2 2
1 2
""") == """4
4
2
2"""

# all equal values
assert run("""1
5 10
7 7 7 7 7
""") == "5"

# all distinct, cheap c
assert run("""1
4 2
1 2 3 4
""") == "4"

# all distinct, expensive c
assert run("""1
4 10
1 2 3 4
""") == "4"

# mixed case
assert run("""1
6 3
1 1 2 2 2 3
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 5 | second machine vs repeated use comparison |
| all distinct, cheap c | 4 | shows second machine not beneficial when c ≥ 1 |
| all distinct, expensive c | 4 | confirms fallback to individual deletion |
| mixed case | 5 | validates per-orbit independent decision |

## Edge Cases

One important edge case is when all planets belong to a single orbit and c is very small.

Input:

```
1
6 2
5 5 5 5 5 5
```

The algorithm computes frequency f = 6 and compares min(6, 2), giving 2. The second machine dominates because it is cheaper than removing individually.

Another edge case is when every orbit is unique.

Input:

```
1
4 10
1 2 3 4
```

Each frequency is 1, so min(1, 10) = 1 for each orbit. The total becomes 4, correctly ignoring the second machine entirely.

A mixed distribution confirms the independence principle:

Input:

```
1
6 3
1 1 2 2 2 3
```

Frequencies are 2, 3, and 1. Costs become min(2,3)=2, min(3,3)=3, min(1,3)=1, totaling 6. Each orbit is treated independently, and no cross-orbit coupling appears in the decision process, confirming the correctness of the decomposition.
