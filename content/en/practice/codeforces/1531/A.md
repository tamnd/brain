---
title: "CF 1531A - \u0417\u0438\u043d\u0433\u0435\u0440 | color"
description: "We need to simulate the behavior of a chatbot that controls the illumination color of the Singer House dome. Initially, the dome is colored blue, and color changes are allowed. The bot receives a sequence of messages."
date: "2026-06-10T16:46:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1531
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2021 - \u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (Engine)"
rating: 0
weight: 1531
solve_time_s: 109
verified: true
draft: false
---

[CF 1531A - \u0417\u0438\u043d\u0433\u0435\u0440 | color](https://codeforces.com/problemset/problem/1531/A)

**Rating:** -  
**Tags:** *special, implementation  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to simulate the behavior of a chatbot that controls the illumination color of the Singer House dome.

Initially, the dome is colored `blue`, and color changes are allowed. The bot receives a sequence of messages. Some messages change the lock state, while others request a color change.

A message `lock` disables future color changes. If the system is already locked, nothing happens.

A message `unlock` enables color changes again. If the system is already unlocked, nothing happens.

A color message such as `red`, `green`, or `violet` changes the dome color only when the system is currently unlocked. If the system is locked, the message is ignored.

The input gives the complete message history in chronological order. We must determine the final dome color after processing all messages.

The constraints are extremely small. There are at most 100 messages, so even a straightforward simulation easily fits within any reasonable time limit. Since each message affects only the current state, there is no need for any advanced data structure or optimization.

The main source of mistakes is handling ignored operations correctly.

Consider this example:

```
3
lock
red
green
```

The correct answer is:

```
blue
```

After `lock`, color changes become disabled. Both color messages are ignored, so the initial color remains unchanged.

Another subtle case is repeated lock operations:

```
4
lock
lock
unlock
red
```

The correct answer is:

```
red
```

The second `lock` does nothing because the system is already locked. A careless implementation that toggles the state instead of setting it explicitly would produce the wrong result.

One more case involves repeated unlock operations:

```
3
unlock
unlock
violet
```

The correct answer is:

```
violet
```

The unlock messages have no effect because the system is already unlocked. The final color change is applied normally.

## Approaches

The most direct approach is to simulate the bot exactly as described. We maintain two variables: the current color and whether color changes are locked. We process messages one by one and update these variables according to the rules.

A brute-force interpretation of the problem is already optimal because every message potentially changes the state. Any correct solution must inspect all messages at least once. With at most 100 messages, this requires only 100 operations, which is negligible.

The key observation is that the entire system state is represented by just two pieces of information: the current color and the lock status. No historical information is needed once a message has been processed. Because each message affects only the current state, a single linear scan is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal State Tracking | O(n) | O(1) | Accepted |

In this problem, the brute-force simulation and the optimal solution are actually the same algorithm.

## Algorithm Walkthrough

1. Initialize the current color as `"blue"` because the dome starts with blue illumination.
2. Initialize the lock state as `False` because color changes are initially allowed.
3. Process each message in chronological order.
4. If the message is `"lock"`, set the lock state to `True`.

This matches the specification that future color changes become blocked.
5. If the message is `"unlock"`, set the lock state to `False`.

This re-enables color changes.
6. Otherwise, the message represents a color.

If the lock state is `False`, update the current color to this message.

If the lock state is `True`, ignore the message.
7. After all messages have been processed, output the current color.

### Why it works

At every moment during processing, the pair `(current_color, locked)` exactly matches the state of the real bot after handling the same prefix of messages.

The initialization matches the problem statement. Each message is processed according to the official rules, updating either the lock state or the color. Since every state transition is reproduced exactly, the maintained state remains identical to the real system after every step. After the final message, the stored color is precisely the dome's final color.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    color = "blue"
    locked = False

    for _ in range(n):
        msg = input().strip()

        if msg == "lock":
            locked = True
        elif msg == "unlock":
            locked = False
        else:
            if not locked:
                color = msg

    print(color)

if __name__ == "__main__":
    solve()
```

The solution keeps exactly the two pieces of state identified in the algorithm discussion.

The variable `color` stores the current dome color. It starts as `"blue"` because that is the initial condition given in the statement.

The variable `locked` records whether color changes are currently blocked. It starts as `False`, meaning color changes are allowed.

For every message, we first check whether it is a lock command or an unlock command. Those commands directly set the lock state. We do not toggle the state because repeated `lock` or `unlock` messages must be harmless.

Any remaining message is necessarily one of the seven color names. We update the color only when the system is not locked. If it is locked, the message is ignored exactly as required.

No special boundary handling is needed because the input guarantees every message belongs to the allowed set.

## Worked Examples

### Example 1

Input:

```
7
red
violet
unlock
red
orange
lock
indigo
```

| Step | Message | Locked | Color |
| --- | --- | --- | --- |
| Start | - | False | blue |
| 1 | red | False | red |
| 2 | violet | False | violet |
| 3 | unlock | False | violet |
| 4 | red | False | red |
| 5 | orange | False | orange |
| 6 | lock | True | orange |
| 7 | indigo | True | orange |

Final output:

```
orange
```

This trace shows that once the system becomes locked, subsequent color messages are ignored. The final `indigo` message has no effect.

### Example 2

Input:

```
5
lock
red
unlock
green
violet
```

| Step | Message | Locked | Color |
| --- | --- | --- | --- |
| Start | - | False | blue |
| 1 | lock | True | blue |
| 2 | red | True | blue |
| 3 | unlock | False | blue |
| 4 | green | False | green |
| 5 | violet | False | violet |

Final output:

```
violet
```

This example demonstrates both behaviors. The `red` message is ignored while locked, but later color changes work normally after unlocking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each message is processed once |
| Space | O(1) | Only the current color and lock state are stored |

Since `n ≤ 100`, the running time is tiny. The algorithm performs a constant amount of work per message and uses only a few variables regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())

    color = "blue"
    locked = False

    for _ in range(n):
        msg = input().strip()

        if msg == "lock":
            locked = True
        elif msg == "unlock":
            locked = False
        else:
            if not locked:
                color = msg

    return color

# provided sample
assert run(
    "7\nred\nviolet\nunlock\nred\norange\nlock\nindigo\n"
) == "orange", "sample 1"

# minimum size input
assert run(
    "1\nred\n"
) == "red", "single color change"

# locked before color change
assert run(
    "2\nlock\nviolet\n"
) == "blue", "color must be ignored"

# repeated lock and unlock commands
assert run(
    "5\nlock\nlock\nunlock\nunlock\ngreen\n"
) == "green", "repeated state commands"

# many color changes while unlocked
assert run(
    "4\nred\nyellow\ngreen\nviolet\n"
) == "violet", "last applied color wins"

# boundary-style long test
assert run(
    "10\nlock\nred\nunlock\norange\nlock\nblue\nunlock\nindigo\nlock\nviolet\n"
) == "indigo", "mixed operations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / red` | `red` | Smallest valid input |
| `lock, violet` | `blue` | Ignored color while locked |
| Repeated lock/unlock commands | `green` | State commands are not toggles |
| Multiple colors while unlocked | `violet` | Latest successful color wins |
| Mixed lock and unlock sequence | `indigo` | Correct interaction of both states |

## Edge Cases

### Color messages while locked

Input:

```
3
lock
red
green
```

Execution starts with `(blue, unlocked)`. After `lock`, the state becomes `(blue, locked)`. Both color messages arrive while locked, so they are ignored. The final color remains `blue`.

Output:

```
blue
```

### Repeated lock operations

Input:

```
4
lock
lock
unlock
red
```

After the first `lock`, the system becomes locked. The second `lock` leaves it locked. It does not switch back to unlocked. After `unlock`, color changes become allowed again, and `red` is applied.

Output:

```
red
```

### Repeated unlock operations

Input:

```
3
unlock
unlock
violet
```

The system starts unlocked, so both `unlock` messages leave the state unchanged. The final color message is processed normally and changes the dome color to `violet`.

Output:

```
violet
```

### No successful color changes

Input:

```
4
lock
red
yellow
green
```

The dome begins as `blue`. The lock command disables all subsequent color changes. Every color message is ignored, so the initial color survives until the end.

Output:

```
blue
```
