---
title: "CF 105051D - \u041f\u0438\u0440\u0430\u043c\u0438\u0434\u0430"
description: "Each input brick is a rectangle with fixed dimensions $wi times hi$. From any brick, you are allowed to “shrink” it into exactly one new rectangle $a times b$, as long as both sides do not increase, meaning $a le wi$ and $b le hi$."
date: "2026-06-28T01:01:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105051
codeforces_index: "D"
codeforces_contest_name: "2023-2024 \u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb"
rating: 0
weight: 105051
solve_time_s: 58
verified: true
draft: false
---

[CF 105051D - \u041f\u0438\u0440\u0430\u043c\u0438\u0434\u0430](https://codeforces.com/problemset/problem/105051/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input brick is a rectangle with fixed dimensions $w_i \times h_i$. From any brick, you are allowed to “shrink” it into exactly one new rectangle $a \times b$, as long as both sides do not increase, meaning $a \le w_i$ and $b \le h_i$. No other transformations are allowed, so every original brick can only produce a single usable smaller rectangle.

A valid pyramid is a stack of exactly $k$ bricks, where the $t$-th layer from the top must be a square of size $(2t-1) \times (2t-1)$. So layer 1 is $1 \times 1$, layer 2 is $3 \times 3$, layer 3 is $5 \times 5$, and so on. Each layer must be supported by choosing one of the given bricks and shrinking it if necessary to match the required square size.

The task is to compute the maximum possible height $k$, meaning the largest number of these required square layers that can be matched using the available bricks, each brick used at most once.

The constraints push us toward an $O(n \log n)$ or $O(n)$ solution. With $n \le 10^5$, any approach that tries all assignments between bricks and layers, or attempts matching via bipartite search, would be too slow if it exceeds roughly $10^8$ operations. Sorting-based or greedy strategies are natural candidates.

A subtle issue is that each brick can only be used once, and shrinking is asymmetric: a brick $(w, h)$ can produce any $(a, b)$ with both coordinates bounded, but it cannot “rotate” or partially split capacity between multiple layers. Another edge case is that a brick large enough for a higher layer automatically works for all smaller layers, so over-allocating large bricks to small requirements can block feasibility for larger ones.

For example, if we need layers $1 \times 1$ and $3 \times 3$, and have a single $5 \times 5$ brick and a single $3 \times 3$ brick, assigning the $5 \times 5$ brick to $1 \times 1$ is correct locally but may block the only feasible assignment for $3 \times 3$ if no other brick fits it.

## Approaches

A brute-force idea is to try assigning bricks to pyramid levels. For each level $t$, we check which bricks can be reduced to $(2t-1) \times (2t-1)$, and then search for a matching assignment across all levels. This becomes a bipartite matching problem between levels and bricks, where an edge exists if a brick can satisfy a level. A maximum matching would give the answer.

This is correct, but the graph has up to $10^5$ nodes on one side and potentially $10^5$ on the other, with up to $10^{10}$ implicit edges in the worst case if many bricks are large. Even if edges are generated on the fly, running matching or flow is far too slow.

The key observation is monotonicity. Requirements for layers strictly increase: layer $t+1$ requires a strictly larger square than layer $t$. Meanwhile, each brick has a “capacity” defined by how large a square it can support, which is $\min(w_i, h_i)$. If we sort bricks by this capacity, we are essentially trying to match the smallest required layers with the smallest sufficient bricks, greedily.

This converts the problem into: given required values $1, 3, 5, \dots$, and available capacities $c_i = \min(w_i, h_i)$, find the longest prefix of requirements that can be covered by assigning each requirement a distinct capacity that is at least that value. This is a standard greedy matching on sorted arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force matching / flow | $O(n^3)$ or worse | $O(n^2)$ | Too slow |
| Greedy sorting + matching | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Convert each brick $(w_i, h_i)$ into a single value $c_i = \min(w_i, h_i)$. This represents the largest square side length the brick can safely support after shrinking.
2. Sort all capacities $c_i$ in non-decreasing order so we can match small requirements first.
3. Initialize a pointer $i = 0$ over bricks and a counter $t = 1$, representing the current required square side length $2t - 1$.
4. While we still have bricks left and we can satisfy the current requirement:

1. Move $i$ forward until we find a brick with $c_i \ge 2t - 1$.
2. If no such brick exists, stop; we cannot build further layers.
3. Assign this brick to level $t$ and increment both $i$ and $t$.
5. Output $t - 1$, which is the maximum achievable height.

The greedy choice is to always use the smallest available brick that can satisfy the current requirement. This preserves larger bricks for future larger requirements, which are harder to satisfy.

### Why it works

At any step, we are matching the current smallest unmet requirement $2t-1$ with the smallest available capacity that can satisfy it. If we instead used a larger brick than necessary, we would only reduce flexibility for later steps, because all future requirements are strictly larger. Any optimal assignment can be transformed into one that respects this ordering without decreasing the number of matched layers, by swapping assignments whenever a larger-than-necessary brick is used for an earlier layer while a smaller feasible brick exists.

This exchange argument guarantees that greedy matching never blocks a feasible solution that an optimal strategy could achieve.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    caps = []
    for _ in range(n):
        w, h = map(int, input().split())
        caps.append(min(w, h))

    caps.sort()

    t = 1
    i = 0
    ans = 0

    while i < n:
        need = 2 * t - 1

        while i < n and caps[i] < need:
            i += 1

        if i == n:
            break

        ans += 1
        i += 1
        t += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution compresses each brick into a single usable value, which avoids dealing with two-dimensional constraints directly. Sorting ensures we always consider weaker bricks first. The inner loop skips unusable bricks, and each brick is consumed at most once, so the pointer only moves forward.

A common mistake is attempting to match from largest bricks downward, which can waste large capacities on small layers and reduce the total achievable height. Another is forgetting that each brick is used once, so reusing capacity across multiple layers is invalid.

## Worked Examples

### Example 1

Input:

```
3
1 1
3 3
5 5
```

Required layers are $1, 3, 5$.

| Step | Required | Pointer i | Caps[i] | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | assign 1x1 | 1 |
| 2 | 3 | 1 | 3 | assign 3x3 | 2 |
| 3 | 5 | 2 | 5 | assign 5x5 | 3 |

This shows perfect alignment when capacities already match requirements exactly.

### Example 2

Input:

```
4
2 2
6 6
4 4
1 1
```

Capacities: [2, 6, 4, 1] → sorted: [1, 2, 4, 6]

| Step | Required | Pointer i | Caps[i] | Action | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | use 1 | 1 |
| 2 | 3 | 1 | 2 | skip 2 | - |
| 2 | 3 | 2 | 4 | use 4 | 2 |
| 3 | 5 | 3 | 6 | use 6 | 3 |

This demonstrates skipping insufficient bricks while preserving larger ones for later requirements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, linear scan afterward |
| Space | $O(n)$ | storing capacities |

The algorithm comfortably fits within limits for $n = 10^5$, since sorting $10^5$ integers and a single linear pass is efficient in 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# NOTE: placeholder; assumes solve() is imported or included

def test():
    import subprocess, textwrap, sys

    def exec_run(inp):
        from subprocess import Popen, PIPE
        p = Popen([sys.executable, "main.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        out, _ = p.communicate(inp)
        return out.strip()

    # minimal
    assert exec_run("1\n1 1\n") == "1"

    # sample-like increasing
    assert exec_run("3\n1 1\n3 3\n5 5\n") == "3"

    # all too small except first
    assert exec_run("3\n1 1\n1 1\n1 1\n") == "1"

    # mixed sizes
    assert exec_run("4\n2 2\n6 6\n4 4\n1 1\n") == "3"

    # large but insufficient chain
    assert exec_run("2\n10 10\n100 100\n") == "2"

test()
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 brick | 1 | minimum case |
| strictly increasing | 3 | full greedy progression |
| all small | 1 | early termination |
| mixed sizes | 3 | skipping logic |
| large chain | 2 | correct monotonic matching |

## Edge Cases

One edge case is when many bricks are too small for early requirements. For input:

```
5
1 1
1 1
10 10
10 10
10 10
```

Requirements are $1, 3, 5, \dots$. The algorithm consumes the first $1 \times 1$, then skips the next $1 \times 1$, and correctly uses larger bricks for later layers. The skip loop ensures we do not mistakenly assign a small brick to a large requirement.

Another case is when large bricks appear early. For:

```
3
10 10
3 3
1 1
```

Sorting produces [1, 3, 10]. The algorithm uses 1 for level 1, 3 for level 2, 10 for level 3. Even though a large brick appears first in input, sorting prevents wasting it early, preserving feasibility for higher layers.
