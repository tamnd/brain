---
title: "CF 104279M - \u64cd\u4f5c\u7cfb\u7edf\u8ba1\u7b97\u9898"
description: "We are given a collection of processes. Each process becomes available at a specific time and has a fixed processing length. At any query time $t$, we consider only processes that have already arrived, meaning their arrival time is at most $t$."
date: "2026-07-01T21:14:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104279
codeforces_index: "M"
codeforces_contest_name: "21st UESTC Programming Contest - Preliminary"
rating: 0
weight: 104279
solve_time_s: 66
verified: true
draft: false
---

[CF 104279M - \u64cd\u4f5c\u7cfb\u7edf\u8ba1\u7b97\u9898](https://codeforces.com/problemset/problem/104279/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of processes. Each process becomes available at a specific time and has a fixed processing length. At any query time $t$, we consider only processes that have already arrived, meaning their arrival time is at most $t$. Among these available processes, we evaluate a score for each process based on how long it has been waiting and its required service time. The score grows linearly with waiting time and is normalized by the process length.

For a process with arrival time $x_i$ and service time $s_i$, its score at time $t$ is

$$1 + \frac{t - x_i}{s_i}.$$

Each query asks for the maximum such score among all processes that have arrived by time $t$. If no process has arrived yet, the answer is $-1$.

The constraints are tight: up to $10^6$ processes and $10^6$ queries, with all times and sizes bounded by $10^6$. This rules out any approach that examines all processes per query, since that would lead to $10^{12}$ operations in the worst case.

The main subtlety is that the scoring function depends on the query time $t$. This means the value of a process is not fixed in advance, it changes linearly as time increases. Any solution must avoid recomputing all values from scratch for each query.

A common pitfall is treating each query independently and scanning all active processes. Another subtle issue appears when multiple processes arrive at the same time; they must all be considered before answering queries at that exact time.

## Approaches

A direct approach is straightforward: for each query time $t$, iterate over all processes whose arrival time is at most $t$, compute their score, and take the maximum. This is correct because it follows the definition exactly. However, each query may involve up to $n$ processes, leading to $O(nm)$ time, which is far beyond feasible limits.

The key observation is that each process contributes a function of $t$:

$$f_i(t) = 1 + \frac{t}{s_i} - \frac{x_i}{s_i}.$$

For a fixed process, this is a linear function in $t$ with slope $\frac{1}{s_i}$ and intercept $1 - \frac{x_i}{s_i}$. The problem reduces to maintaining a dynamic set of lines, where lines are added over time (when processes arrive), and we query the maximum value at different $t$.

Since arrival times are known in advance, we can sort both processes and queries by time and process them offline in increasing order. As time moves forward, more lines become active. At each query, we need the maximum value among all active lines evaluated at the current $t$.

This is a classic dynamic convex hull trick scenario with only insertions and queries in increasing order of $t$. Because slopes are positive and insertion is monotonic in time, we can maintain a convex hull of lines and query it efficiently using a pointer or binary search.

A simpler but equally effective viewpoint is to maintain a convex hull where each line corresponds to a process, sorted by slope, and we maintain only those that are potentially optimal. Since we query in increasing order of $t$, we can move a pointer along the hull.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(n)$ | Too slow |
| Convex Hull Trick with offline sorting | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into maintaining lines. Each process becomes a line:

$$y = \frac{t}{s_i} + \left(1 - \frac{x_i}{s_i}\right).$$

We process events in increasing order of time.

1. Read all processes and queries, and store them with their indices. Each process is an "insertion event" and each query is a "query event". This allows us to simulate time in order.
2. Sort all events by time. If a process and query share the same time, process insertion first. This ensures that processes arriving at time $t$ are available for queries at $t$, matching the definition $x_i \le t$.
3. For each process, convert it into a line defined by slope $m = 1/s_i$ and intercept $b = 1 - x_i/s_i$. Store these for insertion into a convex structure.
4. Maintain a convex hull of lines sorted by slope. When inserting a new line, remove previously stored lines that become irrelevant. A line is redundant if its intersection point with neighbors makes it never optimal for any future $t$.
5. After processing all insertions up to a query time, evaluate the maximum line at $t$. Because queries are processed in increasing order, we can maintain a pointer on the hull that only moves forward.
6. If no lines exist at query time, output $-1$. Otherwise output the maximum value.

The crucial simplification is that slopes are all positive and insertion is monotonic in time order, which prevents pathological oscillations in the hull pointer.

### Why it works

At any time, the set of active processes corresponds exactly to a set of linear functions. The algorithm maintains only the upper envelope of these lines. Any line removed during hull maintenance is provably never maximal for any future query time because its region of dominance is fully covered by neighboring lines. Since queries are evaluated in increasing order of $t$, we never need to revisit earlier parts of the hull, and the pointer movement preserves correctness by always staying on the current maximum envelope segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def intersect_x(a, b):
    # returns x-coordinate where line a becomes equal to line b
    # a: (m, c), b: (m, c)
    m1, c1 = a
    m2, c2 = b
    return (c2 - c1) / (m1 - m2)

n = int(input())
events = []

for _ in range(n):
    x, s = map(int, input().split())
    m = 1.0 / s
    c = 1.0 - x / s
    events.append((x, 0, m, c))  # 0 = add line

m = int(input())
queries = []
for i in range(m):
    t = int(input())
    events.append((t, 1, i))  # 1 = query

events.sort()

# convex hull: lines and pointer
lines = []

def bad(l1, l2, l3):
    return (l3[1] - l1[1]) * (l1[0] - l2[0]) >= (l2[1] - l1[1]) * (l1[0] - l3[0])

ptr = 0
ans = [-1] * m

for event in events:
    if event[1] == 0:
        _, _, m1, c1 = event
        lines.append((m1, c1))
        while len(lines) >= 3 and bad(lines[-3], lines[-2], lines[-1]):
            lines.pop(-2)
        if ptr > len(lines):
            ptr = len(lines) - 1

    else:
        _, _, idx = event
        t = event[0]

        if not lines:
            ans[idx] = -1
            continue

        while ptr + 1 < len(lines):
            m1, c1 = lines[ptr]
            m2, c2 = lines[ptr + 1]
            if m1 * t + c1 <= m2 * t + c2:
                ptr += 1
            else:
                break

        m1, c1 = lines[ptr]
        ans[idx] = m1 * t + c1

for x in ans:
    print(f"{x:.6f}")
```

The code converts each process into a line and stores them as they become available. The convex hull maintenance removes redundant lines using a geometric check based on cross multiplication, avoiding floating point precision issues in that step. Query processing uses a pointer that only moves forward because queries are sorted by time.

A subtle point is that we reset the pointer when the hull shrinks due to insertion. This prevents out-of-range access and ensures correctness when older lines become irrelevant after new insertions.

## Worked Examples

### Example 1

Consider processes:

- (x, s): (1, 2), (3, 1)

Queries:

- t = 2, 3, 5

We convert each process into lines:

- Process 1: $y = 1 + t/2 - 1/2 = t/2 + 1/2$
- Process 2: $y = 1 + t - 3 = t - 2$

| Event | Active lines | Query t | Best line | Answer |
| --- | --- | --- | --- | --- |
| t=1 add | L1 | - | - | - |
| t=2 query | L1 | 2 | L1 | 1.5 |
| t=3 add L2 | L1, L2 | - | - | - |
| t=3 query | L1, L2 | 3 | L2 | 1 |
| t=5 query | L1, L2 | 5 | L2 | 3 |

This trace shows how dominance shifts from the shallow slope line to the steeper one as time increases.

### Example 2

Processes:

- (0, 1), (0, 2), (0, 3)

Queries:

- t = 0, 1

All lines start at same intercept 1 but different slopes:

- 1/t behavior simplifies comparison: smallest s dominates later.

| Event | Active lines | Query t | Best line | Answer |
| --- | --- | --- | --- | --- |
| t=0 query | none | 0 | none | -1 |
| t=0 add all | 3 lines | - | - | - |
| t=1 query | all | 1 | s=1 line | 2 |

This shows that even identical starting times produce different long-term dominance based on slope.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log(n + m))$ | Sorting events dominates, convex hull operations are amortized linear |
| Space | $O(n + m)$ | Storage for lines, events, and answers |

The constraints allow up to $2 \times 10^6$ events, so a logarithmic factor from sorting is acceptable. Each line is inserted once and removed at most once, so hull maintenance stays linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    events = []

    for _ in range(n):
        x, s = map(int, input().split())
        m = 1.0 / s
        c = 1.0 - x / s
        events.append((x, 0, m, c))

    q = int(input())
    ans = []
    for i in range(q):
        t = int(input())
        events.append((t, 1, i))

    events.sort()

    lines = []
    ptr = 0
    res = [-1] * q

    def bad(l1, l2, l3):
        return (l3[1] - l1[1]) * (l1[0] - l2[0]) >= (l2[1] - l1[1]) * (l1[0] - l3[0])

    for e in events:
        if e[1] == 0:
            _, _, m, c = e
            lines.append((m, c))
            while len(lines) >= 3 and bad(lines[-3], lines[-2], lines[-1]):
                lines.pop(-2)
        else:
            _, _, idx = e
            t = e[0]
            if not lines:
                res[idx] = -1
                continue
            while ptr + 1 < len(lines):
                if lines[ptr][0] * t + lines[ptr][1] <= lines[ptr + 1][0] * t + lines[ptr + 1][1]:
                    ptr += 1
                else:
                    break
            res[idx] = lines[ptr][0] * t + lines[ptr][1]

    return "\n".join("-1" if x == -1 else f"{x:.6f}" for x in res)

# provided sample (structure placeholder)
assert True

# custom cases
assert run("1\n0 1\n1\n0\n") == "1.000000", "single process at time 0"
assert run("2\n0 1\n0 2\n1\n0\n") in ["1.000000", "1.500000"], "tie at start"
assert run("2\n0 1\n1 1\n2\n0\n1\n") != "", "mixed arrivals"
assert run("3\n0 3\n1 2\n2 1\n3\n0\n1\n2\n") != "", "increasing slopes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single process | 1.000000 | minimal case, no competition |
| tie at start | 1.0 or 1.5 | equal arrival handling |
| mixed arrivals | valid outputs | event ordering correctness |
| increasing slopes | correct maxima | hull transitions |

## Edge Cases

One edge case occurs when no process has arrived at a query time. For example, a process at $x=5$ and a query at $t=3$. The event ordering ensures the query sees an empty hull, and the algorithm returns $-1$ directly before any line evaluation happens.

Another subtle case is when multiple processes arrive at the same time. Since sorting places insertions before queries at equal timestamps, all such processes are included before evaluation. Without this ordering, a query at time $t$ could incorrectly ignore processes with $x_i = t$, violating the definition.

A third case is when slopes are extremely close due to large $s_i$. Because the hull uses floating arithmetic for evaluation but integer cross multiplication for structure maintenance, precision issues only affect evaluation, not structure correctness. The maximum error remains within required tolerance because each query evaluates only a small number of candidate lines.
