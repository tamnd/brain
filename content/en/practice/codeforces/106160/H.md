---
title: "CF 106160H - Homesick"
description: "We have two lowercase strings of equal length, S and T. One operation chooses a suffix of S and a value k between 1 and 25. Every character in that suffix is shifted forward by k positions in the alphabet, with wraparound from z back to a."
date: "2026-06-25T11:13:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "H"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 39
verified: true
draft: false
---

[CF 106160H - Homesick](https://codeforces.com/problemset/problem/106160/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two lowercase strings of equal length, `S` and `T`.

One operation chooses a suffix of `S` and a value `k` between 1 and 25. Every character in that suffix is shifted forward by `k` positions in the alphabet, with wraparound from `z` back to `a`.

The task is to transform `S` into `T` using as few operations as possible.

A useful way to think about the problem is to forget the actual letters and only track how much each position must be shifted. For every index `i`, define

$$d_i = (T_i - S_i) \bmod 26$$

This is the total shift that position `i` must receive.

The string length can be as large as `2 · 10^5`, so any algorithm that considers all pairs of positions or simulates operations character by character would be too slow. We need something linear or close to linear.

The tricky part is that an operation affects a suffix, not a single position. Changes applied earlier continue to influence all later positions.

Consider a small example:

```
S = aaa
T = bbb
```

Every position needs shift `1`, so

```
d = [1, 1, 1]
```

One operation on the whole string with `k = 1` is enough.

A careless approach might count three positions with nonzero shifts and answer `3`, which is incorrect.

Another interesting case is:

```
S = aaa
T = aba
```

Then

```
d = [0, 1, 0]
```

Position 2 must gain one shift, while position 3 must end up back at zero. Since suffix operations propagate to the right, we need:

```
+1 starting at position 2
+25 starting at position 3
```

The correct answer is `2`.

This illustrates that what matters is not the values `d_i` themselves, but how they change between neighboring positions.

## Approaches

The brute-force viewpoint is to construct operations explicitly.

Suppose we process positions from left to right. At each index we compare the accumulated shift so far with the required shift at that position, then add operations to fix the difference. This already hints at the correct structure, but if implemented by actually updating suffixes, each operation could touch `O(n)` positions. In the worst case that becomes `O(n^2)`, which is far too slow for `n = 2 · 10^5`.

The key observation is that a suffix operation does not change the difference between two positions inside that suffix. It only changes the point where the suffix begins.

Let

$$d_i = (T_i - S_i) \bmod 26$$

and define

$$d_0 = 0.$$

Suppose an operation starts at position `i` and shifts by `k`. Then it increases every `d_j` for `j ≥ i` by `k`, which means the only place where the "discrete derivative" changes is between positions `i-1` and `i`.

Define

$$\Delta_i = (d_i - d_{i-1}) \bmod 26.$$

A shift of `k` starting at position `i` contributes exactly `k` to `Δ_i` and nowhere else.

That means each position is completely independent in the difference array.

If `Δ_i = 0`, no operation is needed there.

If `Δ_i ≠ 0`, a single operation starting at position `i` with `k = Δ_i` creates exactly the required change.

Since one operation can realize any value from 1 to 25, every nonzero `Δ_i` costs exactly one operation.

The answer is simply the number of indices with

$$(d_i - d_{i-1}) \bmod 26 \ne 0.$$

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force suffix simulation | O(n²) | O(n) | Too slow |
| Difference-array observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `S`, and `T`.
2. For every position `i`, compute

$$d_i = (T_i - S_i) \bmod 26.$$

This is the total shift required at that position.
3. Let `prev = 0`, which represents `d_0`.
4. Traverse positions from left to right.
5. Compute

$$\Delta = (d_i - prev) \bmod 26.$$

This is the amount of new shift that must start exactly at this position.
6. If `Δ ≠ 0`, increase the answer by one.

A single suffix operation with shift `Δ` can create this change.
7. Set `prev = d_i` and continue.
8. Output the final count.

### Why it works

Every suffix operation affects all positions from its starting point onward. In the array of required shifts `d`, such an operation changes only one boundary: the transition between positions `i-1` and `i`.

The quantity

$$\Delta_i = (d_i - d_{i-1}) \bmod 26$$

records exactly how much shift must begin at position `i`.

A nonzero `Δ_i` cannot be produced by operations starting elsewhere, so at least one operation is necessary. Conversely, one operation with shift `Δ_i` produces exactly that requirement.

Thus every nonzero `Δ_i` contributes exactly one operation, and every zero `Δ_i` contributes none. Counting nonzero differences gives the minimum possible number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()
t = input().strip()

ans = 0
prev = 0

for i in range(n):
    cur = (ord(t[i]) - ord(s[i])) % 26
    delta = (cur - prev) % 26
    if delta != 0:
        ans += 1
    prev = cur

print(ans)
```

The variable `cur` stores the required total shift for the current position.

The variable `prev` stores the required shift of the previous position. Computing

```
(cur - prev) % 26
```

gives the difference-array value `Δ`.

Whenever that value is nonzero, we need exactly one operation starting at the current position.

The modulo operation is essential. For example, moving from required shift `1` to required shift `0` corresponds to

```
0 - 1 = -1
```

which should be interpreted as `25` in modulo 26 arithmetic. Forgetting the modulo would incorrectly treat this transition as negative.

## Worked Examples

### Example 1

```
S = aaaaaaaaa
T = aaabbbaaa
```

Required shifts:

```
d = [0,0,0,1,1,1,0,0,0]
```

| Position | d[i] | Previous d | Δ | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | 0 |
| 4 | 1 | 0 | 1 | 1 |
| 5 | 1 | 1 | 0 | 1 |
| 6 | 1 | 1 | 0 | 1 |
| 7 | 0 | 1 | 25 | 2 |
| 8 | 0 | 0 | 0 | 2 |
| 9 | 0 | 0 | 0 | 2 |

Final answer: `2`.

The first operation starts the shift region, and the second cancels it afterward.

### Example 2

```
S = aaa
T = bbb
```

Required shifts:

```
d = [1,1,1]
```

| Position | d[i] | Previous d | Δ | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 1 |

Final answer: `1`.

One operation on the entire string is enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the strings |
| Space | O(1) | Only a few variables are stored |

With `n ≤ 2 · 10^5`, a linear scan is easily fast enough for the time limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    ans = 0
    prev = 0

    for i in range(n):
        cur = (ord(t[i]) - ord(s[i])) % 26
        delta = (cur - prev) % 26
        if delta != 0:
            ans += 1
        prev = cur

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# provided samples
assert run("4\naaaa\naaaa\n") == "0\n"
assert run("9\naaaaaaaaa\naaabbbaaa\n") == "2\n"

# minimum size
assert run("1\na\nb\n") == "1\n"

# all positions need same shift
assert run("3\naaa\nbbb\n") == "1\n"

# alternating requirements
assert run("3\naaa\naba\n") == "2\n"

# wraparound case
assert run("2\nba\nab\n") == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a -> b` | `1` | Smallest nontrivial case |
| `aaa -> bbb` | `1` | One operation can affect many positions |
| `aaa -> aba` | `2` | Need both starting and canceling operations |
| `ba -> ab` | `2` | Correct modulo-26 handling |

## Edge Cases

Consider:

```
3
aaa
aba
```

Required shifts are:

```
[0, 1, 0]
```

The algorithm computes:

```
Δ = [0, 1, 25]
```

Both nonzero entries are counted, giving answer `2`.

One operation starts a `+1` shift at position 2. Another operation starts a `+25` shift at position 3, canceling the effect for the remainder of the string.

Now consider:

```
3
aaa
bbb
```

Required shifts:

```
[1, 1, 1]
```

Differences:

```
Δ = [1, 0, 0]
```

Only one nonzero entry exists, so the answer is `1`. This correctly captures that a single suffix operation on the entire string affects all three positions simultaneously.

Finally, consider a wraparound transition:

```
2
ba
ab
```

Required shifts:

```
[25, 1]
```

Differences:

```
Δ1 = 25
Δ2 = (1 - 25) mod 26 = 2
```

Both are nonzero, so the answer is `2`. The modulo arithmetic correctly handles the transition across the alphabet boundary.
