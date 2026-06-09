---
title: "CF 2078D - Scammy Game Ad"
description: "We have two lanes. Each lane starts with exactly one person. The level consists of n rounds. In each round there is a left gate and a right gate. A gate either adds a fixed number of people or multiplies the number of people currently in its lane."
date: "2026-06-09T03:42:15+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2078
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1008 (Div. 2)"
rating: 1800
weight: 2078
solve_time_s: 153
verified: true
draft: false
---

[CF 2078D - Scammy Game Ad](https://codeforces.com/problemset/problem/2078/D)

**Rating:** 1800  
**Tags:** dp, greedy, implementation  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two lanes. Each lane starts with exactly one person.

The level consists of `n` rounds. In each round there is a left gate and a right gate. A gate either adds a fixed number of people or multiplies the number of people currently in its lane.

The crucial detail is that gates do not directly modify lane populations. Instead, each gate produces some number of _new_ people.

If a gate is `+ a`, it creates exactly `a` new people.

If a gate is `x a`, and the lane currently contains `k` people, it creates `(a - 1) * k` new people.

After both gates of the round generate their new people, all newly created people are pooled together. We may distribute those new people between the two lanes however we like. Existing people cannot be moved, only the newly generated people are assignable.

The task is to maximize the total number of people in both lanes after all rounds.

The number of rounds is at most 30, which is tiny. The challenge is not the size of `n`, but the huge number of possible ways to distribute newly created people between lanes. A direct search over all allocations would explode combinatorially.

A subtle point is that a multiplication gate only depends on the number of people already present in its own lane before the round begins. People generated during the same round cannot increase that multiplication effect. Any solution that processes allocations and multiplications in the wrong order will overcount.

Consider:

```
1
1
x 3 x 3
```

Initially both lanes contain one person.

The two gates generate `2 + 2 = 4` new people. We may distribute those four people however we like, but the final total is always `2 + 4 = 6`.

A careless approach might think that putting generated people into a lane could immediately help the other multiplication in the same round, producing a larger value. That is not allowed.

Another easy mistake is assuming that balancing the lanes is always optimal.

Consider:

```
1
2
+ 100 + 0
x 3 + 0
```

All 100 generated people should be placed into the left lane because that lane will later be multiplied. Splitting them evenly loses value. The future rounds determine where current gains should be invested.

The core difficulty is deciding where each round's newly created people should go, taking all future multiplications into account.

## Approaches

A brute-force view is useful for understanding the structure.

Suppose we know the current populations `(l, r)`. A round generates some number `g` of new people. We may choose any split:

```
x people to the left
g - x people to the right
```

for every integer `0 ≤ x ≤ g`.

Recursively exploring all such choices is correct because it checks every possible allocation strategy. The problem is that `g` can become enormous after several multiplications. Even if we somehow bounded the number of choices per round, the branching factor would still grow exponentially with `n`.

The key observation is that the game is completely linear.

Imagine we are standing before some round `i`. Suppose the maximum achievable final answer from that point onward can be written as

```
A * l + B * r + C
```

where `l` and `r` are the current lane populations.

At the very end of the game, this is obviously true:

```
final = l + r
```

so initially

```
A = 1
B = 1
C = 0
```

Now consider one earlier round.

Let `g` be the total number of newly created people in that round. If we send `x` of them to the left lane, the future value becomes

```
A(l + x) + B(r + g - x) + C
```

which simplifies to

```
Al + Br + C + Bg + (A - B)x
```

The only variable is `x`.

If `A > B`, every extra person is more valuable in the left lane, so all newly generated people should go left.

If `B > A`, all newly generated people should go right.

If they are equal, any split is optimal.

This is the breakthrough. We never need to consider partial distributions. Every round's generated people are invested entirely into whichever lane has the larger future coefficient.

Once this is known, we can process rounds backwards and update the coefficients `(A, B, C)`.

Because multiplication gates contribute a value proportional to the current lane population, and addition gates contribute a constant, the linear form is preserved throughout the entire backward sweep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Define the value function for the suffix of rounds as:

```
F(l, r) = A * l + B * r + C
```

where `(A, B, C)` describe the optimal future payoff.
2. Start from the state after the last round.

At that point:

```
F(l, r) = l + r
```

so initialize:

```
A = 1
B = 1
C = 0
```
3. Process rounds from right to left.
4. Let:

```
m = max(A, B)
```

Any newly generated person should be assigned entirely to the lane with coefficient `m`, because that yields the largest future contribution.
5. Express each gate as a linear contribution.

For a gate `+ a`:

```
gain = a
```

which corresponds to:

```
0 * lane + a
```

For a gate `x a`:

```
gain = (a - 1) * lane
```

which corresponds to:

```
(a - 1) * lane + 0
```
6. Let the left gate contribute

```
cL * l + dL
```

and the right gate contribute

```
cR * r + dR
```

The total generated people are

```
g = cL * l + cR * r + dL + dR
```
7. Since every generated person is worth `m` in the future, add `m * g` to the current value function.

This produces:

```
A' = A + m * cL
B' = B + m * cR
C' = C + m * (dL + dR)
```
8. Replace `(A, B, C)` by `(A', B', C')` and continue.
9. After all rounds have been processed, the initial state is `(1, 1)`.

The answer is:

```
A + B + C
```

### Why it works

The invariant is that after processing a suffix of rounds, the optimal final answer from that point can always be represented as a linear function

```
A * l + B * r + C.
```

The base case is true because the final score is simply `l + r`.

Assume the invariant holds for round `i + 1`. During round `i`, the only decision is how to distribute the newly generated people. Since the future value is linear, each extra person contributes either `A` or `B` depending on the lane that receives it. Sending a person to the lane with the larger coefficient is always at least as good as any other choice. Thus every generated person has value `max(A, B)`.

Adding this value to the current linear function yields another linear function, preserving the invariant. By induction, the invariant holds for every round, including the start of the game. The resulting value at `(1, 1)` is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        gates = []

        for _ in range(n):
            op1, a1, op2, a2 = input().split()
            gates.append((op1, int(a1), op2, int(a2)))

        A = 1
        B = 1
        C = 0

        for op1, a1, op2, a2 in reversed(gates):
            m = max(A, B)

            if op1 == '+':
                cL, dL = 0, a1
            else:
                cL, dL = a1 - 1, 0

            if op2 == '+':
                cR, dR = 0, a2
            else:
                cR, dR = a2 - 1, 0

            A = A + m * cL
            B = B + m * cR
            C = C + m * (dL + dR)

        print(A + B + C)

solve()
```

The variables `A`, `B`, and `C` store the coefficients of the optimal value function for the suffix already processed.

For every round we first compute `m = max(A, B)`. This represents the future value of one newly generated person, because all generated people should be invested in the more profitable lane.

Each gate is converted into the form:

```
c * lane + d
```

which makes the update algebra straightforward.

The update must use the old value of `m`. Recomputing `m` after updating `A` or `B` would be incorrect because the allocation decision belongs to the current round, not a future one.

Python's integers automatically grow to arbitrary size, which is necessary because repeated multiplications can make the answer much larger than 64-bit limits.

## Worked Examples

### Sample 1

Input:

```
3
+ 4 x 2
x 3 x 3
+ 7 + 4
```

Backward processing:

| Round | A before | B before | C before | m | A after | B after | C after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| End | 1 | 1 | 0 | - | 1 | 1 | 0 |
| +7 +4 | 1 | 1 | 0 | 1 | 1 | 1 | 11 |
| x3 x3 | 1 | 1 | 11 | 1 | 3 | 3 | 11 |
| +4 x2 | 3 | 3 | 11 | 3 | 3 | 6 | 23 |

Final answer:

```
A + B + C = 3 + 6 + 23 = 32
```

This example shows that the value function remains linear throughout the backward sweep.

### Sample 4

Input:

```
5
x 3 x 3
x 2 x 2
+ 21 + 2
x 2 x 3
+ 41 x 3
```

Backward processing:

| Round | A before | B before | C before | m | A after | B after | C after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| End | 1 | 1 | 0 | - | 1 | 1 | 0 |
| +41 x3 | 1 | 1 | 0 | 1 | 1 | 3 | 41 |
| x2 x3 | 1 | 3 | 41 | 3 | 4 | 9 | 41 |
| +21 +2 | 4 | 9 | 41 | 9 | 4 | 9 | 248 |
| x2 x2 | 4 | 9 | 248 | 9 | 13 | 18 | 248 |
| x3 x3 | 13 | 18 | 248 | 18 | 49 | 54 | 248 |

Final answer:

```
49 + 54 + 248 = 351
```

This trace highlights the role of `m = max(A, B)`. Once the right lane becomes more valuable, all newly generated people are effectively treated as future right-lane investments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One backward pass over the rounds |
| Space | O(1) | Only a few coefficients are stored |

Each test case performs a constant amount of work per round. Since `n ≤ 30`, the running time is tiny. The memory usage remains constant regardless of input size, easily fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        gates = []

        for _ in range(n):
            op1, a1, op2, a2 = input().split()
            gates.append((op1, int(a1), op2, int(a2)))

        A = B = 1
        C = 0

        for op1, a1, op2, a2 in reversed(gates):
            m = max(A, B)

            if op1 == '+':
                cL, dL = 0, a1
            else:
                cL, dL = a1 - 1, 0

            if op2 == '+':
                cR, dR = 0, a2
            else:
                cR, dR = a2 - 1, 0

            A = A + m * cL
            B = B + m * cR
            C = C + m * (dL + dR)

        out.append(str(A + B + C))

    return "\n".join(out)

# provided sample
assert run(
"""4
3
+ 4 x 2
x 3 x 3
+ 7 + 4
4
+ 9 x 2
x 2 x 3
+ 9 + 10
x 2 + 1
4
x 2 + 1
+ 9 + 10
x 2 x 3
+ 9 x 2
5
x 3 x 3
x 2 x 2
+ 21 + 2
x 2 x 3
+ 41 x 3
"""
) == """32
98
144
351"""

# minimum size
assert run(
"""1
1
+ 1 + 1
"""
) == "4"

# single multiplication pair
assert run(
"""1
1
x 3 x 3
"""
) == "6"

# all additions
assert run(
"""1
2
+ 5 + 5
+ 5 + 5
"""
) == "22"

# multiplication only chain
assert run(
"""1
2
x 2 x 2
x 2 x 2
"""
) == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One round, `+1 +1` | 4 | Minimum input size |
| One round, `x3 x3` | 6 | Multiplication gain formula |
| Two rounds of additions | 22 | Constant contributions accumulate correctly |
| Two rounds of `x2 x2` | 8 | Repeated coefficient propagation |

## Edge Cases

Consider the smallest possible level:

```
1
1
+ 1 + 1
```

Backward initialization gives:

```
A = 1
B = 1
C = 0
```

The round contributes two constant people. Since `m = 1`:

```
C = 2
```

The answer becomes:

```
1 + 1 + 2 = 4
```

which matches the direct simulation.

Now consider a pure multiplication round:

```
1
1
x 3 x 3
```

The two gates generate:

```
2 * l + 2 * r
```

With `A = B = 1`, we have `m = 1`, so:

```
A = 3
B = 3
C = 0
```

The answer is:

```
3 + 3 = 6
```

This confirms that newly generated people are not allowed to influence multiplications within the same round.

Finally, consider a case where one lane becomes much more valuable:

```
1
2
+ 100 + 0
x 3 + 0
```

Backward processing yields:

```
After second round: A = 3, B = 1
```

Since `A > B`, every person generated in the first round should be placed into the left lane. The algorithm captures this automatically through

```
m = max(A, B) = 3.
```

A strategy that always balances the lanes would miss this opportunity and produce a smaller answer. The coefficient-based decision correctly identifies where future multiplications make an investment most profitable.
