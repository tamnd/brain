---
title: "CF 1750C - Complementary XOR"
description: "We are given two binary strings of equal length. A single operation chooses a segment ([l,r]). Every bit of string (a) inside the segment is flipped, while every bit of string (b) outside the segment is flipped. The goal is not to transform one string into the other."
date: "2026-06-09T15:10:07+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1750
codeforces_index: "C"
codeforces_contest_name: "CodeTON Round 3 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1400
weight: 1750
solve_time_s: 431
verified: false
draft: false
---

[CF 1750C - Complementary XOR](https://codeforces.com/problemset/problem/1750/C)

**Rating:** 1400  
**Tags:** constructive algorithms, implementation  
**Solve time:** 7m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two binary strings of equal length. A single operation chooses a segment ([l,r]). Every bit of string (a) inside the segment is flipped, while every bit of string (b) outside the segment is flipped.

The goal is not to transform one string into the other. The goal is stronger: after applying some sequence of operations, every character of both strings must become zero. We must either construct such a sequence using at most (n+5) operations or prove that no solution exists.

The length of all strings across all test cases is at most (2 \cdot 10^5). Any solution that explicitly simulates every operation on every character would be too expensive. We need a construction whose total work is linear in the input size.

A subtle point is that the operation affects both strings simultaneously. Looking at only one string hides the structure of the problem. Another easy mistake is assuming that every pair of strings can be solved. Some pairs are fundamentally impossible.

Consider:

```
n = 2
a = 11
b = 10
```

The answer is NO. A construction that only focuses on turning (a) into zero may incorrectly claim success.

Another interesting case is:

```
n = 3
a = 010
b = 101
```

Here every position differs. The answer is YES, even though the strings are complements of each other.

A third edge case is:

```
n = 3
a = 111
b = 111
```

The strings are identical and the answer is YES, but some extra adjustment operations are required after clearing the ones in (a).

## Approaches

A brute-force viewpoint is to treat each pair of strings as a state in a graph and search for a sequence of operations. Each test case has (O(n^2)) possible operations, while the number of states is (2^{2n}). Even for very small (n), this becomes impossible.

The key observation comes from examining what happens to a single position.

Choose an operation on segment ([l,r]). For a position (i):

- If (i \in [l,r]), then (a_i) flips and (b_i) does not.
- If (i \notin [l,r]), then (a_i) does not flip and (b_i) flips.

Exactly one bit of the pair ((a_i,b_i)) is flipped.

This means the relation between (a_i) and (b_i) changes every time. If they were equal, they become different. If they were different, they become equal.

Therefore every operation toggles the equality status of every position simultaneously.

Let

[
c_i = a_i \oplus b_i.
]

Each operation flips every value (c_i). So after any sequence of operations, the vector (c) can only be either its original form or its bitwise complement.

For the final state we need (a_i=b_i=0), which implies (c_i=0) for every position.

Hence a solution exists only if initially:

- all (c_i=0), meaning (a=b), or
- all (c_i=1), meaning (a) and (b) are complements.

If neither condition holds, the answer is impossible.

Once this condition is satisfied, constructing the operations becomes easy. We use operations on single positions to eliminate every (1) in string (a). After doing this, the resulting global parity determines whether we end in the all-equal case or the all-complement case. A tiny fixed correction of three operations resolves the remaining parity issue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| State-space search | Exponential | Exponential | Too slow |
| Constructive greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Check whether every position satisfies (a_i=b_i).
2. Check whether every position satisfies (a_i\neq b_i).
3. If neither condition holds, print `NO`.
4. Otherwise, start with an empty list of operations.
5. For every position (i) where (a_i=1), add operation ((i,i)).

A length-one operation flips exactly one bit of (a). Repeating this for every one makes (a) become all zeros.
6. Let (cnt) be the number of ones in the original string (a).
7. If the strings were initially equal:

- If (cnt) is even, we are already done.
- If (cnt) is odd, append three operations:
[
(1,n),\ (1,1),\ (2,n).
]
8. If the strings were initially complements:

- If (cnt) is odd, we are already done.
- If (cnt) is even, append the same three operations:
[
(1,n),\ (1,1),\ (2,n).
]
9. Output all recorded operations.

### Why it works

Suppose we perform a length-one operation for every position where (a_i=1).

Each such operation flips one bit of (a), so eventually (a) becomes all zeros.

The only remaining question is the state of (b). The answer depends on the parity of the number of performed operations.

Every operation toggles the global relation between the strings. If we start from equal strings, then after an even number of operations they remain equal, and after an odd number they become complements. Since (a) is already all zeros, equality means (b) is also all zeros.

If we start from complementary strings, the opposite parity is required.

The three extra operations are a parity-adjustment gadget. Their combined effect on the strings is neutral, but they change the number of operations by three, which flips the required parity. This allows us to satisfy the correct final relation in all cases.

Because the existence condition is both necessary and sufficient, the construction is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()

        same = all(a[i] == b[i] for i in range(n))
        comp = all(a[i] != b[i] for i in range(n))

        if not same and not comp:
            out.append("NO")
            continue

        ops = []

        ones = 0
        for i, ch in enumerate(a, start=1):
            if ch == '1':
                ops.append((i, i))
                ones += 1

        need_flip = False

        if same:
            need_flip = (ones % 2 == 1)
        else:
            need_flip = (ones % 2 == 0)

        if need_flip:
            ops.append((1, n))
            ops.append((1, 1))
            ops.append((2, n))

        out.append("YES")
        out.append(str(len(ops)))
        for l, r in ops:
            out.append(f"{l} {r}")

    sys.stdout.write("\n".join(out))

solve()
```

The first part checks the only two configurations that can ever reach the target state: identical strings and complementary strings.

The next loop records one single-position operation for every one in (a). This is the simplest way to force (a) to become all zeros.

The parity logic is the heart of the construction. After clearing all ones, only the global equality/complement relation matters. Depending on the starting relation, we either need an even or odd number of operations.

The final three operations are always valid because (n \ge 2). Their combined effect preserves the achieved configuration while changing the parity of the operation count.

## Worked Examples

### Example 1

Input:

```
n = 3
a = 010
b = 101
```

| Step | Action | Operations Count |
| --- | --- | --- |
| Initial | Strings are complements | 0 |
| Position 2 is 1 | Add (2,2) | 1 |
| Ones count = 1 | Odd parity already correct | 1 |

Output:

```
YES
1
2 2
```

This example shows the complementary case. An odd number of single-position operations already gives the required parity.

### Example 2

Input:

```
n = 3
a = 111
b = 111
```

| Step | Action | Operations Count |
| --- | --- | --- |
| Initial | Strings are equal | 0 |
| Add (1,1) | Clear first one | 1 |
| Add (2,2) | Clear second one | 2 |
| Add (3,3) | Clear third one | 3 |
| Odd parity, correction needed | Add three extra operations | 6 |

The number of ones is odd. Equality requires an even number of effective toggles, so the parity-adjustment gadget is added.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | Stores at most (n+3) operations |

The total length over all test cases is at most (2 \cdot 10^5), so linear processing easily fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    res = []

    for _ in range(t):
        n = int(input())
        a = input().strip()
        b = input().strip()

        same = all(a[i] == b[i] for i in range(n))
        comp = all(a[i] != b[i] for i in range(n))

        if not same and not comp:
            res.append("NO")
            continue

        ops = []
        ones = 0

        for i, ch in enumerate(a, 1):
            if ch == '1':
                ops.append((i, i))
                ones += 1

        need = (ones % 2 == 1) if same else (ones % 2 == 0)

        if need:
            ops.append((1, n))
            ops.append((1, 1))
            ops.append((2, n))

        res.append("YES")
        res.append(str(len(ops)))

    return "\n".join(res)

assert run(
"""1
3
010
101
"""
).startswith("YES")

assert run(
"""1
2
11
10
"""
) == "NO"

assert run(
"""1
4
1000
0011
"""
) == "NO"

assert run(
"""1
2
10
10
"""
).startswith("YES")

assert run(
"""1
2
01
10
"""
).startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11 / 10` | NO | Mixed equality pattern is impossible |
| `1000 / 0011` | NO | Another impossible configuration |
| `10 / 10` | YES | Equal strings |
| `01 / 10` | YES | Complementary strings |
| `111 / 111` | YES | Parity-adjustment path |

## Edge Cases

Consider:

```
n = 2
a = 11
b = 10
```

Position 1 is equal while position 2 is different. The equality pattern is mixed. Since every operation flips the status of all positions simultaneously, mixed patterns can never become all zeros. The algorithm immediately prints `NO`.

Consider:

``
