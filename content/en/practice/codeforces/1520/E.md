---
title: "CF 1520E - Arranging The Sheep"
description: "We have a one-dimensional board represented by a string. Each '' is a sheep and each '.' is an empty cell. In one move, a sheep can move exactly one position left or right into an adjacent empty cell."
date: "2026-06-10T18:07:12+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1520
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 719 (Div. 3)"
rating: 1400
weight: 1520
solve_time_s: 139
verified: true
draft: false
---

[CF 1520E - Arranging The Sheep](https://codeforces.com/problemset/problem/1520/E)

**Rating:** 1400  
**Tags:** greedy, math  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a one-dimensional board represented by a string. Each `'*'` is a sheep and each `'.'` is an empty cell. In one move, a sheep can move exactly one position left or right into an adjacent empty cell. The goal is to make all sheep occupy consecutive positions, with no gaps between them, while minimizing the total number of single-cell moves.

The important detail is that sheep are indistinguishable. We do not care which sheep ends up in which final position, only that all sheep become contiguous. Since each move changes a sheep's position by one, the answer is the total distance traveled by all sheep.

The length of a test case can be as large as one million across all test cases combined. Any algorithm that repeatedly simulates movements or tries every possible final segment would be far too slow. We need something close to linear time per test case.

A few edge cases deserve special attention.

If there are no sheep at all:

```
...
```

The answer is `0`. The sheep are already "grouped" because there are none. A careless implementation may try to access the median sheep and crash.

If there is exactly one sheep:

```
.*.
```

The answer is `0`. One sheep is already a contiguous group.

If sheep are separated by large gaps:

```
*...*...*
```

The optimal solution is not to move everything toward one endpoint. A naive strategy that gathers sheep at the leftmost sheep performs unnecessary work. The best gathering point is determined by the median sheep.

Another subtle case is when the number of sheep is even:

```
*.*.*
```

There are two middle sheep candidates. Either median position gives the same minimum total distance. The implementation only needs to choose one consistently.

## Approaches

The most direct idea is to choose a final contiguous block and compute how many moves are needed to place every sheep into that block. Suppose there are `k` sheep. If the block starts at position `L`, then the sheep must occupy positions:

```
L, L+1, L+2, ..., L+k-1
```

We could match sheep from left to right and calculate the total movement cost. Repeating this for every possible starting position produces the correct answer.

The problem is that there are up to `n` possible starting positions, and evaluating each one costs `O(k)`. In the worst case this becomes `O(n²)`, which is impossible for `n = 10^6`.

To improve this, we need to understand what actually matters.

Suppose the sheep positions are:

```
p0, p1, p2, ..., p(k-1)
```

If they end up occupying consecutive cells, then sheep `i` must go to:

```
x + i
```

for some starting position `x`.

The total cost becomes:

```
|p0 - (x+0)| +
|p1 - (x+1)| +
...
|p(k-1) - (x+k-1)|
```

Rearrange the expression by defining:

```
qi = pi - i
```

Then the cost becomes:

```
|q0 - x| + |q1 - x| + ... + |q(k-1) - x|
```

Now the problem has transformed into a classic task: choose a value `x` minimizing the sum of absolute deviations.

The minimum sum of absolute deviations is achieved at the median.

That means we do not need to search over all possible final blocks. We only need:

1. Record the positions of all sheep.
2. Build the transformed values `qi = pi - i`.
3. Choose the median transformed value.
4. Sum distances to that median.

Since the sheep positions are collected in increasing order, the transformed sequence is also nondecreasing, so the median is immediately available.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) worst case | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the string and store the indices of all sheep in an array `pos`.
2. If there are zero or one sheep, output `0`.
3. Let `k` be the number of sheep.
4. Construct the transformed sequence:

```
q[i] = pos[i] - i
```

This removes the effect of forcing sheep into consecutive positions.
5. Choose the median value:

```
median = q[k // 2]
```

Since `q` is sorted, this is a valid median.
6. Compute:

```
answer = Σ |q[i] - median|
```
7. Output the answer.

### Why it works

Assume the final contiguous block starts at position `x`. Then sheep `i` must occupy position `x+i`, because changing the relative order of sheep can only increase movement and is never beneficial.

The cost is:

```
Σ |pos[i] - (x+i)|
```

Rewriting:

```
Σ |(pos[i]-i) - x|
```

The values `pos[i]-i` are fixed. The only remaining variable is `x`. A fundamental property of absolute values is that the sum of distances to a set of numbers is minimized at a median. Choosing the median transformed value yields the minimum possible movement cost, which is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        pos = []

        for i, ch in enumerate(s):
            if ch == '*':
                pos.append(i)

        k = len(pos)

        if k <= 1:
            answers.append("0")
            continue

        q = [pos[i] - i for i in range(k)]
        median = q[k // 2]

        ans = 0
        for x in q:
            ans += abs(x - median)

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The first loop extracts the positions of all sheep. Working only with sheep positions is much simpler than reasoning about empty cells.

The transformation `pos[i] - i` is the key step. Without it, we would still have to account for the fact that the final positions must be consecutive. Subtracting `i` removes that constraint and turns the problem into a pure median minimization problem.

The median is taken directly from the transformed array. No sorting is needed because the original sheep positions are encountered in increasing order, and subtracting increasing indices preserves nondecreasing order.

The answer can become large, so we accumulate it in an integer variable. Python integers automatically handle values beyond 32-bit limits.

## Worked Examples

### Example 1

Input:

```
*.*...*.**
```

Positions of sheep:

```
[0, 2, 6, 8, 9]
```

| i | pos[i] | q[i] = pos[i] - i |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 2 | 1 |
| 2 | 6 | 4 |
| 3 | 8 | 5 |
| 4 | 9 | 5 |

Median:

```
q[2] = 4
```

Distance sum:

| q[i] | |q[i]-4| |

|---|---|

| 0 | 4 |

| 1 | 3 |

| 4 | 0 |

| 5 | 1 |

| 5 | 1 |

Total:

```
4 + 3 + 0 + 1 + 1 = 9
```

Output:

```
9
```

This example shows how the transformed coordinates reduce the problem to finding distances from a median.

### Example 2

Input:

```
**.*..
```

Positions:

```
[0, 1, 3]
```

| i | pos[i] | q[i] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 0 |
| 2 | 3 | 1 |

Median:

```
0
```

Distance sum:

| q[i] | |q[i]-0| |

|---|---|

| 0 | 0 |

| 0 | 0 |

| 1 | 1 |

Total:

```
1
```

Output:

```
1
```

The trace demonstrates that only one move is needed, moving the rightmost sheep left by one cell.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(k) | Stores positions of all sheep |
|  |  | where `k` is the number of sheep |

The sum of all string lengths across test cases is at most `10^6`. A linear scan of each test case easily fits within the time limit, and storing sheep positions requires at most `O(n)` memory.

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
        n = int(input())
        s = input().strip()

        pos = [i for i, c in enumerate(s) if c == '*']

        if len(pos) <= 1:
            out.append("0")
            continue

        q = [pos[i] - i for i in range(len(pos))]
        med = q[len(pos) // 2]

        ans = sum(abs(x - med) for x in q)
        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""5
6
**.*..
5
*****
3
.*.
3
...
10
*.*...*.**
"""
) == """1
0
0
0
9"""

# minimum size, no sheep
assert run(
"""1
1
.
"""
) == "0"

# minimum size, one sheep
assert run(
"""1
1
*
"""
) == "0"

# already contiguous
assert run(
"""1
5
.***.
"""
) == "0"

# symmetric gaps
assert run(
"""1
5
*.*.*
"""
) == "2"

# large gap
assert run(
"""1
9
*.......*
"""
) == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `.` | `0` | No sheep present |
| `*` | `0` | Single sheep |
| `.***.` | `0` | Already contiguous |
| `*.*.*` | `2` | Median handling with odd number of sheep |
| `*.......*` | `7` | Large movement distances |

## Edge Cases

### No sheep

Input:

```
1
3
...
```

The positions array becomes:

```
[]
```

The algorithm immediately detects that the number of sheep is at most one and returns `0`. No median computation is attempted.

### Exactly one sheep

Input:

```
1
3
.*.
```

Positions:

```
[1]
```

Again, the algorithm returns `0`. A single sheep already forms a contiguous block.

### Even number of sheep

Input:

```
1
4
*..*
```

Positions:

```
[0, 3]
```

Transformed values:

```
[0, 2]
```

The implementation chooses:

```
median = 2
```

Cost:

```
|0-2| + |2-2| = 2
```

Choosing the other median value `0` would also produce cost `2`. Either median is optimal, so selecting `q[k//2]` is correct.

### Sheep separated by large gaps

Input:

```
1
9
*...*...*
```

Positions:

```
[0, 4, 8]
```

Transformed values:

```
[0, 3, 6]
```

Median:

```
3
```

Cost:

```
3 + 0 + 3 = 6
```

The algorithm naturally gathers sheep around the middle sheep. This avoids the common mistake of forcing all sheep toward one endpoint, which would require more moves.
