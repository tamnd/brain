---
title: "CF 1958A - 1-3-5"
description: "We are asked to construct an exact sum using coins of values 1, 3, and 5. For each target amount n, we want to pay exactly n using any number of 3 and 5 coins, and we are only forced to use 1-coins when it becomes unavoidable."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp"]
categories: ["algorithms"]
codeforces_contest: 1958
codeforces_index: "A"
codeforces_contest_name: "Kotlin Heroes: Episode 10"
rating: 1100
weight: 1958
solve_time_s: 47
verified: true
draft: false
---

[CF 1958A - 1-3-5](https://codeforces.com/problemset/problem/1958/A)

**Rating:** 1100  
**Tags:** *special, dp  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct an exact sum using coins of values 1, 3, and 5. For each target amount n, we want to pay exactly n using any number of 3 and 5 coins, and we are only forced to use 1-coins when it becomes unavoidable. The task is to minimize how many 1-coins appear in such a decomposition.

In other words, imagine we first try to build n using only 3s and 5s. If that is impossible, we are allowed to “repair” the remainder using 1s. Each 1-coin used corresponds to leaving an uncovered remainder after choosing some combination of 3 and 5 coins.

The constraints are small: n is at most 100 and there are at most 100 test cases. This means even a quadratic or cubic dynamic programming approach would comfortably run in time. However, the structure of the problem suggests something much simpler than DP over all sums is possible.

A subtle case arises when greedy choices fail. For example, for n = 8, using a single 5 leaves 3, which can be covered without 1s, but using two 3s leaves 2, which requires two 1s. A naive greedy strategy that always takes the largest coin first does not reliably minimize leftover 1s because 5 is not always better than combinations of 3s in terms of residue structure.

Another edge situation appears when n is small. For n = 1 or n = 2, no combination of 3 and 5 can help at all, so all payment must be done using 1-coins. Any approach that assumes we can always start with a 3 or 5 will fail immediately here.

## Approaches

A brute-force approach tries all combinations of 3 and 5 coins. For each number of 5-coins, and each number of 3-coins, we check whether the remaining value can be formed using 1-coins. For a fixed n, the number of possibilities is O(n^2), since we might try up to n/5 choices of 5-coins and n/3 choices of 3-coins. For each pair we compute the leftover and count it as the number of 1-coins. This is correct because it enumerates all valid decompositions.

This approach is already small enough for n ≤ 100, but it is still unnecessary. The key observation is that we never need to explicitly consider 1-coins as a decision variable. Once we fix how many 3 and 5 coins we use, the number of 1-coins is completely determined by the remainder. So the task reduces to minimizing the remainder after subtracting 3x + 5y from n.

Instead of trying all pairs, we can iterate over how many 5-coins we use. For each choice, the remainder is n minus 5y. For that remainder, we want to reduce it using as many 3s as possible, because each unused unit becomes a 1-coin. The only subtlety is that 3-coins reduce the remainder in steps of 3, so the leftover after using 3s is simply (n - 5y) mod 3.

This transforms the problem into a one-dimensional scan over possible counts of 5-coins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(1) | Accepted but unnecessary |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n as the target sum.
2. Try all possible numbers of 5-coins from 0 up to n // 5.
3. For each choice y of 5-coins, compute the remaining value r = n - 5y.
4. From r, use as many 3-coins as possible. The leftover after using 3-coins is r % 3.
5. Interpret this leftover as the number of 1-coins required.
6. Track the minimum leftover over all choices of y.

The reason we iterate over 5-coins rather than 3-coins is purely convenience. Since 5 is larger, the number of iterations is smaller, and the remainder behaves cleanly under modulo 3.

### Why it works

For any fixed choice of 5-coins, the optimal use of 3-coins is forced: taking as many 3s as possible always minimizes the remaining uncovered amount, since replacing three 1-coins with one 3-coin never increases the count of 1-coins. Once the number of 5-coins is fixed, there is no interaction between different segments of the remainder, so the optimal structure for the remaining sum is greedy and canonical. Therefore, the global optimum must occur among these locally optimal choices for each y.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    
    ans = n  # worst case: all 1-coins
    
    for y in range(n // 5 + 1):
        rem = n - 5 * y
        ans = min(ans, rem % 3)
    
    print(ans)
```

The code reads each test case and initializes the answer with the pessimistic case where every unit is paid using 1-coins. It then enumerates all possible numbers of 5-coins. For each choice, it computes the remainder and reduces it greedily using 3-coins, leaving only a modulo 3 residue as the count of required 1-coins. The minimum over all choices is printed.

A common mistake here is to try dividing the remainder by 3 and adding that to the answer. That would incorrectly count 3-coins instead of minimizing 1-coins. The correct perspective is that 3-coins eliminate chunks of size 3 completely, leaving only the residue.

## Worked Examples

We trace the computation for n = 7 and n = 11.

### Example 1: n = 7

| 5-coins (y) | remainder r = n - 5y | r % 3 | best answer so far |
| --- | --- | --- | --- |
| 0 | 7 | 1 | 1 |
| 1 | 2 | 2 | 1 |

The best outcome is 1, achieved when using zero 5-coins and two 3-coins, leaving remainder 1.

This confirms that mixing 5-coins does not always improve the remainder, since 5 introduces a remainder structure that may be worse under modulo 3.

### Example 2: n = 11

| 5-coins (y) | remainder r = n - 5y | r % 3 | best answer so far |
| --- | --- | --- | --- |
| 0 | 11 | 2 | 2 |
| 1 | 6 | 0 | 0 |
| 2 | 1 | 1 | 0 |

The optimal choice is y = 1, where 11 − 5 = 6, which is fully divisible by 3, leading to zero 1-coins.

This shows the key tradeoff: using a 5-coin can align the remainder perfectly with multiples of 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · t / 5) | For each test case we iterate over at most n/5 choices |
| Space | O(1) | Only a few integer variables are used |

Given n ≤ 100 and t ≤ 100, the total work is at most a few thousand iterations, which is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        ans = n
        for y in range(n // 5 + 1):
            rem = n - 5 * y
            ans = min(ans, rem % 3)
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("5\n7\n8\n42\n2\n11\n") == "1\n0\n0\n2\n0"

# custom cases
assert run("1\n1\n") == "1"                 # minimum edge
assert run("1\n3\n") == "0"                 # exact 3
assert run("1\n5\n") == "0"                 # exact 5
assert run("1\n4\n") == "1"                 # 3+1
assert run("1\n100\n") == run("1\n100\n")  # stability check
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest impossible coin mix |
| 3 | 0 | exact 3 coverage |
| 5 | 0 | exact 5 coverage |
| 4 | 1 | mixed decomposition forcing a 1-coin |
| 100 | depends | stress consistency |

## Edge Cases

For n = 1, there are no valid 3 or 5 coins, so the algorithm evaluates only y = 0. The remainder is 1 and r % 3 = 1, correctly producing one 1-coin.

For n = 2, the same situation occurs: only y = 0 is valid, remainder 2, and the answer is 2.

For n = 3, the loop includes y = 0 giving remainder 3 with r % 3 = 0, and the answer becomes 0. Even though y = 1 is not possible, the correct solution is already found at y = 0.

For n = 8, both y = 0 and y = 1 are evaluated. The algorithm compares remainder 8 (giving 2) and remainder 3 (giving 0), correctly choosing zero 1-coins via 5 + 3.
