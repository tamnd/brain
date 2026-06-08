---
title: "CF 2064A - Brogramming Contest"
description: "We start with a binary string s and an empty string t. A move allows us to take any suffix of one string and append it to the other string. Since only suffixes may be moved, the relative order of characters never changes. Characters can only cross the boundary between s and t."
date: "2026-06-08T07:23:08+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2064
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1005 (Div. 2)"
rating: 800
weight: 2064
solve_time_s: 95
verified: true
draft: false
---

[CF 2064A - Brogramming Contest](https://codeforces.com/problemset/problem/2064/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a binary string `s` and an empty string `t`.

A move allows us to take any suffix of one string and append it to the other string. Since only suffixes may be moved, the relative order of characters never changes. Characters can only cross the boundary between `s` and `t`.

The goal is to end with every `0` inside `s` and every `1` inside `t`. We need the minimum number of suffix transfers required to reach that state.

The length of each string is at most 1000, and the total length across all test cases is also at most 1000. Even though the constraints are small, the intended solution is much simpler than any search-based approach. The answer can be computed by scanning the string once.

The tricky part is understanding what a move actually changes. Since only suffixes can be transferred, we cannot rearrange characters arbitrarily. Every move only shifts the boundary between the two strings. The structure of consecutive blocks of equal characters becomes the key observation.

Consider some easy edge cases.

If the string already contains only zeros, such as:

```
s = "00000"
```

then `t` can remain empty. The answer is `0`.

A careless solution that always moves all `1`s into `t` might incorrectly perform unnecessary operations.

Now consider:

```
s = "1111"
```

The only valid final state is:

```
s = ""
t = "1111"
```

One move transfers the entire string. The answer is `1`.

Another subtle case is:

```
s = "001"
```

The last block is already a block of ones. We can move that suffix directly to `t` in one move, so the answer is `1`.

A common mistake is counting the number of blocks and returning that value. Here there are two blocks (`00` and `1`), but only one move is needed.

Finally, consider:

```
s = "101"
```

The answer is `3`.

The alternating structure forces us to move multiple suffixes back and forth. Any approach that only counts the number of ones or zeros will fail on this example.

## Approaches

A brute-force view is to treat each state as a pair of strings `(s, t)` and run BFS. Every possible suffix transfer creates a new state. BFS would eventually find the minimum number of moves because all moves have equal cost.

The problem is that the number of states grows explosively. Even for moderate string lengths, there are far too many possible pairs of strings to explore. This approach becomes impractical almost immediately.

To find a better solution, we need to understand what a move accomplishes.

Look at the string as consecutive blocks of equal characters. For example:

```
001110011
```

contains the blocks:

```
00 | 111 | 00 | 11
```

Every time the character changes between adjacent positions, a new block begins.

Suppose we scan the string from left to right. Whenever a block of `1`s appears, those ones eventually have to end up in `t`. Because moves operate on suffixes, each transition between different characters creates an additional obstacle that requires another transfer.

After examining several examples, a simple pattern emerges.

Let `changes` be the number of positions `i` such that:

```
s[i] != s[i - 1]
```

Then:

If the string starts with `0`, the answer is exactly `changes`.

If the string starts with `1`, the answer is `changes + 1`.

Why does the starting character matter?

If the string begins with `1`, the first block of ones must eventually be moved out of `s`. That requires one extra operation. If the string begins with `0`, the first block is already on the correct side and does not require that initial move.

This immediately gives an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the binary string `s`.
2. Count how many times adjacent characters differ.

For every index `i > 0`, if `s[i] != s[i-1]`, increment a counter `changes`.

Each such position marks the beginning of a new block.
3. If the first character is `1`, add one more to the answer.

The leading block of ones must be transferred out of `s`, creating one extra required move.
4. Otherwise, if the first character is `0`, the answer is simply `changes`.
5. Output the result.

### Why it works

The string can be viewed as alternating blocks of zeros and ones.

Every boundary between two neighboring blocks must be crossed by the moving suffix boundary at some point. Each character change contributes exactly one required transfer. This accounts for all transitions in the string.

If the string starts with a block of ones, that block is initially in the wrong place because all ones must finish inside `t`. Moving that first block out requires one additional operation beyond the transitions already counted.

Thus the minimum number of moves equals the number of character changes, plus one when the first character is `1`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s = input().strip()

        changes = 0
        for i in range(1, n):
            if s[i] != s[i - 1]:
                changes += 1

        answer = changes + (1 if s[0] == '1' else 0)
        print(answer)

solve()
```

The implementation directly follows the observation about blocks.

The loop counts every position where the current character differs from the previous one. This is exactly the number of transitions between consecutive blocks.

After that, we check the first character. If it is `1`, we add one extra move. Otherwise nothing additional is needed.

The only boundary condition is a string of length one. In that case the loop never executes, `changes` remains zero, and the formula still works correctly. `"0"` produces `0`, while `"1"` produces `1`.

## Worked Examples

### Example 1

Input:

```
s = "00110"
```

| Index | Character | Change from Previous | changes |
| --- | --- | --- | --- |
| 0 | 0 | - | 0 |
| 1 | 0 | No | 0 |
| 2 | 1 | Yes | 1 |
| 3 | 1 | No | 1 |
| 4 | 0 | Yes | 2 |

The string starts with `0`.

| Variable | Value |
| --- | --- |
| changes | 2 |
| starts with 1 | No |
| answer | 2 |

Output:

```
2
```

This example shows that the answer equals the number of block transitions when the first block already consists of zeros.

### Example 2

Input:

```
s = "101"
```

| Index | Character | Change from Previous | changes |
| --- | --- | --- | --- |
| 0 | 1 | - | 0 |
| 1 | 0 | Yes | 1 |
| 2 | 1 | Yes | 2 |

The string starts with `1`.

| Variable | Value |
| --- | --- |
| changes | 2 |
| starts with 1 | Yes |
| answer | 3 |

Output:

```
3
```

This example demonstrates the extra move caused by a leading block of ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan through the string |
| Space | O(1) | Only a few counters are stored |

Since the total length across all test cases is at most 1000, the algorithm runs comfortably within the limits. Even for much larger inputs, a single linear scan would remain efficient.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            s = input().strip()

            changes = 0
            for i in range(1, n):
                if s[i] != s[i - 1]:
                    changes += 1

            out.append(str(changes + (1 if s[0] == '1' else 0)))

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""5
5
00110
4
1111
3
001
5
00000
3
101
"""
) == """2
1
1
0
3"""

# minimum size, single zero
assert run(
"""1
1
0
"""
) == "0"

# minimum size, single one
assert run(
"""1
1
1
"""
) == "1"

# all zeros
assert run(
"""1
6
000000
"""
) == "0"

# alternating characters
assert run(
"""1
6
101010
"""
) == "6"

# single transition
assert run(
"""1
6
000111
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0` | Smallest valid all-correct string |
| `1` | `1` | Smallest valid leading-one case |
| `000000` | `0` | All characters already belong in `s` |
| `101010` | `6` | Maximum number of transitions |
| `000111` | `1` | Exactly one block boundary |

## Edge Cases

### All zeros

Input:

```
1
5
00000
```

The scan finds no adjacent differences.

```
changes = 0
```

The first character is `0`, so no extra move is added.

Output:

```
0
```

This correctly represents the fact that the initial state already satisfies the goal.

### All ones

Input:

```
1
4
1111
```

The scan again finds no adjacent differences.

```
changes = 0
```

The first character is `1`, so we add one.

```
answer = 1
```

One move transfers the entire string into `t`.

### Single transition

Input:

```
1
6
001111
```

There is exactly one position where the character changes.

```
changes = 1
```

The string starts with `0`.

```
answer = 1
```

Moving the suffix `"1111"` to `t` immediately achieves the goal.

### Alternating characters

Input:

```
1
5
01010
```

Every adjacent pair differs.

```
changes = 4
```

The first character is `0`.

```
answer = 4
```

This is the most demanding structure because every character starts a new block. The formula correctly counts all required transfers.
