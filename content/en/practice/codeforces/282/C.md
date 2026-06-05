---
title: "CF 282C - XOR and OR"
description: "We are given two binary strings. An operation chooses any adjacent pair of bits. If the pair is (x, y), we compute: - p = x xor y - q = x or y We then write p into one position and q into the other position, in either order. The length of the string never changes."
date: "2026-06-05T09:17:08+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 282
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 173 (Div. 2)"
rating: 1500
weight: 282
solve_time_s: 94
verified: true
draft: false
---

[CF 282C - XOR and OR](https://codeforces.com/problemset/problem/282/C)

**Rating:** 1500  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two binary strings. An operation chooses any adjacent pair of bits. If the pair is `(x, y)`, we compute:

- `p = x xor y`
- `q = x or y`

We then write `p` into one position and `q` into the other position, in either order.

The length of the string never changes. Starting from string `a`, we must determine whether some sequence of such operations can transform it into string `b`.

The strings can be as long as one million characters. That immediately rules out any approach that tries to simulate transformations or search through reachable states. Even a linear scan is already processing one million characters, so the target complexity should be `O(n)`.

The tricky part is understanding what information the operation preserves and what information it can change.

A first non-obvious edge case is when the lengths differ.

Input:

```
1
11
```

Output:

```
NO
```

Every operation acts on two existing positions and never inserts or removes characters. Length is invariant, so strings of different lengths can never be transformed into each other.

Another important case is when one string contains only zeros.

Input:

```
000
001
```

Output:

```
NO
```

Starting from all zeros, every adjacent pair is `(0,0)`. The operation produces `(0 xor 0, 0 or 0) = (0,0)`, so the string never changes. A careless solution that only checks lengths would incorrectly answer YES.

A more subtle case is:

Input:

```
10
01
```

Output:

```
YES
```

The operation on `(1,0)` gives `(1,1)` and `(0,1)` as possible outputs. Choosing the second arrangement directly produces `01`. A solution that tracks exact positions of ones would fail because ones can move around.

Another edge case is:

Input:

```
111
000
```

Output:

```
NO
```

Although operations can reduce the number of ones, they can never eliminate the last remaining one. The presence of at least one `1` turns out to be the key invariant.

## Approaches

A brute-force approach would view every binary string of a fixed length as a state and perform a graph search over all reachable states. For a length `n`, there are `2^n` possible strings. Even for `n = 50`, that number is already astronomically large, and the actual limit is `10^6`. State-space exploration is completely impossible.

To find a better solution, we need to understand what the operation actually does.

Consider all possible adjacent pairs:

| Original | xor | or |
| --- | --- | --- |
| 00 | 0 | 0 |
| 01 | 1 | 1 |
| 10 | 1 | 1 |
| 11 | 0 | 1 |

The crucial observation is that the pair after the operation contains a `1` if and only if the original pair contained a `1`.

For `00`, the result is still `00`.

For `01` and `10`, the result becomes two bits whose values are `{1,1}`.

For `11`, the result becomes `{0,1}`.

In every case, a pair that contains at least one `1` continues to contain at least one `1`. A pair with no `1` never gains one.

This means the entire string can never lose its final remaining `1`, and an all-zero string can never create a `1`.

The next question is whether that is the only restriction.

Suppose the string contains at least one `1`. Then we can repeatedly use operations to move that `1` around and create any desired arrangement of zeros and ones. In fact, any two strings of the same length that both contain at least one `1` are mutually reachable. This is the key theorem behind the problem.

The transformation question therefore reduces to only two checks:

1. The lengths must be equal.
2. Either both strings contain at least one `1`, or both strings contain no `1`.

That gives a simple linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(2^n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read strings `a` and `b`.
2. If their lengths differ, print `"NO"`.

The operation never changes the number of positions, so different lengths are impossible.
3. Check whether `a` contains at least one `'1'`.
4. Check whether `b` contains at least one `'1'`.
5. If both checks have the same result, print `"YES"`.

This covers two situations:

- Both strings are all zeros.
- Both strings contain at least one `1`.
6. Otherwise print `"NO"`.

### Why it works

The operation preserves the property "does this string contain at least one `1`?". An all-zero string remains all-zero forever because every operation on `00` produces `00`. Conversely, if a string contains a `1`, every operation preserves the existence of at least one `1`, so the final `1` can never disappear.

The deeper fact is that once a string contains at least one `1`, that `1` can be propagated and moved through the string. Using repeated operations, we can transform any non-zero binary string into any other non-zero binary string of the same length. Thus, among strings of a fixed length, there are exactly two connected components: the all-zero string and all strings containing at least one `1`.

The algorithm checks exactly these invariants, so it is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = input().strip()
b = input().strip()

if len(a) != len(b):
    print("NO")
elif ('1' in a) == ('1' in b):
    print("YES")
else:
    print("NO")
```

The first condition handles the invariant that length never changes.

The second condition checks whether both strings belong to the same reachability class. The expression `('1' in a)` evaluates to `True` if the string contains at least one one-bit and `False` otherwise. Reachability requires these values to match.

No simulation is needed. The entire solution is based on the structural property of the operation.

A common mistake is trying to compare the number of ones. The count of ones is not preserved. For example, `11` can become `01`, reducing the count from two to one. The only preserved property is whether the count is zero or positive.

## Worked Examples

### Example 1

Input:

```
11
10
```

| Variable | Value |
| --- | --- |
| a | 11 |
| b | 10 |
| len(a) == len(b) | True |
| '1' in a | True |
| '1' in b | True |

Result:

```
YES
```

Both strings have the same length and both contain at least one `1`. They belong to the same reachability class.

### Example 2

Input:

```
000
001
```

| Variable | Value |
| --- | --- |
| a | 000 |
| b | 001 |
| len(a) == len(b) | True |
| '1' in a | False |
| '1' in b | True |

Result:

```
NO
```

The starting string is the unique all-zero state. Since no operation can create a `1`, reaching `001` is impossible.

This example demonstrates the key invariant preserved by every operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Membership checks for `'1'` scan each string once |
| Space | O(1) | Only a few variables are used |

With lengths up to `10^6`, a linear scan is easily fast enough. The memory usage stays constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    a = input().strip()
    b = input().strip()

    if len(a) != len(b):
        print("NO")
    elif ('1' in a) == ('1' in b):
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("11\n10\n") == "YES", "sample 1"

# minimum size
assert run("0\n0\n") == "YES", "single zero"

# minimum size, different classes
assert run("0\n1\n") == "NO", "cannot create a one"

# all-zero strings
assert run("00000\n00000\n") == "YES", "all-zero component"

# same length, both non-zero
assert run("1000\n0001\n") == "YES", "all non-zero strings are connected"

# different lengths
assert run("1\n11\n") == "NO", "length is invariant"

# large-style boundary case
assert run(("1" + "0" * 20) + "\n" + ("0" * 20 + "1") + "\n") == "YES", "non-zero strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 / 0` | YES | Smallest possible valid input |
| `0 / 1` | NO | Impossible to create a one |
| `00000 / 00000` | YES | All-zero component |
| `1000 / 0001` | YES | Position of ones does not matter |
| `1 / 11` | NO | Length invariant |
| Large non-zero pair | YES | Any non-zero strings of equal length are connected |

## Edge Cases

Consider:

```
0
0
```

The algorithm first checks lengths, which match. Both strings have no `'1'`, so the boolean values are equal and the answer is YES. This is correct because zero operations already achieve the target.

Consider:

```
0
1
```

Lengths match, but `'1' in a` is `False` while `'1' in b` is `True`. The algorithm outputs NO. Since `00 -> 00` is the only behavior available in an all-zero string, creating a one-bit is impossible.

Consider:

```
111
000
```

Both strings have equal length. The first contains a `1`, the second does not. The algorithm outputs NO. Every operation preserves the existence of at least one `1`, so the last remaining one can never disappear.

Consider:

```
10
01
```

Lengths match and both strings contain a `1`, so the algorithm outputs YES. Indeed, applying the operation to the pair `(1,0)` and choosing the arrangement `(0,1)` directly reaches the target.

These cases cover the only properties that matter: equal length and agreement on whether at least one `1` exists.
