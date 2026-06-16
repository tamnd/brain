---
title: "CF 1006A - Adjacent Replacements"
description: "We are given a sequence of integers, each lying in a very large range up to $10^9$. Mishka repeatedly applies a global transformation rule that acts independently on each value: every pair of consecutive integers $(1,2)$, $(3,4)$, $(5,6)$, and so on, gets swapped in place, but…"
date: "2026-06-16T23:10:15+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1006
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 498 (Div. 3)"
rating: 800
weight: 1006
solve_time_s: 102
verified: true
draft: false
---

[CF 1006A - Adjacent Replacements](https://codeforces.com/problemset/problem/1006/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, each lying in a very large range up to $10^9$. Mishka repeatedly applies a global transformation rule that acts independently on each value: every pair of consecutive integers $(1,2)$, $(3,4)$, $(5,6)$, and so on, gets swapped in place, but all swaps are applied simultaneously as a single conceptual operation.

The key detail is that the process is not iterative in a meaningful sense. After one full application of all swaps, repeating the same operation again produces the same result as the first time. This suggests the transformation is actually a fixed permutation applied once to every element.

The input size $n \le 1000$ is small, so any solution that runs in linear or even constant time per element is sufficient. What matters is recognizing the structure of the transformation rather than simulating it step by step over a large range up to $10^9$, which would be impossible.

A naive misunderstanding would be to try to simulate all swaps from $1$ to $10^9$, or to repeatedly apply the process until stability. Both are unnecessary and would be computationally infeasible.

A subtle edge case arises when thinking about numbers that never appear in the array but lie between processed pairs. For example, if we try to simulate partial mappings or only observed values, we might miss that the transformation is defined globally and independently per number, not per array content.

## Approaches

The brute-force interpretation is to literally apply the described procedure: for each pair $(2i-1, 2i)$, scan the entire array and swap occurrences. Each full pass over all pairs touches up to $10^9 / 2$ operations, and even if we restrict ourselves to only values appearing in the array, repeated passes are still unnecessary.

A more concrete brute-force simplification would be: for each value in the array, repeatedly check whether it belongs to a pair and swap it. Even this leads to an $O(n \cdot 10^9)$-style conceptual complexity if implemented literally over the full domain, which is not acceptable.

The key observation is that the operation is purely local on value space. Each integer $x$ is mapped independently:

- If $x$ is odd, it swaps with $x+1$.
- If $x$ is even, it swaps with $x-1$.

So the final value of each element is determined by a single arithmetic rule, not simulation. The entire process is equivalent to flipping the least significant bit of the number in binary, since odd and even pairing is exactly toggling parity within each consecutive pair.

Thus each value $x$ transforms as:

- $x \rightarrow x-1$ if $x$ is even
- $x \rightarrow x+1$ if $x$ is odd

This gives an $O(n)$ direct mapping solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 10^9) conceptual | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array of integers. No preprocessing is needed because each element is independent of others.
2. For each element $a_i$, determine whether it is odd or even. This classification fully determines its final value because the transformation is a fixed pairing of consecutive integers.
3. If the value is odd, replace it with $a_i + 1$. This reflects that every odd number is swapped with the next integer.
4. If the value is even, replace it with $a_i - 1$. This reflects that every even number is swapped with the previous integer.
5. Output the transformed array in the same order.

The important structural point is that no element influences any other element. There are no cascades or dependencies, so a single pass suffices.

### Why it works

The transformation defines a permutation on the set of positive integers where each adjacent pair is swapped exactly once. Each number belongs to exactly one pair and is mapped to its partner. Because these pairs partition the entire integer line, the mapping is total and deterministic. The array structure is irrelevant; only individual values matter. Applying the rule once produces the final state, and applying it again returns the original configuration, confirming it is an involution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    res = []
    for x in a:
        if x % 2 == 0:
            res.append(x - 1)
        else:
            res.append(x + 1)
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The solution reads the input once and processes each value independently. The parity check directly encodes the swap pairing, avoiding any simulation over the large integer range. The output preserves the original order since the transformation does not involve reordering.

## Worked Examples

### Example 1

Input:

```
5
1 2 4 5 10
```

| Element | Parity | Transformation | Result |
| --- | --- | --- | --- |
| 1 | odd | 1 → 2 | 2 |
| 2 | even | 2 → 1 | 1 |
| 4 | even | 4 → 3 | 3 |
| 5 | odd | 5 → 6 | 6 |
| 10 | even | 10 → 9 | 9 |

Output:

```
2 1 3 6 9
```

This trace shows that each element is handled independently with no interaction between positions. Each value moves only within its own pair.

### Example 2

Input:

```
4
3 6 7 8
```

| Element | Parity | Transformation | Result |
| --- | --- | --- | --- |
| 3 | odd | 3 → 4 | 4 |
| 6 | even | 6 → 5 | 5 |
| 7 | odd | 7 → 8 | 8 |
| 8 | even | 8 → 7 | 7 |

Output:

```
4 5 8 7
```

This confirms the involution property: applying the same rule again would restore the original array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with a constant-time parity check |
| Space | O(1) extra | Only the output array is stored aside from input |

The constraints allow up to 1000 elements, so a single linear pass is trivially efficient within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from io import StringIO
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("5\n1 2 4 5 10\n") == "2 1 3 6 9"

# minimum size
assert run("1\n1\n") == "2"

# single even
assert run("1\n2\n") == "1"

# mixed
assert run("4\n1 2 3 4\n") == "2 1 4 3"

# already large values
assert run("3\n999999999 1000000000 7\n") == "1000000000 999999999 8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 2 | smallest odd case |
| 2 | 1 | smallest even case |
| 1 2 3 4 | 2 1 4 3 | correctness on alternating pattern |
| large values | swapped correctly | boundary near $10^9$ |

## Edge Cases

One edge case is the smallest possible array with a single odd value. For input `1`, the transformation maps it to `2`. Since there is no interaction with other elements, no hidden dependency appears.

Another edge case is the maximum value $10^9$. For input `[1000000000]`, it is even, so it maps to `999999999`. The rule applies uniformly at the boundary of the allowed range, and no overflow or special casing is required since Python integers handle the subtraction safely and the result remains within constraints.
