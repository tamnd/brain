---
title: "CF 1842B - Tenzing and Books"
description: "We have three stacks of books. Each stack contains n books arranged from top to bottom. Every book has a non-negative integer written on it. Tenzing starts with knowledge equal to 0."
date: "2026-06-09T06:12:58+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1842
codeforces_index: "B"
codeforces_contest_name: "CodeTON Round 5 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1100
weight: 1842
solve_time_s: 105
verified: true
draft: false
---

[CF 1842B - Tenzing and Books](https://codeforces.com/problemset/problem/1842/B)

**Rating:** 1100  
**Tags:** bitmasks, greedy, math  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three stacks of books. Each stack contains `n` books arranged from top to bottom. Every book has a non-negative integer written on it.

Tenzing starts with knowledge equal to `0`. Whenever he reads a book with value `v`, his knowledge becomes `knowledge | v`, where `|` is the bitwise OR operation.

The restriction comes from the stack structure. Tenzing can only read the current top book of a stack. After reading it, that book disappears and the next book becomes available. He may switch between stacks at any time and may stop whenever he wants.

The goal is to determine whether some sequence of reads can make his final knowledge exactly equal to `x`.

The input contains multiple test cases. For each test case, we receive the target value `x` and the three stacks. We must output `"Yes"` if some valid reading sequence reaches exactly `x`, otherwise `"No"`.

The sum of all `n` values over the entire input is at most `10^5`. That immediately suggests that a linear or near-linear solution per test case is required. Any approach that tries many different reading orders or explores states of the OR value would quickly become infeasible.

The most dangerous part of the problem is the irreversible nature of bitwise OR. Once a bit becomes `1`, it can never return to `0`. A naive implementation may accidentally allow books that introduce bits not present in `x`, even though such a move permanently makes reaching `x` impossible.

Consider this example:

```
n = 1, x = 2

Stack A: 3
Stack B: 0
Stack C: 0
```

The value `3` contains bits `11₂`, while `x = 2` is `10₂`. Reading `3` introduces an extra bit that does not belong to `x`, so the answer is `"No"`.

Another subtle case is that we may stop at any time.

```
n = 1, x = 0

Stack A: 5
Stack B: 7
Stack C: 9
```

The correct answer is `"Yes"` because reading zero books is allowed.

A third common mistake is thinking that every accessible book must be read.

```
n = 2, x = 1

Stack A: 1 2
Stack B: 0 0
Stack C: 0 0
```

Reading only the first book of stack A already produces `1`. Reading further would create value `3`, which is wrong. Since stopping is allowed, the answer is `"Yes"`.

## Approaches

A brute-force solution would try all possible reading sequences. At every step we could choose one of the currently non-empty stacks or stop. The number of possible sequences grows exponentially because each stack can be advanced independently. Even for modest values of `n`, the number of possibilities becomes enormous.

The brute-force idea is correct because it explicitly explores every valid reading order and checks whether some final OR equals `x`. The problem is that with `n` up to `10^5` overall, such exploration is completely impossible.

The key observation comes from examining when a book can safely be read.

Suppose the current knowledge is `cur`. If a book contains a bit that is not present in `x`, then after performing the OR operation that bit will remain forever. Reaching exactly `x` becomes impossible.

That means every book we ever read must satisfy:

```
(book | x) = x
```

Equivalently, all bits set in the book are already contained in `x`.

Now look at a stack from the top downward. As soon as we encounter a book that contains a forbidden bit, we can never read that book. Since it blocks access to all books below it, the entire remainder of that stack becomes unusable.

This gives a very simple characterization.

For each stack, read books from the top while their bits are a subset of `x`. OR all such values into a global result. The moment we see an invalid book, stop processing that stack.

Why is it safe to OR every accessible valid book? Because OR only adds bits. Every accessible valid book contributes bits that belong to `x`, and there is never a reason to skip such bits. If a bit can be obtained from some accessible valid book, having it in the final OR only helps us reach `x`.

After processing all three stacks, let the accumulated OR be `ans`.

If `ans == x`, then we can choose a reading order that reads exactly those accessible valid books and reaches `x`. Otherwise some bit of `x` was never obtainable, so the answer is `"No"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `ans = 0`.
2. Process each of the three stacks independently from top to bottom.
3. For the current book value `v`, check whether all its set bits belong to `x`.

This is equivalent to checking:

```
(v | x) == x
```
4. If the check succeeds, OR the book into the answer:

```
ans |= v
```

Such a book can safely be read because it never introduces forbidden bits.
5. If the check fails, stop processing this stack immediately.

Any book below it is unreachable because books must be removed from the top first.
6. After all three stacks have been processed, compare `ans` with `x`.
7. Output `"Yes"` if `ans == x`, otherwise output `"No"`.

### Why it works

A book containing a bit outside `x` can never appear in a valid reading sequence. Reading it would permanently set a forbidden bit, making the final value larger than `x` in that bit position.

Consequently, for every stack, only the maximal prefix of valid books is ever accessible. Any book after the first invalid one is unreachable because the blocking book cannot be removed.

The algorithm computes the OR of every book that could possibly participate in a valid sequence. If the resulting OR equals `x`, then all bits of `x` are obtainable and no forbidden bit appears. Reading those books yields exactly `x`.

If the resulting OR is missing some bit of `x`, then no accessible book contains that bit. No reading strategy can create it, so reaching `x` is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())

        stacks = [
            list(map(int, input().split())),
            list(map(int, input().split())),
            list(map(int, input().split()))
        ]

        ans = 0

        for stack in stacks:
            for v in stack:
                if (v | x) == x:
                    ans |= v
                else:
                    break

        print("Yes" if ans == x else "No")

if __name__ == "__main__":
    solve()
```

The solution follows the proof directly.

The condition `(v | x) == x` checks whether every bit set in `v` is also set in `x`. This is the critical observation of the problem. Using any other condition tends to miss cases where a book introduces a forbidden bit.

The `break` is equally important. Once an invalid book appears, that stack becomes blocked forever. Continuing to inspect books below it would incorrectly assume they are reachable.

The variable `ans` stores the OR of all accessible valid books. Since OR is associative and commutative, the exact reading order does not matter for the final value.

Python integers easily handle the values involved because all numbers are at most `10^9`.

## Worked Examples

### Example 1

Input:

```
n = 5, x = 7

A: 1 2 3 4 5
B: 5 4 3 2 1
C: 1 3 5 7 9
```

Processing:

| Stack | Book | Valid? | ans after step |
| --- | --- | --- | --- |
| A | 1 | Yes | 1 |
| A | 2 | Yes | 3 |
| A | 3 | Yes | 3 |
| A | 4 | Yes | 7 |
| A | 5 | Yes | 7 |
| B | 5 | Yes | 7 |
| B | 4 | Yes | 7 |
| B | 3 | Yes | 7 |
| B | 2 | Yes | 7 |
| B | 1 | Yes | 7 |
| C | 1 | Yes | 7 |
| C | 3 | Yes | 7 |
| C | 5 | Yes | 7 |
| C | 7 | Yes | 7 |
| C | 9 | No | stop |

Final value:

| ans | x | Result |
| --- | --- | --- |
| 7 | 7 | Yes |

This example shows that encountering an invalid book only blocks the remainder of that stack. Everything before it remains usable.

### Example 2

Input:

```
n = 2, x = 2

A: 3 2
B: 0 0
C: 0 0
```

Processing:

| Stack | Book | Valid? | ans after step |
| --- | --- | --- | --- |
| A | 3 | No | 0 |
| B | 0 | Yes | 0 |
| B | 0 | Yes | 0 |
| C | 0 | Yes | 0 |
| C | 0 | Yes | 0 |

Final value:

| ans | x | Result |
| --- | --- | --- |
| 0 | 2 | No |

The first book in stack A contains a forbidden bit. Since it cannot be removed, the useful value `2` below it is unreachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each book is examined at most once |
| Space | O(1) | Only a few variables besides the input arrays |

The total number of books across all test cases is at most `3 × 10^5`, so a linear scan easily fits within the one-second time limit. Memory usage remains constant apart from storing the input stacks.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, x = map(int, input().split())

        stacks = [
            list(map(int, input().split())),
            list(map(int, input().split())),
            list(map(int, input().split()))
        ]

        ans = 0

        for stack in stacks:
            for v in stack:
                if (v | x) == x:
                    ans |= v
                else:
                    break

        out.append("Yes" if ans == x else "No")

    return "\n".join(out)

# provided sample
assert run(
"""3
5 7
1 2 3 4 5
5 4 3 2 1
1 3 5 7 9
5 2
3 2 3 4 5
5 4 3 2 1
3 3 5 7 9
3 0
1 2 3
3 2 1
2 2 2
"""
) == "Yes\nNo\nYes"

# minimum size, already equal to zero
assert run(
"""1
1 0
0
0
0
"""
) == "Yes"

# blocked useful value below invalid book
assert run(
"""1
2 2
3 2
0 0
0 0
"""
) == "No"

# all equal values
assert run(
"""1
3 7
7 7 7
7 7 7
7 7 7
"""
) == "Yes"

# need contributions from multiple stacks
assert run(
"""1
1 7
1
2
4
"""
) == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `x = 0`, all books zero | Yes | Reading zero or more books works |
| Invalid top book blocks useful value below | No | Correct handling of stack accessibility |
| All values equal to `x` | Yes | Repeated OR operations |
| Bits split across three stacks | Yes | Combining contributions from different stacks |

## Edge Cases

### Target value is zero

Input:

```
1
1 0
5
7
9
```

Every top book is invalid because each contains bits not present in `0`.

The algorithm immediately stops on all three stacks. `ans` remains `0`, which equals `x`, so the answer is `"Yes"`.

This corresponds to reading no books.

### Useful book hidden below an invalid one

Input:

```
1
2 2
3 2
0 0
0 0
```

The first book in stack A is `3` (`11₂`), which contains a forbidden bit. Processing of stack A stops immediately.

The value `2` below it is never examined because it is unreachable in any valid sequence.

The final OR is `0`, so the answer is `"No"`.

### Reaching x requires multiple stacks

Input:

```
1
1 7
1
2
4
```

Processing yields:

```
ans = 0
ans |= 1 -> 1
ans |= 2 -> 3
ans |= 4 -> 7
```

The final OR equals `7`, so the answer is `"Yes"`.

This demonstrates that the algorithm correctly gathers bits from all accessible stacks and combines them through OR.
