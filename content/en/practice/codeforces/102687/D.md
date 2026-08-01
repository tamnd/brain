---
title: "CF 102687D - Kapuluan ng Kalayaan 2"
description: "We have a collection of islands connected by ferry routes. Each route has a minimum age requirement, meaning a person can use that route only if their age is at least the route's required value."
date: "2026-08-01T10:32:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102687
codeforces_index: "D"
codeforces_contest_name: "2020 National Olympiad in Informatics - Philippines (NOI.PH) Online Finals, Day 1"
rating: 0
weight: 102687
solve_time_s: 53
verified: true
draft: false
---

[CF 102687D - Kapuluan ng Kalayaan 2](https://codeforces.com/problemset/problem/102687/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of islands connected by ferry routes. Each route has a minimum age requirement, meaning a person can use that route only if their age is at least the route's required value. For every rebel, we know their age and must choose two islands: one where the rebel lives and one where their partner lives. The partner never moves, while the rebel can travel through every ferry route that their age allows.

For one rebel, a placement is invalid only when the rebel's starting island and the partner's island belong to the same connected component after keeping only ferry routes whose requirements are at most the rebel's age. We need count the number of valid placements for every rebel and multiply these independent choices.

The input size is large. There can be up to one million islands and two hundred thousand ferry routes and rebels. A solution that explores the graph separately for every rebel would require too much work because the same connectivity information would be recomputed many times. With a few hundred thousand queries, we need to process the graph globally and answer each age threshold efficiently.

The difficult edge cases come from the changing connectivity as the age increases. For example, consider:

```
3 2 1
1 2 5
2 3 10
5
```

At age 5, only the first ferry works. The components are `{1,2}` and `{3}`. The number of invalid ordered placements is `2*2 + 1*1 = 5`, so the valid answer is `9 - 5 = 4`. A careless solution that builds the graph using all routes would incorrectly think all islands are connected.

Another case is when every island becomes connected:

```
3 3 1
1 2 1
2 3 1
1 3 1
10
```

There is only one component of size 3, so every possible placement allows the rebel to eventually reach the partner. The answer is `0`. Forgetting this case often leads to counting the rebel's starting island as a safe location.

## Approaches

A direct solution would process each rebel separately. For a rebel of age `H`, we could run graph traversal while ignoring every ferry with requirement greater than `H`, mark the reachable islands, and count islands outside that set. This is correct because it exactly simulates the rebel's movement rules. However, doing this for every rebel can take `O(k(n+m))` time. With `k` and `m` around `2 * 10^5`, this is far beyond what is possible.

The key observation is that ferry routes only become available as age increases. If we sort all ferry routes by their required age and process rebels in increasing age order, the graph evolves by only adding edges. This is exactly the situation where a disjoint set union structure is useful.

For a fixed age, suppose the connected component sizes are `s1, s2, ...`. The number of bad ordered pairs of islands is:

```
s1^2 + s2^2 + ...
```

because a rebel and partner are unable to avoid each other exactly when they are chosen inside the same component. The total number of ordered placements is `n^2`, so the number of valid placements is:

```
n^2 - (s1^2 + s2^2 + ...)
```

While merging two components of sizes `a` and `b`, the contribution changes from `a^2 + b^2` to `(a+b)^2`. Maintaining this value lets us answer every query immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k(n+m)) | O(n) | Too slow |
| Optimal | O((n+m+k) log m) | O(n+m+k) | Accepted |

## Algorithm Walkthrough

1. Sort all ferry routes by their age requirement. Sort all rebels by their ages while remembering their original positions.
2. Start with every island in its own disjoint set component. Initially the sum of squared component sizes is `n`, because every component has size one.
3. Process rebels from youngest to oldest. Before answering a rebel with age `H`, merge every ferry route whose requirement is at most `H`.
4. During a merge, remove the two old component contributions from the maintained sum and add the contribution of the merged component. If the component sizes are `a` and `b`, update:

```
sum = sum - a^2 - b^2 + (a+b)^2
```

1. After all possible ferries for this age are added, the rebel's valid placements are:

```
n^2 - sum
```

Store this value for that rebel.

1. Multiply all stored values modulo `10^9+7` because every rebel chooses their own two houses independently.

Why it works:

After processing all edges with requirement at most the current rebel's age, the disjoint set structure represents exactly the islands that the rebel can reach. The maintained squared-size sum counts every invalid placement because every pair inside the same component is reachable. Subtracting it from all possible ordered island pairs leaves exactly the safe placements. Since every rebel's choice does not restrict any other rebel's choice, multiplying these counts gives the final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m, k = map(int, input().split())

    edges = []
    for _ in range(m):
        u, v, d = map(int, input().split())
        edges.append((d, u - 1, v - 1))

    ages = list(map(int, input().split()))

    edges.sort()
    queries = sorted((h, i) for i, h in enumerate(ages))

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra

        nonlocal_sum[0] -= size[ra] * size[ra] + size[rb] * size[rb]
        parent[rb] = ra
        size[ra] += size[rb]
        nonlocal_sum[0] += size[ra] * size[ra]

    nonlocal_sum = [n]
    ans = [0] * k
    edge_ptr = 0
    total_pairs = n * n

    for h, idx in queries:
        while edge_ptr < m and edges[edge_ptr][0] <= h:
            _, u, v = edges[edge_ptr]
            union(u, v)
            edge_ptr += 1

        ans[idx] = total_pairs - nonlocal_sum[0]

    result = 1
    for x in ans:
        result = (result * x) % MOD

    print(result)

if __name__ == "__main__":
    solve()
```

The edge list is sorted once, and the pointer `edge_ptr` only moves forward. This means every ferry route is considered exactly once. The disjoint set structure stores the current connected components, and union by size plus path compression keeps each operation almost constant time.

The variable `nonlocal_sum` represents the total number of invalid ordered pairs for the current age threshold. It must be updated before and after merging because the two old components no longer exist after the union. The subtraction is done before changing the parent array, which avoids accidentally losing the original component sizes.

All calculations involving the number of island pairs use Python integers, so there is no overflow issue. The final multiplication is reduced modulo `10^9+7` because the number of assignments can be extremely large.

## Worked Examples

For the first sample:

```
4 3 2
1 2 567600000
2 3 662300000
3 4 567600000
536100000 630700000
```

The first rebel is too young to use any ferry.

| Age | Added edges | Component sizes | Invalid pairs | Valid pairs |
| --- | --- | --- | --- | --- |
| 536100000 | none | 1,1,1,1 | 4 | 12 |
| 630700000 | 1-2 and 3-4 | 2,2 | 8 | 8 |

The product is `12 * 8 = 96`.

This trace shows why each rebel must be evaluated at their own age. The same graph does not apply to every person.

For the second sample:

```
3 4 2
1 2 599200000
2 3 599200000
3 1 599200000
1 3 410000000
504600000 1009200000
```

| Age | Added edges | Component sizes | Invalid pairs | Valid pairs |
| --- | --- | --- | --- | --- |
| 504600000 | 1-3 | 2,1 | 5 | 4 |
| 1009200000 | remaining edges | 3 | 9 | 0 |

The older rebel can travel anywhere, so no placement is safe.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m+k) log m) | Sorting dominates, while each union-find operation is almost constant time |
| Space | O(n+m+k) | Stores the graph, queries, and disjoint set arrays |

The constraints require avoiding repeated graph traversals. Sorting the edges and using DSU allows all connectivity changes to be handled in one pass, which fits comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = inp.strip().split()
    if not data:
        return ""
    n, m, k = map(int, data[:3])
    pos = 3
    edges = []
    for _ in range(m):
        u, v, d = map(int, data[pos:pos+3])
        pos += 3
        edges.append((u, v, d))
    ages = list(map(int, data[pos:pos+k]))

    sys.stdin = old
    return ""

# samples and custom cases should be executed against the full solve function.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 1 / 1 2 5 / 2 3 10 / 5` | `4` | Partial connectivity |
| `3 3 1 / 1 2 1 / 2 3 1 / 1 3 1 / 10` | `0` | Fully connected graph |
| `2 1 1 / 1 2 100 / 1` | `2` | Minimum graph with unavailable edge |
| A graph with many duplicate ferry routes | correct product | Duplicate edge handling |

## Edge Cases

When an age is smaller than every ferry requirement, the disjoint set remains with every island separate. For `n=3`, this gives an invalid-pair count of `3`, so the valid count is `9-3=6`. The algorithm naturally handles this because no edge is merged.

When multiple ferry routes connect the same islands, only the first successful merge matters. Later routes find both islands already in the same component and do nothing. This prevents duplicate routes from changing the component count.

When all islands become connected, the maintained sum becomes `n^2`. The answer becomes zero because every possible rebel and partner placement lies inside one reachable component.

When several rebels have the same age, they all use the same DSU state. Sorting queries by age means the graph is built once for that threshold rather than rebuilt separately for every rebel.

I can also provide a shorter contest-editorial version or a more formal proof-focused version if you want to adapt it for publication.
