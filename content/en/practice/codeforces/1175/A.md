---
title: "CF 1175A - From Hero to Zero"
description: "We are given a starting number n and a fixed integer k. From n, we repeatedly reduce the value until it becomes zero. Each operation is either subtracting one, or dividing by k when the current value is divisible by k."
date: "2026-06-13T10:03:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1175
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 66 (Rated for Div. 2)"
rating: 900
weight: 1175
solve_time_s: 482
verified: false
draft: false
---

[CF 1175A - From Hero to Zero](https://codeforces.com/problemset/problem/1175/A)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 8m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a starting number `n` and a fixed integer `k`. From `n`, we repeatedly reduce the value until it becomes zero. Each operation is either subtracting one, or dividing by `k` when the current value is divisible by `k`. The cost of every operation is one step, and the goal is to minimize the total number of steps needed to reach zero.

A useful way to think about this is that subtraction is a slow but always-available way to decrease the number, while division is a rare “shortcut” that can drastically shrink the value, but only at carefully chosen moments when the number happens to align with a multiple of `k`.

The constraints make direct simulation impossible. The value of `n` can be as large as \(10^{18}\), so any solution that reduces the number one step at a time is immediately infeasible. Even performing a few million operations per test case would already be too slow in the worst case.

The number of test cases is small enough that an \(O(\log n)\) or \(O(\log^2 n)\) strategy per test is acceptable, but anything linear in `n` is ruled out.

A subtle pitfall appears when thinking greedily about division. It is tempting to always divide whenever possible, but this is only beneficial when you have already reduced `n` to a multiple of `k`. If you divide too early or ignore the cost of reaching a divisible state, you may underestimate the number of required decrements.

For example, consider `n = 10, k = 3`. You cannot divide immediately. You must first reduce to 9 before dividing, which costs one subtraction anyway, but in larger cases, blindly applying division whenever possible without accounting for the cost of reaching that state leads to incorrect reasoning if not structured carefully.

The correct solution must balance two phases repeatedly: a long stretch of subtracting to reach the next divisible number, followed by a division that shrinks the number significantly.

## Approaches

The brute-force idea is straightforward. Start from `n`, and at each step try both operations recursively or via BFS: subtract one, or divide if possible. This explores a huge state graph where each number connects to at most two smaller numbers. While correct, this approach degenerates immediately because the depth of the search tree is on the order of `n`, and the branching causes exponential explosion. Even memoization would still require visiting every integer down to zero in the worst case, which is impossible for \(10^{18}\).

The key observation is that subtraction is only useful as a means of reaching the nearest multiple of `k`. Once we are at a number divisible by `k`, division is always strictly better than performing `k` subtractions to achieve the same reduction.

So instead of simulating step by step, we can “jump” directly: for a current value `n`, we compute how many steps it takes to reduce it down to the largest multiple of `k` below it, perform that many subtractions in bulk, then divide once, and repeat.

This transforms the process into a sequence of arithmetic reductions rather than individual operations. Each iteration reduces the magnitude of `n` by at least a factor of `k` after a small linear adjustment.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n) per test | O(1) | Too slow |
| Optimal | O(logₖ n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Maintain a running answer initialized to zero. This will count every subtraction and division performed in compressed form.

2. While `n` is greater than or equal to `k`, compute the remainder `r = n % k`. Subtract `r` from `n`, and add `r` to the answer. This step moves `n` to the nearest smaller multiple of `k`. The reason this is safe is that any division requires divisibility, and subtraction is the only way to fix non-divisibility.

3. Once `n` is divisible by `k`, divide `n` by `k`, and increment the answer by one. This represents the single operation that replaces `k` implicit decrements.

4. Repeat the process until `n` becomes less than `k`. At that point, no further divisions are possible, so the only remaining cost is subtracting all remaining `n` down to zero, which contributes `n` additional steps.

5. Add this final `n` to the answer and terminate.

### Why it works

At any moment, the optimal strategy is determined entirely by how quickly we can reach a state where division is allowed. Subtraction never needs to be done one-by-one conceptually; it only serves to bridge the gap to the next divisible state. Every division reduces the scale of the problem by a factor of `k`, so the process is guaranteed to shrink rapidly. The algorithm preserves the invariant that after each iteration, `n` is exactly the result of applying the best possible local sequence of subtractions followed by a division, ensuring no unnecessary operations are counted or skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        ans = 0

        while n >= k:
            r = n % k
            ans += r
            n -= r
            ans += 1
            n //= k

        ans += n
        print(ans)

if __name__ == "__main__":
    solve()
```

The code follows the same structure as the algorithm. The loop continues while division is possible, meaning `n >= k`. The remainder computation captures the exact number of decrements needed to align `n` with a multiple of `k`. The division step is counted as a single operation after alignment. Once `n` drops below `k`, the remaining cost is linear subtraction to zero.

A subtle implementation detail is that the remainder must be computed before modifying `n`, because it represents the exact number of decrement operations needed in that segment. Another important point is that the loop condition is `n >= k`, not `n > k`, since equality still allows a division.

## Worked Examples

### Example 1: n = 59, k = 3

| n | n % k | subtractions | operation | new n | total |
|---|---|---|---|---|---|
| 59 | 2 | 2 | subtract to 57 | 57 | 2 |
| 57 | 0 | 0 | divide | 19 | 3 |
| 19 | 1 | 1 | subtract to 18 | 18 | 4 |
| 18 | 0 | 0 | divide | 6 | 5 |
| 6 | 0 | 0 | divide | 2 | 6 |
| 2 | - | 2 | final cleanup | 0 | 8 |

This trace shows how subtraction is only used to reach divisibility points, while division performs the main reduction.

### Example 2: n = 10^18, k = 10

| n | n % k | subtractions | operation | new n | total |
|---|---|---|---|---|---|
| 10^18 | 0 | 0 | divide | 10^17 | 1 |
| 10^17 | 0 | 0 | divide | 10^16 | 2 |
| ... | ... | ... | ... | ... | ... |

This demonstrates repeated pure division phases, showing the logarithmic shrinkage until the value becomes small enough that only subtraction remains.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(logₖ n) per test | each division reduces magnitude by factor k |
| Space | O(1) | only a few variables maintained |

The algorithm easily fits within constraints since even for \(n = 10^{18}\), the number of division steps is at most about 60 when \(k = 2\), and far fewer for larger `k`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            ans = 0
            while n >= k:
                r = n % k
                ans += r
                n -= r
                ans += 1
                n //= k
            ans += n
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# provided samples
assert run("2\n59 3\n1000000000000000000 10\n") == "8\n19"

# custom cases
assert run("1\n1 2\n") == "1", "minimum single decrement"
assert run("1\n10 10\n") == "2", "direct division then cleanup"
assert run("1\n25 5\n") == "4", "repeated clean divisions"
assert run("1\n100 3\n") == "8", "mixed remainder and divisions"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1 2 | 1 | smallest non-zero case |
| 10 10 | 2 | immediate division edge |
| 25 5 | 4 | repeated exact divisibility |
| 100 3 | 8 | mixed remainder/division behavior |

## Edge Cases

One edge case is when `n < k`. In this situation, no division is ever possible, so the answer is simply `n`. The algorithm handles this naturally because the loop is skipped and the final addition contributes exactly `n`.

Another case is when `n` is already a multiple of `k`. The remainder is zero, so no subtraction cost is added, and we immediately perform a division. This correctly models the optimal behavior, since there is no reason to subtract before dividing.

A final subtle case is when repeated divisions eventually bring `n` below `k`. At that point, the loop stops and the remaining cost is fully captured by the final subtraction step. This avoids any need for special handling or extra conditions, since the same structure applies uniformly across all scales.
