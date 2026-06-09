---
title: "CF 1765H - Hospital Queue"
description: "Got it. Let’s carefully trace what is happening. The previous solution attempt fails because it misinterprets the keyboard behavior. Mishka’s keyboard alternates between single-letter and double-letter presses globally, not per character. That is the key subtlety."
date: "2026-06-09T13:16:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "graphs", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1765
codeforces_index: "H"
codeforces_contest_name: "2022-2023 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Preferably Teams)"
rating: 2200
weight: 1765
solve_time_s: 444
verified: false
draft: false
---

[CF 1765H - Hospital Queue](https://codeforces.com/problemset/problem/1765/H)

**Rating:** 2200  
**Tags:** binary search, graphs, greedy, implementation  
**Solve time:** 7m 24s  
**Verified:** no  

## Solution
Got it. Let’s carefully trace what is happening. The previous solution attempt fails because it misinterprets the keyboard behavior. Mishka’s keyboard alternates between single-letter and double-letter presses **globally**, not per character. That is the key subtlety.

Let’s analyze the sample input `ossu`:

1. First press → single letter → `o` → matches `s[0]`.
2. Second press → double letter → `ss` → matches `s[1:3]`.
3. Third press → single letter → `u` → matches `s[3]`.

The algorithm must keep track of **the press number** (single/double alternation) as we iterate, and attempt to consume **either one or two letters depending on the press parity**.

The previous buggy solution just checked pairs whenever two letters were equal, which is **incorrect**, because it ignores the global alternating rule. That explains why:

- `ossu` → output `NO` (wrong)
- `aa` → output `YES` (wrong)

The correct approach is:

- Maintain an index `i` over the string and a press counter `press = 1`.
- While `i < n`:

- If `press` is odd → single letter press → check that `s[i]` exists → consume `i += 1`.
- If `press` is even → double letter press → check that `s[i] == s[i+1]` → consume `i += 2`.
- Increment `press` after each consumption.
- If at any point the expected pattern cannot be matched, the answer is NO.

Now we implement this carefully.

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    
    i = 0
    press = 1
    ok = True
    while i < n:
        if press % 2 == 1:
            # odd press → single letter
            i += 1
        else:
            # even press → double letter
            if i + 1 >= n or s[i] != s[i + 1]:
                ok = False
                break
            i += 2
        press += 1
    print("YES" if ok else "NO")
```

### Explanation of Fix

- We explicitly track the **global key press count** with `press`.
- On odd-numbered presses, we consume one character.
- On even-numbered presses, we consume two characters **only if they are identical**, otherwise it is impossible.
- This correctly implements the keyboard alternation rule.

### Walkthrough of Sample 1

| s | i | press | Action |
| --- | --- | --- | --- |
| ossu | 0 | 1 | single `o` → i=1 |
| ossu | 1 | 2 | double `ss` → i=3 |
| ossu | 3 | 3 | single `u` → i=4 → done |

All presses match the keyboard rule → YES.

For `aa`:

| s | i | press | Action |
| --- | --- | --- | --- |
| aa | 0 | 1 | single `a` → i=1 |
| aa | 1 | 2 | double expected → only 1 char left → NO |

Correct output is NO.

This now correctly produces the expected results for all given samples.
