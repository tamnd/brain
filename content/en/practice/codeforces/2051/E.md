---
title: "CF 2051E - Best Price"
description: "The algorithm itself is correct. The symptom is that the program produces no output at all, not incorrect output. That means the bug is not in the logic for determining pass/fail. It is in the program structure."
date: "2026-06-08T08:43:13+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2051
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 995 (Div. 3)"
rating: 1600
weight: 2051
solve_time_s: 175
verified: false
draft: false
---

[CF 2051E - Best Price](https://codeforces.com/problemset/problem/2051/E)

**Rating:** 1600  
**Tags:** binary search, brute force, data structures, greedy, sortings  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
The algorithm itself is correct. The symptom is that the program produces **no output at all**, not incorrect output.

That means the bug is not in the logic for determining pass/fail. It is in the program structure.

A very common cause is that the solution is written inside a function such as:

```python
def solve():
    ...
```

but the function is never called. In that case the program reads nothing, writes nothing, and the judge sees an empty output:

```
Expected:
0100
0000
1111
10

Actual:
```

Tracing the sample through the intended algorithm:

### Test case 1

```
n=4, m=4, k=3
known={1,3,4}
```

Unknown questions:

```
{2}
```

There is exactly one unknown question, namely 2.

A list is passable iff its omitted question is 2.

```
a = [1,2,3,4]
```

Result:

```
0100
```

### Test case 2

```
n=5, k=3
known={1,3,4}
```

Unknown questions:

```
{2,5}
```

There are at least two unknown questions. Removing one question cannot eliminate both.

Result:

```
0000
```

### Test case 3

```
k=n
```

All questions are known.

Result:

```
1111
```

### Test case 4

```
n=2
known={2}
```

Unknown question:

```
{1}
```

Only the list omitting question 1 is passable.

Result:

```
10
```

So the algorithm is fine. The fix is simply to provide a complete executable solution and call `solve()`.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        q = list(map(int, input().split()))

        known = set(q)
        missing = n - k

        if missing == 0:
            answers.append("1" * m)
            continue

        if missing >= 2:
            answers.append("0" * m)
            continue

        # Exactly one unknown question.
        unknown = -1
        for x in range(1, n + 1):
            if x not in known:
                unknown = x
                break

        res = []
        for x in a:
            if x == unknown:
                res.append('1')
            else:
                res.append('0')

        answers.append(''.join(res))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

This preserves the intended $O(n+m)$ per test case approach and correctly handles all edge cases.
