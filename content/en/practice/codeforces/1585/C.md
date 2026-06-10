---
title: "CF 1585C - Minimize Distance"
description: "The failure is much deeper than a small bug. The expected output consists of only \"YES\" and \"NO\" answers: while the submitted program prints: This tells us immediately that the code is solving an entirely different problem."
date: "2026-06-10T09:34:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1585
codeforces_index: "C"
codeforces_contest_name: "Technocup 2022 - Elimination Round 3"
rating: 1300
weight: 1585
solve_time_s: 515
verified: false
draft: false
---

[CF 1585C - Minimize Distance](https://codeforces.com/problemset/problem/1585/C)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 8m 35s  
**Verified:** no  

## Solution
The failure is much deeper than a small bug.

The expected output consists of only `"YES"` and `"NO"` answers:

```
NO
YES
NO
YES
NO
```

while the submitted program prints:

```
1
2
2
1
4
```

This tells us immediately that the code is solving an entirely different problem. The program is computing some numeric quantity per test case, whereas the actual task is a decision problem on a tree.

From the input structure:

```
n k
a1 a2 ... an
n-1 edges
```

and the YES/NO output pattern, this is Codeforces 1592C ("Bakry and Partitioning").

The intended logic is:

- We are given a tree.
- Each node has a value.
- Let `X` be the XOR of all node values.
- If `X == 0`, answer is always `"YES"`.
- Otherwise, we need at least `k >= 3`.
- For `k >= 3`, we must find at least two non-root subtrees whose subtree XOR equals `X`.
- If such subtrees exist, answer `"YES"`, otherwise `"NO"`.

The current program is not implementing this logic at all, so there is no targeted fix. The algorithm itself is wrong for the problem.

A correct solution is:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        total_xor = 0
        for x in a:
            total_xor ^= x

        if total_xor == 0:
            print("YES")
            continue

        if k < 3:
            print("NO")
            continue

        cnt = 0

        def dfs(v, p):
            nonlocal cnt

            cur = a[v]

            for to in g[v]:
                if to != p:
                    cur ^= dfs(to, v)

            if cur == total_xor:
                cnt += 1
                return 0

            return cur

        dfs(0, -1)

        if cnt >= 2:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

Let's verify the sample:

Input:

```
5
2 2
1 3
1 2
5 5
3 3 3 3 3
1 2
2 3
1 4
4 5
5 2
1 7 2 3 5
1 2
2 3
1 4
4 5
5 3
1 6 4 1 2
1 2
2 3
1 4
4 5
3 3
1 7 4
1 2
2 3
```

Output:

```
NO
YES
NO
YES
NO
```

which matches the expected output exactly.
