---
title: "CF 102201A - A Plus Equals B"
description: "We start with two positive integers, A and B, each at most (10^{18}). In one operation, we may double either value, or add one value to the other. The goal is not to minimize the number of operations."
date: "2026-08-18T10:20:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "A"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 707
verified: true
draft: false
---

[CF 102201A - A Plus Equals B](https://codeforces.com/problemset/problem/102201/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with two positive integers, `A` and `B`, each at most (10^{18}). In one operation, we may double either value, or add one value to the other. The goal is not to minimize the number of operations. We only need to produce some valid sequence of at most 5000 operations that eventually makes the two values equal.

The output is a sequence of operation names. Since the judge simulates those operations, our task is constructive: we need to find a reliable process that always terminates quickly enough.

The large upper bound of (10^{18}) rules out any approach that tries to increase the numbers until some conveniently chosen common value. Such a value can be enormous, and even a logarithmic search over possible targets is not naturally tied to the allowed operations. The 5000-operation limit also tells us that the intended solution should have a strong decreasing measure rather than merely relying on eventual termination.

There is a useful equivalence hidden in the doubling operations. Suppose conceptually that our current state is `(A, B)` and `A` is even. If we output `B+=B`, the actual state becomes `(A, 2B)`. Dividing both coordinates of this actual state by 2 gives `(A/2, B)`, and multiplying both coordinates by the same positive constant does not change whether they can be made equal by the same sequence of additive and doubling operations. Thus, from the point of view of the ratio between the two numbers, `B+=B` lets us treat an even `A` as if we had divided `A` by 2. Symmetrically, `A+=A` lets us conceptually divide an even `B` by 2.

This gives the main edge cases.

For input `5 5`, the numbers are already equal, so the correct output is simply `0`. A careless implementation that always performs an addition before checking equality would produce unnecessary operations and can even move away from the target.

For input `2 3`, we can conceptually divide `A` by 2 by performing `B+=B`, giving the equivalent normalized state `(1, 3)`. Then `B+=A` corresponds to `(1, 4)`, and `A` can be doubled twice to reach `4`. The sample uses exactly this idea, producing four operations. A careless implementation that only tries to add the smaller number to the larger one can grow the values indefinitely instead of exploiting powers of two.

For input `1 1`, the answer is again `0`. This catches implementations that enter a normalization loop without first checking whether the numbers are already equal.

## Approaches

A straightforward brute-force approach would treat every possible operation as a branch and search for a state with `A == B`. From any state there are four choices, so a search up to depth 5000 has

[
1+4+4^2+\dots+4^{5000}
]

candidate operation sequences, with the deepest level alone containing (4^{5000}) possibilities. Even with aggressive pruning, there is no useful finite state space because the numbers can grow without bound. This approach is completely impractical.

The brute-force search does have one useful property: every operation preserves positivity, and every successful path eventually reaches two equal values. The problem is finding such a path without exploring an exponential number of choices.

The key observation is that doubling can be used as a conceptual division by two. Once we decide to work with values up to a common scaling factor, every even number can be divided by two using one allowed operation. This means we can repeatedly remove factors of two from both numbers.

Eventually both values are odd. If they are equal, we are done. Otherwise, suppose `A < B`. Since both are odd, `A+B` is even. We perform `B+=A`, changing the pair to `(A, A+B)`. The second value is now even, so we can conceptually divide it by two repeatedly until it becomes odd.

After one division, the new second value is

[
\frac{A+B}{2}.
]

Because `A < B`, this is strictly smaller than `B`. More importantly, the difference is reduced by at least half:

[
\frac{A+B}{2}-A=\frac{B-A}{2}.
]

If more than one division is possible, the second value becomes even smaller, so the difference decreases at least as much.

Thus every time both values are odd and unequal, one addition followed by some divisions substantially reduces their difference. Since the initial difference is below (10^{18}), there can be only about 60 such reduction rounds.

The same argument also gives a comfortable bound on the total number of operations. Between two addition rounds, each value is divided by two until it becomes odd. Since the values never exceed (10^{18}) after normalization, at most about 60 such divisions are needed in a round. The total stays well below 5000.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4^{5000})) candidate sequences | (O(5000)) per search path, potentially exponential overall | Too slow |
| Optimal | (O(\log \max(A,B))) reduction rounds, with logarithmic normalization work | (O(\log \max(A,B))) | Accepted |

## Algorithm Walkthrough

1. Read `A` and `B`. If they are already equal, output zero operations. No transformation is necessary.
2. While `A` is even, record `B+=B` and conceptually replace `A` by `A/2`. The recorded operation doubles the other coordinate, so the actual pair is a common factor of two larger than the conceptual pair. Equality behavior is unchanged by that common scaling.
3. While `B` is even, record `A+=A` and conceptually replace `B` by `B/2`. This is the symmetric version of the previous step.
4. If the normalized values are equal, stop. Both values are now odd, so any remaining unequal state has a particularly simple structure.
5. If `A < B`, record `B+=A`. The conceptual value of `B` becomes `A+B`, which is even because both inputs were odd.
6. Divide the new `B` by two repeatedly, recording `A+=A` for every conceptual division. The resulting odd `B` is smaller than the previous `B`, and the gap between the two values has been reduced by at least half.
7. If `B < A`, perform the symmetric operation `A+=B`, then repeatedly divide `A` by two by recording `B+=B`.
8. Repeat the normalization and addition process until the two conceptual values become equal. Output all recorded operations in their original order.

The invariant is that the conceptual pair always represents the actual pair up to multiplication of both coordinates by the same positive power of two. Such a common scaling does not change whether a future sequence of the allowed operations can make the coordinates equal. Every recorded operation is exactly the real operation that realizes the corresponding conceptual transformation. When both values are odd and unequal, adding the smaller to the larger makes that larger value even, after which the conceptual divisions reduce the difference by at least a factor of two. Since the difference is a nonnegative integer, this process must eventually reach zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    operations = []

    while a != b:
        while a % 2 == 0:
            # Conceptually: a /= 2.
            # Real operation: double b, preserving the ratio.
            operations.append("B+=B")
            a //= 2

        while b % 2 == 0:
            # Conceptually: b /= 2.
            # Real operation: double a, preserving the ratio.
            operations.append("A+=A")
            b //= 2

        if a == b:
            break

        if a < b:
            # Both are odd here, so a + b is even.
            operations.append("B+=A")
            b += a
        else:
            operations.append("A+=B")
            a += b

    print(len(operations))
    sys.stdout.write("\n".join(operations))

if __name__ == "__main__":
    solve()
```

The `operations` list stores the actual commands that must be printed. The variables `a` and `b` are deliberately treated as the normalized conceptual values rather than the literal values obtained by simulating every command.

When `a` is even, the code divides it by two and records `B+=B`. In the real execution, doubling `B` would produce `(a, 2b)`. This is exactly twice the conceptual state `(a/2, b)`, so the two representations have the same ratio and the same future equality behavior.

The same reasoning applies when `b` is even, using `A+=A`.

Once both values are odd, the code adds the smaller value to the larger one. For example, if `a < b`, the operation `B+=A` changes `b` to `a+b`, which is even. The next iteration immediately enters the division loop and removes all factors of two.

The order of the two normalization loops is not significant for correctness. After the first loop, `a` is odd, and after the second loop, `b` is odd. If the two values become equal during normalization, the outer loop terminates before performing an unnecessary addition.

Python integers do not overflow, so values temporarily produced by the conceptual addition are safe. More importantly, the normalized values remain bounded, because after adding two odd values and dividing the result by at least two, the new value is at most the previous larger value.

## Worked Examples

### Sample 1

For the sample input `2 3`, the algorithm starts with `(2, 3)`. The first value is even, so we conceptually divide it by two while recording `B+=B`.

| Step | A | B | Operation |
| --- | --- | --- | --- |
| 0 | 2 | 3 | start |
| 1 | 1 | 3 | `B+=B` |
| 2 | 1 | 4 | `B+=A` |
| 3 | 1 | 2 | `A+=A` |
| 4 | 1 | 1 | `A+=A` |

The conceptual state ends at `(1, 1)`. In the actual execution, the corresponding states are `(2, 6)`, `(2, 8)`, `(4, 8)`, and `(8, 8)`, so the printed sequence really does make the original values equal.

The trace demonstrates the scaling invariant. The normalized values can become smaller even though every actual operation only increases a number.

### Sample 2

Consider the input `1 5`.

| Step | A | B | Operation |
| --- | --- | --- | --- |
| 0 | 1 | 5 | start |
| 1 | 1 | 6 | `B+=A` |
| 2 | 1 | 3 | `A+=A` |
| 3 | 1 | 4 | `B+=A` |
| 4 | 1 | 2 | `A+=A` |
| 5 | 1 | 1 | `A+=A` |

The first addition changes `(1,5)` to `(1,6)`. Because the new `B` is even, we conceptually divide it to obtain `(1,3)`. The same process then transforms `(1,3)` to `(1,1)`.

The difference goes from `4` to `2` to `0`, illustrating the decreasing measure used by the proof.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log^2 \max(A,B))) in a direct conservative bound | There are (O(\log \max(A,B))) reduction rounds, and each round can remove (O(\log \max(A,B))) factors of two |
| Space | (O(\log \max(A,B))) | The operation list contains only the generated commands |

For values at most (10^{18}), there are fewer than 60 meaningful halvings per scale. A conservative bound is below 4000 operations, comfortably inside the required 5000. The Python implementation also performs only a few thousand integer operations, so the 1 second limit is easily sufficient.

## Test Cases

The output is not unique, so the tests should not compare the raw output string with one predetermined sequence. Instead, the test helper parses the generated operations and simulates them on the original values, checking that the final values are equal and that no more than 5000 operations were produced.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    a, b = map(int, input().split())
    operations = []

    while a != b:
        while a % 2 == 0:
            operations.append("B+=B")
            a //= 2

        while b % 2 == 0:
            operations.append("A+=A")
            b //= 2

        if a == b:
            break

        if a < b:
            operations.append("B+=A")
            b += a
        else:
            operations.append("A+=B")
            a += b

    print(len(operations))
    sys.stdout.write("\n".join(operations))

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

def valid(inp: str, out: str) -> bool:
    a, b = map(int, inp.split())
    lines = out.strip().splitlines()

    if not lines:
        return False

    n = int(lines[0])
    if n < 0 or n > 5000:
        return False
    if len(lines) != n + 1:
        return False

    allowed = {"A+=A", "A+=B", "B+=A", "B+=B"}

    for op in lines[1:]:
        if op not in allowed:
            return False

        if op == "A+=A":
            a += a
        elif op == "A+=B":
            a += b
        elif op == "B+=A":
            b += a
        else:
            b += b

    return a == b

# provided sample
sample = "2 3"
assert valid(sample, run(sample)), "sample 1"

# minimum-size input
case = "1 1"
assert valid(case, run(case)), "already equal"

# both values are powers of two
case = "1 1024"
assert valid(case, run(case)), "power-of-two ratio"

# odd values requiring several add-and-normalize rounds
case = "1 5"
assert valid(case, run(case)), "odd values"

# maximum input boundary
case = "1000000000000000000 999999999999999999"
assert valid(case, run(case)), "maximum-size values"

# asymmetric values with many factors of two
case = "576460752303423488 1"
assert valid(case, run(case)), "large power of two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | Any valid sequence | Provided sample and basic construction |
| `1 1` | `0` operations | Already-equal boundary |
| `1 1024` | Any valid sequence | Repeated conceptual halving |
| `1 5` | Any valid sequence | Odd addition followed by normalization |
| `1000000000000000000 999999999999999999` | Any valid sequence | Maximum input magnitude |
| `576460752303423488 1` | Any valid sequence | Many powers of two and operation-count handling |

## Edge Cases

For `5 5`, the outer condition `while a != b` is false immediately. The operation list remains empty, so the program prints `0`. This is the only correct kind of behavior needed here because the initial state already satisfies the goal.

For `2 3`, the first normalization sees that `A` is even. The program records `B+=B` and changes the conceptual state to `(1,3)`. Since both values are now odd and unequal, it records `B+=A`, giving `(1,4)`. The next normalization divides `B` twice, giving `(1,1)`. The actual sequence is `B+=B`, `B+=A`, `A+=A`, `A+=A`, and the real state evolves from `(2,3)` to `(2,6)`, then `(2,8)`, then `(4,8)`, and finally `(8,8)`.

For `1 5`, both values start odd. Since `1 < 5`, the program performs `B+=A`, obtaining the conceptual state `(1,6)`. The even value can now be halved, producing `(1,3)`. The difference has dropped from `4` to `2`. The same process changes `(1,3)` to `(1,1)`. This demonstrates why an odd pair should not simply keep adding the smaller value without normalization.

For `1000000000000000000 999999999999999999`, the numbers are at the maximum allowed magnitude and differ by one. Both are odd, so the algorithm adds the smaller to the larger, making the larger value even. It then repeatedly removes factors of two conceptually. Each such round decreases the difference sharply, and the normalized values never grow beyond the original scale. The large input size is consequently handled without any overflow or search over large target values.

For `576460752303423488 1`, the first number is (2^{59}). The algorithm can remove its powers of two one at a time using `B+=B`, reducing the conceptual `A` from (2^{59}) to `1`. The two values then become equal. This exercises the longest simple normalization chain and confirms that the operation list remains far below the 5000-operation limit.
