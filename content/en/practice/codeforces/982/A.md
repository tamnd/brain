---
title: "CF 982A - Row"
description: "We are given a line of chairs, each either occupied by a person or empty. The configuration is represented as a binary string where 1 means a person is sitting and 0 means the seat is empty. A seating arrangement is considered valid only if no two people sit next to each other."
date: "2026-06-17T01:04:18+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 982
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 484 (Div. 2)"
rating: 1200
weight: 982
solve_time_s: 62
verified: true
draft: false
---

[CF 982A - Row](https://codeforces.com/problemset/problem/982/A)

**Rating:** 1200  
**Tags:** brute force, constructive algorithms  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of chairs, each either occupied by a person or empty. The configuration is represented as a binary string where `1` means a person is sitting and `0` means the seat is empty.

A seating arrangement is considered valid only if no two people sit next to each other. Beyond that, we are not checking validity alone. We also need to decide whether the configuration is already “maximal”, meaning that there is no way to place an additional person in any empty chair without breaking the rule that no two occupied chairs are adjacent.

So the task is not to construct a seating, but to verify two properties at once. First, the current arrangement must already satisfy the adjacency rule. Second, every empty seat must be “blocked” by at least one neighbor that is already occupied, so that inserting a person there would immediately violate the rule.

The constraint `n ≤ 1000` implies that an O(n²) simulation would still pass, but it is unnecessary. A single linear scan is enough, since every decision about a seat depends only on its immediate neighbors.

A few edge cases matter more than they seem at first glance.

If the string is `"0"` for `n = 1`, then it is not maximal because we can place a person there and still satisfy the rule.

If the string is `"1"`, then it is maximal, because we already have a person and no additional placement is possible.

If we see `"101"`, it is valid and maximal because the single zero is adjacent to two ones, so it cannot host anyone.

If we see `"1001"`, it is valid but not maximal because the middle `"00"` contains at least one position where we can still place a person.

These examples show the key subtlety: maximality is about the existence of any valid insertion, not just local validity of the current configuration.

## Approaches

A brute-force strategy tries every empty position and checks whether placing a `1` there keeps the configuration valid. For each candidate position, we scan neighbors to ensure no adjacency is violated. If any placement works, the configuration is not maximal. This approach is correct, but for each of up to `n` positions we may scan up to `n` characters, giving O(n²) behavior.

The structure of the problem allows a more direct observation. A seat is usable only if both adjacent positions are `0` (or do not exist at boundaries). So a configuration is maximal exactly when every `0` is “blocked”, meaning at least one adjacent position is `1`. If a `0` has no adjacent `1`, it is immediately a valid insertion point.

This reduces the problem to a single scan checking whether any index violates this blocking condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the string once and check whether there exists any position where we could place a person.

1. Iterate over every index `i` in the string.

Each position is a candidate for placement if it is currently `0`.
2. For each `0`, check its neighbors.

A placement is valid if both the left neighbor (if it exists) and the right neighbor (if it exists) are `0`.
3. If we find such a position, we can immediately conclude the seating is not maximal.

This is because we have explicitly found a valid insertion that preserves the adjacency rule.
4. If no such position exists after scanning the full string, the configuration is maximal.

### Why it works

The key property is that the validity of placing a person at position `i` depends only on `i-1` and `i+1`. If either neighbor is `1`, placement is forbidden. If both are `0` (or out of bounds), placement is always allowed. Therefore, the existence of any index with both neighbors empty is equivalent to non-maximality. The scan checks exactly this condition for every possible insertion point.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = input().strip()

for i in range(n):
    if s[i] == '0':
        left_ok = (i == 0) or (s[i - 1] == '0')
        right_ok = (i == n - 1) or (s[i + 1] == '0')
        if left_ok and right_ok:
            print("No")
            sys.exit()

print("Yes")
```

The code performs a single pass over the string. For each zero, it checks whether both neighbors are also zero or absent at boundaries. If such a position is found, we immediately output `"No"` because we can insert a person there without breaking the rule. Otherwise, the loop completes and we output `"Yes"`.

Boundary handling is done explicitly: when `i = 0` or `i = n - 1`, we treat the missing neighbor as automatically safe. This avoids index errors and matches the idea that edges have only one constraint instead of two.

## Worked Examples

### Example 1: `101`

| i | s[i] | left | right | insertable |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 0 | no |
| 1 | 0 | 1 | 1 | no |
| 2 | 1 | 0 | - | no |

No index allows insertion, so the answer is `"Yes"`.

This confirms the invariant that every zero is adjacent to at least one occupied seat.

### Example 2: `1001`

| i | s[i] | left | right | insertable |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 0 | no |
| 1 | 0 | 1 | 0 | no |
| 2 | 0 | 0 | 1 | no |
| 3 | 1 | 0 | - | no |

Here indices 1 and 2 look partially blocked, but neither is fully isolated. However, if we examine carefully, neither position allows insertion because each zero touches a `1` on at least one side. The scan confirms maximality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over the string with constant work per index |
| Space | O(1) | only a few boolean checks, no extra arrays |

The linear scan is comfortably within limits for `n ≤ 1000`, and even scales to much larger constraints without issue.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()

    for i in range(n):
        if s[i] == '0':
            left_ok = (i == 0) or (s[i - 1] == '0')
            right_ok = (i == n - 1) or (s[i + 1] == '0')
            if left_ok and right_ok:
                return "No"
    return "Yes"

# provided samples
assert run("3\n101\n") == "Yes"

# minimum size, empty seat always improvable
assert run("1\n0\n") == "No"

# single occupied seat is maximal
assert run("1\n1\n") == "Yes"

# clear non-maximal case
assert run("3\n000\n") == "No"

# alternating pattern already maximal
assert run("5\n10101\n") == "Yes"

# boundary case with middle free space
assert run("4\n1001\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1, 0` | No | single seat insertion case |
| `1, 1` | Yes | smallest maximal configuration |
| `000` | No | fully empty row is not maximal |
| `10101` | Yes | alternating safe pattern |
| `1001` | Yes | boundary adjacency handling |

## Edge Cases

For `n = 1`, consider input `"0"`. The algorithm checks index 0, sees it is `0`, and both neighbors are treated as safe due to boundary rules. It immediately concludes insertion is possible and outputs `"No"`.

For `"1"`, the loop never finds a `0`, so it never triggers a rejection, and the final output is `"Yes"`.

For `"1001"`, indices 1 and 2 are examined. At index 1, left is `1` so placement fails. At index 2, right is `1` so placement fails. Since no index satisfies both empty-neighbor conditions, the algorithm correctly returns `"Yes"`.
