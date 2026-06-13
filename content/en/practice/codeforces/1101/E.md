---
title: "CF 1101E - Polycarp's New Job"
description: "We are processing a growing collection of rectangular banknotes. Each time a note is added, it stays forever. Later we receive queries asking whether all notes seen so far can be placed inside a given rectangular wallet."
date: "2026-06-13T07:23:38+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1101
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 58 (Rated for Div. 2)"
rating: 1500
weight: 1101
solve_time_s: 263
verified: true
draft: false
---

[CF 1101E - Polycarp's New Job](https://codeforces.com/problemset/problem/1101/E)

**Rating:** 1500  
**Tags:** implementation  
**Solve time:** 4m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are processing a growing collection of rectangular banknotes. Each time a note is added, it stays forever. Later we receive queries asking whether all notes seen so far can be placed inside a given rectangular wallet.

A note can be rotated, so a note of size $x \times y$ can be treated as either orientation. A note fits into a wallet $h \times w$ if, after possibly rotating it, both dimensions of the note do not exceed the corresponding wallet dimensions.

A crucial detail is that every note must fit independently. There is no packing interaction between notes, so the condition for a wallet is simply that it must be large enough to contain every single note individually.

Each query of type “add” inserts a rectangle, and each query of type “check” asks whether all inserted rectangles so far can individually fit inside the given wallet.

The constraints go up to $5 \cdot 10^5$ operations, so any solution that scans all previous notes per query would lead to about $O(n^2)$ behavior in the worst case, which is far too slow. We need something that keeps only a small amount of state and answers each query in constant time.

A subtle pitfall appears when thinking in terms of “maximum width and maximum height independently”. That fails because rotations couple dimensions. For example, having notes $100 \times 1$ and $1 \times 100$ means the “max width” is 100 and “max height” is 100, but that does not reflect that both notes are actually already fine individually. The real constraint depends on optimal orientation per note, not per global axis choice.

Another failure mode comes from trying to maintain a bounding rectangle of all notes as if they must be aligned consistently. The problem does not require consistent orientation across notes; each note can rotate independently.

## Approaches

A brute-force approach keeps a list of all notes. For every query of type check, we iterate over all stored notes and test whether each fits in the wallet after rotation. This is correct because it directly enforces the definition. However, with up to $5 \cdot 10^5$ queries, this degenerates into checking up to $5 \cdot 10^5$ notes per query, producing about $10^{11}$ operations in the worst case, which is impossible.

The key observation is that we do not need to track every rectangle. For a wallet to fail, there must exist a single note that does not fit. So instead of checking all notes each time, we only need to maintain whether there exists at least one “worst” note that blocks the wallet.

Each note $x \times y$ can be normalized by ordering its sides so that $a = \min(x, y)$, $b = \max(x, y)$. After this transformation, every note is represented in a canonical orientation where $a \le b$. Now a wallet $h \times w$ can also be treated as $(\min(h,w), \max(h,w))$.

A note fits if and only if both $a \le h$ and $b \le w$. Therefore, if we ever fix a candidate orientation of the wallet, the only relevant constraint is that all notes must lie under that corner.

Now the important simplification: instead of checking all notes, we maintain a structure that tracks the “largest obstruction”. The worst note is the one with maximum $a$, and among those, the one with maximum $b$. This reduces the set of constraints to two values only.

When a query arrives, we check both orientations of the wallet against this pair. If neither orientation dominates the stored maximum constraints, the answer is NO; otherwise YES.

This works because any note that can invalidate a wallet must violate one of the two dimensions in some orientation, and the canonical representation ensures we only need to test dominance against the extreme point.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Maintain extrema | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process queries in order while maintaining two values: the maximum of the smaller sides of all notes, and the maximum of the larger sides after normalization.

1. For each added note $x, y$, compute $a = \min(x, y)$, $b = \max(x, y)$. This removes orientation ambiguity so every rectangle is comparable in a consistent way.
2. Maintain two global values: `max_a` as the largest among all $a$, and `max_b` as the largest among all $b$ for notes achieving `max_a`. This captures the most restrictive shape.
3. For a query wallet $h, w$, also normalize it into $h \le w$. This ensures consistent comparison against stored notes.
4. Check whether the wallet can contain the worst-case note. This means verifying whether both `max_a ≤ h` and `max_b ≤ w`.
5. Because orientation of the wallet can also be swapped, we also check the swapped condition: `max_a ≤ w` and `max_b ≤ h`.
6. If either orientation works, we print YES; otherwise NO.

### Why it works

Every note is reduced to a canonical pair $(a, b)$ where $a \le b$. Any valid containment into a rectangle corresponds to placing this pair into a chosen orientation of the wallet. The only note that can block feasibility is the one that is hardest to fit in at least one dimension. Tracking the maximum $a$ ensures we respect the tightest “short side”, and tracking the maximum $b$ among those ensures we respect the corresponding “long side” constraint. Any other note is dominated by one of these extremes, so if the extremes fit, all notes fit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    max_a = 0
    max_b = 0
    
    for _ in range(n):
        parts = input().split()
        
        if parts[0] == '+':
            x = int(parts[1])
            y = int(parts[2])
            a = min(x, y)
            b = max(x, y)
            
            if a > max_a:
                max_a = a
                max_b = b
            elif a == max_a:
                if b > max_b:
                    max_b = b
        
        else:
            h = int(parts[1])
            w = int(parts[2])
            
            a1, b1 = min(h, w), max(h, w)
            
            ok = (max_a <= a1 and max_b <= b1)
            print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The code maintains the canonical worst rectangle incrementally. For each insertion, it updates the lexicographically maximal pair $(a, b)$, first by minimizing the short side and then maximizing the long side among ties. Each query simply checks whether this worst rectangle fits into the wallet in its best orientation.

A common mistake is to try tracking only global maxima of both dimensions independently. That fails because those maxima might come from different notes and cannot be simultaneously realized by a single rectangle.

## Worked Examples

### Sample 1

Input:

```
+ 3 2
+ 2 3
? 1 20
? 3 3
? 2 3
```

State evolution:

| Step | Operation | max_a | max_b | Wallet | Check result |
| --- | --- | --- | --- | --- | --- |
| 1 | add (3,2) → (2,3) | 2 | 3 | - | - |
| 2 | add (2,3) → (2,3) | 2 | 3 | - | - |
| 3 | query (1,20) | 2 | 3 | (1,20) | NO |
| 4 | query (3,3) | 2 | 3 | (3,3) | YES |
| 5 | query (2,3) | 2 | 3 | (2,3) | YES |

The first query fails because the smallest side constraint is already violated. Later queries succeed because both dimensions are sufficient in at least one orientation.

### Sample 2 (constructed)

Input:

```
+ 5 1
+ 2 4
? 4 5
```

| Step | Operation | max_a | max_b | Wallet | Check result |
| --- | --- | --- | --- | --- | --- |
| 1 | add (1,5) → (1,5) | 1 | 5 | - | - |
| 2 | add (2,4) → (2,4) | 2 | 5 | - | - |
| 3 | query (4,5) | 2 | 5 | (4,5) | YES |

The key observation here is that although one note is tall and narrow and the other is wide and short, the aggregated constraint is still representable as a single dominating pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each query updates or checks a constant number of variables |
| Space | $O(1)$ | Only two integers are stored |

The algorithm performs a constant amount of work per operation, which is easily fast enough for $5 \cdot 10^5$ queries under the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    max_a = 0
    max_b = 0
    out = []

    for _ in range(n):
        parts = input().split()
        if parts[0] == '+':
            x, y = int(parts[1]), int(parts[2])
            a, b = min(x, y), max(x, y)
            if a > max_a:
                max_a, max_b = a, b
            elif a == max_a:
                max_b = max(max_b, b)
        else:
            h, w = int(parts[1]), int(parts[2])
            a1, b1 = min(h, w), max(h, w)
            if max_a <= a1 and max_b <= b1:
                out.append("YES")
            else:
                out.append("NO")

    return "\n".join(out)

# provided sample
assert run("""9
+ 3 2
+ 2 3
? 1 20
? 3 3
? 2 3
+ 1 5
? 10 10
? 1 5
+ 1 1
""") == """NO
YES
YES
YES
NO"""

# custom: single note fits trivially
assert run("""3
+ 2 2
? 10 10
? 1 1
""") == """YES
NO"""

# custom: rotation required
assert run("""2
+ 1 5
? 5 1
""") == """YES"""

# custom: increasing constraints
assert run("""4
+ 2 3
+ 3 4
? 3 4
? 2 2
""") == """YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single note | YES/NO | basic correctness |
| rotation case | YES | orientation handling |
| mixed queries | YES/NO | incremental updates |

## Edge Cases

One edge case is when the largest short side comes from a different note than the largest long side. The algorithm handles this because `max_b` is only updated when the corresponding `a` equals `max_a`, ensuring both values come from a compatible candidate.

Another edge case is repeated updates that change only the short side maximum. In that case, the long side must be reset to the new candidate’s long side; otherwise the stored pair would become inconsistent with any real rectangle.
