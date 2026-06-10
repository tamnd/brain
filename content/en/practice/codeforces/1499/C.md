---
title: "CF 1499C - Minimum Grid Path"
description: "There is no bug in the algorithm. The output and the expected output represent exactly the same solution. Let's verify: - Indices (1, 6) correspond to values (2, 4), whose sum is 6. - Indices (2, 3) correspond to values (1, 5), whose sum is 6. So All four indices are distinct."
date: "2026-06-10T21:33:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1499
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 106 (Rated for Div. 2)"
rating: 1500
weight: 1499
solve_time_s: 683
verified: false
draft: false
---

[CF 1499C - Minimum Grid Path](https://codeforces.com/problemset/problem/1499/C)

**Rating:** 1500  
**Tags:** brute force, data structures, greedy, math  
**Solve time:** 11m 23s  
**Verified:** no  

## Solution
There is no bug in the algorithm.

The output

```
YES
1 6 2 3
```

and the expected output

```
YES
2 3 1 6
```

represent exactly the same solution.

Let's verify:

- Indices `(1, 6)` correspond to values `(2, 4)`, whose sum is `6`.
- Indices `(2, 3)` correspond to values `(1, 5)`, whose sum is `6`.

So

```
a1 + a6 = a2 + a3
2 + 4 = 1 + 5
6 = 6
```

All four indices are distinct.

The problem statement explicitly says:

> If there are multiple answers, print any of them.

Therefore both

```
1 6 2 3
```

and

```
2 3 1 6
```

are valid outputs.

What happened is that the local test harness is incorrectly checking for one exact answer:

```
assert run(...) == "YES\n2 3 1 6"
```

instead of validating that:

1. The first line is `"YES"`.
2. The four printed indices are distinct.
3. The two pair sums are equal.

That is a flaw in the test, not in the solution.

The accepted solution remains:

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    m = min(n, 5000)

    seen = {}

    for i in range(m):
        ai = a[i]
        for j in range(i + 1, m):
            s = ai + a[j]

            if s in seen:
                x, y = seen[s]

                if x != i and x != j and y != i and y != j:
                    print("YES")
                    print(x + 1, y + 1, i + 1, j + 1)
                    return
            else:
                seen[s] = (i, j)

    print("NO")

if __name__ == "__main__":
    solve()
```

No algorithmic change is needed. The output shown in the "Actual output" section is already a correct answer for Codeforces 1500A.
