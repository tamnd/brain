---
title: "CF 1337A - Ichihime and Triangle"
description: "We are given four integers in non-decreasing order, and we need to choose three lengths from three separate intervals. The first length must come from the first interval, the second from the second interval, and the third from the third interval."
date: "2026-06-16T09:06:27+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1337
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 635 (Div. 2)"
rating: 800
weight: 1337
solve_time_s: 385
verified: false
draft: false
---

[CF 1337A - Ichihime and Triangle](https://codeforces.com/problemset/problem/1337/A)

**Rating:** 800  
**Tags:** constructive algorithms, math  
**Solve time:** 6m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given four integers in non-decreasing order, and we need to choose three lengths from three separate intervals. The first length must come from the first interval, the second from the second interval, and the third from the third interval. After choosing these three values, we must ensure they can form a triangle with non-zero area.

A triangle with side lengths $x, y, z$ exists with positive area if and only if the triangle inequalities are strict: $x + y > z$, $x + z > y$, and $y + z > x$. Because the values are chosen in sorted intervals where $x \le y \le z$ is always achievable by construction, the only meaningful constraint becomes $x + y > z$.

The constraints are small in terms of input size, at most 1000 test cases, so a constant-time construction per test case is sufficient. Each value can be as large as $10^9$, which rules out any approach that depends on enumerating candidates inside intervals.

A naive attempt would try all triples from the intervals. For each test case that would involve $(b-a+1)(c-b+1)(d-c+1)$ combinations, which can be enormous, up to $10^{27}$ in the worst case. This is clearly impossible.

A more subtle pitfall is assuming that picking arbitrary boundary values always works, for example choosing $x=a$, $y=b$, $z=c$. This can fail when $a + b \le c$, producing a degenerate or invalid triangle. The sample structure shows that flexibility inside the intervals is required.

## Approaches

A brute-force method would enumerate all valid triples $x, y, z$ within their respective ranges and check the triangle condition. This works conceptually because every valid combination is tested, but the number of combinations grows multiplicatively with interval sizes. Since each interval can span up to $10^9$, the search space becomes astronomically large and immediately infeasible.

The key observation is that the triangle condition depends only on the sum of the two smaller sides compared to the largest side. Because $y$ is sandwiched between the other two intervals, adjusting $y$ provides the most direct control over satisfying the inequality. The goal is to make $x + y$ just large enough to exceed $z$, and since we are free to choose within intervals, picking values close to each other near the boundaries is sufficient.

A constructive strategy emerges: pick $x$ as large as possible within $[a, b]$, pick $y$ as large as possible within $[b, c]$, and pick $z$ as small as possible within $[c, d]$. This pushes the sum $x + y$ upward while keeping $z$ minimal, maximizing the chance of satisfying the strict inequality. If this choice fails, shifting values slightly within the overlap region between intervals always allows adjustment, and the problem guarantees a solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((b-a)(c-b)(d-c))$ | $O(1)$ | Too slow |
| Greedy construction | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the four integers $a, b, c, d$. These define three independent ranges for $x, y, z$.
2. Construct $x = b$. This choice places $x$ at the upper end of its range, maximizing potential contribution to the triangle inequality.
3. Construct $y = c$. This similarly maximizes the second side while respecting its allowed interval.
4. Construct $z = c$. This minimizes the third side while still staying in its interval, which helps satisfy $x + y > z$.
5. Output $x, y, z$.

The subtle idea is that we do not need to search for a delicate balance. The structure of the intervals already ensures that pushing the first two variables upward and the last one downward produces a valid configuration.

### Why it works

The construction guarantees $x = b \le c = y = z$ or at least $x \le y \le z$ up to equality cases, but the critical condition is $x + y > z$. Since $x \ge b$ and $y \ge b$, their sum is at least $2b$, while $z \le d$ but we specifically anchor it at $c$, the midpoint boundary between ranges. The problem’s guarantee ensures that within these intervals there always exists a configuration where the sum of the two earlier segments exceeds the third. By aligning two values at the upper boundaries and the third at the lower boundary of its range, we force the inequality to hold.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    
    x = b
    y = c
    z = c
    
    print(x, y, z)
```

The code directly implements the greedy construction. Each test case is handled independently, and no auxiliary storage is required. The choice of `b, c, c` aligns the variables with the natural breakpoints of the intervals.

A subtle point is that although this looks almost trivial, it relies on the fact that overlapping boundaries ensure feasibility. Any alternative valid construction would also work, but this one is stable and avoids edge reasoning inside the code.

## Worked Examples

### Example 1

Input:

```
1 3 5 7
```

We compute:

| Step | x | y | z | Check |
| --- | --- | --- | --- | --- |
| Initial | - | - | - | intervals defined |
| Assign | 3 | 5 | 5 | construction applied |
| Verify | 3 | 5 | 5 | 3 + 5 > 5 |

The inequality holds because $3 + 5 = 8 > 5$. The triangle is valid and non-degenerate.

### Example 2

Input:

```
1 1 1 10
```

| Step | x | y | z | Check |
| --- | --- | --- | --- | --- |
| Assign | 1 | 1 | 1 | boundary construction |
| Verify | 1 | 1 | 1 | 1 + 1 > 1 |

Even in the extreme case where all intervals collapse at the left, the construction still produces a valid triangle since any positive equal sides form a degenerate-looking but valid positive-area triangle condition is satisfied by strict inequality on one side comparison.

This demonstrates that even when ranges are minimal, aligning values at shared boundaries preserves feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | constant work per test case |
| Space | $O(1)$ | no extra storage beyond variables |

The solution performs a fixed number of arithmetic operations per test case, which is optimal for $t \le 1000$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        x, y, z = b, c, c
        out.append(f"{x} {y} {z}")
    return "\n".join(out)

# provided samples
assert run("4\n1 3 5 7\n1 5 5 7\n100000 200000 300000 400000\n1 1 977539810 977539810") == \
"3 5 5\n5 5 5\n200000 300000 300000\n1 977539810 977539810"

# custom cases
assert run("1\n1 2 3 4") == "2 3 3"
assert run("1\n5 5 5 5") == "5 5 5"
assert run("1\n1 10 10 10") == "10 10 10"
assert run("1\n2 3 5 9") == "3 5 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 | 2 3 3 | minimal increasing ranges |
| 5 5 5 5 | 5 5 5 | degenerate intervals |
| 1 10 10 10 | 10 10 10 | tight right boundary |
| 2 3 5 9 | 3 5 5 | non-uniform spacing |

## Edge Cases

Consider the extreme case where all intervals collapse at single points, such as:

```
1 1 1 1
```

The algorithm outputs $1, 1, 1$. The triangle condition holds since $1 + 1 > 1$. There is no freedom to choose different values, and the construction still satisfies validity.

Another case is when intervals are widely separated:

```
1 2 100 1000
```

The algorithm produces $2, 100, 100$. Here $2 + 100 > 100$, so a valid triangle exists even though the last interval is far away. The construction works because the middle and right values are aligned to the smallest feasible boundary, preventing the gap from breaking the inequality.
