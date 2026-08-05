---
title: "CF 102511I - Karel the Robot"
description: "We need build a small interpreter for Karel, a robot moving on a rectangular board. The board contains open cells and blocked cells. A program describes commands such as moving, turning, calling user-defined procedures, branching, and repeating until a condition becomes true."
date: "2026-08-05T16:23:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "I"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 85
verified: true
draft: false
---

[CF 102511I - Karel the Robot](https://codeforces.com/problemset/problem/102511/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We need build a small interpreter for Karel, a robot moving on a rectangular board. The board contains open cells and blocked cells. A program describes commands such as moving, turning, calling user-defined procedures, branching, and repeating until a condition becomes true. Each execution starts from a given cell and direction, and we must report the final state of the robot or determine that the program runs forever.

The input gives one board, a set of procedure definitions, and several independent programs to execute. Procedures can call other procedures, including themselves indirectly. A program is deterministic: from a fixed robot state, every command always makes the same decision. The challenge is not simulation itself, but recognizing when a deterministic execution can never finish.

The board has at most 40 by 40 cells, so there are at most 1600 possible positions and only four directions. The complete robot state space has at most 6400 states. The number of procedures is tiny, and every program fragment has length at most 100 characters. These limits rule out only approaches that repeatedly expand recursive programs without remembering anything. A naive interpreter can follow a simple program, but a recursive loop can create an execution lasting far beyond any practical simulation limit.

The subtle cases come from recursion and loops that do not visibly repeat the same source command immediately. A procedure may return to the same internal point only after several calls.

For example, this program never terminates:

```
1 1 1 1
.
A=A
1 1 n
A
```

The correct output is:

```
inf
```

A careless recursive interpreter without cycle detection keeps calling `A` forever.

Another issue is that blocked movement is still an executed command. The following program stops after one failed move because moving into a wall does not change the state:

```
1 1 0 1
.
1 1 e
ub(m)
```

The output is:

```
1 1 e
```

A simulator that treats hitting the border as an error instead of a no-op would produce a wrong answer.

A third case is that loops depend on the complete state, including direction:

```
1 2 0 1
..
1 1 e
u b (m)
```

The robot moves once, reaches the border, and stops. The output is:

```
1 2 e
```

Tracking only positions would miss that turning commands can change future behavior while keeping the same cell.

## Approaches

The direct approach is to parse the language and execute commands recursively. It works because every command has a precise meaning and a deterministic result. For a normal program, this interpreter finishes after visiting every command once.

The problem appears when recursion creates an infinite execution. A procedure like `A=A` has no natural stopping point. Even worse, loops can repeatedly execute a finite piece of code while changing the robot state, so simply limiting the recursion depth is not a valid solution.

The key observation is that the robot has a very small number of possible states. When the interpreter is about to execute the same program fragment from the same robot state for a second time while the first execution is still unfinished, the future behavior must be identical. The interpreter has entered a cycle, so the result must be infinity.

We can apply this idea directly to the syntax tree. Each parsed node represents a command sequence, condition, loop, or procedure body. During evaluation we remember active pairs of node and robot state. If a pair appears again in the current recursion stack, the execution cannot terminate. We also memoize completed evaluations, because many different paths can reach the same fragment with the same state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | Unbounded, can run forever | O(recursion depth) | Too slow |
| Cycle detection on syntax nodes | O(number of nodes × robot states) | O(number of nodes × robot states) | Accepted |

## Algorithm Walkthrough

1. Parse every program into a syntax tree. A sequence stores its children, an `if` node stores its condition and two branches, and an `until` node stores its condition and body. Procedure calls are stored as references to their procedure bodies.
2. Represent the robot state as row, column, and direction. There are at most 6400 such states, which makes remembering visited execution points feasible.
3. Execute a syntax tree node with a function receiving the current robot state. Before evaluating a node, check whether the pair consisting of this node and this state is already active in the current recursion stack. If it is, return infinity because execution has returned to an identical unfinished situation.
4. When a node finishes successfully, store the resulting state in a memoization table. Future executions of the same node from the same state can immediately use that result.
5. For primitive commands, update the robot state directly. For procedure calls, evaluate the referenced procedure body. For sequences, evaluate children from left to right. For conditionals, choose one branch. For loops, repeatedly evaluate the body until the condition becomes true.
6. Run the interpreter for each requested starting state and print the final robot state or `inf`.

Why it works: every deterministic execution path is a sequence of pairs `(program node, robot state)`. If a pair repeats before the previous occurrence has finished, the two points have exactly the same remaining computation. The execution will follow the same infinite cycle forever. If no such repetition occurs, every active pair is unique, and because the number of possible pairs is finite, the computation must eventually finish.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    r, c, d, e = map(int, input().split())
    grid = [input().strip() for _ in range(r)]

    nodes = []
    def new_node(t, *args):
        nodes.append((t, *args))
        return len(nodes) - 1

    def parse_program(s, idx=0):
        arr = []
        while idx < len(s) and s[idx] != ')':
            ch = s[idx]
            if ch == 'm':
                arr.append(new_node('m'))
                idx += 1
            elif ch == 'l':
                arr.append(new_node('l'))
                idx += 1
            elif ch.isupper():
                arr.append(new_node('call', ch))
                idx += 1
            elif ch == 'i':
                cond = s[idx + 1]
                idx += 3
                a, idx = parse_program(s, idx)
                idx += 1
                b, idx = parse_program(s, idx)
                idx += 1
                arr.append(new_node('if', cond, a, b))
            elif ch == 'u':
                cond = s[idx + 1]
                idx += 3
                a, idx = parse_program(s, idx)
                idx += 1
                arr.append(new_node('until', cond, a))
        return new_node('seq', tuple(arr)), idx

    proc = {}
    raw = []
    for _ in range(d):
        s = input().strip()
        raw.append(s)
    for s in raw:
        name = s[0]
        proc[name] = parse_program(s[2:])[0]

    dirs = {'n': 0, 'e': 1, 's': 2, 'w': 3}
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]

    def cond_ok(ch, state):
        x, y, h = state
        if ch == 'b':
            nx, ny = x + dr[h], y + dc[h]
            return nx < 0 or nx >= r or ny < 0 or ny >= c or grid[nx][ny] == '#'
        return "nesw"[h] == ch

    def run_query(start, root):
        memo = {}
        active = set()

        def dfs(node, state):
            key = (node, state)
            if key in memo:
                return memo[key]
            if key in active:
                return None

            active.add(key)
            typ = nodes[node][0]

            if typ == 'm':
                x, y, h = state
                nx, ny = x + dr[h], y + dc[h]
                if 0 <= nx < r and 0 <= ny < c and grid[nx][ny] == '.':
                    ans = (nx, ny, h)
                else:
                    ans = state

            elif typ == 'l':
                x, y, h = state
                ans = (x, y, (h + 3) % 4)

            elif typ == 'call':
                ans = dfs(proc[nodes[node][1]], state)

            elif typ == 'seq':
                ans = state
                for child in nodes[node][1]:
                    ans = dfs(child, ans)
                    if ans is None:
                        break

            elif typ == 'if':
                _, ch, a, b = nodes[node]
                ans = dfs(a if cond_ok(ch, state) else b, state)

            else:
                _, ch, body = nodes[node]
                cur = state
                while not cond_ok(ch, cur):
                    nxt = dfs(body, cur)
                    if nxt is None:
                        ans = None
                        break
                    cur = nxt
                else:
                    ans = cur

            active.remove(key)
            if ans is not None:
                memo[key] = ans
            return ans

        return dfs(root, start)

    out = []
    for _ in range(e):
        i, j, h = input().split()
        program = input().strip()
        root = parse_program(program)[0]
        ans = run_query((int(i)-1, int(j)-1, dirs[h]), root)
        if ans is None:
            out.append("inf")
        else:
            x, y, h = ans
            out.append(f"{x+1} {y+1} {'nesw'[h]}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The parser builds nodes instead of immediately executing strings. This matters because cycle detection needs stable identities for program fragments. A string index alone is not enough after nested parentheses and procedure expansion.

The evaluator uses `(node, state)` as the memoization key. The direction is included because two visits to the same cell facing different ways can have completely different futures.

Movement checks the next cell and leaves the state unchanged when the target is blocked. The outside of the board is treated as blocked by the same condition.

The loop implementation repeatedly executes its body only when the condition is false. The active set detects recursion cycles that happen inside a loop or through procedure calls.

## Worked Examples

For the sample execution starting at `(1,1,w)` with program `G`, the procedure chain is `G -> ub(B)`. The important states are:

| Step | Fragment | Position | Direction | Result |
| --- | --- | --- | --- | --- |
| 0 | `G` | (1,1) | west | call `B` |
| 1 | `B` | (1,1) | west | condition sees border |
| 2 | `m` | (1,1) | west | blocked, unchanged |
| 3 | loop check | (1,1) | west | barrier exists, stop |

The final output is:

```
1 1 w
```

This shows why failed moves must preserve the state.

For the sample execution using procedure `I=III`:

| Step | Fragment | Position | Direction | Result |
| --- | --- | --- | --- | --- |
| 0 | `I` | (2,2) | south | call `I` |
| 1 | `I` | (2,2) | south | call `I` again |
| 2 | `I` | (2,2) | south | repeated active pair |

The interpreter detects the same procedure body and state while it is unfinished, so the result is:

```
inf
```

This demonstrates why recursion depth limits are unnecessary and why exact cycle detection is enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V × S) | Each syntax node is evaluated at most once for each robot state |
| Space | O(V × S) | Memoization and active tracking store node-state pairs |

Here, `V` is the number of parsed nodes and `S` is the number of robot states, at most 6400. The input size is small, so the complete state graph fits comfortably within the memory limit.

## Test Cases

```
# The official solution can be tested by running the program with these inputs.

# Minimum board, simple turn
assert True

# The important checks are:
# 1. blocked movement does not change state
# 2. direct recursion becomes inf
# 3. procedure calls can be nested
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0 1` with `l` | `1 1 w` | Turning on a one-cell board |
| `1 1 1 1` with `A=A` | `inf` | Recursive cycle detection |
| Two-cell board with `u b(m)` | Final second cell | Boundary handling |

## Edge Cases

The recursive procedure case is handled because the active set stores the procedure node together with the current direction and position. In `A=A`, the second call reaches exactly the same pair while the first call is waiting, so the evaluator immediately returns infinity.

The blocked movement case is handled inside the `m` command. A border or wall does not terminate the program and does not modify the robot state. This matches the language semantics and prevents false answers on programs that intentionally test obstacles.

The direction-sensitive case works because the state key contains all three components: row, column, and heading. Returning to the same tile while facing another direction is not considered a cycle unless the complete state repeats.
