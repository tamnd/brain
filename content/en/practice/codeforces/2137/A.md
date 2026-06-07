---
title: "CF 2137A - Collatz Conjecture"
description: "We are given the result of running the Collatz operation exactly k times and the final value x. The task is not to find the original value uniquely, because many different starting values may lead to the same result."
date: "2026-06-08T02:30:25+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 2137
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1047 (Div. 3)"
rating: 800
weight: 2137
solve_time_s: 119
verified: false
draft: false
---

[CF 2137A - Collatz Conjecture](https://codeforces.com/problemset/problem/2137/A)

**Rating:** 800  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the result of running the Collatz operation exactly `k` times and the final value `x`. The task is not to find the original value uniquely, because many different starting values may lead to the same result. We only need to construct any starting integer that produces the given final value after exactly `k` operations.

The operation is simple. If the current number is even, the next number becomes `x / 2`. If the current number is odd, the next number becomes `3x + 1`.

The constraints are extremely small. Both `k` and `x` are at most `20`, and there are at most `400` test cases. Even exponential constructions would fit easily. This suggests that the intended solution is not about optimization but about understanding how to reverse the process.

The main difficulty is that the Collatz operation is not always invertible. For example, if we know the current value is `4`, the previous value could have been `8` because `8 → 4` through the even rule, or it could have been `1` because `1 → 4` through the odd rule.

A careless reverse construction may try to use the odd predecessor whenever possible. Consider:

```
k = 1, x = 5
```

The equation `(5 - 1) / 3` is not an integer, so there is no odd predecessor. The correct answer is `10`, since `10 → 5`.

Another trap is forgetting that we only need one valid answer. For

```
k = 1, x = 4
```

both `1` and `8` are valid predecessors. Searching for all possibilities is unnecessary.

A third subtle case occurs when repeatedly reversing many steps. For

```
k = 5, x = 4
```

one valid reconstruction is

```
4 ← 8 ← 16 ← 32 ← 64 ← 21
```

which gives the answer `21`. A reverse strategy must guarantee that every backward step corresponds to a valid forward Collatz move.

## Approaches

The most direct idea is brute force. We could try every possible starting number and simulate `k` Collatz operations until we find one whose final value equals the given `x`.

This works because the constraints are tiny, but there is no obvious upper bound on how large the correct starting value might be. Even for small `k`, many candidates would need to be tested. The approach has no clean guarantee.

The key observation is that we can reverse the process.

Suppose the current value is `y`.

If the previous value was even, then the forward move divided it by two:

```
previous = 2y
```

This predecessor always exists.

If the previous value was odd, then:

```
3 · previous + 1 = y
```

which gives

```
previous = (y - 1) / 3
```

but this is only valid when `(y - 1)` is divisible by `3` and the result is odd.

The crucial fact is that we do not need every predecessor. We only need one valid predecessor at each step. Since doubling always produces a valid predecessor, we can repeatedly apply:

```
y ← 2y
```

exactly `k` times.

After reversing `k` steps this way, the obtained number is:

```
x · 2^k
```

Running the Collatz process forward from this number performs `k` consecutive divisions by two and returns exactly to `x`.

This gives an immediate constructive solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded search | O(1) | Impractical |
| Optimal | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `k` and `x`.
2. Treat the given value `x` as the state after all operations have already been performed.
3. Reverse one Collatz step by choosing the guaranteed predecessor `2x`.

This is always valid because every even number maps to half its value in the forward process.
4. Repeat the previous step exactly `k` times.

After one reverse step the value becomes `2x`, after two steps it becomes `4x`, and after `k` steps it becomes `x · 2^k`.
5. Output the resulting number.

### Why it works

Every reverse step constructs a number whose forward Collatz move is a division by two. If we start from `x · 2^k`, the first operation produces `x · 2^(k-1)`, the second produces `x · 2^(k-2)`, and so on. After exactly `k` operations we arrive at `x`.

Since every intermediate value is even, the Collatz process follows the division-by-two rule at every step, making the reconstruction valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    k, x = map(int, input().split())
    print(x * (1 << k))
```

The solution directly implements the reverse construction.

For each test case we need a number whose next `k` Collatz operations are all divisions by two. Multiplying by `2^k` creates exactly such a number.

The expression `1 << k` computes `2^k` efficiently using a bit shift. Since `k ≤ 20`, the result is very small and easily fits within Python integers.

No simulation is required. We construct the answer immediately and print it.

## Worked Examples

### Example 1

Input:

```
k = 1
x = 4
```

| Step | Current value |
| --- | --- |
| Final value given | 4 |
| Reverse 1 step | 8 |

Output:

```
8
```

Forward verification:

| Operation | Value |
| --- | --- |
| Start | 8 |
| Divide by 2 | 4 |

After one operation we obtain the required final value.

### Example 2

Input:

```
k = 5
x = 4
```

| Step | Current value |
| --- | --- |
| Final value given | 4 |
| Reverse 1 step | 8 |
| Reverse 2 steps | 16 |
| Reverse 3 steps | 32 |
| Reverse 4 steps | 64 |
| Reverse 5 steps | 128 |

Output:

```
128
```

Forward verification:

| Operation | Value |
| --- | --- |
| Start | 128 |
| 1 | 64 |
| 2 | 32 |
| 3 | 16 |
| 4 | 8 |
| 5 | 4 |

This trace shows the invariant clearly. Every step is an even number, so each Collatz operation is forced to be division by two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One multiplication per test case |
| Space | O(1) | Only a few variables are used |

The constraints are tiny, but this solution is even stronger. Each test case requires constant time and constant memory, easily fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        k, x = map(int, input().split())
        ans.append(str(x * (1 << k)))

    return "\n".join(ans) + "\n"

# provided sample format (answers need not match statement exactly)
assert run("3\n1 4\n1 5\n5 4\n") == "8\n10\n128\n"

# minimum values
assert run("1\n1 1\n") == "2\n"

# largest values
assert run("1\n20 20\n") == f"{20 * (1 << 20)}\n"

# x = 1 with several reverse steps
assert run("1\n5 1\n") == "32\n"

# multiple test cases
assert run("2\n2 3\n3 7\n") == "12\n56\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1` | `2` | Smallest valid case |
| `1 / 20 20` | `20971520` | Largest constraint values |
| `1 / 5 1` | `32` | Repeated reverse construction |
| `2 / (2,3) (3,7)` | `12, 56` | Multiple independent test cases |

## Edge Cases

Consider:

```
1
1 5
```

The value `5` does not have a valid odd predecessor because `(5 - 1) / 3` is not an odd integer. The algorithm never relies on odd predecessors. It simply doubles once and returns `10`. Running one Collatz step gives `10 → 5`, so the answer is valid.

Consider:

```
1
1 4
```

There are multiple valid predecessors, including `1` and `8`. The algorithm chooses `8` because doubling always works. Running one step gives `8 → 4`.

Consider:

```
1
20 20
```

The algorithm returns:

```
20 × 2^20 = 20971520
```

All twenty Collatz operations are divisions by two:

```
20971520 → 10485760 → ... → 20
```

The construction remains valid even at the largest allowed values.

Consider:

```
1
5 1
```

The algorithm outputs:

```
32
```

The forward sequence is:

```
32 → 16 → 8 → 4 → 2 → 1
```

After exactly five operations the result is the required final value `1`, confirming that repeated doubling correctly reconstructs a valid starting number.
