---
title: "CF 352A - Jeff and Digits"
description: "We are given a multiset of cards, each card showing either the digit 0 or the digit 5. From these cards we may choose any subset and arrange the chosen digits into a number written in a single line. Our goal is to build the largest possible number that is divisible by 90."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 352
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 204 (Div. 2)"
rating: 1000
weight: 352
solve_time_s: 146
verified: true
draft: false
---

[CF 352A - Jeff and Digits](https://codeforces.com/problemset/problem/352/A)

**Rating:** 1000  
**Tags:** brute force, implementation, math  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of cards, each card showing either the digit 0 or the digit 5. From these cards we may choose any subset and arrange the chosen digits into a number written in a single line. Our goal is to build the largest possible number that is divisible by 90.

A number divisible by 90 must satisfy two conditions simultaneously. First, it must be divisible by 10, which forces its last digit to be 0. Second, it must be divisible by 9, which requires the sum of its digits to be divisible by 9. Since we only have digits 0 and 5, these constraints strongly restrict what is possible.

The output must be the maximum such number in lexicographic magnitude, which for numbers without leading zeros is equivalent to maximizing the number of digits and placing larger digits first. If no valid number can be formed, we output -1. There is one special interpretation: the number 0 is allowed and considered valid without leading zeros.

The constraints are small, with at most 1000 cards, so linear counting and simple arithmetic decisions are sufficient. Anything involving permutations or subset enumeration would be unnecessary.

The main edge cases arise from how divisibility constraints interact with limited digit types. A naive mistake is to try to use all zeros and fives or to only check divisibility by 10 without ensuring divisibility by 9. Another common failure is forgetting that a valid number must end in 0, meaning at least one zero must exist, except in the degenerate case where the answer is exactly "0".

For example, if we had only fives and no zeros, like input `[5, 5, 5]`, we cannot form any number divisible by 10, so the answer is `-1`. If we have zeros but too few fives to make the sum divisible by 9, like one zero and one five, the only candidate is "0".

## Approaches

A brute-force approach would try all subsets of cards and all permutations of each subset to form numbers, then check divisibility by 90 and keep the maximum. This is correct because it explores all possibilities, but it is infeasible. With up to 1000 cards, the number of subsets is $2^{1000}$, and even ignoring subsets, permuting selected elements leads to factorial growth. This approach collapses immediately under the constraints.

The key observation is that the structure of the problem removes almost all freedom. Since only digits 0 and 5 exist, any constructed number is determined entirely by how many 5s and how many 0s we include. Divisibility by 10 forces at least one zero. Divisibility by 9 depends only on the sum of digits, which is $5 \cdot k$ where $k$ is the number of chosen fives. So we need $5k \equiv 0 \pmod{9}$, which is equivalent to $k \equiv 0 \pmod{9}$ because 5 and 9 are coprime.

So the solution becomes: choose the largest possible number of fives divisible by 9, and use all available zeros. If no such fives exist, the only possible answer is either 0 (if at least one zero exists) or impossible.

We then construct the number by printing that many fives followed by all zeros, which ensures maximal value since placing larger digits first maximizes the number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many zeros and how many fives are present in the input. This reduces the problem to reasoning about frequencies rather than individual cards.
2. Check whether we have at least one zero. If not, we cannot form any number divisible by 10, so the answer is immediately -1.
3. Determine how many fives can be used such that their count is divisible by 9. We take the largest multiple of 9 less than or equal to the total number of fives. This maximizes the number of leading digits while preserving divisibility by 9.
4. If this computed number of fives is zero, we cannot build a number containing 5s that satisfies divisibility by 9. In this case, the best we can do is output a single zero.
5. Otherwise, construct the result by printing that many fives followed by all zeros. This ordering ensures the number is as large as possible because all significant digits are 5 and all trailing digits are 0.

### Why it works

Any valid number must end in zero, so at least one zero is mandatory. Once that constraint is satisfied, the remaining requirement is divisibility by 9, which depends only on the total digit sum. Since zeros do not affect the sum, the only meaningful decision is how many fives to include. Maximizing the count of fives while keeping their count divisible by 9 maximizes both the length and lexicographic value of the number. No rearrangement can improve the result because all valid permutations with the same multiset produce the same optimal ordering when sorted descending.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    cnt0 = arr.count(0)
    cnt5 = arr.count(5)
    
    if cnt0 == 0:
        print(-1)
        return
    
    use5 = (cnt5 // 9) * 9
    
    if use5 == 0:
        print(0)
        return
    
    print("5" * use5 + "0" * cnt0)

if __name__ == "__main__":
    solve()
```

The code begins by counting zeros and fives in a single pass. It then enforces the divisibility-by-10 requirement by checking that at least one zero exists. After that, it computes the usable number of fives by rounding down to the nearest multiple of 9, which directly enforces divisibility by 9. The final construction prints all chosen fives first, then all zeros, guaranteeing maximal numeric value.

The subtle point is that we never try to interleave digits or test permutations, because the optimal structure is forced: all fives must come before zeros in any maximum-value arrangement.

## Worked Examples

### Example 1

Input:

```
4
5 0 5 0
```

We count two zeros and two fives.

| Step | cnt0 | cnt5 | use5 | decision |
| --- | --- | --- | --- | --- |
| initial | 2 | 2 | - | start |
| check zero | 2 | 2 | - | valid |
| compute use5 | 2 | 2 | 0 | 2 // 9 = 0 |
| result | - | - | - | output 0 |

Since we cannot form a multiple of 9 using fives, the only valid construction is a single zero.

### Example 2

Input:

```
10
5 5 5 5 5 5 5 5 5 0
```

We have nine fives and one zero.

| Step | cnt0 | cnt5 | use5 | decision |
| --- | --- | --- | --- | --- |
| initial | 1 | 9 | - | start |
| check zero | 1 | 9 | - | valid |
| compute use5 | 1 | 9 | 9 | 9 // 9 = 9 |
| result | - | - | 9 | 5555555550 |

We use all fives since 9 is divisible by 9, then append the zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | counting digits in a single pass |
| Space | O(1) | only frequency counters are stored |

The solution easily fits within constraints since n is at most 1000, and all operations are constant-time arithmetic plus string construction.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))
    cnt0 = arr.count(0)
    cnt5 = arr.count(5)

    if cnt0 == 0:
        return "-1"
    use5 = (cnt5 // 9) * 9
    if use5 == 0:
        return "0"
    return "5" * use5 + "0" * cnt0

# provided sample
assert run("4\n5 0 5 0\n") == "0"

# all zeros minimum case
assert run("1\n0\n") == "0"

# no zeros impossible
assert run("3\n5 5 5\n") == "-1"

# enough fives for multiple of 9
assert run("10\n" + "5 "*9 + "0\n") == "5555555550"

# extra fives beyond multiple of 9
assert run("11\n" + "5 "*10 + "0\n") == "5555555550"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 0 | minimal valid construction |
| only 5s | -1 | impossibility without zero |
| 9 fives + zero | 5555555550 | exact divisibility boundary |
| 10 fives + zero | 5555555550 | rounding down behavior |

## Edge Cases

One critical edge case is when zeros exist but fives cannot form a multiple of 9. For input `0 5`, we have one zero and one five. The algorithm sets usable fives to zero and outputs just "0". This is correct because any inclusion of the five breaks divisibility by 9.

Another edge case is when there are no zeros at all, for example `5 5 5 5 5`. Even though we can make large numbers from fives, none end in zero, so divisibility by 10 fails immediately. The algorithm correctly returns -1 before attempting any further reasoning.
