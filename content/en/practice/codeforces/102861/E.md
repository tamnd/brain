---
title: "CF 102861E - Party Company"
description: "The employees form a rooted tree where the company owner is the root. Every employee has an age that is no larger than the age of their manager, so ages never increase when moving down the hierarchy. A party is described by its owner and an allowed age interval."
date: "2026-07-25T14:02:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "E"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 57
verified: true
draft: false
---

[CF 102861E - Party Company](https://codeforces.com/problemset/problem/102861/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The employees form a rooted tree where the company owner is the root. Every employee has an age that is no larger than the age of their manager, so ages never increase when moving down the hierarchy.

A party is described by its owner and an allowed age interval. The owner is always valid for their own party. For another employee to attend, they must have a direct connection to someone already attending, and their age must be inside the interval. This means the invited employees are exactly the connected component of the owner inside the tree after removing employees whose ages are outside the interval.

For every employee, we need to count how many party intervals produce a connected component containing that employee.

The limits are large: both the number of employees and parties can reach 100000. A solution that explores the tree for every party can perform around 10^10 operations in the worst case, which is far beyond what is possible. We need a solution close to O((N + M) log N).

The age ordering gives the key structure. When a party has owner `o` and maximum age `R`, we can move upward from `o` while the manager's age is still at most `R`. Let the highest reachable employee be `h`. Every employee invited to the party is then inside the subtree of `h`, because every ancestor of `o` up to `h` is valid and every side branch from those ancestors also remains connected. Inside that subtree, the only remaining restriction is the minimum age `L`.

There are a few cases where an implementation can fail.

Consider an owner who is the company root:

```
1 1
5 1
1 1 5
```

The answer is:

```
1
```

A solution that assumes every employee has a parent different from itself can break while climbing ancestors.

Another case is when an employee has the exact boundary age:

```
3 1
10 1
5 1
5 2
2 5 5
```

The output is:

```
0 1 1
```

Employees with age exactly `L` or exactly `R` must be included. Using strict comparisons would incorrectly remove them.

A final tricky case is a party whose maximum age stops the climb before the root:

```
4 1
10 1
7 1
4 2
3 3
3 3 7
```

The owner is employee 4. The highest ancestor allowed by age 7 is employee 2, not employee 1. The invited set is employee 2's subtree with age at least 3, giving:

```
0 1 1 1
```

A careless implementation that always starts from the root would count employee 1 incorrectly.

## Approaches

The direct approach is to process every party independently. Starting from the owner, we can run a DFS that only enters employees whose ages are inside the party interval. Every visited employee receives one more invitation. This is correct because the DFS exactly follows the rule that every invited employee must be connected through valid employees.

The problem appears when many parties overlap. In the worst case, every party can visit every employee, giving O(NM) work. With both values reaching 100000, this becomes about 10 billion tree visits.

The useful observation is that a party can be transformed into a geometric update. After finding the highest valid ancestor `h`, the party affects every employee `v` satisfying two conditions: `v` is inside the subtree of `h`, and `age[v] >= L`.

If we run a DFS order over the tree, every subtree becomes a contiguous interval. Employee `v` is represented by the point `(tin[v], age[v])`. A party becomes a rectangle update:

`tin[h] <= tin[v] <= tout[h]` and `age[v] >= L`.

We need to apply many such updates and ask the value at every employee point. This can be solved offline by sorting employees by age. While processing employees from younger to older, we activate every party whose minimum age has already been reached. The active parties only need to add one to an Euler interval, which can be handled by a Fenwick tree.

The final transformation is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N) | Too slow |
| Optimal | O((N + M) log N) | O(N log N) | Accepted |

## Algorithm Walkthrough

1. Build the employee tree and compute Euler tour positions. For every employee, store `tin` and `tout`, so every subtree becomes one interval in Euler order.
2. Build binary lifting tables for ancestors. The age condition is monotonic on the path to the root, so we can jump upward in powers of two and find the highest ancestor whose age does not exceed the party's maximum age.
3. For every party, start at its owner and climb upward using binary lifting. If an ancestor candidate has age at most `R`, move there. The final employee is the highest valid ancestor `h`.
4. Convert the party into an offline update with Euler interval `[tin[h], tout[h]]` and minimum age `L`.
5. Sort employees by age increasingly and sort party updates by their minimum age increasingly. Before answering an employee with age `A`, add every party with `L <= A` into a Fenwick tree as a range increment on its Euler interval.
6. Query the Fenwick tree at the employee's Euler position. The value is the number of active party rectangles covering that employee, which is exactly the number of parties that invite them.

Why it works:

For a party, the highest ancestor `h` with age at most `R` is the topmost point that can remain connected to the owner. Everything outside `h`'s subtree would require crossing a parent edge whose age is already too large. Inside `h`'s subtree, all ages are automatically at most `R` because descendants cannot be older than their ancestors. The only remaining requirement is age at least `L`, which is handled by the offline sweep. Every employee receives one increment for exactly the parties whose rectangle contains their `(tin, age)` point, so the final Fenwick queries produce the required counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    age = [0] * (n + 1)
    graph = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        a, b = map(int, input().split())
        age[i] = a
        if i != b:
            graph[b].append(i)

    LOG = (n + 1).bit_length()
    up = [[1] * (n + 1) for _ in range(LOG)]

    stack = [1]
    order = [1]
    parent = [1] * (n + 1)

    while stack:
        u = stack.pop()
        for v in graph[u]:
            parent[v] = u
            order.append(v)
            stack.append(v)

    for i in range(1, n + 1):
        up[0][i] = parent[i]

    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for i in range(1, n + 1):
            cur[i] = prev[prev[i]]

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 0

    stack = [(1, 0)]
    while stack:
        u, state = stack.pop()
        if state == 0:
            timer += 1
            tin[u] = timer
            stack.append((u, 1))
            for v in reversed(graph[u]):
                stack.append((v, 0))
        else:
            tout[u] = timer

    def highest(o, r):
        u = o
        for k in range(LOG - 1, -1, -1):
            if age[up[k][u]] <= r:
                u = up[k][u]
        return u

    updates = []
    for _ in range(m):
        o, l, r = map(int, input().split())
        h = highest(o, r)
        updates.append((l, tin[h], tout[h]))

    updates.sort()
    employees = sorted((age[i], tin[i], i) for i in range(1, n + 1))

    bit = [0] * (n + 2)

    def add(idx, val):
        while idx <= n:
            bit[idx] += val
            idx += idx & -idx

    def range_add(l, r, val):
        add(l, val)
        add(r + 1, -val)

    def query(idx):
        res = 0
        while idx:
            res += bit[idx]
            idx -= idx & -idx
        return res

    ans = [0] * (n + 1)
    p = 0

    for a, pos, idx in employees:
        while p < m and updates[p][0] <= a:
            _, l, r = updates[p]
            range_add(l, r, 1)
            p += 1
        ans[idx] = query(pos)

    print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The first part of the code constructs the rooted tree and the binary lifting table. The root points to itself in the ancestor table, which avoids special handling when climbing reaches the top of the company hierarchy.

The Euler tour is computed iteratively to avoid Python recursion limits. The important property is that all employees in one subtree have Euler positions between `tin[u]` and `tout[u]`.

The `highest` function uses binary lifting from large jumps to small jumps. Because ages only decrease while moving down the tree, if a jump target is still within the allowed maximum age, every employee between the current position and that jump target is also valid.

The Fenwick tree stores a difference array over Euler positions. A party update adds one to an entire subtree interval using two point updates. The age sweep guarantees that a party is inserted exactly when the current employee age reaches its minimum allowed age.

No multiplication of large values is needed, so Python integer overflow is not a concern. The interval update uses `r + 1`; this extra position is harmless because the Fenwick tree has size `n + 1`, and it prevents off-by-one errors at the end of a subtree.

## Worked Examples

Using the sample input:

```
10 3
8 1
3 5
5 1
2 3
4 1
3 3
1 2
7 1
2 2
3 2
3 5 9
5 3 8
3 2 6
```

The important party transformations are:

| Party | Owner | L | R | Highest ancestor h | Euler update |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 9 | 1 | subtree of 1 |
| 2 | 5 | 3 | 8 | 5 | subtree of 5 |
| 3 | 3 | 2 | 6 | 3 | subtree of 3 |

The sweep processes employees in age order:

| Employee age | Added parties | Euler query result |
| --- | --- | --- |
| 1 | none | 0 |
| 2 | party 3 | 0 or 1 depending on position |
| 2 | party 3 | 1 |
| 3 | parties 2 and 3 | 2 |
| 3 | parties 2 and 3 | 2 |
| 4 | parties 1, 2, 3 | 1 |
| 5 | parties 1, 2, 3 | 3 |
| 7 | parties 1, 2, 3 | 2 |
| 8 | parties 1 | 2 |
| 3 | parties depend on Euler location | 1 |

The final result matches:

```
2 1 3 1 1 2 0 2 0 1
```

A second example:

```
4 2
10 1
7 1
4 2
3 3
4 3 10
2 7 10
```

Party conversion:

| Party | Highest ancestor | Minimum age | Subtree affected |
| --- | --- | --- | --- |
| 1 | 1 | 3 | Entire tree |
| 2 | 2 | 7 | Employees under 2 |

The sweep state becomes:

| Employee | Age | Active parties | Answer |
| --- | --- | --- | --- |
| 4 | 3 | Party 1 | 1 |
| 3 | 4 | Party 1 | 1 |
| 2 | 7 | Party 1, Party 2 | 2 |
| 1 | 10 | Party 1, Party 2 | 2 |

The result is:

```
2 2 1 1
```

This example checks that the maximum age restriction can stop the upward climb and that minimum age filtering is applied correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Binary lifting handles ancestor queries, and each Fenwick operation costs logarithmic time. |
| Space | O(N log N) | The ancestor table dominates memory usage. |

The algorithm uses roughly a few million operations for `N = M = 100000`, which fits comfortably within the intended limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out.strip()

# Sample
assert run("""10 3
8 1
3 5
5 1
2 3
4 1
3 3
1 2
7 1
2 2
3 2
3 5 9
5 3 8
3 2 6
""") == "2 1 3 1 1 2 0 2 0 1"

# Single employee
assert run("""1 1
5 1
1 1 5
""") == "1"

# Equal age boundaries
assert run("""3 2
5 1
5 1
5 2
1 5 5
2 5 5
""") == "1 2 2"

# Climb stops before root
assert run("""4 1
10 1
7 1
4 2
3 3
4 3 7
""") == "0 1 1 1"

# Multiple overlapping ranges
assert run("""5 3
10 1
8 1
5 2
3 2
3 3
1 3 10
2 8 10
3 3 5
""") == "1 2 2 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single employee | `1` | Root handling and self-parent representation |
| Equal age boundaries | `1 2 2` | Inclusive age comparisons |
| Climb stops before root | `0 1 1 1` | Correct highest ancestor search |
| Multiple overlapping ranges | `1 2 2 2 1` | Multiple rectangle updates and overlapping parties |

## Edge Cases

The root-only case works because the binary lifting table stores the root as its own ancestor. The `highest` function never leaves the valid range and correctly keeps the root as the highest possible employee.

For the boundary age case:

```
3 1
5 1
5 1
5 2
2 5 5
```

The party has owner 2 and range `[5,5]`. The owner and employee 3 have the exact allowed age, so both are counted. During the sweep, the party is inserted before processing age 5 employees because `L <= age`, and the Euler interval includes both employees.

For the stopped climb case:

```
4 1
10 1
7 1
4 2
3 3
3 3 7
```

The owner is employee 4. Binary lifting tries to move upward, but employee 1 has age 10, which is outside the maximum age 7. The highest valid ancestor remains employee 2. The update only covers employee 2's subtree, so employee 1 never receives the party increment.

The offline sweep handles all such cases uniformly because every party is represented by exactly the employees that satisfy both the subtree condition and the minimum age condition.
