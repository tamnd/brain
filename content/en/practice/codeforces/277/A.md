---
title: "CF 277A - Learning Languages"
description: "We can think of the company as a graph of employees. Two employees are directly connected if they share at least one language. Communication is allowed through intermediates, so if employee A can talk to B, and B can talk to C, then A and C are effectively connected as well."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu"]
categories: ["algorithms"]
codeforces_contest: 277
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 170 (Div. 1)"
rating: 1400
weight: 277
solve_time_s: 104
verified: true
draft: false
---

[CF 277A - Learning Languages](https://codeforces.com/problemset/problem/277/A)

**Rating:** 1400  
**Tags:** dfs and similar, dsu  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We can think of the company as a graph of employees. Two employees are directly connected if they share at least one language. Communication is allowed through intermediates, so if employee A can talk to B, and B can talk to C, then A and C are effectively connected as well.

The task is to spend the minimum number of lessons so that the entire employee graph becomes connected. Teaching one employee one language costs exactly 1.

Each employee gives us a list of languages they already know. Some employees may know nothing at all. Those employees start completely isolated.

The constraints are very small, only up to 100 employees and 100 languages. Even an $O(n^2 m)$ solution is easily fast enough. This means we do not need sophisticated optimizations. The real challenge is modeling the connectivity correctly.

The key observation is that employees belong to connected components formed by shared languages. If there are $c$ disconnected components among employees who know at least one language, we can connect all components using exactly $c - 1$ lessons. One employee from one component learns a language from another component, merging them.

There is one special case that changes the answer completely. If nobody knows any language initially, then there is no existing communication network at all. Every employee is isolated, and each person must learn some language individually. The answer becomes $n$, not $n - 1$.

A careless implementation often fails on this scenario.

Example:

```
3 2
0
0
0
```

Correct output:

```
3
```

Why? There are no languages anywhere in the system. Teaching only two employees still leaves the third unable to communicate.

Another easy mistake is forgetting that indirect communication counts.

Example:

```
3 3
1 1
2 1 2
1 2
```

Correct output:

```
0
```

Employee 1 shares language 1 with employee 2. Employee 2 shares language 2 with employee 3. All three are already connected transitively.

A naive implementation that only checks direct language overlap would incorrectly think employees 1 and 3 are disconnected.

One more subtle case is when some employees know nothing, but others already form a connected group.

Example:

```
4 3
1 1
1 1
0
0
```

Correct output:

```
2
```

The first two employees are already connected. Each isolated employee can join the network by learning language 1, costing one lesson each.

## Approaches

The brute-force way is to explicitly build a graph between employees. For every pair of employees, we check whether they share at least one language. If they do, we add an edge. Then we count connected components using DFS or BFS.

This works because communication through translators is exactly graph connectivity.

With $n \le 100$, checking all pairs is completely feasible. For every pair we may scan up to 100 languages, giving roughly $100^3 = 10^6$ operations in the worst case.

Once we know the number of connected components, we still need the key insight about lessons. If there are $c$ components, we can merge them using $c - 1$ lessons. Each lesson can connect one previously separate component to another.

The structure becomes even cleaner if we use DSU, also called Union-Find. Every employee starts in their own set. Whenever two employees share a language, we union their sets. At the end, the number of distinct roots gives the number of connected components.

The special all-zero case still needs separate handling. If nobody knows any language, there are technically $n$ isolated employees with no starting communication infrastructure, so the answer is exactly $n$.

The brute-force graph and DSU approaches are both fast enough here. DSU is slightly cleaner because the problem is fundamentally about repeatedly merging groups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Graph + DFS | $O(n^2 m)$ | $O(n^2)$ | Accepted |
| Optimal DSU | $O(n^2 m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all employees and store the languages each one knows.
2. Track whether at least one language appears anywhere in the input.

This matters because the completely empty case has a different formula for the answer.
3. Create a DSU structure with one node per employee.
4. For every pair of employees, check whether they share at least one language.

If they do, union their DSU sets because they can already communicate directly.
5. After processing all pairs, count how many distinct DSU roots exist among employees who belong to the communication graph.
6. If no employee knows any language at all, print $n$.

Every employee must individually learn some language.
7. Otherwise, print:

$$\text{components} - 1$$

Each lesson can merge one disconnected component into another, so connecting all components needs exactly one fewer merge than the number of components.

### Why it works

The DSU maintains the invariant that two employees belong to the same set if and only if communication is already possible between them through existing language chains.

When two employees share a language, they are directly connected, so unioning them preserves correctness. Because DSU merges transitively, any chain of translators also ends up inside the same component.

Suppose there are $c$ connected components. One lesson can connect at most two components, reducing the count by exactly one. Reaching a single connected component therefore requires at least $c - 1$ lessons.

That bound is achievable. We can repeatedly pick one employee from a component and teach them a language from another component, merging the two groups. After $c - 1$ lessons, all employees become connected.

The only exception is when no language exists initially. In that situation there is no component structure to extend, and each employee must learn a language individually, giving answer $n$.

## Python Solution

```python
import sys
input = sys.stdin.readline

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
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return

        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    n, m = map(int, input().split())

    employees = []
    knows_any = False

    for _ in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        langs = set(data[1:])

        if k > 0:
            knows_any = True

        employees.append(langs)

    dsu = DSU(n)

    for i in range(n):
        for j in range(i + 1, n):
            if employees[i] & employees[j]:
                dsu.union(i, j)

    components = set()

    for i in range(n):
        components.add(dsu.find(i))

    if not knows_any:
        print(n)
    else:
        print(len(components) - 1)

solve()
```

The DSU class handles connectivity maintenance. Path compression and union by size keep operations nearly constant time, although the constraints are small enough that even simpler implementations would pass.

Each employee's languages are stored as a Python set. This makes the overlap test:

```
employees[i] & employees[j]
```

very convenient. If the intersection is non-empty, the employees share at least one language.

The `knows_any` flag is critical. Without it, the formula `components - 1` would fail for the all-zero case.

Consider:

```
3 2
0
0
0
```

There are three components, so `components - 1` would give `2`, which is wrong. No existing language network exists to connect through, so all three employees must learn languages.

Another subtle point is that we count components over all employees, including those who know zero languages. Such employees remain isolated in the DSU unless they share a language after future lessons.

## Worked Examples

### Example 1

Input:

```
5 5
1 2
2 2 3
2 3 4
2 4 5
1 5
```

Processing:

| Pair | Shared Language | Action | Components |
| --- | --- | --- | --- |
| 1,2 | 2 | Union | 4 |
| 2,3 | 3 | Union | 3 |
| 3,4 | 4 | Union | 2 |
| 4,5 | 5 | Union | 1 |

Final number of connected components is 1.

Answer:

```
0
```

This trace shows transitive connectivity. Employee 1 and employee 5 do not share a language directly, but the chain of intermediate employees connects them.

### Example 2

Input:

```
4 3
1 1
1 2
0
0
```

Processing:

| Employee | Languages | Initial Component |
| --- | --- | --- |
| 1 | {1} | Separate |
| 2 | {2} | Separate |
| 3 | {} | Separate |
| 4 | {} | Separate |

No unions happen because nobody shares a language.

Total components = 4.

At least one language exists globally, so answer is:

$$4 - 1 = 3$$

Output:

```
3
```

One possible construction is:

Employee 1 learns language 2, employee 3 learns language 1, employee 4 learns language 1.

Now everybody becomes connected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 m)$ | Every employee pair may compare up to $m$ languages |
| Space | $O(n + m)$ | DSU arrays and language storage |

With $n, m \le 100$, the worst-case runtime is tiny. Even a million basic operations runs comfortably within the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

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
            ra = self.find(a)
            rb = self.find(b)

            if ra == rb:
                return

            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra

            self.parent[rb] = ra
            self.size[ra] += self.size[rb]

    n, m = map(int, input().split())

    employees = []
    knows_any = False

    for _ in range(n):
        data = list(map(int, input().split()))
        k = data[0]
        langs = set(data[1:])

        if k > 0:
            knows_any = True

        employees.append(langs)

    dsu = DSU(n)

    for i in range(n):
        for j in range(i + 1, n):
            if employees[i] & employees[j]:
                dsu.union(i, j)

    components = set()

    for i in range(n):
        components.add(dsu.find(i))

    if not knows_any:
        return str(n) + "\n"

    return str(len(components) - 1) + "\n"

# provided sample
assert run(
"""5 5
1 2
2 2 3
2 3 4
2 4 5
1 5
"""
) == "0\n", "sample 1"

# all employees isolated but languages exist
assert run(
"""4 3
1 1
1 2
0
0
"""
) == "3\n", "isolated components"

# nobody knows any language
assert run(
"""3 2
0
0
0
"""
) == "3\n", "all zero case"

# already connected transitively
assert run(
"""3 3
1 1
2 1 2
1 2
"""
) == "0\n", "transitive connectivity"

# minimum meaningful connected case
assert run(
"""2 2
1 1
1 1
"""
) == "0\n", "already connected"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All employees know nothing | 3 | Special all-zero handling |
| Two disconnected language groups plus empty employees | 3 | Component counting correctness |
| Transitive chain of translators | 0 | Indirect communication |
| Two employees sharing one language | 0 | Smallest connected case |

## Edge Cases

Consider the completely empty language graph:

```
3 2
0
0
0
```

The algorithm sets `knows_any = False`. No unions occur, so there are three DSU components.

A naive `components - 1` formula would produce `2`, but the special-case check overrides this and prints `3`.

Each employee must independently learn a language because there is no existing communication infrastructure.

Now consider indirect connectivity:

```
3 3
1 1
2 1 2
1 2
```

Employee 1 unions with employee 2 through language 1. Employee 2 unions with employee 3 through language 2.

The DSU merges all three employees into one component even though employees 1 and 3 never directly overlap.

The algorithm correctly prints:

```
0
```

Finally, consider isolated employees mixed with a connected group:

```
4 2
1 1
1 1
0
0
```

Employees 1 and 2 become one DSU component. Employees 3 and 4 remain isolated.

Total components = 3.

Since at least one language exists globally, the answer becomes:

```
3 - 1 = 2
```

Teaching employees 3 and 4 language 1 connects everybody with exactly two lessons.
