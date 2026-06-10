---
title: "CF 1433B - Yet Another Bookshelf"
description: "We are given a bookshelf represented as a binary array. A value of 1 means a book is present at that position, while 0 means the position is empty."
date: "2026-06-11T04:56:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1433
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 677 (Div. 3)"
rating: 800
weight: 1433
solve_time_s: 90
verified: true
draft: false
---

[CF 1433B - Yet Another Bookshelf](https://codeforces.com/problemset/problem/1433/B)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bookshelf represented as a binary array. A value of `1` means a book is present at that position, while `0` means the position is empty.

A move allows us to take an entire contiguous block of books and shift that block one position left or right into an adjacent empty space. The goal is to make all books occupy one consecutive segment with no empty positions between them.

The key observation is that books never need to move outside the region between the leftmost and rightmost existing book. Empty positions outside that range do not matter because gaps only matter when they separate books.

The constraints are very small. There are at most 200 test cases and each bookshelf has length at most 50. Even an $O(n^2)$ solution would be easily fast enough. This means the challenge is not performance but recognizing the underlying simplification.

Several edge cases are easy to misunderstand.

Consider:

```
1 0 0 0 1
```

The answer is `3`, not `1`. There are three empty positions between the two books, and each empty position must eventually disappear from between them.

Consider:

```
1 1 0 0 1
```

The answer is `2`.

A common mistake is to count groups of zeros instead of individual zeros. Here there is one gap, but it contains two empty positions, so two moves are required.

Consider:

```
0 0 1 1 1 0 0
```

The answer is `0`.

There are zeros on both sides, but no zeros between books. A careless implementation that counts all zeros would incorrectly return `4`.

Consider:

```
1
```

The answer is `0`.

A single book is already a contiguous segment.

## Approaches

A brute-force way to think about the problem is to simulate movements. We could repeatedly choose segments and shift them until all books become consecutive. Since many different move sequences are possible, a complete search would have to explore many states of the bookshelf.

Even though $n \le 50$, such a state-space approach is unnecessary. The number of possible bookshelf configurations grows exponentially, making it an unattractive solution.

The breakthrough comes from looking at what a move actually accomplishes.

Suppose there is a zero between two books:

```
1 0 1
```

To remove this gap, one of the book groups must move across that empty position. Regardless of which side moves, exactly one move is needed for that zero.

Now consider:

```
1 0 0 1
```

There are two empty positions between the books. One move can eliminate at most one of those positions from the interior. Eventually both zeros must disappear, so the answer is `2`.

This pattern generalizes. The only positions that matter are those between the leftmost book and the rightmost book. Every zero inside that interval represents one unavoidable unit of work, and every such zero can be eliminated with exactly one move.

As a result, the minimum number of moves is simply the number of zeros between the first `1` and the last `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow and unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Find the position of the first book, meaning the first occurrence of `1`.
2. Find the position of the last book, meaning the last occurrence of `1`.
3. Examine every position between these two indices, inclusive.
4. Count how many positions contain `0`.
5. Output that count.

The reason step 4 works is that every interior zero represents a gap separating books. Each such gap position must eventually be filled by moving books across it, and one move can eliminate exactly one interior zero.

### Why it works

Let the first book be at position `L` and the last book be at position `R`.

Any book outside the interval `[L, R]` does not exist by definition. To make all books consecutive, every position inside `[L, R]` that currently contains `0` must eventually contain a book.

Each move shifts a contiguous block by one position and can reduce the number of empty positions inside `[L, R]` by at most one. Thus at least as many moves as interior zeros are required.

Conversely, for every interior zero, we can move an adjacent block toward it and fill it in one move. Repeating this process eliminates all interior zeros using exactly that many moves.

Since the lower bound and upper bound are identical, the minimum number of moves equals the number of zeros between the first and last book.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        left = a.index(1)
        right = n - 1 - a[::-1].index(1)

        ans = 0
        for i in range(left, right + 1):
            if a[i] == 0:
                ans += 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first locates the leftmost and rightmost books. Those positions define the only interval that matters.

The loop then counts zeros inside that interval. Zeros outside the interval are ignored because they do not separate any books.

One subtle detail is computing the last occurrence of `1`. Python does not provide a built-in reverse index operation, so the code reverses the array and finds the first `1` there. Converting that position back to the original indexing gives the location of the rightmost book.

Another detail is that the scan includes both endpoints. Since those endpoints are guaranteed to contain books, including them does not affect the count and avoids off-by-one mistakes.

## Worked Examples

### Example 1

Input:

```
0 0 1 0 1 0 1
```

| Variable | Value |
| --- | --- |
| left | 2 |
| right | 6 |

Positions examined:

| Index | Value | Zero Count |
| --- | --- | --- |
| 2 | 1 | 0 |
| 3 | 0 | 1 |
| 4 | 1 | 1 |
| 5 | 0 | 2 |
| 6 | 1 | 2 |

Final answer: `2`.

This example shows that only zeros between the first and last book matter. The leading zeros at positions 0 and 1 are irrelevant.

### Example 2

Input:

```
1 1 0 1 1
```

| Variable | Value |
| --- | --- |
| left | 0 |
| right | 4 |

Positions examined:

| Index | Value | Zero Count |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 1 | 0 |
| 2 | 0 | 1 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |

Final answer: `1`.

This example demonstrates that a single interior zero corresponds to exactly one required move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan to find endpoints and one scan to count zeros |
| Space | O(1) | Only a few variables are used |

With $n \le 50$, the running time is tiny. Even across all 200 test cases, the total work is only a few thousand operations, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        left = a.index(1)
        right = n - 1 - a[::-1].index(1)

        out.append(str(sum(1 for i in range(left, right + 1) if a[i] == 0)))

    return "\n".join(out)

# provided samples
assert run(
"""5
7
0 0 1 0 1 0 1
3
1 0 0
5
1 1 0 0 1
6
1 0 0 0 0 1
5
1 1 0 1 1
"""
) == "2\n0\n2\n4\n1", "sample 1"

# minimum size
assert run(
"""1
1
1
"""
) == "0", "single book"

# books already consecutive
assert run(
"""1
7
0 0 1 1 1 0 0
"""
) == "0", "no internal gaps"

# large internal gap
assert run(
"""1
5
1 0 0 0 1
"""
) == "3", "count every interior zero"

# alternating pattern
assert run(
"""1
7
1 0 1 0 1 0 1
"""
) == "3", "multiple separated gaps"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | Minimum-size instance |
| `0 0 1 1 1 0 0` | `0` | Ignore zeros outside the active range |
| `1 0 0 0 1` | `3` | Count individual zeros, not gap groups |
| `1 0 1 0 1 0 1` | `3` | Multiple independent gaps |

## Edge Cases

Consider:

```
1
5
1 0 0 0 1
```

The first book is at index 0 and the last book is at index 4. Inside that interval there are three zeros. The algorithm counts all three and returns `3`. A solution that counts gap segments instead of gap cells would incorrectly return `1`.

Consider:

```
1
7
0 0 1 1 1 0 0
```

The first book is at index 2 and the last book is at index 4. The algorithm only examines positions 2 through 4 and finds no zeros. The answer is `0`. This correctly ignores empty positions outside the book range.

Consider:

```
1
3
1 0 0
```

The first and last book are the same position. The interval contains only one cell, which is a book. The count of zeros is `0`, so the answer is `0`. A single book already forms a contiguous segment.

Consider:

```
1
5
1 1 0 0 1
```

The relevant interval is the entire array. Two zeros appear between the outermost books, so the algorithm returns `2`. This matches the minimum number of moves needed to eliminate both gaps.
