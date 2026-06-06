---
title: "CF 411B - Multi-core Processor"
description: "We are simulating a processor with several cores and several memory cells. Time is divided into cycles. For every cycle, each core receives either a command to do nothing or a command to write into a specific memory cell. The interesting part is how deadlocks occur."
date: "2026-06-07T02:15:36+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 411
codeforces_index: "B"
codeforces_contest_name: "Coder-Strike 2014 - Qualification Round"
rating: 1600
weight: 411
solve_time_s: 119
verified: true
draft: false
---

[CF 411B - Multi-core Processor](https://codeforces.com/problemset/problem/411/B)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a processor with several cores and several memory cells. Time is divided into cycles. For every cycle, each core receives either a command to do nothing or a command to write into a specific memory cell.

The interesting part is how deadlocks occur.

If, during the same cycle, two or more active cores try to write into the same memory cell, a conflict happens. Every core involved in that conflict becomes permanently locked, and the memory cell itself also becomes permanently locked.

After a core becomes locked, it ignores all future commands. After a memory cell becomes locked, nobody can successfully write into it again. If an active core later tries to write into an already locked cell, that core immediately becomes locked as well.

For every core, we must determine the first cycle in which it becomes locked. If it never becomes locked during the simulation, we output 0.

The constraints are extremely small. The numbers of cores, cycles, and memory cells are all at most 100. Even an algorithm that performs work proportional to all cores and all cycles simultaneously is easily fast enough. The entire input contains at most 10,000 instructions, so simplicity and correctness matter more than sophisticated optimization.

The main difficulty is not efficiency but faithfully reproducing the timing rules.

One easy mistake is handling simultaneous writes incorrectly.

Consider:

```
2 1 1
1
1
```

Both cores write to cell 1 during cycle 1.

The correct output is:

```
1
1
```

Both cores lock at the same moment because the conflict is detected from the set of writes occurring in that cycle. A careless simulation that processes cores one by one could let the first write succeed and only lock the second core.

Another subtle case occurs when writing into a cell that was locked earlier.

```
2 2 1
1 1
1 0
```

Cycle 1 creates a conflict, locking both cores and the cell.

Correct output:

```
1
1
```

A buggy implementation might continue executing commands for already locked cores during cycle 2, which would violate the statement.

A third edge case is that writes to locked cells are checked only for currently active cores.

```
2 2 1
1 0
1 1
```

Cycle 1 locks both cores and the cell.

Correct output:

```
1
1
```

During cycle 2, the second core would have attempted another write to the locked cell, but it is already locked, so nothing happens. Once a core is locked, it never participates again.

## Approaches

The most direct idea is to simulate the processor exactly as described.

For each cycle, we inspect every active core. If a core wants to write into an already locked cell, that core becomes locked immediately. Otherwise, we group all write requests by destination cell. Any cell receiving requests from two or more active cores causes a conflict, which locks all participating cores and the cell itself.

Because the constraints are tiny, this straightforward simulation is already fast enough.

Suppose we tried an even more naive method. For every cycle and every cell, we could scan all cores to see who wants to write there. That would require roughly $m \cdot k \cdot n$ operations. With all values equal to 100, this is only one million checks, which is still acceptable.

However, grouping writes while processing the cycle is cleaner and more natural. Each instruction is examined once per cycle, giving a simulation whose running time is proportional to the total number of instructions.

The key observation is that every cycle can be processed independently using the current set of active cores and unlocked cells. Conflicts depend only on write requests made during that specific cycle, while previously locked cores and cells simply remain unavailable forever.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nmk) | O(1) | Accepted |
| Optimal Simulation | O(nm) | O(n + k) | Accepted |

## Algorithm Walkthrough

1. Read all instructions into a two-dimensional array where `cmd[i][j]` is the command of core `i` during cycle `j`.
2. Maintain an array `core_locked_time`, initially all zeros. A value of zero means the core is still active.
3. Maintain a boolean array `cell_locked`, initially false for every memory cell.
4. Process cycles from 1 to `m`.
5. For the current cycle, create a mapping from memory cell to the list of active cores attempting to write there during this cycle.
6. Iterate through all cores.

If a core is already locked, ignore it.

If its command is 0, ignore it.

If it tries to write into a locked cell, record the current cycle as its lock time immediately.

Otherwise, add the core to the request list of the target cell.
7. After all active cores have been examined, inspect every cell that received requests during this cycle.
8. If a cell has requests from at least two cores, a conflict occurs.

Mark the cell as locked.

Every participating core becomes locked during the current cycle.
9. Continue with the next cycle.
10. After all cycles are processed, output the recorded lock time for every core.

### Why it works

At the beginning of each cycle, the algorithm's state exactly matches the processor state described in the problem. Every locked core is excluded from further execution, and every locked cell is remembered.

When an active core writes to a locked cell, the statement says that it becomes locked immediately. Step 6 performs exactly this action.

For unlocked cells, all write requests from the current cycle are collected before any conflict decisions are made. This matches the simultaneous nature of a cycle. A cell is locked if and only if at least two active cores attempt to write to it during that cycle, and every participating core receives the current cycle as its lock time.

Since every rule from the statement is applied exactly once and in the correct temporal order, the simulation always produces the same state transitions as the real processor. Consequently, the recorded lock times are correct.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    cmds = [list(map(int, input().split())) for _ in range(n)]

    lock_time = [0] * n
    cell_locked = [False] * (k + 1)

    for cycle in range(1, m + 1):
        requests = defaultdict(list)

        for core in range(n):
            if lock_time[core] != 0:
                continue

            cell = cmds[core][cycle - 1]

            if cell == 0:
                continue

            if cell_locked[cell]:
                lock_time[core] = cycle
            else:
                requests[cell].append(core)

        for cell, cores in requests.items():
            if len(cores) >= 2:
                cell_locked[cell] = True

                for core in cores:
                    if lock_time[core] == 0:
                        lock_time[core] = cycle

    sys.stdout.write("\n".join(map(str, lock_time)) + "\n")

if __name__ == "__main__":
    solve()
```

The `lock_time` array serves two purposes. A value of zero means the core is still active, while a positive value records the first cycle in which it became locked.

The first pass through the cores handles immediate locks caused by writes into already locked cells. Those cores are not inserted into the request lists because they never successfully participate in the current cycle.

The second pass examines grouped requests. Since all requests were collected before checking for conflicts, simultaneous writes are handled correctly. This avoids the common bug of processing writes one by one and accidentally giving priority to whichever core happens to be visited first.

The condition `if lock_time[core] == 0` inside the conflict loop is defensive. In practice, a core in the request list cannot already be locked during the same cycle, but the check makes the logic explicit and preserves the "first lock time" property.

## Worked Examples

### Example 1

Input:

```
4 3 5
1 0 0
1 0 2
2 3 1
3 2 0
```

Cycle-by-cycle trace:

| Cycle | Requests Before Conflict | Locked Cells After Cycle | Newly Locked Cores |
| --- | --- | --- | --- |
| 1 | 1 → {1,2}, 2 → {3}, 3 → {4} | {1} | 1, 2 |
| 2 | 3 → {3}, 2 → {4} | {1} | none |
| 3 | 1 → {3} | {1} | 3 |

Final lock times:

| Core | Lock Time |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 3 |
| 4 | 0 |

Output:

```
1
1
3
0
```

This example demonstrates both kinds of locking. Cores 1 and 2 are locked by a simultaneous conflict, while core 3 is later locked because it attempts to write into the already locked cell 1.

### Example 2

Input:

```
3 2 2
1 0
1 2
2 1
```

Trace:

| Cycle | Requests Before Conflict | Locked Cells After Cycle | Newly Locked Cores |
| --- | --- | --- | --- |
| 1 | 1 → {1,2}, 2 → {3} | {1} | 1, 2 |
| 2 | 1 → {3} | {1} | 3 |

Final lock times:

| Core | Lock Time |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 0 |

Output:

```
1
1
0
```

This trace shows that only active cores continue participating after a conflict. The first two cores disappear from future processing immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each instruction is examined at most once |
| Space | O(n + k) | Stores lock status and per-cycle request groups |

The maximum input size contains only 10,000 instructions. An $O(nm)$ simulation performs at most 10,000 instruction evaluations plus small bookkeeping overhead, which is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    cmds = [list(map(int, input().split())) for _ in range(n)]

    lock_time = [0] * n
    cell_locked = [False] * (k + 1)

    for cycle in range(1, m + 1):
        requests = defaultdict(list)

        for core in range(n):
            if lock_time[core]:
                continue

            cell = cmds[core][cycle - 1]

            if cell == 0:
                continue

            if cell_locked[cell]:
                lock_time[core] = cycle
            else:
                requests[cell].append(core)

        for cell, cores in requests.items():
            if len(cores) >= 2:
                cell_locked[cell] = True
                for core in cores:
                    if lock_time[core] == 0:
                        lock_time[core] = cycle

    return "\n".join(map(str, lock_time))

# provided sample
assert run(
"""4 3 5
1 0 0
1 0 2
2 3 1
3 2 0
"""
) == "1\n1\n3\n0", "sample 1"

# minimum size
assert run(
"""1 1 1
0
"""
) == "0", "single core does nothing"

# immediate conflict
assert run(
"""2 1 1
1
1
"""
) == "1\n1", "simultaneous write conflict"

# write into previously locked cell
assert run(
"""3 2 1
1 0
1 0
0 1
"""
) == "1\n1\n2", "later access to locked cell"

# no conflicts ever
assert run(
"""3 3 3
1 1 1
2 2 2
3 3 3
"""
) == "0\n0\n0", "all writes distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single core, one idle cycle | 0 | Minimum input size |
| Two cores write same cell | 1, 1 | Simultaneous conflict handling |
| Access locked cell later | 1, 1, 2 | Immediate locking on locked-cell access |
| Distinct cells throughout | 0, 0, 0 | No false positives |

## Edge Cases

Consider the simultaneous conflict case:

```
2 1 1
1
1
```

During cycle 1, both active cores request cell 1. The request list for cell 1 contains two cores, so the algorithm locks the cell and both cores. The output is:

```
1
1
```

Because requests are grouped before conflicts are processed, neither core receives priority.

Now consider writing into a cell that was already locked:

```
3 2 1
1 0
1 0
0 1
```

Cycle 1 creates a conflict on cell 1. Cores 1 and 2 lock, and cell 1 becomes locked.

During cycle 2, core 3 attempts to write into cell 1. The algorithm detects that the destination cell is already locked and immediately assigns lock time 2 to core 3.

Output:

```
1
1
2
```

Finally, consider already locked cores receiving future commands:

```
2 2 1
1 0
1 1
```

Cycle 1 locks both cores and cell 1. During cycle 2, the second core's command is ignored because its lock time is already recorded. The algorithm never processes instructions from locked cores again.

Output:

```
1
1
```

This matches the processor specification exactly and prevents double-counting or changing a core's lock time after it has already become locked.
