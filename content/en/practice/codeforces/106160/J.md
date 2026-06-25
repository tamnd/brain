---
title: "CF 106160J - Jacobi Numbers"
description: "The task asks us to express a positive integer n as a sum of cubes. We must print a list of integers, each between -10000 and 10000, whose cubes add up exactly to n. Any valid decomposition is accepted, and the number of printed terms cannot exceed 10000."
date: "2026-06-25T11:13:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "J"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 29
verified: true
draft: false
---

[CF 106160J - Jacobi Numbers](https://codeforces.com/problemset/problem/106160/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to express a positive integer `n` as a sum of cubes. We must print a list of integers, each between `-10000` and `10000`, whose cubes add up exactly to `n`. Any valid decomposition is accepted, and the number of printed terms cannot exceed `10000`.

The input is a single integer representing the target value. The output first gives how many integers are in the decomposition, followed by those integers themselves.

The constraint that `n` is at most `9241` is the key detail. A direct construction can use the fact that `1³ = 1`. If we print `n` copies of the number `1`, their cubes sum to `n`. Since the largest possible `n` is `9241`, this produces at most `9241` terms, which is safely below the limit of `10000`.

This immediately rules out the need for number theory searches, dynamic programming, or precomputation. Any approach that tries to find a shorter representation is solving a harder problem than the one being asked.

The main edge cases are related to output size and handling the smallest possible value. For `n = 1`, the output should contain one term:

```
Input
1

Output
1
1
```

A careless implementation might try to initialize an empty answer and forget to add anything for the smallest value.

For the maximum allowed value:

```
Input
9241

Output
9241
1 1 1 ... 1
```

with `9241` copies of `1`, the answer is still valid. A solution that assumes the number of terms is small could accidentally violate the output limit if it tried to create many unnecessary values.

Another common mistake is printing the cubes instead of the original integers. For example, for `n = 3`, the correct output is:

```
Input
3

Output
3
1 1 1
```

because the sum being checked is `1³ + 1³ + 1³`, not `1 + 1 + 1` as plain values.

## Approaches

The brute-force interpretation would be to search for a combination of numbers whose cubes add to `n`. One could try every possible cube value, use recursion, or build a dynamic programming solution over possible sums. These approaches are correct because they explore valid decompositions, but they completely ignore the generous output limit. The search space is enormous compared with the tiny bound on `n`.

The brute-force search fails because it spends time discovering a decomposition that already exists in the simplest possible form. The observation that `1³ = 1` changes the problem entirely. Since the target is never larger than `9241`, repeating `1` exactly `n` times always satisfies both the sum condition and the maximum number of terms condition.

The optimal solution is simply to output `n` copies of `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Depends on search strategy, potentially exponential | Depends on search strategy | Too slow |
| Optimal | O(n) | O(n) for storing output | Accepted |

## Algorithm Walkthrough

1. Read the target number `n`. The value itself tells us how many terms we need, because every term `1` contributes exactly `1` to the cube sum.
2. Create a decomposition containing `n` copies of the integer `1`. The resulting cube sum is `n × 1³`, which is exactly `n`.
3. Print `n` as the number of terms, followed by the list of ones. The maximum possible number of terms is `9241`, so the output limit is never exceeded.

Why it works: the invariant is that after choosing `k` copies of `1`, the partial cube sum is exactly `k`. When the algorithm finishes after choosing `n` copies, the sum is exactly `n`. Every chosen value is within the allowed range, and the number of chosen values is valid because `n ≤ 9241 < 10000`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    print(n)
    print(" ".join(["1"] * n))

if __name__ == "__main__":
    solve()
```

The program reads the single integer and uses it directly as the number of terms. The list construction creates exactly `n` copies of the value `1`.

The output order matters because the first line must contain the count of numbers. After that, the second line contains the actual decomposition.

There are no overflow concerns because Python integers are arbitrary precision, and the largest output contains only `9241` small integers.

## Worked Examples

Consider the input:

```
3
```

The algorithm creates three copies of `1`.

| Step | n | Generated terms | Cube sum |
| --- | --- | --- | --- |
| Start | 3 | empty | 0 |
| Add first term | 3 | 1 | 1 |
| Add second term | 3 | 1 1 | 2 |
| Add third term | 3 | 1 1 1 | 3 |

The final sum is `1³ + 1³ + 1³ = 3`, which matches the target.

Consider the input:

```
7
```

| Step | n | Generated terms | Cube sum |
| --- | --- | --- | --- |
| Start | 7 | empty | 0 |
| Finish construction | 7 | 1 1 1 1 1 1 1 | 7 |

The example shows that the algorithm does not need to search for special cube identities. It relies only on the always-valid identity `1³ = 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The program writes `n` numbers to the output. |
| Space | O(n) | The list of `n` ones is created before printing. |

The maximum value of `n` is `9241`, so both the running time and memory usage are very small.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    n = int(input())
    return str(n) + "\n" + " ".join(["1"] * n) + "\n"

# minimum-size input
assert solve_data("1\n") == "1\n1\n", "minimum value"

# small normal case
assert solve_data("5\n") == "5\n1 1 1 1 1\n", "small value"

# boundary condition
assert solve_data("9241\n").count("1") == 9241, "maximum value"

# another custom case
assert solve_data("100\n").splitlines()[0] == "100", "term count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | One term containing `1` | Smallest valid target |
| `5` | Five copies of `1` | Basic construction |
| `9241` | `9241` copies of `1` | Maximum allowed target and output size |
| `100` | `100` copies of `1` | Larger ordinary case |

## Edge Cases

For `n = 1`, the algorithm creates exactly one term. The execution is:

```
n = 1
answer = [1]
```

The cube sum is `1³ = 1`, so the output is valid.

For `n = 9241`, the algorithm creates `9241` terms. The execution is:

```
n = 9241
number of terms = 9241
```

The cube sum is:

```
9241 × 1³ = 9241
```

The number of terms is still below the allowed maximum of `10000`, so the construction remains valid.

For values such as `n = 3`, a search-based solution might try to find a shorter representation like `1³ + 1³ + 1³`, but the optimal algorithm does exactly that without searching. The generated sequence always has the required sum because every individual contribution is predictable.
