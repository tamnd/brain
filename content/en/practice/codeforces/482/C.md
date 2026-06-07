---
title: "CF 482C - Game with Strings"
description: "We know all candidate strings in advance. One of them is chosen uniformly at random. We reveal information by asking about character positions. The order of questions is not chosen strategically. At every step we pick uniformly among positions that have not been asked yet."
date: "2026-06-07T17:20:13+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 482
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 275 (Div. 1)"
rating: 2600
weight: 482
solve_time_s: 222
verified: true
draft: false
---

[CF 482C - Game with Strings](https://codeforces.com/problemset/problem/482/C)

**Rating:** 2600  
**Tags:** bitmasks, dp, probabilities  
**Solve time:** 3m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We know all candidate strings in advance. One of them is chosen uniformly at random. We reveal information by asking about character positions.

The order of questions is not chosen strategically. At every step we pick uniformly among positions that have not been asked yet.

After some positions have been revealed, several strings may still be compatible with all answers seen so far. The game stops as soon as only one string remains possible. We must compute the expected number of questions asked.

The key parameters are small in a very specific way. There are at most 50 strings, but the string length is at most 20. A length of 20 immediately suggests that subsets of positions are manageable because $2^{20} = 1{,}048{,}576$. That is large, but still within reach for a carefully designed bitmask DP. On the other hand, any state involving arbitrary subsets of strings would be impossible because there can be 50 strings.

A subtle point is that the random process depends only on which positions have already been asked, not on the order in which they were asked. Once a set of positions is known, the remaining candidate strings are completely determined.

Several edge cases are easy to mishandle.

Consider a single string:

```
1
abc
```

The correct answer is 0. The chosen string is already known before asking anything. A solution that blindly assumes at least one question is required would fail.

Consider two strings differing in only one position:

```
2
aab
aac
```

The game may require 1, 2, or 3 questions depending on when the distinguishing position is asked. A solution that only counts distinguishing positions and ignores the random ordering would produce the wrong expectation.

Consider strings that become distinguishable only after combining information from multiple positions:

```
3
ab
ac
cb
```

No single position uniquely identifies every string. The DP must track the entire set of revealed positions, not just how many positions have been revealed.

## Approaches

A brute force view is straightforward. Let the state be:

- the chosen string,
- the set of positions already asked.

From such a state we can determine whether the string is already uniquely identified. If not, we randomly choose an unasked position and continue recursively.

This gives a correct recurrence, but the state space contains

$$n \cdot 2^m$$

states. With $n=50$ and $m=20$, that is more than fifty million states. Even storing them is impractical.

The observation that unlocks the problem is that we never actually need separate DP values for different chosen strings.

Fix a set of already asked positions $M$.

For a particular string $i$, define it as unresolved if at least one other string is still consistent with all answers on positions in $M$.

Suppose $F(M)$ is the sum of expected remaining questions over all possible chosen strings.

For every unresolved string we must spend one more question before moving to a child state. For every resolved string the expectation is already zero.

This allows us to write a recurrence involving only the position mask $M$. The chosen string disappears from the DP state entirely.

The remaining challenge is computing, for every mask $M$, how many strings are unresolved. This is where the small string length becomes useful.

For two strings $i$ and $j$, let `diff(i,j)` be the set of positions where they differ.

They are still indistinguishable after asking positions $M$ exactly when none of those differing positions has been revealed:

$$M \cap diff(i,j)=\varnothing$$

Equivalently,

$$M \subseteq (\text{all positions}) \setminus diff(i,j)$$

This becomes a classic subset-SOS propagation problem over $2^m$ masks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over (string, mask) states | $O(n2^m m)$ states and transitions | $O(n2^m)$ | Too slow |
| Bitmask DP + SOS propagation | $O(m2^m)$ | $O(2^m)$ | Accepted |

## Algorithm Walkthrough

1. Number the positions from 0 to $m-1$.
2. For every ordered pair of distinct strings $(i,j)$, build a mask `sameMask` containing positions where the two strings are equal.

If the currently revealed positions are a subset of `sameMask`, then strings $i$ and $j$ are still indistinguishable.
3. Create an array `alive[mask]` of 64-bit bitsets.

For every ordered pair $(i,j)$, set bit `i` inside `alive[sameMask]`.

This records that string `i` is unresolved whenever the revealed-position mask is a subset of `sameMask`.
4. Run SOS propagation from supersets to subsets.

After propagation, `alive[M]` contains exactly the set of strings that are still unresolved after revealing positions `M`.

The propagation works because every subset of `sameMask` inherits the indistinguishability relation.
5. Define

$$K(M)=\text{number of set bits in } alive[M]$$

This is the number of strings that are not uniquely identified yet.
6. Let `dp[M]` be the sum of expected remaining questions over all possible chosen strings when positions `M` have already been revealed.
7. Process masks in decreasing order.

If `rem` positions remain unasked, then

$$dp[M]
=
K(M)
+
\frac{1}{rem}
\sum_{p \notin M}
dp[M \cup \{p\}]$$

The first term contributes one question for every unresolved string. The second term averages over the random choice of the next position.
8. The full-mask state has no children. Its value is simply `K(fullMask)`, which is zero.
9. The required answer is

$$\frac{dp[0]}{n}$$

because `dp[0]` is the sum of expectations over all equally likely chosen strings.

### Why it works

For a fixed revealed-position mask $M$, every chosen string falls into one of two categories.

If it is already uniquely identified, its remaining expectation is zero.

If it is not uniquely identified, exactly one more question is asked before moving to a child mask chosen uniformly among the remaining positions.

Summing these equations over all strings produces the recurrence for `dp[M]`. No information about the individual chosen string is needed anymore; only the count of unresolved strings matters.

The SOS phase correctly computes unresolved strings because two strings remain indistinguishable precisely when all revealed positions belong to their equality mask. Propagating information from a mask to all of its subsets enumerates exactly those revealed-position sets.

Together, these two facts completely characterize the random process, so the DP computes the exact expectation.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    s = [input().strip() for _ in range(n)]

    m = len(s[0])
    N = 1 << m
    full = N - 1

    alive = array('Q', [0]) * N

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            same_mask = 0
            si = s[i]
            sj = s[j]

            for k in range(m):
                if si[k] == sj[k]:
                    same_mask |= 1 << k

            alive[same_mask] |= (1 << i)

    for b in range(m):
        bit = 1 << b
        for mask in range(N):
            if (mask & bit) == 0:
                alive[mask] |= alive[mask | bit]

    pc = bytearray(N)
    for mask in range(1, N):
        pc[mask] = pc[mask >> 1] + (mask & 1)

    dp = array('d', [0.0]) * N

    for mask in range(full, -1, -1):
        unresolved = alive[mask].bit_count()

        rem = m - pc[mask]
        if rem == 0:
            dp[mask] = float(unresolved)
            continue

        total = 0.0
        free = full ^ mask

        while free:
            bit = free & -free
            total += dp[mask | bit]
            free ^= bit

        dp[mask] = unresolved + total / rem

    print("{:.15f}".format(dp[0] / n))

solve()
```

The `alive` array is the heart of the preprocessing. Each entry stores a 64-bit bitset because $n \le 50$, so every string fits into one machine word.

The SOS propagation moves information from a mask to all of its subsets. After it finishes, `alive[M]` already contains the exact set of unresolved strings for that revealed-position mask.

The DP runs in reverse mask order. Every transition goes to a strict superset, so all child states are already computed.

One implementation detail that is easy to get wrong is the interpretation of `K(M)`. It is not the number of candidate strings remaining. It is the number of chosen strings that are still unresolved. Those are different quantities.

Another subtle point is the use of ordered pairs. If string `i` can still be confused with string `j`, then string `i` must be marked unresolved. The reverse direction must also be recorded separately.

## Worked Examples

### Sample 1

Input:

```
2
aab
aac
```

The strings differ only at position 2.

| Mask | Revealed positions | Unresolved strings K(mask) |
| --- | --- | --- |
| 000 | none | 2 |
| 001 | pos 0 | 2 |
| 010 | pos 1 | 2 |
| 100 | pos 2 | 0 |
| 111 | all | 0 |

DP values:

| Mask | rem | dp |
| --- | --- | --- |
| 111 | 0 | 0 |
| 110 | 1 | 0 |
| 101 | 1 | 0 |
| 011 | 1 | 2 |
| 100 | 2 | 0 |
| 010 | 2 | 3 |
| 001 | 2 | 3 |
| 000 | 3 | 4 |

The answer is:

$$dp[0]/2 = 2$$

which matches the sample.

This trace shows that the DP is summing expectations over both possible chosen strings simultaneously.

### Example 2

Input:

```
3
ab
ac
cb
```

| Mask | Revealed positions | K(mask) |
| --- | --- | --- |
| 00 | none | 3 |
| 01 | first position | 2 |
| 10 | second position | 2 |
| 11 | both positions | 0 |

DP computation:

| Mask | rem | dp |
| --- | --- | --- |
| 11 | 0 | 0 |
| 10 | 1 | 2 |
| 01 | 1 | 2 |
| 00 | 2 | 5 |

Final answer:

$$5/3$$

This example demonstrates that one revealed position is not always enough even when it eliminates some candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m2^m)$ | SOS propagation and DP each process every mask for every position |
| Space | $O(2^m)$ | Bitset array, popcount array, and DP array |

With $m \le 20$, we have at most $2^{20} = 1{,}048{,}576$ masks. Both the memory usage and the number of operations fit comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from array import array

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    s = [input().strip() for _ in range(n)]

    m = len(s[0])
    N = 1 << m
    full = N - 1

    alive = array('Q', [0]) * N

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            same_mask = 0
            for k in range(m):
                if s[i][k] == s[j][k]:
                    same_mask |= 1 << k

            alive[same_mask] |= (1 << i)

    for b in range(m):
        bit = 1 << b
        for mask in range(N):
            if (mask & bit) == 0:
                alive[mask] |= al
```
