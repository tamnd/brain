---
title: "CF 102264B - Class Treasurer"
description: "We have a string of A and B votes arranged in student-ID order. A representative set is any contiguous interval of this string. For an interval to be safe, Betty must not have more than K votes over Amy."
date: "2026-08-19T02:58:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102264
codeforces_index: "B"
codeforces_contest_name: "2019 Facebook Hacker Cup, Round 1"
rating: 0
weight: 102264
solve_time_s: 260
verified: true
draft: false
---

[CF 102264B - Class Treasurer](https://codeforces.com/problemset/problem/102264/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a string of `A` and `B` votes arranged in student-ID order. A representative set is any contiguous interval of this string. For an interval to be safe, Betty must not have more than `K` votes over Amy. Equivalently, if we encode an `A` as `+1` and a `B` as `-1`, every contiguous subarray must have sum at least `-K`.

Before the representative interval is chosen, we may change some `B` votes into `A` votes. Changing student `i` costs `2^i`, so earlier students are exponentially cheaper. The task is to choose a set of students whose votes are changed so that every interval is safe, while minimizing the actual cost. Only after finding that minimum do we take it modulo `1,000,000,007`.

For a prefix ending at position `i`, let its balance be the number of `A` votes minus the number of `B` votes. If the prefix balances are `P_0, P_1, ..., P_N`, then the balance of interval `[l, r]` is `P_r - P_{l-1}`. Betty wins exactly when this value is less than `-K`, so the condition we need is

`P_r >= P_{l-1} - K`

for every `l <= r`. While scanning from left to right, this means the current prefix balance may never fall more than `K` below the largest prefix balance seen before it.

The value of `N` can reach one million. An `O(N^2)` method would inspect on the order of `10^12` intervals in the worst case, which is completely infeasible. The algorithm needs to process each student a constant number of times, giving an `O(N)` target. The number of test cases is also large, so unnecessary logarithmic factors and large auxiliary structures matter in Python.

There are several boundary cases that easily break an otherwise plausible implementation. With `N = 1`, `K = 0`, and `V = B`, the answer is `2`, because the only representative set is the single student and Betty would otherwise win. A careless implementation that only checks intervals of length at least two would return zero.

With `N = 4`, `K = 0`, and `V = BAAB`, the answer is `18`. Flipping student 1 alone makes the long intervals safe, but student 4 is still a Betty-only representative set, so it must also be flipped. A prefix-only check can silently miss that singleton interval.

With `N = 4`, `K = 1`, and `V = ABBA`, the answer is `4`, not `8`. The bad interval is students 2 through 3, and the cheapest `B` inside it is student 2. A greedy rule that always flips the current student when a violation is detected would flip student 3 and pay `8`.

Finally, when `K = N`, the answer is always zero. No non-empty representative set has more than `N` votes for Betty, so Betty cannot exceed Amy by more than `K`. An implementation using a strict inequality in the wrong direction can incorrectly perform flips here.

## Approaches

The direct approach is to try every possible set of students to flip, then verify every contiguous representative set. There are `2^N` possible choices of students, and even checking one choice requires examining `O(N^2)` intervals. This is already hopeless for very small `N`.

A more reasonable brute force fixes how many students are flipped and chooses the cheapest possible students. Since the costs are `2^i`, among any fixed number of students it is always cheaper to use earlier `B` voters. One can then test whether the first `m` `B` voters are sufficient. This gives a monotone feasibility condition and permits binary search, but every feasibility check scans the entire string, resulting in `O(N log N)` time.

The structure of the violation gives a stronger linear solution. While scanning prefixes, keep the largest effective prefix balance seen so far. If the current balance is at least that maximum minus `K`, every interval ending here is safe. If the current balance is smaller, there is a bad interval whose left endpoint is immediately after a position attaining the maximum prefix balance.

Suppose that position is `p`. Any repair of this bad interval must flip a `B` somewhere in `[p + 1, i]`. Since costs increase strictly with the student index, the cheapest possible choice is the leftmost unflipped `B` in that interval. We flip exactly that student.

The chosen positions move monotonically to the right. Once a `B` lies before the beginning of the current bad interval, it can never be useful for a later violation because future bad intervals start no earlier than the current one. This gives us a single forward pointer for finding the next eligible `B`.

There is one subtlety. Flipping student `p` changes the effective balance of every prefix from `p` onward by `2`, including prefixes that were already processed. To maintain the maximum prefix balance correctly, we keep a monotonic deque over the original prefix sums. When a flip at `p` is made, the maximum original prefix sum on `[p, i]` can be obtained from the deque, and `2` times the number of flips is added to it. Since the left endpoint of this range only moves right, the deque can be maintained in linear time.

The result is a single left-to-right scan with constant amortized work per student.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate flip sets and intervals | `O(2^N N^2)` | `O(N)` | Too slow |
| Binary search number of flips | `O(N log N)` | `O(N)` | Unnecessarily slow |
| Greedy with prefix maximum and monotonic deque | `O(N)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Encode every `A` as `+1` and every `B` as `-1`, and maintain the original prefix sum `P`. If student `i` has been flipped, every effective prefix from `i` onward gains `2`.
2. Maintain `max_balance` and `max_pos`, representing the largest effective prefix balance among positions strictly before the current student and the earliest position where that maximum occurs. The earliest position is useful because it gives the widest possible bad interval and consequently the cheapest eligible `B`.
3. Maintain a pointer `next_b` to the earliest `B` that has not already been selected. The pointer only moves forward. When a violation starts after `max_pos`, any `B` before `max_pos + 1` cannot repair that violation, so advance the pointer until it reaches the first `B` at or after that boundary.
4. At student `i`, compute the current effective balance as `P + 2 * flips`, where `flips` is the number of selected students so far. If this is at least `max_balance - K`, the current endpoint creates no new violation. Update the maximum if necessary.
5. If the current balance is below `max_balance - K`, the interval beginning at `max_pos + 1` and ending at `i` is bad. Select the earliest unflipped `B` in this interval. This is the cheapest student that can repair the newly discovered violation.
6. Add the selected student's cost to the answer modulo `1,000,000,007`. The pointer used to find `B` positions also carries the corresponding power of two, so no array of all powers is required.
7. After selecting position `p`, all original prefix sums from `p` through `i` increase by `2` in the effective sequence. Remove deque entries before `p`, take the maximum original prefix sum remaining in the deque, add `2 * flips`, and compare it with the old maximum. If the new value is strictly larger, update `max_balance` and `max_pos`.
8. Continue until all `N` students have been processed. Every possible representative interval has been considered through its right endpoint, and every violation has been repaired by the cheapest possible eligible student.

### Why it works

The invariant is that after processing position `i`, every representative interval ending at or before `i` is safe, and the selected students are the cheapest choices made by the greedy process for the violations encountered so far. When a new violation appears, its left endpoint is determined by a maximum prefix balance. Any valid solution must flip a `B` inside that interval, because changing a student outside it cannot change that interval's vote difference. Among all eligible unflipped `B` voters, the leftmost one has the smallest cost. Choosing it cannot make a future solution more expensive, because it can only improve intervals beginning at or before its position, while every later `B` remains available for future violations. Thus each greedy choice is compatible with an optimal solution, and processing every endpoint establishes the required guarantee for all contiguous representative sets.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    t = int(input())
    out = []

    for case in range(1, t + 1):
        n, k = map(int, input().split())
        s = input().strip()

        # Monotonic deque of (index, original_prefix_sum).
        # Values are decreasing, and equal values keep the earliest index.
        dq = deque([(0, 0)])

        prefix = 0
        flips = 0

        # Maximum effective prefix sum among processed prefixes.
        max_balance = 0
        max_pos = 0

        # Earliest B which has not been selected yet.
        next_b = 0

        # 2^next_b modulo MOD.
        next_b_cost = 1

        answer = 0

        for i, ch in enumerate(s, 1):
            if ch == 'A':
                prefix += 1
            else:
                prefix -= 1

            # Add current original prefix sum to the monotonic deque.
            while dq and dq[-1][1] < prefix:
                dq.pop()
            dq.append((i, prefix))

            current = prefix + 2 * flips

            if current < max_balance - k:
                # The bad interval starts at max_pos + 1.
                left = max_pos + 1

                # Move to the first unflipped B inside that interval.
                while next_b < left:
                    next_b += 1
                    next_b_cost = next_b_cost * 2 % MOD

                while next_b < i and s[next_b] != 'B':
                    next_b += 1
                    next_b_cost = next_b_cost * 2 % MOD

                # A violation cannot exist without an eligible B.
                # next_b is necessarily <= i and s[next_b] == 'B'.
                p = next_b

                answer = (answer + next_b_cost) % MOD
                flips += 1

                # After flipping p, all prefixes from p onward
                # gain 2. Remove prefixes before p from the range
                # whose maximum needs to be reconsidered.
                while dq and dq[0][0] < p:
                    dq.popleft()

                shifted_max = dq[0][1] + 2 * flips

                # Keep the earliest position on ties.
                if shifted_max > max_balance:
                    max_balance = shifted_max
                    max_pos = dq[0][0]

                # The selected B is no longer available.
                next_b += 1
                next_b_cost = next_b_cost * 2 % MOD

            else:
                if current > max_balance:
                    max_balance = current
                    max_pos = i

        out.append(f"Case #{case}: {answer}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The prefix sum `prefix` always refers to the original vote string. The effect of every selected student is represented separately by `2 * flips`, because every selected student has an index no greater than the current scan position.

The `dq` contains original prefix sums in decreasing order. When a new prefix sum arrives, smaller values at the back can never become the maximum of a future range while the larger value remains in front, so they are discarded. Equal values are not discarded, which preserves the earliest index attaining the maximum. This tie choice matters because an earlier maximum gives the cheapest possible `B` when a violation occurs.

The `next_b` pointer never moves backward. It first skips positions before the current bad interval, then skips `A` positions until it reaches the first eligible `B`. After that student is selected, the pointer moves past it. Every position is passed by this pointer at most once.

The cost variable `next_b_cost` starts at `2^0 = 1`. Whenever the pointer moves from position `x` to `x + 1`, the cost is multiplied by `2` modulo `MOD`. Thus when `next_b` points to student `i`, `next_b_cost` is exactly `2^i mod MOD`.

The order of the operations around a violation is significant. The current original prefix is inserted into the deque before checking the violation because the newly selected student may be the current student, and after the flip its prefix must participate in the new maximum. The violation itself is checked against the maximum from previous effective prefixes, represented by `max_balance`, before the current prefix is accepted as an ordinary new maximum.

Python integers do not overflow, but all costs are reduced modulo `MOD` immediately. The prefix balance itself stays between `-N` and `N`, so it never needs special handling.

## Worked Examples

### Sample 1

For `N = 4`, `K = 0`, and `V = BAAB`, the original prefix balances are `0, -1, 0, 1, 0`. The first student immediately creates a bad interval, so student 1 is selected. Later, after the two `A` votes, student 4 creates another bad interval, so student 4 is selected.

| Student | Vote | Original Prefix | Flips | Effective Prefix | Maximum Before | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B | -1 | 0 | -1 | 0 | Flip 1 |
| 2 | A | 0 | 1 | 2 | 1 | Keep |
| 3 | A | 1 | 1 | 3 | 2 | Keep |
| 4 | B | 0 | 1 | 2 | 3 | Flip 4 |

The selected students are 1 and 4, so the cost is `2^1 + 2^4 = 2 + 16 = 18`. The example demonstrates why checking only long intervals is insufficient. The singleton interval containing student 4 must also be safe.

### Sample 2

For `N = 4`, `K = 1`, and `V = BAAB`, the first `B` is allowed because Betty leads by only one vote. The later `B` is also harmless under the threshold, so no students are flipped.

| Student | Vote | Original Prefix | Flips | Effective Prefix | Maximum Before | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B | -1 | 0 | -1 | 0 | Keep |
| 2 | A | 0 | 0 | 0 | 0 | Keep |
| 3 | A | 1 | 0 | 1 | 0 | Keep |
| 4 | B | 0 | 0 | 0 | 1 | Keep |

At every point, the effective prefix is at least `max_balance - 1`. The answer is consequently zero. This trace also demonstrates the inclusive boundary: a Betty advantage exactly equal to `K` is a draw, not a Betty win.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` per election | The main scan, the `B` pointer, and every deque entry each move only forward. |
| Space | `O(N)` | The input string and monotonic deque require linear storage in the worst case. |

The algorithm performs only a constant amortized number of operations per student. With `N` up to one million, this is the appropriate scale, while an `O(N log N)` or `O(N^2)` approach adds unnecessary work.

## Test Cases

```python
import sys
import io
from collections import deque

MOD = 1_000_000_007

def solve_data(data: str) -> str:
    inp = io.StringIO(data)

    def input():
        return inp.readline

    readline = inp.readline
    t = int(readline())
    out = []

    for case in range(1, t + 1):
        n, k = map(int, readline().split())
        s = readline().strip()

        dq = deque([(0, 0)])
        prefix = 0
        flips = 0
        max_balance = 0
        max_pos = 0

        next_b = 0
        next_b_cost = 1
        answer = 0

        for i, ch in enumerate(s, 1):
            if ch == 'A':
                prefix += 1
            else:
                prefix -= 1

            while dq and dq[-1][1] < prefix:
                dq.pop()
            dq.append((i, prefix))

            current = prefix + 2 * flips

            if current < max_balance - k:
                left = max_pos + 1

                while next_b < left:
                    next_b += 1
                    next_b_cost = next_b_cost * 2 % MOD

                while next_b < i and s[next_b] != 'B':
                    next_b += 1
                    next_b_cost = next_b_cost * 2 % MOD

                answer = (answer + next_b_cost) % MOD
                flips += 1

                while dq and dq[0][0] < next_b:
                    dq.popleft()

                shifted_max = dq[0][1] + 2 * flips

                if shifted_max > max_balance:
                    max_balance = shifted_max
                    max_pos = dq[0][0]

                next_b += 1
                next_b_cost = next_b_cost * 2 % MOD

            elif current > max_balance:
                max_balance = current
                max_pos = i

        out.append(f"Case #{case}: {answer}")

    return "\n".join(out)

# Provided samples
sample = """6
4 0
BAAB
4 1
BAAB
4 1
ABBA
5 2
BBBBB
15 3
ABBBABBBBBABABB
50 4
BBABAABBBBABBBBAABBBBAABBBBBABBBAABABBBBBBABABBAAB
"""

assert solve_data(sample) == """Case #1: 18
Case #2: 0
Case #3: 4
Case #4: 10
Case #5: 324
Case #6: 363067831""", "provided samples"

# Minimum size, Betty must be stopped.
assert solve_data("""1
1 0
B
""") == "Case #1: 2", "single B"

# Minimum size, Amy already wins.
assert solve_data("""1
1 0
A
""") == "Case #1: 0", "single A"

# Threshold equal to N means Betty can never exceed it.
assert solve_data("""1
3 3
BBB
""") == "Case #1: 0", "K = N"

# Boundary case from the statement where the cheapest useful B
# is not the current endpoint.
assert solve_data("""1
4 1
ABBA
""") == "Case #1: 4", "earliest B in bad interval"

# All A, maximum-size input.
n = 1_000_000
assert solve_data(f"1\n{n} 0\n{'A' * n}\n") == "Case #1: 0", "maximum-size all A"

# All B with K = 0 requires flipping every student.
assert solve_data("""1
5 0
BBBBB
""") == "Case #1: 62", "all B with K=0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0 / B` | `Case #1: 2` | Minimum size and singleton Betty interval |
| `1 / 1 0 / A` | `Case #1: 0` | Already-safe election |
| `1 / 3 3 / BBB` | `Case #1: 0` | Maximum threshold boundary |
| `1 / 4 1 / ABBA` | `Case #1: 4` | Choosing the earliest eligible `B`, not the current endpoint |
| `N = 1,000,000`, all `A` | `Case #1: 0` | Maximum input size and linear-time behavior |
| `1 / 5 0 / BBBBB` | `Case #1: 62` | Repeated violations and accumulated powers of two |

## Edge Cases

For `N = 1`, `K = 0`, and `V = B`, the initial effective prefix is `-1`, while the maximum previous prefix is `0`. The condition `-1 < 0 - 0` detects the singleton violation. The earliest eligible `B` is student 1, whose cost is `2`, giving the correct output `Case #1: 2`.

For `N = 4`, `K = 0`, and `V = BAAB`, student 1 is selected immediately. The effective prefixes become `1, 2, 3` through student 3. At student 4, the effective balance falls from the maximum `3` to `2`, which is below the allowed value `3`. The bad interval therefore begins at student 4, and the only eligible `B` is student 4. Its cost is `16`, so the total is `2 + 16 = 18`.

For `N = 4`, `K = 1`, and `V = ABBA`, after student 1 the maximum prefix balance is `1`. At student 2 the balance is `0`, which is exactly `1 - K`, so no flip is needed. At student 3 the balance becomes `-1`, violating the condition. The bad interval starts at student 2, and the earliest `B` in that interval is student 2. Flipping it costs `4`. The later positions are then safe, giving `Case #1: 4`.

For `N = 3`, `K = 3`, and `V = BBB`, the worst possible representative set contains three Betty votes, giving Betty an advantage of exactly `3`. Since Betty only wins when her advantage is strictly greater than `K`, no violation is detected and the answer remains zero.

For the maximum-size all-`A` case, every prefix balance increases by one, so the current balance is always at least the maximum previous balance. The violation branch is never entered, the `B` pointer is never used, and the answer stays zero after one linear scan. This exercises the largest possible input without introducing any special-case behavior.
