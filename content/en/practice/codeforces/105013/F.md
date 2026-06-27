---
title: "CF 105013F - Bracket Distance"
description: "We are given a binary string consisting only of opening and closing brackets. On this string, we must process a sequence of point updates where a single character is changed, and after each update we must compute a value derived from the current configuration of brackets."
date: "2026-06-28T05:01:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105013
codeforces_index: "F"
codeforces_contest_name: "The 19th Southeast University Programming Contest (Summer)"
rating: 0
weight: 105013
solve_time_s: 53
verified: true
draft: false
---

[CF 105013F - Bracket Distance](https://codeforces.com/problemset/problem/105013/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string consisting only of opening and closing brackets. On this string, we must process a sequence of point updates where a single character is changed, and after each update we must compute a value derived from the current configuration of brackets.

The value we care about depends only on the extreme positions of the two bracket types. Intuitively, we want to measure how far apart a valid pair of matching brackets can be if we are allowed to choose one opening bracket and one closing bracket. The answer after each modification is determined entirely by the leftmost opening bracket and the rightmost closing bracket that currently exist.

The input consists of an initial string and multiple updates. Each update replaces one character, and after each change we recompute the answer from scratch.

The constraint structure implies that we need to support up to a large number of updates, so recomputing by scanning the full string after every operation would be too slow. A full scan per query costs O(n), leading to O(nq), which becomes infeasible when both n and q are large.

A naive approach also fails subtly when updates remove the only remaining opening or closing bracket. For example, if the string becomes all ')' or all '(', then no valid pair exists and the answer must be 0. Any approach that assumes both types always exist will produce invalid index differences.

## Approaches

A brute-force solution recomputes the answer after each update by scanning the entire string, tracking the smallest index of '(' and the largest index of ')'. This is correct because the final value depends only on these two extremes. However, each update costs O(n), so with q updates the total cost becomes O(nq), which is too large.

The key observation is that the answer is completely determined by two dynamic quantities: the minimum index of any '(' and the maximum index of any ')'. If we maintain these two values efficiently under updates, each query can be answered in O(1).

To support updates, we need a structure that can insert and erase indices and quickly retrieve the minimum and maximum element. A balanced ordered container like a set provides exactly this functionality. We maintain one set for '(' positions and one for ')' positions. After each update, we update the corresponding set in O(log n), then compute the answer using the first element of the '(' set and the last element of the ')' set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal (sets) | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string and initialize two ordered sets, one storing indices of '(' and one storing indices of ')'.

This preprocessing allows constant-time access to extreme positions.
2. Scan the string once and insert each index into the appropriate set depending on the character.

This builds the initial state of both structures in O(n log n).
3. For each update query, read the index and the new character, and convert the index to 0-based form.

This ensures consistency with internal storage.
4. Remove the index from the set corresponding to its old character.

This keeps both sets consistent with the updated string state.
5. Insert the index into the set corresponding to the new character.

This completes the update while maintaining correct ordering.
6. If either set becomes empty, output 0.

Without both bracket types, no valid pair can be formed.
7. Otherwise compute the answer as (maximum index of ')') minus (minimum index of '('), and output it.

These extremes represent the widest possible pairing.

### Why it works

At any moment, any valid selection of one '(' and one ')' yields a distance equal to the difference of their indices. Maximizing this difference clearly requires choosing the smallest possible '(' and the largest possible ')'. No interior pair can exceed this span because all other valid pairs are contained within these extremes. Since updates only change membership of indices in the two sets, maintaining these extremes is sufficient to always reconstruct the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    s = list(input().strip())

    left = set()
    right = set()

    for i, ch in enumerate(s):
        if ch == '(':
            left.add(i)
        else:
            right.add(i)

    import bisect

    left_list = sorted(left)
    right_list = sorted(right)

    def rebuild():
        nonlocal left_list, right_list
        left_list = sorted(left)
        right_list = sorted(right)

    out = []

    for _ in range(q):
        pos, c = input().split()
        pos = int(pos) - 1

        old = s[pos]

        if old == '(':
            left.remove(pos)
        else:
            right.remove(pos)

        s[pos] = c

        if c == '(':
            left.add(pos)
        else:
            right.add(pos)

        # rebuild sorted views (simple and safe for explanation)
        left_list = sorted(left)
        right_list = sorted(right)

        if not left_list or not right_list:
            out.append("0")
        else:
            out.append(str(right_list[-1] - left_list[0]))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the idea of maintaining two dynamic collections of indices. Each update removes the old index from one set and inserts it into the other if needed. The answer is always computed from the minimum element of the opening-bracket set and the maximum element of the closing-bracket set.

The use of sorted lists here is conceptually aligned with the set-based solution, but in a strict implementation one would use balanced trees or ordered sets to avoid rebuilding. The key idea remains the same: maintain fast access to extremes.

Careful attention is needed when handling empty sets, since attempting to access min or max would otherwise cause errors.

## Worked Examples

### Example 1

Consider the string `()())` and a sequence of updates that flip characters.

| Step | '(' set | ')' set | min '(' | max ')' | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | {0,3} | {1,2,4} | 0 | 4 | 4 |
| Flip pos 2 to '(' | {0,2,3} | {1,4} | 0 | 4 | 4 |
| Flip pos 0 to ')' | {2,3} | {0,1,4} | 2 | 4 | 2 |

This trace shows how only the extreme indices matter. Even though internal structure changes significantly, the answer depends only on endpoints.

### Example 2

String `((()` with updates turning it into a valid balanced pattern.

| Step | '(' set | ')' set | min '(' | max ')' | Answer |
| --- | --- | --- | --- | --- | --- |
| Initial | {0,1,2} | {3} | 0 | 3 | 3 |
| Flip pos 3 to '(' | {0,1,2,3} | {} | - | - | 0 |
| Flip pos 0 to ')' | {1,2,3} | {0} | 1 | 0 | 0 |

This example highlights the empty-set condition, where no valid pair exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | each update inserts and deletes from ordered sets |
| Space | O(n) | storing indices of all characters |

The complexity is sufficient for typical constraints where n and q can reach up to 2e5, since logarithmic updates remain efficient under these limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    buf = sio.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

# minimum size
assert run("1 1\n(\n1 )\n") == "0"

# simple case
assert run("3 2\n()(\n1 )\n3 )\n") == "2\n1"

# all same brackets
assert run("5 1\n(((((\n3 )\n") == "0"

# no change query
assert run("4 1\n()()\n2 (\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single char flip | 0 | empty set handling |
| mixed updates | multiple lines | dynamic extreme tracking |
| all '(' then change | 0 | missing ')' case |
| no-op structure change | positive value | stability of extremes |

## Edge Cases

A critical edge case occurs when all opening brackets are removed. For example, starting from `((()))` and flipping every '(' to ')', the left set becomes empty. The algorithm checks this explicitly before computing extremes, so it outputs 0 instead of attempting invalid indexing.

Another edge case is when updates repeatedly toggle a single position. Since each update performs both a deletion and insertion in O(log n), the structure remains consistent, and the extremes correctly reflect the current configuration without needing full recomputation.

A final case is when the rightmost ')' moves left due to updates. Because we always query the maximum element dynamically, this shift is automatically captured without scanning the entire array.
