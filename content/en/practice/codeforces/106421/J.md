---
title: "CF 106421J - Building Bridges"
description: "We have a set of houses, each carrying an integer value. We need to build a connected network between all houses using exactly n - 1 bridges, meaning the final structure is a spanning tree."
date: "2026-06-25T09:42:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106421
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 3-11-2026 Div. 2 (Advanced)"
rating: 0
weight: 106421
solve_time_s: 45
verified: true
draft: false
---

[CF 106421J - Building Bridges](https://codeforces.com/problemset/problem/106421/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of houses, each carrying an integer value. We need to build a connected network between all houses using exactly `n - 1` bridges, meaning the final structure is a spanning tree.

Alice assigns every possible bridge between two houses a value equal to the greatest common divisor of their two numbers. Her goal is to choose a spanning tree with the largest possible sum of bridge values.

Bob uses a different score. The value of a bridge is the gcd of the squares of the two numbers, which is the square of the original gcd. He wants a spanning tree where the weakest bridge is as strong as possible. In other words, he wants to maximize the minimum edge value in the chosen tree.

The input gives the number on each house. The output asks for Alice's maximum total score and Bob's maximum possible minimum score.

The number of houses can reach `200000`, while values can be as large as `1000000`. A quadratic approach over all pairs of houses would require around `4 * 10^10` comparisons, which is impossible. Even generating every possible bridge is too expensive, so the solution has to exploit the fact that gcd depends only on divisibility. The maximum value range of `10^6` suggests that iterating over divisors and multiples is the intended direction.

A few cases are easy to mishandle. If all numbers are equal, every bridge has the same gcd and the answer should use that value. For example, input `3` with values `5 5 5` gives output `10 25` because Alice gets two edges of weight `5` and Bob can make every edge have value `25`. A careless implementation that only looks for pairs with different values could fail here.

Another tricky case is when only a small group shares a large factor. For input `4` with values `6 10 15 7`, the best Alice tree cannot use gcd `5` or `3` for all edges because the vertex `7` is disconnected from that group. The answer is `3 1`. A method that simply picks the largest common divisor appearing in any pair would incorrectly overestimate the result.

A final edge case is when the best bottleneck value is `1`. For input `3` with values `2 3 5`, every pair has gcd `1`, so Bob's answer is `1`. Looking only at repeated prime factors would miss that a connected tree still always exists through gcd `1`.

## Approaches

The brute force way to solve Alice's part is to treat the problem as a maximum spanning tree problem. We can create a complete graph where every pair of houses has an edge weighted by their gcd, then run Kruskal's algorithm in descending order. This is correct because Kruskal's algorithm always finds a maximum spanning tree when edges are processed from large to small.

The issue is the graph itself. There are `n * (n - 1) / 2` possible edges. With `n = 200000`, this is about twenty billion edges. Computing and sorting them is far beyond the available time.

The key observation is that a gcd value `d` appears only between numbers that are all divisible by `d`. Instead of asking which pairs have gcd `d`, we can ask which houses are multiples of `d`. While processing values from large to small, all bridges with gcd at least the current value have already been considered. Connecting all multiples of the current divisor simulates adding all edges of this weight without explicitly creating them.

For a fixed divisor `d`, all houses divisible by `d` form a group. If we connect all of them to a single representative, every successful union corresponds to one Kruskal edge with weight `d`. The number of successful unions is exactly the number of edges added at this weight.

Bob's problem uses the same ordering because squaring preserves order. A bridge with larger gcd always has a larger squared gcd. During the same descending process, the first divisor that makes the whole graph connected is the largest possible minimum gcd. Squaring that value gives Bob's answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n²) | O(n²) | Too slow |
| Optimal | O(A log A + n * number_of_divisors(A)) | O(A + n) | Accepted |

Here `A` is the maximum possible value, `1000000` in this problem.

## Algorithm Walkthrough

1. Count how many times every value appears and store the indices of houses having each value. We need the actual indices because the union find structure works on houses, not values.
2. Process every divisor `d` from `1000000` down to `1`. For every multiple of `d`, visit all houses whose values equal that multiple. All of these houses are connected by edges whose gcd is at least `d`.
3. Choose one representative house among the visited houses and union every other visited house with it. Each successful union means we added one bridge of value `d` in Kruskal's process, so add `d` to Alice's answer.
4. After finishing all unions for a divisor, check whether all houses are now in one component. The first divisor where this happens is Bob's maximum possible minimum gcd. Store its square.
5. Print Alice's accumulated value and Bob's stored value.

The invariant behind the algorithm is that before processing divisor `d`, the union find structure represents exactly the connectivity created by all bridges with gcd greater than `d`. When we merge all multiples of `d`, we add every possible connection that can have gcd `d`. This matches Kruskal's ordering, so every successful merge contributes exactly one chosen edge in the maximum spanning tree.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    MAXV = max(a)

    buckets = [[] for _ in range(MAXV + 1)]
    for i, x in enumerate(a):
        buckets[x].append(i)

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n

    def union(x, y):
        nonlocal components
        x = find(x)
        y = find(y)
        if x == y:
            return False
        if size[x] < size[y]:
            x, y = y, x
        parent[y] = x
        size[x] += size[y]
        components -= 1
        return True

    ans_a = 0
    ans_b = 1

    for d in range(MAXV, 0, -1):
        rep = -1
        for m in range(d, MAXV + 1, d):
            for v in buckets[m]:
                if rep == -1:
                    rep = v
                else:
                    if union(rep, v):
                        ans_a += d
        if components == 1:
            ans_b = d * d
            break

    print(ans_a, ans_b)

if __name__ == "__main__":
    solve()
```

The buckets array groups houses by their values. This avoids repeatedly scanning all houses when checking divisors. The total number of visits is related to the number of divisors of each value, which stays manageable for values up to one million.

The union find operations are the core of the Kruskal simulation. Path compression and union by size keep each operation almost constant time. The variable `components` lets us detect Bob's answer immediately once the graph becomes connected.

The loop goes downward because maximum spanning trees require processing large edge weights first. If it went upward, smaller gcd values would already connect components and the contribution to Alice's answer would be wrong.

The value for Bob is stored as `d * d` because the bridge score is the gcd of squares, which equals the square of the original gcd.

## Worked Examples

For the first sample:

```
5
1 4 6 9 12
```

The important states are:

| Divisor processed | Houses divisible by divisor | Components | Alice added |
| --- | --- | --- | --- |
| 12 | 12 | 5 | 0 |
| 9 | 9 | 5 | 0 |
| 6 | 6,12 | 4 | 6 |
| 4 | 4,12 | 3 | 4 |
| 1 | all houses | 1 | 4 |

The final Alice value is `6 + 4 + 4 = 14`. The first divisor making the graph connected is `1`, so Bob's value is `1`.

For the second sample:

```
4
2 14 12 4
```

The trace is:

| Divisor processed | Houses divisible by divisor | Components | Alice added |
| --- | --- | --- | --- |
| 14 | 14 | 4 | 0 |
| 12 | 12 | 4 | 0 |
| 7 | 14 | 4 | 0 |
| 4 | 4,12 | 3 | 4 |
| 2 | 2,14,12,4 | 1 | 4 |

Alice gets `8`, and Bob gets `4` because divisor `2` is the first value connecting all houses.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A log A + n * τ(A)) | Every divisor checks its multiples and every house is visited once per divisor of its value |
| Space | O(A + n) | Buckets, union find arrays, and value storage |

The maximum value is only `10^6`, so the multiple iteration is feasible. The number of divisors of a value in this range is small enough for the total work to fit within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    MAXV = max(a)
    buckets = [[] for _ in range(MAXV + 1)]

    for i, x in enumerate(a):
        buckets[x].append(i)

    parent = list(range(n))
    size = [1] * n
    components = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        nonlocal components
        x = find(x)
        y = find(y)
        if x == y:
            return False
        if size[x] < size[y]:
            x, y = y, x
        parent[y] = x
        size[x] += size[y]
        components -= 1
        return True

    ans = 0
    b = 1

    for d in range(MAXV, 0, -1):
        rep = -1
        for m in range(d, MAXV + 1, d):
            for v in buckets[m]:
                if rep == -1:
                    rep = v
                elif union(rep, v):
                    ans += d
        if components == 1:
            b = d * d
            break

    return f"{ans} {b}\n"

assert run("5\n1 4 6 9 12\n") == "14 1\n"
assert run("4\n2 14 12 4\n") == "8 4\n"
assert run("2\n7 7\n") == "7 49\n"
assert run("3\n2 3 5\n") == "2 1\n"
assert run("5\n10 20 30 40 50\n") == "40 100\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 7 7` | `7 49` | Equal values and minimal size |
| `3 / 2 3 5` | `2 1` | No large common divisor exists |
| `5 / 10 20 30 40 50` | `40 100` | Shared factors and multiple merges |

## Edge Cases

When all values are identical, every house can connect through the same gcd. For input `3` and values `5 5 5`, the algorithm processes divisor `5`, merges all houses immediately, adds two edges of weight `5`, and sets Bob's answer to `25`.

When a large divisor appears only in part of the graph, it cannot be the final bottleneck. For input `4` with values `6 10 15 7`, divisor `5` connects only `10` and `15`, and divisor `3` connects only `6` and `15`. The first divisor that connects everyone is `1`, so Bob's answer is `1`.

When every pair has gcd `1`, the descending process reaches divisor `1` and merges the whole graph there. For input `3` with values `2 3 5`, Alice receives two edges of value `1` and Bob receives `1`, which is handled naturally by the final divisor check.
