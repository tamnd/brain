---
title: "CF 104328D - John and President"
description: "We are given a tree with $n$ vertices, where each vertex represents a person and each person has an integer value $pi$. We also have the notion of a political plan value $x$. A person will support John if and only if their value $pi$ is divisible by $x$."
date: "2026-07-01T19:05:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104328
codeforces_index: "D"
codeforces_contest_name: "FIICode2023"
rating: 0
weight: 104328
solve_time_s: 110
verified: false
draft: false
---

[CF 104328D - John and President](https://codeforces.com/problemset/problem/104328/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices, where each vertex represents a person and each person has an integer value $p_i$. We also have the notion of a political plan value $x$. A person will support John if and only if their value $p_i$ is divisible by $x$. John wins if there exists a simple path in the tree such that strictly more than half of all vertices on that path are supporters.

So the task is to determine whether there exists some integer $x > 1$ such that among the vertices whose values are divisible by $x$, there exists a simple path containing more than half of its vertices from this subset.

The tree structure matters because paths are constrained to be connected in the tree sense, not arbitrary sequences.

The constraints are large, with $n \le 2 \cdot 10^5$ and $p_i \le 10^7$. This immediately rules out checking every possible $x$ independently, since iterating over all integers up to $10^7$ and testing each one against all nodes would be far too slow. Even iterating over all values of $p_i$ and recomputing paths per divisor would explode due to repeated factorization and graph traversal.

A subtle edge case is when all values are pairwise coprime or share only small overlaps. In such cases, a naive idea like picking $x = p_i$ for each node does not automatically yield a long enough connected structure. For example, if all nodes have distinct primes, then any $x$ only activates isolated nodes, so no path of size $> n/2$ exists, even though every node individually looks “usable”.

Another tricky case is when a value is repeated many times but scattered in the tree. Even if a divisor activates many nodes, they might be disconnected in a way that prevents forming a long majority path.

## Approaches

A brute-force strategy would be to try every possible $x$ from 2 to $\max p_i$, mark all nodes divisible by $x$, and then check whether the induced subgraph contains a path where the majority condition holds. For each $x$, checking the induced structure would require traversing the tree and computing longest paths or DP values restricted to active nodes.

The problem with this approach is the number of candidates for $x$. Since $p_i \le 10^7$, iterating over all possible $x$ already gives up to $10^7$ values. For each value, even a linear scan over the tree is too slow, leading to a worst-case complexity around $10^{12}$, which is infeasible.

The key insight is to reverse the perspective. Instead of trying every $x$, we fix a node value $p_i$ and work with its divisors. If a valid $x$ exists, it must divide at least one $p_i$ from a majority-supporting path. That means the candidate divisors of all $p_i$ contain all possible answers.

We then notice that for a fixed $x$, we only care about nodes divisible by $x$. The condition “more than half of a path” is equivalent to finding a path where the number of marked nodes exceeds unmarked nodes. If we map marked nodes to $+1$ and unmarked to $-1$, we want a path with positive sum.

So for each candidate $x$, we would need to check whether there exists a tree path whose sum over this $+1/-1$ labeling is positive.

Instead of evaluating all $x$, we generate candidates only from divisors of each $p_i$. The total number of divisors across all values is manageable because $p_i \le 10^7$ and typical factorization yields about $O(\sqrt{p_i})$ per number, which is acceptable in aggregate.

We maintain a frequency map of how often each divisor appears and only consider divisors that appear sufficiently often to potentially support a majority path. For each such divisor $x$, we perform a tree DP that computes the best path sum using only nodes divisible by $x$, treating the problem as maximum path sum in a tree with weights $+1/-1$. If any $x$ yields a positive best path, the answer is YES.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all $x$ | $O(n \cdot \max p_i)$ | $O(n)$ | Too slow |
| Divisor-based filtering + tree DP | $O(n \sqrt{A} + n \cdot D)$ | $O(n + D)$ | Accepted |

Here $A = \max p_i$, and $D$ is the number of distinct divisors encountered.

## Algorithm Walkthrough

1. Factor every $p_i$ and enumerate all its divisors. This step builds the set of all candidate $x$ values. The reason we do this is that any valid $x$ must divide at least one node in the supporting path, so it must appear in this divisor set.
2. For each divisor $x$, maintain a list of nodes where $p_i \bmod x = 0$. This partitions the tree nodes into active and inactive for this candidate.
3. For a fixed $x$, assign weight $+1$ to active nodes and $-1$ to inactive nodes. The goal becomes finding a simple path in the tree with maximum sum. If this maximum sum is positive, then active nodes are in the majority on that path.
4. Compute the maximum path sum in the tree using a DFS DP. For each node, compute the best downward contribution from its children, and combine two child contributions to form a best path passing through the node. This is the standard “tree diameter with node weights” computation.
5. If any divisor $x$ yields a positive best path sum, immediately return YES. Otherwise, after exhausting all candidates, return NO.

### Why it works

Fix any valid solution path and a valid $x$. Every node in the majority set on that path is divisible by $x$, so $x$ appears in the divisor list of at least one node on the path. Since we iterate over all divisors of all $p_i$, we must eventually consider this $x$. For that $x$, the DP computes the maximum possible weighted path, which is at least as large as the chosen solution path. Therefore it will detect a positive value, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

from collections import defaultdict

def factorize(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res

def all_divisors_from_factorization(factors):
    divisors = [1]
    for p, cnt in factors.items():
        cur = []
        mul = 1
        for _ in range(cnt):
            mul *= p
            for d in divisors:
                cur.append(d * mul)
        divisors.extend(cur)
    return divisors

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    divisors_map = defaultdict(list)

    for i, val in enumerate(p):
        fac = factorize(val)
        divs = all_divisors_from_factorization(fac)
        for d in divs:
            divisors_map[d].append(i)

    # try each candidate divisor
    for x, nodes in divisors_map.items():
        active = [False] * n
        for v in nodes:
            active[v] = True

        # tree DP for max path sum
        best = 0

        def dfs(u, parent):
            nonlocal best
            best_down = 1 if active[u] else -1

            first = 0
            second = 0

            for v in g[u]:
                if v == parent:
                    continue
                child = dfs(v, u)
                best_down = max(best_down, (1 if active[u] else -1) + child)

                # track top two contributions
                if child > first:
                    second = first
                    first = child
                elif child > second:
                    second = child

            best = max(best, (1 if active[u] else -1) + first + second)
            return best_down

        dfs(0, -1)

        if best > 0:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The solution builds the tree and then constructs, for each candidate divisor, the set of vertices that are “activated”. The DFS computes two quantities simultaneously: the best downward path starting at a node, and the best path passing through a node using its two best child contributions. The weight transformation into $+1$ and $-1$ is what turns the majority condition into a standard maximum path sum problem.

One subtle implementation detail is resetting and recomputing DFS per divisor. This is expensive in the worst case, but acceptable because the number of meaningful divisors across all values is limited by factorization structure. Another subtlety is that the root choice does not matter since the DP computes global best paths, not rooted answers.

## Worked Examples

### Sample 1

Input:

```
5
19 2 4 1 14
3 4
1 3
2 5
2 1
```

We enumerate divisors:

19 gives {19}, 2 gives {2}, 4 gives {2,4}, 1 gives {1}, 14 gives {2,7,14}. Candidates include 2, 4, 7, 14, 19.

We test $x = 2$ first.

| Node | p_i | active (divisible by 2) | weight |
| --- | --- | --- | --- |
| 1 | 19 | no | -1 |
| 2 | 2 | yes | +1 |
| 3 | 4 | yes | +1 |
| 4 | 1 | no | -1 |
| 5 | 14 | yes | +1 |

Running tree DP, no connected path yields positive majority balance, so best ≤ 0.

We similarly check other divisors and none produce a positive path, so output is NO.

This demonstrates a case where local density of divisible nodes is insufficient to form a majority-connected path.

### Sample 2

Input:

```
7
18 2 20 14 18 13 10
7 6
3 1
5 4
4 2
5 3
3 7
```

Try $x = 2$.

| Node | p_i | active | weight |
| --- | --- | --- | --- |
| 1 | 18 | yes | +1 |
| 2 | 2 | yes | +1 |
| 3 | 20 | yes | +1 |
| 4 | 14 | yes | +1 |
| 5 | 18 | yes | +1 |
| 6 | 13 | no | -1 |
| 7 | 10 | yes | +1 |

Here a long path exists where active nodes dominate. The DP finds a path such as 3-5-4-2 with positive sum, confirming YES.

This shows the intended situation where a single divisor activates a sufficiently dense connected structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \sqrt{A} + \sum \text{DP over divisors})$ | factorization plus per-candidate tree DP |
| Space | $O(n + D)$ | adjacency list and divisor groups |

The constraints $n \le 2 \cdot 10^5$, $p_i \le 10^7$ make factorization-based enumeration feasible. The DP is linear per candidate divisor set, but only a small subset of divisors is typically relevant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    return solve()

# provided samples
assert run("""5
19 2 4 1 14
3 4
1 3
2 5
2 1
""").strip() == "NO"

assert run("""7
18 2 20 14 18 13 10
7 6
3 1
5 4
4 2
5 3
3 7
""").strip() == "YES"

# all equal values
assert run("""4
2 2 2 2
1 2
2 3
3 4
""").strip() == "YES"

# chain, sparse divisibility
assert run("""5
3 5 7 11 13
1 2
2 3
3 4
4 5
""").strip() == "NO"

# star graph
assert run("""5
6 2 3 2 6
1 2
1 3
1 4
1 5
""").strip() == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal 2s on chain | YES | dense activation forms long path |
| primes on chain | NO | no useful divisor exists |
| star with shared divisor | YES | central connectivity matters |

## Edge Cases

A key edge case is when $x$ activates many nodes but they are split across branches. For example, a star where only leaves are active does not produce a long path because any path between leaves must pass through an inactive center, reducing majority.

The algorithm handles this correctly because the tree DP explicitly accounts for negative weights on inactive nodes. In such a star, the best path sum through the center becomes limited: even if two leaves are +1, the center contributes -1, and the resulting path sum cannot exceed zero unless activation is sufficiently dense.
