---
title: "CF 102284G - SIS"
description: "We receive the switches one by one. Switch i has an integer label a[i], and if two switches with labels x and y are connected, that channel costs x XOR y."
date: "2026-08-14T04:24:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102284
codeforces_index: "G"
codeforces_contest_name: "\u041b\u041a\u0428 2019, \u0418\u044e\u043b\u044c, \u041c\u0438\u043a\u0441 \u0441\u0442\u0430\u0440\u0448\u0435\u0439 \u0438 \u043c\u043b\u0430\u0434\u0448\u0435\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434"
rating: 0
weight: 102284
solve_time_s: 1368
verified: false
draft: false
---

[CF 102284G - SIS](https://codeforces.com/problemset/problem/102284/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 22m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We receive the switches one by one. Switch `i` has an integer label `a[i]`, and if two switches with labels `x` and `y` are connected, that channel costs `x XOR y`. For every prefix of the input sequence, we need the minimum possible total cost of a connected network containing exactly the switches that have already arrived.

Since any connected network can be reduced to a spanning tree without increasing its cost, the task after each insertion is exactly the minimum spanning tree weight of the complete graph whose vertices are the current switches and whose edge weight between `x` and `y` is `x XOR y`.

The final number of switches can be `100000`, so rebuilding an MST from scratch for every prefix is far too expensive. Even a quadratic Prim implementation on a prefix of size `k` needs Θ(`k²`) edge comparisons. Summed over all prefixes, this is Θ(`n³`), about `3.3 * 10^14` comparisons when `n = 100000`. A quadratic or cubic algorithm cannot fit a normal competitive programming time limit.

The values satisfy `0 <= a[i] <= 200000`. Since `200000 < 2^18`, every value needs only 18 binary bits, from bit 17 down to bit 0. This small bit width is the structural property that makes a binary trie useful. An algorithm polynomial in the number of bits, rather than in the number of possible pairs of switches, is feasible.

There are several edge cases that are easy to mishandle. First, equal values are distinct switches but their connecting cost is zero. For input `3` with values `5 5 5`, the answers are `0 0 0`. An implementation that treats equal values as duplicate vertices would still happen to get the MST weight right here, but it can easily break its insertion logic by assuming every new value creates a new trie leaf.

A more subtle case is when adding a switch changes the best edge between two binary trie subtrees, while simultaneously changing the MST inside one of those subtrees. For example, with `0 7 3`, the answers are `0 7 7`. After inserting `3`, the best edge between `{0,3}` and `{7}` becomes `3 XOR 7 = 4`, replacing the previous cross edge of cost `7`, but the subtree `{0,3}` itself now needs an edge of cost `3`. The two changes cancel. A careless solution that simply adds the new switch's nearest distance to the previous MST would obtain `7 + 3 = 10`, which is wrong.

The highest allowed bit is another boundary case. For input `3` with values `0 131072 131073`, the answers are `0 131072 131073`. Since `131072 = 2^17`, bit 17 must be included. Using only bits 16 through 0 silently loses the most significant contribution and produces an incorrect result.

Finally, the first switch has no edge at all, so its MST cost is zero. For `2` with values `0 1`, the required output is `0 1`. Code that updates the answer before having an opposite trie branch can accidentally introduce a nonexistent edge.

## Approaches

The direct approach is to process every prefix independently. For a prefix containing `k` switches, we can construct the complete graph implicitly and run Prim's algorithm. For each newly selected vertex, we scan all remaining vertices and compute their XOR distance. This is correct because Prim always produces an MST, and the complete graph contains every possible channel. The problem is the repeated work. One prefix costs Θ(`k²`), so all prefixes cost

`1² + 2² + ... + n² = Θ(n³)`.

For `n = 100000`, that is roughly `3.33 * 10^14` pair checks, which is nowhere near practical.

The key observation comes from looking at XOR by its highest differing bit. Consider all values sharing some fixed prefix, and suppose their next relevant bit is `b`. Split them into `L`, whose bit `b` is zero, and `R`, whose bit `b` is one. Every edge inside `L` and every edge inside `R` has bit `b` equal to zero. Every edge between `L` and `R` has bit `b` equal to one. Since all higher bits are equal inside this trie node, every internal edge is strictly cheaper than every cross edge.

That means Kruskal would completely connect `L` and `R` internally before considering any edge between them. After both sides are connected, exactly one cross edge is needed. The cheapest possible cross edge is therefore the minimum XOR between a value in `L` and a value in `R`.

This gives the fundamental recurrence

`MST(node) = MST(left) + MST(right) + minimum_cross(node)`,

where the last term is zero if one of the two children is empty.

A binary trie represents exactly these recursive partitions. The remaining problem is dynamic: after inserting one value, only the trie nodes on that value's root-to-leaf path can change. At each such node, the internal MST of the chosen child changes deeper in the trie, and the only new possible cross edge is the edge from the newly inserted value to the opposite child.

So we maintain, for every trie node, the current cheapest edge connecting its two children. When a new value `x` is inserted, we walk down its trie path. At a node corresponding to bit `b`, if the opposite child already exists, we query that subtree for the value minimizing `x XOR y`. This gives the only new candidate that can improve the node's cross edge. We update the global MST answer by the difference between the new and old cross-edge costs.

The minimum-XOR query itself is the standard binary-trie greedy walk. At every lower bit, we prefer the branch containing the same bit as `x`, because that contributes zero to the XOR. If that branch does not exist, we take the other branch and add the corresponding power of two to the query result.

The brute-force works because it explicitly recomputes all pair relationships. It fails because almost all of that information is unchanged between consecutive prefixes. The observation that the MST decomposes along binary prefixes lets us update only one root-to-leaf path, and each cross-edge query is another trie walk.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` total | `O(n)` | Too slow |
| Optimal | `O(n log^2 A)` | `O(n log A)` | Accepted |

Here `A` is the maximum possible value, and in this problem `log A <= 18`.

## Algorithm Walkthrough

1. Build an initially empty binary trie containing all values inserted so far. Each trie node stores its two children and the current minimum XOR edge connecting those children.

The root represents all inserted switches. Following bit 17, then bit 16, and so on partitions the switches according to their binary prefixes.
2. For each incoming value `x`, start at the root and follow the path corresponding to the bits of `x` from bit 17 down to bit 0.

Only nodes on this path can change when `x` is added. Every other trie node contains exactly the same set of old switches as before.
3. At a node corresponding to bit `b`, identify the child containing the same bit as `x` and the opposite child.

If the opposite child does not exist, there was no cross edge before the insertion and there is still no cross edge after the insertion. We only continue down the matching child.
4. If the opposite child exists, query that subtree for the minimum XOR with `x`, considering only bits below `b`.

The current bit contributes exactly `2^b`, because the two children differ at bit `b`. The lower-bit trie query determines the remaining part of the edge weight.
5. Compare this candidate cross-edge weight with the value stored for the node.

The only new edges introduced by this insertion are edges from `x` to old switches. Among the edges crossing this node's two children, every old pair already existed. Thus the old minimum can only stay unchanged or be replaced by the edge from `x` to the closest value in the opposite child.
6. If the candidate is smaller, replace the stored cross-edge value and add the difference to the global MST answer.

A decrease here is possible. For example, when inserting `3` into `{0,7}`, the root's cross edge improves from `7` to `4`. At the same time, a deeper node gains the internal edge `0 XOR 3 = 3`. The global answer records both changes, giving `7 - 3 + 3 = 7`.
7. Create the matching child if it does not already exist, then continue to the next lower bit.

Creating the trie path happens after checking the opposite subtree, so every query considers only switches that were present before the current insertion.
8. After processing all 18 bits, append the current global answer to the output.

For one switch there are no edges, so the answer naturally remains zero.

### Why it works

For every trie node, all values in its subtree have the same higher binary prefix. If its children differ at bit `b`, every edge crossing the two children has the same higher contribution and has bit `b` set, while every edge staying inside one child has bit `b` unset. Consequently, all internal edges are cheaper than every cross edge. Kruskal must finish the two child subproblems before using a cross edge, and exactly one minimum cross edge is sufficient to connect them. This proves the recursive MST decomposition.

During insertion, all nodes outside the new value's trie path contain exactly the same vertices, so their MST costs and cross-edge minima cannot change. At a path node, the only newly available cross edges are those incident to the new value. The trie query finds the cheapest such edge. Updating the stored cross-edge minimum is consequently exact, and the sum of all changed node contributions is exactly the new MST weight. By induction over insertions, every reported answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_BIT = 17

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Each node has two children.
    # -1 means that the child does not exist.
    left = [-1]
    right = [-1]

    # cross[v] is the minimum XOR edge between the two
    # children of v. Zero means that one child is absent.
    cross = [0]

    answer = 0
    out = []

    for x in a:
        node = 0

        for b in range(MAX_BIT, -1, -1):
            bit = (x >> b) & 1

            if bit == 0:
                opposite = right[node]
            else:
                opposite = left[node]

            if opposite != -1:
                # Find the minimum XOR between x and a value
                # in the opposite subtree, using lower bits.
                cur = opposite
                lower_xor = 0
                k = b - 1

                while k >= 0:
                    xb = (x >> k) & 1

                    if xb == 0:
                        nxt = left[cur]
                        if nxt == -1:
                            nxt = right[cur]
                            lower_xor |= 1 << k
                    else:
                        nxt = right[cur]
                        if nxt == -1:
                            nxt = left[cur]
                            lower_xor |= 1 << k

                    cur = nxt
                    k -= 1

                candidate = (1 << b) + lower_xor
                old = cross[node]

                if old == 0 or candidate < old:
                    cross[node] = candidate
                    if old == 0:
                        answer += candidate
                    else:
                        answer += candidate - old

            # Move down the trie, creating the new path if necessary.
            if bit == 0:
                nxt = left[node]
                if nxt == -1:
                    nxt = len(left)
                    left.append(-1)
                    right.append(-1)
                    cross.append(0)
                    left[node] = nxt
            else:
                nxt = right[node]
                if nxt == -1:
                    nxt = len(left)
                    left.append(-1)
                    right.append(-1)
                    cross.append(0)
                    right[node] = nxt

            node = nxt

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The three arrays represent the binary trie. `left[v]` and `right[v]` identify the children, while `cross[v]` stores the cheapest edge joining the two child subtrees. There is no need to store the vertices themselves inside trie nodes.

The loop over `b` follows the new value from the highest relevant bit to the lowest. The highest relevant bit is 17 because `200000 < 2^18`. Using 18 bits is enough for every legal input, while starting at bit 18 would also work but would add unnecessary work.

Before descending into the matching child, the code examines the opposite child. This ordering matters. The opposite subtree must contain only previously inserted switches, because the new switch has not yet been attached to the trie. Otherwise the query could accidentally use `x` itself as its own partner.

The query starts directly from the opposite child instead of from the root. At the current bit `b`, the two child prefixes already differ, so the contribution of that bit is known to be `2^b`. Only lower bits need to be optimized. This is why the query begins at `b - 1`.

When the preferred trie branch is missing, the query takes the other branch and sets the corresponding bit in `lower_xor`. This exactly implements minimum XOR search: matching bits are always preferable because they contribute zero.

The `cross` value uses zero as a sentinel because any real edge between two different children has at least one differing bit, so its XOR value is positive. Equal switch labels remain in the same trie leaf and never create a positive cross edge.

Python integers automatically handle the potentially large MST sum, so there is no overflow issue. The maximum possible answer is well within Python's integer capabilities in any case.

## Worked Examples

### Sample 1

For the sequence `4 0 2 2 9 4`, the important changes are shown below.

| Inserted value | Changed trie level | Old cross | New cross | Delta | Total answer |
| --- | --- | --- | --- | --- | --- |
| `4` | none | 0 | 0 | `0` | `0` |
| `0` | bit 2 | 0 | 4 | `+4` | `4` |
| `2` | bit 1 | 0 | 2 | `+2` | `6` |
| `2` | none | unchanged | unchanged | `0` | `6` |
| `9` | bit 3 | 0 | 9 | `+9` | `15` |
| `4` | none | unchanged | unchanged | `0` | `15` |

After inserting `0`, the two values are separated for the first time at bit 2, so the only edge costs `4 XOR 0 = 4`.

When `2` arrives, it belongs to the same bit-2 side as `0`, but differs from `0` at bit 1. That creates a cheaper internal connection of cost `2`. The total becomes `6`.

The second `2` is a duplicate value. It creates another switch but every new edge from it to an existing switch has exactly the same cost as the corresponding edge from the first `2`, and in particular it can use a zero-cost edge to that switch. The MST weight stays `6`.

The value `9` first differs from the existing values at bit 3. The cheapest edge connecting the new bit-3 side to the old side has cost `9`, increasing the answer to `15`. The final `4` is already represented by the existing value `4`, so a zero-cost connection is available and the MST weight remains `15`.

### A second example

Consider the sequence `0 7 3 4`.

| Inserted value | Changed level | Old cross | New cross | Delta | Total answer |
| --- | --- | --- | --- | --- | --- |
| `0` | none | 0 | 0 | `0` | `0` |
| `7` | bit 2 | 0 | 7 | `+7` | `7` |
| `3` | bit 2 | 7 | 4 | `-3` | `4` |
| `3` | bit 1 | 0 | 3 | `+3` | `7` |
| `4` | bit 1 | 0 | 3 | `+3` | `10` |

The third insertion demonstrates the most subtle part of the update. Before inserting `3`, the root separates `{0}` from `{7}`, so its cross cost is `7`. After inserting `3`, the root separates `{0,3}` from `{7}`, and the best cross edge is `3 XOR 7 = 4`. The root contribution decreases by `3`.

At the same time, the subtree containing `{0,3}` gains its own MST edge of cost `0 XOR 3 = 3`. The total change is `-3 + 3 = 0`, so the answer remains `7`.

After inserting `4`, the subtree containing `7` and `4` gains the edge `4 XOR 7 = 3`. The resulting MST can use edges with costs `3`, `3`, and `4`, for a total of `10`.

This trace is especially useful because it shows why maintaining only the distance from the new switch to the old MST is not sufficient. Several trie levels can change at once, and their contributions can increase or decrease independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log^2 A)` | There are `O(log A)` trie levels, and at each level a minimum-XOR query takes `O(log A)` |
| Space | `O(n log A)` | At most `O(n log A)` trie nodes are created |

Here `A <= 200000`, so there are only 18 relevant bits. Each insertion performs at most 18 minimum-XOR searches, and the total number of lower-bit steps is at most `17 + 16 + ... + 0`, which is only 153 trie steps per insertion. For `100000` switches this is about 15.3 million inner query steps, plus the ordinary trie insertion work.

The memory usage is also manageable. In fact, because there are only `2^18` possible values, the complete binary trie would contain fewer than `2^19` nodes, even though the general `O(n log A)` bound is sufficient for the analysis.

## Test Cases

```python
# Helper: run the solution logic on an input string and return its output.
import sys
import io

MAX_BIT = 17

def solve_data(data: str) -> str:
    inp = io.StringIO(data)
    n = int(inp.readline())
    a = list(map(int, inp.readline().split()))

    left = [-1]
    right = [-1]
    cross = [0]

    answer = 0
    out = []

    for x in a:
        node = 0

        for b in range(MAX_BIT, -1, -1):
            bit = (x >> b) & 1

            if bit == 0:
                opposite = right[node]
            else:
                opposite = left[node]

            if opposite != -1:
                cur = opposite
                lower_xor = 0
                k = b - 1

                while k >= 0:
                    xb = (x >> k) & 1

                    if xb == 0:
                        nxt = left[cur]
                        if nxt == -1:
                            nxt = right[cur]
                            lower_xor |= 1 << k
                    else:
                        nxt = right[cur]
                        if nxt == -1:
                            nxt = left[cur]
                            lower_xor |= 1 << k

                    cur = nxt
                    k -= 1

                candidate = (1 << b) + lower_xor
                old = cross[node]

                if old == 0 or candidate < old:
                    cross[node] = candidate
                    answer += candidate if old == 0 else candidate - old

            if bit == 0:
                nxt = left[node]
                if nxt == -1:
                    nxt = len(left)
                    left.append(-1)
                    right.append(-1)
                    cross.append(0)
                    left[node] = nxt
            else:
                nxt = right[node]
                if nxt == -1:
                    nxt = len(left)
                    left.append(-1)
                    right.append(-1)
                    cross.append(0)
                    right[node] = nxt

            node = nxt

        out.append(str(answer))

    return "\n".join(out)

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample
assert run("6\n4 0 2 2 9 4\n") == "0\n4\n6\n6\n15\n15", "sample 1"

# Minimum-size input
assert run("2\n0 1\n") == "0\n1", "minimum size"

# All values equal
assert run("4\n123 123 123 123\n") == "0\n0\n0\n0", "all equal"

# Highest allowed bit and a lower-bit refinement
assert run("3\n0 131072 131073\n") == "0\n131072\n131073", "bit 17 boundary"

# Cases where the new vertex changes different trie levels
assert run("4\n0 7 3 4\n") == "0\n7\n7\n10", "multiple levels"

# Maximum-size input, all equal, answer always zero
vals = " ".join(["0"] * 100000)
expected = "\n".join(["0"] * 100000)
assert run("100000\n" + vals + "\n") == expected, "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 1` | `0 1` | Minimum number of switches and first nonzero edge |
| `4 / 123 123 123 123` | `0 0 0 0` | Duplicate values and zero-cost edges |
| `3 / 0 131072 131073` | `0 131072 131073` | Highest allowed bit, plus a lower-bit improvement |
| `4 / 0 7 3 4` | `0 7 7 10` | Multiple trie levels changing during one insertion |
| `100000` zeros | 100000 zeros | Maximum input size and repeated identical values |

## Edge Cases

The duplicate-value case is handled naturally by the trie. For input `4` with values `123 123 123 123`, every new value follows exactly the same path as the first one. No opposite child is created at any level, so no cross-edge contribution changes. The output is `0 0 0 0`. The switches are still distinct vertices, but connecting equal labels costs zero.

The first insertion has no opposite subtree anywhere because the trie contains no previous values. For input `2` with values `0 1`, the first answer is `0`. When `1` is inserted, the two values first differ at bit 0, the query below that bit is empty, and the new cross edge has cost `1`. The output is `0 1`.

The maximum-value boundary uses bit 17. For input `3` with values `0 131072 131073`, inserting `131072` creates a split at bit 17 and adds `2^17 = 131072`. When `131073` arrives, it belongs to the same bit-17 subtree as `131072` and differs from it only at bit 0, so the MST gains an edge of cost `1`. The output is `0 131072 131073`.

The most deceptive case is `0 7 3`. After `0` and `7`, the only edge has cost `7`. When `3` arrives, the root's best cross edge improves from `7` to `3 XOR 7 = 4`, reducing the root contribution by `3`. At the lower bit where `0` and `3` split, a new internal edge of cost `3` appears. The two changes cancel, leaving the answer at `7`. This is exactly why the algorithm updates every trie node on the insertion path rather than treating the new switch as a single edge added to the previous MST.

The final sample also exercises duplicate insertion after several trie levels have already been built. In `4 0 2 2 9 4`, the second `2` and second `4` do not improve any stored cross edge, so the answer stays unchanged at their respective insertions. The algorithm does not need special duplicate handling because the trie structure and the minimum-XOR queries already account for zero-cost connections.
