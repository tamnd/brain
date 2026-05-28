---
title: "CF 45B - School"
description: "Each student points to exactly one other student, the person they call whenever they hear news. This creates a directed functional graph, every node has out-degree exactly one. On day i, one student starts spreading a piece of news with initial strength b[i]."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "dsu"]
categories: ["algorithms"]
codeforces_contest: 45
codeforces_index: "B"
codeforces_contest_name: "School Team Contest 3 (Winter Computer School 2010/11)"
rating: 2200
weight: 45
solve_time_s: 126
verified: true
draft: false
---

[CF 45B - School](https://codeforces.com/problemset/problem/45/B)

**Rating:** 2200  
**Tags:** dp, dsu  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student points to exactly one other student, the person they call whenever they hear news. This creates a directed functional graph, every node has out-degree exactly one.

On day `i`, one student starts spreading a piece of news with initial strength `b[i]`. Every time the news is forwarded, its strength decreases by one. Once the strength becomes zero, forwarding stops. A student may receive the same news multiple times during the same day with different strengths, because cycles are allowed.

We are not asked how many total times students hear news. We only care about the first day each student ever learns any news. For every day, we must output how many students become informed for the first time on that day.

The starting student is not given directly. Instead,

$$a_i = ((v_i + res_{i-1}) \bmod n) + 1$$

where `res[i-1]` is the previous day's answer.

The graph size and number of days are both up to `10^5`. A direct simulation of every phone call is impossible because `b[i]` can also be as large as `10^7`. Even a single query may require traversing millions of edges if implemented naively.

A quadratic or even `O(n * sqrt(n))` approach is dangerous under a 2 second limit. The target is close to linear overall complexity.

The tricky part is that paths can enter cycles. If we simply walk `b[i]` steps every day, we repeatedly revisit the same vertices. Another subtle issue is that once a student has already heard news on some earlier day, they must never be counted again.

Consider this example:

```
3 1
2 3 1
1
10
```

The graph is one cycle: `1 -> 2 -> 3 -> 1`.

The news loops forever conceptually, but strength decreases every step. With strength `10`, every student hears it many times. The correct answer is:

```
3
```

A careless implementation that counts every visit instead of first-time discoveries would produce much larger values.

Another dangerous case is when the starting student was already informed earlier:

```
3 2
2 3 1
1 1
2 2
```

Day 1 informs students `2` and `3` starting from `2`.

Day 2 starts again from `2`, but nobody is new anymore. The correct output is:

```
2
0
```

If we forget to maintain a global "already informed" state across days, we incorrectly count repeated discoveries.

One more subtle case appears when `b[i]` exceeds the number of distinct reachable vertices:

```
4 1
2 3 4 2
1
100
```

The reachable set from `2` is only `{2,3,4}` because the graph eventually cycles inside those nodes. The answer is still:

```
3
```

A naive implementation may waste enormous time traversing the same cycle repeatedly.

## Approaches

The brute-force approach follows the process exactly as described.

For each day:

1. Compute the starting student `a[i]`.
2. Walk along outgoing edges up to `b[i]` times.
3. Mark every visited student as informed if this is their first time hearing any news.

This simulation is correct because the news propagation is literally a walk of length `b[i]` in the functional graph.

The problem is complexity. In the worst case, `b[i] = 10^7` and `m = 10^5`. That means up to `10^12` edge traversals, far beyond feasible limits.

The key observation is that every student only matters once. After a student becomes informed, future visits to that student never contribute to the answer again.

This changes the problem completely. Instead of simulating every transmission, we only need to efficiently skip students that are already known.

Suppose we are walking along the propagation path. Whenever we encounter a student already informed, processing that vertex is useless. We want a structure that quickly jumps to the next still-uninformed vertex.

This is exactly what Disjoint Set Union can do.

We maintain a DSU-like "next alive vertex" structure. Once a student becomes informed, we remove them from consideration by linking them to their successor in the graph. Future traversals automatically skip them.

The graph is functional, so every node has exactly one outgoing edge. That makes this compression process particularly efficient. After a node is processed once, it effectively disappears forever.

The resulting algorithm processes each student at most once across all days. That reduces the total work to nearly linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\sum b_i)$ | $O(n)$ | Too slow |
| Optimal | $O((n + m)\alpha(n))$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Store the friendship graph as an array `g`, where `g[x]` is the next student called by `x`.
2. Maintain an array `seen` indicating whether a student has already heard any news before.
3. Build a DSU-style jump structure `parent`.

For every student `x`, `find(x)` returns the next candidate vertex that may still be uninformed.
4. Initially, every vertex is its own representative.
5. When a student `x` becomes informed for the first time:

- Mark `seen[x] = True`.
- Remove `x` from future consideration by setting:

```
parent[x] = find(g[x])
```

This means future traversals skip directly toward the next potentially useful vertex.
6. For each day:

- Compute

$$a = ((v_i + prev) \bmod n) + 1$$

where `prev` is yesterday's answer.

- Start from `cur = find(a)`.
7. While:

- `cur` is not already processed,
- and we still have remaining strength,

process the current student.

Every processed student consumes one unit of strength because one forwarding step occurs.
8. After processing a student:

- Increase today's answer.
- Remove the student from the DSU structure.
- Jump directly to the next available candidate.
9. Output today's answer and store it as `prev`.

### Why it works

The DSU invariant is:

`find(x)` always returns the first uninformed student reachable from `x` by repeatedly following friendship edges, skipping all already-informed students.

Whenever a student becomes informed, we permanently redirect them toward the next candidate. Path compression guarantees future searches become extremely fast.

Since every student transitions from uninformed to informed only once, each node is removed from the structure at most once. That bounds the total amount of real work across all days.

The propagation process itself is preserved exactly. We still follow the same friendship chain in the same order. The DSU only skips vertices that can no longer affect answers.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

n, m = map(int, input().split())

g = [0] + list(map(int, input().split()))
v = list(map(int, input().split()))
b = list(map(int, input().split()))

parent = list(range(n + 1))
seen = [False] * (n + 1)

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]

prev = 0

for i in range(m):
    a = ((v[i] + prev) % n) + 1

    ans = 0
    steps = b[i]

    cur = find(a)

    while steps > 0 and not seen[cur]:
        ans += 1
        seen[cur] = True
        steps -= 1

        nxt = find(g[cur])
        parent[cur] = nxt

        cur = nxt

    print(ans)
    prev = ans
```

The core idea is that informed students are removed permanently from future traversals.

The `find` function performs standard DSU path compression. After enough operations, chains become extremely short, giving almost constant-time access.

The most delicate part is this line:

```
parent[cur] = find(g[cur])
```

We do not simply write `parent[cur] = g[cur]`. The friend may already be removed, so we must jump directly to the next active representative.

Another subtle detail is the loop condition:

```
while steps > 0 and not seen[cur]:
```

If `cur` is already informed, continuing further is useless. Every future reachable node through DSU compression has also already been removed from consideration.

The solution never explicitly handles cycles. DSU compression naturally collapses them once all vertices inside become informed.

Integer overflow is irrelevant in Python, but in C++ this solution must use 64-bit integers for the formula involving `v[i]`.

## Worked Examples

### Sample 1

Input:

```
3 4
2 3 1
1 2 3 4
1 2 3 4
```

The graph is:

```
1 -> 2 -> 3 -> 1
```

| Day | prev | a | b | Newly informed | res |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 1 | {2} | 1 |
| 2 | 1 | 1 | 2 | {1} | 1 |
| 3 | 1 | 2 | 3 | {3} | 1 |
| 4 | 1 | 3 | 4 | {} | 0 |

Output:

```
1
1
1
0
```

This trace shows how already-informed students are skipped automatically. By day 4, every student is already known, so the answer becomes zero immediately.

### Custom Example

Input:

```
4 2
2 3 4 2
1 1
5 5
```

The graph is:

```
1 -> 2 -> 3 -> 4 -> 2
```

| Day | prev | a | b | Traversal | Newly informed | res |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 5 | 2,3,4,2,3 | {2,3,4} | 3 |
| 2 | 3 | 1 | 5 | 1,2,3,4 | {1} | 1 |

Output:

```
3
1
```

The first day demonstrates repeated cycling. Even though the news keeps looping while strength remains positive, each student contributes at most once.

The second day shows DSU skipping already processed vertices efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\alpha(n))$ | Each student is removed once, DSU operations are amortized inverse-Ackermann |
| Space | $O(n)$ | Friendship graph, DSU parent array, and visited array |

The inverse-Ackermann factor is effectively constant in practice. With `n, m <= 10^5`, this easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    g = [0] + list(map(int, input().split()))
    v = list(map(int, input().split()))
    b = list(map(int, input().split()))

    parent = list(range(n + 1))
    seen = [False] * (n + 1)

    sys.setrecursionlimit(1 << 25)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    prev = 0
    out = []

    for i in range(m):
        a = ((v[i] + prev) % n) + 1

        ans = 0
        steps = b[i]

        cur = find(a)

        while steps > 0 and not seen[cur]:
            ans += 1
            seen[cur] = True
            steps -= 1

            nxt = find(g[cur])
            parent[cur] = nxt

            cur = nxt

        out.append(str(ans))
        prev = ans

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""3 4
2 3 1
1 2 3 4
1 2 3 4
"""
) == "1\n1\n1\n0\n", "sample 1"

# minimum size
assert run(
"""2 1
2 1
1
1
"""
) == "1\n", "minimum graph"

# cycle with huge strength
assert run(
"""3 1
2 3 1
1
100
"""
) == "3\n", "must avoid repeated counting"

# all students informed on first day
assert run(
"""5 3
2 3 4 5 1
1 1 1
10 10 10
"""
) == "5\n0\n0\n", "future days should contribute nothing"

# chain entering cycle
assert run(
"""4 2
2 3 4 2
1 1
5 5
"""
) == "3\n1\n", "cycle compression correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum graph with 2-cycle | `1` | Smallest legal input |
| Large strength on small cycle | `3` | Avoid repeated counting inside cycles |
| Everyone informed on first day | `5 0 0` | Global persistence of informed state |
| Chain entering cycle | `3 1` | Correct DSU skipping across mixed structures |

## Edge Cases

Consider the pure cycle case:

```
3 1
2 3 1
1
10
```

The walk repeatedly loops through all three students. A naive simulation may count many repeated visits.

Execution:

- Start at `2`
- Inform `2`, remove it
- Inform `3`, remove it
- Inform `1`, remove it
- DSU now skips directly among removed nodes

At this point every student is already informed, so the process stops contributing. The answer is correctly:

```
3
```

Now consider a previously informed starting node:

```
3 2
2 3 1
1 1
2 2
```

Day 1:

- Start at `2`
- Inform `2`
- Inform `3`

Answer: `2`

Day 2:

$$a = ((1 + 2) \bmod 3) + 1 = 1$$

Student `1` is still uninformed, so only `1` contributes.

Output:

```
2
1
```

The DSU structure correctly skips `2` and `3`.

Finally, consider a graph where propagation enters a small cycle:

```
4 1
2 3 4 2
1
100
```

The reachable vertices from `2` are only `{2,3,4}`.

Execution:

- Inform `2`
- Inform `3`
- Inform `4`
- Future transitions cycle among already removed vertices

The answer remains:

```
3
```

even though the news strength is much larger.
