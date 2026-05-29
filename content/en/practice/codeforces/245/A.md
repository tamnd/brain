---
title: "CF 245A - System Administrator"
description: "We process the results of several ping commands sent to two servers. Every command targets either server a or server b, and always sends exactly 10 packets. For each command, we know how many packets arrived successfully and how many were lost."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "A"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 800
weight: 245
solve_time_s: 209
verified: true
draft: false
---

[CF 245A - System Administrator](https://codeforces.com/problemset/problem/245/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We process the results of several ping commands sent to two servers. Every command targets either server `a` or server `b`, and always sends exactly 10 packets. For each command, we know how many packets arrived successfully and how many were lost.

For each server, we must combine the results of all commands sent to that server and decide whether the server is considered alive. A server is alive if at least half of all packets sent to it arrived successfully.

The input gives `n` command results. Each line contains the server identifier and the numbers of successful and failed packets. Since every command sends exactly 10 packets, the total number of packets for a server is simply `10 * number_of_commands_for_that_server`.

The constraints are extremely small. At most 1000 commands exist, so even inefficient solutions would run comfortably within the time limit. A linear scan over the input is more than enough. The task is mainly about implementing the condition correctly.

The main edge case is the exact boundary where successful packets equal half of all sent packets. The statement says "at least half", so equality counts as alive.

Consider this input:

```
2
1 5 5
2 4 6
```

Server `a` received 5 out of 10 packets successfully, which is exactly half, so the correct output is:

```
LIVE
DEAD
```

A careless implementation using `>` instead of `>=` would incorrectly mark server `a` as dead.

Another subtle case appears when one server receives many commands and the other receives very few.

```
3
1 10 0
1 0 10
2 6 4
```

Server `a` received `10 + 0 = 10` successful packets out of `20`, which is still alive because half succeeded. Looking only at individual commands instead of totals would produce the wrong answer.

## Approaches

The most direct solution is to simulate the process exactly as described. For every command, we add the successful packet count to the corresponding server and also track how many packets were sent in total. After processing all commands, we compare successful packets against half of total packets.

Even a brute-force interpretation works easily here because the input size is tiny. We could literally imagine storing every single packet outcome for each command and counting successes afterward. Since each command contains only 10 packets and there are at most 1000 commands, this would still involve only 10,000 packet states.

The problem becomes much simpler once we observe that individual packets do not matter. Only aggregate counts matter. Instead of expanding packets one by one, we can directly accumulate successful packets and total packets for each server.

This reduces the task to maintaining four integers:

- successful packets for server `a`
- total packets for server `a`
- successful packets for server `b`
- total packets for server `b`

After reading all commands, we check whether:

```
successful * 2 >= total
```

Using multiplication avoids floating point arithmetic entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * 10) | O(n * 10) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of commands `n`.
2. Create counters for both servers:

`success_a`, `total_a`, `success_b`, `total_b`.
3. Process each command one by one.
4. If the command targets server `a`, add the successful packets `x` to `success_a` and add `x + y` to `total_a`.
5. Otherwise, add the values to the counters for server `b`.

Since every command sends exactly 10 packets, `x + y` is always 10, but using `x + y` directly keeps the implementation consistent with the input format.
6. After all commands are processed, check server `a`.
7. If `success_a * 2 >= total_a`, print `"LIVE"`. Otherwise print `"DEAD"`.
8. Repeat the same check for server `b`.

### Why it works

For each server, the algorithm maintains the exact total number of successful packets and the exact total number of packets sent to that server. No information relevant to the final decision is discarded.

A server is alive precisely when:

```
successful_packets >= total_packets / 2
```

Multiplying both sides by 2 gives the equivalent integer condition:

```
successful_packets * 2 >= total_packets
```

Since the algorithm computes these totals correctly, the final classification is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

success_a = 0
total_a = 0

success_b = 0
total_b = 0

for _ in range(n):
    t, x, y = map(int, input().split())

    if t == 1:
        success_a += x
        total_a += x + y
    else:
        success_b += x
        total_b += x + y

if success_a * 2 >= total_a:
    print("LIVE")
else:
    print("DEAD")

if success_b * 2 >= total_b:
    print("LIVE")
else:
    print("DEAD")
```

The program starts by reading the number of commands. Four counters store successful and total packet counts separately for the two servers.

Each command updates only one server. The variable `x` represents successful packets, while `x + y` gives the total packets sent during that command.

The final condition uses integer arithmetic:

```
success * 2 >= total
```

This avoids floating point precision issues and directly matches the mathematical condition "at least half".

One easy mistake is using `>` instead of `>=`. Equality must count as alive because the statement says "at least half".

Another common mistake is checking each command independently instead of combining totals across all commands for the same server.

## Worked Examples

### Sample 1

Input:

```
2
1 5 5
2 6 4
```

| Step | Command | success_a | total_a | success_b | total_b |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 | 0 |
| 1 | 1 5 5 | 5 | 10 | 0 | 0 |
| 2 | 2 6 4 | 5 | 10 | 6 | 10 |

Final checks:

- Server `a`: `5 * 2 = 10 >= 10`, so LIVE
- Server `b`: `6 * 2 = 12 >= 10`, so LIVE

Output:

```
LIVE
LIVE
```

This example confirms the equality boundary. Server `a` succeeds with exactly half of its packets.

### Sample 2

Input:

```
3
1 10 0
1 0 10
2 0 10
```

| Step | Command | success_a | total_a | success_b | total_b |
| --- | --- | --- | --- | --- | --- |
| Start | - | 0 | 0 | 0 | 0 |
| 1 | 1 10 0 | 10 | 10 | 0 | 0 |
| 2 | 1 0 10 | 10 | 20 | 0 | 0 |
| 3 | 2 0 10 | 10 | 20 | 0 | 10 |

Final checks:

- Server `a`: `10 * 2 = 20 >= 20`, so LIVE
- Server `b`: `0 * 2 = 0 < 10`, so DEAD

Output:

```
LIVE
DEAD
```

This trace shows why totals across multiple commands matter. Server `a` remains alive even after one completely failed ping because its cumulative success rate is still 50%.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each command is processed once |
| Space | O(1) | Only a few integer counters are stored |

With at most 1000 commands, the linear solution runs instantly within the limits. Memory usage is constant because no arrays or additional data structures are needed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    success_a = 0
    total_a = 0

    success_b = 0
    total_b = 0

    for _ in range(n):
        t, x, y = map(int, input().split())

        if t == 1:
            success_a += x
            total_a += x + y
        else:
            success_b += x
            total_b += x + y

    if success_a * 2 >= total_a:
        print("LIVE")
    else:
        print("DEAD")

    if success_b * 2 >= total_b:
        print("LIVE")
    else:
        print("DEAD")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue()

# provided sample
assert run(
"""2
1 5 5
2 6 4
"""
) == "LIVE\nLIVE\n", "sample 1"

# boundary case: exactly half
assert run(
"""2
1 5 5
2 4 6
"""
) == "LIVE\nDEAD\n", "exactly half should be LIVE"

# multiple commands accumulated together
assert run(
"""3
1 10 0
1 0 10
2 0 10
"""
) == "LIVE\nDEAD\n", "must combine totals across commands"

# minimum valid input size
assert run(
"""2
1 0 10
2 10 0
"""
) == "DEAD\nLIVE\n", "minimum number of commands"

# all successes
assert run(
"""4
1 10 0
1 10 0
2 10 0
2 10 0
"""
) == "LIVE\nLIVE\n", "all packets successful"

# all failures
assert run(
"""4
1 0 10
1 0 10
2 0 10
2 0 10
"""
) == "DEAD\nDEAD\n", "all packets lost"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Exact 50% success | LIVE | Equality boundary uses `>=` |
| Multiple commands per server | Correct cumulative result | Totals must be aggregated |
| Minimum input size | Correct handling | Smallest valid case |
| All successes | Both LIVE | Upper success boundary |
| All failures | Both DEAD | Lower success boundary |

## Edge Cases

Consider the exact half-success boundary:

```
2
1 5 5
2 4 6
```

For server `a`, the algorithm computes:

```
success_a = 5
total_a = 10
```

The check becomes:

```
5 * 2 >= 10
```

which is true, so the output is `"LIVE"`.

A wrong implementation using `>` would incorrectly output `"DEAD"`.

Now consider cumulative aggregation:

```
3
1 10 0
1 0 10
2 6 4
```

After the first command:

```
success_a = 10
total_a = 10
```

After the second command:

```
success_a = 10
total_a = 20
```

The success rate for server `a` becomes exactly 50%, so the algorithm still prints `"LIVE"`.

A careless implementation that judged each command separately could incorrectly conclude that the second failed command makes the server dead.

Finally, consider a server with complete packet loss:

```
2
1 10 0
2 0 10
```

For server `b`:

```
success_b = 0
total_b = 10
```

The condition:

```
0 * 2 >= 10
```

is false, so the algorithm correctly prints `"DEAD"` without any special handling.
