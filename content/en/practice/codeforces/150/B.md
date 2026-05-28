---
title: "CF 150B - Quantity of Strings"
description: "We want to count strings of length n built from an alphabet of size m, under one strong restriction: every substring of length k must be a palindrome."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 150
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 107 (Div. 1)"
rating: 1600
weight: 150
solve_time_s: 100
verified: true
draft: false
---

[CF 150B - Quantity of Strings](https://codeforces.com/problemset/problem/150/B)

**Rating:** 1600  
**Tags:** combinatorics, dfs and similar, graphs, math  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We want to count strings of length `n` built from an alphabet of size `m`, under one strong restriction: every substring of length `k` must be a palindrome.

A substring of length `k` starting at position `i` contains characters

$$s_i, s_{i+1}, \dots, s_{i+k-1}$$

and being a palindrome means

$$s_i = s_{i+k-1}, \quad s_{i+1} = s_{i+k-2}, \dots$$

The task is to count how many full strings satisfy all such constraints simultaneously. Since the number can become enormous, we output the answer modulo $10^9 + 7$.

The limits are small enough to allow graph construction or DFS over positions. With `n, k ≤ 2000`, an $O(n^2)$ algorithm is perfectly safe. A cubic solution would start becoming risky, especially in Python. Enumerating all strings is impossible because there are $m^n$ candidates, and even for `n = 50` that number is already astronomically large.

The tricky part is that palindrome conditions from overlapping substrings interact with each other. A local condition can force equalities very far apart.

Consider this example:

```
n = 5, k = 3
```

The substrings are:

```
s[0..2], s[1..3], s[2..4]
```

From the first palindrome we get:

```
s0 = s2
```

From the second:

```
s1 = s3
```

From the third:

```
s2 = s4
```

Combining them gives:

```
s0 = s2 = s4
s1 = s3
```

So the whole string is determined by only two independent character groups.

A common mistake is to treat each substring independently and multiply possibilities. That overcounts because the same positions appear in many substrings.

Another subtle edge case is `k = 1`. Every substring of length `1` is automatically a palindrome, so there are no equality constraints at all.

Example:

```
n = 4, m = 3, k = 1
```

Every string works, so the answer is:

```
3^4 = 81
```

A careless implementation that always merges positions inside windows might accidentally add constraints even when none exist.

The opposite extreme is `k = n`. Then the entire string itself must be a palindrome.

Example:

```
n = 5, m = 2, k = 5
```

We need:

```
s0 = s4
s1 = s3
```

Only three positions are independent, so the answer is:

```
2^3 = 8
```

Understanding that the problem is really about equality relations between indices is the key observation.

## Approaches

The brute-force approach is straightforward. Generate every string of length `n`, then check whether every substring of length `k` is a palindrome.

There are $m^n$ strings. For each string, we inspect roughly `n` substrings, and each palindrome check costs up to `k`.

That gives:

$$O(m^n \cdot n \cdot k)$$

which is hopeless even for moderate values.

The reason brute force works conceptually is that the condition is easy to verify locally. The problem is that the number of candidate strings explodes exponentially.

The important observation is that palindrome constraints only force some positions to be equal. They never restrict which actual character is used.

Suppose a substring of length `k` starts at `i`. Then for every offset `j`:

$$s_{i+j} = s_{i+k-1-j}$$

So positions become connected by equality relations.

Once two positions are known to be equal, they behave as a single variable. After processing all substrings, the string is partitioned into connected components of equal positions.

If there are `c` independent components, then each component may choose any of the `m` letters independently.

So the answer becomes:

$$m^c$$

modulo $10^9+7$.

This transforms the problem from constructing strings into counting connected components in a graph.

We can model positions `0 ... n-1` as graph vertices. Whenever a palindrome condition says two positions must match, we connect them. Then we compute how many connected components remain.

DFS, BFS, or DSU all work. Since the constraints are tiny, a simple DFS solution is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m^n \cdot n \cdot k)$ | $O(n)$ | Too slow |
| Optimal | $O(nk)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Create a graph with `n` vertices, one for each string position.
2. For every substring of length `k`, add equality edges implied by the palindrome condition.

If the substring starts at `i`, then:

$$s_{i+j} = s_{i+k-1-j}$$

for all valid `j`.

So we connect those two indices in the graph.
3. After processing all substrings, positions connected through any path must contain the same character.

This works because equality is transitive. If `a = b` and `b = c`, then `a = c`.
4. Run DFS over the graph to count connected components.

Every connected component corresponds to one independent character choice.
5. Compute:

$$m^{\text{components}} \bmod (10^9+7)$$

using fast modular exponentiation.

### Why it works

Every palindrome constraint can be written as a collection of equalities between pairs of positions. The graph stores exactly these equalities.

If two positions belong to the same connected component, there exists a chain of equality relations connecting them, so they must contain the same character.

If two positions are in different components, no constraint links them, so they may be chosen independently.

Thus each connected component behaves like one free variable with `m` choices. Multiplying over all components gives:

$$m^c$$

where `c` is the number of connected components.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n, m, k = map(int, input().split())

    graph = [[] for _ in range(n)]

    # Add palindrome equality constraints
    for start in range(n - k + 1):
        l = start
        r = start + k - 1

        while l < r:
            graph[l].append(r)
            graph[r].append(l)
            l += 1
            r -= 1

    visited = [False] * n

    def dfs(node):
        stack = [node]
        visited[node] = True

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            dfs(i)

    print(pow(m, components, MOD))

if __name__ == "__main__":
    main()
```

The graph stores equality constraints between positions. For every substring of length `k`, we connect mirrored indices because those positions must match in a palindrome.

The loop:

```
while l < r:
```

is important. We only connect mirrored pairs once. When `k` is odd, the middle character does not create any constraint because it mirrors itself.

The DFS computes connected components. Every unvisited node starts a new component, which represents one independent character group.

Using iterative DFS avoids recursion depth concerns, although recursion would also fit within these limits.

The final answer uses Python's built-in modular exponentiation:

```
pow(m, components, MOD)
```

which runs in logarithmic time.

A subtle implementation detail is indexing. The problem statement is naturally 1-based, but the code uses 0-based indexing throughout. The substring `[start, start + k - 1]` must be handled carefully to avoid off-by-one mistakes.

## Worked Examples

### Example 1

Input:

```
1 1 1
```

There is only one position and one possible character.

| Step | Action | Graph | Components |
| --- | --- | --- | --- |
| 1 | Create node 0 | No edges | 0 |
| 2 | No palindrome pairs needed | No edges | 0 |
| 3 | DFS from node 0 | One component | 1 |
| 4 | Compute $1^1$ | Final answer | 1 |

The trace shows the `k = 1` edge case. No equality constraints are added, so every position stays independent.

### Example 2

Input:

```
5 2 3
```

Substrings of length 3:

```
[0,1,2]
[1,2,3]
[2,3,4]
```

Palindrome constraints:

```
0 = 2
1 = 3
2 = 4
```

| Step | Added Edge | Connected Groups |
| --- | --- | --- |
| 1 | (0, 2) | {0,2} |
| 2 | (1, 3) | {1,3} |
| 3 | (2, 4) | {0,2,4}, {1,3} |

Now there are exactly two connected components.

So the answer is:

$$2^2 = 4$$

The valid strings are:

```
ababa
babab
aaaaa
bbbbb
```

This example demonstrates how overlapping substrings propagate equalities across long distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nk)$ | Each substring contributes at most `k/2` equality edges |
| Space | $O(n^2)$ | The graph can contain $O(nk)$ edges in the worst case |

With `n ≤ 2000`, the graph remains comfortably small. Even in the densest cases, the total work is only a few million operations, well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    graph = [[] for _ in range(n)]

    for start in range(n - k + 1):
        l = start
        r = start + k - 1

        while l < r:
            graph[l].append(r)
            graph[r].append(l)
            l += 1
            r -= 1

    visited = [False] * n

    def dfs(node):
        stack = [node]
        visited[node] = True

        while stack:
            u = stack.pop()

            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append(v)

    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            dfs(i)

    print(pow(m, components, MOD))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup

    return out.getvalue().strip()

# provided sample
assert run("1 1 1\n") == "1", "sample 1"

# k = 1, every string valid
assert run("4 3 1\n") == "81", "all strings allowed"

# full string must be palindrome
assert run("5 2 5\n") == "8", "entire string palindrome"

# overlapping constraints create one component
assert run("4 10 2\n") == "10", "adjacent equality chain"

# odd palindrome propagation
assert run("5 2 3\n") == "4", "two independent groups"

# maximum-style stress shape
assert run("2000 1 2000\n") == "1", "single alphabet letter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 3 1` | `81` | No constraints when `k = 1` |
| `5 2 5` | `8` | Whole string palindrome behavior |
| `4 10 2` | `10` | Adjacent equalities merge everything |
| `5 2 3` | `4` | Overlapping windows propagate constraints |
| `2000 1 2000` | `1` | Large boundary values |

## Edge Cases

Consider:

```
4 3 1
```

Every substring of length `1` is automatically a palindrome. The graph receives no edges at all.

DFS sees four separate components:

```
{0}, {1}, {2}, {3}
```

So the answer is:

$$3^4 = 81$$

This confirms the algorithm does not accidentally introduce constraints when `k = 1`.

Now consider:

```
5 2 5
```

The entire string must be a palindrome.

The algorithm adds:

```
0 = 4
1 = 3
```

Position `2` stays alone.

Connected components become:

```
{0,4}, {1,3}, {2}
```

So there are three independent choices:

$$2^3 = 8$$

This verifies correct handling when the palindrome spans the whole string.

Finally, consider a case where equalities propagate transitively:

```
4 10 2
```

Every substring of length `2` must be a palindrome, meaning adjacent characters must match.

The graph edges are:

```
0-1
1-2
2-3
```

DFS merges everything into one component:

```
{0,1,2,3}
```

Only one character choice remains, so the answer is:

$$10^1 = 10$$

This confirms that connected components correctly capture transitive equality.
