---
title: "CF 300B - Coach"
description: "We can think of the students as vertices of an undirected graph. Every friendship relation means two students must belong to the same team. Since each team has exactly three students, every connected component of this graph must fit entirely inside one team."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 300
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 181 (Div. 2)"
rating: 1500
weight: 300
solve_time_s: 138
verified: true
draft: false
---

[CF 300B - Coach](https://codeforces.com/problemset/problem/300/B)

**Rating:** 1500  
**Tags:** brute force, dfs and similar, graphs  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We can think of the students as vertices of an undirected graph. Every friendship relation means two students must belong to the same team. Since each team has exactly three students, every connected component of this graph must fit entirely inside one team.

The task is to partition all students into groups of size three while respecting every required pairing. If this is impossible, we print `-1`.

The key observation is that friendship constraints are transitive. If student `1` must stay with `2`, and `2` must stay with `3`, then all three must be placed together. In graph terms, every connected component must appear inside one team.

The constraints are tiny. `n ≤ 48`, so even cubic or quartic algorithms are completely safe. The challenge is not performance, it is handling all corner cases correctly.

The dangerous situations come from connected components with awkward sizes.

Consider this input:

```
6 3
1 2
2 3
3 4
```

Students `1,2,3,4` form one connected component of size four. Since teams must contain exactly three students, there is no way to split this component without breaking a friendship requirement. The correct answer is:

```
-1
```

A careless solution that only checks direct edges might incorrectly output:

```
1 2 3
4 5 6
```

which separates `4` from the rest of its component.

Another subtle case happens when there are too many pairs but not enough isolated students to complete them.

```
6 2
1 2
3 4
```

We have two components of size two. Each pair needs one extra student to form a team of three. Students `5` and `6` can complete them:

```
1 2 5
3 4 6
```

Now look at:

```
6 3
1 2
3 4
5 6
```

All components have size two, but there are no isolated students available to complete the teams. The correct output is `-1`.

One more edge case is a component already of size three:

```
6 2
1 2
2 3
```

The first team is forced to be `{1,2,3}`. The remaining students become the second team automatically.

A buggy implementation might try to merge this component with extra vertices and accidentally create a team of size four.

## Approaches

A brute force approach would try every possible partition of students into groups of three and verify whether every friendship edge stays inside a team.

The number of ways to partition `n` elements into triples grows extremely fast. Even for `n = 48`, the count is astronomically large:

$$\frac{48!}{(3!)^{16} \cdot 16!}$$

This is far beyond anything computable.

The brute force is conceptually correct because the problem only asks for any valid partition, but it fails because the search space explodes.

The graph structure gives a much better direction. Friendship constraints force vertices into connected components. Once we compute these components, each one behaves like a block that cannot be split.

Now the problem becomes much simpler.

A component of size:

- `1` is flexible and can join any team.
- `2` needs exactly one isolated student.
- `3` already forms a complete team.
- `4` or more makes the answer impossible immediately.

This completely removes combinatorial explosion. We only need DFS or BFS to build connected components, then some greedy assembly of teams.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an undirected graph from the friendship relations.

Each student is a vertex, and every constraint edge connects two students that must stay together.
2. Run DFS or BFS to find all connected components.

Every connected component represents a set of students that must belong to the same team.
3. If any connected component has more than three vertices, print `-1`.

A team can contain only three students, so such a component can never fit.
4. Separate the components by size.

Components of size three are already complete teams.

Components of size two need one isolated student later.

Components of size one are stored as free students.
5. For every size-two component, attach one isolated student.

If we ever run out of isolated students, print `-1`.
6. Group the remaining isolated students into triples.

If the number of leftover isolated students is not divisible by three, print `-1`.
7. Output all constructed teams.

### Why it works

The invariant is that every connected component must remain entirely inside one team.

DFS finds exactly those maximal groups of mutually connected students. Since no friendship edge crosses components, we are free to combine different components together as long as the final team size is three.

A component of size three already occupies a full team and cannot accept extra students. A component of size two requires exactly one additional student. A component of size one is completely flexible.

The algorithm never separates vertices from the same component, so every friendship constraint is preserved. It also guarantees every team has exactly three students. If the algorithm declares failure, then some component size or student count makes a valid partition mathematically impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * (n + 1)
    components = []

    def dfs(start):
        stack = [start]
        visited[start] = True
        comp = []

        while stack:
            node = stack.pop()
            comp.append(node)

            for nei in graph[node]:
                if not visited[nei]:
                    visited[nei] = True
                    stack.append(nei)

        return comp

    for i in range(1, n + 1):
        if not visited[i]:
            comp = dfs(i)

            if len(comp) > 3:
                print(-1)
                return

            components.append(comp)

    singles = []
    answer = []

    for comp in components:
        if len(comp) == 3:
            answer.append(comp)
        elif len(comp) == 2:
            answer.append(comp)
        else:
            singles.append(comp[0])

    ptr = 0

    for team in answer:
        if len(team) == 2:
            if ptr >= len(singles):
                print(-1)
                return

            team.append(singles[ptr])
            ptr += 1

    remaining = singles[ptr:]

    if len(remaining) % 3 != 0:
        print(-1)
        return

    for i in range(0, len(remaining), 3):
        answer.append(remaining[i:i + 3])

    for team in answer:
        print(*team)

solve()
```

The first section builds the adjacency list for the graph. Since the graph is undirected, every edge is inserted in both directions.

The DFS collects one connected component at a time. Iterative DFS avoids recursion depth concerns, although recursion would also work here because `n` is tiny.

The moment a component larger than three is discovered, the program exits immediately with `-1`. There is no need to continue because such a component can never fit into one team.

After component discovery, the code separates students into three categories. Components of size three are already valid teams. Components of size two are temporarily incomplete teams waiting for one isolated student. Components of size one are stored in `singles`.

The pointer `ptr` tracks how many isolated students have already been consumed. This avoids repeatedly removing elements from the front of the list, which would be inefficient in larger constraints.

The final grouping step processes leftover isolated students in chunks of three. If the count is not divisible by three, then some students cannot be assigned.

One subtle implementation detail is that size-two components are added to `answer` immediately, then completed later. This avoids managing multiple separate collections.

## Worked Examples

### Example 1

Input:

```
3 0
```

There are no friendship constraints.

| Step | Components | Singles | Answer |
| --- | --- | --- | --- |
| DFS from 1 | [1] | [1] | [] |
| DFS from 2 | [2] | [1,2] | [] |
| DFS from 3 | [3] | [1,2,3] | [] |
| Build triples | - | [] | [[1,2,3]] |

Output:

```
1 2 3
```

This example shows the completely unconstrained case. Every student is isolated, so we can group them arbitrarily.

### Example 2

Input:

```
9 3
1 2
3 4
4 5
```

| Step | Components Found | Singles | Partial Teams |
| --- | --- | --- | --- |
| DFS from 1 | [1,2] | [] | [[1,2]] |
| DFS from 3 | [3,4,5] | [] | [[1,2],[3,4,5]] |
| DFS from 6 | [6] | [6] | [[1,2],[3,4,5]] |
| DFS from 7 | [7] | [6,7] | [[1,2],[3,4,5]] |
| DFS from 8 | [8] | [6,7,8] | [[1,2],[3,4,5]] |
| DFS from 9 | [9] | [6,7,8,9] | [[1,2],[3,4,5]] |
| Complete pair | - | [7,8,9] | [[1,2,6],[3,4,5]] |
| Final triples | - | [] | [[1,2,6],[3,4,5],[7,8,9]] |

Possible output:

```
1 2 6
3 4 5
7 8 9
```

This trace demonstrates all three component types at once. One component already forms a complete team, one pair consumes a singleton, and the remaining isolated students form their own team.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS visits every vertex and edge once |
| Space | O(n + m) | Adjacency list and visited arrays |

With `n ≤ 48`, this solution is far below the limits. Even a quadratic solution would pass comfortably, but linear graph traversal keeps the implementation clean and scalable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())

        graph = [[] for _ in range(n + 1)]

        for _ in range(m):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)

        visited = [False] * (n + 1)
        components = []

        def dfs(start):
            stack = [start]
            visited[start] = True
            comp = []

            while stack:
                node = stack.pop()
                comp.append(node)

                for nei in graph[node]:
                    if not visited[nei]:
                        visited[nei] = True
                        stack.append(nei)

            return comp

        for i in range(1, n + 1):
            if not visited[i]:
                comp = dfs(i)

                if len(comp) > 3:
                    return "-1"

                components.append(comp)

        singles = []
        answer = []

        for comp in components:
            if len(comp) == 3:
                answer.append(comp)
            elif len(comp) == 2:
                answer.append(comp)
            else:
                singles.append(comp[0])

        ptr = 0

        for team in answer:
            if len(team) == 2:
                if ptr >= len(singles):
                    return "-1"

                team.append(singles[ptr])
                ptr += 1

        remaining = singles[ptr:]

        if len(remaining) % 3 != 0:
            return "-1"

        for i in range(0, len(remaining), 3):
            answer.append(remaining[i:i + 3])

        out = []
        for team in answer:
            out.append(" ".join(map(str, team)))

        return "\n".join(out)

    return solve()

# provided sample
assert run("3 0\n") != "-1", "sample 1"

# component of size 4
assert run(
    "6 3\n1 2\n2 3\n3 4\n"
) == "-1", "component too large"

# too many pairs, not enough singles
assert run(
    "6 3\n1 2\n3 4\n5 6\n"
) == "-1", "pairs cannot be completed"

# already valid triple
assert run(
    "6 2\n1 2\n2 3\n"
) != "-1", "size-3 component"

# all isolated students
assert run(
    "9 0\n"
) != "-1", "all singles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 3 / 1 2 / 2 3 / 3 4` | `-1` | Rejects components larger than 3 |
| `6 3 / 1 2 / 3 4 / 5 6` | `-1` | Detects shortage of isolated students |
| `6 2 / 1 2 / 2 3` | Any valid grouping | Handles already completed triples |
| `9 0` | Any valid grouping | Arbitrary grouping of isolated students |

## Edge Cases

Consider the oversized component case:

```
6 3
1 2
2 3
3 4
```

DFS starting from `1` visits `{1,2,3,4}`. The component size becomes `4`, which exceeds the allowed team size immediately. The algorithm prints `-1` before attempting any grouping.

Now examine the insufficient singleton case:

```
6 3
1 2
3 4
5 6
```

The connected components are `{1,2}`, `{3,4}`, and `{5,6}`. Each pair requires one extra isolated student, but there are no singleton components. During the completion phase, the first pair already fails because the `singles` list is empty. The algorithm correctly outputs `-1`.

Finally, consider a mixed valid configuration:

```
9 2
1 2
4 5
```

The components are `{1,2}`, `{4,5}`, and singleton vertices `{3}`, `{6}`, `{7}`, `{8}`, `{9}`.

The algorithm attaches `3` to `{1,2}` and `6` to `{4,5}`. The remaining isolated students `{7,8,9}` naturally form the last team.

Every friendship edge remains inside one team, and every student appears exactly once.
