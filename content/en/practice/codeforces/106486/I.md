---
title: "CF 106486I - \u5976\u9f99\u5854"
description: "We are given a collection of blocks, each block having a positive integer size. We want to stack all of them into a single vertical tower. The only rule is that a block can be placed on top of another block only if its size is strictly smaller than the block below it."
date: "2026-06-19T17:31:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106486
codeforces_index: "I"
codeforces_contest_name: "Dalian University of Technology, Software College 2025 Freshman Contest"
rating: 0
weight: 106486
solve_time_s: 48
verified: true
draft: false
---

[CF 106486I - \u5976\u9f99\u5854](https://codeforces.com/problemset/problem/106486/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of blocks, each block having a positive integer size. We want to stack all of them into a single vertical tower. The only rule is that a block can be placed on top of another block only if its size is strictly smaller than the block below it. Every block must be used exactly once, and all blocks must belong to the same tower.

The task is to decide whether such a single tower can be formed.

The input size can be as large as 200000 blocks, and each size can be as large as 10^9. This immediately rules out any solution that tries to simulate all possible stacking orders or backtracking over permutations. Anything quadratic or exponential is out of reach. A solution must be essentially linear or linearithmic, most likely O(n log n).

A subtle point is that equality is forbidden. If two blocks have the same size, they cannot be stacked on each other in either direction. This creates a hard constraint: equal values behave like identical “heights” that block each other.

One edge case that often breaks naive reasoning is when all values are equal. For example, input `1 1` clearly cannot form a tower, because neither can go on top of the other. Another important edge case is a single element array like `5`, which is always valid.

## Approaches

A brute-force interpretation would be to try to construct a valid ordering by picking any block as the bottom, then repeatedly choosing any unused smaller block to place on top. This essentially explores permutations with a constraint check at each step.

This works conceptually because it enforces the strict decreasing condition directly. However, at each layer there can be many candidate choices, and the search space becomes factorial in size. With n up to 200000, this is completely infeasible.

The key observation is that the problem does not actually depend on adjacency choices beyond ordering. Since every block must appear in a strictly decreasing sequence, we are asking a simpler question: can we arrange all elements into a strictly decreasing sequence using all elements exactly once?

That is only possible if and only if all values are distinct. If two elements are equal, there is no way to order them strictly decreasing without violating the rule, because equality breaks strictness and we cannot “separate” them with intermediate values of the same size.

So the entire problem reduces to checking whether duplicates exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sort / Hash check duplicates | O(n log n) or O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all numbers representing block sizes.
2. Detect whether any value appears more than once.
3. If a duplicate exists, immediately conclude that a strict stacking order is impossible.
4. Otherwise, conclude that all elements can be arranged in strictly decreasing order, hence a valid tower exists.

The reasoning behind step 3 is that any duplicate pair forces a violation of strict inequality somewhere in the final stack, regardless of ordering.

## Why it works

A valid tower corresponds exactly to a permutation of all elements arranged in strictly decreasing order. Strict decreasing sequences require every adjacent pair to satisfy `a[i] > a[i+1]`. If two values are equal, they must appear somewhere in the sequence, but no matter where they are placed, they will either become adjacent or be separated by smaller values. In both cases, one of them will fail to maintain strict ordering relative to its neighbors in a full permutation. Therefore, the existence of any duplicate makes the task impossible, and absence of duplicates guarantees that sorting in decreasing order produces a valid tower.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
a = list(map(int, input().split()))

seen = set()
for x in a:
    if x in seen:
        print("No")
        sys.exit(0)
    seen.add(x)

print("Yes")
```

The implementation directly tracks whether we have seen a value before. The moment a repetition is found, we can terminate early since a valid tower is impossible. If the loop finishes, all values are distinct and a strictly decreasing ordering exists by sorting, even though we do not explicitly construct it.

The key design choice is early exit, which avoids unnecessary work in worst cases. Using a set ensures average O(1) membership checks, keeping the solution linear in expectation.

## Worked Examples

### Example 1

Input:

`1 2 3 4 5`

| Processed value | Seen set before | Action | Duplicate found |
| --- | --- | --- | --- |
| 1 | {} | add 1 | No |
| 2 | {1} | add 2 | No |
| 3 | {1,2} | add 3 | No |
| 4 | {1,2,3} | add 4 | No |
| 5 | {1,2,3,4} | add 5 | No |

Result: Yes

This confirms that when all elements are distinct, a strict ordering exists.

### Example 2

Input:

`1 1`

| Processed value | Seen set before | Action | Duplicate found |
| --- | --- | --- | --- |
| 1 | {} | add 1 | No |
| 1 | {1} | stop | Yes |

Result: No

This shows the failure case: equality immediately breaks strict stacking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) average | Each element is inserted and checked in a hash set once |
| Space | O(n) | Storage of seen elements in worst case |

The constraints allow up to 200000 elements, so a linear solution easily fits within time limits. The memory usage is also small compared to the 1024 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    a = list(map(int, input().split()))

    seen = set()
    for x in a:
        if x in seen:
            return "No"
        seen.add(x)
    return "Yes"

# provided samples
assert run("5\n1 2 3 4 5\n") == "Yes"
assert run("2\n1 1\n") == "No"

# custom cases
assert run("1\n10\n") == "Yes"
assert run("3\n3 2 1\n") == "Yes"
assert run("4\n1 2 2 3\n") == "No"
assert run("6\n6 5 4 3 2 1\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | Yes | minimum case |
| all distinct descending | Yes | already valid structure |
| one duplicate in middle | No | detects non-adjacent duplication |
| full reversed order | Yes | maximum strict case |

## Edge Cases

A single element case like `7` passes immediately since no comparison is needed, and the set remains empty until insertion completes. The algorithm correctly outputs Yes.

A fully equal array like `5 5 5 5` fails at the second insertion because the second element is already in the set. The detection is immediate, so no further processing occurs.

A mixed case such as `2 1 2` also fails correctly. After inserting `2` and `1`, the final `2` triggers the duplicate check even though the duplicate is not adjacent, confirming that adjacency is irrelevant and only global uniqueness matters.
