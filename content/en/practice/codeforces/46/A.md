---
title: "CF 46A - Ball Game"
description: "The children stand in a circle numbered from 1 to n. Child 1 starts with the ball. The first throw moves the ball forward by 1 position, the second throw moves it forward by 2 positions, the third throw by 3 positions, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 46
codeforces_index: "A"
codeforces_contest_name: "School Personal Contest #2 (Winter Computer School 2010/11) - Codeforces Beta Round 43 (ACM-ICPC Rules)"
rating: 800
weight: 46
solve_time_s: 83
verified: true
draft: false
---

[CF 46A - Ball Game](https://codeforces.com/problemset/problem/46/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The children stand in a circle numbered from `1` to `n`. Child `1` starts with the ball. The first throw moves the ball forward by `1` position, the second throw moves it forward by `2` positions, the third throw by `3` positions, and so on. After exactly `n - 1` throws, we must print which child receives the ball after each throw.

The movement wraps around the circle. If we move past child `n`, we continue again from child `1`. This is classic circular movement, so modular arithmetic is the natural tool here.

The constraint is very small, `n ≤ 100`. Even an inefficient simulation would easily fit within the time limit. A quadratic solution would perform around `10^4` operations, which is tiny. The challenge is not performance, it is handling the circular indexing correctly.

The most common mistake is mixing 0-based and 1-based numbering. The children are numbered starting from `1`, but modular arithmetic is usually easier with 0-based indices.

Consider `n = 5`.

The sequence of moves is:

- Start at `1`
- Move `1` step → `2`
- Move `2` steps → `4`
- Move `3` steps → `2`
- Move `4` steps → `1`

The correct output is:

```
2 4 2 1
```

A careless implementation might compute:

```
pos = (pos + step) % n
```

while keeping `pos` in 1-based form. That produces invalid child `0` when the position wraps around.

Another easy mistake is misunderstanding the distance. On the `k`-th throw, we move exactly `k` positions forward, not `k + 1`.

For example, with `n = 4`:

```
Start at 1
Throw 1: move 1 → 2
Throw 2: move 2 → 4
Throw 3: move 3 → 3
```

Correct output:

```
2 4 3
```

If someone increments the step too early, they would incorrectly move by `2, 3, 4`.

## Approaches

The direct brute-force simulation follows the game literally. We store the current child and repeatedly move forward by the required number of positions. Since the children form a circle, after each move we wrap around using modulo arithmetic.

One way to implement this is to physically simulate every step of movement. For the `k`-th throw, we advance one position at a time exactly `k` times. The total number of single-step movements becomes:

```
1 + 2 + 3 + ... + (n - 1)
```

which is `O(n²)`.

With `n = 100`, this still runs instantly, so even the naive simulation is accepted.

The cleaner solution comes from observing that we never actually need intermediate positions. We only care about the final child after each throw. Circular movement can be represented directly with modular arithmetic.

If the current position is `pos` and the next throw length is `step`, then:

```
new_position = (pos + step) % n
```

when using 0-based indexing.

This reduces each throw to constant time, giving an `O(n)` solution.

The brute-force works because the constraints are tiny, but modular arithmetic captures the structure of circular movement directly and produces a much simpler implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of children `n`.
2. Store the current position as `0`, representing child `1` in 0-based indexing.

Using 0-based indices makes modulo operations straightforward because positions naturally stay in the range `[0, n - 1]`.
3. Iterate `step` from `1` to `n - 1`.

The `step` value directly matches the throw number and the number of positions moved.
4. Update the current position:

```
pos = (pos + step) % n
```

The modulo operation wraps the movement around the circle whenever we pass the last child.
5. Convert the position back to 1-based numbering by printing `pos + 1`.
6. Continue until all `n - 1` throws are processed.

### Why it works

After every iteration, `pos` stores the current holder of the ball in 0-based indexing. On the `k`-th throw, the rules require moving exactly `k` positions clockwise. Adding `k` to the current position performs this movement, and modulo `n` correctly handles wrapping around the circle. Since each update exactly matches one throw in the game, the produced sequence is exactly the sequence of children receiving the ball.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

pos = 0
ans = []

for step in range(1, n):
    pos = (pos + step) % n
    ans.append(str(pos + 1))

print(" ".join(ans))
```

The variable `pos` stores the current child using 0-based indexing. Child `1` is represented as `0`, child `2` as `1`, and so on.

For each throw number `step`, we move forward by exactly that many positions. The expression:

```
(pos + step) % n
```

keeps the position inside the valid circular range.

The output must use the original 1-based numbering, so we print `pos + 1`.

A subtle detail is the order of operations. We first update the position, then print it. Printing before the update would incorrectly include the child who throws the ball rather than the child who receives it.

Another important detail is starting the loop from `1`. The first throw moves by one position, not zero.

## Worked Examples

### Example 1

Input:

```
10
```

| Throw | Step Size | Previous Position | New Position (0-based) | Printed Child |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 2 |
| 2 | 2 | 1 | 3 | 4 |
| 3 | 3 | 3 | 6 | 7 |
| 4 | 4 | 6 | 0 | 1 |
| 5 | 5 | 0 | 5 | 6 |
| 6 | 6 | 5 | 1 | 2 |
| 7 | 7 | 1 | 8 | 9 |
| 8 | 8 | 8 | 6 | 7 |
| 9 | 9 | 6 | 5 | 6 |

Output:

```
2 4 7 1 6 2 9 7 6
```

This trace shows how modulo arithmetic naturally handles wraparound. On throw `4`, position `6 + 4 = 10`, and `10 % 10 = 0`, which correctly returns to child `1`.

### Example 2

Input:

```
5
```

| Throw | Step Size | Previous Position | New Position (0-based) | Printed Child |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 2 |
| 2 | 2 | 1 | 3 | 4 |
| 3 | 3 | 3 | 1 | 2 |
| 4 | 4 | 1 | 0 | 1 |

Output:

```
2 4 2 1
```

This example exercises repeated wraparounds. The third throw moves from position `3` by `3` more steps, producing `6 % 5 = 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One constant-time update for each of the `n - 1` throws |
| Space | O(1) | Only a few variables are stored apart from the output list |

With `n ≤ 100`, the algorithm easily fits within the limits. Even a quadratic solution would pass, but the modular arithmetic approach is both cleaner and asymptotically optimal.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    pos = 0
    ans = []

    for step in range(1, n):
        pos = (pos + step) % n
        ans.append(str(pos + 1))

    print(" ".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("10\n") == "2 4 7 1 6 2 9 7 6", "sample 1"

# minimum size
assert run("2\n") == "2", "minimum n"

# small wraparound case
assert run("5\n") == "2 4 2 1", "multiple wraparounds"

# off-by-one check
assert run("4\n") == "2 4 3", "correct step sizes"

# larger case
assert run("7\n") == "2 4 7 4 2 1", "general circular movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `2` | Smallest valid input |
| `5` | `2 4 2 1` | Repeated wraparound behavior |
| `4` | `2 4 3` | Correct step counting and indexing |
| `7` | `2 4 7 4 2 1` | General circular simulation |

## Edge Cases

Consider the smallest possible input:

```
2
```

There is only one throw.

The algorithm starts with:

```
pos = 0
```

For `step = 1`:

```
pos = (0 + 1) % 2 = 1
```

We print `1 + 1 = 2`.

Output:

```
2
```

This confirms that the loop boundaries are correct and that we perform exactly `n - 1` throws.

Now consider a case with immediate wraparound:

```
5
```

During the fourth throw, the current position is:

```
pos = 1
```

The move is:

```
(1 + 4) % 5 = 0
```

Position `0` corresponds to child `1`.

Output at this step:

```
1
```

This verifies that modulo arithmetic correctly returns to the beginning of the circle.

Finally, consider a case that catches indexing mistakes:

```
4
```

Correct sequence:

```
2 4 3
```

If someone used 1-based indexing directly inside the modulo expression, they could accidentally produce child `0`. Our implementation avoids this completely by storing positions internally as 0-based values and converting back only when printing.
