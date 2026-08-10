---
title: "CF 102396A - King's Inspection"
description: "We have three chests containing a, b, and c coins. In one second, we choose exactly two different chests and add one coin to each chosen chest. We need all three chests to end with the same number of coins, and we want the minimum number of seconds."
date: "2026-08-10T18:31:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "A"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 793
verified: true
draft: false
---

[CF 102396A - King's Inspection](https://codeforces.com/problemset/problem/102396/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three chests containing `a`, `b`, and `c` coins. In one second, we choose exactly two different chests and add one coin to each chosen chest. We need all three chests to end with the same number of coins, and we want the minimum number of seconds.

The input contains the three initial coin counts, each between `1` and `5 * 10^8`. Only three values are involved, so there is no need for a sophisticated data structure. The large upper bound is the real signal: a simulation that performs one operation per second can require close to one billion iterations, which is far beyond what a 1 second limit allows. A constant-time or logarithmic solution is the appropriate target.

The main edge case is when the largest chest already has the target value we might initially consider. For example, with

```
1
2
3
```

a careless approach might try to raise the first two chests to `3`. The deficits are `2` and `1`, while the third chest needs no coins. Since every operation affects two chests, the first two cannot independently be increased by different amounts while leaving the third unchanged. The correct answer is `3`, reaching `4, 4, 4`.

Another edge case is an already equal configuration:

```
2
2
2
```

The answer is `0`. A simulation that always performs at least one operation before checking equality would incorrectly return a positive value.

Repeated values also deserve attention. For

```
1
3
3
```

the answer is `4`, not `2`. Raising the first chest by `2` is not enough because every operation also raises one of the other two chests. The correct final value is `5`, requiring four operations.

## Approaches

A direct approach is to simulate the operations one second at a time. At every step we could choose a pair of chests that moves us toward equality, update their values, and stop once all three values match. This is correct if the pair is chosen appropriately, but the number of seconds itself can be enormous.

After sorting the values as `x <= y <= z`, the worst case under the constraints is `x = 1`, `y = z = 5 * 10^8`. The minimum answer is then

`y + z - 2x = 999,999,998`.

A simulation would consequently perform almost one billion iterations. Even though each iteration is constant time, that is far too much for the time limit.

The key observation is that an operation always adds exactly two coins in total. Instead of deciding which pair to choose at every second, we can reason about how many coins each chest must receive in the final state.

Suppose the final common value is `T`. The three chests need `T-x`, `T-y`, and `T-z` additional coins. Since every operation gives one coin to two chests, the required increases must be pairable. In particular, the largest required increase cannot exceed the sum of the other two increases.

For the smallest chest, the required increase is `T-x`, which is the largest of the three. Thus we need

`T - x <= (T - y) + (T - z)`.

Rearranging gives

`T >= y + z - x`.

So the smallest possible common value is exactly

`T = y + z - x`.

This target is always reachable. Its required increases become

`y + z - 2x`, `z - x`, and `y - x`.

The first is exactly the sum of the other two, so every coin given to the smallest chest can be paired with a coin given to one of the other chests.

Since each operation adds two coins, the total number of operations can also be obtained directly. The total number of required coins is

`(y + z - 2x) + (z - x) + (y - x) = 2(y + z - 2x)`.

Dividing by two gives the answer

`y + z - 2x`.

Thus the entire problem reduces to sorting three numbers and applying one formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow, up to 999,999,998 iterations |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three chest values and sort them so that `x <= y <= z`. Sorting three values takes constant time and lets us reason about the smallest, middle, and largest chest without handling separate cases for their original positions.
2. Consider a final common value `T`. The smallest chest needs `T - x` additional coins, while the other two need `T - y` and `T - z`.
3. Require the largest deficit to be no greater than the sum of the other two deficits. This is necessary because every coin added to the smallest chest must be accompanied by a coin added to one of the other chests. Hence

`T - x <= T - y + T - z`.
4. Rearrange the inequality to obtain `T >= y + z - x`. Choosing the smallest possible target gives `T = y + z - x`, which minimizes the amount of work.
5. Compute the required increase of the smallest chest:

`T - x = y + z - 2x`.

At this target, this increase is exactly the sum of the other two increases, so a valid sequence of pair operations exists.
6. Output `y + z - 2x`. This is already the number of operations because the total number of added coins is twice this value, and every operation adds exactly two coins.

The invariant behind the construction is that the required increase of the smallest chest equals the combined required increases of the other two chests. We can pair every required coin for the smallest chest with exactly one required coin for either other chest. No operation needs to touch the same chest twice, and all three deficits are exhausted simultaneously. Any smaller target would violate the pairing condition, so no solution can use fewer operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
b = int(input())
c = int(input())

x, y, z = sorted((a, b, c))

print(y + z - 2 * x)
```

The first three lines read the three chest sizes. There is no test-case count in the input, so the program processes exactly one instance.

Sorting gives `x <= y <= z`, matching the variables used in the derivation. The expression `y + z - 2 * x` is the number of operations directly, so there is no need to explicitly compute the final target or simulate individual operations.

Python integers have arbitrary precision, so the multiplication by `2` is safe even though the input values are as large as `5 * 10^8`. In a language with fixed-width integers, the same expression is still comfortably within 32-bit signed integer range here, but using a wider integer type would also be harmless.

## Worked Examples

For Sample 1, the input is `1, 2, 3`. After sorting, we have `x = 1`, `y = 2`, and `z = 3`.

| x | y | z | Target `y + z - x` | Answer `y + z - 2x` |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 3 |

The final common value is `4`. The three chests need `3`, `2`, and `1` additional coins respectively. Those increases can be paired as `(1,3)`, `(1,2)`, and `(1,2)`, giving exactly three operations and producing `4, 4, 4`.

For Sample 2, all three chests already contain two coins.

| x | y | z | Target `y + z - x` | Answer `y + z - 2x` |
| --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 2 | 0 |

The required increase of every chest is zero, so no operation is needed. The formula naturally handles this case without a special condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three values are sorted and one arithmetic expression is evaluated. |
| Space | O(1) | Only three integer variables are stored. |

The input values can be as large as `5 * 10^8`, but the algorithm never loops based on their magnitude. It performs a fixed amount of work, so the 1 second time limit and 512 MB memory limit are easily satisfied.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    a = int(input())
    b = int(input())
    c = int(input())

    x, y, z = sorted((a, b, c))
    print(y + z - 2 * x)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("1\n2\n3\n") == "3\n", "sample 1"
assert run("2\n2\n2\n") == "0\n", "sample 2"

# Minimum-size input
assert run("1\n1\n1\n") == "0\n", "minimum values and already equal"

# Maximum-size input
assert run("1\n500000000\n500000000\n") == "999999998\n", "maximum values"

# Repeated maximum values
assert run("1\n3\n3\n") == "4\n", "repeated maximum values"

# Repeated minimum values
assert run("2\n2\n5\n") == "3\n", "repeated minimum values"

# Values in unsorted order
assert run("5\n1\n3\n") == "6\n", "input order must not matter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Minimum values and already equal chests |
| `1 500000000 500000000` | `999999998` | Maximum answer and large-value arithmetic |
| `1 3 3` | `4` | Repeated maximum values |
| `2 2 5` | `3` | Repeated minimum values |
| `5 1 3` | `6` | Sorting is necessary because input order is arbitrary |

## Edge Cases

For the already equal case

```
2
2
2
```

sorting gives `x = y = z = 2`. The formula becomes `2 + 2 - 4 = 0`. No operation is performed, which is the minimum possible result.

For the case where the largest chest initially looks like it could be left untouched,

```
1
2
3
```

we get `x = 1`, `y = 2`, `z = 3`. Leaving the largest chest at `3` would require increases of `2, 1, 0`, which cannot be produced by pair operations. The smallest feasible target is instead `2 + 3 - 1 = 4`. The required increases are `3, 2, 1`, and the three units needed by the smallest chest can be paired with the two units needed by the middle chest and one unit needed by the largest chest. The formula returns `2 + 3 - 2 = 3`.

For repeated maximum values,

```
1
3
3
```

the sorted values are `1, 3, 3`. The target is `3 + 3 - 1 = 5`, so the deficits are `4, 2, 2`. Four operations are sufficient, pairing the first chest with each of the other chests twice. The formula gives `3 + 3 - 2 = 4`.

For the maximum-sized case,

```
1
500000000
500000000
```

the answer is `500000000 + 500000000 - 2 = 999999998`. A second-by-second simulation would need almost one billion iterations, while the formula computes the result immediately. This case demonstrates why the constant-time derivation is necessary rather than merely a cleaner implementation.

Edit

## Problem Understanding

We have three chests containing `a`, `b`, and `c` coins. In one second, we choose exactly two different chests and add one coin to each chosen chest. We need all three chests to end with the same number of coins, and we want the minimum number of seconds.

The input contains the three initial coin counts, each between `1` and `5 * 10^8`. Only three values are involved, so there is no need for a sophisticated data structure. The large upper bound is the real signal: a simulation that performs one operation per second can require close to one billion iterations, which is far beyond what a 1 second limit allows. A constant-time solution is the appropriate target.

The main edge case is when the largest chest already has the value we might initially consider as the target. For example, with `1, 2, 3`, simply raising the first two chests to `3` does not work because their required increases are different, while the third chest would need no increase. The correct answer is `3`, reaching `4, 4, 4`.

Another edge case is an already equal configuration such as `2, 2, 2`. The answer is `0`, so a simulation that performs an operation before checking equality would be incorrect.

Repeated values also matter. For `1, 3, 3`, the answer is `4`, not `2`. Every operation that increases the first chest must also increase one of the other two, so the target must be higher than the current maximum.

## Approaches

A direct approach is to simulate the operations one second at a time. At every step we could choose a pair of chests that moves us toward equality, update their values, and stop once all three values match. This is correct with a suitable choice of pairs, but the number of seconds can be enormous.

After sorting the values as `x <= y <= z`, the worst case under the constraints is `x = 1`, `y = z = 5 * 10^8`. The minimum answer is then `999,999,998`, so a simulation would perform almost one billion iterations.

The key observation is to reason about the required increases instead of the individual operations. Suppose the final common value is `T`. The three chests need `T-x`, `T-y`, and `T-z` additional coins. Since every operation adds one coin to two different chests, the largest required increase cannot exceed the sum of the other two.

The largest deficit belongs to the smallest chest, so

`T - x <= (T - y) + (T - z)`.

Rearranging gives

`T >= y + z - x`.

The smallest feasible target is consequently `T = y + z - x`. At that target, the required increases are `y + z - 2x`, `z - x`, and `y - x`. The first quantity is exactly the sum of the other two, so every required coin for the smallest chest can be paired with a required coin for one of the other chests.

The total number of added coins is therefore twice `y + z - 2x`, and every operation adds exactly two coins. The minimum number of operations is simply

`y + z - 2x`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow, up to 999,999,998 iterations |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three chest values and sort them so that `x <= y <= z`. Sorting three numbers takes constant time and lets us reason about the smallest, middle, and largest chest.
2. Assume the final common value is `T`. The three required increases are `T-x`, `T-y`, and `T-z`.
3. The smallest chest has the largest deficit. Every coin added to it must be accompanied by a coin added to one of the other two chests, so its deficit cannot exceed the sum of their deficits.
4. Solve `T-x <= T-y + T-z`, obtaining `T >= y + z - x`. The smallest possible target is therefore `T = y + z - x`.
5. At this target, the smallest chest needs `y + z - 2x` coins. The other two chests need `z-x` and `y-x`, whose sum is exactly `y + z - 2x`.
6. Since the largest deficit equals the sum of the other two, all required increases can be paired into valid operations. The number of operations is consequently `y + z - 2x`.

The invariant is that every operation contributes one unit to exactly two required deficits. At the chosen target, the largest deficit is exactly the combined size of the other two deficits, so the required increases can be completely paired. Any smaller target would make the largest deficit too large to pair, proving that the computed answer is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
b = int(input())
c = int(input())

x, y, z = sorted((a, b, c))

print(y + z - 2 * x)
```

The input consists of exactly three lines, so there is no test-case loop. Sorting puts the values into the order used by the mathematical derivation.

The final expression directly computes the number of operations, so the implementation does not need to construct the final state or simulate any operations. Python integers also handle all intermediate values safely.

## Worked Examples

For Sample 1, the values are `1, 2, 3`.

| x | y | z | Target | Answer |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 4 | 3 |

The required increases are `3, 2, 1`. They can be paired as three operations, producing `4, 4, 4`.

For Sample 2, the values are already equal.

| x | y | z | Target | Answer |
| --- | --- | --- | --- | --- |
| 2 | 2 | 2 | 2 | 0 |

Every deficit is zero, so the formula immediately returns zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting only three values and evaluating one formula |
| Space | O(1) | Only a constant number of integers are stored |

The algorithm never performs work proportional to the coin counts. Even when the answer is almost one billion, it performs only a fixed number of arithmetic operations, so it comfortably fits the 1 second and 512 MB limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    a = int(input())
    b = int(input())
    c = int(input())

    x, y, z = sorted((a, b, c))
    print(y + z - 2 * x)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

assert run("1\n2\n3\n") == "3\n", "sample 1"
assert run("2\n2\n2\n") == "0\n", "sample 2"

assert run("1\n1\n1\n") == "0\n", "minimum values"
assert run("1\n500000000\n500000000\n") == "999999998\n", "maximum values"
assert run("1\n3\n3\n") == "4\n", "repeated maximum values"
assert run("2\n2\n5\n") == "3\n", "repeated minimum values"
assert run("5\n1\n3\n") == "6\n", "unsorted input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Minimum values and equality |
| `1 500000000 500000000` | `999999998` | Maximum answer |
| `1 3 3` | `4` | Repeated maximum values |
| `2 2 5` | `3` | Repeated minimum values |
| `5 1 3` | `6` | Independence from input order |

## Edge Cases

For `2, 2, 2`, sorting gives `x = y = z = 2`, and the answer is `2 + 2 - 4 = 0`. The algorithm correctly recognizes that no operation is necessary.

For `1, 2, 3`, the smallest feasible target is `2 + 3 - 1 = 4`. The deficits are `3, 2, 1`, so the smallest chest can be paired with the middle chest twice and the largest chest once. The result is `3`.

For `1, 3, 3`, the target is `3 + 3 - 1 = 5`. The deficits are `4, 2, 2`, allowing four valid operations. The formula returns `3 + 3 - 2 = 4`.

For `1, 500000000, 500000000`, the result is `999999998`. A direct simulation would require that many iterations, while the optimal algorithm reaches the answer immediately through the closed-form expression.
