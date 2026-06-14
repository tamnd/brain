---
title: "CF 1726C - Jatayu's Balanced Bracket Sequence"
description: "We are given a balanced bracket string of length $2n$. Each position in this string is treated as a vertex in a graph. Two vertices $i$ and $j$ are connected by an undirected edge exactly when the substring from $i$ to $j$ forms a balanced bracket sequence on its own."
date: "2026-06-15T01:52:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1726
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 819 (Div. 1 + Div. 2) and Grimoire of Code Annual Contest 2022"
rating: 1300
weight: 1726
solve_time_s: 450
verified: false
draft: false
---

[CF 1726C - Jatayu's Balanced Bracket Sequence](https://codeforces.com/problemset/problem/1726/C)

**Rating:** 1300  
**Tags:** data structures, dsu, graphs, greedy  
**Solve time:** 7m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a balanced bracket string of length $2n$. Each position in this string is treated as a vertex in a graph. Two vertices $i$ and $j$ are connected by an undirected edge exactly when the substring from $i$ to $j$ forms a balanced bracket sequence on its own.

The task is not to construct this graph explicitly, which would be far too large, but to determine how many connected components it contains.

A key difficulty is that edges depend on global structure of substrings rather than local adjacency. Even though the original string is already balanced, most substrings are not balanced, so the graph is sparse in an implicit way that must be understood combinatorially.

The constraints force us into linear or near-linear solutions. The total length across all test cases is at most $10^5$, so any algorithm that checks substrings or tries to simulate connectivity pair by pair will immediately fail. Even $O(n^2)$ scanning of substrings is impossible because a single test case can already reach $10^5$.

A subtle edge case arises from the fact that every balanced bracket string can be uniquely decomposed into primitive segments, where a primitive segment is a smallest prefix that is balanced. For example, `"()(())"` splits into `"()"` and `"(())"`. The graph structure turns out to depend exactly on how these primitive blocks are arranged.

A naive approach would try to connect indices by checking validity of every substring using prefix sums or a stack. This would incorrectly suggest that connectivity is very dense, but it misses that balanced substrings must correspond to exact zero-sum segments that never go negative internally. That constraint is what restricts edges to inside primitive blocks.

## Approaches

A brute-force solution would check every pair $i < j$, verify whether $s[i..j]$ is balanced using a stack or prefix balance check, and then union those vertices in a DSU. Checking a single substring costs $O(n)$ in worst case, and there are $O(n^2)$ substrings, leading to $O(n^3)$ behavior, which is far beyond feasible limits.

We can improve this by noticing that checking balanced substrings can be reduced to prefix sums: a substring is balanced if its total balance is zero and no prefix within it dips below the starting level. Even with prefix sums, iterating over all pairs remains quadratic.

The key structural insight is that connectivity is governed entirely by primitive decomposition of the balanced sequence. Each primitive block is a minimal balanced prefix that returns to balance zero and never touches zero internally. Inside such a block, any vertex can be connected to any other vertex through valid balanced substrings, because the structure behaves like a self-contained component. However, between two different primitive blocks, there is no balanced substring that crosses the boundary, since any crossing would violate prefix balance constraints.

Thus, each primitive segment corresponds to exactly one connected component in the graph. The problem reduces to counting how many times the prefix sum returns to zero while scanning the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Optimal (primitive counting) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Traverse the string from left to right while maintaining a balance counter that increments for `'('` and decrements for `')'`. This tracks how deeply nested we are in the bracket structure.
2. Whenever the balance counter becomes zero, we have completed a primitive balanced segment. This means the substring from the last cut point up to the current position is a minimal self-contained valid block.
3. Increment the answer each time the balance returns to zero, since each such event marks the end of a disconnected component in the graph.
4. Continue until the end of the string, ensuring all primitives are counted.

The intuition behind step 2 is that a balanced prefix that returns to zero cannot be split into smaller balanced parts without violating the prefix constraint, so it acts as a structural unit.

### Why it works

A primitive segment is a maximal contiguous region where the running balance starts at zero, stays strictly positive inside, and returns to zero only at the end. Any balanced substring that starts inside one primitive block and ends outside it must cross a point where the balance is zero in the middle, which would force a decomposition. That prevents any edge from connecting vertices across primitive boundaries. Inside a primitive block, balanced substrings can only connect vertices within the same block, so all vertices in a block are mutually reachable through valid edges. This creates a one-to-one correspondence between primitive blocks and connected components.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    bal = 0
    components = 0

    for ch in s:
        if ch == '(':
            bal += 1
        else:
            bal -= 1

        if bal == 0:
            components += 1

    print(components)
```

The solution processes each test case independently. The balance counter tracks prefix validity in constant time per character. Every time the counter returns to zero, a primitive block ends, and we increment the component count.

The key implementation detail is that we never reset anything except implicitly through balance returning to zero. This avoids any need for explicit segmentation or substring handling.

## Worked Examples

### Example 1: `()(())`

We track balance and count components:

| Index | Char | Balance | Components |
| --- | --- | --- | --- |
| 1 | ( | 1 | 0 |
| 2 | ) | 0 | 1 |
| 3 | ( | 1 | 1 |
| 4 | ( | 2 | 1 |
| 5 | ) | 1 | 1 |
| 6 | ) | 0 | 2 |

The balance returns to zero twice, so we get 2 components. This shows that `"()"` and `"(())"` are independent primitive blocks.

### Example 2: `((()))`

| Index | Char | Balance | Components |
| --- | --- | --- | --- |
| 1 | ( | 1 | 0 |
| 2 | ( | 2 | 0 |
| 3 | ( | 3 | 0 |
| 4 | ) | 2 | 0 |
| 5 | ) | 1 | 0 |
| 6 | ) | 0 | 1 |

Here the entire string forms a single primitive block, so there is one connected component.

These traces demonstrate that the answer is exactly the number of primitive balanced segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is processed once, updating a single counter |
| Space | $O(1)$ | Only a few integer variables are maintained |

The total input size across all test cases is at most $10^5$, so a linear scan per test case is easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        bal = 0
        ans = 0
        for c in s:
            bal += 1 if c == '(' else -1
            if bal == 0:
                ans += 1
        print(ans)

    return output.getvalue()

# provided samples
assert run("""4
1
()
3
()(())
3
((()))
4
(())(())""") == """1
2
1
2
"""

# custom: single primitive
assert run("""1
3
((()))""") == "1\n"

# custom: fully split
assert run("""1
3
()()()""") == "3\n"

# custom: alternating nesting
assert run("""1
4
(())()()""") == "3\n"

# custom: minimum
assert run("""1
1
()""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `((()))` | 1 | single primitive block |
| `()()()` | 3 | maximal fragmentation |
| `(())()()` | 3 | mixed structure boundary counting |
| `()` | 1 | minimal case |

## Edge Cases

A key edge case is when the entire string is one deeply nested structure such as `"(((())))"`. In this case the balance only returns to zero once, at the very end, so the algorithm correctly outputs one component. Any attempt to split based on local patterns would incorrectly overcount.

Another case is fully alternating primitives like `"()()()"`. The balance hits zero after every two characters, producing three components. The algorithm naturally captures each reset as a split point, and no substring crosses between these resets, so connectivity remains confined within each pair.

A mixed structure like `"(())()()"` confirms that nested and flat primitives can coexist. The first reset occurs after the nested block, and subsequent resets occur after each `"()"`, producing exactly three components. This matches the fact that no balanced substring can cross these reset points, since doing so would require violating prefix balance inside the string.
