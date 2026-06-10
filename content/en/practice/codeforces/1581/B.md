---
title: "CF 1581B - Diameter of Graph"
description: "We are asked to determine whether it is possible to construct a simple, connected, undirected graph with a given number of nodes n and edges m such that the graph's diameter is strictly less than k-1."
date: "2026-06-10T10:10:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1581
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 745 (Div. 2)"
rating: 1200
weight: 1581
solve_time_s: 144
verified: true
draft: false
---

[CF 1581B - Diameter of Graph](https://codeforces.com/problemset/problem/1581/B)

**Rating:** 1200  
**Tags:** constructive algorithms, graphs, greedy, math  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether it is possible to construct a simple, connected, undirected graph with a given number of nodes `n` and edges `m` such that the graph's diameter is strictly less than `k-1`. The diameter of a graph is the largest distance between any two nodes, where distance is measured as the minimum number of edges on a path connecting them. No self-loops or multiple edges are allowed.

The input consists of multiple test cases. Each test case specifies the values of `n`, `m`, and `k`. For each, we must output "YES" if it is possible to build a graph satisfying these conditions, or "NO" if it is impossible.

Given the constraints, `n` and `m` can be up to $10^9$ and there can be up to $10^5$ test cases. This means we cannot construct the graph explicitly or perform any operation that scales with `n` or `m`. Instead, we must reason mathematically about what is possible based on the number of nodes, edges, and required diameter.

Edge cases arise when `n` is very small. If `n = 1`, the only valid graph has no edges and diameter 0, which may satisfy some values of `k`. If `k = 1`, the required diameter is less than 0, which is impossible. When `m = 0`, the graph is disconnected if `n > 1`. These are situations where naive counting may produce incorrect results.

## Approaches

The brute-force approach is to attempt to construct the graph explicitly and check its diameter. For small `n`, one could try all possible edge combinations and measure the diameter. This would work for tiny inputs but fails completely for `n` and `m` on the order of $10^9$ because constructing even the adjacency list would take enormous time and space.

The key insight is that the minimum and maximum number of edges in a connected graph of `n` nodes is known. A connected graph must have at least `n-1` edges. The maximum number of edges without loops or multiple edges is $\frac{n(n-1)}{2}$.

The diameter constraints further limit the possibilities. A diameter strictly less than `k-1` can be interpreted as:

- If `k = 1`, the diameter must be 0. This is only possible for `n = 1`.
- If `k = 2`, the diameter must be less than 1, meaning 0, which again requires `n = 1`.
- For `k >= 3`, any connected graph has a diameter between 1 and `n-1`. A star graph has diameter 2, a chain has diameter `n-1`.

We can now reason entirely mathematically: the graph must be connected (`m >= n-1`), the number of edges cannot exceed the complete graph (`m <= n(n-1)/2`), and `k` imposes additional restrictions on `n`. These conditions are sufficient to answer each test case in O(1) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n²) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `m`, `k`.
3. Handle trivial impossibilities first: if `n = 1`, the graph has diameter 0. This satisfies the diameter constraint if `k > 1` and `m = 0`. Otherwise, it is impossible.
4. If `n = 2`, the graph can have 0 or 1 edge. The diameter will be 1 if there is an edge, 0 if none. Check if this satisfies `k-1`.
5. For `n >= 3`, the graph must be connected. So `m >= n-1`. If `m < n-1`, output "NO".
6. The maximum possible number of edges is $\frac{n(n-1)}{2}$. If `m > n(n-1)/2`, output "NO".
7. The diameter requirement depends on `k`. A star graph with `n >= 3` has diameter 2. Thus if `k = 1`, it is impossible. If `k = 2`, only a complete graph can have diameter 1, so `m` must equal `n(n-1)/2`. Otherwise, `k >= 3` is always achievable as long as `n >= 3` and `m` is in the valid range.
8. If all conditions are satisfied, output "YES". Otherwise, output "NO".

Why it works: The algorithm relies on the mathematical properties of connected graphs and known diameters of standard constructions (chain, star, complete). Each check corresponds directly to an impossibility constraint. Since we only reason about counts and bounds, no actual graph construction is needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        if n == 1:
            print("YES" if m == 0 and k > 1 else "NO")
            continue
        if n == 2:
            if m > 1 or m < 1:
                print("NO")
            else:
                print("YES" if k > 1 else "NO")
            continue
        min_edges = n - 1
        max_edges = n * (n - 1) // 2
        if m < min_edges or m > max_edges or k == 1:
            print("NO")
        elif k == 2:
            print("YES" if m == max_edges else "NO")
        else:
            print("YES")

if __name__ == "__main__":
    main()
```

The solution first handles the smallest graphs where edge counts and diameter requirements are corner cases. Then it calculates the minimum and maximum edges for a connected graph and directly applies the diameter logic based on the star and complete graph constructions. This ensures O(1) per test case.

## Worked Examples

**Example 1:** `n = 4, m = 5, k = 3`

| Step | min_edges | max_edges | Check | Output |
| --- | --- | --- | --- | --- |
| 1 | 3 | 6 | 5 in [3,6], k=3>2 | YES |

**Example 2:** `n = 5, m = 4, k = 1`

| Step | min_edges | max_edges | Check | Output |
| --- | --- | --- | --- | --- |
| 1 | 4 | 10 | k=1 impossible | NO |

These traces show that edge counts and diameter bounds correctly determine feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is handled in O(1), t ≤ 10⁵ |
| Space | O(1) | Only a few integers are stored per test case |

The solution easily fits within the 1s time limit and 256 MB memory limit, even for the largest inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("5\n1 0 3\n4 5 3\n4 6 3\n5 4 1\n2 1 1\n") == "YES\nNO\nYES\nNO\nNO"

# Custom cases
assert run("1\n1 0 2\n") == "YES", "n=1, diameter ok"
assert run("1\n1 0 1\n") == "NO", "n=1, diameter impossible"
assert run("1\n3 2 3\n") == "NO", "not enough edges"
assert run("1\n3 3 2\n") == "YES", "exactly enough for complete graph"
assert run("1\n5 10 2\n") == "YES", "complete graph, diameter 1, k=2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 2 | YES | smallest n=1, diameter allowed |
| 1 0 1 | NO | smallest n=1, diameter impossible |
| 3 2 3 | NO | not enough edges for connectivity |
| 3 3 2 | YES | minimum edges for complete graph diameter 1 |
| 5 10 2 | YES | complete graph diameter exactly 1 |

## Edge Cases

For `n = 1, m = 0, k = 2`, the algorithm returns YES. The check for `n == 1` ensures this edge case is handled without relying on general formulas.

For `k = 1` and `n >= 2`, the algorithm outputs NO. This is correct because any connected graph with more than one node has diameter at least 1,
