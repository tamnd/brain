---
title: "CF 1758C - Almost All Multiples"
description: "We need to construct a permutation of the integers from 1 to n with three special requirements. The first position must contain x. The last position must contain 1. For every position i from 1 to n-1, the value placed there must be a multiple of i."
date: "2026-06-09T14:44:21+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1758
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 836 (Div. 2)"
rating: 1400
weight: 1758
solve_time_s: 547
verified: false
draft: false
---

[CF 1758C - Almost All Multiples](https://codeforces.com/problemset/problem/1758/C)

**Rating:** 1400  
**Tags:** greedy, number theory  
**Solve time:** 9m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We need to construct a permutation of the integers from `1` to `n` with three special requirements.

The first position must contain `x`. The last position must contain `1`. For every position `i` from `1` to `n-1`, the value placed there must be a multiple of `i`.

Among all valid permutations, we need the lexicographically smallest one. If no valid permutation exists, we output `-1`.

The constraints are large enough that we must build the answer directly. The sum of all `n` values is at most `2·10^5`, which means an `O(n log n)` or even `O(n√n)` solution per test case is fine as long as the total work across all test cases remains near linear. A brute-force search over permutations is impossible. Even for `n = 15`, there are already more than a trillion permutations.

A subtle edge case appears when `x` does not divide `n`.

For example:

```
n = 5, x = 4
```

The first position contains `4`. Eventually the value `5` must appear somewhere. Since every position except the last must contain a multiple of its index, there is no way to route the required values so that all constraints hold. The correct answer is:

```
-1
```

Another easy mistake is assuming that placing `x` at position `1` and `1` at position `n` automatically determines the rest.

Consider:

```
n = 12, x = 3
```

The identity permutation with those two modifications is not valid because the value removed from position `1` must be relocated while preserving all divisibility constraints.

A third subtle point is lexicographic minimality. We are not merely looking for any valid permutation. If several valid permutations exist, we must keep every position as small as possible from left to right.

## Approaches

A brute-force approach would generate permutations and test whether every position satisfies the divisibility condition. Even checking all permutations of size 15 is already hopeless, so we need to exploit the structure of the constraints.

The key observation is that the identity permutation already satisfies the divisibility requirement because every number is a multiple of itself.

If there were no restrictions on positions `1` and `n`, the permutation

```
1 2 3 ... n
```

would be valid.

The only problem is that position `1` must contain `x` and position `n` must contain `1`.

This suggests starting from the identity permutation and modifying only a small chain of positions. The divisibility condition is extremely restrictive. If position `i` does not contain `i`, then it must contain some larger multiple of `i`.

Suppose we place `x` at position `1`. Then the value originally belonging to position `x` must move somewhere else. Repeating this argument creates a chain of positions where each next position is a multiple of the previous one.

For a solution to exist, we eventually need to reach position `n`. This immediately implies that `x` must divide `n`. If `x` does not divide `n`, no valid chain exists.

To obtain the lexicographically smallest answer, we always want the earliest changed position to receive the smallest possible valid value. That leads to a greedy transition from the current position to the smallest divisor-multiple that still allows reaching `n`.

The resulting construction follows a divisor chain from `x` to `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy divisor chain | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. If `n` is not divisible by `x`, output `-1`.
2. Initialize the permutation as the identity permutation:

```
p[i] = i
```
3. Set:

```
p[1] = x
p[n] = 1
```
4. Let `cur = x`.
5. While `cur != n`, find the smallest multiple `next` of `cur` such that:

- `next` divides `n`
- `next > cur`

Among all such candidates, choose the smallest one.
6. Set:

```
p[cur] = next
```

and move:

```
cur = next
```
7. After reaching `n`, set:

```
p[n] = 1
```
8. Output the permutation.

The greedy choice is the heart of the solution. At each step we choose the smallest valid next divisor of `n` that is also a multiple of the current position. Any larger choice would increase an earlier position of the permutation and therefore produce a lexicographically larger answer.

### Why it works

Every modified position belongs to a chain

```
1 -> x -> ... -> n -> 1
```

Each transition goes from a number to one of its multiples, so the divisibility requirement remains satisfied.

All positions outside the chain keep their original values, which also satisfy the divisibility requirement.

The chain only uses divisors of `n`, so every step can eventually reach `n`. If `x` does not divide `n`, such a chain cannot exist because every move preserves divisibility relationships with `n`.

The greedy rule chooses the smallest possible next value at the earliest position where a choice exists. Lexicographic order is determined by the first differing position, so this guarantees the smallest valid permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())

        if n % x != 0:
            print(-1)
            continue

        p = list(range(n + 1))

        p[1] = x
        p[n] = 1

        cur = x

        while cur != n:
            nxt = n

            d = cur * 2
            while d <= n:
                if n % d == 0 and d % cur == 0:
                    nxt = d
                    break
                d += cur

            p[cur] = nxt
            cur = nxt

        print(*p[1:])

solve()
```

The permutation begins as the identity permutation because that already satisfies all divisibility constraints.

The only positions that change are those on the divisor chain. For a current position `cur`, we search through multiples of `cur` and pick the smallest one that still divides `n`. That choice preserves the possibility of eventually reaching `n` while making the permutation lexicographically minimal.

A common implementation mistake is forgetting that `p[n]` must end up as `1`. Another is replacing positions outside the chain. Every untouched position should remain equal to its index.

## Worked Examples

### Example 1

Input:

```
n = 4
x = 2
```

Initial permutation:

| Position | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Value | 2 | 2 | 3 | 1 |

Current chain position is `2`.

The smallest multiple of `2` that divides `4` is `4`.

| Current | Next |
| --- | --- |
| 2 | 4 |

Update:

```
p[2] = 4
```

Final permutation:

| Position | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| Value | 2 | 4 | 3 | 1 |

Output:

```
2 4 3 1
```

This example shows the simplest nontrivial chain.

### Example 2

Input:

```
n = 12
x = 3
```

Start:

| Current |
| --- |
| 3 |

Candidates are multiples of 3 dividing 12.

Smallest valid choice:

| Current | Next |
| --- | --- |
| 3 | 6 |

Then:

| Current | Next |
| --- | --- |
| 6 | 12 |

Updates:

```
p[3] = 6
p[6] = 12
```

Final permutation:

```
3 2 6 4 5 12 7 8 9 10 11 1
```

The chain is:

```
3 -> 6 -> 12
```

and every other position stays unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each chain step scans multiples, total work across a test case is bounded by harmonic-series behavior |
| Space | O(n) | Stores the permutation |

Since the sum of all `n` values is at most `2·10^5`, this comfortably fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())

        if n % x:
            out.append("-1")
            continue

        p = list(range(n + 1))
        p[1] = x
        p[n] = 1

        cur = x

        while cur != n:
            nxt = n

            d = cur * 2
            while d <= n:
                if n % d == 0 and d % cur == 0:
                    nxt = d
                    break
                d += cur

            p[cur] = nxt
            cur = nxt

        out.append(" ".join(map(str, p[1:])))

    return "\n".join(out)

# provided samples
assert run("3\n3 3\n4 2\n5 4\n") == (
    "3 2 1\n"
    "2 4 3 1\n"
    "-1"
)

# minimum valid case
assert run("1\n2 2\n") == "2 1"

# impossible because x does not divide n
assert run("1\n10 6\n") == "-1"

# direct chain
assert run("1\n6 3\n") == "3 2 6 4 5 1"

# larger divisor chain
assert run("1\n12 3\n") == "3 2 6 4 5 12 7 8 9 10 11 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2` | `2 1` | Smallest valid instance |
| `10 6` | `-1` | Necessary condition `x |
| `6 3` | `3 2 6 4 5 1` | Single chain transition |
| `12 3` | `3 2 6 4 5 12 7 8 9 10 11 1` | Multiple chain transitions |

## Edge Cases

Consider:

```
n = 5
x = 4
```

Since `5 % 4 != 0`, the algorithm immediately returns:

```
-1
```

No divisor chain from `4` can reach `5`, so a valid permutation cannot exist.

Consider:

```
n = 2
x = 2
```

The identity permutation becomes:

```
2 1
```

The chain starts at `2`, which is already `n`, so no further work is needed.

Consider:

```
n = 16
x = 2
```

The chain becomes:

```
2 -> 4 -> 8 -> 16
```

The algorithm updates exactly those positions and leaves every other position unchanged. Each assigned value is a multiple of its position, and the greedy choice at every step produces the lexicographically smallest valid permutation.
