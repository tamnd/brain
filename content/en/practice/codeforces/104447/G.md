---
title: "CF 104447G - What is Kaito's delimma?"
description: "We are given multiple independent test cases. In each test case, there is a list of integers representing Kaito’s friends, and a target value x."
date: "2026-06-30T18:00:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104447
codeforces_index: "G"
codeforces_contest_name: "Al-Baath Collegiate Programming Contest 2023"
rating: 0
weight: 104447
solve_time_s: 63
verified: true
draft: false
---

[CF 104447G - What is Kaito's delimma?](https://codeforces.com/problemset/problem/104447/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. In each test case, there is a list of integers representing Kaito’s friends, and a target value x. We want to choose a group of friends such that the bitwise AND of all chosen values is exactly x, and among all valid groups we want the largest possible size. If it is impossible to form any group whose AND equals x, we output −1.

The key operation is bitwise AND across all selected numbers. This operation only keeps a bit set if that bit is set in every chosen number. So the final result is the intersection of all binary representations in the subset.

The constraints are large: up to 5 × 10^5 total numbers across test cases. That immediately rules out any approach that tries all subsets or even tries all pairs or triples. Anything worse than linear per test case will fail.

A subtle failure case appears when x contains bits that are not present in some chosen number. For example, if x = 6 (110₂), but we pick a number like 1 (001₂), the AND immediately loses required bits and can never recover them. So such numbers can never be part of a valid subset. Another important edge case is when all numbers that could possibly be used still share some extra bit that is not in x. In that case, no subset can remove that bit from the AND, because removing elements only decreases the AND, and if every element has that bit set, it will always survive.

## Approaches

The most direct idea is to try every subset of friends, compute the bitwise AND for each subset, and track the largest size whose result equals x. This is correct, because it explores all possibilities. The problem is that the number of subsets is exponential in n, and even for n = 40 this already becomes infeasible, while here n goes up to 10^5.

A more structured observation comes from understanding how AND behaves. A number can only participate in a valid subset if it does not miss any bit that x requires. That means every selected value must satisfy (ai & x) = x. This immediately filters the input down to a candidate pool.

Now we only work with this filtered pool. If we take all of them, their AND is fixed. If this AND already equals x, then taking all candidates is optimal, because adding more elements only makes the AND smaller or equal in bits, never larger. So if we are already exactly at x, we should keep everything.

If the AND of all valid candidates is not equal to x, then there exists at least one bit that is 1 in all candidates but 0 in x. That bit can never be eliminated by removing some elements, because removal does not introduce zeros where none exist. In that case, no valid subset exists at all.

This collapses the problem into a single pass over the array with bitwise filtering and a final AND computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all subsets | O(2^n · n) | O(1) | Too slow |
| Filter + global AND check | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and reduce the problem to a simple filtering and aggregation step.

### Steps

1. Read n and x, and the array a.
2. Discard every value ai that does not satisfy (ai & x) = x.

This step ensures we never lose required bits of x in the final AND.
3. If no values remain after filtering, output −1.
4. Compute the bitwise AND of all remaining values.
5. If this final AND equals x, output the number of remaining elements.
6. Otherwise output −1.

### Why it works

Any valid subset must consist only of numbers that contain all bits of x, because a single violation would destroy x in the final AND. So filtering is not a restriction, it is a necessary condition for feasibility.

Once we restrict ourselves to valid numbers, the AND of any subset can only be greater than or equal to the AND of the full set in terms of bit containment, because removing elements can only turn 1 bits into 0 bits. This means the full filtered set gives the strongest possible AND. If even this strongest AND does not match x, then no subset can fix the missing or extra bits, so no solution exists. If it does match x, removing elements would only weaken the AND and move away from x, so keeping all is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        arr = list(map(int, input().split()))

        filtered = []
        for v in arr:
            if (v & x) == x:
                filtered.append(v)

        if not filtered:
            print(-1)
            continue

        cur = filtered[0]
        for v in filtered[1:]:
            cur &= v

        if cur == x:
            print(len(filtered))
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the reasoning directly. The filtering step enforces the necessary condition that every chosen number must contain all bits of x. The second loop computes the global AND of all remaining candidates, which represents the strongest possible AND achievable from any subset.

A common pitfall is trying to be clever about subsets after filtering, but there is no need. The monotonic nature of bitwise AND ensures that either the entire filtered set works or nothing works.

## Worked Examples

### Example 1

Input:

n = 4, x = 2

a = [2, 4, 7, 6]

First we filter by (ai & x) = x. Since x = 2 (010₂), we keep only numbers that have the second bit set. That gives [2, 7, 6].

Now we compute their AND step by step.

| Step | Current AND |
| --- | --- |
| Start | 2 (010) |
| AND with 7 | 2 (010) |
| AND with 6 | 2 (010) |

Final result is 2, which matches x, so we output 3.

This shows that keeping all valid candidates preserves enough structure to achieve the target.

### Example 2

Input:

n = 3, x = 3

a = [1, 2, 3]

Filtering with (ai & 3) = 3 keeps only 3, since both 1 and 2 miss required bits.

Now filtered = [3]. The AND is 3, matching x, so the answer is 1.

This demonstrates that the algorithm correctly handles cases where most elements are invalid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is checked once and then combined via a single AND pass |
| Space | O(n) worst case | Stores filtered list |

The total complexity across all test cases is linear in the input size, which fits comfortably within the constraints of 5 × 10^5 total elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    output = []

    def input():
        return sys.stdin.readline()

    t = int(sys.stdin.readline())
    for _ in range(t):
        n, x = map(int, sys.stdin.readline().split())
        arr = list(map(int, sys.stdin.readline().split()))

        filtered = [v for v in arr if (v & x) == x]
        if not filtered:
            output.append("-1")
            continue

        cur = filtered[0]
        for v in filtered[1:]:
            cur &= v

        output.append(str(len(filtered) if cur == x else -1))

    return "\n".join(output)

assert run("""1
6 0
7 3 5 2 8 4
""") == "6"

assert run("""1
4 2
2 4 7 6
""") == "3"

assert run("""1
2 1
3 7
""") == "-1"

assert run("""1
3 3
3 3 3
""") == "3"

assert run("""1
3 3
1 2 3
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| x = 0 case | all valid counted | zero-bit constraint handling |
| mixed values | partial filtering correctness | filter + AND behavior |
| impossible case | -1 | no valid subset |
| all equal valid | full acceptance | stability case |
| mixed validity | correct filtering dominance | edge filtering logic |

## Edge Cases

A key edge case is when x = 0. In this situation, every number automatically satisfies (ai & x) = x because x has no bits set. The filtered set becomes the entire array, and the AND of all numbers determines whether any extra constraints exist. If all numbers share a common bit, the AND will not be zero and the answer becomes −1; otherwise all elements can be taken.

Another important edge case is when filtering removes everything. For example, if x requires a bit that no number contains, then no element can satisfy (ai & x) = x. The algorithm correctly outputs −1 immediately without attempting any further computation.

A final subtle case occurs when the filtered set is non-empty but all elements share an extra common bit not present in x. In this case the global AND retains that bit, and since no subset can eliminate it, the final answer is correctly −1.
