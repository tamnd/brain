---
title: "CF 102202D - A Plus Equals B"
description: "We start with two positive integers stored in variables A and B. The only allowed operations either double one variable or add the other variable to it. The goal is to produce any sequence of at most 5000 such operations after which the two variables contain the same value."
date: "2026-08-18T01:06:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "D"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 176
verified: false
draft: false
---

[CF 102202D - A Plus Equals B](https://codeforces.com/problemset/problem/102202/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We start with two positive integers stored in variables `A` and `B`. The only allowed operations either double one variable or add the other variable to it. The goal is to produce any sequence of at most 5000 such operations after which the two variables contain the same value. The sequence does not have to be shortest.

The values can initially be as large as (10^{18}), so a strategy that repeatedly adds the smaller value to the larger one is dangerous. For example, with `A = 1` and `B = 10^18`, repeatedly doing `B += A` would require (10^{18}-1) operations before equality, far beyond the limit. The 5000-operation restriction rules out any approach whose number of additions depends linearly on the numerical difference.

The useful operations are the doubling operations. If we conceptually replace `A` by `A / 2`, we can realize exactly the same normalized state by first doing `B += B`, because both variables then become twice as large relative to the conceptual state. More precisely, multiplying both current values by the same positive constant never changes which future sequence of additions makes them equal. Thus, when `A` is even, we may conceptually replace `A` by `A / 2` and output `B += B`. Similarly, when `B` is even, we may conceptually replace `B` by `B / 2` and output `A += A`.

After removing factors of two, both values are odd. If they are unequal, adding the smaller one to the larger one makes the larger value even. We can then repeatedly remove factors of two. This gives a Euclidean-algorithm-like process in which the difference becomes smaller very quickly.

The first edge case is equality at the beginning. For input `5 5`, the correct output is simply `0`, with no operation lines. A careless implementation that always performs an addition before checking equality would unnecessarily change the state and could miss the zero-operation answer.

The second edge case is an even value. For input `2 3`, we can conceptually divide `2` to get `1`, then proceed from the odd pair. One valid output is the sample sequence `B += B`, `B += A`, `A += A`, `A += A`. Starting from `(2,3)`, these states are `(2,6)`, `(2,8)`, `(4,8)`, and `(8,8)`. An implementation that treats division as an actual output operation would be invalid, because division is not allowed. The division must be translated back into the opposite variable's doubling operation.

The third edge case is when both values are even. For example, `4 6` can first be reduced conceptually to `2 3`, because both values have a common factor of two. If an implementation blindly assumes that one value is odd after a single division, it can make an incorrect parity decision. Dividing all common factors first avoids this situation cleanly.

## Approaches

A direct brute-force strategy could explore possible operation sequences. From every state there are four possible next operations, so searching to depth (d) can require examining (4^d) sequences. With a limit of 5000 operations, that is completely infeasible. Even a much simpler greedy strategy that repeatedly adds the smaller value to the larger one can require (10^{18}-1) operations on `1 10^18`. The problem is not asking for a shortest path through a small state space, so brute force gives us no useful structure.

The key observation is that doubling one variable can be interpreted as halving the other after scaling both variables by the same factor. Suppose the current conceptual state is `(A,B)` and `A` is even. Replacing it by `(A/2,B)` is equivalent, up to a common factor of two, to the actual state `(A,2B)`. The actual operation that produces that state is `B += B`. Since equality is unchanged by multiplying both values by the same positive number, this conceptual division is safe.

This gives us a way to make numbers smaller instead of larger. Whenever one value is even, repeatedly divide it by two. Once both values are odd, suppose `A < B`. We perform `B += A`. Now `B` is even because odd plus odd is even. We can divide `B` by two repeatedly until it becomes odd again. The difference also shrinks during this process.

To see the crucial reduction, let the current odd values be `A < B`, and let `D = B - A`. After `B += A`, the new value of `B` is `A + B`. Dividing it by two gives

[
B' = \frac{A+B}{2}.
]

The new difference is

[
B'-A = \frac{B-A}{2} = \frac{D}{2}.
]

If more divisions are possible, the difference becomes even smaller. Thus every nonterminal odd-to-odd round at least halves the positive difference. Since the initial difference is below (10^{18}), there can be at most about 60 such reductions.

The number of divisions performed during the process is also logarithmic. A standard bound for this construction is below 5000 operations for values up to (10^{18}). One convenient upper bound comes from observing that the difference loses at least one binary bit after each odd round. The total number of parity reductions over all rounds is bounded by a sum of logarithms, well below the 5000-operation allowance. This is the same structural reason the binary Euclidean algorithm is fast.

The brute-force approach works only because every operation is locally simple, but it has no way to exploit the enormous amount of information represented by repeated doubling. The parity observation compresses many useless additions into logarithmically many doubling operations and turns the problem into a binary version of Euclid's algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(4^d)) for depth (d) | (O(4^d)) | Too slow |
| Repeated smaller-to-larger addition | (O(\max(A,B))) | (O(1)) | Too slow |
| Binary reduction | (O(\log^2 \max(A,B))) | (O(\log \max(A,B))) for output | Accepted |

## Algorithm Walkthrough

1. Read `A` and `B`. If they are already equal, output zero operations. There is no reason to perform any operation because the target condition already holds.
2. Divide both values by their greatest common divisor conceptually. We do not need to output anything for this normalization. If the original values are `gA` and `gB`, every later operation on `(A,B)` produces exactly the corresponding value multiplied by `g` on the original pair, so the same operation sequence remains valid.
3. While `A` is even, conceptually replace `A` by `A / 2` and record `B += B`. Doubling `B` multiplies the whole pair by two relative to the conceptual state, so the recorded operation realizes the division without using an illegal operation.
4. While `B` is even, conceptually replace `B` by `B / 2` and record `A += A`. The same scaling argument applies with the roles reversed.
5. If the two conceptual values are equal, stop. All recorded operations are valid on the original values and have made the original variables equal.
6. If both values are odd and `A < B`, record `B += A` and replace the conceptual value of `B` by `A + B`. The new `B` is even, so the next iteration will divide it by two. This is the operation that decreases the difference.
7. If both values are odd and `B < A`, do the symmetric operation `A += B`. Again, the larger value becomes even, allowing it to be divided until it becomes odd.
8. Repeat the parity reductions and odd-value addition until the two values become equal. The difference decreases by at least a factor of two after every odd round, so only logarithmically many rounds are possible.

### Why it works

The invariant is that the conceptual pair represents the actual pair up to multiplication of both coordinates by the same positive integer. Such a common scaling does not affect whether the two coordinates can be made equal using the same future operations. A conceptual division by two is valid exactly when the corresponding coordinate is even, and the required scaling is implemented by doubling the other coordinate.

When both conceptual values are odd and unequal, adding the smaller to the larger makes the larger even. After dividing that value by two until it is odd, the difference between the two odd values is strictly smaller, in fact at least halved. A positive integer difference cannot be halved indefinitely, so eventually the process reaches equality. Every recorded operation is one of the four legal operations, and the common-scaling invariant guarantees that the conceptual equality corresponds to actual equality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_operations(a, b):
    g = __import__("math").gcd(a, b)
    a //= g
    b //= g

    ops = []

    while a != b:
        while a % 2 == 0:
            a //= 2
            ops.append("B+=B")

        while b % 2 == 0:
            b //= 2
            ops.append("A+=A")

        if a == b:
            break

        if a < b:
            b += a
            ops.append("B+=A")
        else:
            a += b
            ops.append("A+=B")

    return ops

def main():
    a, b = map(int, input().split())
    ops = build_operations(a, b)

    print(len(ops))
    sys.stdout.write("\n".join(ops))

if __name__ == "__main__":
    main()
```

The first section computes the greatest common divisor and removes it from both values. This is optional for correctness, but it keeps the conceptual numbers smaller and makes the termination argument cleaner. The actual input values are never modified directly, so the operations are still interpreted against the original pair.

The first inner loop handles an even `A`. The conceptual assignment `A //= 2` is represented by the real operation `B += B`. The mapping is easy to reverse accidentally, so the direction matters: dividing `A` corresponds to doubling `B`, while dividing `B` corresponds to doubling `A`.

The second inner loop handles the same transformation for `B`.

Only after both parity reductions do we compare the values. At this point, if they are different, both are odd. Adding the smaller value to the larger one is deliberate. Adding the larger value to the smaller one would also be legal, but it would destroy the decreasing-difference argument that gives the operation bound.

Python integers have arbitrary precision, so there is no integer overflow issue when an addition temporarily makes a value larger. In fact, after normalization and before the next division, the larger value is at most the sum of the two current values, so the numbers remain small enough that Python's arbitrary-precision arithmetic is easily sufficient.

The output contains only legal operations. The conceptual divisions never appear in the output, which is the central implementation detail of the solution.

## Worked Examples

### Example 1

For the sample input `2 3`, the greatest common divisor is `1`, so the conceptual state starts as `(2,3)`.

| Step | Operation | Conceptual A | Conceptual B |
| --- | --- | --- | --- |
| 0 | Initial | 2 | 3 |
| 1 | `B+=B` | 1 | 3 |
| 2 | `B+=A` | 1 | 4 |
| 3 | `A+=A` | 2 | 4 |
| 4 | `A+=A` | 4 | 4 |

The first operation represents dividing `A` from 2 to 1. The next operation adds the smaller odd value to the larger one, producing 4. The two following operations represent dividing `B` conceptually from 4 to 1 through the scaling interpretation, although the actual sequence is more naturally understood by applying the recorded operations to the original pair. Applying all four real operations to `(2,3)` gives `(8,8)`, so equality is reached exactly.

### Example 2

Consider `4 6`. Their greatest common divisor is 2, so the algorithm works with `(2,3)` instead.

| Step | Operation | Conceptual A | Conceptual B |
| --- | --- | --- | --- |
| 0 | Initial after gcd | 2 | 3 |
| 1 | `B+=B` | 1 | 3 |
| 2 | `B+=A` | 1 | 4 |
| 3 | `A+=A` | 2 | 4 |
| 4 | `A+=A` | 4 | 4 |

Applying these operations to the original `(4,6)` gives `(16,16)`. The same sequence works because the original pair is exactly twice the normalized pair throughout the process.

This example exercises the common-factor normalization. It also demonstrates why the operations can be derived using a smaller conceptual state without changing their validity on the original input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\log^2 M)) | There are (O(\log M)) reduction rounds, and the total parity reductions across the rounds are logarithmically bounded. |
| Space | (O(\log^2 M)) | The operation list stores every emitted operation, and the number of operations is below 5000. |

Here (M = \max(A,B)), with (M \le 10^{18}). The algorithm performs only logarithmically many meaningful reductions and emits fewer than 5000 operations, so both the computation and output size comfortably fit the 1 second time limit and 1024 MB memory limit.

## Test Cases

The output of this problem is not unique, so tests should validate the produced sequence rather than compare it with one fixed sequence. The following test harness runs the same construction as the submitted solution and checks that every emitted operation is legal, that no more than 5000 operations are produced, and that the final values are equal.

```python
import sys
import io
import math

def build_operations(a, b):
    g = math.gcd(a, b)
    a //= g
    b //= g

    ops = []

    while a != b:
        while a % 2 == 0:
            a //= 2
            ops.append("B+=B")

        while b % 2 == 0:
            b //= 2
            ops.append("A+=A")

        if a == b:
            break

        if a < b:
            b += a
            ops.append("B+=A")
        else:
            a += b
            ops.append("A+=B")

    return ops

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    a, b = map(int, sys.stdin.readline().split())
    ops = build_operations(a, b)

    result = str(len(ops))
    if ops:
        result += "\n" + "\n".join(ops)

    sys.stdin = old_stdin
    return result

def validate(inp: str, out: str):
    a, b = map(int, inp.split())
    lines = out.strip().splitlines()

    assert lines
    n = int(lines[0])
    assert 0 <= n <= 5000
    assert len(lines) == n + 1

    for op in lines[1:]:
        if op == "A+=A":
            a += a
        elif op == "A+=B":
            a += b
        elif op == "B+=A":
            b += a
        elif op == "B+=B":
            b += b
        else:
            raise AssertionError(f"Invalid operation: {op}")

    assert a == b

# Provided sample.
sample1 = run("2 3")
validate("2 3", sample1)

# Minimum-size input.
case2 = run("1 1")
validate("1 1", case2)
assert case2 == "0", "equal values need zero operations"

# Both values even with a common factor.
case3 = run("4 6")
validate("4 6", case3)

# Boundary values near 10^18.
case4 = run("1000000000000000000 999999999999999999")
validate("1000000000000000000 999999999999999999", case4)

# A large common factor and very different normalized values.
case5 = run("1000000000000000000 2000000000")
validate("1000000000000000000 2000000000", case5)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` | Any valid sequence, including the 4-operation sample | Provided sample and basic odd/even transition |
| `1 1` | `0` | Equality at the start |
| `4 6` | Any valid sequence ending with equal values | Common-factor normalization and both-even input |
| `1000000000000000000 999999999999999999` | Any valid sequence with at most 5000 operations | Values near the (10^{18}) boundary |
| `1000000000000000000 2000000000` | Any valid sequence with at most 5000 operations | Large common factor and repeated parity reductions |

## Edge Cases

For equal values, consider the exact input `5 5`. The gcd is 5, so the conceptual pair becomes `(1,1)`, and the main loop never runs. The output is `0`. The actual variables are already equal, so this is the correct and shortest possible result.

For an even and an odd value, consider `2 3`. The conceptual algorithm first divides `2` by two and records `B+=B`. The pair becomes `(1,3)`. Both values are then odd, so it records `B+=A`, conceptually producing `(1,4)`. The next parity reduction divides `4`, eventually reaching `(1,1)`. The recorded operations are all legal, and when executed on the original values they produce equal values.

For both values even, consider `4 6`. The gcd reduction changes the conceptual pair to `(2,3)`. The algorithm never needs to explicitly manipulate the common factor. The same operations that turn `(2,3)` into equality also turn `(4,6)` into equality because every operation is linear and preserves the common scaling factor.

For values close to the maximum, consider `1000000000000000000 999999999999999999`. The algorithm does not attempt to repeatedly add one value to the other. It first removes powers of two and then repeatedly reduces the difference through the odd-value addition and division process. Python's integer type safely handles every intermediate value, and the generated operation count remains within the 5000 limit.

For a highly unbalanced pair such as `1 1000000000000000000`, a naive repeated-addition solution would need essentially (10^{18}) operations. The binary method instead repeatedly exploits the evenness created after adding the smaller odd value. The conceptual difference loses binary magnitude rather than decreasing by one, which is exactly why the construction remains fast on such inputs.
