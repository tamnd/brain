---
title: "CF 1296B - Food Buying"
description: "We are given an initial amount of money, and we repeatedly perform a very specific type of purchase operation. In each operation, we choose some amount $x$ that we can afford at that moment, spend it, and immediately receive back $lfloor x/10 rfloor$."
date: "2026-06-16T04:48:11+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1296
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 617 (Div. 3)"
rating: 900
weight: 1296
solve_time_s: 133
verified: true
draft: false
---

[CF 1296B - Food Buying](https://codeforces.com/problemset/problem/1296/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial amount of money, and we repeatedly perform a very specific type of purchase operation. In each operation, we choose some amount $x$ that we can afford at that moment, spend it, and immediately receive back $\lfloor x/10 \rfloor$. That cashback can be reused in future purchases, so money can circulate through repeated partial refunds.

The task is not to simulate purchases, but to determine the maximum total amount of money that can be spent across all operations if we choose the sequence of purchases optimally.

The key subtlety is that the cashback is proportional to the chosen purchase size. Small purchases lose almost everything, while large purchases recycle part of the spent value. The problem is essentially asking how much "extra spending" can be extracted through repeated reuse of the refunded tenth.

The input size allows up to $10^4$ test cases with values up to $10^9$. This rules out any simulation that depends on iterating through each unit of money or performing a large number of step-by-step greedy choices per test case. An $O(s)$ or even $O(s/10)$ simulation is far too slow in the worst case.

A naive greedy approach can also fail in less obvious ways. For example, always taking the largest possible $x = s$ might look reasonable, but it does not account for the fact that the cashback can be reused repeatedly, and the optimal strategy is about forcing repeated “10-block recycling.”

The main edge case pattern is when the remaining amount is just below a multiple of 10. For instance, with $s = 19$, choosing $x = 19$ first gives cashback 1, leaving 1 behind, and loses structure. The optimal strategy instead repeatedly uses 10-sized purchases to maximize reuse of cashback cycles.

## Approaches

A brute-force strategy would simulate all possible choices of $x$ at each step, branching over all $1 \le x \le s$. After each operation, the state changes to $s - x + \lfloor x/10 \rfloor$, and we would try all possibilities recursively to maximize total spent. This is correct in principle because it explores every valid sequence of operations.

However, this branching explodes immediately. Even if we prune identical states, the number of reachable states grows rapidly because each spend creates a new amount that can again branch into many possibilities. With $s$ up to $10^9$, even a linear simulation is impossible.

The key insight is to stop thinking in terms of arbitrary $x$, and instead classify money into two components: full tens and leftovers. Spending 10 units is special because it returns exactly 1, meaning net loss is 9 but it preserves the ability to continue the same operation. This creates a stable cycle: every 10 spent generates 1 reusable unit, which in turn can eventually form another 10.

So the problem reduces to repeatedly converting groups of 10 into extra usable units, while accumulating all possible spending from cascading remainders.

This leads to a digit-based process: each time we extract tens from the current amount, those tens generate additional money, which can again produce more tens.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential | O(s) | Too slow |
| Optimal | O(log s) | O(1) | Accepted |

## Algorithm Walkthrough

We process each number independently, repeatedly extracting contributions from its decimal structure.

1. Initialize a variable `ans` to 0. This will accumulate total spent money, including both original spending and recycled cashback contributions.
2. While the current amount `s` is at least 10, take out its last digit structure by dividing it into tens and remainder. Let `t = s // 10`. These represent how many full 10-unit blocks exist.
3. Add `t * 10` to `ans`. This corresponds to spending all full tens directly.
4. Update `s` to be `t + s % 10`. This step is crucial: each 10 spent produces 1 cashback unit, so the number of usable units increases by `t`, and we also keep the leftover digits.
5. Repeat until `s < 10`.
6. Finally, add the remaining `s` to `ans`, since any leftover units can be fully spent once without further recycling.

The reason this works is that every block of 10 spent effectively transforms into 1 new unit of currency, which can itself contribute to forming future blocks of 10. The process therefore compresses repeated spending into a digit-carrying accumulation process.

### Why it works

At any moment, the state of the system can be represented as an integer amount of money. Spending 10 units is the only operation that produces a non-zero return, and it produces exactly 1 unit. This means the system evolves exactly like carrying in base-10 arithmetic, where every group of 10 spent creates a new unit in the next iteration.

The algorithm preserves the invariant that `s` represents all currently unspent units, including cashback that has not yet been converted into full 10-unit spending opportunities. Each iteration resolves all possible immediate 10-unit cycles before moving upward, so no potential spending opportunity is ever skipped or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = int(input())
        ans = 0
        
        while s >= 10:
            t10 = s // 10
            ans += t10 * 10
            s = t10 + (s % 10)
        
        ans += s
        print(ans)

if __name__ == "__main__":
    solve()
```

The code directly follows the iterative decomposition of the money into tens and leftovers. The variable `t10` represents how many full 10-cost purchases can be made at the current stage. Those contribute `t10 * 10` to the answer.

The update `s = t10 + (s % 10)` encodes cashback reinjection: every group of 10 spent produces one new unit, and the remainder stays unchanged.

The loop continues until no further tens can be formed, at which point all remaining units are directly added to the answer.

A subtle point is that we never subtract explicitly the cashback from spending; instead, it is implicitly added back into `s`, which keeps the state compact and avoids tracking past transactions.

## Worked Examples

We trace two inputs: `19` and `9876`.

### Example 1: s = 19

| s | t10 = s//10 | ans add | new s |
| --- | --- | --- | --- |
| 19 | 1 | 10 | 1 + 9 = 10 |
| 10 | 1 | 10 | 1 + 0 = 1 |

Final step adds remaining 1, total = 21.

This shows how the cashback from the first 10 creates another full purchase opportunity, which is essential for the optimal answer.

### Example 2: s = 9876

| s | t10 | ans add | new s |
| --- | --- | --- | --- |
| 9876 | 987 | 9870 | 987 + 6 = 993 |
| 993 | 99 | 990 | 99 + 3 = 102 |
| 102 | 10 | 100 | 10 + 2 = 12 |
| 12 | 1 | 10 | 1 + 2 = 3 |

Final answer adds 3, total accumulates to 10973.

This trace shows repeated compression of tens into higher-order units, demonstrating how cashback propagates upward through multiple iterations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log_{10} s)$ per test | Each iteration reduces magnitude by at least a factor of 10 in effective scale |
| Space | $O(1)$ | Only a few integer variables are used |

The logarithmic behavior is easily fast enough for $10^4$ test cases with $s \le 10^9$, since each test runs in under 10 iterations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = int(input())
        ans = 0
        while s >= 10:
            t10 = s // 10
            ans += t10 * 10
            s = t10 + (s % 10)
        ans += s
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("6\n1\n10\n19\n9876\n12345\n1000000000\n") == \
"1\n11\n21\n10973\n13716\n1111111111"

# custom cases
assert run("1\n9\n") == "9", "single digit no operations"
assert run("1\n10\n") == "11", "single exact block"
assert run("1\n20\n") == "22", "two tens cascade"
assert run("1\n99\n") == "109", "repeated cascading carry behavior"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 | 9 | no cashback cycle |
| 10 | 11 | single conversion loop |
| 20 | 22 | multi-cycle reinforcement |
| 99 | 109 | cascading digit carry behavior |

## Edge Cases

For small inputs like $s = 1$ through $s = 9$, the loop never runs. The algorithm directly returns the same value because no 10-unit cycle exists. For example, with $s = 7$, `s >= 10` is false, so `ans = 0` and final output is 7.

For exact multiples of 10, such as $s = 10$, the first iteration converts it into a cashback unit: `t10 = 1`, so `ans = 10`, and `s` becomes 1. The final result becomes 11, which matches the fact that the cashback allows one extra unit of spending.

For larger cascading cases like $s = 19$, the first 10 creates a new unit that immediately recombines into another 10, showing that the process correctly captures multi-level reuse of cashback without explicit recursion.
