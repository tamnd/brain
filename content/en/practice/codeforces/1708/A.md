---
title: "CF 1708A - Difference Operations"
description: "We are given an array of positive integers. The only allowed operation chooses some position i 1 and replaces a[i] with a[i] - a[i-1]. The operation affects only one element, and it always subtracts the current value immediately to its left."
date: "2026-06-09T21:03:49+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1708
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 808 (Div. 2)"
rating: 800
weight: 1708
solve_time_s: 122
verified: true
draft: false
---

[CF 1708A - Difference Operations](https://codeforces.com/problemset/problem/1708/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. The only allowed operation chooses some position `i > 1` and replaces `a[i]` with `a[i] - a[i-1]`.

The operation affects only one element, and it always subtracts the current value immediately to its left. We may perform the operation any number of times and in any order. The goal is to make every element except the first become zero.

For each test case, we must determine whether such a sequence of operations exists.

The constraints are very small. The array length is at most 100 and there are at most 100 test cases. Even relatively inefficient approaches would fit comfortably within the limits. The real challenge is recognizing the mathematical property that completely characterizes when the transformation is possible.

A subtle point is that the operation never changes `a[1]`. Whatever value the first element starts with, it keeps forever. Since every other element must eventually become zero by repeatedly subtracting values from the left, the first element acts as the "unit" that all later elements must be compatible with.

One easy mistake is to assume that every element can be reduced to zero independently.

Consider:

```
1
2
5 7
```

The correct answer is:

```
NO
```

Starting from 7, repeated subtraction of 5 gives 2, then -3, and we can never hit exactly 0. A careless solution that only checks whether each element is at least the previous one would incorrectly answer YES.

Another common mistake is to focus on adjacent divisibility.

Consider:

```
1
3
2 4 6
```

The answer is:

```
YES
```

Although 6 is not divisible by 4, we can first turn 4 into 0 by subtracting 2 twice, and 6 can be reduced using the unchanged first element value 2. The relationship between neighboring elements is not the key property.

A third edge case occurs when all elements are already equal:

```
1
4
7 7 7 7
```

The answer is:

```
YES
```

Each non-first element can be reduced to zero by subtracting 7 exactly once.

## Approaches

A brute-force viewpoint is to simulate the process. For each position, we could repeatedly subtract the current left neighbor until the value becomes either zero or smaller than the left neighbor. If it reaches zero, that position is solved. Otherwise the answer is impossible.

This works because repeated subtraction is exactly what the operation does. The problem is that values can be as large as `10^9`. If `a[1] = 1`, reducing a value of `10^9` might require one billion operations. The actual operation sequence is far too large to simulate.

The key observation is that the first element never changes.

Suppose the first element equals `x = a[1]`.

To make `a[2]` become zero, we repeatedly subtract `x`. This is possible if and only if `a[2]` is divisible by `x`.

Now consider later positions. Even if we modify `a[2]`, `a[3]`, and so on, once a position becomes zero it stays zero because subtracting zero changes nothing. Eventually every earlier element can be reduced to zero, leaving `a[1] = x` unchanged.

For any position `i > 1`, the only nonzero value that can ever help reduce it is still `x`. Repeated subtraction by `x` reaches zero exactly when `a[i]` is divisible by `x`.

So the entire problem reduces to checking whether every element is divisible by the first element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum(aᵢ) / a₁) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and store the first element as `x = a[1]`.
2. Check every element from the second position to the last.
3. For each element `a[i]`, compute `a[i] % x`.
4. If any remainder is nonzero, print `"NO"` because repeated subtraction of `x` can never reduce that value exactly to zero.
5. If all elements are divisible by `x`, print `"YES"`.

### Why it works

The first element never changes during any operation. Let its value be `x`.

For any position `i > 1`, every operation that affects `a[i]` subtracts some value from it. To end at exactly zero, the total amount subtracted must equal the original value `a[i]`.

After all earlier positions have been reduced, the only persistent nonzero value available on the left is `x`. Every reduction of `a[i]` is effectively repeated subtraction by `x`. A number can be reduced to zero by repeated subtraction of `x` if and only if it is a multiple of `x`.

Thus every position must satisfy `a[i] % x == 0`. If this condition holds for all positions, we can independently reduce each element to zero. If it fails for even one position, the target configuration is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        x = a[0]
        
        ok = True
        for v in a[1:]:
            if v % x != 0:
                ok = False
                break
        
        print("YES" if ok else "NO")

solve()
```

The solution begins by storing the first element because it is the only value that never changes throughout the process.

The loop over the remaining elements checks the divisibility condition derived in the proof. The moment a non-divisible element is found, we already know the answer must be `"NO"`, so the loop can terminate early.

All arithmetic uses Python integers. Since Python supports arbitrary-precision integers, there are no overflow concerns, although the given bounds are already small enough for standard 64-bit integers.

The indexing is straightforward because the first element is handled separately and every later element must satisfy the same condition.

## Worked Examples

### Example 1

Input:

```
2
5 10
```

| Step | Current Element | First Element x | v % x | Result |
| --- | --- | --- | --- | --- |
| 1 | 10 | 5 | 0 | Continue |

All checks pass.

Output:

```
YES
```

This demonstrates the basic successful case. Since 10 is a multiple of 5, repeated subtraction of 5 reaches zero exactly.

### Example 2

Input:

```
4
9 9 8 2
```

| Step | Current Element | First Element x | v % x | Result |
| --- | --- | --- | --- | --- |
| 1 | 9 | 9 | 0 | Continue |
| 2 | 8 | 9 | 8 | Fail |

The algorithm stops immediately.

Output:

```
NO
```

This example shows why divisibility is necessary. Starting from 8, repeated subtraction of 9 skips over zero and can never land on it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One divisibility check per element |
| Space | O(1) | Only a few variables are used |

Since `n ≤ 100`, the algorithm is far below the limits. Even across all test cases, only a few thousand modulo operations are performed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        x = a[0]
        ok = all(v % x == 0 for v in a[1:])
        print("YES" if ok else "NO")

    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run(
"""4
2
5 10
3
1 2 3
4
1 1 1 1
9
9 9 8 2 4 4 3 5 3
"""
) == """YES
YES
YES
NO
"""

# minimum size, divisible
assert run(
"""1
2
1 1
"""
) == """YES
"""

# minimum size, not divisible
assert run(
"""1
2
5 7
"""
) == """NO
"""

# all equal values
assert run(
"""1
5
7 7 7 7 7
"""
) == """YES
"""

# large values near limit
assert run(
"""1
3
1000000000 2000000000 3000000000
"""
) == """YES
"""

# catches implementations that check adjacent divisibility
assert run(
"""1
3
2 4 6
"""
) == """YES
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1` | YES | Smallest valid array |
| `2 / 5 7` | NO | Non-divisible second element |
| `7 7 7 7 7` | YES | All-equal values |
| Large multiples of `10^9` | YES | Large-number arithmetic |
| `2 4 6` | YES | Rejects incorrect adjacent-divisibility logic |

## Edge Cases

Consider:

```
1
2
5 7
```

The algorithm sets `x = 5` and checks `7 % 5 = 2`. Since the remainder is nonzero, it outputs `"NO"`.

Trying the operation sequence confirms this. The value 7 becomes 2 after one subtraction, then would become negative after another. Zero is unreachable.

Consider:

```
1
3
2 4 6
```

The algorithm checks:

```
4 % 2 = 0
6 % 2 = 0
```

and outputs `"YES"`.

This is a useful counterexample to the idea that every element must be divisible by its immediate predecessor. The actual invariant depends only on the first element.

Consider:

```
1
4
7 7 7 7
```

The algorithm finds every element divisible by 7 and outputs `"YES"`.

Each non-first element can be reduced to zero in exactly one operation, confirming that equal arrays are always valid.
