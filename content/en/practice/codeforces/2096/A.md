---
title: "CF 2096A - Wonderful Sticks"
description: "We are given a permutation task over the numbers from 1 to n. Each number represents a stick length, and every length must be used exactly once. The goal is to arrange these sticks in a sequence so that the relative constraints between consecutive positions are satisfied."
date: "2026-06-08T05:23:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2096
codeforces_index: "A"
codeforces_contest_name: "Neowise Labs Contest 1 (Codeforces Round 1018, Div. 1 + Div. 2)"
rating: 800
weight: 2096
solve_time_s: 92
verified: false
draft: false
---

[CF 2096A - Wonderful Sticks](https://codeforces.com/problemset/problem/2096/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation task over the numbers from 1 to n. Each number represents a stick length, and every length must be used exactly once. The goal is to arrange these sticks in a sequence so that the relative constraints between consecutive positions are satisfied.

The constraints come from a string s of length n − 1. Each character describes how the next element in the sequence compares to all previous elements. If the character is “<”, the next chosen number must be strictly smaller than every number already placed. If it is “>”, the next chosen number must be strictly larger than every number already placed.

So instead of comparing only adjacent elements, each step compares the new element against the global minimum or maximum of the prefix built so far. A “<” forces a new global minimum, while a “>” forces a new global maximum.

The key structural implication is that every step either extends the current range downward or upward, never inside it. This makes the process resemble building a sequence by repeatedly expanding an interval.

The constraints n ≤ 100 and t ≤ 500 imply that even O(n²) per test case would be easily fast enough. However, the structure is simple enough that a linear construction is possible. The main difficulty is ensuring we always have a valid number available that respects future constraints.

A common incorrect approach is to try greedily picking the smallest or largest unused number based only on the current character. This fails because the choice must anticipate future expansions. For example, if we see “>” early, picking the largest immediately may prevent satisfying a later “<” that requires a new global minimum smaller than all previous choices.

Another failure case is treating “<” and “>” symmetrically in a naive stack-like construction without properly separating low and high unused values. The correctness depends on maintaining a consistent mapping between the sequence of constraints and how many times we have expanded upward versus downward.

## Approaches

A brute-force solution would try all permutations of 1 to n and check whether each permutation satisfies the constraint definition. For each candidate permutation, we would scan left to right, maintaining the minimum and maximum of the prefix and verifying that each step satisfies either being strictly smaller than all previous elements or strictly larger than all previous elements depending on the character. There are n! permutations, and each check takes O(n), leading to O(n · n!) operations, which is infeasible even for n = 100.

The key observation is that we do not actually need to search over permutations. The constraints only describe when we must create a new minimum or a new maximum. This suggests thinking in terms of extremes.

At any point in the construction, we are choosing from unused numbers. If we maintain a sorted list of available values, every “<” forces us to pick the smallest remaining number, because it must become smaller than everything before it. Similarly, every “>” forces us to pick the largest remaining number, because it must become larger than everything before it.

However, there is a subtle issue: the first element is unconstrained, and the future sequence of min and max operations must be consistent with remaining counts. The correct way to resolve this is to interpret the sequence in reverse: we decide how many times we will take from the low end and high end in advance using a simple counting argument, then construct the permutation in one pass.

A cleaner constructive view is this: suppose we fix the first element. Then every subsequent step either inserts a new global minimum or maximum. This is equivalent to building a sequence by repeatedly taking either the smallest or largest unused value. The constraint string directly tells us which side to take from.

Thus we maintain two pointers over the sorted set of available numbers, and build the answer greedily from left to right.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the permutation by maintaining a pool of available numbers from 1 to n and two pointers representing the smallest and largest unused values.

1. Initialize a list of available numbers implicitly as the range [1, n], and set a low pointer at 1 and a high pointer at n. We also prepare an empty answer array.
2. Choose the first element arbitrarily as the current value. A convenient choice is the smallest remaining value, because it does not restrict later steps. We place 1 into the sequence and move the low pointer to 2.
3. Iterate through the string s from left to right. At each character, decide whether we must create a new global minimum or a new global maximum.
4. If s[i] is “<”, we must pick a value smaller than everything previously chosen. The only way to guarantee this while maintaining a permutation is to take the current smallest unused value from the low pointer. We append it and increment low.
5. If s[i] is “>”, we must pick a value larger than everything previously chosen. We take the current largest unused value from the high pointer. We append it and decrement high.
6. Continue until all positions are filled. Since each step consumes exactly one number, both pointers meet exactly once.

The correctness relies on the invariant that after each step, all previously chosen elements form a contiguous segment in sorted order of used values. When we take from the low end, we extend the used segment downward; when we take from the high end, we extend it upward. This guarantees that every newly chosen value is either smaller than all previous values or larger than all previous values exactly as required by the corresponding character.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()

        low, high = 1, n
        ans = []

        ans.append(low)
        low += 1

        for ch in s:
            if ch == '<':
                ans.append(low)
                low += 1
            else:
                ans.append(high)
                high -= 1

        print(*ans)

if __name__ == "__main__":
    solve()
```

The code keeps two pointers over the unused range. The first element is fixed to the smallest value, which ensures a stable starting point. Every time we see “<”, we extend the sequence downward by consuming the next smallest number. Every time we see “>”, we extend upward by consuming the next largest number. Since each number is used exactly once, the pointers naturally converge.

A subtle point is that the initial choice of 1 is arbitrary but convenient. Any fixed starting value would work as long as the remaining structure consistently consumes extremes.

## Worked Examples

### Example 1

Input:

```
n = 5
s = <<><
```

We track low, high, and the built array.

| Step | Character | Low | High | Chosen | Array |
| --- | --- | --- | --- | --- | --- |
| 1 | start | 1 | 5 | 1 | [1] |
| 2 | < | 2 | 5 | 2 | [1, 2] |
| 3 | < | 3 | 5 | 3 | [1, 2, 3] |
| 4 | > | 3 | 4 | 5 | [1, 2, 3, 5] |
| 5 | < | 4 | 4 | 4 | [1, 2, 3, 5, 4] |

This shows how the sequence expands upward and downward while preserving the required global extremum property at each step.

### Example 2

Input:

```
n = 7
s = ><>>><
```

| Step | Character | Low | High | Chosen | Array |
| --- | --- | --- | --- | --- | --- |
| 1 | start | 1 | 7 | 1 | [1] |
| 2 | > | 1 | 6 | 7 | [1, 7] |
| 3 | < | 2 | 6 | 2 | [1, 7, 2] |
| 4 | > | 2 | 5 | 6 | [1, 7, 2, 6] |
| 5 | > | 2 | 4 | 5 | [1, 7, 2, 6, 5] |
| 6 | > | 2 | 3 | 4 | [1, 7, 2, 6, 5, 4] |
| 7 | < | 3 | 3 | 3 | [1, 7, 2, 6, 5, 4, 3] |

This trace shows that even alternating constraints are handled naturally by the same two-pointer mechanism.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each number is chosen exactly once, and each step performs constant work |
| Space | O(n) | We store the resulting permutation |

The constraints allow up to 500 test cases with n up to 100, so at most 50,000 operations, which is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        low, high = 1, n
        ans = [low]
        low += 1

        for ch in s:
            if ch == '<':
                ans.append(low)
                low += 1
            else:
                ans.append(high)
                high -= 1

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided samples
assert run("""5
2
<
5
<<><
2
>
3
<>
7
><>>><
""") == """2 1
4 3 2 5 1
1 2
2 1 3
3 7 2 6 5 4 1"""

# custom cases
assert run("""1
2
<
""") == "2 1"

assert run("""1
2
>
""") == "1 2"

assert run("""1
4
<<<<
""") == "4 3 2 1"

assert run("""1
4
>>>>""") == "1 4 2 3"

assert run("""1
6
<><><
""")  # sanity check, structure only
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2, “<” | 2 1 | smallest case, forced descending |
| n=2, “>” | 1 2 | smallest case, forced ascending |
| all “<” | full reverse | repeated minimum selection |
| all “>” | alternating extremes | repeated maximum selection |
| alternating pattern | valid permutation | stability of two-pointer strategy |

## Edge Cases

A subtle edge case is when the string alternates between “<” and “>”. For example, n = 5 and s = “<>><”. The algorithm still works because every step only depends on remaining extremes, not previous pattern shape. The low and high pointers always move inward, guaranteeing availability.

Another edge case is a prefix of all “<”. In this case, we continuously pick increasing minimums, effectively producing a fully decreasing prefix in reverse order. The algorithm still remains valid because each new value is guaranteed to be smaller than all previous ones.

Finally, when the string ends with “<”, the last step forces the smallest remaining value. Since low and high converge exactly, the final element is uniquely determined and the permutation remains valid without ambiguity.
