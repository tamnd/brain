---
title: "CF 102299G - Hunting leshys"
description: "We have n leshys, each with a fixed power. At the beginning, every leshy is the root of its own hierarchy, so there are n separate trees. A meeting operation + i j says that leshy j becomes subordinate to leshy i."
date: "2026-08-13T08:12:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102299
codeforces_index: "G"
codeforces_contest_name: "2019 USP Try-outs"
rating: 0
weight: 102299
solve_time_s: 53
verified: true
draft: false
---

[CF 102299G - Hunting leshys](https://codeforces.com/problemset/problem/102299/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` leshys, each with a fixed power. At the beginning, every leshy is the root of its own hierarchy, so there are `n` separate trees.

A meeting operation `+ i j` says that leshy `j` becomes subordinate to leshy `i`. Since hierarchies are guaranteed never to contain a cycle, this operation joins two previously separate hierarchy trees. The exact parent-child direction matters for reporting, but for answering queries we only need to know which leshys belong to the same tree.

A threat operation `? i` starts at leshy `i` and travels upward until it reaches the leader of that hierarchy. Once the whole hierarchy knows about the threat, the least powerful leshy in that entire tree is assigned to handle it. Thus a query asks for the minimum power among all leshys in the connected component containing `i`.

The constraints make the intended representation fairly clear. There can be up to `10^5` leshys and as many as `5 * 10^5` operations, with a one-second time limit. An algorithm that scans an entire hierarchy for every query can perform around `10^5 * 5 * 10^5 = 5 * 10^10` operations in the worst case, which is far beyond what the time limit allows. We need nearly constant amortized work per operation.

The powers can be as large as `10^9`, but they are only compared and stored, so Python integers are more than sufficient. The fact that the hierarchy is guaranteed acyclic means every successful meeting merges two different trees, which is exactly the setting where a disjoint-set union structure applies.

A first edge case is a single leshy.

```
1 1
7
? 1
```

The answer is `7`. A solution that assumes every query has a parent to follow could fail here because the queried leshy is already the leader.

Another edge case is equal power values.

```
2 2
5 5
+ 1 2
? 2
```

The answer is `5`. The hierarchy determines who is the leader, but power determines who handles the threat. Confusing those two notions can produce the wrong result if the implementation tries to choose the leader based on power.

A third useful case is when a new subordinate is attached below a non-root leshy.

```
3 3
10 4 7
+ 1 2
+ 2 3
? 3
```

The resulting hierarchy is `1 -> 2 -> 3`, and the answer is `4`. The component is `{1, 2, 3}`, so the answer is the minimum power in the whole component, not merely the minimum on the path from `3` to the root. A solution that only follows the parent chain and tries to inspect the visited vertices would happen to work here, but it would still be doing unnecessary work because the answer depends on the entire tree.

## Approaches

The direct approach is to explicitly maintain the parent of every leshy. For a query `? i`, we could walk from `i` through its parents until reaching the leader, collect the members of that hierarchy, and then find their minimum power. This is correct because every leshy in the same hierarchy eventually reports to the same leader, and the assigned leshy is simply the minimum-power member of that hierarchy.

The problem is the amount of work. A hierarchy can contain all `n` leshys, and a query can require examining all of them. With `m` operations, a worst-case sequence can require `O(nm)` work, which is up to `5 * 10^10` elementary visits for the given bounds. Even if we optimize the parent traversal, repeatedly scanning the hierarchy for its minimum remains too expensive.

The useful observation is that the answer to a query does not depend on the shape or direction of the hierarchy. It only depends on the set of leshys belonging to the same hierarchy. A meeting merges two such sets, while a query asks for the minimum power stored in one set.

This is precisely the abstraction handled by a disjoint-set union, or DSU. Each hierarchy is represented by one DSU component. For every component we store its minimum power. When `+ i j` occurs, we merge the components containing `i` and `j`, and the minimum of the new component is simply the minimum of the two old minima. When `? i` occurs, we find the representative of `i` and return the stored minimum for that representative.

The brute-force method works because it reconstructs the hierarchy for every query, but fails when the same large hierarchy is queried repeatedly. The observation that only component membership and the component minimum matter lets us discard the hierarchy structure entirely and maintain exactly the information queries need.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` worst case | `O(n)` | Too slow |
| Optimal | `O((n + m) α(n))` | `O(n)` | Accepted |

Here `α(n)` is the inverse Ackermann function, which grows so slowly that for all practical competitive-programming constraints it behaves like a small constant.

## Algorithm Walkthrough

1. Read the power of every leshy and initialize a DSU component containing only that leshy. Its component minimum is its own power because no other leshy belongs to it yet.
2. For a `+ i j` operation, find the DSU representatives of `i` and `j`. The meeting joins their two hierarchies, so their components must be merged.

The direction saying that `j` becomes subordinate to `i` is irrelevant for future answers. Regardless of which leshy is the formal parent, both sets now belong to one hierarchy.
3. When merging two components, use union by size or rank so that DSU trees stay shallow. Store the smaller of the two component minima as the minimum of the merged component.
4. For a `? i` operation, find the representative of `i` and output the minimum stored for that representative. Every leshy in that component belongs to the same hierarchy, so this value is exactly the power of the leshy who handles the threat.
5. Use path compression in `find`. Whenever a representative is discovered, compress the path from the queried leshy directly toward that representative. Future operations can then locate the component much faster.

### Why it works

The invariant is that every DSU component represents exactly one current hierarchy, and the minimum stored at its representative is the minimum power among all leshys in that hierarchy.

Initially every hierarchy consists of one leshy, so the invariant holds. A meeting joins two distinct hierarchies into one. DSU performs exactly that merge, and taking the minimum of the two stored minima gives the minimum over the combined hierarchy. A query does not modify the hierarchy, so finding the component of `i` and returning its stored minimum gives the least powerful leshy among exactly the people who become aware of the threat. Since every operation preserves this invariant, every query returns the required power.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    power = list(map(int, input().split()))

    parent = list(range(n))
    size = [1] * n
    minimum = power[:]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(m):
        op = input().split()

        if op[0] == '+':
            a = int(op[1]) - 1
            b = int(op[2]) - 1

            a = find(a)
            b = find(b)

            if a == b:
                continue

            if size[a] < size[b]:
                a, b = b, a

            parent[b] = a
            size[a] += size[b]
            minimum[a] = min(minimum[a], minimum[b])

        else:
            x = int(op[1]) - 1
            root = find(x)
            out.append(str(minimum[root]))

    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()
```

The `parent` array is the DSU forest. Initially `parent[i] = i`, because every leshy starts as the representative of its own hierarchy. The `size` array supports union by size, preventing the DSU structure from degenerating into a long chain.

The `minimum` array stores the minimum power for each component representative. Values belonging to non-representatives do not need to be updated because every query first calls `find` and then reads the value from the current representative.

The `find` implementation uses iterative path halving. The assignment `parent[x] = parent[parent[x]]` shortens the path while walking upward, giving the same asymptotic behavior as ordinary path compression without recursion. This also avoids Python recursion-depth concerns.

The indices in the input are one-based, while Python arrays are zero-based, so every input index is decreased by one immediately. The union operation checks whether the two representatives are already equal. The problem guarantees that the hierarchy never becomes cyclic, so such a merge should not occur in valid input, but keeping the check makes the DSU robust and avoids corrupting the component size or minimum.

There is no integer-overflow issue in Python, and the largest power fits comfortably in a Python integer anyway. The output is accumulated in a list and written once at the end, which avoids the overhead of performing a separate output operation for every query.

## Worked Examples

For the first sample,

```
4 6
3 12 5 6
? 2
+ 3 2
? 2
? 3
+ 4 1
? 1
```

The DSU starts with four singleton components.

| Operation | Component of queried/merged vertices | Component minimums | Output |
| --- | --- | --- | --- |
| `? 2` | `{2}` | `{2}: 12` | `12` |
| `+ 3 2` | `{2,3}` | `{2,3}: 5` |  |
| `? 2` | `{2,3}` | `{2,3}: 5` | `5` |
| `? 3` | `{2,3}` | `{2,3}: 5` | `5` |
| `+ 4 1` | `{1,4}`, `{2,3}` | `{1,4}: 3`, `{2,3}: 5` |  |
| `? 1` | `{1,4}` | `{1,4}: 3` | `3` |

The resulting output is `12`, `5`, `5`, `3`. The trace shows why hierarchy direction does not matter to the query. After `+ 3 2`, leshy `2` reports through `3`, but both simply belong to the same DSU component whose minimum power is `5`.

For the second sample,

```
5 5
5 2 2 1 9
+ 4 2
+ 3 1
+ 5 3
+ 1 4
? 1
```

The operations progressively connect all five leshys.

| Operation | Merged components | New component minimum |
| --- | --- | --- |
| `+ 4 2` | `{4}` and `{2}` | `1` |
| `+ 3 1` | `{3}` and `{1}` | `2` |
| `+ 5 3` | `{5}` and `{3,1}` | `2` |
| `+ 1 4` | `{5,3,1}` and `{4,2}` | `1` |
| `? 1` | query component `{1,2,3,4,5}` | `1` |

The answer is `1`. This example demonstrates that the final hierarchy can be shaped as a chain or any other tree, while the DSU only needs the fact that all five vertices now belong to one component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n + m) α(n))` | Each union and query performs a constant number of DSU operations, each amortized by inverse Ackermann complexity. |
| Space | `O(n)` | The DSU stores a parent, size, and minimum value for every leshy. |

With `n <= 10^5` and `m <= 5 * 10^5`, the solution performs essentially constant amortized work per operation. This is comfortably suitable for the one-second time limit, while a repeated traversal of large hierarchies can require tens of billions of operations.

## Test Cases

The following test harness uses the same `solve()` function as the submitted solution. The maximum-size test creates `100000` leshys and `499999` merge operations, which is large enough to exercise the intended asymptotic behavior while keeping the test practical.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    power = list(map(int, input().split()))

    parent = list(range(n))
    size = [1] * n
    minimum = power[:]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(m):
        op = input().split()

        if op[0] == '+':
            a = int(op[1]) - 1
            b = int(op[2]) - 1

            a = find(a)
            b = find(b)

            if a == b:
                continue

            if size[a] < size[b]:
                a, b = b, a

            parent[b] = a
            size[a] += size[b]
            minimum[a] = min(minimum[a], minimum[b])
        else:
            x = int(op[1]) - 1
            out.append(str(minimum[find(x)]))

    sys.stdout.write('\n'.join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Sample 1
assert run("""\
4 6
3 12 5 6
? 2
+ 3 2
? 2
? 3
+ 4 1
? 1
""") == "12\n5\n5\n3", "sample 1"

# Sample 2
assert run("""\
5 5
5 2 2 1 9
+ 4 2
+ 3 1
+ 5 3
+ 1 4
? 1
""") == "1", "sample 2"

# Minimum-size input
assert run("""\
1 3
42
? 1
? 1
? 1
""") == "42\n42\n42", "single leshy"

# All powers equal
assert run("""\
4 5
7 7 7 7
+ 1 2
+ 3 4
? 2
+ 2 3
? 4
""") == "7\n7", "equal powers"

# Boundary and off-by-one case
assert run("""\
5 6
10 8 6 4 2
+ 2 5
? 5
+ 4 3
? 3
+ 1 4
? 5
""") == "2\n4\n2", "component boundaries"

# Large input
n = 100000
m = 499999
powers = " ".join(["1000000000"] * n)

ops = []
for i in range(1, n):
    ops.append(f"+ {i} {i + 1}")
ops.append("? 100000")

large_input = f"{n} {m}\n{powers}\n" + "\n".join(
    ops + ["? 1"] * (m - len(ops))
) + "\n"

# The generated sequence has many repeated queries after all merges.
assert run(large_input).splitlines()[0] == "1000000000", "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 3 / 42 / ? 1 / ? 1 / ? 1` | `42`, `42`, `42` | A hierarchy containing only its leader |
| Four powers all equal to `7` | `7`, `7` | Minimum handling when several leshys tie |
| Five leshys with progressively merged components | `2`, `4`, `2` | Component boundaries and index conversion |
| `100000` leshys with hundreds of thousands of operations | `1000000000` for the first query | Large-scale DSU performance and repeated queries |

## Edge Cases

The singleton hierarchy case is handled by the initial DSU state. For

```
1 1
7
? 1
```

`find(1)` immediately returns the only representative, and `minimum[0]` is `7`, so the output is `7`. No special-case code is needed because a one-element hierarchy is already a valid DSU component.

Equal powers are also handled naturally. For

```
2 2
5 5
+ 1 2
? 2
```

the merge computes `min(5, 5)`, which is `5`. The algorithm never uses the leshy index or hierarchy leader as a substitute for power, so equal values do not introduce an ambiguity.

A merge can attach a hierarchy below a leshy that is not its own representative. For example,

```
3 3
10 4 7
+ 1 2
+ 2 3
? 3
```

After the first merge, `{1,2}` has minimum `4`. The second merge joins leshy `3` with that component, giving minimum `4` again. The query finds the representative of `3` and returns `4`. The DSU does not need to know that the formal hierarchy is `1 -> 2 -> 3`, because the entire set is what determines the answer.

The largest power value is another boundary worth checking. A value such as `1000000000` is stored directly in `minimum`, and `min()` compares it normally. Python has arbitrary-precision integers, so there is no overflow risk even if the implementation is later adapted to store other derived integer values.

Finally, a query may arrive immediately before any merge involving the queried leshy. For example,

```
3 2
8 3 5
? 3
? 1
```

both queries operate on singleton components, producing `5` and `8`. The DSU representation is valid from the very first operation, so queries do not require any prior construction phase.
