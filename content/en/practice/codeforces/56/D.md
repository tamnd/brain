---
title: "CF 56D - Changing a String"
description: "We are given two uppercase strings, s and t. We may transform s using three operations: 1. Insert a character at any position. 2. Delete a character from any position. 3. Replace one character with another. Every operation costs exactly one move."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 56
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 52 (Div. 2)"
rating: 2100
weight: 56
solve_time_s: 132
verified: true
draft: false
---

[CF 56D - Changing a String](https://codeforces.com/problemset/problem/56/D)

**Rating:** 2100  
**Tags:** dp  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two uppercase strings, `s` and `t`. We may transform `s` using three operations:

1. Insert a character at any position.
2. Delete a character from any position.
3. Replace one character with another.

Every operation costs exactly one move. The task is not only to compute the minimum number of moves needed to turn `s` into `t`, but also to output one actual sequence of operations that achieves this minimum.

This is the classical edit distance problem, but with reconstruction of the operations. The reconstruction part is where most implementation mistakes happen.

The strings have length at most 1000. A brute-force search over all possible operation sequences is hopeless because the branching factor is huge. Even trying all operations for only 20 steps already explodes exponentially. With lengths up to 1000, we need something close to quadratic time.

A dynamic programming solution with `O(n * m)` states is completely feasible here. With both lengths equal to 1000, we have one million states. Each state transitions in constant time, which easily fits within the limits.

The tricky part is producing valid operation indices while the string is changing over time.

Consider this example:

```
s = ABC
t = ADBC
```

If we decide to insert `D` after `A`, the operation must be:

```
INSERT 2 D
```

After the insertion, all later positions shift by one. A careless reconstruction that computes positions relative to the original string will quickly become inconsistent.

Another subtle case is when multiple optimal answers exist.

```
s = A
t = B
```

We can either:

```
REPLACE 1 B
```

or:

```
DELETE 1
INSERT 1 B
```

The second sequence is longer, so reconstruction must follow only transitions that preserve optimality.

A final common bug appears when one string is exhausted before the other.

```
s = ABC
t = ABCDE
```

The remaining work is pure insertion:

```
INSERT 4 D
INSERT 5 E
```

If indices are computed incorrectly after earlier insertions, the generated operations become invalid.

## Approaches

The brute-force approach is straightforward conceptually. At every step we try every possible insertion, deletion, and replacement, recursively exploring all transformation sequences until we reach the target string. Since every operation changes the string, the number of reachable states grows exponentially.

Even for strings of length 20, the number of possibilities becomes enormous. Suppose we allow roughly 60 possible operations per step and need only 15 edits. That already gives around `60^15` possibilities, far beyond anything computable.

The reason brute force works conceptually is that edit operations naturally form a search tree. The problem is that many different sequences lead to the same intermediate prefixes repeatedly. We recompute equivalent subproblems again and again.

The key observation is that the future only depends on the remaining suffixes of the strings.

Suppose we are matching:

```
s[i:]
t[j:]
```

The optimal answer from this point does not care how we arrived here. That means we can define a DP state:

```
dp[i][j] = minimum edits needed to transform s[i:] into t[j:]
```

Now every state has only three meaningful transitions:

1. Delete `s[i]`
2. Insert `t[j]`
3. Replace `s[i]` with `t[j]` if they differ

If the characters already match, we simply move diagonally without paying anything.

This reduces the problem from exponential search to a grid DP with only `n * m` states.

After computing the minimum distances, we reconstruct one optimal path by walking through the DP table and choosing transitions consistent with the stored optimal values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Let `n = len(s)` and `m = len(t)`.
2. Create a DP table `dp` of size `(n + 1) × (m + 1)`.

`dp[i][j]` represents the minimum edits needed to transform the suffix `s[i:]` into `t[j:]`.
3. Initialize the base cases.

If `i = n`, the source string is exhausted, so we must insert all remaining characters of `t`.

```
dp[n][j] = m - j
```

If `j = m`, the target string is exhausted, so we must delete all remaining characters of `s`.

```
dp[i][m] = n - i
```
4. Fill the table from bottom-right to top-left.

If `s[i] == t[j]`, no operation is needed for these characters.

```
dp[i][j] = dp[i + 1][j + 1]
```

Otherwise we consider the three edit operations.

Delete:

```
1 + dp[i + 1][j]
```

Insert:

```
1 + dp[i][j + 1]
```

Replace:

```
1 + dp[i + 1][j + 1]
```

We take the minimum.
5. Reconstruct one optimal sequence of operations.

Start from `(i, j) = (0, 0)` and maintain a variable `shift`.

`shift` tracks how much the current string length differs from the original because insertions and deletions change indices.
6. If `s[i] == t[j]` and:

```
dp[i][j] == dp[i + 1][j + 1]
```

move diagonally without producing an operation.
7. Otherwise check which operation preserves optimality.

For deletion:

```
dp[i][j] == 1 + dp[i + 1][j]
```

Output:

```
DELETE position
```

The current position is:

```
i + shift + 1
```

Then increment `i` and decrement `shift`.
8. For insertion:

```
dp[i][j] == 1 + dp[i][j + 1]
```

Output:

```
INSERT position character
```

The insertion position is again:

```
i + shift + 1
```

Then increment `j` and increment `shift`.
9. For replacement:

```
dp[i][j] == 1 + dp[i + 1][j + 1]
```

Output:

```
REPLACE position character
```

Then increment both `i` and `j`.
10. Continue until both strings are fully processed.

### Why it works

The DP invariant is that `dp[i][j]` always stores the true minimum number of edits required to transform `s[i:]` into `t[j:]`.

Every valid transformation must begin with exactly one of four possibilities:

1. Match equal characters.
2. Delete the current character of `s`.
3. Insert the current character of `t`.
4. Replace the current character of `s`.

The recurrence checks all of them and chooses the best. Since each transition moves toward smaller suffixes, all needed states are already computed.

During reconstruction, we only follow transitions whose cost exactly matches the stored optimum. That guarantees every chosen operation belongs to some globally optimal solution.

The `shift` variable guarantees positions stay correct even after the string length changes dynamically.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    t = input().strip()

    n = len(s)
    m = len(t)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][m] = n - i

    for j in range(m + 1):
        dp[n][j] = m - j

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s[i] == t[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i + 1][j],      # delete
                    dp[i][j + 1],      # insert
                    dp[i + 1][j + 1]   # replace
                )

    operations = []

    i = 0
    j = 0
    shift = 0

    while i < n or j < m:
        if i < n and j < m and s[i] == t[j] and dp[i][j] == dp[i + 1][j + 1]:
            i += 1
            j += 1

        elif i < n and dp[i][j] == 1 + dp[i + 1][j]:
            pos = i + shift + 1
            operations.append(f"DELETE {pos}")
            i += 1
            shift -= 1

        elif j < m and dp[i][j] == 1 + dp[i][j + 1]:
            pos = i + shift + 1
            operations.append(f"INSERT {pos} {t[j]}")
            j += 1
            shift += 1

        else:
            pos = i + shift + 1
            operations.append(f"REPLACE {pos} {t[j]}")
            i += 1
            j += 1

    print(len(operations))
    print("\n".join(operations))

solve()
```

The first part builds the DP table from smaller suffixes toward larger ones. Since every transition references states with larger indices, iterating backward guarantees those values already exist.

The reconstruction phase is where most care is required.

The variable `shift` tracks how positions change relative to the original string. Suppose we inserted two characters earlier. Then every future position in the current string is shifted by `+2`.

Without this adjustment, operations would target incorrect indices after the first insertion or deletion.

The reconstruction order matters too. Matching characters must be checked before edit operations. Otherwise the algorithm might unnecessarily replace equal characters and still preserve optimality numerically in some tied situations.

The loop condition:

```
while i < n or j < m:
```

is important because one string may finish before the other. We still need to emit remaining insertions or deletions.

## Worked Examples

### Example 1

Input:

```
s = ABA
t = ABBBA
```

The optimal answer is two insertions.

| Step | i | j | shift | Action | Current Result |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | Match A | ABA |
| 2 | 1 | 1 | 0 | Match B | ABA |
| 3 | 2 | 2 | 0 | INSERT 3 B | ABBA |
| 4 | 2 | 3 | 1 | INSERT 4 B | ABBBA |
| 5 | 2 | 4 | 2 | Match A | ABBBA |

Output:

```
2
INSERT 3 B
INSERT 4 B
```

This trace demonstrates why `shift` is necessary. After the first insertion, all later positions move right by one.

### Example 2

Input:

```
s = ABC
t = ADC
```

Only one replacement is needed.

| Step | i | j | shift | Action | Current Result |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | Match A | ABC |
| 2 | 1 | 1 | 0 | REPLACE 2 D | ADC |
| 3 | 2 | 2 | 0 | Match C | ADC |

Output:

```
1
REPLACE 2 D
```

This example shows diagonal transitions in the DP. Matching characters cost nothing, while differing characters may be handled by replacement instead of separate delete and insert operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every DP state is computed once |
| Space | O(nm) | The full DP table is stored for reconstruction |

With both strings limited to length 1000, the DP table contains roughly one million cells. This comfortably fits within the memory limit, and the number of operations is small enough for Python within 2 seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    n = len(s)
    m = len(t)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][m] = n - i

    for j in range(m + 1):
        dp[n][j] = m - j

    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s[i] == t[j]:
                dp[i][j] = dp[i + 1][j + 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i + 1][j],
                    dp[i][j + 1],
                    dp[i + 1][j + 1]
                )

    ops = []

    i = 0
    j = 0
    shift = 0

    while i < n or j < m:
        if i < n and j < m and s[i] == t[j] and dp[i][j] == dp[i + 1][j + 1]:
            i += 1
            j += 1

        elif i < n and dp[i][j] == 1 + dp[i + 1][j]:
            pos = i + shift + 1
            ops.append(f"DELETE {pos}")
            i += 1
            shift -= 1

        elif j < m and dp[i][j] == 1 + dp[i][j + 1]:
            pos = i + shift + 1
            ops.append(f"INSERT {pos} {t[j]}")
            j += 1
            shift += 1

        else:
            pos = i + shift + 1
            ops.append(f"REPLACE {pos} {t[j]}")
            i += 1
            j += 1

    return str(len(ops)) + "\n" + "\n".join(ops)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
out = run("ABA\nABBBA\n")
assert out.startswith("2"), "sample 1"

# identical strings
out = run("ABC\nABC\n")
assert out.strip() == "0", "already equal"

# pure insertion
out = run("A\nABCD\n")
assert out.startswith("3"), "insertions"

# pure deletion
out = run("ABCD\nA\n")
assert out.startswith("3"), "deletions"

# replacement only
out = run("AAAA\nBBBB\n")
assert out.startswith("4"), "replacements"

# minimum size
out = run("A\nB\n")
assert out.startswith("1"), "single replacement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `ABC → ABC` | `0` operations | Already-equal strings |
| `A → ABCD` | `3` operations | Correct insertion indices |
| `ABCD → A` | `3` operations | Correct deletion handling |
| `AAAA → BBBB` | `4` operations | Replacement transitions |
| `A → B` | `1` operation | Smallest non-trivial case |

## Edge Cases

Consider the case where the target string is longer only because of suffix additions.

Input:

```
ABC
ABCDE
```

The DP eventually reaches:

```
dp[3][3] = 2
```

because the source suffix is empty while the target suffix is `"DE"`.

Reconstruction outputs:

```
INSERT 4 D
INSERT 5 E
```

After inserting `D`, the current string becomes `ABCD`, so the next insertion position must become `5`. The `shift` variable handles this automatically.

Now consider a deletion-heavy example.

Input:

```
ABCDE
AB
```

The optimal sequence is:

```
DELETE 3
DELETE 3
DELETE 3
```

After deleting the original `C`, the original `D` moves into position 3. A reconstruction based on original indices would incorrectly try deleting positions 4 and 5 afterward.

Finally, consider equal strings.

Input:

```
HELLO
HELLO
```

Every character match follows the zero-cost diagonal transition:

```
dp[i][j] = dp[i+1][j+1]
```

No operations are emitted, and the answer is correctly `0`.
