---
title: "CF 102791E - Numbers on Whiteboard"
description: "The board starts with every integer from 1 to n written exactly once. An operation removes two existing numbers a and b and replaces them with the ceiling of their average. After repeating this exactly n - 1 times, only one number remains."
date: "2026-07-27T18:11:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "E"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 78
verified: true
draft: false
---

[CF 102791E - Numbers on Whiteboard](https://codeforces.com/problemset/problem/102791/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The board starts with every integer from 1 to n written exactly once. An operation removes two existing numbers a and b and replaces them with the ceiling of their average. After repeating this exactly n - 1 times, only one number remains. The task is to make that final number as small as possible and print the sequence of chosen pairs that achieves it.

The value of n can be as large as 200000, so any approach that repeatedly searches through all current board values or simulates many possible choices is impossible. A solution needs to perform only a constant amount of work per operation, because there are already n - 1 operations that must be printed. This rules out approaches with quadratic behavior such as trying every possible pair.

A common mistake is to assume that always combining the two smallest values is optimal. The operation is not ordinary averaging because the result is rounded upward, and the construction needs to control which values survive, not just reduce the current minimum. For example, when n = 3, the input is:

```
3
```

A careless greedy strategy might combine 1 and 2 first, producing 2, then combine 2 and 3, producing 3. The final value becomes 3, but the optimal output leaves 2. The right sequence is to combine 2 and 3 first, producing 3, then combine 1 and 3, producing 2.

Another edge case is n = 2. There is no room to create duplicate values or perform a multi-step construction. The only possible operation is combining 1 and 2, which gives 2, so any algorithm that assumes it can always use a repeated value will fail.

## Approaches

A brute-force solution would try different pairs to discover the smallest possible final number. This is correct because every valid sequence of operations can be represented as a tree of pair selections, and exploring all trees would eventually find the optimum. The problem is that the number of possible choices grows extremely quickly. Even the first operation has about n² possible pairs, and there are n - 1 operations, making exhaustive exploration far beyond the available limits.

The key observation is that the minimum possible answer is always 2. The operation can never produce a value smaller than 2 at the very end because the last operation combines two positive integers and the smallest possible pair available after reductions cannot create 1. The remaining challenge is constructing operations that reach 2.

The construction works by repeatedly creating a controlled large value and moving it downward. First, combine n and n - 2. The result is n - 1 because the average of these two numbers is exactly n - 1. Then combine n - 1 with itself, producing n - 1 again. After this, the same idea can be applied to the remaining lower numbers: combine i with i + 2 for decreasing i. Each operation removes one unused number while keeping the important value available. Eventually the only remaining number is 2.

The brute-force works because it explores every possible reduction, but it fails when n grows because the search space is enormous. The observation that the operation can preserve carefully chosen values lets us replace the search with a direct construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of possible operation trees) | O(n) | Too slow |
| Optimal | O(n) | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Print 2 as the minimum final value. The construction below always leaves exactly this number.
2. If n equals 2, combine 1 and 2 directly. Their rounded average is 2, which is the only possible answer.
3. For n greater than 2, combine n and n - 2. The produced value is n - 1 because ceil((n + n - 2) / 2) equals n - 1.
4. Combine n - 1 with n - 1. This keeps n - 1 unchanged and removes the original n - 1 value.
5. For every i from n - 3 down to 1, combine i and i + 2. The current board contains i + 2 at this stage, and the operation creates i + 1, which becomes the value needed for the next step.

The reason the construction moves downward by one is that every operation transforms two numbers with distance two between them into the middle number. This allows us to eliminate all large values while maintaining a single chain that eventually reaches 2.

Why it works:

The invariant is that after handling a number i, all values larger than i + 1 have been removed and the board still contains the value i + 1. The first two operations establish this invariant for the largest values. Every following operation preserves it because combining i and i + 2 creates i + 1. When i reaches 1, the last operation combines 1 and 3, producing 2. Since no final value below 2 is possible, the construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = ["2"]

    if n == 2:
        ans.append("1 2")
    else:
        ans.append(f"{n - 2} {n}")
        ans.append(f"{n - 1} {n - 1}")
        for i in range(n - 3, 0, -1):
            ans.append(f"{i} {i + 2}")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program stores the output lines instead of printing after every operation. This avoids unnecessary output overhead while still using only linear memory for the generated answer.

The special case n = 2 is handled separately because the general construction needs the numbers n - 2 and n - 1 to exist. For larger n, the first operation uses n and n - 2, which are always valid values. The loop starts at n - 3 and stops at 1, producing exactly n - 3 additional operations after the first two, for a total of n - 1 operations.

All arithmetic stays within normal integer limits because the largest value involved is n, which is at most 200000.

## Worked Examples

For n = 4, the algorithm produces:

| Step | Operation | Resulting important value |
| --- | --- | --- |
| Initial | Values 1, 2, 3, 4 | 4 |
| 1 | Combine 2 and 4 | 3 |
| 2 | Combine 3 and 3 | 3 |
| 3 | Combine 1 and 3 | 2 |

The final number is 2. This demonstrates the first part of the construction where the largest values are converted into a chain leading downward.

For n = 5, the algorithm produces:

| Step | Operation | Resulting important value |
| --- | --- | --- |
| Initial | Values 1, 2, 3, 4, 5 | 5 |
| 1 | Combine 3 and 5 | 4 |
| 2 | Combine 4 and 4 | 4 |
| 3 | Combine 2 and 4 | 3 |
| 4 | Combine 1 and 3 | 2 |

This trace shows how the invariant is maintained. After the first two operations, the remaining large value decreases one by one until only 2 is left.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Exactly n - 1 operations are generated. |
| Space | O(n) | The output itself contains n lines, while the algorithm logic uses constant extra memory. |

The limits require a linear solution because n can reach 200000. The algorithm performs a small fixed amount of work for each operation, so it easily fits within the time limit.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    ans = ["2"]

    if n == 2:
        ans.append("1 2")
    else:
        ans.append(f"{n - 2} {n}")
        ans.append(f"{n - 1} {n - 1}")
        for i in range(n - 3, 0, -1):
            ans.append(f"{i} {i + 2}")

    return "\n".join(ans)

assert solve("2\n") == "2\n1 2", "minimum n"
assert solve("4\n") == "2\n2 4\n3 3\n1 3", "sample style case"
assert solve("5\n") == "2\n3 5\n4 4\n2 4\n1 3", "chain construction"
assert solve("200000\n").splitlines()[0] == "2", "maximum size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | Final value 2 with one operation | The smallest allowed n |
| 4 | A valid three-operation construction | The standard example pattern |
| 5 | A longer decreasing chain | The invariant through multiple steps |
| 200000 | First line is 2 | Handling the maximum constraint |

## Edge Cases

For n = 2, the board contains only 1 and 2. The algorithm immediately prints the only possible operation, `1 2`. The resulting value is ceil(3 / 2), which equals 2.

For n = 3, the algorithm does not use the special case. It first combines 1 and 3, creating 2, then combines 2 and 2, keeping 2. The final value is still 2, and the construction avoids the incorrect strategy of reducing the smallest numbers first.

For large n, the algorithm never stores the board explicitly. It only prints a sequence whose values are guaranteed to exist at the moment they are used. The decreasing loop guarantees that no invalid pair is requested, even when n reaches 200000.
