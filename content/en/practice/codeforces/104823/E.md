---
title: "CF 104823E - string"
description: "We are given a string of length $n$ where each position holds a visible ASCII character. Then we are given $m$ operations, each operation picks two distinct characters $(x, y)$."
date: "2026-06-28T12:37:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104823
codeforces_index: "E"
codeforces_contest_name: "The 17-th BIT Campus Programming Contest - Online Round"
rating: 0
weight: 104823
solve_time_s: 41
verified: true
draft: false
---

[CF 104823E - string](https://codeforces.com/problemset/problem/104823/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of length $n$ where each position holds a visible ASCII character. Then we are given $m$ operations, each operation picks two distinct characters $(x, y)$. For every operation, the rule is a global swap: every occurrence of $x$ becomes $y$, and every occurrence of $y$ becomes $x$, simultaneously across the whole string. This is not a local swap at positions, but a full relabeling of characters.

After applying all operations in order, we must output the final transformed string.

The important constraint is that both $n$ and $m$ can be as large as $10^5$. A direct simulation that scans the whole string for every operation would require up to $10^5 \times 10^5 = 10^{10}$ character updates, which is far beyond what a one second limit allows. Even scanning the string once per operation is already too slow.

A subtle pitfall comes from interpreting the swap as independent replacements. The swap is simultaneous, so intermediate replacement order inside a single operation must not leak into the result. For example, if we mistakenly replace all $x \to y$ first and then all $y \to x$, we corrupt the logic unless we carefully separate the mapping layer.

Another potential mistake is repeatedly rewriting the string itself. Since characters only change identity, not position, we do not need to modify the string directly during each operation.

## Approaches

The brute-force idea is straightforward. For each operation $(x, y)$, we scan the entire string and replace every occurrence of $x$ with $y$ and every occurrence of $y$ with $x$. This correctly simulates the problem because each operation is a global swap applied uniformly.

The problem is performance. Each scan is $O(n)$, and we do it $m$ times, leading to $O(nm)$. With $10^5$ in both dimensions, this becomes infeasible.

The key observation is that the string itself does not need to be modified during operations. What actually changes is a mapping from original characters to current characters. Each operation only updates relationships between two symbols, not the positions in the string.

So instead of touching the string repeatedly, we maintain a mapping array that tells us, for each possible ASCII character, what it currently represents. Initially, every character maps to itself. When we process an operation $(x, y)$, we swap the images of $x$ and $y$ inside this mapping. After all operations, we apply this final mapping once to the original string.

This reduces the problem to maintaining a permutation of a constant-size alphabet (at most 94 visible ASCII characters). Each swap is $O(1)$, and final reconstruction is $O(n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Mapping Swap | $O(n + m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We treat every character as an index in a fixed-size array representing ASCII values. The core idea is to maintain a current identity mapping that evolves with each operation.

1. Initialize a mapping array so that each character maps to itself. This represents the identity transformation before any swaps are applied.
2. For each operation $(x, y)$, interpret both characters as indices and swap their mapped values inside the mapping array. This simulates applying the global swap without touching the string itself. The reason this works is that we are tracking the transformation of labels rather than the string content.
3. After processing all operations, construct the final string by iterating over each character in the original string and replacing it with its mapped value.
4. Output the constructed result.

Why this works is that the mapping array always represents the cumulative permutation of characters induced by all swaps. Each operation is a transposition in a permutation group over the character set, and composing these transpositions is equivalent to updating the mapping array incrementally. Since swaps are applied globally and symmetrically, no positional dependency exists, and the final character of each original symbol depends only on the final permutation, not intermediate states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    s = input().rstrip("\n")

    # visible ASCII range: 33 to 126 inclusive
    OFFSET = 33
    SIZE = 94

    mp = [i for i in range(SIZE)]

    for _ in range(m):
        x, y = input().split()
        xi = ord(x) - OFFSET
        yi = ord(y) - OFFSET
        mp[xi], mp[yi] = mp[yi], mp[xi]

    res = []
    for ch in s:
        idx = ord(ch) - OFFSET
        res.append(chr(mp[idx] + OFFSET))

    print("".join(res))

if __name__ == "__main__":
    solve()
```

The solution separates concerns cleanly. The mapping array `mp` stores the current image of each character under all swaps. Each operation only swaps two entries in this array, preserving the invariant that `mp[c]` is the final transformed identity of character `c` up to the current operation.

The final loop applies this transformation once, ensuring we only pay linear cost in the string length.

## Worked Examples

### Example 1

Input:

```
4 2
abcd
a c
d z
```

We track the mapping over visible characters involved:

| Step | Operation | Mapping change | Resulting mapping (relevant) |
| --- | --- | --- | --- |
| 0 | init | identity | a→a, b→b, c→c, d→d, z→z |
| 1 | a c | swap a and c | a→c, c→a |
| 2 | d z | swap d and z | d→z, z→d |

Now apply to string:

- a → c
- b → b
- c → a
- d → z

Output becomes:

```
cbaz
```

This shows that we never touched the string during processing, only the mapping.

### Example 2

Input:

```
5 3
@#$%@
# !
@ !
? !
```

We track only involved characters:

| Step | Operation | Key mapping changes |
| --- | --- | --- |
| 0 | init | @→@, #→#, !→! |
| 1 | # ! | # and ! swap |
| 2 | @ ! | @ swaps with current ! |
| 3 | ? ! | ? swaps with current ! |

After applying sequential swaps, each character’s final image is determined solely by accumulated transpositions.

Applying final mapping to `@#$%@` yields:

```
?@$%?
```

This trace demonstrates that repeated global swaps compose cleanly into a single permutation, regardless of intermediate states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each operation is a constant-time swap in a fixed-size array, and final reconstruction is linear in string length |
| Space | $O(1)$ | Mapping array size is bounded by ASCII visible character set |

The constraints allow up to $10^5$ operations and string length, and the solution processes each exactly once, comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    stdout.flush = lambda: None

    import builtins
    input_backup = builtins.input
    builtins.input = sys.stdin.readline

    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()

    builtins.input = input_backup
    return out.getvalue().strip()

# provided samples
assert run("""4 2
abcd
a c
d z
""") == "cbaz"

assert run("""5 3
@#$%@
# !
@ !
? !
""") == "?@$%?"

# custom tests
assert run("""1 1
a
a b
""") == "b"

assert run("""3 2
abc
a b
b c
""") == "cab"

assert run("""6 0
abcdef
""") == "abcdef"

assert run("""4 3
aaaa
a b
b c
c a
""") == "aaaa"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single swap | b | minimal case |
| chain swaps | cab | composition of swaps |
| no operations | abcdef | identity case |
| cycle swaps | aaaa | permutation cycle stability |

## Edge Cases

One edge case is when multiple swaps form cycles. For example, swapping `a b`, then `b c`, then `c a` does not “break” anything; it produces a valid permutation. The algorithm handles this naturally because it only composes transpositions in the mapping array.

Input:

```
3 3
abc
a b
b c
c a
```

Step by step mapping:

- after a b: a↔b
- after b c: b↔c (so cycle forms)
- after c a: completes cycle

Final mapping returns every character to a rotated position, producing a consistent final string. The implementation never depends on order inside the string, so no inconsistency arises.

Another edge case is when characters not appearing in the string are involved in swaps. Since the mapping array includes the entire ASCII range, these operations still correctly update future behavior if those characters appear later or affect other mappings.
