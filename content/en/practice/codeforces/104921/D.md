---
title: "CF 104921D - Gift Carpet"
description: "We are given a rectangular grid of lowercase letters. Think of it as a carpet where each column is a vertical strip of characters. The reading rule is unusual: we move from left to right across columns, and from each chosen column we are allowed to pick at most one letter."
date: "2026-06-28T08:00:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104921
codeforces_index: "D"
codeforces_contest_name: "Easy_Training"
rating: 0
weight: 104921
solve_time_s: 67
verified: false
draft: false
---

[CF 104921D - Gift Carpet](https://codeforces.com/problemset/problem/104921/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular grid of lowercase letters. Think of it as a carpet where each column is a vertical strip of characters. The reading rule is unusual: we move from left to right across columns, and from each chosen column we are allowed to pick at most one letter. We want to know whether it is possible to choose four distinct columns in increasing order such that from the first chosen column we can take a letter ‘v’, from the second an ‘i’, from the third a ‘k’, and from the fourth an ‘a’.

So the task is not about forming a subsequence in a string directly, but about forming a subsequence of columns, where each column contributes at most one character, and we only care whether a column contains a required letter.

The grid is very small, with both dimensions up to 20 and at most 100 test cases. This immediately rules out any heavy combinatorial search over columns and rows. Even something like checking all subsets of columns is theoretically feasible since there are at most 20 columns, but we should aim for a cleaner linear scan solution per test.

A naive but important observation is that each column can be compressed into a small set of characters it contains. We never need more than a boolean answer per letter requirement per column.

A subtle failure case appears when a column contains multiple relevant letters. For example, if a column contains both ‘v’ and ‘i’, we are not allowed to reuse the column twice. We must ensure column distinctness strictly. Another failure case arises if someone tries to greedily pick the earliest possible match for each character without ensuring future feasibility, but here the pattern is fixed length 4 and monotone, so greedy is safe.

## Approaches

A brute-force interpretation would try to assign columns for each of the four letters. We could pick a column for ‘v’, then a later one for ‘i’, then ‘k’, then ‘a’. For each step we scan possible columns, check validity, and recurse. Since there are at most 20 columns, this becomes a bounded depth search. In worst case, we might try up to 20 choices for each of 4 positions, leading to about $20^4 = 160{,}000$ states per test, which is already fine, but still unnecessary overhead for such a simple pattern.

The key simplification is to notice that the structure is exactly a subsequence check over columns. Each column can be reduced to a set membership check: does it contain ‘v’, ‘i’, ‘k’, or ‘a’. Once we compress each column into a boolean indicator, the problem becomes scanning left to right and matching a fixed pattern "vika".

This reduces everything to a single pointer over the target string. As soon as we see a column that satisfies the current needed character, we consume it and move to the next character. If we reach the end of columns before consuming all four characters, the answer is negative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | O(20⁴ · n) | O(1) | Accepted but unnecessary |
| Greedy Scan | O(n · m) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each column as a potential “event” that may satisfy one of the letters in order.

1. Initialize a pointer `need = 0`, where `need` tracks our progress through the string "vika". This represents which character we are currently trying to match.
2. Iterate over columns from left to right. For each column, scan all rows in that column to check whether the current required character exists anywhere in it. This step is necessary because we are allowed to pick any one cell from the column, not necessarily a fixed row.
3. If the column contains the character `target[need]`, we treat this column as used for that character and increment `need` by one. We do not consider any other character from this column afterward, because columns must be distinct.
4. Continue until either all columns are processed or `need` becomes 4, meaning we successfully matched "vika".
5. If `need == 4`, output "YES", otherwise output "NO".

### Why it works

The correctness relies on the fact that the target sequence is fixed and order-preserving. At any moment, the only meaningful decision is whether a column can satisfy the next required character. Choosing the earliest valid column for each character cannot harm future choices because skipping a valid column would only reduce available options later without increasing flexibility. Since columns are strictly increasing in index, once we commit to a column for a character, all future choices are naturally constrained to the right side, matching the required structure of the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = "vika"

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    
    need = 0
    
    for col in range(m):
        if need == 4:
            break
        
        found = False
        for row in range(n):
            if grid[row][col] == TARGET[need]:
                found = True
                break
        
        if found:
            need += 1
    
    print("YES" if need == 4 else "NO")

t = int(input())
for _ in range(t):
    solve()
```

The solution iterates over columns and checks each column against the current needed character. The inner loop scans rows to determine whether the column is usable. The `need` pointer enforces strict ordering of "v", "i", "k", "a". Once it reaches 4, we stop early since all requirements are satisfied.

A common mistake is scanning rows incorrectly or trying to match characters without respecting column uniqueness. Another is attempting to collect all occurrences of each letter and then checking ordering afterward, which risks mixing row information incorrectly. Here we avoid that entirely by working directly in column order.

## Worked Examples

### Example 1

Input:

```
n=1, m=4
vika
```

| col | column letters | need before | match? | need after |
| --- | --- | --- | --- | --- |
| 0 | v | 0 (v) | yes | 1 (i) |
| 1 | i | 1 (i) | yes | 2 (k) |
| 2 | k | 2 (k) | yes | 3 (a) |
| 3 | a | 3 (a) | yes | 4 |

We successfully consume all characters in order. The process shows that when each column aligns perfectly with the required sequence, the greedy scan advances deterministically.

### Example 2

Input:

```
n=3, m=3
bad
car
pet
```

We need "vika".

| col | column letters | need before | match? | need after |
| --- | --- | --- | --- | --- |
| 0 | b,c,p | 0 (v) | no | 0 |
| 1 | a,a,e | 0 (v) | no | 0 |
| 2 | d,r,t | 0 (v) | no | 0 |

We never find 'v', so progression stalls immediately. This demonstrates that failure can occur at the very first stage, and later columns cannot compensate because ordering is strictly left-to-right.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n · m) | Each test scans every cell once in worst case |
| Space | O(nm) | Storage for the grid |

The maximum grid size is 20 by 20 and at most 100 test cases, so the total number of character checks is bounded by 40,000, which is comfortably within limits for Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    TARGET = "vika"

    t = int(input())
    out = []

    def solve():
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
        need = 0

        for col in range(m):
            if need == 4:
                break
            for row in range(n):
                if grid[row][col] == TARGET[need]:
                    need += 1
                    break

        out.append("YES" if need == 4 else "NO")

    for _ in range(t):
        solve()

    return "\n".join(out)

# provided samples
assert run("5\n1 4\nvika\n3 3\nbad\ncar\npet\n4 4\nvvvv\niiii\nkkkk\naaaa\n4 4\nvkak\niiai\navvk\nviaa\n4 7\nvbickda\nvbickda\nvbickda\nvbickda\n") == "YES\nNO\nYES\nNO\nYES"

# custom cases
assert run("1\n1 4\nvikk") == "NO", "missing v"
assert run("1\n2 4\nvxxx\nixka") == "YES", "spread across rows"
assert run("1\n4 1\nv\ni\nk\na\n") == "YES", "single column impossible case structure"
assert run("1\n2 2\nvv\nii\n") == "NO", "cannot reuse column"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single missing letter | NO | missing first requirement |
| distributed letters | YES | letters can come from different rows |
| single column grid | YES/NO | column reuse constraint behavior |
| duplicate columns | NO | prevents double-use of same column |

## Edge Cases

One edge case is when a column contains multiple relevant characters. For example:

```
n=2, m=1
v
i
```

This column contains both ‘v’ and ‘i’, but we can only use it once. The algorithm processes columns in order and will match only the first required character, increment `need`, and never reconsider the same column. When it later requires ‘i’, it will not reuse this column, correctly leading to failure.

Another case is when all required characters exist but are out of order in columns:

```
n=4, m=4
i...
v...
k...
a...
```

Even though all letters exist, the first column does not contain ‘v’, so matching cannot start. The scan preserves ordering strictly, so no rearrangement is possible.

A final case is when multiple valid columns exist for the same character. The greedy strategy still works because consuming the earliest valid column leaves maximal remaining suffix for later matches, and there are only four fixed steps, so no backtracking is required.
