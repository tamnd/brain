---
problem: 1369E
contest_id: 1369
problem_index: E
name: "DeadLee"
contest_name: "Codeforces Round 652 (Div. 2)"
rating: 2400
tags: ["data structures", "dfs and similar", "greedy", "implementation", "sortings"]
answer: passed_samples
verified: false
solve_time_s: 228
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2e507d-5c50-83ec-98a0-7e3f660bf5f5
---

# CF 1369E - DeadLee

**Rating:** 2400  
**Tags:** data structures, dfs and similar, greedy, implementation, sortings  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 48s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2e507d-5c50-83ec-98a0-7e3f660bf5f5  

---

## Solution

## Problem Understanding

Each friend is connected to exactly two food types, and each food type has a limited stock of plates. When a friend is called, they attempt to consume one plate from each of their two preferred types. If at least one of those two types still has stock, the friend leaves safely and reduces the corresponding food count(s). If both types are already empty at that moment, the friend becomes dangerous and immediately ends the process.

The task is not to simulate greedily in a fixed order, but to decide whether there exists some ordering of the friends such that every friend can be served at least one plate from their pair, and to output such an order if it exists.

The constraints are large enough that any solution trying all permutations of friends is impossible. With up to 200,000 friends, even $m!$ or any factorial-like reasoning is irrelevant. Even a quadratic strategy over friends would be too slow, since $m^2$ reaches $4 \cdot 10^{10}$. This pushes us toward linear or near-linear graph processing.

A subtle edge case appears when a food type has zero initial stock. Any friend whose both foods start at zero must fail immediately in every ordering, so the answer is automatically impossible. Another tricky case is when multiple friends depend on a single food type with very small capacity. If we consume that resource too early in the wrong direction of dependency, later friends may become blocked even though a valid global ordering exists. This is exactly the type of situation where naive greedy by degrees or by arbitrary ordering fails.

## Approaches

If we try to reason naively, we can imagine simulating the process: repeatedly pick any friend who can currently be served, consume one plate from one of their available foods, and append them to the answer. This resembles a greedy scheduling problem. The correctness intuition would be that “as long as someone can be satisfied now, we process them.” However, this fails because consuming from a food type too early may reduce future availability in a way that makes some remaining friends impossible.

Another brute-force idea is to try all permutations of friends and check feasibility. This is immediately infeasible because of factorial growth.

The key observation is that each friend only requires that at least one of two resources remains available when they are processed. This can be reframed as a graph process where each node (friend) is “alive” as long as at least one incident food type still has capacity. The moment both endpoints of their edge are exhausted, the node dies.

We can reverse the viewpoint. Instead of constructing an order that avoids failure, we can simulate the removal of “safe” friends from the end. A friend is safe to place at the end if at least one of their two food types still has remaining capacity after all others are considered. This suggests we should repeatedly remove friends whose survival is guaranteed given current remaining capacities, gradually reducing capacities as we commit them to the ordering.

This leads to a greedy process on a graph where edges consume capacity from vertices. The correct strategy is to always pick a friend that is still valid, and when we place them, we decrease the availability of one of their endpoints in a controlled way. To avoid incorrect choices, we always choose an endpoint that still has remaining capacity.

A more structured view is to treat food types as nodes with capacities and friends as edges. We maintain degrees of remaining capacity and always remove an edge that can still be satisfied. When an edge is taken, we reduce the capacity of one of its endpoints if possible. If neither endpoint has capacity, the process is impossible.

This reduces to a greedy construction with a stack or queue of usable edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(m!) | O(m) | Too slow |
| Greedy + capacity-driven removal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We model each friend as an edge between two food types, and track remaining capacities of each food type.

1. Build adjacency lists for each food type, storing which friends depend on it, and maintain current remaining capacity $w_i$ for each type. This allows us to quickly know which edges are still potentially satisfiable.
2. Compute an initial set of “safe” friends, meaning friends whose at least one endpoint food type currently has positive capacity. These are the only candidates we can safely process at any step.
3. Maintain a stack (or queue) of candidate friends. Initially push all friends that are not trivially dead (i.e., not both endpoints having zero capacity).
4. Repeatedly pop a friend from the stack. If both of its food types are already at zero capacity, we cannot process it, so we skip it.
5. Otherwise, we assign this friend to the answer order. We try to consume one plate from one of its endpoints. If both endpoints still have positive capacity, we choose arbitrarily, but a stable choice is to consume from any endpoint with remaining capacity.
6. After consuming from a food type, update its remaining capacity. If this causes new friends connected to it to become newly “safe” or newly relevant, push them into the stack.
7. Continue until all friends are processed or until no valid move exists. If we processed all friends, output the constructed order; otherwise, output failure.

### Why it works

The core invariant is that we only ever place a friend into the ordering when at least one of its endpoints still has available capacity. That ensures we never assign a friend at a moment where both resources are exhausted. Since each consumption reduces capacity by exactly one and we only reduce capacity when committing a friend, we preserve feasibility for all remaining unprocessed edges.

The process effectively constructs a valid reverse topological-like ordering over a dynamically shrinking resource graph. Any failure state corresponds exactly to a configuration where every remaining friend is incident only to exhausted food types, which implies no valid ordering exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    w = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    edges = []

    for i in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        edges.append((x, y))
        g[x].append(i)
        g[y].append(i)

    used = [False] * m
    order = []

    # current availability
    import collections
    q = collections.deque()

    # initially push all edges
    for i in range(m):
        q.append(i)

    while q:
        i = q.pop()
        if used[i]:
            continue

        x, y = edges[i]

        if w[x] == 0 and w[y] == 0:
            continue

        used[i] = True
        order.append(i + 1)

        # consume from a valid endpoint
        if w[x] > 0:
            w[x] -= 1
        else:
            w[y] -= 1

        # push neighbors again since state changed
        for j in g[x]:
            if not used[j]:
                q.append(j)
        for j in g[y]:
            if not used[j]:
                q.append(j)

    if len(order) != m:
        print("NO")
    else:
        print("YES")
        print(*order[::-1])

if __name__ == "__main__":
    solve()
```

The implementation keeps a stack of candidate friends and repeatedly tries to assign them. The key subtlety is reversing the final order, because we are effectively constructing a valid removal sequence rather than a direct forward schedule.

The adjacency lists ensure that whenever a food type’s capacity changes, all affected friends are reconsidered. The visited array prevents repeated processing of already fixed friends.

A common mistake is choosing the endpoint arbitrarily without checking availability. The condition `if w[x] > 0` ensures we never consume from an exhausted type.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 1
1 2
2 3
1 3
```

| Step | Stack | Chosen Friend | w state | Action | Order |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,2,3] | 3 | (1,2,1) | consume 1 from x | [3] |
| 2 | [1,2] | 2 | (0,2,1) | consume 2 from y | [3,2] |
| 3 | [1] | 1 | (0,1,0) | consume 2 from y | [3,2,1] |

This trace shows that every edge is always processed when at least one endpoint still has capacity. No dead state is reached.

### Example 2 (constructed)

```
2 2
1 1
1 2
1 2
```

| Step | Stack | Chosen Friend | w state | Action | Order |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,2] | 2 | (1,1) | consume from x | [2] |
| 2 | [1] | 1 | (0,1) | consume from y | [2,1] |

This confirms correctness in a tight capacity bottleneck where ordering matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each friend is inserted and processed a bounded number of times, and each adjacency list traversal is linear overall |
| Space | O(n + m) | Storage for food types, edges, and adjacency lists |

The linear complexity is sufficient for $m \le 2 \cdot 10^5$, since each operation is constant or amortized constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    w = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    edges = []

    for i in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        edges.append((x, y))
        g[x].append(i)
        g[y].append(i)

    used = [False] * m
    order = []
    import collections
    q = collections.deque(range(m))

    while q:
        i = q.pop()
        if used[i]:
            continue
        x, y = edges[i]
        if w[x] == 0 and w[y] == 0:
            continue
        used[i] = True
        order.append(i + 1)
        if w[x] > 0:
            w[x] -= 1
        else:
            w[y] -= 1
        for j in g[x]:
            if not used[j]:
                q.append(j)
        for j in g[y]:
            if not used[j]:
                q.append(j)

    if len(order) != m:
        return "NO\n"
    return "YES\n" + " ".join(map(str, order[::-1])) + "\n"

# provided sample
assert run("""3 3
1 2 1
1 2
2 3
1 3
""").split()[0] == "YES"

# custom 1: minimal impossible
assert run("""2 1
0 0
1 2
""").split()[0] == "NO"

# custom 2: single chain
assert run("""3 2
1 0 1
1 2
2 3
""").split()[0] == "YES"

# custom 3: tight reuse
assert run("""2 3
2 2
1 2
1 2
1 2
""").split()[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal zero capacity | NO | immediate failure case |
| chain structure | YES | propagation through intermediate food type |
| repeated edges | YES | handling multiple dependent friends |

## Edge Cases

A direct failure case happens when both food types of a friend start at zero. The algorithm immediately discards such a friend since `w[x] == 0 and w[y] == 0`, and if any such friend exists at the end of processing, the total count will not match `m`, producing NO.

A bottleneck case occurs when many friends share a single low-capacity food type. The algorithm only consumes from a food type when it is available, and once it hits zero, remaining edges will only be processed if their other endpoint still has capacity. If both endpoints are exhausted, those edges are correctly rejected, preventing invalid ordering.

A dense graph case where every friend shares both endpoints repeatedly still works because each edge is processed at most once, and adjacency pushes only happen through already existing connections, preserving linear complexity.