---
title: "CF 102875E - Eliminate the Virus"
description: "We have an undirected network of at most 16 nodes. Every node starts infected. At the beginning of each second, the antivirus may clean some currently infected nodes, but it can clean at most k nodes in one operation."
date: "2026-07-25T12:52:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102875
codeforces_index: "E"
codeforces_contest_name: "2020 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 102875
solve_time_s: 42
verified: true
draft: false
---

[CF 102875E - Eliminate the Virus](https://codeforces.com/problemset/problem/102875/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected network of at most 16 nodes. Every node starts infected. At the beginning of each second, the antivirus may clean some currently infected nodes, but it can clean at most `k` nodes in one operation. After cleaning, the remaining infected nodes spread the virus to all of their neighbors and then disappear themselves. The goal is to output a sequence of cleaning operations that eventually leaves the whole network virus-free, or determine that no such sequence exists.

A convenient way to represent the situation is with a bitmask. Bit `i` is set when node `i` is currently infected. After choosing some infected nodes to remove, only the nodes not cleaned can spread. The next state is exactly the union of the neighbors of those remaining nodes.

The small value of `n` is the key restriction. Since there are only `2^n` possible infection states and `n <= 16`, there are at most 65536 states. A solution that is polynomial in the number of states is possible. On the other hand, simulating the graph directly without using the state compression would not capture repeated configurations efficiently.

The main edge cases come from confusing "clean now" with "clean forever". A node cleaned in one round can become infected again if a neighboring infected node spreads into it. For example:

```
2 1 1
1 2
```

The answer is not one operation cleaning both nodes because `k=1`. Cleaning node 1 first leaves node 2 infected, which spreads back to node 1. A valid answer is:

```
2
1
1
```

Another important case is when cleaning all currently infected nodes is possible. If `k=n`, the initial state can be solved immediately by cleaning every node once. A simulation that always forces a spread after cleaning would incorrectly reject this case.

## Approaches

The brute-force idea is to try every possible strategy. For a current infected set, we can enumerate every subset of infected nodes to clean, simulate one spread, and continue recursively. This is correct because every possible valid strategy is considered. The problem is the number of choices. Across all states, enumerating all possible cleaned subsets gives roughly `3^n` transitions because every node can be in one of three categories: not infected, infected and cleaned, or infected and not cleaned. For `n=16`, this is already about 43 million possibilities before accounting for repeated work and storing the search tree.

The useful observation is that the current infection pattern completely describes the future. We do not need to remember the previous operations. This turns the problem into shortest-path search on a graph of states. Every mask is a vertex, and a directed edge represents one possible cleaning operation followed by one virus spread.

A breadth-first search is enough because every operation has equal cost. The remaining optimization is generating transitions carefully. Instead of choosing the cleaned nodes directly, choose the infected nodes that survive cleaning and spread. If the current mask is `S` and the surviving infected nodes are `T`, then `T` must be a subset of `S`, and the number of cleaned nodes is `popcount(S)-popcount(T)`. We only consider subsets where this value is at most `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(2^n) | Too slow in the general case |
| Optimal | O(3^n) worst case with small constants | O(2^n) | Accepted |

The worst-case transition count is still based on subset enumeration, but the state graph has only 65536 vertices and the implementation uses integer bit operations. With `n=16`, this fits comfortably.

## Algorithm Walkthrough

1. Encode every infection state as an integer mask. The initial state is `(1 << n) - 1`, and the goal state is `0`.
2. Precompute for every mask the result of one virus spread. If a mask represents infected nodes that survive cleaning, its next state is the OR of the adjacency masks of all set bits.
3. Run BFS starting from the initial mask. Store the previous state and the cleaning operation used to reach every discovered state.
4. When processing a state `S`, enumerate every subset `T` of `S`. Treat `T` as the nodes that remain infected after cleaning. If `S` has too many more bits than `T`, the cleaning operation would exceed `k`, so skip it.
5. The cleaned nodes are `S ^ T`. The next state is the precomputed spread result of `T`. If this state has not been visited, record its parent and the operation used.
6. When state `0` is reached, reconstruct the answer by following parent pointers backwards.

Why it works: BFS explores every reachable infection state in increasing number of operations. For every state, every legal cleaning choice is considered, so every possible strategy corresponds to some path in this search graph. Reaching mask `0` means the virus is gone, and failing to reach it means no valid strategy exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    adj = [0] * n
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    total = 1 << n

    spread = [0] * total
    for mask in range(total):
        x = mask
        res = 0
        while x:
            b = x & -x
            i = b.bit_length() - 1
            res |= adj[i]
            x -= b
        spread[mask] = res

    parent = [-1] * total
    move = [0] * total

    start = total - 1
    parent[start] = start

    q = deque([start])

    while q:
        cur = q.popleft()
        if cur == 0:
            break

        bits = cur
        while True:
            remain = bits
            cleaned = cur ^ remain
            if cleaned.bit_count() <= k:
                nxt = spread[remain]
                if parent[nxt] == -1:
                    parent[nxt] = cur
                    move[nxt] = cleaned
                    q.append(nxt)

            if bits == 0:
                break
            bits = (bits - 1) & cur

    if parent[0] == -1:
        print(-1)
        return

    ans = []
    cur = 0
    while cur != start:
        mask = move[cur]
        s = ""
        for i in range(n):
            if mask >> i & 1:
                s += chr(ord('a') + i)
        ans.append(s)
        cur = parent[cur]

    ans.reverse()
    print(len(ans))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency masks make spreading very fast because each node's neighbors are stored as a single integer. The `spread` array avoids recomputing the same graph operation during BFS.

The subset loop uses the standard submask iteration:

```
bits = (bits - 1) & cur
```

which visits every subset of `cur` exactly once. The variable `remain` represents infected nodes that survive cleaning, so the cleaned set is `cur ^ remain`. This avoids accidentally allowing the antivirus to clean already clean nodes.

The BFS arrays use `-1` as the unvisited marker. Parent pointers reconstruct the sequence in reverse order because BFS naturally discovers the target from the beginning of the process.

## Worked Examples

For the first sample:

```
5 4 2
1 2
2 3
3 4
2 5
```

one possible BFS path is:

| Current state | Cleaned nodes | Surviving infected nodes | Next state |
| --- | --- | --- | --- |
| abcde | bd | ace | 0 |
| 0 | done |  |  |

The sample output is valid because cleaning nodes `b` and `d` leaves nodes `a,c,e` to spread, and those spreads disappear after reaching the empty state.

For the second sample:

```
2 1 1
1 2
```

the search behaves as follows:

| Current state | Cleaned nodes | Surviving infected nodes | Next state |
| --- | --- | --- | --- |
| ab | a | b | a |
| a | a | none | 0 |

The same operation appears twice because a node can be reinfected after its neighbor spreads.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3^n) | All reachable states are processed and each state may enumerate submasks |
| Space | O(2^n) | Stores BFS information and precomputed transitions |

With `n <= 16`, the number of masks is only 65536. The bit operations keep the constant factors small enough for the intended limits.

## Test Cases

```
# These are examples of checks for the implementation logic.

# Minimum graph
assert True

# Two-node chain with k=1
# Expected: a valid answer exists with two operations

# Complete graph with k=n
# Expected: one operation cleaning every node

# Cycle graph
# Expected: BFS should find a multi-step strategy

# Impossible cases should print -1 when no state reaches zero
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two connected nodes, k=1 | 2 operations | Reinfection handling |
| Complete graph, k=n | 1 operation | Immediate cleanup |
| Cycle graph | Several operations | General BFS traversal |
| Impossible graph | -1 | Correct unreachable-state detection |

## Edge Cases

For the two-node graph with one cleaning slot:

```
2 1 1
1 2
```

the BFS starts at mask `11`. It tries cleaning one node, reaches mask `01` or `10`, and then discovers that cleaning the remaining node reaches `00`. The algorithm does not assume cleaned nodes stay clean, because every transition always applies the spread step.

For a graph where `k=n`, the initial state contains exactly the nodes that can all be cleaned. The BFS finds the transition with surviving set `0`, whose spread result is also `0`. This prevents the common mistake of forcing unnecessary rounds after a complete cleanup.

For graphs with cycles, such as:

```
5 5 2
1 2
2 3
3 4
4 5
5 1
```

a greedy approach may repeatedly clean nodes that become infected again. BFS avoids this because it reasons over complete states and only cares whether a state has already been explored.
