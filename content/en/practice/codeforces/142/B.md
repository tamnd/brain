---
title: "CF 142B - Help General"
description: "We have an n × m chessboard-like grid, and we want to place as many soldiers as possible. Two soldiers conflict if the squared Euclidean distance between their cells is exactly 5. The only integer pairs whose squared distance equals 5 are (1, 2) and (2, 1) up to sign."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 142
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 102 (Div. 1)"
rating: 1800
weight: 142
solve_time_s: 98
verified: true
draft: false
---

[CF 142B - Help General](https://codeforces.com/problemset/problem/142/B)

**Rating:** 1800  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an `n × m` chessboard-like grid, and we want to place as many soldiers as possible. Two soldiers conflict if the squared Euclidean distance between their cells is exactly `5`.

The only integer pairs whose squared distance equals `5` are `(1, 2)` and `(2, 1)` up to sign. In other words, soldiers attack each other exactly like knights in chess. The task is really asking for the maximum number of non-attacking knights on an `n × m` board.

The board dimensions are at most `1000 × 1000`, so the total number of cells can reach one million. That immediately rules out any exponential search or backtracking. Even algorithms that try to explore subsets or run heavy graph algorithms over all cells would struggle. We need a direct constructive or mathematical observation.

Several edge cases are easy to mishandle if we jump straight to a checkerboard pattern.

Consider a single row:

Input:

```
1 7
```

Correct output:

```
7
```

Knights need both a horizontal and vertical offset to attack. On a `1 × 7` board, no two cells attack each other, so every square can be occupied. A careless checkerboard solution would incorrectly return `4`.

The `2 × m` case is the real trap.

Input:

```
2 4
```

Correct output:

```
4
```

A standard checkerboard gives only `4`, which happens to be correct here, but for:

Input:

```
2 5
```

Correct output:

```
6
```

A simple alternating coloring gives `5`, which is not optimal. On boards with one dimension equal to `2`, knights can be packed in repeating blocks of four columns.

Another subtle example:

Input:

```
2 2
```

Correct output:

```
4
```

No knight attack is possible because moving by `(1,2)` or `(2,1)` does not fit inside the board. Every cell may contain a soldier. Any formula that blindly uses half the cells would fail.

## Approaches

The brute-force interpretation is straightforward. Treat every cell as a vertex in a graph, connect two cells if knights attack each other, and search for the maximum independent set. That guarantees correctness because an independent set is exactly a set of non-conflicting soldiers.

The problem is that maximum independent set is exponential in general. Even with only 40 cells, brute force becomes impractical. Our board may contain up to one million cells, so this direction is hopeless.

The structure of knight movement changes everything. Knights always jump from one color of a checkerboard to the other. That means the attack graph is bipartite. On most boards, placing knights on all black squares or all white squares immediately gives about half the cells, and in fact that is optimal for boards where both dimensions are at least `3`.

The only exceptions happen when one dimension is very small.

If either dimension equals `1`, knights cannot attack at all. Every square may be used.

If either dimension equals `2`, the pattern becomes special. Knights can only interact inside groups of four consecutive columns. In each such block of four, we can safely place four knights. Any leftover columns contribute at most two extra knights per column pair.

For all larger boards, a simple checkerboard arrangement is optimal, giving:

```
ceil(n * m / 2)
```

The entire problem reduces to handling these three structural cases carefully.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(nm)) | O(nm) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Normalize the dimensions so that `n <= m`.

This simplifies handling special cases because we only need to check small values of `n`.
3. If `n == 1`, output `m`.

A knight needs movement in two directions. On a single row, no attacks are possible.
4. If `n == 2`, process the board in blocks of four columns.

In every block of four columns, we can place four knights safely using a repeating pattern.
5. Compute:

```
blocks = m // 4
rem = m % 4
```
6. Add `blocks * 4` knights for the complete blocks.
7. For the remaining columns:

- if `rem == 0`, add `0`
- if `rem == 1`, add `2`
- if `rem >= 2`, add `4`

The leftover columns can contribute at most four additional knights.
8. Otherwise, when `n >= 3`, output:

```
(n * m + 1) // 2
```

This is the number of cells of the larger color in a checkerboard coloring.

### Why it works

When both dimensions are at least `3`, every knight move changes checkerboard color. Placing knights on only one color guarantees no conflicts, and no arrangement can exceed the larger partition size of the bipartite graph.

The `1 × m` case has no legal knight moves at all, so every square is safe.

The `2 × m` case behaves differently because knights can only interact across a very restricted structure. The optimal arrangement repeats every four columns. Inside each four-column segment, all four knights can be placed safely. Any incomplete segment contributes at most two knights per remaining column pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

if n > m:
    n, m = m, n

if n == 1:
    print(m)

elif n == 2:
    blocks = m // 4
    rem = m % 4

    ans = blocks * 4

    if rem == 1:
        ans += 2
    elif rem > 1:
        ans += 4

    print(ans)

else:
    print((n * m + 1) // 2)
```

The first step swaps the dimensions so that `n` is always the smaller one. That allows all special handling to focus on `n == 1` and `n == 2`.

The `n == 1` branch is direct. Knights cannot attack because every attack requires movement across two dimensions.

The `n == 2` logic is the only tricky part. The repeating pattern spans four columns. Each complete group contributes exactly four knights. The remainder handling is subtle:

For one extra column, we can place two more knights.

For two or three extra columns, we can place four more knights.

A common mistake is using:

```
ans += rem * 2
```

which overcounts when `rem == 3`.

The final branch handles all larger boards using the checkerboard formula. The expression:

```
(n * m + 1) // 2
```

computes the ceiling of half the cells.

Python integers easily handle the maximum product here, but even in languages with fixed-width integers, `1000 × 1000` is completely safe.

## Worked Examples

### Example 1

Input:

```
2 4
```

| Step | Value |
| --- | --- |
| Normalized `(n, m)` | `(2, 4)` |
| `blocks` | `1` |
| `rem` | `0` |
| Base answer | `4` |
| Extra from remainder | `0` |
| Final answer | `4` |

This example shows a perfect four-column block. The repeating construction fits exactly once.

### Example 2

Input:

```
3 4
```

| Step | Value |
| --- | --- |
| Normalized `(n, m)` | `(3, 4)` |
| Special case triggered | No |
| Total cells | `12` |
| Formula | `(12 + 1) // 2` |
| Final answer | `6` |

This demonstrates the general checkerboard case. Half the cells can be occupied without conflicts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and condition checks |
| Space | O(1) | No auxiliary data structures are used |

The solution performs constant work regardless of board size. Even the maximum `1000 × 1000` board is processed instantly, well within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    if n > m:
        n, m = m, n

    if n == 1:
        print(m)

    elif n == 2:
        blocks = m // 4
        rem = m % 4

        ans = blocks * 4

        if rem == 1:
            ans += 2
        elif rem > 1:
            ans += 4

        print(ans)

    else:
        print((n * m + 1) // 2)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("2 4\n") == "4", "sample 1"

# custom cases
assert run("1 1\n") == "1", "minimum board"
assert run("1 7\n") == "7", "single row"
assert run("2 5\n") == "6", "special 2-row pattern"
assert run("3 3\n") == "5", "checkerboard case"
assert run("1000 1000\n") == "500000", "maximum size"
assert run("2 2\n") == "4", "small special case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum board |
| `1 7` | `7` | No attacks on single row |
| `2 5` | `6` | Correct remainder handling for `n = 2` |
| `3 3` | `5` | General checkerboard formula |
| `1000 1000` | `500000` | Maximum constraints |
| `2 2` | `4` | Small board where every square is usable |

## Edge Cases

Consider the input:

```
1 7
```

The algorithm normalizes dimensions and enters the `n == 1` branch. It immediately returns `7`.

No knight move can exist because vertical movement is impossible. The algorithm correctly avoids the checkerboard formula, which would incorrectly give `4`.

Now consider:

```
2 5
```

The computation becomes:

| Variable | Value |
| --- | --- |
| `blocks` | `1` |
| `rem` | `1` |
| Base | `4` |
| Extra | `2` |
| Answer | `6` |

The leftover single column contributes exactly two additional knights. This catches implementations that incorrectly add only one.

Finally:

```
2 2
```

We get:

| Variable | Value |
| --- | --- |
| `blocks` | `0` |
| `rem` | `2` |
| Base | `0` |
| Extra | `4` |
| Answer | `4` |

Even though the board is tiny, no knight attack fits inside it. The special handling correctly allows every square to be occupied.
