---
problem: 1256D
contest_id: 1256
problem_index: D
name: "Binary String Minimizing"
contest_name: "Codeforces Round 598 (Div. 3)"
rating: 1500
tags: ["greedy"]
answer: passed_samples
verified: true
solve_time_s: 430
date: 2026-06-13
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d779c-d51c-83ec-92b9-0b69bdc465a4
---

# CF 1256D - Binary String Minimizing

**Rating:** 1500  
**Tags:** greedy  
**Model:** gpt-5-5  
**Solve time:** 7m 10s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d779c-d51c-83ec-92b9-0b69bdc465a4  

---

## Solution

## Problem Understanding

We are given a binary string and a budget of adjacent swaps. Each swap exchanges two neighboring characters, and every such exchange consumes one unit of the budget. Our goal is to rearrange the string into the smallest possible binary string in lexicographic order while respecting the limit on how many swaps we are allowed to perform.

Lexicographic order here is the usual string comparison: we want as many leading `0`s as possible, and among strings with the same prefix, we prefer the one that pushes `1`s as far to the right as possible.

A useful way to reinterpret the operation is to think of moving each `0` left across `1`s. Every time a `0` passes a `1`, it costs exactly one swap. This immediately suggests that the problem is about greedily advancing zeros leftward as far as the budget allows.

The constraints are large in aggregate: total length over all test cases is up to one million, and the number of swaps allowed per test can be as large as $n^2$. This rules out any approach that simulates swaps or repeatedly scans the string in a quadratic manner. Even an $O(nk)$ simulation per test case is impossible because $k$ can be huge. We need a linear or near-linear strategy per test.

A subtle pitfall appears when multiple zeros compete for early positions. A naive greedy strategy that always moves the current zero as far left as possible can fail if it does not account for the remaining budget globally. Another common mistake is to simulate swaps step-by-step, which explodes to quadratic behavior even for moderate inputs.

## Approaches

A brute-force approach literally performs swaps greedily. One could repeatedly scan the string and whenever a `10` pattern is found, swap it if we still have budget left. This produces correct lexicographic improvement because each swap locally improves order. However, in the worst case, such as a string like `111...1000...0`, each zero must cross many ones, and the number of swaps performed can be on the order of $n^2$. Each swap also requires scanning or updating positions, leading to quadratic or worse complexity per test case, which is infeasible.

The key observation is that we never need to simulate swaps explicitly. Instead, we process zeros from left to right and decide how far each zero can move left based on how many ones are currently in front of it and how much budget remains. Each zero contributes to consuming budget equal to the number of `1`s it jumps over, but it cannot interfere with earlier decisions beyond reducing remaining budget.

We can maintain a structure where we track how many zeros have already been placed and how many ones remain available to cross. A cleaner viewpoint is to iterate through the string while maintaining a queue-like structure of pending zeros and a running count of available swaps, greedily placing `0` as far left as possible whenever budget allows.

Another equivalent and more implementation-friendly idea is to simulate constructing the answer from left to right. At each position, we decide whether we can bring a `0` from some future position into the current slot. We greedily pick the earliest reachable `0` that can be moved into the current position using remaining swaps.

This leads to a process where we scan the string, maintain how many zeros are still unused, and for each position decide whether a zero can be “pulled” into it under the remaining cost constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Swapping | $O(n^2)$ | $O(1)$ | Too slow |
| Greedy Budgeted Placement | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Precompute, while scanning the string, the positions of all `0`s. We will consider moving them left in order of appearance.
2. Maintain a pointer `i` over the final answer being constructed and another pointer over zeros in the original string. Also maintain a variable `k` representing remaining swap budget.
3. For each position `i` from left to right, decide which character should occupy it. We want `0` if possible, because it minimizes lexicographic order.
4. To decide whether a `0` can be placed at position `i`, compute the cost of moving the next unused `0` to position `i`. This cost is the number of non-moved characters between its original position and `i`, which effectively equals how many swaps it must perform to cross intervening `1`s.
5. If this cost is less than or equal to remaining `k`, we place `0` at position `i`, consume that cost, and advance the zero pointer. Otherwise, we place `1` and continue.
6. Continue until all positions are filled.

The key idea behind step 4 is that each `0` moves independently in a left-to-right construction, and its movement cost depends only on how many positions it skips over. By always selecting the next available zero when it is affordable, we ensure that earlier positions get zeros whenever possible, which is exactly what lexicographic minimization requires.

### Why it works

The algorithm maintains a greedy invariant: at every position, if it is possible to place a `0` there using some valid sequence of swaps within the remaining budget, the algorithm will do so. Any optimal solution must also place a `0` there in that case, because replacing it with `1` would only push a `0` further right without saving budget that could improve lexicographic order earlier. Since swaps only affect relative ordering and each `0` has a fixed cost to reach earlier positions, greedily consuming the cheapest available `0` preserves optimality locally and globally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        n, k = map(int, input().split())
        s = input().strip()

        zeros = []
        ones_before = 0

        for i, ch in enumerate(s):
            if ch == '0':
                zeros.append(i)

        z = 0
        used = [False] * n
        res = []

        for i in range(n):
            # cost to bring next zero here
            if z < len(zeros):
                pos = zeros[z]
                cost = pos - i
                if cost <= k:
                    res.append('0')
                    k -= cost
                    z += 1
                    continue
            res.append('1')

        print("".join(res))

if __name__ == "__main__":
    solve()
```

The implementation precomputes the positions of all zeros and then greedily decides whether the next unused zero can be moved to the current position. The expression `pos - i` captures how far the zero must be shifted left in terms of adjacent swaps. If the budget allows, we place it; otherwise we place `1`.

A subtle point is that we never explicitly simulate swaps. The cost calculation implicitly accounts for all required adjacent swaps. This is what keeps the solution linear.

## Worked Examples

We trace the algorithm on two inputs.

### Example 1

Input:

```
n=8, k=5
11011010
```

Zeros are at positions: `[2, 5, 7]`.

| i | next zero pos | cost | k before | action | k after | output |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 5 | take 0 | 3 | 0 |
| 1 | 5 | 4 | 3 | cannot take | 3 | 01 |
| 2 | 5 | 3 | 3 | take 0 | 0 | 010 |
| 3 | 7 | 4 | 0 | cannot take | 0 | 0101 |
| 4 | 7 | 3 | 0 | cannot take | 0 | 01011 |
| 5 | 7 | 2 | 0 | cannot take | 0 | 010111 |
| 6 | 7 | 1 | 0 | cannot take | 0 | 0101111 |
| 7 | 7 | 0 | 0 | take 0 | 0 | 01011110 |

This confirms that zeros are pulled left whenever affordable, and once the budget is exhausted, remaining structure is fixed.

### Example 2

Input:

```
n=7, k=11
1111100
```

Zeros are at positions `[5, 6]`.

| i | next zero pos | cost | k before | action | k after | output |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 5 | 11 | take 0 | 6 | 0 |
| 1 | 6 | 5 | 6 | take 0 | 1 | 00 |
| 2 | (none) | - | 1 | 1 | 1 | 001 |
| 3 | (none) | - | 1 | 1 | 1 | 0011 |
| 4 | (none) | - | 1 | 1 | 1 | 00111 |
| 5 | (none) | - | 1 | 1 | 1 | 001111 |
| 6 | (none) | - | 1 | 1 | 1 | 0011111 |

Here the budget is sufficient to fully sort the string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each character is processed once and each zero is advanced once |
| Space | $O(n)$ | Storage for zero positions and output string |

The total length across all test cases is at most one million, so a linear-time per test case approach is sufficient and runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""3
8 5
11011010
7 9
1111100
7 11
1111100
""") == """01011110
0101111
0011111"""

# minimum size
assert run("""1
1 100
0
""") == "0"

# no budget effect
assert run("""1
5 0
01010
""") == "01010"

# already sorted
assert run("""1
6 3
000111
""") == "000111"

# maximum swaps sufficient
assert run("""1
5 10
11100
""") == "00111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `0` | single character handling |
| `k=0` case | unchanged | no-move constraint |
| already sorted | same string | stability |
| high k | fully sorted | full transformation |

## Edge Cases

One edge case occurs when the string starts with many `1`s and has a small number of `0`s far to the right. The algorithm still behaves correctly because the first few positions can only be filled with `1`s until enough budget accumulates to pull a `0` forward.

Another edge case is when `k` is extremely large. In this case, every zero becomes affordable at its earliest possible position, and the algorithm degenerates into producing a fully sorted string with all `0`s at the front.

A third case is when zeros are dense near the end. Even if multiple zeros exist, each is considered exactly once, and their costs decrease as `i` increases, ensuring no zero is skipped incorrectly or double-counted.