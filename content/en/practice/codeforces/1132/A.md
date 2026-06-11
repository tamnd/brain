---
title: "CF 1132A - Regular Bracket Sequence"
description: "We are given four types of bracket strings, each of length two: \"((\", \"()\", \")(\", and \"))\". The input provides counts of how many of each type we have."
date: "2026-06-12T04:07:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1132
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 61 (Rated for Div. 2)"
rating: 1100
weight: 1132
solve_time_s: 70
verified: true
draft: false
---

[CF 1132A - Regular Bracket Sequence](https://codeforces.com/problemset/problem/1132/A)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four types of bracket strings, each of length two: "((", "()", ")(", and "))". The input provides counts of how many of each type we have. Our task is to determine whether it is possible to concatenate all these strings in some order to form a valid regular bracket sequence. A regular bracket sequence is one that could represent a valid arithmetic expression if we inserted "+" and "1" between the brackets. Examples include "(())" or "()()". Sequences like "))(" or ")((" are invalid because there is no way to match opening and closing brackets correctly.

Each string contributes exactly two characters, so the total length of the final sequence is twice the sum of the counts. The key observation is that each type of string affects the "balance" of opening and closing brackets differently. "((" increases the balance by two, "()" keeps it neutral, ")(" first decreases then increases balance, and "))" decreases the balance by two.

Constraints allow counts up to $10^9$, so any solution that tries to generate sequences or simulate concatenation explicitly will be far too slow. We must reason purely using arithmetic and invariants rather than building the sequence.

An important edge case is when the number of strings that start with ")" or end with "(" exceeds what can be matched. For example, if we have one ")(" and no "((", it is impossible to place it anywhere without creating a negative balance at some point. Another edge case is when all counts are zero; the empty sequence is regular. Handling these boundary conditions correctly is crucial for passing all tests.

## Approaches

A brute-force approach would attempt to try all permutations of the strings and check whether the concatenated sequence is regular. This is correct in principle because it explores all possibilities, but the factorial growth of permutations makes it infeasible even for very small numbers of strings. With counts up to $10^9$, trying permutations is impossible.

The optimal approach relies on maintaining the bracket balance. Every regular bracket sequence must satisfy two conditions. First, the total number of opening brackets must equal the total number of closing brackets. Second, scanning from left to right, the running balance (open minus close) must never be negative. These two conditions can be computed directly from the counts without simulating every string.

Specifically, we check if the number of "((" plus the number of ")(" equals the number of "))" plus the number of "((". This ensures the total balance is zero. To satisfy the non-negative running balance, the difference between ")(" and "((" must not exceed one at any point, as ")(" is the only string that can decrease the balance in the middle of the sequence. This leads to the concise rule: the absolute difference between the count of "((" and "))" must be at most one, and if there is at least one ")(", we need a corresponding "((" to start with.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all permutations) | O((cnt1+cnt2+cnt3+cnt4)!) | O(1) | Too slow |
| Balance-based check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the counts of the four string types: $cnt1, cnt2, cnt3, cnt4$. These correspond to "((", "()", ")(", and "))".
2. Compute the total opening brackets as $2*cnt1 + cnt2 + cnt3$ and total closing brackets as $2*cnt4 + cnt2 + cnt3$. Verify they are equal. If not, output 0 because a regular sequence requires the same number of opening and closing brackets.
3. Check the balance requirement. The only tricky string is ")(" because it starts with a closing bracket. We must ensure there is at least one "((" to place before any ")(" to avoid a negative running balance at the start. If $cnt3 > 0$ and $cnt1 = 0$, output 0.
4. Check the difference between the counts of "((" and "))". If $|cnt1 - cnt4| > 1$, output 0 because we cannot keep the running balance non-negative.
5. If all conditions pass, output 1.

The invariant maintained is that at every point in the concatenated sequence, the running balance of "(" minus ")" is never negative and ends at zero. This guarantees a regular bracket sequence without needing to simulate the concatenation.

## Python Solution

```python
import sys
input = sys.stdin.readline

cnt1 = int(input())
cnt2 = int(input())
cnt3 = int(input())
cnt4 = int(input())

# check if total number of opening and closing brackets are equal
total_open = 2*cnt1 + cnt2 + cnt3
total_close = 2*cnt4 + cnt2 + cnt3

if total_open != total_close:
    print(0)
elif cnt3 > 0 and cnt1 == 0:
    # cannot start with ")("
    print(0)
elif abs(cnt1 - cnt4) > 1:
    # balance at ends is off by more than 1
    print(0)
else:
    print(1)
```

The solution first checks total balance, which guarantees the final sequence has matching brackets. It then handles edge cases for the tricky ")(" string and ensures the difference between pure open "((" and pure close "))" strings does not violate the non-negative running balance. Each condition corresponds directly to the properties of a regular bracket sequence.

## Worked Examples

### Sample 1

Input:

```
3
1
4
3
```

| Step | cnt1 | cnt2 | cnt3 | cnt4 | total_open | total_close | Pass checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Read input | 3 | 1 | 4 | 3 | 2*3+1+4=11 | 2*3+1+4=11 | balance ok |
| cnt3>0 and cnt1=0? | 4>0 and 3=0? | No | - | - | - |  |  |
| abs(cnt1-cnt4)>1? | abs(3-3)=0 | - | - | - | - |  |  |

Output: 1. The algorithm confirms it is possible.

### Sample 2 (empty sequence)

Input:

```
0
0
0
0
```

| Step | total_open | total_close | Pass checks |
| --- | --- | --- | --- |
| Read input | 0 | 0 | balance ok |
| cnt3>0 and cnt1=0? | 0>0 and 0=0? | No | - |
| abs(cnt1-cnt4)>1? | abs(0-0)=0 | - | - |

Output: 1. The empty sequence is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic and comparisons on four integers |
| Space | O(1) | Only stores counts and totals |

Even with counts up to $10^9$, the algorithm performs a fixed number of operations, easily fitting within the 1-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    cnt1 = int(input())
    cnt2 = int(input())
    cnt3 = int(input())
    cnt4 = int(input())

    total_open = 2*cnt1 + cnt2 + cnt3
    total_close = 2*cnt4 + cnt2 + cnt3

    if total_open != total_close:
        return "0"
    elif cnt3 > 0 and cnt1 == 0:
        return "0"
    elif abs(cnt1 - cnt4) > 1:
        return "0"
    else:
        return "1"

# provided samples
assert run("3\n1\n4\n3\n") == "1", "sample 1"
assert run("0\n0\n0\n0\n") == "1", "empty sequence"

# custom cases
assert run("1\n0\n0\n1\n") == "1", "single matching brackets"
assert run("0\n0\n1\n0\n") == "0", "cannot start with )("
assert run("10\n0\n0\n12\n") == "0", "imbalance too large"
assert run("2\n1\n1\n2\n") == "1", "mixed case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 1 | 1 | simple valid sequence |
| 0 0 1 0 | 0 | cannot start with ")(" |
| 10 0 0 12 | 0 | imbalance between "((" and "))" |
| 2 1 1 2 | 1 | general mixed case with all types |

## Edge Cases

When there is at least one ")(" but no "((", the algorithm returns 0. For input `0 0 1 0`, `cnt3>0` and `cnt1=0` triggers the check. The negative balance occurs immediately if we attempt to place ")(" at the start. The algorithm detects this and correctly outputs 0.

When the difference between pure open and pure close strings exceeds 1, such as `10 0 0 12`, the algorithm outputs 0 because the final sequence would require more opening brackets at some point than allowed, violating the non-negative running balance invariant.
