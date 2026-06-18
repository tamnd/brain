---
problem: 1388C
contest_id: 1388
problem_index: C
name: "Uncle Bogdan and Country Happiness"
contest_name: "Codeforces Round 660 (Div. 2)"
rating: 1800
tags: ["dfs and similar", "greedy", "math", "trees"]
answer: passed_samples
verified: true
solve_time_s: 155
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e786e-940c-83ec-aff8-b894ca81a057
---

# CF 1388C - Uncle Bogdan and Country Happiness

**Rating:** 1800  
**Tags:** dfs and similar, greedy, math, trees  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 35s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e786e-940c-83ec-aff8-b894ca81a057  

---

## Solution

## Problem Understanding

The country is a tree of cities rooted at city 1, and every citizen starts their day in the capital before returning to their home city along the unique shortest path in the tree. Each city has a known population split across cities, and every person contributes either +1 or −1 depending on whether they are in a good or bad mood.

The key observation is that the only time a person can affect a city’s happiness index is when they pass through it on their path from the capital to their home. Since all paths are simple root-to-node paths, every citizen contributes along exactly one path in the tree.

For each city, we are given a target value h[i], which is supposed to equal the final sum of contributions of all people passing through that city. The task is to determine whether there exists an assignment of moods (good or bad) and possible mood changes along paths such that all these h[i] values can be achieved simultaneously.

The constraints push us toward a linear or near linear solution per test case. With up to 2⋅10^5 total nodes and up to 10^4 test cases, any solution that does more than O(n) per test case or O(n log n) overall is at risk. A naive simulation that tracks every person individually is impossible because m can be as large as 10^9.

A subtle edge case appears when a city has no population but a nonzero h[i]. For example, if a leaf city has p[i] = 0 but h[i] = 5, this is immediately impossible since no path can generate extra people there. Another tricky situation is when values locally look consistent but globally violate conservation of flow from parent to children.

## Approaches

A brute-force interpretation would treat each person separately. We could imagine assigning each of the m people a mood and simulating their path from the root to their home, marking contributions at every visited node. This is conceptually correct but immediately infeasible since each person may traverse up to O(n) nodes, giving O(nm) operations, which is far beyond limits when m reaches 10^9.

We need to shift from thinking about individuals to thinking about aggregated flows. Instead of tracking people, we track how many people must pass through each subtree and how many of them are allowed to be bad. The key insight is that the tree structure forces a recursive decomposition: each subtree must “explain” its required happiness using only the people inside it plus what flows from above.

We root the tree at 1 and perform a DFS. At each node, we compute how many people are in its subtree (call it total) and how many of them must be good to satisfy the required happiness constraints. The problem becomes a feasibility check on whether these required good counts can stay within valid bounds at every subtree.

At node u, if we already know that a child subtree requires more “good contributions” than available people in that subtree, the configuration is impossible. Similarly, if the required number of good people is negative or exceeds total available people, it is impossible.

This leads to a greedy postorder traversal where each subtree aggregates its requirements upward, and feasibility is checked locally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate individuals) | O(nm) | O(nm) | Too slow |
| Tree DFS with subtree aggregation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at node 1 and treat it as a directed structure from parent to children.

1. Build an adjacency list for the tree. This allows efficient traversal in O(n).
2. Run a DFS from the root. For each node u, we compute two values from its children: the total number of people in its subtree and the number of “required good people” that must exist in that subtree to satisfy all constraints below.

The reason we use a postorder traversal is that a node’s feasibility depends entirely on how its children distribute their required contributions.
3. At each node u, initialize total_people = p[u] and required_good = 0.
4. For every child v of u, recursively compute its (total_v, good_v). Add total_v to total_people and add good_v to required_good.

This aggregation reflects that all people in child subtrees must pass through u before reaching the root, so their constraints accumulate upward.
5. After processing children, incorporate the happiness constraint h[u]. Let current balance be the difference between good and bad contributions passing through u. Since total people in subtree is fixed, we interpret required_good as the number of people that must remain good in this subtree to achieve h[u].

We translate h[u] into a constraint on how many good people must exist in subtree u:

required_good = (total_people + h[u]) / 2.

This comes from solving:

good - bad = h[u]

good + bad = total_people

which implies:

good = (total_people + h[u]) / 2
6. If (total_people + h[u]) is odd or required_good is outside [0, total_people], return impossible.
7. Return (total_people, required_good) upward to the parent.
8. If the root is feasible, answer YES.

### Why it works

Each subtree is treated as a closed system where all people inside it contribute exactly once to every node on their path to the root. Because contributions are additive and paths are unique in a tree, each subtree only needs to ensure that the number of good assignments it claims is consistent with its total population and the required net difference h[u]. The DFS ensures that all descendant constraints are satisfied before a node commits to a value, so any violation must be detected at the earliest possible subtree boundary.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    h = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)

    def dfs(u, parent):
        total = p[u]
        good = 0

        for v in g[u]:
            if v == parent:
                continue
            t_v, g_v = dfs(v, u)
            total += t_v
            good += g_v

        if (total + h[u]) % 2 != 0:
            return -1, -1

        req_good = (total + h[u]) // 2

        if req_good < 0 or req_good > total:
            return -1, -1

        if good > req_good:
            return -1, -1

        return total, req_good

    ok_total, ok_good = dfs(0, -1)
    print("YES" if ok_total != -1 else "NO")

t = int(input())
for _ in range(t):
    solve()
```

The DFS returns two values per node: the total population in its subtree and the required number of good people needed to satisfy the happiness constraint at that node. The parity check enforces that a valid split between good and bad people exists.

A common mistake is ignoring the parity condition. Since good and bad are integers, (total + h[u]) must be even. Another subtle point is ensuring that the computed required_good does not exceed the subtree total or fall below zero.

## Worked Examples

### Example 1

Input:

```
1
3 3
1 1 1
1 1 -1
1 2
1 3
```

Tree:

1 is root, children 2 and 3.

| Node | total subtree | h[u] | required_good | validity |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 | OK |
| 3 | 1 | -1 | 0 | OK |
| 1 | 3 | 1 | 2 | OK |

Both children are valid, and root constraint is consistent.

This shows how subtree values are independently valid and combine cleanly at the root.

### Example 2

Input:

```
1
2 2
1 1
-1 1
1 2
```

| Node | total subtree | h[u] | required_good | validity |
| --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 1 | OK |
| 1 | 2 | -1 | 0.5 | invalid |

At the root, parity fails immediately because total + h is odd. This captures a case where local subtree consistency exists but global feasibility breaks due to integer constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node and edge is visited once in DFS |
| Space | O(n) | Adjacency list and recursion stack |

The total number of nodes across test cases is at most 2⋅10^5, so a linear DFS per test case remains within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    output = []
    def input():
        return sys.stdin.readline().strip()

    def solve_all():
        t = int(input())
        for _ in range(t):
            n, m = map(int, input().split())
            p = list(map(int, input().split()))
            h = list(map(int, input().split()))
            g = [[] for _ in range(n)]
            for _ in range(n - 1):
                a, b = map(int, input().split())
                g[a-1].append(b-1)
                g[b-1].append(a-1)

            sys.setrecursionlimit(10**7)

            def dfs(u, par):
                total = p[u]
                good = 0
                for v in g[u]:
                    if v == par:
                        continue
                    t, gg = dfs(v, u)
                    total += t
                    good += gg
                if (total + h[u]) % 2 != 0:
                    return -1, -1
                req = (total + h[u]) // 2
                if req < 0 or req > total:
                    return -1, -1
                if good > req:
                    return -1, -1
                return total, req

            ok = dfs(0, -1)[0] != -1
            output.append("YES" if ok else "NO")

    solve_all()
    return "\n".join(output)

# provided samples
assert run("""2
7 4
1 0 1 1 0 1 0
4 0 0 -1 0 -1 0
1 2
1 3
1 4
3 5
3 6
3 7
5 11
1 2 5 2 1
-11 -2 -6 -2 -1
1 2
1 3
1 4
3 5
""") == "YES\nYES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | YES | base case correctness |
| star tree with invalid parity | NO | parity constraint detection |
| deep chain consistent values | YES | propagation correctness |
| inconsistent subtree requirement | NO | local feasibility failure |

## Edge Cases

A key edge case is when a subtree has zero population but a nonzero required happiness. For example, a leaf node with p[i] = 0 and h[i] = 2 immediately fails because no assignment of good or bad states exists. The DFS catches this when computing (total + h[i]) / 2, which produces a negative or fractional value.

Another important case is when all constraints are locally valid but a parent node demands fewer good people than already fixed by children. In that situation, good > required_good triggers failure, ensuring that child commitments are not violated by higher-level aggregation.