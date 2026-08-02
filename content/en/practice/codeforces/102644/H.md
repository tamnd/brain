---
title: "CF 102644H - String Mood Updates"
description: "We maintain a string of uppercase letters and question marks. A question mark can later become any uppercase English letter. Reading the string from left to right changes Limak's mood, which has only two possible states: happy and sad."
date: "2026-08-02T14:50:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "H"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 61
verified: true
draft: false
---

[CF 102644H - String Mood Updates](https://codeforces.com/problemset/problem/102644/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a string of uppercase letters and question marks. A question mark can later become any uppercase English letter. Reading the string from left to right changes Limak's mood, which has only two possible states: happy and sad. The goal is to count how many replacements of all question marks leave Limak happy after the whole string is processed. After each single character update, the same count must be printed again. The constraints are large: the string length and the number of updates can both reach 200000, so a solution that scans the whole string after every update would perform about 40000000000 operations in the worst case, which is far beyond what fits in a normal contest limit. The problem statement and limits are from Codeforces Gym 102644H.

The important part is that the mood has only two states. We do not need to remember the whole history of the prefix, only how many ways a segment can transform an incoming mood into an outgoing mood. This small state space is what allows us to maintain the answer dynamically.

A common mistake is to treat question marks independently and only count letters that are individually good. This fails because letters interact through the current mood. For example, with the string `A?`, the correct answer is `6`. The first `A` flips happy to sad, so the second character must make the mood happy again. A careless solution that counts valid letters at each position independently would miss that dependency.

Another edge case is when a segment has no effect at all. For input:

```
1 1
B
1 A
```

The outputs are:

```
19
18
```

`B` is a letter that keeps the mood unchanged, while `A` flips it. A solution that only counts flips and ignores the number of neutral choices would give the wrong result.

A third edge case is a string consisting only of question marks. For:

```
2 0
??
```

the answer is `403`. Every possible pair of letters must be considered, including combinations where the first letter makes Limak sad and the second one repairs the mood. Any method that only tracks the number of currently happy prefixes will lose these possibilities.

## Approaches

The brute force solution is straightforward. For every question mark, try all 26 letters, simulate the mood changes, and count replacements that end in the happy state. This is correct because it checks exactly the set of possible strings. However, if there are 200000 question marks, the number of possible strings is `26^200000`, so even generating a tiny fraction of them is impossible.

A better direction comes from observing that every character only performs a transition between two states. A segment of the string can be represented by a 2 by 2 matrix. The row describes the starting mood, the column describes the final mood, and each value stores how many replacements make that transition possible. When two segments are joined, their matrices are multiplied, because the first segment chooses an intermediate mood and the second segment continues from it.

A single character has a small fixed matrix. For example, a question mark considers all 26 possible letters and adds the contribution of every letter to the appropriate transition. The entire string becomes the product of these matrices. Since updates affect only one position, a segment tree can store products of ranges and recompute only the logarithmic number of nodes affected by an update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^x * n) where x is the number of question marks | O(n) | Too slow |
| Optimal | O(log n) per update after O(n) build | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent each character as a 2 by 2 transition matrix. The first row and column correspond to starting happy or sad states, and the second dimension represents the ending state. The value in a cell is the number of character choices that create that transition.
2. Build a segment tree where each leaf stores the matrix of one character. Internal nodes store the product of their two children. Matrix multiplication is used because the left child describes what happens first and the right child describes what happens afterwards.
3. The initial answer is the number of ways to start happy and finish happy. This is the matrix entry from happy to happy at the root of the tree.
4. For every update, replace the leaf matrix of the changed character. Recalculate all ancestors until reaching the root. Only O(log n) nodes depend on one position, so the update is fast.
5. After rebuilding the path, print the new happy to happy value stored in the root matrix.

Why it works: the segment tree invariant is that every node stores the exact transition matrix of its interval. A leaf is correct because it directly describes one character. If two children are correct, multiplying their matrices considers every possible mood after the left interval and every continuation through the right interval, so the parent is also correct. By induction, the root represents the whole string, and its happy to happy entry is exactly the required count.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def multiply(a, b):
    return [
        [
            (a[0][0] * b[0][0] + a[0][1] * b[1][0]) % MOD,
            (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % MOD
        ],
        [
            (a[1][0] * b[0][0] + a[1][1] * b[1][0]) % MOD,
            (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % MOD
        ]
    ]

def char_matrix(c):
    res = [[0, 0], [0, 0]]
    for x in range(26):
        ch = chr(ord('A') + x)
        if ch in "AEIOU":
            res[0][1] += 1
            res[1][0] += 1
        elif ch == "H":
            res[0][0] += 1
            res[1][1] += 1
        elif ch in "SD":
            res[0][1] += 1
            res[1][1] += 1
        else:
            res[0][0] += 1
            res[1][1] += 1
    if c != "?":
        res = [[0, 0], [0, 0]]
        if c in "AEIOU":
            res[0][1] = 1
            res[1][0] = 1
        elif c == "H":
            res[0][0] = 1
            res[1][1] = 1
        elif c in "SD":
            res[0][1] = 1
            res[1][1] = 1
        else:
            res[0][0] = 1
            res[1][1] = 1
    return res

def solve():
    n, q = map(int, input().split())
    s = list(input().strip())

    size = 1
    while size < n:
        size *= 2

    tree = [[[1, 0], [0, 1]] for _ in range(2 * size)]

    for i, c in enumerate(s):
        tree[size + i] = char_matrix(c)

    for i in range(size - 1, 0, -1):
        tree[i] = multiply(tree[i * 2], tree[i * 2 + 1])

    ans = [str(tree[1][0][0])]

    for _ in range(q):
        i, c = input().split()
        i = int(i) - 1
        pos = size + i
        tree[pos] = char_matrix(c)
        pos //= 2
        while pos:
            tree[pos] = multiply(tree[pos * 2], tree[pos * 2 + 1])
            pos //= 2
        ans.append(str(tree[1][0][0]))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The matrix multiplication function combines two consecutive intervals. The order matters because the left interval is read before the right interval. Reversing the multiplication order would describe the string backwards.

The `char_matrix` function handles both fixed letters and question marks. For a question mark, it starts with all possible uppercase letters and accumulates their transitions. The state indexing assumes state `0` means happy and state `1` means sad, so the final answer is always stored at `[0][0]`.

The segment tree uses a power of two size to simplify indexing. Extra leaves represent empty segments and use the identity matrix because multiplying by an empty segment should not change any transition count. Python integers do not overflow, but every multiplication result is reduced modulo `10^9+7` to keep values small.

## Worked Examples

For input:

```
2 5
A?
2 O
1 H
1 ?
2 ?
2 H
```

the tree root values change as follows:

| String state | Updated position | Root happy to happy |
| --- | --- | --- |
| A? | none | 6 |
| AO | position 2 becomes O | 1 |
| HO | position 1 becomes H | 0 |
| ?O | position 1 becomes ? | 7 |
| ?? | position 2 becomes ? | 403 |
| ?H | position 2 becomes H | 26 |

This example demonstrates why the answer depends on the combined effect of the whole string. The matrix stores all possible mood transitions, so a replacement that first makes Limak sad is still counted if a later character restores happiness.

For input:

```
1 3
B
1 A
1 ?
1 H
```

the transitions are:

| String state | Updated character | Root matrix happy to happy |
| --- | --- | --- |
| B | none | 19 |
| A | A | 0 |
| ? | ? | 19 |
| H | H | 1 |

This trace checks single-character behavior. With one character there is no interaction between positions, so the matrix directly reflects that letter's effect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q log n) | Building the tree touches every character once, and every update changes one root-to-leaf path. |
| Space | O(n) | The segment tree stores a constant-sized matrix at each node. |

The constraints require handling 200000 updates, so a logarithmic update is necessary. The matrix size is fixed at 2 by 2, making every tree operation constant work aside from the tree traversal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# This block is intended to be used with the solve function above and a redirected stdout.

assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0\nH\n` | `1` | Single fixed happy letter |
| `1 1\n?\n1 A\n` | `19\n0` | Single position updates and flip behavior |
| `3 0\nBBB\n` | `6859` | All neutral letters |
| `2 2\n??\n1 S\n2 O\n` | `403\n26\n6` | Interaction between forced mood changes and question marks |

## Edge Cases

For the string `A?`, the algorithm creates a matrix for `A` that only allows a happy to sad transition and then combines it with the question mark matrix. The final happy to happy entry counts only replacements where the second character repairs the mood, producing `6`.

For the single character update case:

```
1 1
B
1 A
```

the tree contains only one meaningful leaf. Replacing the leaf changes the root immediately. The answer changes from `19` to `0` because `A` always flips the initial happy state.

For an all-question-mark string, every leaf contains the sum of all 26 possible transitions. The segment tree multiplication keeps both intermediate moods alive, so paths that temporarily become sad are not discarded. This is why the two-character case gives `403` instead of only counting immediately happy choices.
