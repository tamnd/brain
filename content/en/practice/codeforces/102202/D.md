---
title: "CF 102202D - A Plus Equals B"
description: "We start with two positive integers, A and B. The only way to change them is to add one of the current values to either variable. Thus an operation can double one variable, or replace one variable by the sum of the two."
date: "2026-08-24T16:10:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "D"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 2420
verified: false
draft: false
---

[CF 102202D - A Plus Equals B](https://codeforces.com/problemset/problem/102202/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 40m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We start with two positive integers, `A` and `B`. The only way to change them is to add one of the current values to either variable. Thus an operation can double one variable, or replace one variable by the sum of the two. The goal is to output any sequence of at most 5000 such operations that makes the two values equal. The input contains the initial values of `A` and `B`, each at most \(10^{18}\). The official contest statement has exactly this construction and limit. citeturn3search1

The bound of \(10^{18}\) immediately rules out any method whose number of operations depends linearly on the values. A construction that needs \(A+B\), \(|A-B|\), or even \(\max(A,B)\) steps can require around \(10^{18}\) operations. The 5000 operation limit is the real algorithmic constraint, so we need a logarithmic or similarly small construction. Since the input contains only two integers, there is no need for sophisticated data structures, and the memory limit is generous enough that storing a few thousand operation strings is trivial.

The first edge case is equality from the start. For input `5 5`, the correct output is simply `0`, because no operation is needed. A careless implementation that always enters its reduction loop can perform unnecessary operations and, more seriously, may move away from the already valid answer.

The second edge case is an even value. For input `4 6`, we can conceptually reduce the pair to `(1, 3)` by halving both values, but the allowed operations do not contain division. The construction has to realize those divisions indirectly. Outputting `B+=B` corresponds to treating `A` as halved after removing a common factor of two, while `A+=A` plays the symmetric role for `B`. Directly writing `A//=2` without producing the corresponding operation would produce a mathematically useful calculation but an invalid answer.

The third edge case is a pair of odd values. For input `3 5`, adding the smaller value to the larger gives `(3, 8)`. The new larger value is even, so it can be halved in the normalized representation. If we instead repeatedly add the smaller value without using parity, the values can grow rather than approach equality.

## Approaches

A straightforward approach is to search through possible operation sequences. From every state there are four choices, so after \(k\) steps there can be as many as \(4^k\) sequences to consider. Searching up to the allowed depth of 5000 is completely impossible, since the sequence count is on the order of \(4^{5000}\). Even memoizing states does not give a useful bound because the values grow rapidly and there are far too many reachable states.

A more natural constructive attempt is to use addition in the same spirit as the Euclidean algorithm. The problem is that the Euclidean algorithm wants subtraction, while every available operation only adds. For example, starting from `(1, 1000000000000000000)`, repeatedly adding the smaller value to the larger one would need an enormous number of additions if we tried to emulate subtraction directly.

The key observation is that multiplying both numbers by the same positive factor does not affect whether they are equal. We can freely reason about a normalized pair obtained by dividing out common factors of two. This lets us reinterpret the doubling operations as virtual halving operations.

Suppose the normalized pair is `(A, B)` and `A` is even. If we perform the real operation `B+=B`, the physical pair becomes `(A, 2B)`. If we conceptually divide both values by two, this is equivalent to `(A/2, B)`. Thus one legal operation gives us the same normalized state as halving `A`. Similarly, `A+=A` can be regarded as halving `B` in the normalized representation.

Once both normalized values are odd, suppose `A < B`. We perform `B+=A`, giving `(A, A+B)`. Since both operands were odd, `A+B` is even, so the next normalization can divide that larger value by two. The conceptual transition is

\[
(A,B)\rightarrow \left(A,\frac{A+B}{2}\right).
\]

This is the crucial reduction. If `B-A=C`, then after this transition the new difference is

\[
\frac{A+B}{2}-A=\frac{B-A}{2}=\frac C2.
\]

So when both values are odd, one addition followed by normalization roughly halves the difference. This is the same parity idea behind the binary Euclidean algorithm.

The resulting construction repeatedly removes factors of two, then adds the smaller odd value to the larger odd value. The normalized values steadily decrease until they both become one, at which point the actual values are equal because all transformations preserved the equality relation. A detailed operation-count argument gives a bound below 5000, with a tighter analysis giving 3969 operations for values up to \(10^{18}\). citeturn4view0

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---:|---:|---|
| Brute Force | \(O(4^{5000})\) sequence space | \(O(5000)\) per sequence | Too slow |
| Optimal | \(O(\log^2 10^{18})\) | \(O(\log^2 10^{18})\) | Accepted |

## Algorithm Walkthrough

1. Keep `a` and `b` as the normalized values used for reasoning. They do not represent the literal values stored by the judge after every operation. Instead, they represent an equivalent pair after removing common factors of two.

2. While `a` is even, append `B+=B` to the answer and replace `a` by `a // 2`. The real operation doubles `B`, and after dividing both values by two conceptually, the normalized state is exactly the same as halving `a`.

3. While `b` is even, append `A+=A` and replace `b` by `b // 2`. This is the symmetric transformation. The real operation doubles `A`, which is equivalent to halving `B` after removing the common factor of two.

4. If `a == b`, stop. The normalized values are equal, so the actual values represented by them are equal as well.

5. If both normalized values are now odd and `a < b`, append `B+=A` and replace `b` by `a + b`. The sum of two odd numbers is even, so the next iteration will be able to halve `b`.

6. If both normalized values are odd and `b < a`, append `A+=B` and replace `a` by `a + b`. Again, the updated larger value is even and will be halved at the beginning of the next iteration.

The reason the process makes progress is easiest to see from the difference. Assume `a < b` and both are odd. After the addition and subsequent halving, the difference becomes `(b-a)/2`. Thus the distance between the two normalized values is reduced by a factor of two whenever the addition step is needed. The parity-removal steps reduce the numbers themselves.

### Why it works

The invariant is that the normalized pair `(a, b)` represents the current actual pair up to multiplication of both values by the same positive power of two. Such a common scaling cannot change whether the two values are equal.

When `a` is even, `B+=B` changes the actual pair from `(A,B)` to `(A,2B)`. Dividing both by two gives `(A/2,B)`, so replacing normalized `a` by `a/2` is legitimate. The same argument applies when `b` is even.

When both normalized values are odd and unequal, adding the smaller to the larger is a legal operation. The resulting larger value is even, and the following normalization halves it. If the smaller value is `a`, the pair changes conceptually from `(a,b)` to `(a,(a+b)/2)`. The new difference is `(b-a)/2`, so the process cannot keep the same positive difference forever. Eventually the normalized values reach equality, and the invariant then tells us that the actual values are equal too.

The operation count is also small enough for the 5000 limit. One useful bound groups the process into phases where the product of the normalized values is reduced by at least a factor of two. Each such phase needs at most \(2\lfloor\log_2 B\rfloor+1\) operations, and because the initial product is below \(10^{36}\), summing these bounds gives fewer than 7200 operations. A sharper phase analysis gives the required bound of 3969, comfortably below 5000. citeturn6view0turn4view0

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b = map(int, input().split())
    ans = []

    while a != b:
        while a % 2 == 0:
            ans.append("B+=B")
            a //= 2

        while b % 2 == 0:
            ans.append("A+=A")
            b //= 2

        if a == b:
            break

        if a < b:
            ans.append("B+=A")
            b += a
        else:
            ans.append("A+=B")
            a += b

    print(len(ans))
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is read once because the problem has a single pair of values. The `ans` array stores the exact legal operations that must be printed.

The first `while` loop handles every factor of two in `a`. The operation appended to the answer is `B+=B`, not `A+=A`, because doubling the other actual value is what makes halving `A` valid after common normalization. This reversal is the easiest implementation detail to get wrong.

The second loop does the symmetric operation for `b`. Since the original values are at most \(10^{18}\), Python's integers are more than sufficient, and there is no overflow issue.

After both loops, if the normalized values are equal, the construction is finished. Otherwise both are odd. Exactly one is larger, so we add the smaller one to the larger one. The new larger value is even, which guarantees useful work in the next iteration.

The code does not explicitly simulate the actual values after every operation. Doing so is unnecessary and can make the reasoning confusing. The normalized values are enough because every halving step represents the removal of a common factor of two from the actual pair.

## Worked Examples

For the first example, the input is `2 3`.

| Step | Normalized `a` | Normalized `b` | Operation |
|---:|---:|---:|---|
| 0 | 2 | 3 | start |
| 1 | 1 | 3 | `B+=B` |
| 2 | 1 | 4 | `B+=A` |
| 3 | 1 | 2 | `A+=A` |
| 4 | 1 | 1 | `A+=A` |

The corresponding actual sequence is

```text
B+=B
B+=A
A+=A
A+=A
```

Starting from `(2,3)`, the actual values become `(2,6)`, `(2,8)`, `(4,8)`, and finally `(8,8)`. The normalized trace divides out common powers of two and reaches `(1,1)`.

For a second example, consider `4 6`.

| Step | Normalized `a` | Normalized `b` | Operation |
|---:|---:|---:|---|
| 0 | 4 | 6 | start |
| 1 | 2 | 6 | `B+=B` |
| 2 | 1 | 6 | `B+=B` |
| 3 | 1 | 3 | `A+=A` |
| 4 | 1 | 4 | `B+=A` |
| 5 | 1 | 2 | `A+=A` |
| 6 | 1 | 1 | `A+=A` |

The actual values follow `(4,6)`, `(4,12)`, `(4,24)`, `(8,24)`, `(8,32)`, `(16,32)`, `(32,32)`. The normalized values are allowed to shrink even though the actual values never decrease, because each normalization removes a common factor from both values.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---:|---|
| Time | \(O(\log^2 V)\) | There are logarithmically many parity reductions across phases, and each phase performs at most logarithmically many additions and reductions. |
| Space | \(O(\log^2 V)\) | The operation list contains fewer than 5000 strings. |

Here \(V=\max(A,B)\le10^{18}\). The construction has a proven operation bound below 5000, so it satisfies the special output restriction. Python only performs a few thousand integer operations and stores a few thousand short strings, which is easily within the 1 second and 1024 MB limits. citeturn6view0

## Test Cases

Because this is a special-judge construction problem, there is no single required output string. The test harness below checks that the produced sequence contains only legal operations, has at most 5000 operations, and actually makes the two original values equal.

```python
# helper: run solution on input string, return output string
import sys
 < b:
                ans.append("B+=A")
                b += a
            else:
                ans.append("A+=B")
                a += b

        print(len(ans))
        print("\n".join(ans))
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def run(inp: str) -> str:
    return solution(inp)

def validate(inp: str, out: str):
    a, b = map(int, inp.split())
    lines = out.strip().splitlines()

    assert lines
    n = int(lines[0])
    assert 0 <= n <= 5000
    assert len(lines) == n + 1

    allowed = {"A+=A", "A+=B", "B+=A", "B+=B"}

    for op in lines[1:]:
        assert op in allowed

        if op == "A+=A":
            a += a
        elif op == "A+=B":
            a += b
        elif op == "B+=A":
            b += a
        else:
            b += b

    assert a == b

# Provided sample
out = run("2 3")
validate("2 3", out)

# Minimum-size input
out = run("1 1")
validate("1 1", out)
assert out.strip() == "0"

# Even values with several factors of two
out = run("4 6")
validate("4 6", out)

# Boundary values
out = run("1 1000000000000000000")
validate("1 1000000000000000000", out)

# Maximum-size equal values
out = run("1000000000000000000 1000000000000000000")
validate("1000000000000000000 1000000000000000000", out)
assert out.strip() == "0"

# Close odd values, useful for catching parity mistakes
out = run("999999999999999999 1000000000000000000")
validate("999999999999999999 1000000000000000000", out)
```

| Test input | Expected output | What it validates |
|---|---|---|
| `2 3` | Any valid sequence, including the sample's 4 operations | Provided sample and basic odd/even transitions |
| `1 1` | `0` | Already-equal boundary case |
| `4 6` | Any valid sequence | Repeated halving of even normalized values |
| `1 1000000000000000000` | Any valid sequence with at most 5000 operations | Extremely unbalanced values |
| `1000000000000000000 1000000000000000000` | `0` | Maximum input values that are already equal |
| `999999999999999999 1000000000000000000` | Any valid sequence | Adjacent values and parity-sensitive transitions |

## Edge Cases

For `5 5`, the algorithm enters the outer loop condition `a != b`, sees that it is already false, and immediately prints zero operations. This is the only sensible construction because the target condition already holds.

For `4 6`, the normalized algorithm first removes the factors of two from `a`. The first `B+=B` represents `4 -> 2`, and the second represents `2 -> 1`. Then `A+=A` represents `6 -> 3`. The normalized state is now `(1,3)`. The operation `B+=A` changes it conceptually to `(1,4)`, after which two `A+=A` operations represent `4 -> 2 -> 1`. The normalized state reaches `(1,1)`, and the actual values have reached `(32,32)`.

For `1 1000000000000000000`, the large value contains many factors of two. The algorithm removes those factors using `A+=A` operations in the normalized representation, rather than performing \(10^{18}\) individual additions. Once the remaining odd parts are exposed, the addition step repeatedly halves the relevant difference. This is precisely the situation where a direct additive approach would fail but the parity-based construction stays within the operation limit.

For `999999999999999999 1000000000000000000`, the values are adjacent but have opposite parity. The first parity-removal stage immediately changes the even normalized value by a virtual halving. The algorithm never assumes that the original values are both odd, only that they are both odd after the parity-removal loops. This boundary condition prevents an incorrect application of the odd-plus-odd transition.

For `1 1`, the minimum possible input, the answer is again zero. For `1000000000000000000 1000000000000000000`, the maximum possible equal input behaves identically. The magnitude of the integers has no effect when equality is already present.
:::
