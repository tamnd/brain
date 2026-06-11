---
title: "CF 1167C - News Distribution"
description: "We are given a social network with n users and m groups of friends. Each group contains a list of users who are mutually friends with each other."
date: "2026-06-12T02:11:02+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 1400
weight: 1167
solve_time_s: 198
verified: true
draft: false
---

[CF 1167C - News Distribution](https://codeforces.com/problemset/problem/1167/C)

**Rating:** 1400  
**Tags:** dfs and similar, dsu, graphs  
**Solve time:** 3m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a social network with `n` users and `m` groups of friends. Each group contains a list of users who are mutually friends with each other. Friendship is transitive through these groups: if two users are in the same group, they are friends, and the news spreads through chains of friendship. For each user, we are asked to compute how many users would eventually know a piece of news if that user were the only initial source.

Conceptually, this is a graph problem. Each user is a node, and there is an edge between two users if they belong to the same group. The news spreads along connected components of this graph. Therefore, the number of users who eventually know the news starting from user `x` is equal to the size of the connected component that contains `x`.

The constraints are high: `n` and `m` can go up to `5 * 10^5`, and the total number of group memberships is also up to `5 * 10^5`. Any solution that explicitly computes neighbors for each user and runs a BFS or DFS from every node will be too slow, because it could require `O(n*(n+m))` operations in the worst case. This forces us to find an approach that avoids repeated traversals of the same component.

Non-obvious edge cases include empty groups and single-user groups. A group with `0` users should be ignored since it connects no one. A group with one user does not increase connectivity but must not break the union logic. For instance, an input where all groups are empty would produce an output of `1` for each user, since each user forms a singleton component.

## Approaches

The naive approach is to build an adjacency list of all users, then run BFS or DFS from every user to count the size of the connected component. This is correct but inefficient. For `n = 5*10^5`, running BFS `n` times is prohibitively slow, because the cumulative operations could exceed `10^{11}` in the worst case.

The key insight is that connectivity is symmetric and transitive. Users in the same connected component will always share the same final answer. This suggests that we only need to compute the size of each connected component once. A natural structure for this is Disjoint Set Union (DSU), also called Union-Find. We can iterate through each group and merge all its members into one set. After processing all groups, each set represents a connected component, and the size of each set gives the answer for all its members. This reduces the time complexity to near-linear in the total number of group memberships.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS/DFS from every user | O(n*(n+m)) | O(n+m) | Too slow |
| DSU / Union-Find on groups | O(n + m + total group size * α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a DSU with `n` elements, where each user initially belongs to their own set. Each set tracks its size.
2. Iterate through each group. For a group of size `k`, merge all `k` users into one set. We can do this by sequentially merging the first user with each of the remaining users.
3. After all groups are processed, each connected component has been merged into one set, and the size of the set represents the number of users reachable from any member.
4. For each user from `1` to `n`, output the size of the set they belong to. This is the number of users who will know the news if that user starts distributing it.

Why it works: The union-find structure ensures that all users that can reach each other through any sequence of groups are merged into a single set. By keeping track of set sizes, we know exactly how many users each initial user can reach. Path compression guarantees that `find` operations are fast, giving near-linear overall complexity.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if self.size[x_root] < self.size[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        self.size[x_root] += self.size[y_root]

n, m = map(int, input().split())
dsu = DSU(n)

for _ in range(m):
    line = list(map(int, input().split()))
    k = line[0]
    if k == 0:
        continue
    users = [x-1 for x in line[1:]]
    first = users[0]
    for u in users[1:]:
        dsu.union(first, u)

result = [dsu.size[dsu.find(i)] for i in range(n)]
print(*result)
```

The code defines a standard DSU with path compression. For each group, it converts user IDs to 0-based indices and unions all members of the group. After all unions, the size of the set containing each user is printed. Using path compression ensures that repeated `find` calls are fast even for large inputs.

## Worked Examples

**Sample Input 1**

```
7 5
3 2 5 4
0
2 1 2
1 1
2 6 7
```

| Step | Group processed | DSU state (parent) | Component sizes |
| --- | --- | --- | --- |
| initial | - | 0 1 2 3 4 5 6 | 1 1 1 1 1 1 1 |
| group1 2,5,4 | merge(2,5), merge(2,4) | 0 1 2 2 2 2 6 | 1 1 3 3 3 3 1 |
| group2 empty | - | unchanged | unchanged |
| group3 1,2 | merge(1,2) | 0 2 2 2 2 2 6 | 4 4 4 4 3 3 1 |
| group4 1 | single | unchanged | unchanged |
| group5 6,7 | merge(5,6) | 0 2 2 2 2 5 5 | 4 4 4 4 4 2 2 |

Output: `4 4 1 4 4 2 2`

The trace confirms that each user belongs to a connected component of correct size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + total group size * α(n)) | Each union and find is nearly constant; we process each group member once |
| Space | O(n) | DSU parent and size arrays store one integer per user |

With `n, m` up to `5*10^5` and total group size up to `5*10^5`, the algorithm easily fits within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1]*n
        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        def union(self, x, y):
            x_root = self.find(x)
            y_root = self.find(y)
            if x_root == y_root: return
            if self.size[x_root] < self.size[y_root]:
                x_root, y_root = y_root, x_root
            self.parent[y_root] = x_root
            self.size[x_root] += self.size[y_root]

    n, m = map(int, input().split())
    dsu = DSU(n)
    for _ in range(m):
        line = list(map(int, input().split()))
        k = line[0]
        if k == 0: continue
        users = [x-1 for x in line[1:]]
        first = users[0]
        for u in users[1:]:
            dsu.union(first, u)

    return ' '.join(str(dsu.size[dsu.find(i)]) for i in range(n))

# Provided sample
assert run("7 5\n3 2 5 4\n0\n2 1 2\n1 1\n2 6 7\n") == "4 4 1 4 4 2 2", "sample 1"

# Custom cases
assert run("5 0\n0\n0\n0\n0\n0\n") == "1 1 1 1 1", "all empty groups"
assert run("3 3\n1 1\n1 2\n1 3\n") == "1 1 1", "singletons"
assert run("4 2\n2 1 2\n2 3
```
