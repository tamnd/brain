---
title: "CF 102412F - IQ Test"
description: "We start with a set containing 0, 1, and 2. One operation chooses any two numbers x and y already in the set and inserts x 2 −y. The inserted value must stay between 0 and 10 18, and we may perform at most 43 operations."
date: "2026-08-11T08:28:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "F"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 93
verified: true
draft: false
---

[CF 102412F - IQ Test](https://codeforces.com/problemset/problem/102412/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a set containing `0`, `1`, and `2`. One operation chooses any two numbers `x` and `y` already in the set and inserts

x 2 −y.

The inserted value must stay between `0` and 10 18, and we may perform at most `43` operations. Given a target `n`, we only need to construct it, not minimize the number of operations. The official statement allows any valid construction within those limits.

The target can be as large as 10 18, so trying to search through all possible constructions is hopeless. The useful structure is the square in the operation. If we want to construct some number `p`, we can choose `x` close to p ​, which makes both numbers needed to construct `p` dramatically smaller than `p`.

The small values `0`, `1`, and `2` are already available, so they must be treated as terminal states. For example, if `n = 2`, the correct output is simply empty output because the target is already in the initial set. A careless implementation that always tries to generate `n` would unnecessarily construct another value and can even create an invalid recursive loop.

Another edge case is a perfect square. For `n = 9`, choosing `x = 3` gives `y = 0`, so `3^2 - 0 = 9`. The correct construction can be just

```
3 0
```

A careless implementation that assumes `y` must be positive would reject a perfectly valid construction, even though the statement explicitly allows zero.

The other boundary case is a value just below a square. For example, `n = 15` gives `x = 4` and `y = 1`, because 4 2 −1=15. The important detail is that `x` must be the ceiling of the square root, not the floor. Using `x = 3` would make 3 2 −15 negative and violate the output condition.

The actual constraints are unusually friendly to a square-root reduction. The target is at most 10 18, so its square root is at most 10 9. Repeatedly taking square roots reduces the magnitude extremely quickly, reaching tiny values after only a handful of levels. The official limits are one second and 256 MiB, with at most 43 operations allowed.

## Approaches

A brute-force approach would try to explore the possible sets reachable after every operation. Given the current set, it could choose every ordered pair `(x, y)`, compute `x²-y`, and recursively explore the resulting state. This is correct because every legal construction is represented by some sequence of such choices.

The problem is the number of choices. Even from the initial set there are 3 2 =9 ordered pairs. If we naïvely branch on every pair for 43 operations, just the number of possible choice sequences is already

9 43 ≈10 41 .

The actual branching becomes even larger once the set contains more values. Keeping track of entire sets also creates a huge state space, so brute force is not remotely practical.

The key observation is to reverse the final operation. Suppose we want to construct `p`. We need some already constructible `x` and `y` satisfying

x 2 −y=p.

Choose

x=⌈ p ​ ⌉,y=x 2 −p.

Then the equation is automatically satisfied. The interesting part is the size of the two new targets. Since `x` is the smallest integer with x 2 ≥p, we have

(x−1) 2 <p≤x 2 .

Thus

0≤y=x 2 −p<x 2 −(x−1) 2 =2x−1.

So `x` is about p ​, and `y` is at most about 2 p ​. Instead of constructing one number of size `p`, we recursively construct two numbers whose sizes are roughly square roots of `p`.

For p≤10 18, the first `x` is at most 10 9, and `y` is at most about 2⋅10 9. The next recursion level drops to roughly 10 5, then a few hundred, then a few dozen, and finally the initial values `0`, `1`, and `2`. The resulting construction comfortably stays below the required 43 operations.

The construction is essentially divide and conquer, but the split is based on square roots rather than halves. We recursively construct the dependencies first, then print the operation that creates the current number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | At least O(9 43 ) construction branches | Exponential | Too slow |
| Optimal | O(Klogn), where K≤43 | O(K) | Accepted |

## Algorithm Walkthrough

1. Initialize the set of already available numbers with `0`, `1`, and `2`. These numbers require no operations, so the recursion stops immediately when it reaches one of them.
2. For a target `p` that is not already available, compute x=⌈ p ​ ⌉. In Python, this can be obtained exactly with `math.isqrt`, avoiding floating-point precision problems for values near 10 18.
3. Compute y=x 2 −p. By construction, x 2 −y=p, so once `x` and `y` have been constructed, one final operation creates `p`.
4. Recursively construct `x` and `y` before recording `(x, y)`. This ordering is required because the operation is only legal when both operands already belong to the set.
5. Store every constructed value in a `seen` set. This prevents repeating the same operation when two different recursive branches need the same intermediate value.
6. After both dependencies are available, append `(x, y)` to the answer and mark `p` as constructed. The resulting list is already in a valid execution order because every operation appears after the operations needed for its operands.

### Why it works

The invariant is that whenever `build(p)` finishes, `p` belongs to the constructed set and every operation stored so far is legal in the order in which it is printed. For a new `p`, we choose x=⌈ p ​ ⌉ and y=x 2 −p, so x 2 −y=p exactly. The recursive calls construct `x` and `y` first, after which the final operation is legal and inserts `p`. Since `x` and `y` are much smaller than `p`, recursion reaches `0`, `1`, or `2` and terminates.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import isqrt

def solve():
    n = int(input())

    # These numbers are present before any operation.
    seen = {0, 1, 2}
    operations = []

    def build(p):
        if p in seen:
            return

        # x is the smallest integer with x^2 >= p.
        x = isqrt(p)
        if x * x < p:
            x += 1

        y = x * x - p

        # Both operands must already exist before we can use them.
        build(x)
        build(y)

        operations.append((x, y))
        seen.add(p)

    build(n)

    out = []
    for x, y in operations:
        out.append(f"{x} {y}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `seen` set represents exactly the numbers that are currently available in the simulated construction. Starting it with `0`, `1`, and `2` matches the initial state of the problem.

The square-root calculation deserves some care. Using `int(math.sqrt(p))` is unsafe as a general integer technique because floating-point numbers do not represent every integer up to 10 18 exactly. `isqrt` computes the integer square root exactly. If `x*x < p`, incrementing `x` gives the ceiling square root.

The recursive calls happen before `operations.append((x, y))`. Reversing these two lines would produce an invalid answer because the printed operation could refer to numbers that have not been generated yet.

Python integers have arbitrary precision, so there is no overflow issue. In fact, the largest `x` is only 10 9, while `y` is only on the order of 10 9, even though the target itself may be 10 18.

The `seen` check also handles shared dependencies. If the same intermediate value appears in two branches, it is generated only once, keeping the operation count safely within the limit.

## Worked Examples

For Sample 1, the target is `5`.

| Step | Target being built | x | y | Operation |
| --- | --- | --- | --- | --- |
| 1 | `3` | `2` | `1` | 2 2 −1=3 |
| 2 | `4` | `2` | `0` | 2 2 −0=4 |
| 3 | `5` | `3` | `4` | 3 2 −4=5 |

The resulting output can be

```
2 1
2 0
3 4
```

The sample itself also constructs `0` first using `1 1`, but that operation is unnecessary because `0` is already in the initial set. Since the problem accepts any valid construction, omitting redundant operations is preferable.

The trace shows the dependency ordering clearly. To construct `5`, we need `3` and `4`; both are constructed from the initial values before the final operation is printed.

For Sample 2, the target is `7`.

| Step | Target being built | x | y | Operation |
| --- | --- | --- | --- | --- |
| 1 | `3` | `2` | `1` | 2 2 −1=3 |
| 2 | `7` | `3` | `2` | 3 2 −2=7 |

The resulting output is

```
2 1
3 2
```

This demonstrates the particularly short case where the target's square-root dependency is itself immediately constructible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Klogn) | At most `K <= 43` distinct operations are produced, and each uses an integer square root and set operations |
| Space | O(K) | The recursion, `seen` set, and operation list contain only the generated intermediate values |

The important part of the complexity is not a conventional polynomial bound over n. The recursion depth is tiny because the largest dependency is roughly 2 n ​. Starting from 10 18, the magnitudes fall through approximately 10 9, 10 5, 10 2, and then small integers. The construction therefore fits comfortably inside the 43-operation limit and uses negligible memory under the 256 MiB limit.

## Test Cases

Because the output is not unique, the test harness should validate the generated sequence instead of comparing it with one fixed string. The validator below checks that every operand was already available, every generated value is legal, the target is eventually generated, and no more than 43 operations are printed.

```python
# helper: run solution on input string, return output string
import sys
import io
from math import isqrt

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        n = int(sys.stdin.readline())

        seen = {0, 1, 2}
        operations = []

        def build(p):
            if p in seen:
                return

            x = isqrt(p)
            if x * x < p:
                x += 1

            y = x * x - p

            build(x)
            build(y)

            operations.append((x, y))
            seen.add(p)

        build(n)

        sys.stdout.write(
            "\n".join(f"{x} {y}" for x, y in operations)
        )
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, output: str) -> bool:
    n = int(inp.strip())

    available = {0, 1, 2}
    lines = output.strip().splitlines() if output.strip() else []

    assert len(lines) <= 43, "too many operations"

    for line in lines:
        parts = line.split()
        assert len(parts) == 2, "each operation needs x and y"

        x, y = map(int, parts)

        assert x in available, f"x={x} was not constructed"
        assert y in available, f"y={y} was not constructed"

        value = x * x - y
        assert 0 <= value <= 10**18, "generated value is out of range"

        available.add(value)

    assert n in available, f"target {n} was not constructed"
    return True

# Provided sample 1.
out = run("5\n") if False else solution("5\n")
assert validate("5\n", out), "sample 1"

# Provided sample 2.
out = solution("7\n")
assert validate("7\n", out), "sample 2"

# Minimum-size input: target already exists initially.
out = solution("0\n")
assert out == "", "zero needs no operations"

# All-equal / smallest nontrivial construction.
out = solution("4\n")
assert validate("4\n", out), "constructing a perfect square"

# Boundary case just below a square.
out = solution("15\n")
assert validate("15\n", out), "value just below 16"

# Maximum-size target.
out = solution("1000000000000000000\n")
assert validate("1000000000000000000\n", out), "maximum target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | Empty output | Initial-set boundary |
| `4` | Any valid construction | Perfect-square handling and zero as `y` |
| `15` | Any valid construction | Ceiling-square-root boundary |
| `1000000000000000000` | Any valid construction with at most 43 operations | Maximum target and recursion depth |

## Edge Cases

For `n = 0`, the algorithm enters `build(0)`, immediately sees that `0` is already in `seen`, and returns. The exact input is

```
0
```

and the correct output is empty. No operation is necessary, and printing an unnecessary operation would only make the construction longer.

For a perfect square such as `n = 9`, `isqrt(9)` returns `3` and `3*3` is already equal to `n`, so `y = 0`. The recursive calls for `3` and `0` construct `3` and then print

```
3 0
```

which gives 3 2 −0=9. Zero is a legitimate operand because it is present from the beginning.

For a number just below a square, such as `n = 15`, the floor square root is `3`, but that cannot be used because 3 2 −15 is negative. The algorithm detects `3*3 < 15`, increments `x` to `4`, and obtains `y = 1`. The final operation is

```
4 1
```

which gives 16−1=15. This is exactly why the ceiling square root is required.

For the maximum target,

```
1000000000000000000
```

the first choice is `x = 1000000000` and `y = 0`. The algorithm only needs to construct `1000000000`, after which the target is produced by

```
1000000000 0
```

The recursive construction of `1000000000` uses values around its square root, and the same reduction continues until only the initial values remain. The magnitude shrinks so quickly that the entire dependency tree remains within the permitted 43 operations.
