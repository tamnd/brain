---
title: "CF 102263A - Is It Easy ?"
description: "Each participating team needs exactly one printed copy of the problem statement. If printing one copy costs k coins and there are n teams, the total cost is the cost of one copy multiplied by the number of teams. The input contains two integers, n and k."
date: "2026-08-17T19:52:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102263
codeforces_index: "A"
codeforces_contest_name: "ArabellaCPC 2019"
rating: 0
weight: 102263
solve_time_s: 49
verified: true
draft: false
---

[CF 102263A - Is It Easy ?](https://codeforces.com/problemset/problem/102263/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Each participating team needs exactly one printed copy of the problem statement. If printing one copy costs `k` coins and there are `n` teams, the total cost is the cost of one copy multiplied by the number of teams.

The input contains two integers, `n` and `k`. The value `n` tells us how many teams need copies, while `k` is the price of printing one copy. The required output is the total number of coins needed to print one copy for every team, which is simply `n * k`.

Both values are between 1 and 1000. These bounds are extremely small, so even a linear algorithm would finish immediately. There is no need for arrays, graphs, dynamic programming, or any iterative process. Since the total is obtained directly from two input values, constant time is the natural solution.

The smallest possible input is `1 1`, which produces `1`. A careless implementation that assumes there are multiple teams could mishandle this case, but there is nothing special about a single team mathematically.

For example, with input `1 7`, only one copy is needed, so the output is `7`. An implementation that accidentally adds the price once more because of an incorrect loop boundary could produce `14`.

The largest possible values are also straightforward. With input `1000 1000`, the answer is `1000000`. The result is larger than either input, so an implementation using an unnecessarily narrow integer type in a language with fixed-width integer types could overflow in a different version of this problem. Python integers do not have this issue.

## Approaches

A direct brute-force approach would simulate the printing process. Start with a total of zero and repeat `n` times, adding `k` to the total on every iteration. This is correct because every iteration represents one team receiving one printed copy, so after all iterations the accumulated value is exactly the cost of all copies.

With the actual constraints, this brute-force method performs at most 1000 additions. It is not too slow at all, and it would be accepted easily. There is no honest input size here at which this particular brute-force method becomes a practical problem.

The better observation is that repeatedly adding the same value `k`, exactly `n` times, is the definition of multiplication. Instead of performing `k + k + ... + k` through a loop, we can calculate `n * k` directly. This reduces the work from proportional to `n` to a fixed number of arithmetic operations.

The brute-force works because each team contributes exactly `k` coins, but it performs that identical calculation separately for every team. The structure of the problem tells us that every contribution is equal, so the whole sum can be collapsed into one multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted for these constraints |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers `n` and `k`. The first represents the number of teams, and the second represents the printing cost of one copy.
2. Compute `n * k`. Each of the `n` teams requires one copy, and every copy costs exactly `k`, so multiplication gives the complete cost without explicitly simulating individual teams.
3. Print the resulting value. No additional processing is required because the multiplication already represents the requested total.

### Why it works

For every team, the judges spend exactly `k` coins. With `n` teams, the total can be written as the repeated sum `k + k + ... + k`, containing `n` terms. By the definition of multiplication, this sum equals `n * k`. The algorithm computes exactly this value, so the printed result is the required total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
print(n * k)
```

The first line imports `sys`, allowing the solution to use `sys.stdin.readline` as requested for competitive-programming input.

The second line reads the only input line and converts its two whitespace-separated values to integers. There is no need to handle multiple test cases because the problem contains exactly one pair of values.

The final line performs the complete calculation and prints it. There are no loop boundaries or indexing operations, so there is no off-by-one issue. Python's integer type also handles the entire allowed result safely.

## Worked Examples

### Sample 1

For input `5 3`, there are five teams and each printed copy costs three coins.

| n | k | Total |
| --- | --- | --- |
| 5 | 3 | 15 |

The multiplication `5 * 3` gives `15`, so the judges need 15 coins.

### Sample 2

For input `4 1`, there are four teams and each copy costs one coin.

| n | k | Total |
| --- | --- | --- |
| 4 | 1 | 4 |

Here the multiplication is `4 * 1`, giving `4`. This also demonstrates the boundary behavior when the cost of one copy is the minimum possible value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The solution performs one multiplication and one output operation. |
| Space | O(1) | Only the two input integers and the result are stored. |

The constraints allow `n` and `k` to be at most 1000, so even the simulated O(n) approach would be easily fast enough. The optimal O(1) solution is simpler and removes the unnecessary repetition entirely. Its memory usage is constant as well.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())
    print(n * k)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# provided samples
assert run("5 3\n") == "15\n", "sample 1"
assert run("4 1\n") == "4\n", "sample 2"

# minimum-size input
assert run("1 1\n") == "1\n", "minimum values"

# maximum-size input
assert run("1000 1000\n") == "1000000\n", "maximum values"

# one team with a larger printing cost
assert run("1 1000\n") == "1000\n", "single team"

# minimum printing cost with the maximum number of teams
assert run("1000 1\n") == "1000\n", "unit cost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum allowed values |
| `1000 1000` | `1000000` | Maximum values and multiplication |
| `1 1000` | `1000` | Single-team boundary case |
| `1000 1` | `1000` | Minimum cost with many teams |

## Edge Cases

The input `1 1` is the smallest valid case. The algorithm reads `n = 1` and `k = 1`, computes `1 * 1`, and prints `1`. Nothing needs to be special-cased, which is preferable to introducing a condition that could create a boundary error.

The input `1 7` represents exactly one team paying for exactly one copy at seven coins. The calculation is `1 * 7 = 7`, so the output is `7`. A loop-based implementation with an incorrect range such as `range(1, n)` would execute zero times and incorrectly produce zero.

The input `1000 1000` exercises the largest values permitted by the problem. The calculation is `1000 * 1000 = 1000000`. The algorithm does not depend on the magnitude of `n` for its number of operations, and Python can represent the resulting integer directly.

The input `1000 1` tests the other boundary where every copy costs the minimum amount. The total is `1000 * 1 = 1000`. This confirms that the number of teams, rather than the cost of an individual copy, determines the number of contributions to the total.
