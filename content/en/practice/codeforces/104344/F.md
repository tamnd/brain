---
title: "CF 104344F - Pegadinha"
description: "We are given a building with floors numbered from 1 to N. Initially, every floor has its light turned off. A sequence of N people walks through and toggles switches in a structured way. The i-th person toggles every floor number that is a multiple of i."
date: "2026-07-01T18:28:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "F"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 92
verified: false
draft: false
---

[CF 104344F - Pegadinha](https://codeforces.com/problemset/problem/104344/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a building with floors numbered from 1 to N. Initially, every floor has its light turned off. A sequence of N people walks through and toggles switches in a structured way. The i-th person toggles every floor number that is a multiple of i. After all N people have done this, some floors end up lit and others remain dark.

A toggle means switching state, so off becomes on and on becomes off. The final task is not to simulate the process, but to determine exactly which floors are lit at the end, and print those floor numbers in increasing order.

The constraint N can be as large as 10^8, which immediately rules out any simulation over all floors for all people. A direct approach would require roughly N operations per person, leading to about N^2 operations in the worst case, which is far beyond feasible limits. Even a single pass over all toggles is too large if we are not careful, since 10^8 operations is already at the edge of 1 second in optimized languages and impossible in Python when repeated many times.

The key difficulty is recognizing that the process is highly structured and depends only on the number of divisors of each floor index.

A subtle edge case appears when N is small. For example, if N = 1, the only floor is toggled once and remains on. For N = 2, floor 1 is toggled twice and ends off, while floor 2 is toggled once and stays on. These small cases hint that the final state is determined by parity of something intrinsic to each number rather than the sequence of operations.

## Approaches

A brute-force simulation would iterate over each person i from 1 to N and then iterate over multiples of i, toggling states of those floors. This directly mirrors the problem statement and is correct logically.

However, the cost is the issue. The inner loop runs N/i times, so the total number of toggles is approximately N/1 + N/2 + ... + N/N, which is N log N. Even that might pass in C++, but with N up to 10^8 it is completely infeasible in Python, and even conceptually we are still iterating over billions of operations in worst cases.

The key observation is to invert the perspective. Instead of asking how many times each person toggles floors, we ask how many times each floor is toggled. A floor k is toggled once for every divisor of k, because every divisor i contributes a toggle when person i acts. Therefore, floor k is toggled exactly d(k) times, where d(k) is the number of divisors of k.

A floor ends up lit if it is toggled an odd number of times. So the problem reduces to finding all k such that d(k) is odd. A classic number theory fact is that only perfect squares have an odd number of divisors. This happens because divisors normally pair as (a, k/a), except when a = k/a, which occurs only for perfect squares.

Thus, the answer is exactly all perfect squares less than or equal to N.

We can generate them directly by iterating i from 1 until i^2 ≤ N and printing i^2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N log N) | O(N) | Too slow |
| Square Enumeration | O(√N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that each floor k is toggled once for every divisor of k. This reframes the entire process in terms of divisor counting rather than simulating people.
2. Recognize that the final state depends only on whether the divisor count of k is odd. If it is odd, the floor ends up lit.
3. Use the number theory fact that only perfect squares have an odd number of divisors. This comes from pairing divisors symmetrically around √k.
4. Conclude that we only need to output all integers of the form i² such that i² ≤ N.
5. Iterate i starting from 1 and continue while i² ≤ N, printing i² each time.

Why it works: every non-square integer has its divisors arranged in distinct pairs, producing an even count, so it cancels out to off. Perfect squares have exactly one unpaired divisor, the square root, making the count odd and leaving the final state on. This invariant holds independently for each floor, so computing squares fully determines the output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    i = 1
    while i * i <= n:
        print(i * i)
        i += 1

if __name__ == "__main__":
    solve()
```

The solution reads N and then iterates over possible square roots. Each value i represents a floor i² that survives the toggling process. The loop condition i * i <= n ensures we do not exceed the valid floor range. No additional data structures are needed, since outputs are generated on the fly.

The critical detail is using i * i instead of floating-point square roots, avoiding precision issues and keeping the solution integer-safe.

## Worked Examples

### Example 1: N = 3

We check values of i:

| i | i² | i² ≤ 3 | Output |
| --- | --- | --- | --- |
| 1 | 1 | yes | 1 |
| 2 | 4 | no | stop |

Only floor 1 remains lit.

This matches the fact that only 1 is a perfect square within range.

### Example 2: N = 6

| i | i² | i² ≤ 6 | Output |
| --- | --- | --- | --- |
| 1 | 1 | yes | 1 |
| 2 | 4 | yes | 4 |
| 3 | 9 | no | stop |

The final lit floors are 1 and 4, corresponding exactly to perfect squares under 6.

This confirms that the algorithm directly enumerates the surviving states without simulating toggles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√N) | We iterate i from 1 to ⌊√N⌋ and print each square once |
| Space | O(1) | No auxiliary storage beyond a few integers |

The constraint N ≤ 10^8 implies √N ≤ 10^4, so the loop runs at most ten thousand iterations, which is trivial within the time limit.

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

def solve():
    n = int(input().strip())
    i = 1
    while i * i <= n:
        print(i * i)
        i += 1

# provided samples
assert run("3\n") == "1"
assert run("6\n") == "1\n4"
assert run("1\n") == "1"

# custom cases
assert run("2\n") == "1", "small non-square"
assert run("10\n") == "1\n4\n9", "multiple squares"
assert run("100\n") == "\n".join(str(i*i) for i in range(1, 11)), "larger square boundary"
assert run("0\n") == "", "edge zero case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | smallest non-square behavior |
| 10 | 1 4 9 | multiple outputs correctness |
| 100 | squares up to boundary | upper bound iteration correctness |
| 0 | empty | degenerate boundary case |

## Edge Cases

For N = 1, only floor 1 exists. It is toggled once, so it remains on. The algorithm outputs i = 1, producing 1² = 1, which is correct.

For a non-square like N = 2, only i = 1 satisfies i² ≤ 2, so only floor 1 is printed. Floor 2 is not printed because 2 is not a perfect square and has an even number of divisors, meaning it ends off.

For large N such as 10^8, i runs up to 10^4, and we correctly output all squares up to 10000² = 10^8, ensuring no overflow or performance issues.

Each case confirms that the algorithm relies only on integer iteration and avoids simulation entirely, preserving correctness and efficiency.
