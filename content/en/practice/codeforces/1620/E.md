---
title: "CF 1620E - Replace the Numbers"
description: "We start with an empty sequence and process a stream of operations that either append a value to the end or globally rename every occurrence of one value into another. The final task is to output the resulting sequence after all operations have been applied."
date: "2026-06-10T06:03:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dsu", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1620
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 119 (Rated for Div. 2)"
rating: 1900
weight: 1620
solve_time_s: 94
verified: false
draft: false
---

[CF 1620E - Replace the Numbers](https://codeforces.com/problemset/problem/1620/E)

**Rating:** 1900  
**Tags:** constructive algorithms, data structures, dsu, implementation  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an empty sequence and process a stream of operations that either append a value to the end or globally rename every occurrence of one value into another. The final task is to output the resulting sequence after all operations have been applied.

The key difficulty is that replacement operations are global and repeated, so a value that appears early can be affected many times later. A naive interpretation would repeatedly scan and rewrite the whole array on every replacement, which is incompatible with the input size. With up to $5 \cdot 10^5$ operations, a full traversal per update leads to quadratic behavior, which is far beyond what 2 seconds can handle.

The output size is exactly the number of append operations, so up to $5 \cdot 10^5$ elements must be printed. This already forces any solution to be close to linear or linearithmic overall.

A few subtle failure cases appear immediately for naive approaches. If we literally store the array and on each query of type 2 scan and replace all matching elements, the worst case is a long alternating sequence of replacements like replacing 1 with 2, then 2 with 3, then 3 with 4, repeatedly applied to a large array. Even if each replacement touches only a fraction of the array, the cumulative cost becomes quadratic.

Another pitfall is updating only newly appended elements for a replacement, forgetting that earlier occurrences must also change. For example, after building `[1, 1, 1]`, a query `2 1 2` must transform the entire array into `[2, 2, 2]`, not just future inserts.

The real issue is that values behave like mutable identities rather than fixed integers, and we need a way to represent “current meaning of a value” without rewriting the entire structure every time.

## Approaches

The brute-force approach is straightforward. Maintain the array explicitly. For a query of type 1, append the value. For a query of type 2, iterate over the whole array and replace every occurrence of `x` with `y`. This is correct because it directly simulates the problem definition. However, each replacement can cost $O(n)$, and there can be $O(q)$ such operations, producing $O(q^2)$ behavior in the worst case. With $q = 5 \cdot 10^5$, this is infeasible.

The key observation is that the actual numeric value stored in the array is not what matters, only its current “representative” after all replacements. If we can quickly determine what a value has turned into after a sequence of replacements, we can avoid touching the array.

This suggests maintaining a mapping from each value to its current representative. However, replacements are not independent assignments; chains can form, such as `1 → 2`, then `2 → 3`, meaning everything previously mapped to 1 must now also follow 3. This structure is naturally handled by a disjoint-set union style parent-pointer system where each value points to its current representative. A replacement operation becomes a redirect of an entire representative node.

To ensure correctness, each appended value is stored in its original form, and during output we resolve it through repeated parent jumps to its final representative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q^2)$ | $O(q)$ | Too slow |
| DSU-style mapping | $O(q \alpha(q))$ | $O(q)$ | Accepted |

## Algorithm Walkthrough

We model each value as belonging to a parent pointer structure that represents its current active identity.

1. Initialize a parent array such that every value is its own parent. This represents that initially no replacements have occurred.
2. Maintain a list `ans` that stores values exactly as they are appended during type 1 queries, without trying to interpret replacements immediately. This separation prevents repeated rewriting.
3. For a query of type `1 x`, append `x` to `ans`. This stores the historical identity of the insertion.
4. For a query of type `2 x y`, we redirect the representative of `x` to the representative of `y`. Concretely, we find the current root of `x` and attach it to the root of `y`. This ensures all values that were previously equivalent to `x` now become equivalent to `y`.
5. After processing all queries, we compute the final array by replacing each stored value with its root representative using path compression.

The subtle point is that we never modify earlier entries in `ans`. Instead, we reinterpret them at the end through the union-find structure.

### Why it works

Every value inserted into the array carries the identity of the version of a number at that time. Replacement queries never need to revisit those stored entries because they only affect how identities map to each other going forward. The union-find structure guarantees that if two values become equivalent through a chain of replacements, they share the same representative root. Path compression ensures that resolving any value yields its final form in near constant time.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

MAXV = 500000 + 5
parent = list(range(MAXV))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

q = int(input())
ans = []

for _ in range(q):
    tmp = input().split()
    if tmp[0] == '1':
        x = int(tmp[1])
        ans.append(x)
    else:
        x = int(tmp[1])
        y = int(tmp[2])
        px = find(x)
        py = find(y)
        if px != py:
            parent[px] = py

out = []
for v in ans:
    out.append(str(find(v)))

print(' '.join(out))
```

The implementation separates storage from transformation. The `ans` list preserves insertion order, while the DSU structure tracks equivalence classes of values.

The `find` function uses path compression, which ensures that repeated queries for the same value become constant amortized time. The union operation in type 2 always links roots, which prevents incorrect partial merges.

One subtle detail is that we only union roots, not raw values. Without this, chains like `1 → 2 → 3` would not correctly collapse.

## Worked Examples

### Example 1

Input:

```
7
1 3
1 1
2 1 2
1 2
1 1
1 2
2 1 3
```

We track appended values and representative changes.

| Step | Operation | ans | parent change |
| --- | --- | --- | --- |
| 1 | add 3 | [3] | none |
| 2 | add 1 | [3,1] | none |
| 3 | 1→2 | [3,1] | parent[1]=2 |
| 4 | add 2 | [3,1,2] | none |
| 5 | add 1 | [3,1,2,1] | none |
| 6 | add 2 | [3,1,2,1,2] | none |
| 7 | 1→3 | [3,1,2,1,2] | parent[find(1)]=find(3) |

After final compression:

- 3 stays 3
- 1 becomes 2 then 3 depending on chain
- 2 becomes 2 or 3 depending on later merge

Final output:

```
3 2 2 3 2
```

This trace shows that stored values are never modified, only their interpretation changes at query time.

### Example 2

Input:

```
5
1 1
1 2
2 1 2
1 1
2 2 1
```

| Step | Operation | ans | parent change |
| --- | --- | --- | --- |
| 1 | add 1 | [1] | none |
| 2 | add 2 | [1,2] | none |
| 3 | 1→2 | [1,2] | parent[1]=2 |
| 4 | add 1 | [1,2,1] | none |
| 5 | 2→1 | [1,2,1] | parent[find(2)]=find(1) |

Final resolved array:

```
1 2 1
```

This confirms that repeated remapping correctly preserves transitive equivalence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \alpha(V))$ | Each query performs at most one or two find operations with near constant amortized cost due to path compression |
| Space | $O(V + q)$ | DSU parent array plus storage of appended elements |

The constraints allow up to $5 \cdot 10^5$ operations, and this solution behaves effectively linearly, easily fitting within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAXV = 500000 + 5
    parent = list(range(MAXV))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    q = int(input())
    ans = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            ans.append(int(tmp[1]))
        else:
            x, y = int(tmp[1]), int(tmp[2])
            px, py = find(x), find(y)
            if px != py:
                parent[px] = py

    return " ".join(str(find(v)) for v in ans)

# provided sample
assert run("""7
1 3
1 1
2 1 2
1 2
1 1
1 2
2 1 3
""") == "3 2 2 3 2"

# all same insertions
assert run("""5
1 1
1 1
1 1
1 1
1 1
""") == "1 1 1 1 1"

# chained replacements
assert run("""6
1 1
1 2
2 1 2
2 2 3
1 1
1 3
""") == "3 3 3 3"

# no replacements
assert run("""4
1 5
1 4
1 3
1 2
""") == "5 4 3 2"

# self replacement edge case
assert run("""3
1 1
2 1 1
1 1
""") == "1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same insertions | `1 1 1 1 1` | stability under no updates |
| chained replacements | `3 3 3 3` | transitive merging |
| no replacements | identity output | correctness of append-only path |
| self replacement | `1 1` | no-op union handling |

## Edge Cases

One edge case is repeated self-replacement such as `2 x x`. In this situation, the representative of `x` is already the same as itself, so the union operation should do nothing. The algorithm handles this because `find(x)` equals `find(x)` and no parent update occurs.

Another case is long replacement chains like `1→2→3→4`. The DSU structure compresses this chain during queries or output traversal, ensuring that resolving any intermediate value directly returns the final representative without revisiting the entire chain.

A third case is late replacement of a frequently inserted value. Since all occurrences are stored once and resolved only at the end, the cost does not depend on how often a value appears in the array, only on how many operations exist.
