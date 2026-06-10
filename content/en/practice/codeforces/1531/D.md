---
title: "CF 1531D - \u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u0443\u0435\u043c \u0417\u0438\u043d\u0433\u0435\u0440 | color"
description: "We have a chronological list of bot messages. The bot keeps two pieces of state. The first is whether color changes are currently locked. The second is the current dome color, one of seven rainbow colors. Initially the dome is blue and color changes are unlocked."
date: "2026-06-10T16:48:08+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1531
codeforces_index: "D"
codeforces_contest_name: "VK Cup 2021 - \u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (Engine)"
rating: 0
weight: 1531
solve_time_s: 127
verified: true
draft: false
---

[CF 1531D - \u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u0443\u0435\u043c \u0417\u0438\u043d\u0433\u0435\u0440 | color](https://codeforces.com/problemset/problem/1531/D)

**Rating:** -  
**Tags:** *special  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a chronological list of bot messages. The bot keeps two pieces of state.

The first is whether color changes are currently locked.

The second is the current dome color, one of seven rainbow colors.

Initially the dome is blue and color changes are unlocked.

Each message acts on the current state.

A `lock` message turns the system into the locked state if it is not already locked.

An `unlock` message turns the system into the unlocked state if it is not already unlocked.

A color message changes the dome color only when the system is currently unlocked. If the system is locked, the color message is ignored.

After the initial history, we receive up to $10^5$ edits. Each edit replaces one message in the history. After every edit, the whole history must be reprocessed from the original initial state, and we must output the resulting dome color.

The constraints are the real challenge. Both the number of messages and the number of edits can reach $10^5$. Replaying the entire history after every edit would require roughly $10^{10}$ message applications in the worst case, which is far beyond what fits in a contest time limit.

The key observation is that the bot's state space is tiny. There are only seven colors and two lock states, so only fourteen possible states exist.

A subtle edge case appears when a color message is executed while locked.

Example:

```
lock
red
unlock
```

The final color is still blue. The `red` command is ignored because the system was locked when it arrived.

Another easy mistake is treating `lock` and `unlock` as unconditional assignments.

Example:

```
lock
lock
unlock
```

The second `lock` does nothing. The behavior is still well-defined because messages operate on the current state, not on the message history itself.

A third edge case is editing an old message.

Example:

```
1: red
2: lock
3: green
```

Initially the result is `red`.

If message 2 is edited into `unlock`, then message 3 suddenly becomes effective and the answer becomes `green`.

Any solution that tries to update only the suffix color without reconsidering the state transition structure will fail.

## Approaches

The brute-force solution is straightforward. Treat the message list as a program. Starting from the initial state, process all $n$ messages and obtain the final color. After every edit, modify the message and run the entire simulation again.

This works because the bot's rules are deterministic. The problem is cost. Each query needs $O(n)$ work, and there are $10^5$ queries. The total complexity becomes $O(nt)$, which reaches $10^{10}$ operations.

The important observation is that every message is actually a function on the set of fourteen possible states.

For example, `lock` maps every unlocked state to the corresponding locked state and leaves locked states unchanged.

A color command such as `red` maps every unlocked state to the unlocked-red state and leaves every locked state unchanged.

Since each message is a state transition function, a whole segment of messages is simply the composition of their functions.

This immediately suggests a segment tree.

For every node we store the function represented by that segment. Since the state space contains only fourteen states, a function can be stored as an array of length fourteen where `f[s]` is the resulting state after applying the segment to state `s`.

When combining two child segments, we compose their functions. If the left segment represents `L` and the right segment represents `R`, then the parent represents `R ∘ L`, because messages from the left half execute before messages from the right half.

A point update changes one message, so only $O(\log n)$ segment tree nodes must be recomputed. Each recomputation composes two functions of size fourteen, which is constant work.

The answer is obtained by applying the root function to the initial state `(unlocked, blue)` and extracting the resulting color.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nt)$ | $O(1)$ | Too slow |
| Optimal | $O(14 \cdot (n + t \log n))$ | $O(14n)$ | Accepted |

## Algorithm Walkthrough

1. Encode every possible bot state as an integer from 0 to 13.
2. Represent a state as `(locked, color)`.
3. For every possible message type, precompute its transition function on all fourteen states.
4. Build a segment tree where each leaf stores the function corresponding to one message.
5. For an internal node, compose the functions of its children. If `left` and `right` are the child functions, then:

`parent[s] = right[left[s]]`

because the left segment executes first.
6. To obtain the current answer, apply the root function to the initial state `(unlocked, blue)`.
7. Extract the color component of the resulting state and print its name.
8. For an edit operation, replace the corresponding leaf function.
9. Recompute all ancestors up to the root using the same composition rule.
10. Query the root again and output the resulting color.

### Why it works

Each message defines a deterministic transformation of the fourteen-state automaton. Function composition exactly matches sequential execution of messages. A segment tree node stores the transformation produced by its entire interval. By induction on the tree structure, every node correctly represents the effect of processing all messages in its segment.

The root interval covers the entire history, so its function is exactly the effect of replaying the complete message sequence from the initial state. After a point update, only segments containing that position change, and recomputing compositions restores the correct transformation for every affected node. Thus every reported color matches the result of a full replay.

## Python Solution

```python
import sys
input = sys.stdin.readline

colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
color_id = {c: i for i, c in enumerate(colors)}

STATE_COUNT = 14

def state_id(locked, color):
    return locked * 7 + color

# Precompute transition function for every possible message.
funcs = {}

for msg in ["lock", "unlock"] + colors:
    f = [0] * STATE_COUNT

    for locked in range(2):
        for color in range(7):
            s = state_id(locked, color)

            if msg == "lock":
                ns = state_id(1, color) if locked == 0 else s
            elif msg == "unlock":
                ns = state_id(0, color) if locked == 1 else s
            else:
                if locked == 0:
                    ns = state_id(0, color_id[msg])
                else:
                    ns = s

            f[s] = ns

    funcs[msg] = f

def compose(left, right):
    # right ∘ left
    return [right[left[i]] for i in range(STATE_COUNT)]

n = int(input())
messages = [input().strip() for _ in range(n)]

size = 1
while size < n:
    size <<= 1

identity = list(range(STATE_COUNT))
seg = [identity[:] for _ in range(2 * size)]

for i in range(n):
    seg[size + i] = funcs[messages[i]]

for i in range(size - 1, 0, -1):
    seg[i] = compose(seg[i * 2], seg[i * 2 + 1])

initial_state = state_id(0, color_id["blue"])

def answer():
    final_state = seg[1][initial_state]
    color = final_state % 7
    return colors[color]

out = [answer()]

t = int(input())

for _ in range(t):
    pos, msg = input().split()
    pos = int(pos) - 1

    p = size + pos
    seg[p] = funcs[msg]

    p //= 2
    while p:
        seg[p] = compose(seg[p * 2], seg[p * 2 + 1])
        p //= 2

    out.append(answer())

sys.stdout.write("\n".join(out))
```

The state encoding is the most important implementation detail. Every state must uniquely represent both the lock flag and the current color. Using `locked * 7 + color` gives a compact range from 0 to 13.

Each message is converted into a length-14 transition table. This turns the problem from simulating messages into composing functions.

The segment tree stores complete functions rather than scalar values. Composition order matters. If the left segment executes before the right segment, the parent must represent `right[left[s]]`. Reversing this order produces incorrect answers.

The identity function is used for unused leaves. Since composing with identity changes nothing, padding the tree becomes safe.

## Worked Examples

### Sample 1

Initial history:

| Step | Message | Locked | Color |
| --- | --- | --- | --- |
| Start | - | No | blue |
| 1 | red | No | red |
| 2 | violet | No | violet |
| 3 | unlock | No | violet |
| 4 | red | No | red |
| 5 | orange | No | orange |
| 6 | lock | Yes | orange |
| 7 | indigo | Yes | orange |

Final answer is `orange`.

The last `indigo` is ignored because the system is locked.

After editing message 5 to `green`, the same replay produces `green`, which matches the sample output.

### Custom Example

```
3
lock
red
unlock
```

| Step | Message | Locked | Color |
| --- | --- | --- | --- |
| Start | - | No | blue |
| 1 | lock | Yes | blue |
| 2 | red | Yes | blue |
| 3 | unlock | No | blue |

The result remains `blue`.

This example shows why color commands cannot be treated as unconditional assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(14 \cdot (n + t \log n))$ | Building requires function compositions, each update touches $O(\log n)$ nodes |
| Space | $O(14n)$ | Every segment tree node stores a function of size 14 |

Since 14 is a fixed constant, the practical complexity is essentially $O(n + t \log n)$, which comfortably handles $10^5$ messages and $10^5$ edits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
    color_id = {c: i for i, c in enumerate(colors)}

    STATE_COUNT = 14

    def state_id(locked, color):
        return locked * 7 + color

    funcs = {}

    for msg in ["lock", "unlock"] + colors:
        f = [0] * STATE_COUNT
        for locked in range(2):
            for color in range(7):
                s = state_id(locked, color)

                if msg == "lock":
                    ns = state_id(1, color) if locked == 0 else s
                elif msg == "unlock":
                    ns = state_id(0, color) if locked == 1 else s
                else:
                    ns = state_id(0, color_id[msg]) if locked == 0 else s

                f[s] = ns
        funcs[msg] = f

    def compose(a, b):
        return [b[a[i]] for i in range(STATE_COUNT)]

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    msgs = [input().strip() for _ in range(n)]

    size = 1
    while size < n:
        size <<= 1

    identity = list(range(STATE_COUNT))
    seg = [identity[:] for _ in range(2 * size)]

    for i in range(n):
        seg[size + i] = funcs[msgs[i]]

    for i in range(size - 1, 0, -1):
        seg[i] = compose(seg[i * 2], seg[i * 2 + 1])

    initial = state_id(0, color_id["blue"])

    def ans():
        s = seg[1][initial]
        return colors[s % 7]

    out = [ans()]

    t = int(input())
    for _ in range(t):
        p, msg = input().split()
        p = int(p) - 1

        idx = size + p
        seg[idx] = funcs[msg]

        idx //= 2
        while idx:
            seg[idx] = compose(seg[idx * 2], seg[idx * 2 + 1])
            idx //= 2

        out.append(ans())

    return "\n".join(out)

# provided sample
assert run(
"""7
red
violet
unlock
red
orange
lock
indigo
6
5 green
6 lock
6 yellow
4 lock
1 lock
5 unlock
"""
) == """orange
green
green
indigo
violet
blue
indigo"""

# minimum size
assert run(
"""1
blue
1
1 red
"""
) == """blue
red"""

# locked color ignored
assert run(
"""2
lock
red
1
2 green
"""
) == """blue
blue"""

# unlock enables later color
assert run(
"""3
lock
red
unlock
1
2 green
"""
) == """blue
blue"""

# edit old message changes future behavior
assert run(
"""3
red
lock
green
1
2 unlock
"""
) == """red
green"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single message edited | blue → red | Minimum size |
| `lock` then color | blue | Ignored color while locked |
| `lock`, color, `unlock` | blue | Unlock does not replay old colors |
| Edit `lock` into `unlock` | red → green | Historical edits affecting later messages |

## Edge Cases

Consider:

```
2
lock
red
```

The system becomes locked before the color command arrives. The transition function for `red` leaves every locked state unchanged, so the final color remains blue. The segment tree composition naturally preserves this behavior.

Consider:

```
3
lock
lock
unlock
```

The second `lock` maps the locked state to itself. Its transition function is idempotent. Composing it with the first `lock` produces exactly the same effect as a single lock operation.

Consider:

```
3
red
lock
green
```

The answer is `red`. If message 2 is edited to `unlock`, then the third message becomes effective and the answer changes to `green`. The update changes only one leaf, but the recomputed compositions automatically propagate the effect through the entire history.
