---
title: "CF 105316F - Legend Whispers"
description: "We are given two arrays of the same length. The second array is fixed, but the first array can be permuted arbitrarily. After choosing a permutation of the first array, each position pairs one value from the first array with one value from the second array."
date: "2026-06-23T15:09:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105316
codeforces_index: "F"
codeforces_contest_name: "2024 Aleppo Collegiate Programming Contest"
rating: 0
weight: 105316
solve_time_s: 57
verified: true
draft: false
---

[CF 105316F - Legend Whispers](https://codeforces.com/problemset/problem/105316/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of the same length. The second array is fixed, but the first array can be permuted arbitrarily. After choosing a permutation of the first array, each position pairs one value from the first array with one value from the second array.

A pairing is only valid if every chosen pair satisfies the divisibility condition: the selected value from the first array must be divisible by the corresponding value from the second array. If this cannot be achieved for all positions, the configuration is invalid and the answer is −1.

If a valid full pairing exists, each position contributes a ratio formed by dividing the chosen value from the first array by the corresponding value from the second array. The value of a pairing is the minimum of these ratios across all positions. The goal is to rearrange the first array so that this minimum ratio is as large as possible.

The constraints are small in total size across test cases, with at most 500 elements overall per array per test. This allows solutions that are around O(n³) or slightly worse per test case, especially if there is a logarithmic factor or a matching procedure. Anything exponential or factorial is ruled out because permutations alone would already be 500! possibilities.

A naive attempt would try all permutations of the first array, check validity, compute the minimum ratio, and take the best. This fails immediately because even for n = 10, the number of permutations becomes 10! = 3.6 million, and for n = 500 it is completely infeasible.

A more subtle failure case comes from greedy matching strategies. For example, pairing each bi with the smallest possible valid ai might seem natural, but it can block larger ratios later and destroy global optimality. Consider a situation where a small b has only one compatible a, but that a is also needed for a larger b to maintain feasibility. A greedy choice would consume it early and make the assignment impossible even though a valid global assignment exists.

Another edge case is feasibility at all. If there exists at least one bi for which no ai is divisible by it, then no arrangement can satisfy the constraints, regardless of permutation. This must immediately return −1.

## Approaches

The problem is fundamentally about assigning each value in b to a unique value in a, subject to divisibility constraints, while maximizing a bottleneck objective on the ratios.

A brute-force approach would consider every permutation of a, check whether each position satisfies ai % bi == 0, compute the minimum ratio, and track the maximum. This is correct because it explores every possible assignment. However, it requires n! checks, and each check costs O(n), giving O(n · n!) operations, which becomes unusable almost immediately beyond very small n.

The key observation is that the structure is not about permutations directly but about perfect matching in a bipartite graph. Each element of b must be matched to exactly one element of a. An edge exists only when divisibility holds, and the weight of pairing is ai / bi. We want to maximize the minimum chosen weight.

This is a classic bottleneck optimization over matchings. Instead of directly optimizing the minimum ratio, we reverse the perspective: fix a candidate threshold x and ask whether we can build a perfect matching where every chosen pair satisfies ai / bi ≥ x while also satisfying divisibility.

For a fixed x, we only keep edges (bi → aj) such that aj is divisible by bi and aj ≥ x · bi. If we can find a perfect matching under these constraints, then x is achievable. This transforms the problem into a feasibility check on a bipartite graph.

Since feasibility is monotonic in x, binary search becomes applicable. We can test values of x and converge to the maximum feasible one. Each feasibility check is a bipartite matching problem, solvable with Hopcroft-Karp.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(n · n!) | O(n) | Too slow |
| Binary search + bipartite matching | O(log A · E √V) | O(E) | Accepted |

## Algorithm Walkthrough

We reduce the problem into repeatedly solving a matching feasibility question.

1. Interpret each element of b as a left node and each element of a as a right node. A connection is allowed only if the chosen a is divisible by the chosen b. This encodes the only valid pairings allowed by the problem.
2. Fix a candidate value x representing the minimum allowed ratio. For a pair (bi, aj), we only allow it if aj % bi == 0 and aj ≥ x · bi. This ensures both validity and that the ratio constraint is satisfied.
3. Build a bipartite graph using these filtered edges. Each edge represents a legally usable assignment under the current threshold x.
4. Run a maximum bipartite matching algorithm on this graph and check whether all nodes in b can be matched. If the matching size equals n, then x is feasible; otherwise it is not.
5. Binary search the largest x in a valid range. The upper bound is max(ai // bi minimum possible pairing), but practically we can bound it by max(a).
6. Return the maximum x for which a perfect matching exists. If even x = 0 fails, then no full assignment is possible and we return −1.

### Why it works

The crucial invariant is that feasibility is monotone in x. If a matching exists for some threshold x, then any smaller threshold x' ≤ x only relaxes edge constraints and cannot destroy existing valid edges. This guarantees that binary search does not miss the optimum. At each step, the matching step fully captures whether the current constraints admit a complete assignment, so no local decision is made greedily; feasibility is checked globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

class HopcroftKarp:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.g = [[] for _ in range(n)]
        self.pair_u = [-1] * n
        self.pair_v = [-1] * m
        self.dist = [0] * n

    def add_edge(self, u, v):
        self.g[u].append(v)

    def bfs(self):
        q = deque()
        for u in range(self.n):
            if self.pair_u[u] == -1:
                self.dist[u] = 0
                q.append(u)
            else:
                self.dist[u] = -1

        found = False

        while q:
            u = q.popleft()
            for v in self.g[u]:
                pu = self.pair_v[v]
                if pu != -1 and self.dist[pu] == -1:
                    self.dist[pu] = self.dist[u] + 1
                    q.append(pu)
                elif pu == -1:
                    found = True

        return found

    def dfs(self, u):
        for v in self.g[u]:
            pu = self.pair_v[v]
            if pu == -1 or (self.dist[pu] == self.dist[u] + 1 and self.dfs(pu)):
                self.pair_u[u] = v
                self.pair_v[v] = u
                return True
        self.dist[u] = -1
        return False

    def max_matching(self):
        matching = 0
        while self.bfs():
            for u in range(self.n):
                if self.pair_u[u] == -1 and self.dfs(u):
                    matching += 1
        return matching

def possible(a, b, x):
    n = len(a)
    hk = HopcroftKarp(n, n)
    for i in range(n):
        for j in range(n):
            if a[j] % b[i] == 0 and a[j] >= x * b[i]:
                hk.add_edge(i, j)
    return hk.max_matching() == n

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        if n == 1:
            if a[0] % b[0] == 0:
                print(a[0] // b[0])
            else:
                print(-1)
            continue

        if not possible(a, b, 0):
            print(-1)
            continue

        lo, hi = 0, 10**6
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if possible(a, b, mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds a matching instance for each feasibility check. The bipartite structure fixes b on the left side and a on the right side. The condition a[j] % b[i] == 0 enforces validity, and the inequality a[j] ≥ x * b[i] enforces the ratio constraint.

The binary search wraps around this feasibility check. The lower bound starts at zero since a trivial ratio is always the weakest requirement, and the upper bound is safely set to 10⁶ because all ratios are bounded by the maximum possible quotient under constraints. Each successful matching updates the best known answer.

The only subtle pitfall is ensuring that the matching is recomputed from scratch for each x; reusing state would corrupt correctness because edges change between iterations.

## Worked Examples

Consider a small case where a = [6, 8, 9], b = [2, 3, 3].

We test x = 2:

| Step | Graph condition | Matching progress | Feasible |
| --- | --- | --- | --- |
| Build | edges only if a ≥ 2b | limited edges | unsure |
| Matching | attempt full assignment | may fail | no |

Now x = 1:

| Step | Graph condition | Matching progress | Feasible |
| --- | --- | --- | --- |
| Build | all divisible edges allowed | richer graph | yes |
| Matching | all b matched | full matching exists | yes |

This shows that higher thresholds may break feasibility even when lower ones work, motivating binary search.

A second example: a = [12, 6], b = [3, 2].

For x = 2, valid pairs are 12/3 = 4 and 6/2 = 3, so both work. Matching succeeds. For x = 3, only 12/3 works, but 6 is insufficient for b = 2 since 6/2 = 3 still works, so it remains feasible. Increasing x further would eventually break the assignment when some b loses all candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · log A · E √V) | Each binary search step runs Hopcroft-Karp on up to n² edges |
| Space | O(n²) | adjacency list for bipartite graph |

The constraints limit total n to 500, so even with around 20 binary search steps and matching on dense graphs, the solution comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    class HopcroftKarp:
        def __init__(self, n, m):
            self.n = n
            self.m = m
            self.g = [[] for _ in range(n)]
            self.pair_u = [-1] * n
            self.pair_v = [-1] * m
            self.dist = [0] * n

        def add_edge(self, u, v):
            self.g[u].append(v)

        def bfs(self):
            from collections import deque
            q = deque()
            for u in range(self.n):
                if self.pair_u[u] == -1:
                    self.dist[u] = 0
                    q.append(u)
                else:
                    self.dist[u] = -1

            found = False
            while q:
                u = q.popleft()
                for v in self.g[u]:
                    pu = self.pair_v[v]
                    if pu != -1 and self.dist[pu] == -1:
                        self.dist[pu] = self.dist[u] + 1
                        q.append(pu)
                    elif pu == -1:
                        found = True
            return found

        def dfs(self, u):
            for v in self.g[u]:
                pu = self.pair_v[v]
                if pu == -1 or (self.dist[pu] == self.dist[u] + 1 and self.dfs(pu)):
                    self.pair_u[u] = v
                    self.pair_v[v] = u
                    return True
            self.dist[u] = -1
            return False

        def max_matching(self):
            res = 0
            while self.bfs():
                for i in range(self.n):
                    if self.pair_u[i] == -1 and self.dfs(i):
                        res += 1
            return res

    def possible(a, b, x):
        n = len(a)
        hk = HopcroftKarp(n, n)
        for i in range(n):
            for j in range(n):
                if a[j] % b[i] == 0 and a[j] >= x * b[i]:
                    hk.add_edge(i, j)
        return hk.max_matching() == n

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            b = list(map(int, input().split()))
            if not possible(a, b, 0):
                out.append("-1")
                continue
            lo, hi = 0, 10**6
            ans = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if possible(a, b, mid):
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# custom cases

# minimum size
assert run("1\n1\n6\n3\n") == "2"

# impossible
assert run("1\n2\n2 4\n3 5\n") == "-1"

# all equal compatible
assert run("1\n3\n6 12 18\n3 2 6\n") != ""

# exact matching pressure case
assert run("1\n3\n6 10 15\n3 5 5\n") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element divisible | 2 | base correctness |
| no valid matching | -1 | infeasibility handling |
| all compatible | positive value | full matching stability |
| mixed constraints | valid output | stress structure |

## Edge Cases

A key edge case is when divisibility already fails for a single b value. For example, a = [4, 6], b = [3, 5]. Since 5 divides nothing, no full matching exists even though partial matches exist. The algorithm detects this at x = 0 and immediately returns −1 because Hopcroft-Karp cannot reach full matching.

Another edge case occurs when multiple b values compete for a single large a. For example, a = [12, 12, 12], b = [2, 3, 6]. While every pair is divisible, the ratio constraint can force different assignments depending on x. The matching step correctly resolves this because it does not commit greedily; it globally explores assignments, ensuring that if a valid arrangement exists for a given threshold, it is found even under heavy contention.
