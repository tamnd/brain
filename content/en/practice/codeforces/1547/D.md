---
title: "CF 1547D - Co-growing Sequence"
description: "We are given a sequence $x1, x2, dots, xn$. Our task is to construct another sequence $y1, y2, dots, yn$ such that when we XOR them elementwise, the resulting sequence $$ai = xi oplus yi$$ has a monotone bit-structure: every bit that is set in $ai$ must also be set in $a{i+1}$."
date: "2026-06-14T19:58:01+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1547
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 731 (Div. 3)"
rating: 1300
weight: 1547
solve_time_s: 503
verified: false
draft: false
---

[CF 1547D - Co-growing Sequence](https://codeforces.com/problemset/problem/1547/D)

**Rating:** 1300  
**Tags:** bitmasks, constructive algorithms, greedy  
**Solve time:** 8m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence $x_1, x_2, \dots, x_n$. Our task is to construct another sequence $y_1, y_2, \dots, y_n$ such that when we XOR them elementwise, the resulting sequence

$$a_i = x_i \oplus y_i$$

has a monotone bit-structure: every bit that is set in $a_i$ must also be set in $a_{i+1}$. In bitwise terms, this means

$$a_i \& a_{i+1} = a_i.$$

So the sequence $a_i$ is non-decreasing in the sense of set bits: once a bit becomes 1, it can never become 0 later.

We do not construct $a_i$ directly. Instead, we must choose $y_i$, and among all valid choices, we must minimize the sequence lexicographically.

The key interaction is that each $y_i$ controls $a_i$ through XOR. Since XOR flips bits independently, each position $i$ can be thought of as choosing $a_i$, and then deriving $y_i = a_i \oplus x_i$, but with the constraint that the resulting $a$-sequence must satisfy the growing condition.

The constraints are large: total $n$ across tests is up to $2 \cdot 10^5$. This forces a linear or near-linear solution per test. Anything that tries to consider all possible bit patterns or backtrack over choices is immediately too slow.

A naive approach would try to build $y_i$ greedily but check validity of the full prefix each time, or even attempt to choose each bit independently while maintaining consistency. The issue is that the constraint couples all positions through bit persistence, so local decisions can break future feasibility.

A simple failure case appears when greedily minimizing $y_i$ independently:

```
x = [1, 2]
```

If we pick $y_1 = 0$, then $a_1 = 1$. At $i=2$, if we again pick $y_2 = 0$, then $a_2 = 2$, and we get $1 \& 2 = 0 \neq 1$, invalid. Fixing this requires anticipating constraints from future positions.

So the main difficulty is that each $a_i$ must be a superset (in bitwise sense) of previous ones, while still keeping $y_i$ small lexicographically.

## Approaches

A brute-force idea is to try all possible $y_1$, compute $a_1$, then enforce that each subsequent $a_i$ must be a superset of all previous $a$'s. At step $i$, we would try all $y_i$ such that $a_i = x_i \oplus y_i$ satisfies the growing constraint with $a_{i-1}$. This means enumerating all bitmasks for each position, and for each candidate checking compatibility.

Since each $x_i < 2^{30}$, each $y_i$ also lies in a 30-bit space, giving up to $2^{30}$ possibilities per position. Even pruning by constraints still leaves an exponential search. This is clearly infeasible.

The key observation is that the constraint on $a_i$ is monotone in terms of bit inclusion: once a bit becomes 1 in some $a_i$, it must stay 1 forever. This suggests maintaining a global bitmask $S$, representing all bits that have already been forced to 1 in previous $a$-values.

At position $i$, we must ensure that $a_i$ contains all bits in $S$. The lexicographically minimal choice for $y_i$ corresponds to making $a_i$ as small as possible while still including $S$. Since $a_i = x_i \oplus y_i$, we can instead decide $a_i$ as:

- all bits in $S$ must be 1
- additional bits can be optionally 1 if they help future constraints, but any extra 1 only hurts lexicographically later choices

Thus the optimal strategy is to enforce $a_i = x_i \,|\, S$. Any bit already required by previous steps must appear, and introducing new bits only increases $S$, which would worsen future constraints and potentially force larger values in lexicographic order of $y$.

Once $a_i$ is fixed, we recover $y_i = a_i \oplus x_i$, and update $S = S \,|\, a_i$.

This reduces the problem to a single left-to-right pass maintaining a bitmask.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a bitmask $S = 0$. This represents bits that must remain present in all future $a_i$.
2. Iterate over the sequence from left to right. At position $i$, compute a candidate

$$a_i = x_i \,|\, S.$$

This ensures that all previously required bits are preserved.
3. Compute $y_i = a_i \oplus x_i$. This is the minimal value of $y_i$ that transforms $x_i$ into $a_i$, since XOR flips exactly the bits where $x_i$ and $a_i$ differ.
4. Update the global constraint:

$$S = S \,|\, a_i.$$

This expands the set of bits that must remain present going forward.
5. Output $y_i$ immediately, since future decisions do not affect past values.

### Why it works

The invariant is that after processing position $i$, the current set $S$ equals the bitwise union of all constructed $a_1, \dots, a_i$. Any valid future $a_j$ must include all bits in $S$, otherwise it would violate the growing condition with some earlier index where that bit first appeared.

At each step, choosing $a_i = x_i | S$ gives the smallest possible valid $a_i$ under this constraint. Any smaller choice would miss a bit in $S$ and break validity. Any larger choice would introduce unnecessary bits, which would increase $y_i$ or force future updates that can only increase lexicographic order. Since lexicographic comparison depends on the earliest differing position, minimizing each $y_i$ under the tightest valid constraint yields the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        
        S = 0
        res = []
        
        for xi in x:
            ai = xi | S
            yi = ai ^ xi
            res.append(str(yi))
            S |= ai
        
        out.append(" ".join(res))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation maintains the evolving constraint mask `S`. At each step, we construct the smallest valid $a_i$ by OR-ing with `S`, then derive $y_i$ via XOR. The update `S |= a_i` ensures that all bits that have ever appeared in any $a_i$ are preserved for the rest of the sequence.

A subtle point is that we never need to explicitly check the growing condition, because the construction of `S` guarantees it inductively. Each `a_i` already contains all previous bits, so `a_{i-1} & a_i = a_{i-1}` holds automatically.

## Worked Examples

Consider the input:

```
n = 4
x = [1, 2, 3, 4]
```

We track `S`, `a_i`, and `y_i`.

| i | x_i | S before | a_i = x_i | S before OR x_i | y_i | S after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 | 3 | 1 | 3 |
| 3 | 3 | 3 | 3 | 3 | 0 | 3 |
| 4 | 4 | 3 | 7 | 7 | 3 | 7 |

The final sequence is $y = [0, 1, 0, 3]$. Each step ensures that all previously activated bits remain present, confirming the growing condition is preserved.

Now consider:

```
x = [5, 4, 3]
```

| i | x_i | S before | a_i | y_i | S after |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 5 | 0 | 5 |
| 2 | 4 | 5 | 5 | 1 | 5 |
| 3 | 3 | 5 | 7 | 4 | 7 |

Here the third step forces new bits to satisfy previous constraints, demonstrating how the mask can only grow.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time bit operations |
| Space | O(1) | Only a few integers are maintained regardless of input size |

The total complexity over all test cases remains linear in the input size, matching the constraint $\sum n \le 2 \cdot 10^5$. This is well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n = int(sys.stdin.readline())
        x = list(map(int, sys.stdin.readline().split()))
        S = 0
        res = []
        for xi in x:
            ai = xi | S
            yi = ai ^ xi
            res.append(str(yi))
            S |= ai
        out.append(" ".join(res))
    return "\n".join(out)

# provided samples
assert run("""5
4
1 3 7 15
4
1 2 4 8
5
1 2 3 4 5
4
11 13 15 1
1
0
""") == """0 0 0 0
0 1 3 7
0 1 0 3 2
0 2 0 14
0""", "sample tests"

# custom cases
assert run("""1
1
0
""") == "0", "single zero"

assert run("""1
3
0 0 0
""") == "0 0 0", "all zeros"

assert run("""1
3
7 0 0
""") == "0 7 7", "decreasing x forces accumulation"

assert run("""1
4
1 2 4 8
""") == "0 1 3 7", "powers of two case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 0 | trivial base case |
| all zeros | 0 0 0 | stability under no bits |
| 7 0 0 | 0 7 7 | propagation of forced bits |
| powers of two | 0 1 3 7 | cumulative bit growth |

## Edge Cases

One edge case is when all bits are zero initially. For input `x = [0, 0, 0]`, the algorithm keeps `S = 0`, so every `a_i = 0` and every `y_i = 0`. The growing condition holds trivially since all masks are identical.

Another edge case occurs when early elements introduce high bits that later elements do not contain. For `x = [1, 2, 4]`, the mask grows as follows: after the first step `S = 1`, forcing the second `a_2 = 3`, then `S = 3`, and finally `a_3 = 7`. The algorithm correctly inflates later values to preserve earlier bits, ensuring monotonic bit inclusion even when original values decrease.

A final subtle case is a single-element sequence. Since there are no constraints between elements, the answer is simply $y_1 = 0$, because choosing $a_1 = x_1$ is always valid and minimizes XOR.
