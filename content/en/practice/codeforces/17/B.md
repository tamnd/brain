---
title: "CF 17B - Hierarchy"
description: "We have employees and directed supervisor offers between them. An offer (a, b, c) means employee a is willing to supervi"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "greedy", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 17
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 17"
rating: 1500
weight: 17
solve_time_s: 94
verified: true
draft: false
---

[CF 17B - Hierarchy](https://codeforces.com/problemset/problem/17/B)

**Rating:** 1500  
**Tags:** dfs and similar, dsu, greedy, shortest paths  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have employees and directed supervisor offers between them. An offer `(a, b, c)` means employee `a` is willing to supervise employee `b` for cost `c`. Qualifications are strictly decreasing along every offer, so `q[a] > q[b]`.

The final hierarchy must be a rooted tree. One employee becomes the overall boss and has no supervisor. Every other employee must have exactly one incoming edge, meaning exactly one direct supervisor. The total cost of all chosen offers should be as small as possible.

The qualification restriction is the key structural property. Since every edge goes from higher qualification to lower qualification, cycles can never exist. The graph is already a DAG ordered by qualification.

The limits are small enough to allow graph algorithms with quadratic behavior. We have at most `1000` employees and `10000` offers. An `O(m log m)` or `O(m α(n))` solution is easily fast enough. Even `O(n^2)` passes are acceptable. Exhaustive search over all subsets of edges is impossible because there can be up to `2^10000` choices.

The dangerous part is that a minimum-cost incoming edge for every node does not automatically guarantee a valid hierarchy. The chosen edges must connect all employees into one rooted structure.

Consider this example:

```
3
10 9 8
2
1 2 1
1 3 1
```

The answer is `2`. Employee `1` is the root and both others point to it indirectly through the chosen edges.

Now consider:

```
3
10 9 8
1
1 2 1
```

Employee `3` has no possible supervisor at all. The correct answer is `-1`.

A careless implementation might also incorrectly require the graph to be connected in the undirected sense. That is unnecessary because the qualification ordering already forbids cycles. We only need every non-root node to have one parent.

Another subtle case is when multiple employees have no incoming offers.

```
4
10 8 6 4
1
1 2 5
```

Employees `3` and `4` cannot be supervised by anyone. A rooted tree can only have one root, so the answer is `-1`.

The qualification ordering also implies something stronger. The employee with maximum qualification can never have a supervisor, because no higher-qualified employee exists. If there are several employees with the same maximum qualification, no edges can exist between them either, since offers require strict inequality. Then multiple roots become unavoidable and the answer is immediately `-1`.

## Approaches

A brute-force solution would try all subsets of offers with exactly `n - 1` edges and check whether they form a valid rooted tree. The validation itself is easy because the graph is acyclic, but the number of subsets is astronomical. With `10000` edges, even iterating over all subsets is hopeless.

A more intelligent brute-force idea is to think in terms of incoming edges. Every employee except the root must choose exactly one supervisor. Since the graph is acyclic already, if every node except one has indegree exactly one, the structure automatically becomes a rooted tree.

This observation changes the problem completely.

Because qualifications strictly decrease along edges, cycles are impossible. That means we do not need DSU, MST logic, or cycle detection at all. The only thing that matters is whether every non-root employee has at least one incoming offer. If so, choosing the cheapest incoming edge for each such employee is always optimal.

Why? Because the choice for one employee never affects the validity of another employee's choice. There are no cycles to accidentally create. The graph structure guarantees consistency automatically.

So the optimal algorithm becomes:

For every employee, find the minimum-cost incoming edge. Exactly one employee is allowed to have no incoming edge, that employee becomes the root. If more than one employee lacks incoming edges, building the hierarchy is impossible.

This reduces the problem to a simple scan over all edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(m) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an array `best` where `best[i]` stores the minimum cost of any edge entering employee `i`.
2. Initialize every value in `best` with infinity, meaning no supervisor offer has been seen yet.
3. Process every application `(a, b, c)`.

Employee `a` can supervise employee `b` for cost `c`. Since only the cheapest incoming edge matters, update:

```
best[b] = min(best[b], c)
```
4. After processing all offers, scan all employees.

If `best[i]` is still infinity, employee `i` has no possible supervisor.
5. Count how many employees have no incoming edge.

A valid hierarchy must have exactly one such employee, the root.
6. If the count is not exactly one, print `-1`.

Zero roots are impossible because the graph is acyclic. More than one root means the company splits into disconnected components.
7. Otherwise, sum all finite values in `best`.

These are exactly the costs of the chosen supervisor edges.

### Why it works

The crucial invariant is that the offer graph is acyclic because qualifications strictly decrease along every edge.

Suppose every employee except one has exactly one incoming edge. In any finite DAG, that structure must form a rooted tree. Cycles cannot exist, and all nodes eventually trace upward to the unique node with indegree zero.

Since the parent choice for one employee never affects feasibility for another employee, minimizing each incoming edge independently minimizes the global total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

n = int(input())
q = list(map(int, input().split()))

m = int(input())

best = [INF] * n

for _ in range(m):
    a, b, c = map(int, input().split())
    b -= 1
    best[b] = min(best[b], c)

roots = 0
answer = 0

for x in best:
    if x == INF:
        roots += 1
    else:
        answer += x

if roots != 1:
    print(-1)
else:
    print(answer)
```

The array `best` stores the minimum incoming edge cost for each employee. We never need adjacency lists because the final answer depends only on the cheapest incoming edge per node.

The qualification values are read but never used directly. Their purpose is already encoded in the guarantees about the edges. Since every offer satisfies `q[a] > q[b]`, the graph is acyclic automatically.

A common mistake is trying to run Kruskal or Prim. Minimum spanning tree algorithms solve undirected connectivity problems, but this problem is fundamentally different. We already know the graph direction eliminates cycles, so independent local minimization is sufficient.

Another easy mistake is forgetting that employee numbering in the input is `1`-based. The code converts `b` to `0`-based indexing before updating `best`.

The variable `roots` counts employees with no incoming edge. Exactly one such employee must exist. If there are multiple employees without supervisors, they cannot be connected into one hierarchy.

## Worked Examples

### Sample 1

Input:

```
4
7 2 3 1
4
1 2 5
2 4 1
3 4 1
1 3 5
```

Processing edges:

| Edge | Updated `best` |
| --- | --- |
| 1 → 2 cost 5 | [INF, 5, INF, INF] |
| 2 → 4 cost 1 | [INF, 5, INF, 1] |
| 3 → 4 cost 1 | [INF, 5, INF, 1] |
| 1 → 3 cost 5 | [INF, 5, 5, 1] |

Final scan:

| Employee | Minimum Incoming Cost |
| --- | --- |
| 1 | INF |
| 2 | 5 |
| 3 | 5 |
| 4 | 1 |

There is exactly one root, employee `1`. The total cost is `5 + 5 + 1 = 11`.

This trace demonstrates the central idea of the solution. Employee `4` has two possible supervisors, but only the cheaper incoming edge matters.

### Impossible Example

Input:

```
3
10 9 8
1
1 2 1
```

Processing edges:

| Edge | Updated `best` |
| --- | --- |
| 1 → 2 cost 1 | [INF, 1, INF] |

Final scan:

| Employee | Minimum Incoming Cost |
| --- | --- |
| 1 | INF |
| 2 | 1 |
| 3 | INF |

Two employees have no incoming edge. That means two separate roots would be required, which violates the hierarchy requirement. The algorithm prints `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | One pass over employees and offers |
| Space | O(n) | Stores minimum incoming cost for each employee |

With at most `10000` offers, a linear scan is extremely fast. The memory usage is tiny because only one array of size `n` is maintained.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    INF = 10**18

    n = int(input())
    q = list(map(int, input().split()))

    m = int(input())

    best = [INF] * n

    for _ in range(m):
        a, b, c = map(int, input().split())
        b -= 1
        best[b] = min(best[b], c)

    roots = 0
    ans = 0

    for x in best:
        if x == INF:
            roots += 1
        else:
            ans += x

    print(ans if roots == 1 else -1)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
"""4
7 2 3 1
4
1 2 5
2 4 1
3 4 1
1 3 5
"""
) == "11", "sample 1"

# impossible case
assert run(
"""3
10 9 8
1
1 2 1
"""
) == "-1", "multiple roots"

# minimum size
assert run(
"""1
5
0
"""
) == "0", "single employee is root"

# choose cheapest incoming edge
assert run(
"""3
10 5 1
3
1 2 10
1 2 3
2 3 7
"""
) == "10", "minimum incoming edge"

# disconnected components
assert run(
"""4
10 9 8 7
2
1 2 1
3 4 1
"""
) == "-1", "two roots"

# chain structure
assert run(
"""5
9 8 7 6 5
4
1 2 1
2 3 2
3 4 3
4 5 4
"""
) == "10", "simple chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single employee, no edges | 0 | One-node hierarchy |
| Multiple edges into same node | 10 | Cheapest incoming edge selection |
| Two disconnected chains | -1 | Multiple roots detection |
| Simple chain | 10 | Standard valid hierarchy |
| Missing supervisor for one node | -1 | Impossible construction |

## Edge Cases

Consider the case where several offers target the same employee.

```
3
10 5 1
3
1 2 10
1 2 3
2 3 7
```

Employee `2` has incoming costs `10` and `3`. The algorithm stores only the minimum, `3`. Employee `3` receives cost `7`. The total becomes `10`. Since the graph is acyclic already, there is never a reason to choose a more expensive incoming edge.

Now consider multiple unavoidable roots.

```
4
10 9 8 7
2
1 2 1
3 4 1
```

Employees `1` and `3` both have no incoming edge. The algorithm counts two roots and immediately returns `-1`. Even though every other employee has a supervisor, the company splits into two independent hierarchies.

The smallest possible input is also important.

```
1
42
0
```

There is exactly one employee and no edges. The lone employee naturally becomes the root. The algorithm finds one node with no incoming edge and sums zero costs, producing `0`.

Finally, consider a node with no possible supervisor.

```
3
10 8 6
1
1 2 5
```

Employee `3` never receives an incoming edge, so both employees `1` and `3` would need to be roots. The algorithm detects two nodes with infinite incoming cost and prints `-1`.
