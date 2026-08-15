---
title: "CF 102386D - \u0410\u0440\u0442\u0435\u043c \u0432 \u0430\u0440\u043c\u0438\u0438"
description: "There are exactly three tanks, numbered 1, 2, and 3, and Artem starts in tank k. Each command names two different tanks. The crews of those two tanks exchange their tanks, so Artem moves only when his current tank is one of the two mentioned in the command."
date: "2026-08-15T07:38:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "D"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 261
verified: false
draft: false
---

[CF 102386D - \u0410\u0440\u0442\u0435\u043c \u0432 \u0430\u0440\u043c\u0438\u0438](https://codeforces.com/problemset/problem/102386/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 21s  
**Verified:** no  

## Solution
## Problem Understanding

There are exactly three tanks, numbered 1, 2, and 3, and Artem starts in tank `k`. Each command names two different tanks. The crews of those two tanks exchange their tanks, so Artem moves only when his current tank is one of the two mentioned in the command.

The input contains `n` commands followed in their given order. The first line gives the number of commands and Artem's initial tank. Each following line contains the two tank numbers involved in one swap. The required output is the tank number containing Artem after every command has been processed.

The constraint `n <= 10^5` means the solution should process each command a constant number of times. An `O(n)` algorithm performs only a few hundred thousand basic operations, which is easily suitable for a normal competitive programming time limit. An `O(n^2)` simulation could require about `10^10` operations at the maximum input size, which is far beyond what is practical.

The first edge case is a command that does not involve Artem's current tank. For example,

```
1 1
2 3
```

produces `1`. Artem remains in tank 1 because the swap happens entirely between tanks 2 and 3. A careless implementation that changes Artem's position after every command, without checking whether his tank is involved, could incorrectly move him.

The second edge case is when Artem is in one of the swapped tanks and the command moves him to the other one. For example,

```
1 2
1 2
```

produces `1`. Artem starts in tank 2, so exchanging tanks 1 and 2 moves him to tank 1. The two numbers in the command must be treated as the two endpoints of the swap, not as an ordered operation where one replaces the other.

A third useful case is a repeated swap. For example,

```
2 3
2 3
2 3
```

produces `3`. The first swap moves Artem from 3 to 2, and the second moves him back to 3. An implementation that accidentally ignores repeated commands or tries to simplify commands without preserving their order can get this wrong.

## Approaches

A direct but unnecessarily expensive approach would be to recompute Artem's position from the beginning after every command. After processing command `i`, it would simulate all `i` commands to determine where Artem is, even though the answer after command `i-1` is already known. The total number of simulated commands would be

`1 + 2 + 3 + ... + n = n(n + 1) / 2`.

For `n = 100000`, that is `5,000,050,000` command simulations. The simulation itself is correct, because it follows exactly the same swaps as the original process, but it repeats almost all of the work many times.

The key observation is that we do not need the full arrangement of crews. We only care about Artem's current tank. For one command `(a, b)`, there are only three possibilities. If Artem is in neither `a` nor `b`, his position stays unchanged. If he is in `a`, he moves to `b`. If he is in `b`, he moves to `a`.

The brute-force recomputation works because every command is deterministic, but fails when it repeatedly reconstructs information that has already been computed. The observation that the next position depends only on Artem's current position and the current command lets us reduce the entire process to one constant-time update per command.

The resulting algorithm needs no array of tank contents and no representation of the crews. A single integer containing Artem's current tank is enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and Artem's initial tank `k`. Store `k` as the current position because before any command is executed, it is exactly where Artem is.
2. Process the `n` commands in their input order. For each command, read the two swapped tanks `a` and `b`.
3. If the current position equals `a`, change it to `b`. Artem is sitting in one of the two tanks being exchanged, so he moves into the other tank.
4. Otherwise, if the current position equals `b`, change it to `a`. The same swap rule applies in the opposite direction.
5. If the current position is neither `a` nor `b`, leave it unchanged. The command affects two other tanks and cannot move Artem.
6. After all commands have been processed, print the current position. Every update has been applied in the original order, so this value is Artem's final tank.

### Why it works

The invariant is that immediately before processing every command, `k` stores Artem's actual current tank. For a command `(a, b)`, if `k` is `a`, the crew in tank `a` moves to tank `b`, so Artem moves to `b`. The symmetric case holds when `k` is `b`, and when `k` is neither tank, Artem does not move. Thus the invariant remains true after every command. After the last command, `k` must consequently be the required final tank.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    for _ in range(n):
        a, b = map(int, input().split())

        if k == a:
            k = b
        elif k == b:
            k = a

    print(k)

if __name__ == "__main__":
    solve()
```

The first line reads both the number of commands and Artem's initial tank. The variable `k` is deliberately reused to represent the current tank, so there is no need for a separate state structure.

Inside the loop, each command is processed exactly once. The `if` branch handles the case where Artem is in the first tank of the command, while the `elif` handles the second tank. If neither condition is true, nothing is assigned to `k`, so Artem remains where he is.

The order of these updates matters because a later command must use Artem's position after all earlier commands. There are no indexing conversions here because the tanks are already numbered from 1 through 3. Python integers also have no overflow concern for these values, although in fact `k` never becomes anything outside the range 1 through 3.

The input contains only one test case, so there is no outer test-case loop. Using `sys.stdin.readline` gives efficient input handling for up to `10^5` commands.

## Worked Examples

For the provided sample, Artem starts in tank 1. The first command exchanges tanks 1 and 2, so Artem moves to 2. The second command exchanges tanks 2 and 3, so he moves to 3.

| Command | `a` | `b` | `k` before | `k` after |
| --- | --- | --- | --- | --- |
| Start |  |  |  | 1 |
| 1 | 1 | 2 | 1 | 2 |
| 2 | 2 | 3 | 2 | 3 |

The final value is `3`, matching the sample output. This trace demonstrates the main transition rule twice in succession.

For a second example, consider:

```
5 3
1 2
2 3
1 3
1 2
2 3
```

The state changes as follows.

| Command | `a` | `b` | `k` before | `k` after |
| --- | --- | --- | --- | --- |
| Start |  |  |  | 3 |
| 1 | 1 | 2 | 3 | 3 |
| 2 | 2 | 3 | 3 | 2 |
| 3 | 1 | 3 | 2 | 2 |
| 4 | 1 | 2 | 2 | 1 |
| 5 | 2 | 3 | 1 | 1 |

The final answer is `1`. The first and third commands do not involve Artem's current tank, so his position stays unchanged during those steps. This confirms that every command must be checked against the current position rather than blindly moving Artem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the `n` commands is read and processed once with constant work. |
| Space | O(1) | Only `n`, `k`, `a`, and `b` are stored, regardless of the number of commands. |

With `n <= 10^5`, the algorithm performs only a constant amount of work per command, so the total number of operations grows linearly with the input size. It also stores no command list, making its memory usage independent of `n`.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n, k = map(int, input().split())

    for _ in range(n):
        a, b = map(int, input().split())

        if k == a:
            k = b
        elif k == b:
            k = a

    print(k)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""2 1
1 2
2 3
""") == "3\n", "sample 1"

# Minimum-size input
assert run("""1 1
2 3
""") == "1\n", "Artem is not involved in the only swap"

# Artem starts at the largest tank number
assert run("""1 3
1 3
""") == "1\n", "boundary tank 3 moves to tank 1"

# Repeated swaps return Artem to the original tank
assert run("""2 3
2 3
2 3
""") == "3\n", "two identical swaps cancel each other"

# Multiple commands, including commands that do not involve Artem
assert run("""5 3
1 2
2 3
1 3
1 2
2 3
""") == "1\n", "mixed swaps"

# Maximum-size input, repeated identical swaps
n = 100000
large_input = f"{n} 1\n" + "1 2\n" * n
expected = "1\n" if n % 2 == 0 else "2\n"
assert run(large_input) == expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 2 3` | `1` | Minimum input and a swap that does not involve Artem |
| `1 3 / 1 3` | `1` | Boundary tank number and direct movement |
| `2 3 / 2 3 / 2 3` | `3` | Repeated swaps and order of operations |
| `5 3 / 1 2 / 2 3 / 1 3 / 1 2 / 2 3` | `1` | Commands both involving and not involving Artem |
| `100000 1 / 1 2` repeated | `1` | Maximum input size and repeated state transitions |

## Edge Cases

When Artem is not involved in a swap, his position must remain unchanged. For the input

```
1 1
2 3
```

the initial position is `1`. The command only exchanges tanks `2` and `3`, so neither `k == a` nor `k == b` is true. The algorithm leaves `k` equal to `1` and prints `1`. This prevents the common mistake of assuming every command moves Artem.

When Artem starts in tank 2 and tanks 1 and 2 are exchanged, the update must use the other endpoint of the command. For

```
1 2
1 2
```

the algorithm begins with `k = 2`. The first condition fails because `2 != 1`, while the second succeeds because `2 == 2`, so `k` becomes `1`. The output is `1`.

Repeated swaps must be processed independently. For

```
2 3
2 3
2 3
```

the first command changes `k` from `3` to `2`. The second command sees the updated value `2` and changes it back to `3`. The final output is `3`. This demonstrates why commands cannot be reordered or treated as a single permanent mapping.

The maximum-size case does not require any special logic. With `100000` commands such as

```
100000 1
1 2
1 2
1 2
...
```

the algorithm performs one constant-time comparison for each command. Since there are an even number of swaps, Artem starts in tank 1 and returns to tank 1, so the output is `1`. The state itself never grows with the input, which is why the solution remains `O(1)` in auxiliary space.
