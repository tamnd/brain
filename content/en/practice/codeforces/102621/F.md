---
title: "CF 102621F - Gorilla Grouping"
description: "We have gorillas identified by integer IDs. Two gorillas cannot be placed together if their IDs differ by exactly K. The task is to count how many non-empty groups of gorillas can be formed where every chosen pair is compatible."
date: "2026-08-02T13:55:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102621
codeforces_index: "F"
codeforces_contest_name: "mBIT Advanced June 2020"
rating: 0
weight: 102621
solve_time_s: 84
verified: true
draft: false
---

[CF 102621F - Gorilla Grouping](https://codeforces.com/problemset/problem/102621/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have gorillas identified by integer IDs. Two gorillas cannot be placed together if their IDs differ by exactly `K`. The task is to count how many non-empty groups of gorillas can be formed where every chosen pair is compatible.

The input describes the total number of gorillas and the fixed distance `K` that creates incompatibilities. The output is the number of valid non-empty selections modulo `10^9 + 7`.

The important observation comes from the structure of the conflicts. If gorilla `x` conflicts with `x + K`, then `x + K` conflicts with `x + 2K`, and so on. Every ID belongs to exactly one sequence of numbers having the same remainder when divided by `K`. Inside each sequence, adjacent elements conflict, while non-adjacent elements do not. This means the conflict graph is not arbitrary. It is a collection of paths.

The constraints are designed so that constructing every possible group is impossible. If there are `N` gorillas, the number of possible subsets is `2^N`, which becomes unusable even for moderately sized `N`. A quadratic approach that checks all pairs can also fail when `N` reaches around `10^5`. We need a solution that touches each gorilla only a constant number of times.

A few edge cases are easy to miss.

Consider a single gorilla:

```
Input:
1 1
```

There are no conflicts, and the only valid non-empty group contains that gorilla, so the answer is:

```
1
```

A solution that only counts chains with length at least two could incorrectly output zero.

Consider a chain where every second gorilla can be chosen:

```
Input:
5 1
```

The conflict chain is:

```
1 - 2 - 3 - 4 - 5
```

The answer is not `5`. Valid choices include `{1,3,5}`, `{1,3}`, `{2,4}`, and many others. A greedy strategy that always takes the largest possible number of gorillas would fail because choosing one vertex changes which neighbors are available.

Consider multiple disconnected chains:

```
Input:
6 3
```

The chains are:

```
1 - 4
2 - 5
3 - 6
```

The choices from each chain are independent, so the final answer must combine the possibilities from all three chains. Treating the whole graph as one path would produce the wrong count.

## Approaches

A brute-force solution can try every subset of gorillas and check whether any conflicting pair appears inside it. The check is correct because a subset is valid exactly when it contains no edge from the conflict graph. However, there are `2^N` subsets, and even with a fast validity check this becomes impossible as soon as `N` is large.

A slightly better idea is to build the graph of conflicts first. The brute-force approach works because the graph representation tells us exactly which pairs matter, but it still explores too many possibilities. The important observation is that this graph has a very restricted shape.

Every gorilla has at most two conflicting neighbors, `id - K` and `id + K`. There cannot be cycles because repeatedly adding or subtracting `K` always moves the ID in one direction until it leaves the valid range. Therefore every connected component is a simple chain.

The remaining problem is counting independent sets in a collection of chains. For a chain of length `c`, let `dp[c]` be the number of ways to select vertices. Looking at one endpoint, either we do not select it and have `dp[c-1]` choices for the rest, or we select it and cannot select its neighbor, leaving `dp[c-2]` choices. This is exactly the Fibonacci recurrence.

Since components do not affect each other, we multiply the number of choices from every chain. The empty selection is included in this product, so we subtract one at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Precompute the number of independent sets for chains of every possible length. Use the recurrence `ways[i] = ways[i-1] + ways[i-2]`, with `ways[0] = 1` and `ways[1] = 2`. The first value represents choosing nothing from an empty chain, and the second represents choosing either the single gorilla or nothing.
2. Mark every gorilla as unvisited. Each unvisited gorilla represents the start of a new connected component in the conflict graph.
3. Walk through all gorilla IDs. For every unvisited ID, follow the sequence `id, id + K, id + 2K, ...` while the IDs remain valid. Count how many gorillas belong to this chain.
4. Multiply the answer by `ways[length]` for this chain. The multiplication works because choices inside different chains never interact.
5. After all chains are processed, subtract one to remove the empty grouping.

Why it works:

Every valid grouping is exactly an independent set of the conflict graph because a chosen pair cannot share an edge. The conflict graph is a disjoint collection of chains. For each chain, the recurrence counts every possible independent set exactly once by deciding whether the first vertex is selected or not. Multiplying the chain counts combines all independent sets from separate components. Removing the empty set leaves exactly the non-empty valid groups.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]

    fib = [0] * (n + 2)
    fib[0] = 1
    fib[1] = 2
    for i in range(2, n + 1):
        fib[i] = (fib[i - 1] + fib[i - 2]) % MOD

    seen = [False] * (n + 1)
    ans = 1

    for i in range(1, n + 1):
        if not seen[i]:
            length = 0
            x = i
            while x <= n:
                seen[x] = True
                length += 1
                x += k
            ans = (ans * fib[length]) % MOD

    print((ans - 1) % MOD)

if __name__ == "__main__":
    solve()
```

The Fibonacci array stores the number of valid selections for every possible chain size. The initialization is slightly different from the usual Fibonacci sequence because an empty chain has one valid selection, and a chain of length one has two selections: choose the gorilla or do not choose it.

The main loop searches for connected components. Starting from an unvisited ID, repeatedly adding `K` visits exactly the vertices in that chain. No separate graph construction is needed because the neighbors are determined directly by the ID difference.

The multiplication happens immediately after a chain is counted. This avoids storing the components and keeps the implementation linear.

There are no overflow issues in Python, but every multiplication is reduced modulo `10^9 + 7` to keep the stored values small and match the required output.

## Worked Examples

Since the statement information provided here does not include official samples, the traces below use constructed examples.

For:

```
Input:
5 1
```

the chain is `1 - 2 - 3 - 4 - 5`.

| Current chain length | ways[length] | Answer after multiplication |
| --- | --- | --- |
| 5 | 13 | 13 |
| Remove empty grouping |  | 12 |

The chain has 13 independent sets, including the empty one. Subtracting one leaves 12 valid non-empty groups.

For:

```
Input:
6 3
```

the chains are `1 - 4`, `2 - 5`, and `3 - 6`.

| Chain | Length | ways[length] | Running answer |
| --- | --- | --- | --- |
| 1 - 4 | 2 | 3 | 3 |
| 2 - 5 | 2 | 3 | 9 |
| 3 - 6 | 2 | 3 | 27 |
| Remove empty grouping |  |  | 26 |

Each chain independently has three choices: choose neither vertex, choose the first, or choose the second.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each gorilla is visited once while discovering its chain, and the Fibonacci table is built once. |
| Space | O(N) | The visited array and Fibonacci table both have linear size. |

The algorithm fits the intended constraints because it never builds all conflict edges and never explores subsets. Even when the number of gorillas is large, every ID participates in only a constant amount of work.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    data = list(map(int, sys.stdin.buffer.read().split()))
    if data:
        n, k = data[0], data[1]
        MOD = 10**9 + 7

        fib = [0] * (n + 2)
        fib[0] = 1
        fib[1] = 2
        for i in range(2, n + 1):
            fib[i] = (fib[i - 1] + fib[i - 2]) % MOD

        seen = [False] * (n + 1)
        ans = 1

        for i in range(1, n + 1):
            if not seen[i]:
                length = 0
                x = i
                while x <= n:
                    seen[x] = True
                    length += 1
                    x += k
                ans = ans * fib[length] % MOD

        print((ans - 1) % MOD)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("1 1\n") == "1\n", "single gorilla"
assert run("5 1\n") == "12\n", "one long chain"
assert run("6 3\n") == "26\n", "multiple chains"
assert run("4 10\n") == "15\n", "no conflicts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum-size case |
| `5 1` | `12` | Fibonacci counting on one chain |
| `6 3` | `26` | Independent multiplication of components |
| `4 10` | `15` | All gorillas are isolated |

## Edge Cases

For a single gorilla, the algorithm creates a chain of length one. The Fibonacci value is `2`, representing the empty choice and the choice containing that gorilla. The final subtraction removes the empty choice and leaves one valid group.

For a long chain such as:

```
5 1
```

the algorithm does not greedily choose alternating vertices. It counts every possible independent set through the recurrence. The chain contributes `13` possibilities including the empty one, and the final answer is `12`.

For multiple chains such as:

```
6 3
```

the traversal starting at `1`, `2`, and `3` discovers three separate components. Each component contributes independently, so the total is the product of the three chain counts rather than the count of one larger structure.

For a case where `K` is larger than the number of gorillas, such as:

```
4 10
```

no ID has a conflicting neighbor. Every gorilla forms a chain of length one, giving `2^4` total subsets. Removing the empty subset produces `15`, which matches the algorithm's result.
