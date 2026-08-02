---
title: "CF 102680C - The Halting Problem"
description: "The program in this problem is a very small artificial machine. It has a single 8-bit register r, so the register can only contain values from 0 to 255. Execution starts at the first instruction with r = 0."
date: "2026-08-03T03:55:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102680
codeforces_index: "C"
codeforces_contest_name: "Brookfield Computer Programming Challenge 1"
rating: 0
weight: 102680
solve_time_s: 143
verified: true
draft: false
---

[CF 102680C - The Halting Problem](https://codeforces.com/problemset/problem/102680/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The program in this problem is a very small artificial machine. It has a single 8-bit register `r`, so the register can only contain values from `0` to `255`. Execution starts at the first instruction with `r = 0`. Each instruction either changes the register and moves to the next instruction, or checks the register and possibly jumps to another instruction. The program stops only when execution moves past the last instruction.

The task is to decide whether the given program eventually reaches this stopping point or whether it keeps executing forever.

The constraints are designed around the special structure of the language. A normal program may have up to `10^4` instructions, and the total number of instructions over all test cases is at most `10^5`. Simulating an arbitrary program for an unknown amount of time is impossible in general, but this language has a bounded state space. The current instruction can have `n + 1` possible positions, and the register has only 256 possible values. This gives at most about `256 * n` different execution states. For `n = 10^4`, that is about 2.56 million states, which is small enough to visit once.

The main edge case is a program that loops without changing the register. For example:

```
2
add 0
beq 0 1
```

The correct output is:

```
No
```

After the first instruction, the register is still zero. The second instruction jumps back to the first instruction forever. A simple simulation without cycle detection would never finish.

Another case is a loop that eventually reaches a new state because the register wraps around. For example:

```
3
add 252
add 1
bgt 252 2
```

The correct output is:

```
Yes
```

The register is 8-bit, so after reaching 255 it wraps to 0. A solution treating the register as an unlimited integer would incorrectly believe the value keeps increasing and miss the halting path.

A third common mistake is ignoring the fact that the instruction pointer is part of the state. Consider:

```
3
add 1
bne 252 1
beq 252 1
```

The correct output is:

```
No
```

The register values alone are not enough to detect repetition. The same register value at different instructions represents different future behavior.

## Approaches

The direct approach is to execute the program instruction by instruction. If execution reaches instruction `n + 1`, the program halts and the answer is `Yes`. If the execution continues forever, this simulation will never terminate, so we need a way to recognize an infinite run.

The brute-force version can only run the program for some arbitrary number of steps. It is not correct because a valid program may require more steps before halting. The worst case can contain every possible `(instruction, register)` state before repeating, which is up to `256 * n` states. With `n = 10^4`, this is around 2.56 million transitions, so a full bounded simulation is enough, but an unbounded simulation is not.

The key observation is that this machine is deterministic. Once we know the current instruction and the register value, the next state is completely fixed. A deterministic process over a finite number of states must either reach the halting state or eventually revisit a state. A revisited state means the same future execution will repeat forever.

The observation that the state space is finite lets us reduce the problem to graph traversal on an implicit graph. We do not need to build the graph. We only need to remember which states have already appeared while following the single execution path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded | O(1) | Incorrect because infinite loops never finish |
| Optimal | O(256n) | O(256n) | Accepted |

## Algorithm Walkthrough

1. Store every instruction in a convenient representation. An `add` instruction stores only its value, while branch instructions store their condition, destination, and type.
2. Start execution from instruction `0` with register value `0`. Use a visited table indexed by instruction position and register value.
3. Before executing an instruction, check whether the current `(instruction, register)` pair was already visited. If it was, the machine is repeating a previous situation, so the program will never halt.
4. Mark the current state as visited and execute the instruction. For arithmetic instructions, update the register using modulo 256 because the register has only 8 bits.
5. For branch instructions, compare the register with the stored value. If the condition is true, jump to the destination instruction. Otherwise, continue to the next instruction.
6. Repeat until either instruction `n + 1` is reached or a repeated state is found.

The reason this works is that the execution is deterministic. A state is completely described by the instruction being executed and the current register value. If the same state appears twice, every following transition will also be identical, creating an infinite cycle. If no state repeats, the execution must eventually leave the finite state space by reaching the halting position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        prog = []

        for _ in range(n):
            parts = input().split()
            if parts[0] == "add":
                prog.append(("add", int(parts[1])))
            else:
                prog.append((parts[0], int(parts[1]), int(parts[2]) - 1))

        visited = [[False] * 256 for _ in range(n)]
        pc = 0
        r = 0

        while pc < n:
            if visited[pc][r]:
                ans.append("No")
                break

            visited[pc][r] = True
            ins = prog[pc]

            if ins[0] == "add":
                r = (r + ins[1]) % 256
                pc += 1
            else:
                op, v, k = ins
                ok = False

                if op == "beq":
                    ok = (r == v)
                elif op == "bne":
                    ok = (r != v)
                elif op == "blt":
                    ok = (r < v)
                elif op == "bgt":
                    ok = (r > v)

                if ok:
                    pc = k
                else:
                    pc += 1
        else:
            ans.append("Yes")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The program representation keeps the operation name together with only the parameters needed for that operation. Jump targets are converted to zero-based indices immediately, which avoids repeatedly subtracting one during simulation.

The `visited` array has one row per instruction and 256 columns for all possible register values. The register update uses `% 256` because overflowing an 8-bit register discards higher bits.

The loop checks for a repeated state before executing the instruction. Checking after execution would also work, but checking before execution makes the invariant clearer: every state that reaches the execution point has either been handled once or detected as a cycle.

Python integers do not overflow, so no special handling is required for counters or indices.

## Worked Examples

For the first sample:

```
2
add 1
blt 5 1
```

| Step | Instruction | Register | Next action |
| --- | --- | --- | --- |
| 0 | 1: add 1 | 0 | Register becomes 1, move to instruction 2 |
| 1 | 2: blt 5 1 | 1 | Jump back to instruction 1 |
| 2 | 1: add 1 | 1 | Register becomes 2, move to instruction 2 |
| 3 | 2: blt 5 1 | 2 | Jump back to instruction 1 |
| 4 | 1: add 1 | 2 | Register becomes 3, move to instruction 2 |
| 5 | 2: blt 5 1 | 3 | Jump back to instruction 1 |
| 6 | 1: add 1 | 3 | Register becomes 4, move to instruction 2 |
| 7 | 2: blt 5 1 | 4 | Jump back to instruction 1 |
| 8 | 1: add 1 | 4 | Register becomes 5, move to instruction 2 |
| 9 | 2: blt 5 1 | 5 | Continue to instruction 3 and halt |

The machine reaches the end after the register stops satisfying the branch condition. This shows that a program containing a loop in its control flow can still halt because the register changes.

For the third sample:

```
3
add 1
bne 252 1
beq 252 1
```

| Step | Instruction | Register | Next action |
| --- | --- | --- | --- |
| 0 | 1: add 1 | 0 | Register becomes 1 |
| 1 | 2: bne 252 1 | 1 | Jump to instruction 1 |
| 2 | 1: add 1 | 1 | Register becomes 2 |
| ... | repeated | increasing odd/even sequence | Continue |
| 252 | 1: add 1 | 251 | Register becomes 252 |
| 253 | 2: bne 252 1 | 252 | Move to instruction 3 |
| 254 | 3: beq 252 1 | 252 | Jump to instruction 1 |
| 255 | 1: add 1 | 252 | Register becomes 253 |

The execution eventually returns to the same instruction and register combinations, so the visited-state check detects the infinite loop.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(256n) | Each instruction and register combination is processed at most once |
| Space | O(256n) | The visited table stores one boolean for every possible state |

The maximum number of states is about 2.56 million for a single largest test case, which fits comfortably in memory. The total number of instructions across all cases is bounded, so the complete solution remains within the limits.

## Test Cases

```python
import sys
import io

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

assert run("""4
2
add 1
blt 5 1
3
add 252
add 1
bgt 252 2
2
add 2
bne 7 1
3
add 1
bne 252 1
beq 252 1
""") == """Yes
Yes
No
No
""", "provided samples"

assert run("""1
1
add 0
""") == """Yes
""", "single instruction halts"

assert run("""1
2
add 0
beq 0 1
""") == """No
""", "immediate infinite loop"

assert run("""1
2
add 255
bne 255 1
""") == """Yes
""", "register wraparound"

assert run("""1
3
add 1
bne 3 1
beq 3 1
""") == """No
""", "unreachable branch condition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `add` instruction | Yes | Halting after reaching the end |
| Jump with unchanged register | No | Detection of a fixed cycle |
| Register overflow case | Yes | Correct modulo 256 behavior |
| Impossible branch value | No | Correct handling of unreachable conditions |

## Edge Cases

The unchanged-register infinite loop is handled because the state `(instruction, register)` repeats immediately. For:

```
2
add 0
beq 0 1
```

the states `(1,0)` and `(2,0)` are visited repeatedly. When `(1,0)` appears again, the algorithm outputs `No` instead of simulating forever.

Register overflow is handled by keeping every value inside the range `0` to `255`. For:

```
3
add 252
add 1
bgt 252 2
```

the register sequence eventually wraps from `255` to `0`. The algorithm sees the actual machine behavior and reaches the halting instruction.

Cases where the same register value appears at different instructions are handled by storing the instruction index as part of the state. A register-only visited set would incorrectly report cycles too early because two instructions with the same register value can have different futures. The pair `(program counter, register)` is the complete machine state, so the algorithm only stops when the real execution repeats.
