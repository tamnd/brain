---
title: "CF 11B - Jumping Jack"
description: "Jack starts at position 0 on a number line. His jumps have fixed lengths: the first jump must have length 1, the second"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 11
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 11"
rating: 1600
weight: 11
solve_time_s: 86
verified: true
draft: false
---

[CF 11B - Jumping Jack](https://codeforces.com/problemset/problem/11/B)

**Rating:** 1600  
**Tags:** math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Jack starts at position `0` on a number line. His jumps have fixed lengths: the first jump must have length `1`, the second jump length `2`, the third jump length `3`, and so on. For every jump he may choose either direction. The task is to find the minimum number of jumps needed to land exactly on position `x`.

The direction choice is the interesting part. After `k` jumps, the total distance moved is always:

$1+2+3+\dots+k=\frac{k(k+1)}{2}$

The only thing we control is which jumps are positive and which are negative.

The input size goes up to `10^9`, which immediately rules out any state-space search over positions. A breadth-first search over reachable coordinates would explode because after `k` jumps there are `2^k` direction choices. Even `k = 40` already produces more than a trillion possibilities.

The answer itself stays small because triangular numbers grow quadratically. To reach distance around `10^9`, we only need roughly:

$\frac{k(k+1)}{2}\approx 10^9$

which gives `k ≈ 44721`. That means an `O(sqrt(x))` solution is completely safe.

Negative targets are an easy place to make mistakes. The problem is symmetric around zero because every sequence of left and right jumps can be mirrored. Reaching `-5` takes the same number of jumps as reaching `5`. A careless implementation that treats negative values separately may introduce unnecessary complexity.

Another subtle case appears when the accumulated sum first exceeds the target but has the wrong parity. For example:

Input:

```
2
```

After two jumps, the total distance is `1 + 2 = 3`. We cannot make `2` because changing the direction of a jump changes the final position by twice that jump length. The difference `3 - 2 = 1` is odd, so no subset of jumps can fix it. We need one more jump, giving total `6`, and now `6 - 2 = 4` is even, so the answer becomes `3`.

A second parity trap is:

Input:

```
5
```

The sum after three jumps is `6`, which already exceeds `5`, but `6 - 5 = 1` is odd. After four jumps the sum becomes `10`, and `10 - 5 = 5` is still odd. Only after five jumps do we get `15 - 5 = 10`, which is even. The correct answer is `5`, not `3` or `4`.

## Approaches

The brute-force idea is straightforward. At jump `i`, choose either left or right and recursively continue. After `k` jumps there are `2^k` possible paths. The method is correct because it explores every legal sequence of directions, but it becomes useless almost immediately. Even with only `40` jumps, the search space exceeds one trillion states.

The key observation is that only the total signed sum matters. Suppose after `k` jumps the total distance is:

$S=1+2+\dots+k$

If we initially imagine all jumps going to the right, we land at `S`. Flipping a jump of length `d` to the opposite direction changes the final position by `2d`, because that jump contributes `+d` instead of `-d`.

So every reachable position after `k` jumps has the form:

$S-2t$

where `t` is the sum of some subset of jump lengths.

This immediately gives two necessary conditions for reaching `x`.

First, `S` must be at least `|x|`, otherwise we simply do not have enough total movement.

Second, `S - |x|` must be even, because it equals `2t`.

The beautiful part is that these conditions are also sufficient. Since the numbers `1,2,3,...,k` can form every value from `0` to `S`, any even difference can be corrected by flipping an appropriate subset of jumps.

That reduces the problem to finding the smallest `k` such that:

$\frac{k(k+1)}{2}\ge |x|$

and

$\left(\frac{k(k+1)}{2}-|x|\right)\bmod 2=0$

We can simply keep increasing `k` until both conditions hold.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(k) | Too slow |
| Optimal | O(sqrt(x)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target position `x`.
2. Replace `x` with `abs(x)`. Reaching `-x` requires the same number of jumps as reaching `x` because every direction can be mirrored.
3. Initialize `k = 0` and `total = 0`. Here `k` is the number of jumps used so far, and `total` is the sum `1 + 2 + ... + k`.
4. Repeatedly increase `k` by one and add it to `total`.
5. After every update, check two conditions:

1. `total >= x`
2. `(total - x) % 2 == 0`
6. Stop as soon as both conditions become true. At this point we know some subset of jumps can be flipped to produce exactly `x`.
7. Output `k`.

The parity check is the core insight. Flipping a jump changes the final coordinate by an even number, so the difference between `total` and `x` must be even.

### Why it works

After `k` jumps, the maximum reachable coordinate is `total = 1 + 2 + ... + k`. Any other reachable coordinate is obtained by flipping some jumps, and every flipped jump changes the final value by `2d`. That means every reachable coordinate differs from `total` by an even number.

So the reachable positions are exactly all integers with the same parity as `total` inside the interval `[-total, total]`.

The algorithm searches for the first `k` where `x` lies inside this reachable set. Since we test `k` in increasing order, the first valid one is the minimum answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = abs(int(input()))

k = 0
total = 0

while total < x or (total - x) % 2 != 0:
    k += 1
    total += k

print(k)
```

The implementation mirrors the mathematical reasoning directly.

The first line converts the target to its absolute value. This removes the need to think about left and right separately. The answer for `-17` is identical to the answer for `17`.

The variables `k` and `total` track the current number of jumps and the triangular sum after those jumps. Every iteration simulates adding the next mandatory jump length.

The loop condition contains both required properties. The first part checks whether we have accumulated enough distance to even reach the target. The second part checks parity compatibility.

A common mistake is to stop as soon as `total >= x`. That fails on cases like `x = 2`, because `3` and `2` have different parity. Another mistake is checking parity before verifying `total >= x`, which can accidentally accept impossible states.

Python integers automatically handle large values, so there is no overflow risk. In languages with fixed-width integers, a 32-bit signed integer is still enough here because the largest triangular sum stays near `10^9`.

## Worked Examples

### Example 1

Input:

```
2
```

| Iteration | k | total | total >= x | (total - x) even? |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | No | Yes |
| 1 | 1 | 1 | No | No |
| 2 | 2 | 3 | Yes | No |
| 3 | 3 | 6 | Yes | Yes |

Output:

```
3
```

This trace demonstrates why exceeding the target is not enough. After two jumps we can reach `3`, `1`, `-1`, or `-3`, but not `2`. The parity mismatch blocks it.

### Example 2

Input:

```
5
```

| Iteration | k | total | total >= x | (total - x) even? |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | No | No |
| 1 | 1 | 1 | No | Yes |
| 2 | 2 | 3 | No | Yes |
| 3 | 3 | 6 | Yes | No |
| 4 | 4 | 10 | Yes | No |
| 5 | 5 | 15 | Yes | Yes |

Output:

```
5
```

This example shows that one extra jump is not always enough to fix parity. Adding jump `4` changed the total from `6` to `10`, which still differs from `5` by an odd number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(x)) | The triangular sum grows quadratically, so the loop runs about `sqrt(2x)` times |
| Space | O(1) | Only a few integer variables are stored |

For `x = 10^9`, the loop executes roughly `45000` iterations, which is tiny for a 1-second time limit. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    x = abs(int(input()))

    k = 0
    total = 0

    while total < x or (total - x) % 2 != 0:
        k += 1
        total += k

    print(k)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("2\n") == "3\n", "sample 1"

# minimum value
assert run("0\n") == "0\n", "already at origin"

# negative target
assert run("-2\n") == "3\n", "symmetry around zero"

# exact triangular number
assert run("6\n") == "3\n", "1+2+3 reaches target exactly"

# parity adjustment case
assert run("5\n") == "5\n", "needs extra jumps for parity"

# large boundary
assert run("1000000000\n") == "44723\n", "large input performance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0` | No jumps needed |
| `-2` | `3` | Symmetry for negative targets |
| `6` | `3` | Exact triangular sum case |
| `5` | `5` | Multiple parity corrections |
| `1000000000` | `44723` | Performance near upper bound |

## Edge Cases

Consider the input:

```
0
```

The algorithm immediately succeeds because `total = 0` already satisfies both conditions. The loop never runs, and the answer is correctly `0`.

Now consider:

```
-2
```

The algorithm converts this to `2`. The iterations become identical to the earlier worked example. After three jumps we have `total = 6`, and `6 - 2 = 4` is even, so the answer is `3`. Mirroring directions transforms any solution for `2` into a solution for `-2`.

The parity trap appears clearly with:

```
2
```

After two jumps the total is `3`. Since `3 - 2 = 1` is odd, no subset of jumps can adjust the position to exactly `2`. The algorithm correctly continues one more step.

A more subtle parity case is:

```
5
```

The totals evolve as `1, 3, 6, 10, 15`. The first two totals are too small. The next two have odd difference from `5`. Only `15` produces an even difference. The algorithm correctly outputs `5`.
