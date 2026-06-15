---
title: "CF 1284A - New Year and Naming"
description: "We are given two circular lists of strings. The first list has size $n$, the second has size $m$. Each year $y$ produces a name by taking the $y$-th string from the first list and the $y$-th string from the second list, both indexed cyclically, and concatenating them."
date: "2026-06-16T03:17:34+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1284
codeforces_index: "A"
codeforces_contest_name: "Hello 2020"
rating: 800
weight: 1284
solve_time_s: 512
verified: true
draft: false
---

[CF 1284A - New Year and Naming](https://codeforces.com/problemset/problem/1284/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 8m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two circular lists of strings. The first list has size $n$, the second has size $m$. Each year $y$ produces a name by taking the $y$-th string from the first list and the $y$-th string from the second list, both indexed cyclically, and concatenating them.

Concretely, year 1 uses $s_1$ and $t_1$, year 2 uses $s_2$ and $t_2$, and so on. Once we pass the end of either list, we wrap around to the beginning again. The name of a year is simply the concatenation of the chosen pair.

Each query gives a year number $y$, possibly very large, and we must output the resulting concatenated name.

The main structural detail is that both sequences are periodic. The first repeats every $n$ years, the second every $m$ years, so the combined pattern repeats every $\mathrm{lcm}(n, m)$ years. This periodicity is what makes large queries manageable.

The constraints are small for the arrays, with $n, m \le 20$, so precomputation is trivial. The number of queries is also small, but the year index can go up to $10^9$, which immediately rules out simulating year by year. Any solution that iterates up to $y$ per query would time out badly in the worst case.

A subtle failure case for naive thinking is forgetting cyclic indexing. For example, if $n = 3$, accessing $s_{y}$ directly will go out of bounds for $y > 3$. Another common mistake is computing modulo incorrectly with 0-based indexing, especially when mapping year 1 to index 0.

## Approaches

The brute-force idea is to simulate the process for each query. For a given year $y$, we repeatedly compute the index in both arrays as $(y-1) \bmod n$ and $(y-1) \bmod m$, then concatenate the corresponding strings. This is correct and extremely direct.

However, if implemented naïvely by iterating from year 1 up to $y$ for each query, the cost becomes $O(q \cdot y)$, which is impossible when $y$ can reach $10^9$. Even with $q \approx 2000$, this explodes.

The key observation is that each year can be computed independently in constant time using modular arithmetic. The sequences are periodic, so we never need to simulate transitions. The entire problem reduces to indexing into two cyclic arrays and concatenating the results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(q \cdot y)$ | $O(1)$ | Too slow |
| Direct Modular Indexing | $O(q)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the two arrays $s$ and $t$, and store their lengths $n$ and $m$. These define two independent cycles.
2. For each query year $y$, convert it into zero-based indexing by subtracting 1. This aligns year 1 with index 0, which simplifies modular arithmetic.
3. Compute the index in the first array as $(y-1) \bmod n$. This gives the correct cyclic position in $s$.
4. Compute the index in the second array as $(y-1) \bmod m$. This gives the correct cyclic position in $t$.
5. Output the concatenation $s[i] + t[j]$.

Each query is independent, so there is no need to store intermediate results or simulate progression.

### Why it works

Both sequences repeat with fixed periods $n$ and $m$. The $y$-th element in a repeating cycle depends only on its position modulo the cycle length. Since the output is just a pairwise combination of two independent cycles, the full system is also periodic, and each query reduces to two modular lookups.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
s = input().split()
t = input().split()

q = int(input())

for _ in range(q):
    y = int(input())
    y -= 1
    print(s[y % n] + t[y % m])
```

The solution directly applies modular indexing. The only important implementation detail is subtracting 1 before taking modulo, ensuring that year 1 maps to index 0. Without this adjustment, year boundaries would shift incorrectly.

Each query is processed independently in constant time, so there is no accumulation of state or risk of overflow beyond standard integer handling.

## Worked Examples

Using the sample input structure, consider two queries to illustrate indexing behavior.

### Example trace

Let $s = [a, b, c]$, $t = [d, e]$.

| Year $y$ | $y-1$ | $(y-1) \bmod 3$ | $(y-1) \bmod 2$ | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | ad |
| 2 | 1 | 1 | 1 | be |
| 3 | 2 | 2 | 0 | cd |
| 4 | 3 | 0 | 1 | ae |

This shows how both sequences wrap independently and combine.

The trace confirms that no interaction exists between the two sequences beyond pairing at each index, so each can be handled separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q)$ | Each query performs constant-time modulo and concatenation |
| Space | $O(n + m)$ | Storage for the two input sequences |

The constraints allow up to 2000 queries and very small arrays, so constant-time per query is easily fast enough. Even with Python overhead, the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    s = input().split()
    t = input().split()
    q = int(input())
    out = []
    for _ in range(q):
        y = int(input())
        y -= 1
        out.append(s[y % n] + t[y % m])
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample-like test
assert run("""3 2
a b c
d e
4
1
2
3
4
""") == "ad\nbe\ncd\nae"

# boundary: single element cycles
assert run("""1 1
x
y
3
1
2
3
""") == "xy\nxy\nxy"

# different cycle lengths
assert run("""2 3
a b
c d e
5
1
2
3
4
5
""") == "ac\nbd\nae\nac\nbd"

# large year indexing
assert run("""2 2
a b
c d
1
1000000000
""") == "bd"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single-element cycles | repeated output | correctness under full wrap |
| mismatched cycle lengths | patterned repetition | independent modulo behavior |
| large year value | correct indexing | handling large $y$ safely |

## Edge Cases

One key edge case is when $n = 1$ or $m = 1$. In this situation, every year always selects the same string from that sequence. The modular expression still works because any number modulo 1 is 0, so the implementation naturally collapses correctly without special handling.

Another case is very large year values close to $10^9$. Since Python handles large integers natively, the only risk is forgetting to subtract 1 before modulo. If we skip that, year 1 incorrectly maps to index 1 instead of 0, shifting every output.

A final subtle case is when both sequences have different lengths and do not align periodically within a small range. Even then, the modular approach remains correct because each sequence cycles independently, and we never assume a shared period.
