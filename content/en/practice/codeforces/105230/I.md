---
title: "CF 105230I - Pizzas"
description: "We are given a set of ingredients, and some pairs of ingredients are known to taste the same. That relation is not just pairwise, it extends transitively, so if ingredient A matches B and B matches C, then A, B, and C all belong to the same flavor group."
date: "2026-06-24T16:01:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105230
codeforces_index: "I"
codeforces_contest_name: "2024-2025 ICPC Bolivia Pre-National Contest"
rating: 0
weight: 105230
solve_time_s: 77
verified: true
draft: false
---

[CF 105230I - Pizzas](https://codeforces.com/problemset/problem/105230/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of ingredients, and some pairs of ingredients are known to taste the same. That relation is not just pairwise, it extends transitively, so if ingredient A matches B and B matches C, then A, B, and C all belong to the same flavor group.

The process used to build a pizza is described as taking a random ordering of all ingredients and scanning them from left to right. When we see an ingredient, we try to add it. It is added only if it introduces a flavor that has not appeared before among already selected ingredients, according to the equivalence information. Otherwise it is ignored.

The final output is not about one execution. We are asked how many different ingredient sets can possibly be produced by this process over all possible permutations of the ingredients. Two pizzas are different if the actual sets of chosen ingredients differ, not just in ordering.

The constraint n up to 100000 and m up to 100000 implies we need essentially linear or near-linear processing. Any approach that tries to enumerate permutations or simulate ordering is impossible because n factorial is far too large, and even quadratic behavior over edges would risk timeouts.

A subtle difficulty is that the equivalence relation is transitive but only given as edges. A naive approach that only considers direct pairs would misclassify flavor groups.

Another tricky point is interpreting the randomness. The problem is not asking for probability or expected value over permutations. It is asking for the number of distinct resulting sets that can appear for any permutation.

## Approaches

A brute-force interpretation would be to generate every permutation of the n ingredients, simulate the scanning process, and store the resulting selected set. The simulation itself is linear in n, so this would be O(n · n!) time, which is immediately infeasible even for very small n. The bottleneck is not the simulation, but the explosion of possible orderings.

The key observation is that the only thing that matters about the graph of equal-flavor relations is its connected components. Inside a connected component, once any ingredient from that component is selected, every other ingredient in that component is considered to have an already seen flavor and will be rejected when encountered later.

Now consider what determines the final set for a fixed permutation. In each connected component, exactly one ingredient will be the first encountered in that permutation among that component. That ingredient is selected, and all others in the same component are skipped. This means every permutation produces a set containing exactly one representative from each connected component.

The crucial point is that different permutations can choose different representatives from the same component, and these choices are independent across components. In a component of size s, any of its s nodes can be the first one appearing in the permutation relative to that component, and therefore become the selected representative. Since components do not interfere with each other, the total number of possible pizzas is the product of component sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n · n!) | O(n) | Too slow |
| Connected components + counting | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We first interpret the given pairs as edges in an undirected graph. Two ingredients connected by a path belong to the same flavor group, so we need to compute connected components. This can be done using a disjoint set union structure or a DFS.

After grouping nodes into components, we compute the size of each component. Each component contributes independently to the final count because the ordering process never mixes how a component resolves its chosen representative.

Finally, for each component of size s, we multiply the answer by s, because there are exactly s choices for which node becomes the first encountered node of that component in the random permutation.

We take the product modulo 10^9 + 7.

Why it works is based on the invariant that in any permutation, exactly one element per connected component is selected, specifically the earliest element of that component in the ordering. The mapping from permutations to resulting pizzas is determined entirely by the choice of this earliest element in each component. Every such choice is achievable by constructing a permutation where that chosen element appears before all other elements of its component, and components do not constrain each other, so these choices multiply independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    n, m = map(int, input().split())
    dsu = DSU(n)

    for _ in range(m):
        a, b = map(int, input().split())
        dsu.union(a - 1, b - 1)

    comp_size = {}
    for i in range(n):
        r = dsu.find(i)
        comp_size[r] = comp_size.get(r, 0) + 1

    ans = 1
    for sz in comp_size.values():
        ans = (ans * sz) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds connected components using a disjoint set union structure. Each union merges flavor-equivalent ingredients into a single representative set.

After processing all edges, we iterate through all nodes once to count the size of each root component. This step is necessary because DSU only maintains structure, not explicit component listings.

The final loop multiplies the sizes of all components under modulo arithmetic. The result directly corresponds to the number of ways each component can contribute its representative ingredient.

## Worked Examples

### Sample 1

Input:

```
5 3
1 3
2 4
3 5
```

We form components by merging connected ingredients.

| Step | Edge | DSU Components (conceptual) |
| --- | --- | --- |
| 1 | 1-3 | {1,3}, {2}, {4}, {5} |
| 2 | 2-4 | {1,3}, {2,4}, {5} |
| 3 | 3-5 | {1,3,5}, {2,4} |

Now we compute sizes 3 and 2. The answer is 3 × 2 = 6.

This shows that each component contributes independently, and permutations only decide which element becomes the first seen in its group.

### Sample 2

Input:

```
20 9
1 9
2 6
2 16
6 20
7 13
8 15
10 20
16 18
17 18
```

We track the main merges:

| Component | Members | Size |
| --- | --- | --- |
| A | {1,9} | 2 |
| B | {2,6,16,20,10,18,17} | 7 |
| C | {7,13} | 2 |
| D | {8,15} | 2 |

The product is 2 × 7 × 2 × 2 = 56.

This confirms that even large connected components behave the same way: they only contribute multiplicatively through their size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m α(n)) | DSU operations with near-constant amortized find/union plus a single pass over nodes |
| Space | O(n) | Parent and size arrays plus component counting map |

The constraints allow up to 100000 nodes and edges, so a near-linear DSU solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else __import__("builtins").open  # placeholder
```

Since we cannot directly capture stdout in this format cleanly without restructuring the solver, below are assert-style logical tests assuming solve() is adapted to return a string.

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""5 3
1 3
2 4
3 5
""") == "6"

assert run("""20 9
1 9
2 6
2 16
6 20
7 13
8 15
10 20
16 18
17 18
""") == "56"

# single node
assert run("""1 0
""") == "1"

# all isolated
assert run("""4 0
""") == "1"

# chain
assert run("""4 3
1 2
2 3
3 4
""") == "4"

# fully connected
assert run("""4 6
1 2
2 3
3 4
1 3
1 4
2 4
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | base case |
| no edges | 1 | all singleton components |
| chain graph | 4 | one component of size n |
| complete graph | 4 | single large component |

## Edge Cases

When there are no edges, every ingredient forms its own component. The algorithm treats each node as a separate root, and the product becomes 1 repeatedly, resulting in 1, which matches the fact that every permutation yields the same deterministic selection pattern across singleton components.

When all ingredients are connected through a chain, the DSU compresses everything into one component. The final answer becomes n, since any of the n nodes can be the first encountered in that component, and that fully determines the resulting pizza set.

When components are highly unbalanced, such as one large component and many isolated nodes, the multiplication still works correctly because isolated nodes contribute a factor of 1, leaving only the large component size to determine variability.
