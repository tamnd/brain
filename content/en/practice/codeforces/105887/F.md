---
title: "CF 105887F - \u8d62\u9ebb\u4e86"
description: "Each test describes a simple comparison game between three values: Alice’s strength a, Bob’s strength b, and Candy’s strength c. The output is a string chosen by applying a priority rule over these comparisons. The decision process is sequential."
date: "2026-06-21T15:06:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105887
codeforces_index: "F"
codeforces_contest_name: "\u7b2c\u5341\u4e09\u5c4a\u91cd\u5e86\u5e02\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b"
rating: 0
weight: 105887
solve_time_s: 50
verified: true
draft: false
---

[CF 105887F - \u8d62\u9ebb\u4e86](https://codeforces.com/problemset/problem/105887/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test describes a simple comparison game between three values: Alice’s strength `a`, Bob’s strength `b`, and Candy’s strength `c`. The output is a string chosen by applying a priority rule over these comparisons.

The decision process is sequential. First, Alice tries to determine whether she directly defeats Bob, which corresponds to checking whether `a > b`. If this holds, the answer is fixed as `"Win"` and no further reasoning is needed.

If Alice does not directly beat Bob, the game switches to an indirect interpretation: Bob is considered weaker if Candy is stronger than Bob, meaning `c > b`. In that case the output becomes `"WIN"`.

If neither condition holds, meaning Alice does not beat Bob and Candy does not beat Bob either, the result is `"nowin"`.

The input consists of multiple independent test cases. Each test case contains three integers, and each must be evaluated under the same logic. The constraints are small enough that each test can be handled in constant time. Even at the maximum of 100 test cases, any O(T) or O(T log T) solution is trivially sufficient, and there is no need for preprocessing or data structures.

The main subtlety is the strict ordering of conditions. A common mistake is to check `c > b` before `a > b`, which would incorrectly classify cases where Alice already wins directly. Another edge case is when values are equal, especially `a == b` or `c == b`, which must both be treated as failures of their respective strict inequalities.

For example, when `a = 6, b = 6, c = 100`, Alice does not beat Bob, but Candy does, so the correct output is `"WIN"`. If `a = 10, b = 5, c = 0`, the correct output is `"Win"` even though Candy is irrelevant. If `a = 5, b = 10, c = 7`, neither condition holds, so the output is `"nowin"`.

## Approaches

A brute-force interpretation would attempt to model the narrative literally: simulate comparisons, possibly even reasoning about transitive “wins” between characters. One might try to construct a relationship graph where a node is considered winning if it beats another or is indirectly stronger through Candy. Such a model is unnecessary because the rules collapse into two direct comparisons only. Even if implemented, this simulation would still evaluate a constant number of edges per test, but it introduces complexity without benefit.

The key simplification is recognizing that the entire game is defined by a fixed priority decision tree. The first condition `a > b` fully determines the outcome when true, which means any further reasoning is irrelevant in that branch. Only when it fails do we check the second condition `c > b`. If both fail, we default to the final state.

This reduces the problem from any form of relational reasoning to a strict ordered conditional check. The structure is essentially a two-level decision function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive relational simulation | O(T) | O(1) | Accepted but unnecessary |
| Direct conditional evaluation | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the number of test cases `T`. Each test case is independent, so no state is carried across iterations.
2. For each test case, read the three integers `a`, `b`, and `c`. These represent fixed strengths, and no transformations are applied to them.
3. Check whether `a > b`. If this condition holds, immediately output `"Win"`. This step comes first because the problem defines it as the highest-priority rule.
4. If `a > b` is false, check whether `c > b`. If this condition holds, output `"WIN"`. This represents the secondary interpretation where Candy determines Bob’s loss.
5. If neither condition is satisfied, output `"nowin"`. This corresponds to the remaining region where Bob is not beaten by either Alice or Candy.

### Why it works

The logic partitions the entire space of `(a, b, c)` into three disjoint regions defined by strict inequalities. The first condition fully captures all cases where Alice dominates Bob, and it is checked first so that no alternative rule overrides it. The second condition only activates when Alice fails, and it relies solely on Candy’s comparison with Bob. Since both checks are mutually exclusive in execution order and collectively exhaustive when combined with the final fallback, every input maps to exactly one output without ambiguity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        if a > b:
            print("Win")
        elif c > b:
            print("WIN")
        else:
            print("nowin")

if __name__ == "__main__":
    solve()
```

The solution reads all test cases once and processes each independently. The branching structure mirrors the decision tree directly, ensuring the priority of conditions is preserved exactly as specified.

The critical implementation detail is the use of `elif`. This guarantees that once `a > b` is satisfied, the program does not mistakenly evaluate the second condition. Without this structure, a separate `if` for `c > b` could incorrectly overwrite the correct output.

## Worked Examples

We trace two representative cases.

### Example 1

Input:

```
a = 6, b = 500, c = 1000
```

| Step | Condition checked | Result |
| --- | --- | --- |
| 1 | a > b | False |
| 2 | c > b | True |
| 3 | Output | WIN |

This demonstrates the second rule activating only after the first fails.

### Example 2

Input:

```
a = 6, b = 5, c = 1000
```

| Step | Condition checked | Result |
| --- | --- | --- |
| 1 | a > b | True |
| 2 | (skipped) | - |
| 3 | Output | Win |

This shows that Candy’s value is irrelevant once Alice directly beats Bob.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires a constant number of comparisons |
| Space | O(1) | No additional data structures are used |

The constraints allow up to 100 test cases, so a linear scan with constant work per case is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample (interpreted with T = 5)
assert run("""5
6 5 1000
6 500 1000
6 5000 1000
1234 4009 4039
6 6 6
""") == """Win
WIN
nowin
WIN
nowin"""

# all equal
assert run("""1
10 10 10
""") == "nowin"

# Alice wins directly
assert run("""1
7 3 100
""") == "Win"

# Candy determines win
assert run("""1
3 10 20
""") == "WIN"

# boundary equality case
assert run("""1
5 5 6
""") == "WIN"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | nowin | strict inequalities |
| a > b dominates | Win | priority of first rule |
| c > b only | WIN | second rule activation |
| equal b edge | WIN or nowin depending | boundary handling |

## Edge Cases

One edge case occurs when all values are equal. For input `a = b = c = 10`, the algorithm checks `a > b` which fails, then checks `c > b` which also fails, producing `"nowin"`. This matches the rule structure because neither Alice nor Candy strictly exceeds Bob.

Another case is when only equality separates outcomes, such as `a = 5, b = 5, c = 6`. Here the first condition fails due to equality, but the second succeeds because Candy strictly exceeds Bob, producing `"WIN"`. This confirms that equality does not trigger any win condition.

A final case is when Alice is strictly stronger regardless of Candy, such as `a = 100, b = 1, c = 0`. The algorithm stops immediately at the first check and returns `"Win"`, demonstrating that Candy is never evaluated in this branch.
