---
title: "CF 78B - Easter Eggs"
description: "We need to construct a circular coloring of n eggs using exactly seven possible colors: R, O, Y, G, B, I, and V. Two conditions must hold at the same time."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 1200
weight: 78
solve_time_s: 130
verified: false
draft: false
---

[CF 78B - Easter Eggs](https://codeforces.com/problemset/problem/78/B)

**Rating:** 1200  
**Tags:** constructive algorithms, implementation  
**Solve time:** 2m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct a circular coloring of `n` eggs using exactly seven possible colors: `R`, `O`, `Y`, `G`, `B`, `I`, and `V`.

Two conditions must hold at the same time. Every color must appear at least once, and every group of four consecutive eggs around the circle must contain four distinct colors. Since the eggs form a circle, the last eggs connect back to the first ones.

The input is just a single integer `n`, the number of eggs. The output is any valid string of length `n` where each character represents the color of one egg in clockwise order.

The constraints are very small. `n` is at most `100`, so even a brute-force search is technically possible. A complete search over all colorings would still explode quickly because there are `7^n` possible strings. For `n = 100`, that is completely infeasible. On the other hand, a linear construction is trivial within the limits. Any `O(n)` or `O(n^2)` approach is comfortably fast.

The tricky part is understanding what the “every four consecutive eggs are different” condition actually implies. A careless solution might only check adjacent eggs or might forget that the arrangement is circular.

Consider `n = 8`. A naive repetition like:

```
ROYGBIVR
```

fails. The last four eggs are `BIVR`, which are distinct, but the circular segment crossing the boundary contains `VRRO`, where `R` repeats.

Another common mistake is repeating all seven colors in order forever:

```
ROYGBIVROYGBIV...
```

This fails for some circular lengths because the suffix and prefix can create duplicate colors inside a length-4 window.

For example, with `n = 10`:

```
ROYGBIVROY
```

the circular segment `YROY` contains two `Y` characters.

The construction must account for the wraparound windows as well, not just the windows inside the string.

## Approaches

A brute-force approach would try to assign colors one by one and check whether the current partial sequence violates the rules. Since there are seven choices for every position, the search space is exponential. Even pruning aggressively, the worst case still grows far too quickly.

The reason brute force works conceptually is that the validity condition is local. To verify a coloring, we only need to inspect consecutive groups of four eggs. The problem is that constructing a valid sequence by trial and error wastes time rediscovering the same patterns.

The key observation is that the condition “every four consecutive eggs are distinct” is already satisfied by a repeating pattern of four distinct colors. If we repeatedly use only `R`, `O`, `Y`, and `G`, then every length-4 block is exactly those four colors in some rotation.

The second observation is that we still must use all seven colors at least once. The simplest way to achieve that is to start with the fixed sequence:

```
ROYGBIV
```

This already uses all colors once and satisfies the condition for every internal length-4 segment.

Now we only need to append extra characters for the remaining `n - 7` positions. We can safely repeat the pattern:

```
GBIV
```

Why this particular suffix works is the important insight. The last four characters of `ROYGBIV` are already `GBIV`. Repeating this block preserves the “all distinct in every window of size four” property across boundaries.

For example:

```
ROYGBIVGBIVGBIV...
```

Any consecutive block of four characters is some rotation of `GBIV`.

This gives a direct linear construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(7^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with the base string `"ROYGBIV"`.

This guarantees that all seven colors appear at least once.
2. Compute how many additional eggs still need colors.

Let:

```
remaining = n - 7
```
3. Prepare the repeating extension `"GBIV"`.

This pattern preserves the property that every four consecutive eggs are different, even across concatenation boundaries.
4. Append characters from `"GBIV"` cyclically until the total length becomes `n`.

For example, if `remaining = 5`, append:

```
GBIVG
```
5. Print the final string.

### Why it works

The first seven characters use every color exactly once, so the first requirement is satisfied immediately.

The repeating suffix only uses the pattern `GBIV`. Every consecutive block of four characters inside this repetition is exactly the set `{G, B, I, V}` in some order, so all four are distinct.

The boundary between `"ROYGBIV"` and the repeated suffix is also safe because the original string already ends with `"GBIV"`. Appending another `"GBIV"` simply continues the same valid cycle.

Since every length-4 window contains four distinct colors, the circular condition also holds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    ans = "ROYGBIV"
    extra = "GBIV"

    remaining = n - 7

    for i in range(remaining):
        ans += extra[i % 4]

    print(ans)

solve()
```

The solution begins with the fixed valid base `"ROYGBIV"`. This is the smallest sequence that already contains every required color exactly once.

The variable `remaining` stores how many more positions must be filled. Those positions are generated using the repeating block `"GBIV"`.

The modulo operation `i % 4` cycles through the characters of `"GBIV"` repeatedly. Since the extension length can be any value from `0` to `93`, this avoids boundary issues cleanly.

One subtle point is choosing the correct repeating block. Repeating `"ROYG"` would not always work because the transition from the suffix back to the prefix could create repeated colors in a length-4 window. The block `"GBIV"` works specifically because it matches the ending of the initial valid sequence.

## Worked Examples

### Example 1

Input:

```
8
```

Initial state:

```
ROYGBIV
```

We still need one more character.

| Step | remaining index | appended char | current answer |
| --- | --- | --- | --- |
| Start | - | - | ROYGBIV |
| 1 | 0 | G | ROYGBIVG |

Final output:

```
ROYGBIVG
```

Every consecutive block of four characters contains distinct colors. The circular windows also remain valid.

### Example 2

Input:

```
12
```

Initial state:

```
ROYGBIV
```

We need five additional characters.

| Step | remaining index | appended char | current answer |
| --- | --- | --- | --- |
| Start | - | - | ROYGBIV |
| 1 | 0 | G | ROYGBIVG |
| 2 | 1 | B | ROYGBIVGB |
| 3 | 2 | I | ROYGBIVGBI |
| 4 | 3 | V | ROYGBIVGBIV |
| 5 | 4 | G | ROYGBIVGBIVG |

Final output:

```
ROYGBIVGBIVG
```

This example demonstrates the cyclic repetition of `"GBIV"`. Every new character extends the existing valid pattern without breaking any length-4 window.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We append exactly `n - 7` characters |
| Space | O(n) | The output string itself has length `n` |

The maximum value of `n` is only `100`, so this linear solution runs instantly and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    ans = "ROYGBIV"
    extra = "GBIV"

    for i in range(n - 7):
        ans += extra[i % 4]

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("8\n") == "ROYGBIVG\n", "sample 1"

# minimum size
assert run("7\n") == "ROYGBIV\n", "minimum n"

# exact repetition boundary
assert run("11\n") == "ROYGBIVGBIV\n", "full GBIV cycle"

# one past repetition boundary
assert run("12\n") == "ROYGBIVGBIVG\n", "partial cycle"

# maximum size
out = run("100\n").strip()
assert len(out) == 100, "maximum n length"

# verify all windows of size 4 are distinct
s = out
n = len(s)

for i in range(n):
    window = [s[(i + j) % n] for j in range(4)]
    assert len(set(window)) == 4, "window condition failed"

# verify all seven colors appear
assert set("ROYGBIV").issubset(set(out)), "missing colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `ROYGBIV` | Smallest valid size |
| `8` | `ROYGBIVG` | First repeated character |
| `11` | `ROYGBIVGBIV` | Exact full repetition block |
| `12` | `ROYGBIVGBIVG` | Partial repetition cycle |
| `100` | Any valid length-100 string | Maximum constraint and circular validation |

## Edge Cases

The smallest possible input is:

```
7
```

The algorithm immediately returns:

```
ROYGBIV
```

No extra characters are appended. Every consecutive group of four characters is distinct, and all seven colors appear exactly once.

Another subtle case is when the remaining length is not divisible by four.

Input:

```
10
```

The algorithm builds:

```
ROYGBIVGBI
```

The appended suffix is only `"GBI"`, not a full cycle. This still works because every length-4 window crossing the boundary remains distinct:

```
VGBI
BGIV
```

A careless implementation that repeated the wrong pattern could fail exactly in these partial-cycle cases.

The maximum input:

```
100
```

also works safely because the construction never depends on backtracking or recursion. The algorithm simply extends the valid periodic structure until the target length is reached.
