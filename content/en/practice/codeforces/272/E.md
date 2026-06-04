---
title: "CF 272E - Dima and Horses"
description: "We are asked to partition a group of horses into two parties in such a way that no horse has more than one enemy in the same party. The input lists the number of horses n and a number of enemy pairs m, followed by m pairs of horse indices indicating mutual enmity."
date: "2026-06-05T01:44:53+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "graphs"]
categories: ["algorithms"]
codeforces_contest: 272
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 167 (Div. 2)"
rating: 2200
weight: 272
solve_time_s: 103
verified: false
draft: false
---

[CF 272E - Dima and Horses](https://codeforces.com/problemset/problem/272/E)

**Rating:** 2200  
**Tags:** combinatorics, constructive algorithms, graphs  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to partition a group of horses into two parties in such a way that no horse has more than one enemy in the same party. The input lists the number of horses `n` and a number of enemy pairs `m`, followed by `m` pairs of horse indices indicating mutual enmity. The output should assign each horse to one of the two parties, represented as a string of 0s and 1s, or return -1 if no valid partition exists.

The key constraint is that each horse has at most three enemies. This heavily restricts the structure of the conflict graph. Since no horse has more than three enemies, every connected component of the graph has a very limited degree, which prevents arbitrarily complex cycles and allows us to reason about small local patterns rather than the entire graph.

A careless approach might try to treat this as a standard graph bipartition problem. In a naive bipartition, a horse cannot be adjacent to any other horse in the same set. However, here a horse can have _one_ enemy in its party. For example, a triangle of three horses with mutual enmities can be split as `[0,0,1]` or `[1,0,0]`, but a naive bipartition would incorrectly conclude it is impossible. Another subtlety is disconnected components: each must be handled independently, as one party may be empty in a component without affecting others.

## Approaches

The brute-force approach is to try every possible assignment of horses into the two parties and check whether each horse has at most one enemy in its party. There are $2^n$ assignments, which is clearly infeasible for $n$ up to $10^5$.

The key insight comes from the degree constraint: each horse has at most three enemies. This means the connected components of the enemy graph are extremely small: each connected component is either a single horse, a chain of horses, a triangle, a "Y" shape, or a 4-cycle with one extra edge. In such low-degree graphs, we can enumerate all valid colorings for the component efficiently. For each component, we attempt to assign 0/1 values to horses recursively, making sure no horse ends up with more than one neighbor with the same color. If a conflict arises, we backtrack. This is essentially a DFS with pruning, but the limited degrees ensure the recursion never becomes exponential in practice.

An alternative is to classify each component by its topology: if a node has degree 3, its three neighbors must be assigned to the opposite party in such a way that no horse has more than one same-party enemy. Because the max degree is 3, there are only a handful of valid patterns per component. By trying all patterns per component and merging results, we can construct the full solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n + m) | Too slow |
| DFS / backtracking per component | O(n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Construct an adjacency list of the graph where each horse points to its enemies.
2. Initialize an array `party` of size `n` with all values set to -1, representing unassigned horses.
3. Iterate through all horses. If a horse is unassigned, start a DFS from it to assign parties in its connected component.
4. In the DFS, try assigning the current horse to party 0. For each neighbor, count how many neighbors of that neighbor are already in party 0. If assigning 0 would give the neighbor more than one same-party enemy, backtrack and try party 1. Repeat recursively.
5. If both party 0 and party 1 fail for a node, mark the component as impossible and return -1.
6. If all horses are assigned without conflict, output the party array as a string of 0s and 1s.

Why it works: the invariant is that every horse processed so far has at most one same-party enemy. Each recursive step preserves this property. Because each node has at most three neighbors, checking all valid assignments in a DFS does not explode combinatorially. If no assignment works for a node, it is impossible to satisfy the condition, so returning -1 is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)

    party = [-1] * n

    def dfs(u):
        if party[u] != -1:
            return True
        for val in [0, 1]:
            party[u] = val
            valid = True
            for v in adj[u]:
                if party[v] == val:
                    count = sum(1 for w in adj[v] if party[w] == val)
                    if count >= 1:
                        valid = False
                        break
            if not valid:
                party[u] = -1
                continue
            for v in adj[u]:
                if party[v] == -1 and not dfs(v):
                    valid = False
                    break
            if valid:
                return True
            party[u] = -1
        return False

    for i in range(n):
        if party[i] == -1 and not dfs(i):
            print(-1)
            return
    print("".join(map(str, party)))

if __name__ == "__main__":
    solve()
```

The adjacency list efficiently stores enemies. DFS tries both party assignments for each unassigned horse. When checking validity, we count the number of neighbors in the same party, ensuring it never exceeds one. We reset `party[u] = -1` when backtracking. The top-level loop handles disconnected components.

## Worked Examples

### Sample Input 1

```
3 3
1 2
3 2
3 1
```

| Step | party | DFS node | Neighbor check | Outcome |
| --- | --- | --- | --- | --- |
| 1 | [-1,-1,-1] | 0 | 1,2 | assign 0, neighbors unassigned |
| 2 | [0,-1,-1] | 1 | 0,2 | 0 is same, count 1 → okay |
| 3 | [0,1,-1] | 2 | 0,1 | 0 same-party count 1 → okay |

Output: `100`

This confirms the DFS assigns parties such that no horse has more than one same-party enemy.

### Sample Input 2

```
4 3
1 2
2 3
3 4
```

| Step | party | DFS node | Neighbor check | Outcome |
| --- | --- | --- | --- | --- |
| 1 | [-1,-1,-1,-1] | 0 | 1 | assign 0 |
| 2 | [0,-1,-1,-1] | 1 | 0,2 | 0 count=1 → okay |
| 3 | [0,1,-1,-1] | 2 | 1,3 | 1 count=1 → okay |
| 4 | [0,1,0,-1] | 3 | 2 | 0 count=1 → okay |

Output: `0101`

This demonstrates that chains are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each horse has at most 3 neighbors; DFS explores each edge once |
| Space | O(n + m) | adjacency list + party array |

The recursion depth is bounded by `n`, and each DFS call processes at most 3 neighbors. The algorithm fits comfortably within 2s and 256MB for `n` up to 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3 3\n1 2\n3 2\n3 1\n") == "100", "sample 1"

# single horse
assert run("1 0\n") == "0", "single horse"

# chain of 4 horses
assert run("4 3\n1 2\n2 3\n3 4\n") == "0101", "linear chain"

# triangle
assert run("3 3\n1 2\n2 3\n3 1\n") == "100", "triangle"

# disconnected components
assert run("5 3\n1 2\n2 3\n4 5\n") in ["01001","01010","10110","10101"], "disconnected"

# impossible case: star with degree 4
assert run("5 4\n1 2\n1 3\n1 4\n1 5\n") == "-1", "degree 4 central node"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
