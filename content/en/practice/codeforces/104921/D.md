---
title: "CF 104921D - Gift Carpet"
description: "The carpet is a small grid of lowercase letters. You read it column by column from left to right, but you are not forced to take every character. From each column you may either pick exactly one letter from that column or skip the column entirely."
date: "2026-06-28T18:07:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104921
codeforces_index: "D"
codeforces_contest_name: "Easy_Training"
rating: 0
weight: 104921
solve_time_s: 82
verified: false
draft: false
---

[CF 104921D - Gift Carpet](https://codeforces.com/problemset/problem/104921/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

The carpet is a small grid of lowercase letters. You read it column by column from left to right, but you are not forced to take every character. From each column you may either pick exactly one letter from that column or skip the column entirely. The goal is to see whether you can form the word “vika” in this order, by selecting four distinct columns, strictly increasing in index from left to right, where the first chosen column contributes a ‘v’, the second an ‘i’, the third a ‘k’, and the fourth an ‘a’.

What matters is not the full structure of the grid, but only whether each column contains at least one occurrence of the required letter. Each column acts like a “yes/no availability set” for letters. Once a column is used for one character, it cannot be reused for another because columns must be distinct and ordered.

The constraints are small, with both dimensions at most 20. This immediately rules out any need for heavy optimization. Even checking every possible selection of columns would be feasible since the total number of columns is at most 20, and combinations of four columns would be bounded.

A subtle failure case appears when a column contains multiple relevant letters. For example, a column might contain both ‘v’ and ‘i’. It is still usable, but only for a single step in the sequence. Another corner case is when multiple columns contain the same letter; only ordering matters, not uniqueness of letters across columns.

A naive mistake would be trying to pick letters row-wise or treating the grid as a general path problem. For instance, in a grid like:

```
v a
i k
```

Someone might incorrectly assume a path-based traversal is needed, but the problem ignores row movement entirely. Only column membership matters.

## Approaches

The most direct approach is to try all ways of choosing four distinct columns in increasing order and check whether they can match the sequence v, i, k, a. For each quadruple of columns, we scan the rows inside each column to see whether the required character exists.

This works because the grid is tiny, but the number of quadruples can still be large in the worst case. With up to 20 columns, the number of ways to choose 4 is 4845, and for each we might scan up to 20 rows per column, leading to roughly 4845 × 80 checks per test case. Across 100 test cases, this is still acceptable, but it is unnecessary overhead.

The key observation is that each column can be compressed into a simple state: whether it contains ‘v’, ‘i’, ‘k’, or ‘a’. Once this is done, the problem becomes equivalent to checking whether the sequence v → i → k → a appears as a subsequence in the list of columns. This turns the task into a linear scan where we greedily advance through columns and match the next required character whenever possible.

We no longer need to consider combinations explicitly because any valid selection must respect column order, and greedy progression from left to right preserves all valid possibilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over column quadruples | O(t · m⁴ · n) | O(1) | Accepted but unnecessary |
| Greedy subsequence check | O(t · n · m) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each column, determine whether it contains the characters ‘v’, ‘i’, ‘k’, or ‘a’. This reduces each column to a simple set of flags instead of a full list of letters. The grid structure is no longer needed after this compression.
2. Create the target sequence [‘v’, ‘i’, ‘k’, ‘a’]. We will attempt to match these in order using columns from left to right.
3. Maintain a pointer p starting at 0, representing the next character in the target sequence we still need to match.
4. Iterate through columns from left to right. For each column, check whether it contains the character target[p]. If it does, advance p by one. This simulates choosing this column for the next required character.
5. Stop early if p reaches 4, meaning all characters have been matched successfully. At that point we already know the answer is positive.
6. After scanning all columns, check whether p equals 4. If yes, output “YES”, otherwise output “NO”.

### Why it works

Any valid solution corresponds to choosing four increasing column indices, each satisfying a specific character requirement. If such a sequence exists, scanning left to right and greedily consuming the earliest possible valid column for each character never blocks future matches. This is because delaying a match cannot create new opportunities that were not already available earlier; columns are only ordered constraints, not capacity-limited resources. Thus, the greedy subsequence check preserves existence of any valid quadruple.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        cols = [set() for _ in range(m)]

        for i in range(n):
            row = input().strip()
            for j, ch in enumerate(row):
                cols[j].add(ch)

        target = "vika"
        p = 0

        for j in range(m):
            if p < 4 and target[p] in cols[j]:
                p += 1

        print("YES" if p == 4 else "NO")

if __name__ == "__main__":
    solve()
```

The solution first compresses each column into a set of characters, which allows O(1) membership checks for required letters. This avoids repeatedly scanning rows later.

The main loop then performs a single left-to-right pass over columns, advancing a pointer through the string “vika”. The early exit condition is implicit: once the pointer reaches 4, all required letters have been found in increasing column order.

A common implementation mistake is to reset the pointer for each column or try to match all letters inside a single column. That would incorrectly allow reuse of a column for multiple characters, which violates the distinct column requirement.

## Worked Examples

### Example 1

Input:

```
n = 4, m = 4
v i k a
v i k a
v i k a
v i k a
```

Column states:

| Column | Letters | Matches |
| --- | --- | --- |
| 0 | v | v |
| 1 | i | i |
| 2 | k | k |
| 3 | a | a |

| Step | Column | Target needed | Match? | Pointer p |
| --- | --- | --- | --- | --- |
| 1 | 0 | v | yes | 1 |
| 2 | 1 | i | yes | 2 |
| 3 | 2 | k | yes | 3 |
| 4 | 3 | a | yes | 4 |

The pointer reaches 4 exactly after processing the fourth column, confirming that the word can be formed in order.

### Example 2

Input:

```
n = 2, m = 3
v a c
i x z
```

Column states:

| Column | Letters |
| --- | --- |
| 0 | v, i |
| 1 | a, x |
| 2 | c, z |

| Step | Column | Target needed | Match? | Pointer p |
| --- | --- | --- | --- | --- |
| 1 | 0 | v | yes | 1 |
| 2 | 1 | i | no | 1 |
| 3 | 2 | i | no | 1 |

We never reach ‘i’, so the process ends with p = 1, producing “NO”.

This shows that even if a column contains multiple useful letters, only one can be consumed, and ordering constraints prevent skipping backwards.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n · m) | Each cell is read once to build column sets, then each column is scanned once per test case |
| Space | O(m) | Each column stores at most n characters in a set |

The bounds n, m ≤ 20 make this effectively constant time per test case. Even with 100 test cases, the solution runs far below limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        cols = [set() for _ in range(m)]

        for i in range(n):
            row = input().strip()
            for j, ch in enumerate(row):
                cols[j].add(ch)

        target = "vika"
        p = 0
        for j in range(m):
            if p < 4 and target[p] in cols[j]:
                p += 1

        print("YES" if p == 4 else "NO")

    sys.stdout.seek(0)
    return sys.stdout.read().strip()

# provided samples
assert run("""5
1 4
vika
3 3
bad
car
pet
4 4
vvvv
iiii
kkkk
aaaa
4 4
vkak
iiai
avvk
viaa
4 7
vbickda
vbickda
vbickda
vbickda
""") == """YES
NO
YES
NO
YES"""

# custom cases
assert run("""1
1 4
viii
""") == "NO", "missing characters"

assert run("""1
4 1
v
i
k
a
""") == "NO", "only one column"

assert run("""1
2 5
vxxxx
ixxka
""") == "YES", "spread across columns"

assert run("""1
3 4
abcd
efgh
ijkl
""") == "NO", "no relevant letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| missing characters | NO | incomplete sequence |
| only one column | NO | distinct column requirement |
| spread across columns | YES | greedy accumulation works |
| no relevant letters | NO | empty matching case |

## Edge Cases

A key edge case is when multiple required letters appear in the same column. For example:

```
v i k a
v v v v
v i k a
```

Column 1 contains both ‘v’ and ‘i’. The algorithm processes it only once for the first needed character. It consumes ‘v’ and advances to ‘i’ later when another column provides it. This preserves correctness because a single column cannot satisfy more than one position in the sequence.

Another case is when letters appear in reverse order across columns:

```
a k i v
a k i v
```

Even though all required letters exist somewhere, the left-to-right requirement blocks forming “vika”. The greedy scan never finds ‘v’ early enough, so the pointer remains at 0 and the output becomes “NO”.

A final edge case is minimal input:

```
1 1
v
```

Only one column exists, so it is impossible to select four distinct columns. The scan consumes at most one character and correctly returns “NO” without needing any special handling.
