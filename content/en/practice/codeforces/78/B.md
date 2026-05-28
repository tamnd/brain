---
title: "CF 78B - Easter Eggs"
description: "We need to build a circular sequence of colors for n eggs. There are exactly seven available colors: R, O, Y, G, B, I, V Two conditions must hold simultaneously. First, every color must appear at least once."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 1200
weight: 78
solve_time_s: 119
verified: false
draft: false
---

[CF 78B - Easter Eggs](https://codeforces.com/problemset/problem/78/B)

**Rating:** 1200  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We need to build a circular sequence of colors for `n` eggs. There are exactly seven available colors:

`R, O, Y, G, B, I, V`

Two conditions must hold simultaneously.

First, every color must appear at least once.

Second, every block of four consecutive eggs on the circle must contain four distinct colors. Since the eggs form a circle, the sequence wraps around. The last eggs and the first eggs are also neighbors.

The input is just one integer `n`, the number of eggs. The output is any valid coloring string of length `n`.

The constraints are very small. `n` is at most `100`, so even fairly inefficient approaches would run comfortably within the time limit. A brute-force backtracking solution over all color assignments is theoretically possible for such a small limit, but the branching factor is still large enough that it becomes messy and unnecessary. The problem is actually constructive, there is a simple pattern that always works.

The tricky part is the circular condition. A sequence that works linearly may fail after wrapping around. For example:

```
ROYGBIVR
```

looks fine if checked only left-to-right, but the last three characters plus the first one form:

```
IVRR
```

which repeats `R`.

Another common mistake is using all seven colors once and then repeating from the start:

```
ROYGBIVROY...
```

This fails because some windows of four contain repeated colors near the joining point.

For example, with `n = 8`:

```
ROYGBIVR
```

the four consecutive eggs across the boundary are:

```
V R R O
```

Two `R`s appear.

The key observation is that we do not actually need all seven colors in every local window. We only need every group of four consecutive eggs to be pairwise distinct. A carefully chosen repeating suffix can satisfy that condition indefinitely.

## Approaches

A brute-force solution would try assigning one of seven colors to each egg while checking whether the current partial sequence violates the "four consecutive distinct" rule. At the end, it would also verify that all seven colors were used and that the circular wrap-around windows are valid.

This works because the constraints are tiny, but the search space is still exponential. In the worst case we explore roughly `7^n` possibilities, which is astronomically large even for moderate `n`. Pruning helps, but the approach is still unnecessarily complicated for a problem intended to be constructive.

The real insight comes from studying the condition on four consecutive eggs. If we already have a valid repeating pattern where every adjacent block of four contains different letters, then repeating that pattern forever remains valid.

The standard rainbow sequence:

```
ROYGBIV
```

already satisfies the condition. The problem appears when we continue repeating it from the beginning because the circular overlap introduces duplicates.

Instead of repeating the whole seven-letter pattern, we only repeat a suffix that maintains the four-distinct property. The sequence:

```
GBIV
```

can repeat forever because every consecutive block of four inside that repetition is exactly some rotation of distinct letters.

So the construction becomes:

1. Start with `"ROYGBIV"` to guarantee all seven colors appear.
2. For every extra position, append characters cyclically from `"GBIV"`.

Example for `n = 10`:

```
ROYGBIVGBI
```

Every four consecutive characters remain distinct, including across the circular boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(7^n) | O(n) | Too slow conceptually |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create the base string:

```
ROYGBIV
```

This immediately guarantees that every color appears at least once.

1. Compute how many additional characters are needed.

```
extra = n - 7
```

1. Use the repeating pattern:

```
GBIV
```

This pattern is chosen because every consecutive block of four characters inside repeated copies remains distinct.

1. Append characters from `"GBIV"` cyclically until the total length becomes `n`.

If `extra = 5`, we append:

```
GBIVG
```

1. Print the final string.

### Why it works

The first seven characters contain all seven colors exactly once, so the first condition is satisfied immediately.

The repeating suffix `"GBIV"` has length four and all four characters are distinct. Any consecutive block of four inside repeated copies of this pattern is just a cyclic shift of those same four letters, so no repetition appears.

The boundary between `"ROYGBIV"` and the appended suffix also works because the last few characters of the base already align naturally with `"GBIV"`.

As a result, every circular window of four consecutive eggs contains four distinct colors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    base = "ROYGBIV"
    extra_pattern = "GBIV"
    
    ans = base
    
    for i in range(n - 7):
        ans += extra_pattern[i % 4]
    
    print(ans)

solve()
```

The solution begins with the mandatory seven-color sequence. That part is fixed because the problem requires every color to appear at least once.

The remaining positions are filled using `"GBIV"` cyclically. The modulo operation handles wrapping inside that four-character pattern.

A subtle detail is that we append only after the first seven characters. Repeating the entire seven-letter rainbow would break the circular condition near the boundary.

Another important detail is that the answer length must become exactly `n`. Since the loop runs `n - 7` times, the final length is correct without extra checks.

## Worked Examples

### Example 1

Input:

```
8
```

Construction steps:

| Step | Current Answer | Added Character |
| --- | --- | --- |
| Initial | ROYGBIV | - |
| 1 | ROYGBIVG | G |

Final output:

```
ROYGBIVG
```

This example shows the smallest case where an extra character must be appended. The added `G` continues the safe repeating structure without breaking any four-character window.

### Example 2

Input:

```
12
```

Construction steps:

| Step | Current Answer | Added Character |
| --- | --- | --- |
| Initial | ROYGBIV | - |
| 1 | ROYGBIVG | G |
| 2 | ROYGBIVGB | B |
| 3 | ROYGBIVGBI | I |
| 4 | ROYGBIVGBIV | V |
| 5 | ROYGBIVGBIVG | G |

Final output:

```
ROYGBIVGBIVG
```

This trace demonstrates the cyclic repetition of `"GBIV"`. Every group of four consecutive characters remains distinct because the suffix itself is a four-character cycle of distinct letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We append exactly `n` characters overall |
| Space | O(n) | The output string stores `n` characters |

With `n ≤ 100`, this solution is easily within both the time and memory limits. The implementation performs only simple string operations and a single loop.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())
    
    base = "ROYGBIV"
    extra_pattern = "GBIV"
    
    ans = base
    
    for i in range(n - 7):
        ans += extra_pattern[i % 4]
    
    print(ans)

def run(inp: str) -> str:
    global input
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    
    solve()
    
    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run("8\n") == "ROYGBIVG", "sample 1"

# minimum size
assert run("7\n") == "ROYGBIV", "minimum n"

# one full extra cycle
assert run("11\n") == "ROYGBIVGBIV", "full GBIV repetition"

# off-by-one after cycle restart
assert run("12\n") == "ROYGBIVGBIVG", "cycle restart"

# maximum size length check
res = run("100\n")
assert len(res) == 100, "maximum size"

# all colors appear
for c in "ROYGBIV":
    assert c in res, "missing color"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `ROYGBIV` | Minimum valid size |
| `8` | `ROYGBIVG` | First appended character |
| `11` | `ROYGBIVGBIV` | Exact full suffix cycle |
| `12` | `ROYGBIVGBIVG` | Correct modulo restart |
| `100` | Length 100 valid string | Maximum constraint |

## Edge Cases

Consider the minimum input:

```
7
```

The algorithm outputs:

```
ROYGBIV
```

Every color appears once, and every group of four consecutive eggs contains distinct colors because all characters are unique.

Now consider the first nontrivial extension:

```
8
```

The construction becomes:

```
ROYGBIVG
```

Checking the circular windows:

```
ROYG
OYGB
YGBI
GBIV
BIVG
IVGR
VGRO
GROY
```

All four-character windows contain distinct letters.

A naive repetition such as:

```
ROYGBIVR
```

would fail because the circular window:

```
IVRR
```

contains repeated `R`.

Another subtle case is when the appended pattern wraps around:

```
12
```

Output:

```
ROYGBIVGBIVG
```

The suffix repeats as:

```
GBIVG
```

Even after restarting at `G`, every block of four consecutive characters remains a permutation of `G, B, I, V`, so the condition continues to hold.
