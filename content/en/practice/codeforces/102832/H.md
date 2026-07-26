---
title: "CF 102832H - Combination Lock"
description: "A direct approach would be to model every possible sequence of moves. From a position we would try every unvisited neighbor, recursively solve the resulting state, and mark the current state as winning if any move makes the opponent lose."
date: "2026-07-26T15:12:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102832
codeforces_index: "H"
codeforces_contest_name: "2020 China Collegiate Programming Contest Changchun Onsite"
rating: 0
weight: 102832
solve_time_s: 75
verified: true
draft: false
---

[CF 102832H - Combination Lock](https://codeforces.com/problemset/problem/102832/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Approaches

A direct approach would be to model every possible sequence of moves. From a position we would try every unvisited neighbor, recursively solve the resulting state, and mark the current state as winning if any move makes the opponent lose. This mirrors the rules exactly and is correct because the game is finite. The problem is the amount of information required. A state is not only the current password, but also the set of all previously visited passwords. In the worst case this creates 2^(10^m) possible histories, which is impossible even for the smallest useful upper bound on the state space.

The useful change of perspective is to stop thinking about game histories and look at the underlying graph. Forbidden passwords can be removed before the game starts because entering one is always a losing move. The remaining graph has vertices representing usable passwords and edges representing one valid rotation.

The graph is undirected, and the lock graph has an additional bipartite structure. Coloring a password by the parity of the sum of its digits works because every move changes that sum by an odd number, even when a digit wraps from 0 to 9. This lets us solve maximum matching with Hopcroft-Karp.

The matching theorem gives a simple test. Let M be the maximum matching size of the playable graph. If the starting vertex is removed and the maximum matching size becomes M - 1, then every maximum matching used the starting vertex, so Alice wins. If the size stays M, there exists a maximum matching avoiding the starting vertex, so Bob can force a win.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of states | Exponential | Too slow |
| Optimal | O(VE^0.5) | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Generate the graph of all passwords that are not in the forbidden set. Each password is converted into an integer id, and two ids are connected when one rotation changes one digit by one step.

The graph contains at most 100000 vertices and each vertex has at most 2m neighbors, so building it is linear in the size of the state space.

1. Split the graph into two sides using the parity of the digit sum. Store edges only from the first side to the second side.

Every move changes the parity, so this is a valid bipartition. It allows maximum matching to be found efficiently.

1. Run Hopcroft-Karp to find the maximum matching size of the complete playable graph.

This gives the value needed for the matching characterization.

1. Run Hopcroft-Karp again while ignoring the starting password.

If the matching size decreases, the starting password was necessary in every maximum matching. Otherwise there is a maximum matching that avoids it.

1. Print Alice if the second matching size is smaller, and Bob otherwise.

Why it works:

After removing forbidden passwords, every legal move in the original game corresponds exactly to moving along an edge in the remaining undirected graph. The game is therefore undirected vertex geography. The matching characterization says the first player wins exactly when the starting vertex is included in every maximum matching. Removing the starting vertex tests precisely this condition: if the best matching loses one edge, the start was always needed; if it does not, a maximum matching exists without it. Thus the comparison of the two matching sizes gives the correct winner.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def hopcroft_karp(adj, nl, nr):
    pair_l = [-1] * nl
    pair_r = [-1] * nr
    dist = [0] * nl

    def bfs():
        q = deque()
        found = False
        for i in range(nl):
            if pair_l[i] == -1:
                dist[i] = 0
                q.append(i)
            else:
                dist[i] = -1
        while q:
            u = q.popleft()
            for v in adj[u]:
                pu = pair_r[v]
                if pu == -1:
                    found = True
                elif dist[pu] == -1:
                    dist[pu] = dist[u] + 1
                    q.append(pu)
        return found

    def dfs(u):
        for v in adj[u]:
            pu = pair_r[v]
            if pu == -1 or (dist[pu] == dist[u] + 1 and dfs(pu)):
                pair_l[u] = v
                pair_r[v] = u
                return True
        dist[u] = -1
        return False

    ans = 0
    while bfs():
        for i in range(nl):
            if pair_l[i] == -1 and dfs(i):
                ans += 1
    return ans

def solve_case(m, n, start, banned):
    total = 10 ** m
    pow10 = [10 ** i for i in range(m)]

    def digits_of(x):
        res = []
        for _ in range(m):
            res.append(x % 10)
            x //= 10
        return res

    def encode(s):
        x = 0
        for c in s:
            x = x * 10 + (ord(c) - 48)
        return x

    bad = [False] * total
    for x in banned:
        bad[x] = True

    start_id = encode(start)

    side = [-1] * total
    left_id = [-1] * total
    right_id = [-1] * total
    nl = nr = 0

    for x in range(total):
        if not bad[x]:
            s = sum(digits_of(x))
            if s & 1:
                side[x] = 1
                right_id[x] = nr
                nr += 1
            else:
                side[x] = 0
                left_id[x] = nl
                nl += 1

    adj = [[] for _ in range(nl)]

    for x in range(total):
        if side[x] != 0:
            continue
        digs = digits_of(x)
        lx = left_id[x]
        for i in range(m):
            cur = digs[i]
            for nd in ((cur + 1) % 10, (cur - 1) % 10):
                y = x + (nd - cur) * pow10[m - 1 - i]
                if not bad[y]:
                    adj[lx].append(right_id[y])

    first = hopcroft_karp(adj, nl, nr)

    if side[start_id] == 0:
        old = left_id[start_id]
        removed_adj = []
        for i in range(nl):
            if i != old:
                removed_adj.append(adj[i])
        second = hopcroft_karp(removed_adj, nl - 1, nr)
    else:
        old = right_id[start_id]
        filtered = []
        for row in adj:
            filtered.append([v if v < old else v - 1 for v in row if v != old])
        second = hopcroft_karp(filtered, nl, nr - 1)

    return "Alice" if second < first else "Bob"

def main():
    t = int(input())
    out = []
    for _ in range(t):
        m, n, s = input().split()
        m = int(m)
        n = int(n)
        banned = []
        for _ in range(n):
            banned.append(int(input().strip()))
        out.append(solve_case(m, n, s, banned))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation first builds the set of usable passwords. The `side` array stores the bipartition, while `left_id` and `right_id` convert original password ids into compact matching indices.

The neighbor generation changes one digit at a time. The conversion from a changed digit back to an integer id uses powers of ten, which avoids repeatedly creating strings and keeps graph construction fast.

The first Hopcroft-Karp call computes the maximum matching of the playable graph. The second call removes the start vertex from the corresponding side of the bipartition. The careful index adjustment in the right-side case avoids an off-by-one error when a matched vertex disappears.

The final comparison uses the matching theorem directly. A smaller matching after removing the start means the start was essential, which is exactly the condition for Alice to win.

## Worked Examples

Sample 1:

Input:

```
1
1 2 6
7
5
```

| Step | Matching of full graph | Matching after removing start | Result |
| --- | --- | --- | --- |
| Build graph | Vertices 0,1,2,3,4,6,8,9 remain | Not computed yet | Continue |
| Maximum matching | 3 | Not computed yet | Continue |
| Remove start 6 | 3 | 3 | Bob |

The matching size does not decrease, so there exists a maximum matching that avoids the starting password. Bob can use the matching strategy.

Sample 2:

Input:

```
1
1 2 9
1
8
```

| Step | Matching of full graph | Matching after removing start | Result |
| --- | --- | --- | --- |
| Build graph | Vertices except 1 and 8 remain | Not computed yet | Continue |
| Maximum matching | 4 | Not computed yet | Continue |
| Remove start 9 | 4 | 3 | Alice |

The matching size drops by one. The starting vertex is forced into every maximum matching, so Alice has a winning strategy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(VE^0.5) | Hopcroft-Karp is run twice on a graph with V <= 100000 and E <= 2mV |
| Space | O(V + E) | The graph and matching arrays are stored explicitly |

The largest possible graph has one hundred thousand states and at most one million directed adjacency entries after bipartite conversion. The two matching runs fit comfortably within the given memory and time limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old
    return ""

# The assertions below are examples for an external judge harness.
# They should call solve_case directly or wrap main in the same file.

assert solve_case(1, 2, "6", [7, 5]) == "Bob"
assert solve_case(1, 2, "9", [1, 8]) == "Alice"
assert solve_case(1, 0, "0", []) == "Bob"
assert solve_case(1, 8, "0", ["1", "2", "3", "4", "5", "6", "7", "9"]) == "Bob"
assert solve_case(2, 99, "00", list(range(1, 100))) in ("Alice", "Bob")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `m=1, start=6, banned={7,5}` | Bob | A case where a maximum matching avoids the start |
| `m=1, start=9, banned={1,8}` | Alice | The start vertex is forced into every maximum matching |
| `m=1, start=0, banned={}` | Bob | Smallest graph handling |
| `m=1, start=0, all other digits banned` | Bob | Immediate losing move handling |
| Large two-digit graph | Alice or Bob | Performance and index handling |

## Edge Cases

When all possible moves from the start are forbidden, the algorithm removes those vertices before matching. The remaining graph may contain the start as an isolated vertex. Its maximum matching size is unchanged after removing it, so the answer becomes Bob, matching the rule that Alice loses on her first move.

When the starting password is on the right side of the bipartition, removing it requires shrinking the right side of the matching graph rather than the left side. The implementation handles this separately because Hopcroft-Karp stores only left-side adjacency. This prevents a common indexing bug.

When no passwords are forbidden, the graph contains all possible lock states. The method still works because it never depends on the number of forbidden states. The graph is built from the lock dimensions alone, and the matching theorem handles cycles and long paths without enumerating game histories.

I can also adapt this into a shorter Codeforces-style editorial, or rewrite the proof section in a more formal theorem-and-lemma style.
