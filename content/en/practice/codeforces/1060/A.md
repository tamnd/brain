---
title: "CF 1060A - Phone Numbers"
description: "We are given a multiset of digit cards, each card containing a single character from 0 to 9. From these cards, we want to assemble as many valid phone numbers as possible."
date: "2026-06-15T09:09:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1060
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 513 by Barcelona Bootcamp (rated, Div. 1 + Div. 2)"
rating: 800
weight: 1060
solve_time_s: 284
verified: true
draft: false
---

[CF 1060A - Phone Numbers](https://codeforces.com/problemset/problem/1060/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 4m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of digit cards, each card containing a single character from 0 to 9. From these cards, we want to assemble as many valid phone numbers as possible. A valid phone number has a fixed structure: it consists of exactly 11 digits, and its first digit must be 8, while the remaining 10 positions can be filled with any digits.

Each card can be used at most once, and we are allowed to reuse the same resulting phone number pattern conceptually multiple times as long as we have enough cards to build each copy independently.

The task is to determine the maximum number of such 11-digit strings starting with 8 that can be formed from the available digits.

The constraint n ≤ 100 is small enough that even quadratic or simple greedy counting approaches are safe. This immediately rules out any need for sophisticated data structures or combinatorics. We are dealing purely with frequency accounting.

A key observation is that the only special requirement is the leading 8. Every phone number consumes exactly one occurrence of digit 8, and a total of 11 cards overall. Everything else is just a pool of filler digits.

Edge cases appear when there are no 8s at all. In that case, regardless of how many other digits exist, no valid phone number can be formed. For example, input `11111111111` yields 0.

Another subtle case is when there are enough total digits but insufficient 8s. For example, `888` repeated with too few other digits still limits the answer strictly by the number of available 8s.

Finally, if there are many 8s but too few total digits, then total capacity dominates: even though each phone number needs an 8, it also needs 10 more digits, so leftover 8s are useless without support digits.

## Approaches

A brute-force way to think about the problem is to try constructing phone numbers one by one. We repeatedly scan the current multiset of digits, check if we can pick one 8 and any 10 other digits, then remove those digits and continue. Each attempt costs O(11) scanning or bookkeeping, and we may repeat up to O(n) times, leading to O(n²) behavior. With n ≤ 100 this is already fine, but it is unnecessary.

The structure of the problem reveals a simpler constraint system. Each phone number consumes exactly 11 cards, and among those 11, exactly one must be an 8. So if we denote the number of 8s as c8 and total digits as n, then the number of phone numbers k must satisfy both k ≤ c8 and 11k ≤ n. The second condition comes from total card consumption, and the first comes from the fixed requirement of one 8 per number.

The optimal solution is therefore just the minimum of these two limiting factors. This reduces the problem to counting frequencies and taking a simple bound.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force construction | O(n²) | O(1) | Accepted |
| Counting + min constraint | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times digit 8 appears in the input. This represents the maximum possible number of phone numbers from the perspective of the required leading digit.
2. Compute how many full groups of 11 cards exist in total, which is n // 11. This represents the absolute upper bound imposed by total available cards.
3. The answer is the smaller of these two values, since every valid phone number must satisfy both constraints simultaneously.
4. Output this value directly.

### Why it works

Each valid phone number consumes exactly 11 distinct cards, and exactly one of them must be an 8. Any valid construction can be mapped to a pairing between phone numbers and disjoint groups of 11 cards, each group containing at least one 8 at its first position. Therefore, no solution can exceed either the total number of 8s or the number of disjoint 11-card blocks. The construction that greedily uses cards without violation of these constraints always achieves the minimum bound because there is no additional structure beyond counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()
    
    c8 = s.count('8')
    
    print(min(c8, n // 11))

if __name__ == "__main__":
    solve()
```

The implementation first reads the number of cards and the digit string. It then counts occurrences of '8', which directly controls how many phone numbers can be formed due to the mandatory leading digit constraint. The second constraint is derived from total length: each phone number consumes 11 digits, so n // 11 is the maximum number of complete phone numbers possible regardless of digit composition. The final answer is the minimum of these two limits.

There are no ordering issues or greedy choices required because the problem does not depend on arrangement, only on counts.

## Worked Examples

### Example 1

Input:

```
11
00000000008
```

We compute c8 = 1 and n // 11 = 1.

| Step | c8 | n // 11 | Current answer |
| --- | --- | --- | --- |
| Initial | 1 | 1 | min(1, 1) = 1 |

The result is 1, meaning we can form exactly one valid phone number using all digits.

This confirms that even if most digits are zeros, a single 8 is sufficient when total length supports only one group.

### Example 2

Input:

```
22
8888888888888888888888
```

Here c8 = 22 and n // 11 = 2.

| Step | c8 | n // 11 | Current answer |
| --- | --- | --- | --- |
| Initial | 22 | 2 | min(22, 2) = 2 |

Even though there are many 8s, total length restricts us to only 2 phone numbers. This demonstrates the dominance of the grouping constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the string once to count digit frequencies |
| Space | O(1) | Only a single counter is maintained |

The solution easily satisfies the constraints since n is at most 100, and even for much larger inputs, a single pass frequency count remains efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline().strip())
    s = sys.stdin.readline().strip()
    
    return str(min(s.count('8'), n // 11))

# provided sample
assert run("11\n00000000008\n") == "1", "sample 1"

# no 8 at all
assert run("11\n11111111111\n") == "0", "no valid phone numbers"

# exactly one full valid set
assert run("11\n81234567890\n") == "1", "single possible number"

# too few digits for even one number
assert run("10\n8888888888\n") == "0", "insufficient length"

# many 8s but limited by length
assert run("22\n8888888888888888888888\n") == "2", "length constraint dominates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 11 digits, no 8 | 0 | absence of required leading digit |
| mixed valid set | 1 | normal construction |
| 10 digits of 8s | 0 | length constraint prevents formation |
| many 8s | 2 | min(n//11, c8) behavior |

## Edge Cases

For an input with no digit 8, such as `11111111111`, the algorithm computes c8 = 0 and returns 0 immediately. This matches the fact that no valid phone number can even begin.

For an input where n < 11, such as `8888888888`, n // 11 is 0, so the result is 0 regardless of how many 8s exist. This correctly captures the impossibility of forming any full phone number.

For an input like `8888888888888888888888` with n = 22, c8 = 22 and n // 11 = 2, so the output is 2. The algorithm correctly limits by total available grouping capacity rather than overusing digit 8s.
