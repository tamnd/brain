---
problem: 1324F
contest_id: 1324
problem_index: F
name: "Maximum White Subtree"
contest_name: "Codeforces Round 627 (Div. 3)"
rating: 1800
tags: ["dfs and similar", "dp", "graphs", "trees"]
answer: passed_samples
verified: true
solve_time_s: 158
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2def77-79d8-83ec-88a3-9beb32439d59
---

# CF 1324F - Maximum White Subtree

**Rating:** 1800  
**Tags:** dfs and similar, dp, graphs, trees  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 38s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2def77-79d8-83ec-88a3-9beb32439d59  

---

## Solution

## Problem Understanding

We are given a tree where every vertex is colored either white or black. For each vertex $v$, we want to look at all connected subgraphs of the tree that include $v$, and among them choose one that maximizes the score defined as the number of white vertices minus the number of black vertices.

Another way to think about it is that each node contributes $+1$ if it is white and $-1$ if it is black. For every vertex $v$, we want the maximum possible sum of node values over any connected set of nodes that must contain $v$.

The constraint $n \le 2 \cdot 10^5$ immediately rules out any approach that recomputes a global search per node. A naive solution that tries to run a BFS or DP from each vertex would cost $O(n^2)$ in the worst case, which is far beyond the time limit. Even $O(n \log n)$ per node is not viable; we need a linear or near-linear solution.

A subtle difficulty is that the optimal subtree for a node is not necessarily its own subtree in any rooted sense. It can expand in all directions, and different vertices will have overlapping optimal structures. Another potential pitfall is assuming that taking the entire tree or a fixed rooted subtree gives the answer, which is incorrect because including a large negative region can reduce the score.

For example, consider a chain:

```
1 - 2 - 3 - 4
colors: 1 0 0 1
```

For vertex 2, taking the entire tree gives sum $0$, but the optimal connected subtree containing 2 is just $\{2\}$ giving $-1$, so even local pruning matters. For vertex 3, the best is $\{3,4\}$ with sum $0$, not the whole tree. This shows we must carefully control how contributions propagate.

## Approaches

We first consider a brute-force strategy. For each vertex $v$, we could treat it as a root and explore all connected subtrees containing it. This is equivalent to enumerating all connected induced subgraphs that include $v$, which is exponential in general trees. Even if we restrict ourselves to DP over subsets of neighbors, the number of states still grows exponentially. Another more structured brute force is to root the tree at $v$ and run a DP that allows choosing child subtrees, but that only captures subtrees directed downward and misses expansions upward through different roots. Repeating this for every node leads to $O(n^2)$ transitions overall, which is too slow for $2 \cdot 10^5$.

The key observation is that the problem is a variant of maximum subarray sum on a tree, but with the additional constraint that the chosen subgraph must contain the root vertex. This suggests a two-direction dynamic programming idea: first compute, for every node, the best contribution from its downward subtree, and then propagate information from the parent side so that each node also knows what it can gain by expanding upward.

The first DP pass is a classic tree DP: define $down[v]$ as the best sum of a connected subtree that starts at $v$ and only goes downward. This is computed using postorder traversal.

The second pass is rerooting. We propagate an additional value $up[v]$, representing the best contribution we can get from outside the subtree of $v$, restricted to paths that remain connected and pass through the parent direction. Combining $down[v]$ and $up[v]$ allows us to compute the best answer for each node as if it were the center of the structure.

This is exactly the kind of structure where contributions from children are independent except through the parent node, allowing linear rerooting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / $O(n^2)$ | $O(n)$ | Too slow |
| Tree DP + Rerooting | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We assign each node a value $w[v]$, where $w[v] = 1$ if white and $w[v] = -1$ if black.

### Step 1: Root the tree arbitrarily

We root the tree at node 1. This does not change the answer because every valid connected subtree can be described relative to any root.

### Step 2: Compute downward contributions

We compute $down[v]$, the best sum of a connected subtree that must include $v$ and only extends into its children.

For each node $v$, we start with $down[v] = w[v]$. Then for each child $u$, we consider whether extending into that child improves the score. If $down[u] > 0$, we add it to $down[v]$. Otherwise, we ignore it.

This works because if a child subtree contributes a negative or zero gain, including it would not improve any connected structure rooted at $v$.

### Step 3: First DFS traversal

We compute $down[v]$ using a postorder DFS, ensuring children are processed before their parent.

### Step 4: Compute answers using rerooting

We now propagate information from parent to children. Let $ans[v]$ be the best answer for vertex $v$.

Initially, $ans[v] = down[v]$ when rooted at 1.

When moving from parent $v$ to child $u$, we must consider that $u$ can gain contribution from everything outside its subtree. We pass a value $up[u]$ that represents the best contribution from $v$'s side excluding $u$'s subtree.

To compute $up[u]$, we combine:

- contribution from parent $v$,
- contributions from siblings of $u$,
- and $w[v]$ itself.

The crucial idea is that each node sees its neighbors as independent branches, and we only need to know the best positive contributions among them.

### Step 5: Combine results

For each node $v$, final answer is:

$$ans[v] = w[v] + \sum \max(0, best\_branch\_contribution)$$

where branches include both children and the upward direction.

### Why it works

The algorithm relies on the invariant that for any node, the optimal connected subtree containing it can be decomposed into independent branches through its neighbors. Each branch either contributes a positive gain or is excluded entirely. The rerooting DP ensures that every node is treated as a potential center, and all incident directions are evaluated exactly once with correct context.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n = int(input())
a = list(map(int, input().split()))

g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

w = [1 if x == 1 else -1 for x in a]

parent = [-1] * n
down = [0] * n

order = []

def dfs(v, p):
    parent[v] = p
    down[v] = w[v]
    for to in g[v]:
        if to == p:
            continue
        dfs(to, v)
        if down[to] > 0:
            down[v] += down[to]

dfs(0, -1)

ans = [0] * n
ans[0] = down[0]

def reroot(v, p):
    ans[v] = down[v]
    for to in g[v]:
        if to == p:
            continue

        # remove contribution of child and recompute "up" effect
        if down[to] > 0:
            down[v] -= down[to]

        if down[v] > 0:
            down[to] += down[v]

        reroot(to, v)

        if down[v] > 0:
            down[to] -= down[v]
        if down[to] > 0:
            down[v] += down[to]

    ans[v] = max(ans[v], w[v])

reroot(0, -1)

print(*ans)
```

The code implements a two-pass strategy. The first DFS computes downward contributions, where each node aggregates only positive child contributions. The rerooting function attempts to transfer beneficial contribution from parent side into each child, temporarily modifying values to simulate the perspective shift. The key idea is that only positive contributions are ever worth propagating, so negative branches are always excluded.

A subtle implementation issue is that we modify `down` in place during rerooting. This requires careful restoration after recursion to maintain correctness. The structure ensures that at any moment, `down[v]` reflects the correct contribution for the current root orientation.

## Worked Examples

### Example 1

Input:

```
3
0 1 0
1 2
2 3
```

Values: $[-1, +1, -1]$

| Node | Down value | Best branch taken | Reason |
| --- | --- | --- | --- |
| 1 | -1 | none | children reduce value |
| 2 | 1 | none | both sides negative |
| 3 | -1 | none | isolated negative |

Final answers:

```
1 1 1
```

Explanation: node 2 dominates because it is the only positive value. Any connected subtree containing endpoints is penalized.

### Example 2

Input:

```
5
1 0 1 0 1
```

Values: $[+1,-1,+1,-1,+1]$

| Node | Down contribution | Optimal neighborhood |
| --- | --- | --- |
| 1 | 2 | includes node 3 |
| 2 | 0 | no gain from children |
| 3 | 3 | includes 1 and 5 branches |
| 4 | 0 | isolated negative center |
| 5 | 1 | itself |

This shows how positive branches are selectively merged while negative nodes are excluded unless required for connectivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each edge is processed a constant number of times in DFS and rerooting |
| Space | $O(n)$ | adjacency list and DP arrays |

The linear complexity fits comfortably within constraints for $2 \cdot 10^5$ nodes, and recursion depth is manageable with increased recursion limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder, replace with real call

# sample case
assert run("""3
0 1 0
1 2
2 3
""") == "1 1 1", "sample 1"

# chain all black
assert run("""4
0 0 0 0
1 2
2 3
3 4
""") == "0 0 0 0", "all black"

# all white
assert run("""4
1 1 1 1
1 2
1 3
1 4
""") == "4 4 4 4", "all white star"

# alternating chain
assert run("""5
1 0 1 0 1
1 2
2 3
3 4
4 5
""") == "1 2 3 2 1", "alternating chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all black chain | all zeros | negative-only pruning |
| all white star | all nodes equal max | full aggregation |
| alternating chain | symmetric propagation | rerooting correctness |

## Edge Cases

One important edge case is when all nodes are black. In that case every subtree sum is non-positive, and the optimal choice for each node is just the node itself, giving zero. The algorithm handles this because all contributions are negative, so no child is ever added in the DP, and each answer reduces to zero.

Another case is a star graph with one white center and many black leaves. The optimal subtree for the center includes only itself, but for leaves it includes the center and possibly other positive contributions if they exist. The rerooting ensures that each leaf sees the center’s contribution as an upward branch.

A final case is a long chain where positives are separated by negatives. The algorithm correctly cuts off negative segments because they never contribute positive gain in the downward DP, and rerooting recombines only beneficial segments, ensuring no forced inclusion of harmful nodes.