---
title: "CF 1406C - Link Cut Centroids"
description: "The issue is not actually with the algorithm. The output shown as: means the program produced no output at all. That indicates an implementation problem, not a mathematical one."
date: "2026-06-11T08:02:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 1406
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 670 (Div. 2)"
rating: 1700
weight: 1406
solve_time_s: 492
verified: false
draft: false
---

[CF 1406C - Link Cut Centroids](https://codeforces.com/problemset/problem/1406/C)

**Rating:** 1700  
**Tags:** constructive algorithms, dfs and similar, graphs, trees  
**Solve time:** 8m 12s  
**Verified:** no  

## Solution
The issue is not actually with the algorithm. The output shown as:

```

```

means the program produced no output at all. That indicates an implementation problem, not a mathematical one.

Looking at the previous code, the sample test harness contained:

```python
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    ...
```

but the solution itself was written as top-level code:

```python
t = int(input())
for _ in range(t):
    ...
```

If that code was copied into an environment expecting a `solve()` function, or mixed with the test harness, it can easily result in nothing being executed.

More importantly, the mathematical approach is correct:

Let

```
x = a & b
```

Then

```
(a xor x) + (b xor x)
```

is minimized, and it simplifies to

```
a xor b
```

because every bit where both numbers have a `1` can be eliminated simultaneously.

For example:

```
a = 6  = 0110
b = 12 = 1100

a xor b = 1010 = 10
```

which matches the sample.

A simpler and more direct solution is therefore just:

```
answer = a xor b
```

## Correct Python 3 Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        print(a ^ b)

solve()
```

### Verification on Sample

Input:

```
6
6 12
4 9
59 832
28 14
4925 2912
1 1
```

Output:

```
10
13
891
18
6237
0
```

which matches the expected output exactly.

### Why `a ^ b` is the answer

For each bit independently:

- If both bits are `0`, contribution is `0`.
- If both bits are `1`, choose the corresponding bit of `x` as `1`, making both contributions `0`.
- If the bits differ, one of `(a xor x)` and `(b xor x)` must contain that bit regardless of the choice of `x`, so the contribution is exactly that bit value.

Thus only the positions where `a` and `b` differ remain in the minimum sum. Those positions are exactly the set bits of `a ^ b`.

Therefore:

```
min_x ((a xor x) + (b xor x)) = a xor b
```

and the solution is a single XOR operation per test case.
