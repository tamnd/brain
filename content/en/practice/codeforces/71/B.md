---
title: "CF 71B - Progress Bar"
description: "We have a progress bar made of n consecutive squares. Every square stores an integer saturation value between 0 and k. The structure of the bar is very restricted. Some prefix of squares is completely filled, so their value is exactly k."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 1300
weight: 71
solve_time_s: 105
verified: true
draft: false
---

[CF 71B - Progress Bar](https://codeforces.com/problemset/problem/71/B)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a progress bar made of `n` consecutive squares. Every square stores an integer saturation value between `0` and `k`.

The structure of the bar is very restricted. Some prefix of squares is completely filled, so their value is exactly `k`. Some suffix is completely empty, so their value is `0`. Between them, there can be at most one partially filled square whose value is somewhere between `0` and `k`.

The percentage `t` describes how much of the total capacity is filled. Since each square can contribute at most `k`, the total capacity of the entire bar is `n * k`. The actual filled amount must satisfy:

$$\frac{100 \cdot \sum a_i}{n \cdot k} = t$$

Rearranging this gives:

$$\sum a_i = \frac{t \cdot n \cdot k}{100}$$

The task is to construct one valid progress bar configuration.

The constraints are tiny. Both `n` and `k` are at most `100`, so even inefficient simulation would fit comfortably within the time limit. This means the problem is not about optimization pressure, it is about translating the percentage into the exact configuration of full, partial, and empty cells without making arithmetic mistakes.

The tricky part is handling percentages that do not align perfectly with whole squares. For example:

Input:

```
3 10 50
```

The total capacity is `30`, and `50%` means the filled amount is `15`. The correct output is:

```
10 5 0
```

A careless solution might compute `50 / 100 = 0` using integer division and produce all zeros.

Another subtle case appears when the percentage lands exactly on a square boundary.

Input:

```
5 7 40
```

The filled amount is `14`, which means exactly two full squares:

```
7 7 0 0 0
```

A buggy implementation might incorrectly create a partial third square with value `0`, which is harmless visually but often comes from flawed logic around remainders.

The extreme percentages also matter.

Input:

```
4 9 0
```

Correct output:

```
0 0 0 0
```

Input:

```
4 9 100
```

Correct output:

```
9 9 9 9
```

These cases verify that the algorithm handles fully empty and fully filled bars without accessing indices outside the array.

## Approaches

A brute-force mindset would start by computing the exact filled amount and then trying every possible split between full squares, one partial square, and empty squares until the total sum matches the required value.

For example, if the filled amount is `37` and `k = 10`, we could test:

- `3` full squares and remainder `7`
- `2` full squares and remainder `17`
- `1` full square and remainder `27`

Only the first arrangement respects the rule that each square must stay between `0` and `k`.

This works because the constraints are tiny. We would perform at most a few hundred operations. Even an `O(n^2)` search would pass easily.

The structure of the progress bar gives a much cleaner observation. Every square contributes either:

- `k`, meaning completely full
- `0`, meaning empty
- one leftover remainder between `1` and `k - 1`

So after computing the total filled amount, we can divide it directly by `k`.

If:

$$filled = q \cdot k + r$$

then:

- the first `q` squares are completely full
- the next square has value `r`
- all remaining squares are `0`

This removes all searching and turns the construction into a direct arithmetic decomposition.

The brute-force works because the answer space is very small, but it still treats the arrangement as something to discover. The key insight is that the allowed shape of the bar already determines the answer uniquely once we know how many full blocks and leftover units exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, and `t`.
2. Compute the total filled amount:

$$filled = \frac{n \cdot k \cdot t}{100}$$

The statement guarantees the percentage corresponds to a valid integer amount.
3. Compute:

$$full = filled // k$$

and

$$rem = filled \% k$$

`full` tells us how many completely filled squares exist. `rem` is the value of the single partially filled square.
4. Create an array of size `n` initialized with zeros.
5. Set the first `full` positions to `k`.

These are the fully saturated squares.
6. If `full < n`, place `rem` into position `full`.

This becomes the partially filled square. If `rem` is zero, this position simply stays zero.
7. Print the array.

### Why it works

The total filled amount is decomposed uniquely into:

$$filled = full \cdot k + rem$$

where `0 ≤ rem < k`.

Assigning `full` complete squares contributes exactly `full * k`. Assigning one more square with value `rem` contributes the remaining amount. Every later square stays `0`.

The resulting array satisfies all required properties:

- every value is between `0` and `k`
- only one square can be partially filled
- the total saturation equals the required percentage

Since the decomposition is exact, the algorithm cannot overfill or underfill the progress bar.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k, t = map(int, input().split())

filled = n * k * t // 100

full = filled // k
rem = filled % k

ans = [0] * n

for i in range(full):
    ans[i] = k

if full < n:
    ans[full] = rem

print(*ans)
```

The first computation converts the percentage into the exact total saturation amount. Using integer arithmetic is safe because the problem guarantees a valid percentage configuration.

The division by `k` separates the contribution into complete squares and one remainder. This mirrors the exact structure required by the statement.

The array starts with all zeros because empty squares naturally form the suffix of the progress bar. Then the loop fills the prefix with `k`.

The condition:

```
if full < n:
```

prevents an out-of-bounds write when the progress bar is completely full. For example, when `t = 100`, we get `full = n`, so there is no partially filled square.

The order of operations matters. We first assign all fully saturated squares, then place the remainder after them. Reversing the order would overwrite the partial value when `rem = k`, although that situation never occurs because remainders are always strictly smaller than `k`.

## Worked Examples

### Example 1

Input:

```
10 10 54
```

The total capacity is `100`, so `54%` means the filled amount is `54`.

| Step | Variable | Value |
| --- | --- | --- |
| Initial | `n, k, t` | `10, 10, 54` |
| Compute filled | `filled` | `54` |
| Full squares | `full` | `5` |
| Remainder | `rem` | `4` |
| After filling prefix | `ans` | `[10, 10, 10, 10, 10, 0, 0, 0, 0, 0]` |
| After partial square | `ans` | `[10, 10, 10, 10, 10, 4, 0, 0, 0, 0]` |

Final output:

```
10 10 10 10 10 4 0 0 0 0
```

This trace shows the central decomposition idea. Five complete squares contribute `50`, and the partial square contributes the remaining `4`.

### Example 2

Input:

```
5 7 40
```

The total capacity is `35`, and `40%` equals `14`.

| Step | Variable | Value |
| --- | --- | --- |
| Initial | `n, k, t` | `5, 7, 40` |
| Compute filled | `filled` | `14` |
| Full squares | `full` | `2` |
| Remainder | `rem` | `0` |
| After filling prefix | `ans` | `[7, 7, 0, 0, 0]` |
| After partial square | `ans` | `[7, 7, 0, 0, 0]` |

Final output:

```
7 7 0 0 0
```

This example demonstrates the boundary case where the percentage lands exactly at the end of a square. No partial square is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through the array once |
| Space | O(n) | The answer array stores `n` integers |

With `n ≤ 100`, the running time is tiny. Even much slower approaches would pass comfortably, but the direct construction is both simpler and mathematically cleaner.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n, k, t = map(int, input().split())

    filled = n * k * t // 100

    full = filled // k
    rem = filled % k

    ans = [0] * n

    for i in range(full):
        ans[i] = k

    if full < n:
        ans[full] = rem

    print(*ans)

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
assert run("10 10 54\n") == "10 10 10 10 10 4 0 0 0 0\n", "sample 1"

# minimum size, empty bar
assert run("1 1 0\n") == "0\n", "minimum empty"

# minimum size, full bar
assert run("1 1 100\n") == "1\n", "minimum full"

# exact boundary between squares
assert run("5 7 40\n") == "7 7 0 0 0\n", "exact full squares"

# partial middle square
assert run("3 10 50\n") == "10 5 0\n", "partial square"

# larger values
assert run("100 100 1\n") == (
    "100 " + "0 " * 99
).strip() + "\n", "small percentage"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `0` | Minimum constraints with empty progress |
| `1 1 100` | `1` | Minimum constraints with full progress |
| `5 7 40` | `7 7 0 0 0` | Exact division with no partial square |
| `3 10 50` | `10 5 0` | Correct remainder handling |
| `100 100 1` | `100 0 0 ...` | Large dimensions and tiny percentage |

## Edge Cases

Consider the completely empty progress bar:

Input:

```
4 9 0
```

The algorithm computes:

$$filled = 4 \times 9 \times 0 / 100 = 0$$

Then:

- `full = 0`
- `rem = 0`

No prefix squares are filled, and the array remains:

```
0 0 0 0
```

This confirms the algorithm correctly handles zero progress without accidentally filling any cells.

Now consider a completely full progress bar:

Input:

```
4 9 100
```

We get:

$$filled = 36$$

Then:

- `full = 4`
- `rem = 0`

All four positions become `9`. The condition:

```
if full < n:
```

prevents writing to index `4`, which does not exist.

Final output:

```
9 9 9 9
```

Another subtle case is a partially filled square.

Input:

```
3 10 50
```

The total filled amount is:

$$15$$

So:

- `full = 1`
- `rem = 5`

The algorithm creates:

```
10 5 0
```

This verifies that the remainder becomes exactly one partial square and does not spill into later positions.
