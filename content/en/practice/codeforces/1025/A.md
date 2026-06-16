---
title: "CF 1025A - Doggo Recoloring"
description: "We are given a string representing the colors of a line of puppies, where each character is a color from 'a' to 'z'. The goal is to determine whether we can transform this string so that all characters become the same, using a very specific operation."
date: "2026-06-16T21:41:58+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1025
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 505 (rated, Div. 1 + Div. 2, based on VK Cup 2018 Final)"
rating: 900
weight: 1025
solve_time_s: 133
verified: true
draft: false
---

[CF 1025A - Doggo Recoloring](https://codeforces.com/problemset/problem/1025/A)

**Rating:** 900  
**Tags:** implementation, sortings  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string representing the colors of a line of puppies, where each character is a color from 'a' to 'z'. The goal is to determine whether we can transform this string so that all characters become the same, using a very specific operation.

The operation allows us to pick a color x only if it currently appears at least twice, and then recolor every occurrence of x into some other color y of our choice. We can repeat this operation any number of times.

What matters is not the exact sequence of recolorings, but whether we can eventually eliminate all but one color class.

The key constraint is that a color becomes usable for recoloring only when it has frequency at least 2. A color that appears once can never be chosen directly as a source of recoloring, so singletons behave like “locked” elements unless they are absorbed indirectly by other operations.

With n up to 100,000, any solution must run in linear time or near-linear time. This immediately rules out simulation of operations or repeated scanning of the string after each recoloring, since those could degrade to O(n²) in adversarial cases.

A subtle corner case arises when all characters are distinct. For example, `abcdef`. Every color appears once, so no operation can be performed. The answer is clearly "No".

Another corner case is when all characters are already identical, like `aaaaa`. Here we need no operations at all, so the answer is "Yes".

A more interesting case is when there is exactly one color with frequency greater than one and all others are singletons, such as `aab`. Even though one color is usable, there are colors that can never be eliminated because no other color has enough frequency to be selected as a source in a chain of recolorings.

## Approaches

The brute-force interpretation would try to simulate operations. At each step, we would scan the string, pick any color with frequency at least two, and recolor all its occurrences into another color. After each operation we would recompute frequencies and repeat until either all characters are equal or no operation is possible.

This works in principle because it directly follows the rules, but each step requires recomputing frequencies over the entire string, and we may perform up to O(n) operations. Each recomputation costs O(n), so the worst-case complexity becomes O(n²), which is too slow for n = 100,000.

The key observation is that the operation does not depend on positions, only on frequency counts. The process can be thought of as repeatedly merging color classes, but only classes of size at least two can initiate merges.

This leads to a much simpler invariant: if there exists at least one color that appears more than once, then we can use it as a “collector” color and eventually absorb all other colors into it, because once we choose a target color y, it does not need to satisfy any constraint when receiving elements. The only requirement is having at least one source color with frequency ≥ 2 at every step until all merges are complete.

Thus, the only situation where we are stuck is when no color has frequency ≥ 2 at the start. In that case, no operation can ever be performed, so we can never unify the string unless it is already uniform.

So the problem reduces to a simple check: if the string already has one distinct character, answer "Yes". Otherwise, check whether any character frequency is at least 2. If yes, answer "Yes", otherwise "No".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Frequency Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by analyzing frequency structure of the string.

1. Count the frequency of each character from 'a' to 'z'. This captures all information relevant to the operation, since positions do not matter.
2. Check how many distinct characters exist. If there is exactly one, the string is already uniform, so no operation is needed and we can immediately return "Yes". This works because the target condition is already satisfied.
3. If there are multiple distinct characters, scan whether any character appears at least twice. If such a character exists, we return "Yes" because it can serve as a valid source for at least one operation.
4. If no character has frequency ≥ 2, return "No". In this situation every character is unique, so no operation can ever be applied, and no merging process can begin.

### Why it works

The crucial property is that the only way to change the configuration is through selecting a source color with frequency at least two. If no such color exists, the system is completely frozen. If at least one exists, we can always use it to absorb other colors because the destination color has no restrictions. This means a single “active” color class is sufficient to drive the system toward full unification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    freq = [0] * 26
    for ch in s:
        freq[ord(ch) - 97] += 1

    distinct = sum(1 for x in freq if x > 0)
    if distinct == 1:
        print("Yes")
        return

    for x in freq:
        if x >= 2:
            print("Yes")
            return

    print("No")

if __name__ == "__main__":
    solve()
```

The frequency array compresses the entire input into constant-size state since only 26 characters exist. The check for `distinct == 1` handles the already uniform case directly. The second loop detects whether any valid operation can start; without such a starter, no transformation is possible.

No ordering issues arise because we never simulate operations, only test existence conditions.

## Worked Examples

### Example 1

Input: `aabddc`

Frequencies evolve as follows:

| Step | Frequencies (non-zero) | Distinct colors | Any freq ≥ 2 | Decision |
| --- | --- | --- | --- | --- |
| Initial | a:2, b:1, d:2, c:1 | 4 | Yes | Yes |

We immediately observe multiple duplicates, so at least one valid source exists. The system can start merging, eventually collapsing all colors into one.

### Example 2

Input: `abcd`

| Step | Frequencies (non-zero) | Distinct colors | Any freq ≥ 2 | Decision |
| --- | --- | --- | --- | --- |
| Initial | a:1, b:1, c:1, d:1 | 4 | No | No |

No character appears twice, so no operation is possible. Since the string is not already uniform, we are stuck.

The trace shows the key failure mode: absence of any usable source prevents even the first transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute frequencies plus constant scan over 26 letters |
| Space | O(1) | Fixed-size frequency array of length 26 |

The solution easily fits within limits since n is at most 100,000 and all operations are linear with very small constants.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        solve()
    return output.getvalue().strip()

# provided samples
assert run("6\naabddc\n") == "Yes"
assert run("4\nabcd\n") == "No"

# custom cases
assert run("1\na\n") == "Yes"          # single character
assert run("5\naaaaa\n") == "Yes"      # already uniform
assert run("3\nabc\n") == "No"         # all distinct
assert run("4\naabc\n") == "Yes"       # one duplicate enables process
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 a` | Yes | Minimum size |
| `aaaaa` | Yes | Already uniform |
| `abc` | No | No duplicates exist |
| `aabc` | Yes | Single valid source exists |

## Edge Cases

For the input `a`, the frequency array contains a single non-zero entry. The algorithm detects `distinct == 1` and immediately returns "Yes", correctly handling the trivial case.

For `abcd`, all frequencies are 1. The algorithm skips the first condition and finds no `freq >= 2`, returning "No", matching the fact that no operation can be performed.

For `aab`, frequencies are `a:2, b:1`. The algorithm detects a valid source and returns "Yes", reflecting that the presence of a single duplicable color is sufficient to drive the transformation process.
