---
title: "CF 1398A - Bad Triangle"
description: "This failure is not caused by the algorithm at all. It is a pure syntax error in the test harness. The traceback says: So the string passed into run() is never closed."
date: "2026-06-11T09:17:31+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1398
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 93 (Rated for Div. 2)"
rating: 800
weight: 1398
solve_time_s: 679
verified: false
draft: false
---

[CF 1398A - Bad Triangle](https://codeforces.com/problemset/problem/1398/A)

**Rating:** 800  
**Tags:** geometry, math  
**Solve time:** 11m 19s  
**Verified:** no  

## Solution
This failure is not caused by the algorithm at all. It is a pure syntax error in the test harness.

The traceback says:

```
SyntaxError: unterminated string literal
assert run("4\n1
```

So the string passed into `run()` is never closed. That means the code that produced this failure is something like:

```
assert run("4\n1
```

instead of a properly closed multiline string such as:

```
assert run("4\n1\n8\n...")
```

Python raises this error before any logic runs, because it parses the file itself and detects that the string literal is incomplete.

### What exactly went wrong

The bug is in the test-case construction:

- A newline inside the string was not escaped or closed properly.
- The closing quote is missing.
- As a result, Python treats everything after `"4\n1` as part of the same string, until EOF, and fails.

This is unrelated to the solution logic for 1401C. There is no evidence that the algorithm for checking divisibility by the minimum or sorting feasibility was executed.

### Correct fix

You must ensure that:

- Every string passed into `run()` is properly closed with `"`.
- Newlines inside test cases are written as `\n`.
- The full input is wrapped correctly.

For example:

```
assert run("4\n1\n8\n") == "YES"
```

or for full samples:

```
assert run("""4
1
8
6
4 3 6 6 2 9
4
4 5 6 7
5
7 5 2 2 4
""") == """YES
YES
YES
NO"""
```

### Correct complete solution (algorithm unchanged)

Below is the correct and clean implementation of the actual problem logic. This is independent of the broken test harness.

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mn = min(a)
        b = sorted(a)

        ok = True
        for i in range(n):
            if a[i] != b[i] and a[i] % mn != 0:
                ok = False
                break

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

### Why this logic is correct (brief recap)

The minimum element acts as the only “connector” for rearrangements. Any value divisible by it can be moved into any position that is also reachable through swaps involving valid GCD conditions. Elements not divisible by the minimum are effectively locked: if they are not already in their sorted position, there is no legal sequence of swaps that can fix them.

So sorting is possible exactly when every misplaced element is divisible by the global minimum.

### Key takeaway

Your runtime failure is purely due to malformed test input strings, not an incorrect algorithm. Fixing the quoting and newline formatting will eliminate the error immediately.
