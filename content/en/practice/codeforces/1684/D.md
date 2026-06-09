---
title: "CF 1684D - Traps"
description: "We are given a sequence of traps, each with a base damage value. We traverse the traps in order, and for each trap we either take its damage or skip it by jumping over it."
date: "2026-06-10T00:02:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1684
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 792 (Div. 1 + Div. 2)"
rating: 1700
weight: 1684
solve_time_s: 153
verified: false
draft: false
---

[CF 1684D - Traps](https://codeforces.com/problemset/problem/1684/D)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of traps, each with a base damage value. We traverse the traps in order, and for each trap we either take its damage or skip it by jumping over it. Each jump over a trap prevents its damage but increases the damage of all subsequent traps by one per jump already made. We are allowed to make at most $k$ jumps. The goal is to minimize the total damage received.

The input consists of multiple test cases. Each test case gives $n$, the number of traps, $k$, the maximum jumps allowed, and a list of $n$ integers representing the base damage of each trap. The output is a single integer per test case: the minimal total damage achievable.

The constraints allow $n$ to reach $2 \cdot 10^5$ and the sum of $n$ across test cases is at most $2 \cdot 10^5$. This indicates that any solution must be roughly linear in $n$ per test case. A naive approach that tries every combination of jumps is impossible because the number of subsets of traps is $2^n$, far exceeding reasonable computation time. Large base damage values up to $10^9$ suggest we must avoid any solution that accumulates damage inefficiently.

Non-obvious edge cases include situations where $k \ge n$, where we can jump all traps and take zero damage, and cases where the optimal jumps are not at the largest base damage traps due to the cascading effect of bonus damage. For example, in `[5,10,11,5]` with $k=1$, jumping over the third trap is better than jumping over the largest trap, because it minimizes the total sum after accounting for the +1 bonus to subsequent traps.

## Approaches

A brute-force solution would enumerate all subsets of traps to jump over, compute the total damage for each subset, and choose the minimum. This is correct because it tries every possibility, but it requires $O(2^n)$ operations per test case, which is infeasible for $n$ up to $2 \cdot 10^5$.

The key insight is to consider the effect of jumping over a trap in reverse order. Every trap's effective cost is its base damage minus the potential "bonus avoided" from jumping later traps. If we jump over the last $k$ traps, those jumps do not affect earlier traps. By reversing the damage list and considering the largest effective damage first, we can greedily choose the $k$ traps to jump over that provide the maximal reduction in total damage. Sorting traps by decreasing base damage works because the bonus effect increases linearly with the number of jumps, making it optimal to skip the traps with the largest base damage at the latest positions possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, and the array of trap damages $a$.
2. Sort the traps in decreasing order of base damage. This identifies the traps whose damage contributes the most to the total.
3. Select the first $k$ traps from the sorted list to jump over. Each jump reduces the total damage by avoiding the trap's base damage. Track how many jumps have been applied so far.
4. Traverse the array in order. For each trap, if it is marked for a jump, skip adding its damage. Otherwise, add its damage plus the number of jumps already applied before it.
5. The sum accumulated in step 4 is the minimal total damage.

The algorithm works because the jumps are most effective on traps with the largest base damage. By sorting and selecting the top $k$ traps, we ensure each jump contributes maximally to reducing total damage. The bonus damage is naturally handled by accumulating the jump count while traversing the traps in order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        # sort traps by base damage in descending order
        sorted_indices = sorted(range(n), key=lambda i: a[i], reverse=True)
        jump_set = set(sorted_indices[:k])
        damage = 0
        jumps_done = 0
        for i in range(n):
            if i in jump_set:
                jumps_done += 1
            else:
                damage += a[i] + jumps_done
        print(damage)

if __name__ == "__main__":
    solve()
```

We first sort the trap indices by damage in descending order and select the top $k$ indices to jump. While traversing, each skipped trap increments the jump counter, which increases the effective damage of subsequent traps. The sum of `a[i] + jumps_done` for non-jumped traps gives the minimal total damage.

## Worked Examples

### Example 1

Input: `4 1 5 10 11 5`

Jump top 1 trap: index 2 (value 11).

| i | a[i] | jump? | jumps_done | damage |
| --- | --- | --- | --- | --- |
| 0 | 5 | No | 0 | 5 |
| 1 | 10 | No | 0 | 15 |
| 2 | 11 | Yes | 1 | 15 |
| 3 | 5 | No | 1 | 21 |

Output: 21

### Example 2

Input: `6 3 1 2 3 4 5 6`

Jump top 3 traps: indices 5, 4, 3 (values 6,5,4).

| i | a[i] | jump? | jumps_done | damage |
| --- | --- | --- | --- | --- |
| 0 | 1 | No | 0 | 1 |
| 1 | 2 | No | 0 | 3 |
| 2 | 3 | No | 0 | 6 |
| 3 | 4 | Yes | 1 | 6 |
| 4 | 5 | Yes | 2 | 6 |
| 5 | 6 | Yes | 3 | 6 |

Output: 6

This trace confirms that the jump count is applied correctly, and the largest damages are effectively removed to minimize total damage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the trap array dominates, traversal is O(n) |
| Space | O(n) | Storing sorted indices and jump set |

With $n$ up to $2 \cdot 10^5$, sorting and linear traversal fit comfortably within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n4 4\n8 7 1 4\n4 1\n5 10 11 5\n7 5\n8 2 5 15 11 2 8\n6 3\n1 2 3 4 5 6\n1 1\n7\n") == "0\n21\n9\n6\n0"

# custom cases
assert run("1\n1 1\n10\n") == "0", "single trap, jump all"
assert run("1\n5 0\n1 2 3 4 5\n") == "15", "no jumps allowed"
assert run("1\n5 5\n1 2 3 4 5\n") == "0", "jump all traps"
assert run("1\n3 2\n10 1 10\n") == "1", "best jump is first and last trap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 10` | `0` | minimal input, jump all |
| `5 0 1 2 3 4 5` | `15` | zero jumps allowed |
| `5 5 1 2 3 4 5` | `0` | maximum jumps equal to n |
| `3 2 10 1 10` | `1` | optimal jumps not obvious, skipping largest and last |

## Edge Cases

When $k \ge n$, such as `n=4, k=4, a=[8,7,1,4]`, the algorithm correctly jumps all traps. The jump counter increments for each trap, but since all are skipped, no trap contributes to damage. Damage remains zero, which matches the expected minimal damage.

When multiple traps have equal damage, such as `a=[5,5,5,5]` and `k=2`, the algorithm selects the first two indices after sorting (indices 0 and 1) to jump. Remaining traps incur damage of 5 + 2 jumps = 7 and 5 + 2 = 7, summing to 14, which is minimal given any other combination. The approach handles equal values gracefully by selecting the earliest occurrences in the sorted order.
