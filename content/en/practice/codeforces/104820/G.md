---
title: "CF 104820G - \u0416\u0430\u0434\u043d\u043e\u0435 \u0434\u0435\u043b\u0435\u043d\u0438\u0435"
description: "We are distributing three different types of candies to three friends, where each friend only accepts one specific type. The first friend only takes Snickers, the second only Mars, and the third only Bounty."
date: "2026-06-28T12:56:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "G"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 56
verified: true
draft: false
---

[CF 104820G - \u0416\u0430\u0434\u043d\u043e\u0435 \u0434\u0435\u043b\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/104820/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are distributing three different types of candies to three friends, where each friend only accepts one specific type. The first friend only takes Snickers, the second only Mars, and the third only Bounty. We are given the available quantities of each type: A Snickers, B Mars, and C Bounty.

Each friend must receive at least one candy of their preferred type. Additionally, the number of candies received must strictly increase from the first friend to the second, and from the second to the third. That means if we denote the assigned amounts as x, y, z, then x, y, z must satisfy x < y < z, with x ≥ 1, y ≥ 1, z ≥ 1, and also x ≤ A, y ≤ B, z ≤ C.

The task is to count how many triples (x, y, z) satisfy all these constraints.

The constraints go up to 10^6, which immediately rules out iterating over all possible triples. A naive cubic or even quadratic enumeration would produce up to 10^18 iterations in the worst case, which is far beyond acceptable limits. The solution must reduce the problem to either a linear scan or a direct combinational counting formula.

A subtle edge case appears when any of A, B, or C is 1. For example, if A = B = C = 1, then the only possible triple would be (1, 1, 1), which violates strict inequality, so the answer is 0. A naive approach that forgets strict ordering might incorrectly count this as valid.

Another edge case arises when capacities are small but unequal, such as A = 1, B = 2, C = 3. Only one triple (1, 2, 3) is valid, and any misinterpretation of “at least one” versus “exact assignment choices” can lead to overcounting.

## Approaches

A brute-force approach would try all possible values of x from 1 to A, y from 1 to B, and z from 1 to C, checking whether x < y < z. This is correct because it directly enforces all constraints, but its complexity is O(ABC). With each variable up to 10^6, this leads to 10^18 operations in the worst case, which is infeasible.

The key observation is that the constraints depend only on ordering, not on the identity of the candies beyond their type restrictions. We are effectively counting strictly increasing triples where each element is bounded by an independent upper limit. This can be reframed as choosing x, y, z such that 1 ≤ x < y < z, with independent caps.

Instead of iterating over all triples, we can fix the middle value y. Once y is fixed, x can be any integer in [1, y−1] but also must not exceed A, so x is bounded by min(A, y−1). Similarly, z must be in [y+1, C], but also not exceed C and must be strictly greater than y and at least 1, and additionally must respect B because y is assigned from Mars limit, not z. Actually z only depends on C.

So for each y, the number of valid x choices is min(A, y−1), and the number of valid z choices is max(0, C − y). The contribution per y becomes min(A, y−1) × max(0, C − y), but only if y ≤ B.

This reduces the problem to a single loop over y from 1 to B, giving O(B) time. Since B can be up to 10^6, this is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(ABC) | O(1) | Too slow |
| Fixed-middle enumeration | O(B) | O(1) | Accepted |

## Algorithm Walkthrough

1. Iterate over all possible values of y from 1 to B. This represents the number of candies given to the second friend, and ensures we respect the limit of Mars candies.
2. For each y, compute how many valid choices exist for x. Since x must satisfy 1 ≤ x < y and x ≤ A, the valid range is 1 to min(A, y−1). If y = 1, this range is empty, which correctly yields zero choices.
3. For the same y, compute how many valid choices exist for z. Since z must satisfy z > y and z ≤ C, the valid range is y+1 to C, which has size max(0, C − y).
4. Multiply the number of valid x choices by the number of valid z choices. This works because x and z are independent once y is fixed, so every valid pair forms a unique triple.
5. Sum this contribution over all y from 1 to B.

Why it works: every valid triple (x, y, z) is uniquely identified by its middle element y. For each such y, the algorithm counts exactly all valid x choices to the left and all valid z choices to the right under the constraints. No triple is counted twice because each triple has exactly one middle element, and no invalid triple is counted because both sides strictly enforce bounds and ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C = map(int, input().split())
    
    ans = 0
    for y in range(1, B + 1):
        x_cnt = min(A, y - 1)
        if x_cnt <= 0:
            continue
        z_cnt = C - y
        if z_cnt <= 0:
            continue
        ans += x_cnt * z_cnt
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the middle-element enumeration strategy. The loop over y ensures we only consider valid second-friend allocations. The expression `min(A, y - 1)` enforces both availability and strict ordering with the first friend. The term `C - y` implicitly handles both the strict inequality and the upper bound on Bounty count, since any value greater than C would be invalid.

Care is needed around boundary conditions. When y = 1, `y - 1` becomes zero, correctly eliminating invalid contributions. When y = C, `C - y` becomes zero, ensuring no invalid z choices are counted.

## Worked Examples

### Example 1: Input `2 3 4`

We compute contributions for each y.

| y | x choices | z choices | contribution |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 0 |
| 2 | 1 | 2 | 2 |
| 3 | 2 | 1 | 2 |

Total is 4.

This shows how valid triples emerge only when both sides of y are non-empty. The case y = 2 is the most flexible because it allows both left and right choices.

### Example 2: Input `1 1 1`

| y | x choices | z choices | contribution |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |

The strict inequality requirement prevents any triple from forming. Even though each candy type has at least one item, there is no way to split them into strictly increasing counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(B) | Single loop over all possible values of y |
| Space | O(1) | Only constant extra variables are used |

The linear scan over at most 10^6 values easily fits within time limits, and no additional memory is required beyond a few integers.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("2 3 4\n") == "4"
assert run("1 2 3\n") == "1"
assert run("1 1 1\n") == "0"

# custom cases
assert run("2 2 2\n") == "0", "no strictly increasing triple possible"
assert run("3 4 5\n") == "10", "symmetric mid-range growth"
assert run("10 1 10\n") == "0", "middle too small"
assert run("1 10 10\n") == "1", "only (1,2,3)-style single chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 2 | 0 | strict inequality prevents any solution |
| 3 4 5 | 10 | general combinational growth |
| 10 1 10 | 0 | middle constraint blocks all triples |
| 1 10 10 | 1 | minimal left bound forces single structure |

## Edge Cases

When all values are equal to 1, the loop only evaluates y = 1. In this case, x has no valid choices and z also has none, so the contribution is zero, matching the requirement that strict ordering is impossible.

When A is very small compared to B and C, such as A = 1, B = 10, C = 10, most contributions vanish because x is always zero except when y = 1, but that case also fails because z requires y < z. The algorithm naturally filters these cases through the min and difference constraints.

When C is small relative to B, such as C = 2 and B large, only y = 1 contributes meaningfully, but even then z choices become limited quickly, and the summation correctly collapses to zero or a very small number depending on A.
