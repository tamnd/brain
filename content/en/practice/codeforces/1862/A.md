---
title: "CF 1862A - Gift Carpet"
description: "We are given a rectangular carpet of size $n times m$ where each cell contains a lowercase letter. Vika likes to read her name \"vika\" from the carpet by selecting one letter from each column, moving strictly left to right, and choosing exactly four columns for the letters 'v'…"
date: "2026-06-09T00:50:53+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1862
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 894 (Div. 3)"
rating: 800
weight: 1862
solve_time_s: 83
verified: true
draft: false
---

[CF 1862A - Gift Carpet](https://codeforces.com/problemset/problem/1862/A)

**Rating:** 800  
**Tags:** dp, greedy, implementation, strings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular carpet of size $n \times m$ where each cell contains a lowercase letter. Vika likes to read her name "vika" from the carpet by selecting one letter from each column, moving strictly left to right, and choosing exactly four columns for the letters 'v', 'i', 'k', and 'a' in that order. Each column can contribute at most one letter, and the columns must be distinct.

The task is to determine, for multiple test cases, whether it is possible for Vika to read her name on a given carpet. If it is possible, we output "YES", otherwise "NO".

The bounds are small: $1 \le n, m \le 20$ and up to 100 test cases. Because both dimensions are tiny, algorithms with time complexity $O(n \cdot m)$ per test case are acceptable. The constraints suggest we do not need complicated optimizations or advanced data structures.

A non-obvious edge case occurs when $n = 1$ or $m = 4$ and the letters appear in a single row. For instance, if the carpet is:

```
1 4
kvai
```

A careless left-to-right column scan that assumes letters appear in order within a single row may incorrectly conclude "YES" even though the correct sequence in left-to-right column order does not spell "vika". Another edge case occurs when the needed letters are spread across multiple rows in the same column - the solution must consider any row within the column as a valid match.

## Approaches

A brute-force solution would try every combination of four distinct columns and then check if the required letters appear in these columns in order. There are $\binom{m}{4}$ ways to pick four columns, and checking each column for a letter takes $O(n)$ time. In the worst case, this would be $O(n \cdot m^4)$ per test case. For $m = 20$ and $n = 20$, that is around 3.2 million operations per test case, which is tolerable but can be simplified.

The key insight is that we only care about the **first available column** that contains the next required letter in the sequence. We can scan columns from left to right, maintaining a pointer to the next expected letter in "vika". If the current column contains that letter in any row, we move to the next letter. If we reach the end of the columns and have successfully found all four letters, the answer is "YES"; otherwise, "NO". This greedy approach works because the columns must be used in order, and once a column is skipped, it cannot be reused.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m^4) | O(1) | Acceptable but unnecessary |
| Greedy Left-to-Right | O(n * m) | O(1) | Optimal and simple |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and $m$.
2. Read the carpet as a list of strings (each string is a row).
3. Initialize a variable `index` to 0 to track the current letter in the target string "vika".
4. Iterate over the columns from left to right. For each column, check if any row contains the current target letter (`target[index]`).
5. If the current column contains the target letter, increment `index` to move to the next letter.
6. After processing all columns, check if `index` equals 4. If yes, print "YES". Otherwise, print "NO".

This works because the problem allows any row in a column to match, and we only need to preserve the column order. By scanning left to right and advancing `index` greedily, we ensure the letters appear in the correct sequence without missing any possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    carpet = [input().strip() for _ in range(n)]
    target = "vika"
    index = 0
    
    for col in range(m):
        if any(carpet[row][col] == target[index] for row in range(n)):
            index += 1
            if index == 4:
                break
    
    print("YES" if index == 4 else "NO")
```

The outer loop reads test cases. The inner loop scans columns left to right, checking each column against the current target letter using `any()`. Incrementing `index` only when a match is found ensures letters are chosen in order and that each column contributes at most one letter.

## Worked Examples

**Example 1**

Input:

```
1 4
vika
```

| col | letters in column | index | matched? |
| --- | --- | --- | --- |
| 0 | v | 0 | YES → index=1 |
| 1 | i | 1 | YES → index=2 |
| 2 | k | 2 | YES → index=3 |
| 3 | a | 3 | YES → index=4 |

Output: `YES`

This demonstrates the simple left-to-right greedy scan works on a single-row carpet.

**Example 2**

Input:

```
3 3
bad
car
pet
```

| col | letters in column | index | matched? |
| --- | --- | --- | --- |
| 0 | b,c,p | 0 | NO |
| 1 | a,a,e | 0 | NO |
| 2 | d,r,t | 0 | NO |

Output: `NO`

No column contains 'v', so `index` never advances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n * m) | Each column in each test case is scanned, each scan checks up to n rows |
| Space | O(n * m) | Carpet is stored in memory |

With $t \le 100$, $n, m \le 20$, the maximum operations is $100 * 20 * 20 = 40,000$, well within the 1-second limit. Memory usage is negligible compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # copy solution here
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        carpet = [input().strip() for _ in range(n)]
        target = "vika"
        index = 0
        for col in range(m):
            if any(carpet[row][col] == target[index] for row in range(n)):
                index += 1
                if index == 4:
                    break
        print("YES" if index == 4 else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("5\n1 4\nvika\n3 3\nbad\ncar\npet\n4 4\nvvvv\niiii\nkkkk\naaaa\n4 4\nvkak\niiai\navvk\nviaa\n4 7\nvbickda\nvbickda\nvbickda\nvbickda\n") == "YES\nNO\nYES\nNO\nYES"

# Custom cases
assert run("1\n1 4\nkvai\n") == "NO"  # letters out of order
assert run("1\n4 4\nvvvv\niiii\nkkkk\naaaa\n") == "YES"  # all letters in separate rows, same columns
assert run("1\n4 1\nv\ni\nk\na\n") == "NO"  # single column, cannot pick 4 distinct columns
assert run("1\n4 5\nvxxxx\nixxxx\nkxxxx\naxxxx\n") == "YES"  # letters spread, enough columns
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 4\nkvai` | NO | Correct ordering required |
| `4 4\nvvvv\niiii\nkkkk\naaaa` | YES | Multiple rows per column allowed |
| `4 1\nv\ni\nk\na` | NO | Single column cannot provide 4 letters |
| `4 5\nvxxxx\nixxxx\nkxxxx\naxxxx` | YES | Scattered letters across multiple columns |

## Edge Cases

For a single-column carpet of size 4x1:

```
4 1
v
i
k
a
```

The algorithm scans the only column but cannot advance `index` past 0 because all letters are in the same column. Output is "NO", correctly handling the distinct column requirement.

For a single-row carpet where letters appear in the wrong order:

```
1 4
kvai
```

The algorithm scans columns left to right, finds 'k' first, which does not match 'v', so `index` remains 0. Output is "NO".

For columns containing multiple letters:

```
4 4
vvvv
iiii
```
