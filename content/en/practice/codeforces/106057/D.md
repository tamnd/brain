---
title: "CF 106057D - Zero is not an option!"
description: "We are given a rectangular grid where each cell contains a non-negative integer. From each row, we must pick exactly one element. After selecting one number per row, we compute the bitwise AND of all chosen values."
date: "2026-06-21T15:54:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106057
codeforces_index: "D"
codeforces_contest_name: "CoU CSE Fest 2025 - Inter University Programming Contest (Divisional)"
rating: 0
weight: 106057
solve_time_s: 41
verified: true
draft: false
---

[CF 106057D - Zero is not an option!](https://codeforces.com/problemset/problem/106057/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid where each cell contains a non-negative integer. From each row, we must pick exactly one element. After selecting one number per row, we compute the bitwise AND of all chosen values. The task is to determine whether there exists at least one way to pick such values so that the final AND result is strictly positive.

A bitwise AND is positive exactly when there is at least one bit position where every chosen number has a 1. So the problem is really asking whether we can find a bit that can be made common across all chosen row-elements simultaneously.

The grid can be large enough that trying all combinations of one element per row becomes impossible. If there are N rows and M columns, a brute force approach would require checking M^N selections, which grows exponentially and is infeasible even for moderate values like N = 20, M = 20.

The structure of the input suggests that we only care about bit-level availability per row, not about exact numbers. Each row contributes a set of bits that can potentially be supplied by at least one element in that row.

A key edge case arises when a bit appears somewhere in every row but not in the same column index across rows. For example, consider:

Row 1: 2 (010), 1 (001)

Row 2: 4 (100), 1 (001)

Each row contains the bit 0 (value 1), so a valid selection exists: choose 1 from both rows. The answer is YES.

But if we instead had:

Row 1: 2 (010)

Row 2: 4 (100)

No single bit is common to both rows, so regardless of selection, AND becomes 0.

This shows the problem is about intersection of per-row bit availability rather than direct value comparison.

## Approaches

The brute-force idea is straightforward: enumerate one element per row, compute the AND, and check if it is non-zero. This is correct because it explores all valid selections. However, each row has M choices, so the total number of combinations is M^N. Even for N = 10 and M = 10, this already reaches 10^10 possibilities, which is far beyond any feasible limit.

The key observation is that the AND result is determined entirely by which bit positions are present in all chosen numbers. Instead of reasoning about individual selections, we can reframe the problem: we need to know whether there exists a bit such that every row has at least one number containing that bit.

This reduces the problem to per-row bit availability. For each row, we compute a bitmask representing all bits that appear in any number in that row using OR. Then we check which bits are common across all rows by taking the AND of these masks. If the final intersection mask is non-zero, at least one bit can be preserved in every row, meaning we can choose values that maintain that bit in the final AND.

An alternative viewpoint is to test each bit independently. For each bit position, check whether every row contains at least one number with that bit set. If any bit satisfies this condition, we immediately know a valid selection exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M^N · N) | O(N) | Too slow |
| Row OR + Global AND | O(NM) | O(N) | Accepted |

## Algorithm Walkthrough

1. Initialize an array or variable to store a bitmask per row. Each mask starts at 0 because initially no bits are recorded.
2. For each row, scan all M values and update the row mask using bitwise OR. This captures every bit that appears in at least one element of that row.
3. Maintain a global mask initialized to all bits set (or the first row mask). After processing each row, update it using bitwise AND with the current row mask. This step keeps only bits that are still possible across all processed rows.
4. After processing all rows, check whether the global mask is non-zero. If it is non-zero, output YES; otherwise output NO.

The reason for building row-wise OR masks is that we only care whether a bit is available in a row at all, not which specific element provides it. The AND across rows ensures that we only keep bits that survive in every row.

### Why it works

For any bit position b, the algorithm preserves b in a row mask exactly when there exists at least one element in that row with bit b set. After ANDing across all rows, a bit remains in the final mask if and only if every row has at least one element containing that bit. This is precisely the condition required to pick one element per row such that all chosen elements share that bit, guaranteeing the final AND is positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    global_mask = (1 << 60) - 1  # large enough for constraints
    
    for _ in range(n):
        row_mask = 0
        row = list(map(int, input().split()))
        for x in row:
            row_mask |= x
        global_mask &= row_mask
    
    print("YES" if global_mask != 0 else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads each row, compresses it into a single bitmask, and then intersects all row masks using bitwise AND. The initialization of `global_mask` with all bits set ensures that the first row correctly defines the starting set of possible bits.

A subtle point is that we never need to track actual chosen elements. The OR step abstracts each row into its available bit space, and the AND step enforces consistency across rows.

## Worked Examples

### Example 1

Input:

```
2 3
1 2 4
4 8 1
```

Row processing:

| Step | Row | Row Mask | Global Mask |
| --- | --- | --- | --- |
| 1 | [1,2,4] | 111 (7) | 111 |
| 2 | [4,8,1] | 10101 (21) | 101 |

Final global mask is non-zero, so answer is YES.

This confirms that bit 0 is available in both rows, allowing selection of 1 from each row.

### Example 2

Input:

```
2 2
2 4
8 16
```

| Step | Row | Row Mask | Global Mask |
| --- | --- | --- | --- |
| 1 | [2,4] | 110 (6) | 110 |
| 2 | [8,16] | 11000 (24) | 0 |

Final mask is zero, so answer is NO.

This demonstrates a case where each row has valid bits internally, but no bit is shared across all rows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | each element is processed once to build row masks |
| Space | O(N) | only per-row storage or streaming masks required |

The algorithm is efficient for typical constraints where N and M are up to 10^5 total elements. The bit operations are constant time per element, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, sys.stdin.readline().split())
    global_mask = (1 << 60) - 1
    
    for _ in range(n):
        row = list(map(int, sys.stdin.readline().split()))
        row_mask = 0
        for x in row:
            row_mask |= x
        global_mask &= row_mask
    
    return "YES\n" if global_mask != 0 else "NO\n"

# provided samples
assert run("2 3\n1 2 4\n4 8 1\n") == "YES\n"

# all zeros case
assert run("2 2\n0 0\n0 0\n") == "NO\n"

# single row
assert run("1 3\n1 2 4\n") == "YES\n"

# disjoint bits across rows
assert run("2 2\n1 2\n4 8\n") == "NO\n"

# full overlap via one bit
assert run("3 2\n1 0\n1 2\n5 1\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 / 0 0 / 0 0 | NO | all zeros cannot produce positive AND |
| 1 3 / 1 2 4 | YES | single row always works if any number is positive |
| 2 2 / 1 2 / 4 8 | NO | disjoint bit sets across rows |
| 3 2 / 1 0 / 1 2 / 5 1 | YES | intersection exists through bit 0 |

## Edge Cases

One important edge case is when rows contain zeros only. For example:

```
2 2
0 0
0 0
```

Each row mask becomes 0, so the global mask becomes 0 immediately. The algorithm outputs NO, which is correct because no selection can produce a positive AND.

Another case is a single row:

```
1 3
1 2 4
```

The row mask is non-zero, and since there is no second row to eliminate bits, the global mask remains non-zero. The answer is YES because we can pick any positive number and its AND over a single element is itself.

A more subtle case is disjoint bit distributions:

```
2 2
1 2
4 8
```

Row masks are 3 and 12, and their intersection is 0. Even though each row contains valid bits, no bit appears in both rows, so no selection can preserve a bit in the final AND.
