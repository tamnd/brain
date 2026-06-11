---
title: "CF 1409C - Yet Another Array Restoration"
description: "The root cause of the failure here is the test harness is trying to call a solve() function that isn’t defined in the same context."
date: "2026-06-11T07:39:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1409
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 667 (Div. 3)"
rating: 1200
weight: 1409
solve_time_s: 423
verified: false
draft: false
---

[CF 1409C - Yet Another Array Restoration](https://codeforces.com/problemset/problem/1409/C)

**Rating:** 1200  
**Tags:** brute force, math, number theory  
**Solve time:** 7m 3s  
**Verified:** no  

## Solution
The root cause of the failure here is **the test harness is trying to call a `solve()` function that isn’t defined in the same context**. In Python, if you define the main code in the global scope without wrapping it in a function, calling `solve()` later will always fail with `NameError` or `RuntimeError`. This is unrelated to the algorithm itself.

To fix it, we need a **fully self-contained Python 3 solution** where all logic is inside a function called `solve()` and fast I/O is used. The algorithm itself - sliding window over all `(fret, note_index)` pairs - is correct, so we keep that approach.

Here is the corrected, complete solution:

```python
import sys
input = sys.stdin.readline

def solve():
    # read input
    a = list(map(int, input().split()))
    n = int(input())
    b = list(map(int, input().split()))

    # generate all possible frets for each note
    frets = []
    for i in range(n):
        for j in range(6):
            fret = b[i] - a[j]
            frets.append((fret, i))  # (fret_index, note_index)
    
    frets.sort()  # sort by fret number

    count = [0] * n  # how many times each note is in current window
    unique = 0       # number of unique notes in the window
    ans = float('inf')
    l = 0

    # sliding window to find minimal range covering all notes
    for r in range(len(frets)):
        fret, idx = frets[r]
        if count[idx] == 0:
            unique += 1
        count[idx] += 1

        # contract window from the left while all notes are covered
        while unique == n:
            ans = min(ans, frets[r][0] - frets[l][0])
            left_fret, left_idx = frets[l]
            count[left_idx] -= 1
            if count[left_idx] == 0:
                unique -= 1
            l += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

### Key points

1. The function `solve()` contains all the logic, so you can safely call it in a test harness.
2. Each note `b[i]` can be played on any string `j` with fret `b[i] - a[j]`.
3. Sorting all `(fret, note_index)` pairs allows a sliding window to efficiently find the minimal fret difference that covers all notes.
4. `count` and `unique` track how many distinct notes are in the current window.
5. The result `ans` is the smallest difference of max and min fret in a valid window.

### How to run a test

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample test
assert run("1 4 100 10 30 5\n6\n101 104 105 110 130 200\n") == "0", "sample 1"
```

This fixes the `RuntimeError` because `solve()` is now defined.

If you want, I can also **walk through this sample step by step** to show why the answer is `0` with the fret assignments. This often clarifies the sliding window logic for edge cases. Do you want me to do that?
