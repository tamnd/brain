---
title: "CF 106113A - El Camino del Robot Humanoide"
description: "A humanoid robot starts at coordinate (0, 0) on a 2D plane and executes a sequence of movements. Each character in the command string represents one move: F moves the robot up, increasing y by 1. B moves the robot down, decreasing y by 1."
date: "2026-06-25T11:37:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106113
codeforces_index: "A"
codeforces_contest_name: "Coding Cup TecNM 2025"
rating: 0
weight: 106113
solve_time_s: 34
verified: true
draft: false
---

[CF 106113A - El Camino del Robot Humanoide](https://codeforces.com/problemset/problem/106113/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

A humanoid robot starts at coordinate `(0, 0)` on a 2D plane and executes a sequence of movements.

Each character in the command string represents one move:

`F` moves the robot up, increasing `y` by 1.

`B` moves the robot down, decreasing `y` by 1.

`L` moves the robot left, decreasing `x` by 1.

`R` moves the robot right, increasing `x` by 1.

After processing all commands, we only care about the final horizontal position. If the final `x` coordinate is negative, we print `"Izquierda"`. If it is positive, we print `"Derecha"`. If it is exactly zero, we print `"Linea Recta"`.

The input size is tiny. The number of moves is at most 1000, so even a straightforward simulation is more than fast enough. A single pass through the string performs only 1000 operations in the worst case.

The main source of mistakes is paying attention to the wrong coordinate. Vertical moves change only `y`, but the output depends exclusively on `x`.

Consider the input:

```
5
FFFFF
```

The robot ends at `(0, 5)`. The correct output is:

```
Linea Recta
```

A careless solution that tries to classify the final position using both coordinates could incorrectly conclude that the robot moved somewhere and should not be considered on the straight line.

Another easy mistake is forgetting that left and right movements can cancel each other.

```
4
LRLR
```

The final horizontal position is `0`, so the answer is:

```
Linea Recta
```

Simply checking whether an `L` or `R` appears in the string would give the wrong result.

A third edge case occurs when there are no horizontal moves at all.

```
3
FBF
```

The robot finishes at `x = 0`, regardless of the vertical displacement. The answer remains:

```
Linea Recta
```

## Approaches

The most direct solution is to simulate the robot exactly as described. Start with `x = 0` and `y = 0`, process every character, and update the coordinates according to the movement rules. After all commands have been processed, inspect the final value of `x` and print the corresponding word.

Since there are at most 1000 commands, this simulation performs only 1000 updates. That is effectively instantaneous.

An even more compact observation is that the final answer depends only on the difference between the number of `R` commands and the number of `L` commands. Vertical moves never affect the decision. We could count left and right moves directly instead of maintaining both coordinates.

Both viewpoints lead to the same linear-time solution. The simulation version mirrors the problem statement exactly and is easy to verify.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(1) | Accepted |
| Count Left/Right Moves | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `N`, the number of commands.
2. Read the command string.
3. Initialize `x = 0`.
4. Process each character in the string.

If the character is `L`, decrement `x`.

If the character is `R`, increment `x`.

Characters `F` and `B` do not affect the horizontal position, so they can be ignored.
5. After processing the entire string, inspect `x`.
6. If `x < 0`, print `"Izquierda"`.
7. If `x > 0`, print `"Derecha"`.
8. Otherwise print `"Linea Recta"`.

### Why it works

The horizontal coordinate starts at zero. Every `L` decreases it by one, and every `R` increases it by one. No other command changes `x`. After all commands are processed, the final value of `x` is exactly the robot's horizontal displacement from the origin. The statement defines the output solely from the sign of this value, so checking whether `x` is negative, positive, or zero produces the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

x = 0

for c in s:
    if c == 'L':
        x -= 1
    elif c == 'R':
        x += 1

if x < 0:
    print("Izquierda")
elif x > 0:
    print("Derecha")
else:
    print("Linea Recta")
```

The implementation keeps only the horizontal coordinate because the vertical coordinate never affects the output.

Inside the loop, only `L` and `R` modify the state. Ignoring `F` and `B` is completely safe because they change only `y`.

The final conditional follows the exact order required by the statement. Checking negative and positive cases first leaves the remaining possibility as `x = 0`, which corresponds to `"Linea Recta"`.

## Worked Examples

### Example 1

Input:

```
5
FFLRF
```

| Step | Command | x |
| --- | --- | --- |
| Start | - | 0 |
| 1 | F | 0 |
| 2 | F | 0 |
| 3 | L | -1 |
| 4 | R | 0 |
| 5 | F | 0 |

Final `x = 0`.

Output:

```
Linea Recta
```

This example shows that vertical movements do not matter. Only the left and right moves contribute to the answer.

### Example 2

Input:

```
8
FRFRLLBL
```

| Step | Command | x |
| --- | --- | --- |
| Start | - | 0 |
| 1 | F | 0 |
| 2 | R | 1 |
| 3 | F | 1 |
| 4 | R | 2 |
| 5 | L | 1 |
| 6 | L | 0 |
| 7 | B | 0 |
| 8 | L | -1 |

Final `x = -1`.

Output:

```
Izquierda
```

This trace demonstrates that the answer depends on the net horizontal displacement rather than the total number of moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass through the command string |
| Space | O(1) | Only a few integer variables are stored |

With `N ≤ 1000`, a linear scan is trivial to execute within the limits. The memory usage remains constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    s = input().strip()

    x = 0
    for c in s:
        if c == 'L':
            x -= 1
        elif c == 'R':
            x += 1

    if x < 0:
        return "Izquierda\n"
    elif x > 0:
        return "Derecha\n"
    else:
        return "Linea Recta\n"

# provided samples
assert run("5\nFFLRF\n") == "Linea Recta\n", "sample 1"
assert run("4\nFFRR\n") == "Derecha\n", "sample 2"
assert run("8\nFRFRLLBL\n") == "Izquierda\n", "sample 3"

# custom cases
assert run("1\nL\n") == "Izquierda\n", "single left move"
assert run("1\nR\n") == "Derecha\n", "single right move"
assert run("4\nLRLR\n") == "Linea Recta\n", "cancelling moves"
assert run("3\nFBF\n") == "Linea Recta\n", "only vertical moves"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / L` | `Izquierda` | Minimum size, negative displacement |
| `1 / R` | `Derecha` | Minimum size, positive displacement |
| `LRLR` | `Linea Recta` | Left and right moves cancel exactly |
| `FBF` | `Linea Recta` | Vertical moves must not affect the answer |

## Edge Cases

Consider the case where all moves are vertical:

```
3
FBF
```

The algorithm starts with `x = 0`. Each character is either `F` or `B`, so `x` never changes. After the loop, `x` remains zero and the algorithm prints:

```
Linea Recta
```

This is correct because the robot never moved left or right.

Now consider cancelling horizontal moves:

```
4
LRLR
```

The updates are:

`0 → -1 → 0 → -1 → 0`

The final value is zero, so the output is:

```
Linea Recta
```

Even though horizontal movement occurred, the net displacement is zero, which is exactly what the problem asks us to evaluate.

Finally, consider a strongly negative displacement:

```
5
LLLLF
```

The horizontal coordinate evolves as:

`0 → -1 → -2 → -3 → -4`

The final `F` does not change `x`. Since `x = -4`, the algorithm prints:

```
Izquierda
```

This confirms that vertical moves after horizontal moves do not alter the classification.
