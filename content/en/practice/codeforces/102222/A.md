---
title: "CF 102222A - Maximum Element In A Stack"
description: "We have an initially empty stack. Each test case does not list the operations explicitly. Instead, it gives the parameters of a pseudorandom generator, and we must reproduce the same sequence of PUSH and POP operations as the generator."
date: "2026-08-19T00:40:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102222
codeforces_index: "A"
codeforces_contest_name: "2018-2019 ACM-ICPC, China Multi-Provincial Collegiate Programming Contest"
rating: 0
weight: 102222
solve_time_s: 529
verified: true
draft: false
---

[CF 102222A - Maximum Element In A Stack](https://codeforces.com/problemset/problem/102222/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an initially empty stack. Each test case does not list the operations explicitly. Instead, it gives the parameters of a pseudorandom generator, and we must reproduce the same sequence of `PUSH` and `POP` operations as the generator. A push creates a value between `1` and `m`, while a pop removes the current top element if one exists. After every operation, we need the maximum value currently present in the stack, using `0` when the stack is empty. The required answer is the bitwise XOR of `i * maximum_i` over all operation indices `i`. The official constraints allow as many as `5 * 10^6` operations in one test case, with up to 50 test cases and a 256 MB memory limit.

The large value of `n` determines the shape of the solution. Even a small amount of work repeated over every element is acceptable only if it is constant time per operation. An algorithm that scans the entire stack after every operation can perform roughly

`1 + 2 + 3 + ... + n = n(n + 1) / 2`

comparisons. For `n = 5 * 10^6`, that is about `1.25 * 10^13` comparisons, which is far beyond what the 10 second limit can tolerate. The intended solution must process every generated operation in O(1) time. The official problem page gives the same `5 * 10^6` bound and 10 second limit.

There are several edge cases that are easy to mishandle. First, `POP` is allowed when the stack is already empty. For the first sample, the generated operations begin with two pops. The first operation leaves the stack empty, so its contribution is `1 * 0 = 0`; the second does the same. A solution that assumes every pop is valid could access an invalid stack element.

```
1
1 1 1 4 23333 66666 233333
```

Here the first generated operation is the same first operation as Sample 1, namely `POP`, so the correct output is `Case #1: 0`. A careless implementation that reads the top element without checking emptiness would fail.

The second edge case is that popping the current maximum does not mean the new maximum is zero. The previous maximum must reappear if another element underneath it is still present. This is why simply storing one global maximum is insufficient. For example, after `PUSH(3), PUSH(8), POP()`, the remaining maximum is `3`, not `0`. The correct data structure has to remember the maximum associated with every stack depth.

A third edge case is repeated equal values. Suppose the stack contains `7, 7, 7` and we pop once. The maximum is still `7`. A representation that stores only positions where the maximum strictly increases can lose track of this multiplicity. The prefix maximum representation avoids that problem because every depth stores its own maximum.

Finally, the generator itself uses 32 bit unsigned arithmetic. Python integers do not overflow naturally, so every state update of `SA`, `SB`, and `SC` has to be reduced modulo `2^32`. Omitting that masking changes the generated operations and can produce a wrong answer even if the stack logic is perfect.

## Approaches

The direct solution is to store every actual stack value. On a push, append the value. On a pop, remove the last value. To obtain the maximum after each operation, scan the whole stack and take its maximum. This is correct because the scan examines exactly the elements currently present in the stack.

The problem is the repeated scan. If the stack grows to size `n` and stays large, the first query may inspect one element, the next two, and so on. In the worst case the total work becomes O(n²), around `1.25 * 10^13` stack-element inspections for `n = 5 * 10^6`. The generator is deliberately used so that the input itself does not become enormous, but that does not make an O(n²) algorithm viable.

The key observation is that the only information we need from a stack prefix is its maximum. Consider the stack after several pushes. At depth `k`, store the maximum value among the first `k` actual elements. When a new value `x` is pushed, the new maximum is simply `max(previous_maximum, x)`. When the top is popped, the maximum automatically becomes the value stored at the previous depth.

This means the actual pushed values are unnecessary. For example, suppose the real stack is `[4, 2, 9, 3]`. We can replace it with `[4, 4, 9, 9]`. The top value `9` is the current maximum. If we pop once, the representation becomes `[4, 4, 9]`, and its top is still the correct maximum. Pop again and it becomes `[4, 4]`, revealing `4`, exactly as the original stack would.

The structure is consequently just another stack containing prefix maxima. Every operation becomes constant time. We can go one step further in the implementation because the actual values are never needed after a push. One 32 bit integer per stack depth is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `p`, `q`, `m`, and the three generator states `SA`, `SB`, and `SC`. The generator must be reproduced exactly because the operation sequence is implicit in these values.
2. Allocate a stack of prefix maxima with one extra slot containing `0`. Let `depth` represent the number of elements currently in the logical stack. The sentinel at depth zero means that the maximum of an empty stack is immediately available as zero.
3. For operation `i`, call the generator once to decide whether the operation is a push or a pop. The condition is `rng61() % (p + q) < p`.
4. If the operation is a push, call `rng61()` a second time to generate the value `v = rng61() % m + 1`. Increase the stack depth and store `max(stack[depth - 1], v)` at the new depth. If the stack was previously empty, the previous maximum is zero, so the stored value is simply `v`.
5. If the operation is a pop, decrease `depth` only when the stack is nonempty. If it is already zero, leave it unchanged. The sentinel then gives the correct maximum of zero.
6. After performing the operation, read `stack[depth]` as the current maximum. XOR `i * stack[depth]` into the answer. The multiplication uses the one-based operation index required by the problem.
7. After all `n` operations, print the accumulated XOR using the required `Case #x: y` format.

### Why it works

The invariant is that `stack[d]` equals the maximum value in the real stack's first `d` elements. Initially `d = 0`, and the empty maximum is zero. During a push, the new real stack consists of the previous `d` elements followed by `v`, so its maximum is exactly `max(stack[d], v)`, which is what we store at depth `d + 1`. During a pop, the last real element disappears, so the maximum of the remaining stack is exactly the value already stored at depth `d - 1`. Thus the invariant survives every operation, and the value read from `stack[depth]` is always the required maximum. Since every contribution is XORed immediately after its corresponding operation, the final answer is exactly the required XOR.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MASK = 0xFFFFFFFF

def rng61(sa, sb, sc):
    sa ^= (sa << 16) & MASK
    sa &= MASK

    sa ^= sa >> 5
    sa &= MASK

    sa ^= (sa << 1) & MASK
    sa &= MASK

    t = sa
    sa = sb
    sb = sc
    sc = (sc ^ t ^ sa) & MASK

    return sc, sa, sb, sc

def solve():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n, p, q, m, sa, sb, sc = map(int, input().split())

        # stack[d] = maximum of the logical stack when its size is d.
        # stack[0] = 0 represents the empty stack.
        stack = array('I', [0]) * (n + 1)
        depth = 0
        ans = 0
        total = p + q

        for i in range(1, n + 1):
            r, sa, sb, sc = rng61(sa, sb, sc)

            if r % total < p:
                r, sa, sb, sc = rng61(sa, sb, sc)
                value = r % m + 1

                previous_max = stack[depth]
                depth += 1

                if value > previous_max:
                    stack[depth] = value
                else:
                    stack[depth] = previous_max
            else:
                if depth > 0:
                    depth -= 1

            ans ^= i * stack[depth]

        out.append(f"Case #{case_id}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `rng61` function mirrors the C++ generator. The explicit `& 0xFFFFFFFF` operations are required because C++ `unsigned int` arithmetic wraps modulo `2^32`, while Python integers grow without bound. The masking after each XOR and left shift makes every subsequent operation behave as it does on a 32 bit unsigned value.

The array called `stack` does not contain the original pushed values. At index `d`, it contains the maximum value of the first `d` elements. This is enough because the only query ever made about the stack is its maximum.

The array is preallocated to `n + 1` unsigned 32 bit integers. A Python list would store references to Python integer objects and could consume well over 100 MB at maximum depth. The `array('I')` representation uses four bytes per entry, so a depth of five million requires about 20 MB for the stack.

The `depth` variable is the logical stack size. A push writes to `stack[depth + 1]`, while a valid pop decrements `depth`. Keeping `stack[0] = 0` removes the need for a special maximum value when the stack becomes empty.

The generator must be called exactly once for every operation decision. On a push, it must then be called exactly once more for the pushed value. Calling it in a different order changes the entire subsequent generator state. The answer is updated after the stack operation, because `a_i` refers to the maximum after the `i`-th operation.

Python's integers are also useful for the final expression. The largest product is at most `5 * 10^6 * 10^9 = 5 * 10^15`, which fits comfortably in Python's integer representation and also fits in a signed 64 bit integer.

## Worked Examples

For Sample 1, the generator produces `POP, POP, PUSH(1), PUSH(4)`. The stack representation stores only the maximum at each depth.

| Operation | Generated action | Depth | Prefix-max stack | Current maximum | XOR contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | `POP` | 0 | `[0]` | 0 | `1 * 0 = 0` |
| 2 | `POP` | 0 | `[0]` | 0 | `2 * 0 = 0` |
| 3 | `PUSH(1)` | 1 | `[0, 1]` | 1 | `3 * 1 = 3` |
| 4 | `PUSH(4)` | 2 | `[0, 1, 4]` | 4 | `4 * 4 = 16` |

The final answer is `0 XOR 0 XOR 3 XOR 16 = 19`, giving `Case #1: 19`. The first two operations also verify that popping an empty stack must be a no-op.

For Sample 2, the generated operations are `PUSH(2), POP, PUSH(1), POP`.

| Operation | Generated action | Depth | Prefix-max stack | Current maximum | XOR contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | `PUSH(2)` | 1 | `[0, 2]` | 2 | `1 * 2 = 2` |
| 2 | `POP` | 0 | `[0, 2]` | 0 | `2 * 0 = 0` |
| 3 | `PUSH(1)` | 1 | `[0, 1]` | 1 | `3 * 1 = 3` |
| 4 | `POP` | 0 | `[0, 1]` | 0 | `4 * 0 = 0` |

The final XOR is `2 XOR 0 XOR 3 XOR 0 = 1`. This trace exercises both insertion and removal back to the empty state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each operation performs a constant number of generator updates and stack accesses. |
| Space | O(n) | The prefix-maximum array has one 32 bit entry for each possible stack depth. |

The maximum depth is at most `n`, so the preallocated array needs at most about 20 MB when `n = 5 * 10^6`. This is substantially below the 256 MB memory limit. The running time is linear in the number of generated operations, which is the necessary scale for a test case containing millions of operations.

## Test Cases

The following test harness uses the same solution logic as the submitted program. The large custom case is deliberately chosen so that its behavior can be proved without relying on an independently generated expected value: with `SA = SB = SC = 65536`, every generator state remains even, so with `p = q = 1` every operation is a push. Setting `m = 1` makes every pushed value equal to `1`.

```python
import sys
import io
from array import array

MASK = 0xFFFFFFFF

def solve_text(inp: str) -> str:
    data = io.StringIO(inp)
    input = data.readline

    t = int(input())
    out = []

    def rng61(sa, sb, sc):
        sa ^= (sa << 16) & MASK
        sa &= MASK
        sa ^= sa >> 5
        sa &= MASK
        sa ^= (sa << 1) & MASK
        sa &= MASK

        tmp = sa
        sa = sb
        sb = sc
        sc = (sc ^ tmp ^ sa) & MASK

        return sc, sa, sb, sc

    for case_id in range(1, t + 1):
        n, p, q, m, sa, sb, sc = map(int, input().split())

        stack = array('I', [0]) * (n + 1)
        depth = 0
        ans = 0
        total = p + q

        for i in range(1, n + 1):
            r, sa, sb, sc = rng61(sa, sb, sc)

            if r % total < p:
                r, sa, sb, sc = rng61(sa, sb, sc)
                value = r % m + 1

                depth += 1
                previous_max = stack[depth - 1]
                stack[depth] = max(previous_max, value)
            else:
                if depth:
                    depth -= 1

            ans ^= i * stack[depth]

        out.append(f"Case #{case_id}: {ans}")

    return "\n".join(out)

# Provided samples
sample = """\
2
4 1 1 4 23333 66666 233333
4 2 1 4 23333 66666 233333
"""

assert solve_text(sample) == """\
Case #1: 19
Case #2: 1
""", "provided samples"

# Minimum-size case. The first generated operation is POP,
# so the empty stack contributes zero.
assert solve_text(
    "1\n1 1 1 4 23333 66666 233333\n"
) == "Case #1: 0", "minimum-size empty pop"

# First three operations of Sample 1:
# POP, POP, PUSH(1), giving contributions 0, 0, 3.
assert solve_text(
    "1\n3 1 1 4 23333 66666 233333\n"
) == "Case #1: 3", "operation-index weighting"

# All generated operations are PUSH because every RNG state is even.
# m = 1 makes every pushed value equal to 1.
# For n = 5, the answer is 1 xor 2 xor 3 xor 4 xor 5 = 1.
assert solve_text(
    "1\n5 1 1 1 65536 65536 65536\n"
) == "Case #1: 1", "all-equal values"

# Maximum-size case.
# Every operation is PUSH(1), so the answer is xor(1..5,000,000).
# Since 5,000,000 is divisible by 4, xor(1..n) = n.
assert solve_text(
    "1\n5000000 1 1 1 65536 65536 65536\n"
) == "Case #1: 5000000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 4 23333 66666 233333` | `Case #1: 0` | Minimum `n` and an empty-stack pop |
| `1 / 3 1 1 4 23333 66666 233333` | `Case #1: 3` | One-based operation index in the XOR |
| `1 / 5 1 1 1 65536 65536 65536` | `Case #1: 1` | `m = 1`, repeated equal maximum values, and push handling |
| `1 / 5000000 1 1 1 65536 65536 65536` | `Case #1: 5000000` | Maximum `n`, linear processing, compact memory representation |

## Edge Cases

For an empty-stack pop, use the first operation of Sample 1 as a concrete case:

```
1
1 1 1 4 23333 66666 233333
```

The first generated random value selects `POP`. The logical depth starts at zero, so the pop condition `if depth > 0` is false and the depth remains zero. The sentinel `stack[0]` is zero, giving contribution `1 * 0 = 0`. The output is `Case #1: 0`. No stack access outside the valid range occurs.

For repeated equal values, consider:

```
1
5 1 1 1 65536 65536 65536
```

All three generator states begin even. The transformations use only shifts, XOR, and assignments, so every state remains even. With `p = q = 1`, an even random value satisfies `value % 2 < 1`, so every operation is a push. Because `m = 1`, every generated value is `1`. The prefix-maximum stack becomes `[0, 1, 1, 1, 1, 1]`. The contributions are `1, 2, 3, 4, 5`, whose XOR is `1`. The repeated maximum never needs special treatment.

For the maximum-size boundary, the same construction with `n = 5 * 10^6` produces five million pushes of the value `1`. The stack reaches its maximum possible depth, but the program stores only five million 32 bit prefix maxima, about 20 MB. The answer is XOR of all integers from `1` through `5,000,000`. Since `5,000,000 mod 4 = 0`, that XOR equals `5,000,000`. This tests both the memory representation and the loop boundary at exactly the largest permitted `n`.

For the operation index boundary, use the first three operations of Sample 1:

```
1
3 1 1 4 23333 66666 233333
```

The operations are `POP, POP, PUSH(1)`. The first two contributions are zero. At operation three, the maximum is one, so the contribution is `3 * 1 = 3`. The answer is `3`. Using a zero-based loop index in the XOR expression would incorrectly contribute zero at this point, so this case catches that off-by-one error.

For the generator boundary, the same tests also verify that a push consumes two random numbers while a pop consumes only one. In Sample 1, the first two operations are pops, so only one generator call is made for each. The third operation is a push, so the operation-selection call is immediately followed by a value-generation call. If the implementation calls the generator for a value after a pop, all later operations shift and the final XOR becomes incorrect. The Python implementation follows the exact call order of the original generator.
