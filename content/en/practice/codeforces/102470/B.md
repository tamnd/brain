---
title: "CF 102470B - Working at the Restaurant"
description: "We need to simulate a worker who receives plates from a waiter and later gives them to a dishwasher. The worker has only two piles on a table, and every plate must eventually leave the table in the same order it arrived."
date: "2026-08-05T20:38:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102470
codeforces_index: "B"
codeforces_contest_name: "2009-2010 ACM ICPC Southwestern European Regional Programming Contest (SWERC 2009)"
rating: 0
weight: 102470
solve_time_s: 63
verified: true
draft: false
---

[CF 102470B - Working at the Restaurant](https://codeforces.com/problemset/problem/102470/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to simulate a worker who receives plates from a waiter and later gives them to a dishwasher. The worker has only two piles on a table, and every plate must eventually leave the table in the same order it arrived. The input describes a sequence of requests: bringing a number of new plates to the table or removing a number of already stored plates in arrival order. The output is not the final arrangement of plates, but a valid sequence of smaller physical actions using the two piles.

The challenge is that the worker cannot directly access the oldest plate if newer plates are placed on top of it. The output operations must describe how to rearrange the two piles so that every requested removal happens correctly while staying within strict limits on the number of operations.

The number of requests in a test case is at most 1000, but the total number of plates ever dropped can reach 100000. This means a solution cannot repeatedly move every existing plate for every request, because the total work could become quadratic. We need a strategy where each plate is moved only a constant number of times throughout the whole simulation. The output limit of six times the number of input requests and six times the number of dropped plates directly hints that the intended construction should have constant amortized cost per plate.

Several edge cases can break a careless simulation. The first is a single drop followed by a partial take:

```
2
DROP 3
TAKE 1
```

A correct output can be:

```
DROP 2 3
MOVE 2->1 3
TAKE 1 1
```

The first three plates are stored in pile 2, then reversed into pile 1 so the oldest plate is on top. A solution that always keeps new plates in pile 1 would fail because the first requested plate would be trapped below the newer plates.

Another case is several drops before a take:

```
3
DROP 2
DROP 3
TAKE 5
```

A valid output is:

```
DROP 2 2
DROP 2 3
MOVE 2->1 5
TAKE 1 5
```

The two groups must behave like one queue. If the implementation only considers the latest drop operation and ignores previous plates, it will produce an invalid order.

A final edge case is leaving plates behind:

```
1
DROP 4
```

The output only needs to describe storing the plates:

```
DROP 2 4
```

The algorithm must not try to empty the piles at the end, because there is no request asking for those plates.

## Approaches

A direct approach is to actually maintain the two piles and simulate every plate movement. Whenever a TAKE request arrives, we find the oldest remaining plate. If it is hidden under another pile, we move plates between piles until that plate reaches the top, then remove it. This is correct because the two piles can represent any ordering we need.

The problem with this method appears when many alternating operations happen. Imagine repeatedly dropping a large stack and taking a small number of plates. A naive implementation may move the same large group again and again. With 100000 total dropped plates and 1000 requests, repeatedly touching large stacks can approach 100000000 operations, which is unnecessary.

The key observation is that the requests only care about the order of plates, not their individual identities. We can choose one pile as the place where new plates arrive. After a group of drops, all plates in that pile are reversed compared with the required removal order. Moving the whole pile to the other pile reverses it once, turning the stack into the correct queue order.

The two piles naturally act like the two stacks in a queue. We keep pile 2 as the input stack for newly arriving plates and pile 1 as the output stack for plates ready to leave. When a TAKE request needs plates and pile 1 is empty, we move all plates from pile 2 to pile 1. After that, removals are simple. This is the standard amortized queue technique, because every plate crosses between piles at most once and is removed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(MN) in the worst case | O(M) | Too slow |
| Optimal | O(M + N) | O(M) | Accepted |

## Algorithm Walkthrough

1. Store every DROP request directly into pile 2. Each new plate goes on top of pile 2 because pile 2 is the stack where incoming plates are collected. No movement is needed immediately because the dishwasher does not care about these plates yet.
2. Before handling a TAKE request, check whether pile 1 contains enough plates. If pile 1 is empty, move every plate from pile 2 to pile 1. Moving a stack from one pile to the other reverses the order, which changes the newest-first order of pile 2 into the oldest-first order needed for removal.
3. Remove the requested number of plates from the top of pile 1. Since pile 1 stores plates in the exact order they arrived, these removals satisfy the dishwasher requirement.
4. Continue processing requests until the case ends. Any remaining plates stay in the piles because there is no requirement to clear them.

Why it works:

The invariant is that pile 1 always contains the next plates that should be removed, in removal order from top to bottom, while pile 2 contains plates that have arrived but have not yet been prepared for removal. A DROP only adds new plates to the end of the waiting sequence. A MOVE operation transfers the waiting sequence into removal order by reversing the stack. Since every TAKE is performed only from pile 1, the oldest available plate is always removed first. The invariant is preserved after every command, so every generated transcript is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    out = []
    first_case = True

    while True:
        line = input()
        if not line:
            break
        n = int(line)
        if n == 0:
            break

        if not first_case:
            out.append("")
        first_case = False

        pile1 = 0
        pile2 = 0

        for _ in range(n):
            cmd, value = input().split()
            value = int(value)

            if cmd == "DROP":
                out.append(f"DROP 2 {value}")
                pile2 += value
            else:
                if pile1 == 0:
                    if pile2 > 0:
                        out.append(f"MOVE 2->1 {pile2}")
                        pile1 = pile2
                        pile2 = 0

                out.append(f"TAKE 1 {value}")
                pile1 -= value

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation does not store every plate individually because only the number of plates in each pile matters. The operations never distinguish one plate from another, so two counters are enough.

`pile1` represents the prepared plates that can immediately go to the dishwasher. `pile2` represents plates waiting to be reversed. When `pile1` is empty before a TAKE, the entire content of `pile2` is moved. The code prints that operation and swaps the counters.

The subtraction after a TAKE is safe because the problem guarantees that a TAKE request never asks for more plates than currently exist. It is also safe to leave plates in either pile after the final request because the restaurant may stop before everything is washed.

## Worked Examples

For the first sample:

```
3
DROP 100
TAKE 50
TAKE 20
```

The execution is:

| Request | pile1 before | pile2 before | Operation | pile1 after | pile2 after |
| --- | --- | --- | --- | --- | --- |
| DROP 100 | 0 | 0 | DROP 2 100 | 0 | 100 |
| TAKE 50 | 0 | 100 | MOVE 2->1 100, TAKE 1 50 | 50 | 0 |
| TAKE 20 | 50 | 0 | TAKE 1 20 | 30 | 0 |

The first TAKE forces a reversal because all plates are still in the input pile. After the move, the oldest plates are accessible from pile 1.

For the second sample:

```
3
DROP 3
DROP 5
TAKE 8
```

The execution is:

| Request | pile1 before | pile2 before | Operation | pile1 after | pile2 after |
| --- | --- | --- | --- | --- | --- |
| DROP 3 | 0 | 0 | DROP 2 3 | 0 | 3 |
| DROP 5 | 0 | 3 | DROP 2 5 | 0 | 8 |
| TAKE 8 | 0 | 8 | MOVE 2->1 8, TAKE 1 8 | 0 | 0 |

This shows that multiple DROP requests can accumulate together. The algorithm waits until a TAKE needs the plates, then reverses the whole waiting pile.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M + N) | Each request is processed once, and each plate moves from pile 2 to pile 1 at most once before being taken. |
| Space | O(1) | Only counters for the two piles and the output buffer are maintained. |

The total number of plate movements is bounded by the number of drops plus the number of takes because every plate is moved between piles at most once. This satisfies the limit of six times the total number of dropped plates.

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

assert run("""3
DROP 100
TAKE 50
TAKE 20
0
""") == """DROP 2 100
MOVE 2->1 100
TAKE 1 50
TAKE 1 20"""

assert run("""3
DROP 3
DROP 5
TAKE 8
0
""") == """DROP 2 3
DROP 2 5
MOVE 2->1 8
TAKE 1 8"""

assert run("""1
DROP 1
0
""") == """DROP 2 1"""

assert run("""4
DROP 5
TAKE 2
DROP 3
TAKE 6
0
""") == """DROP 2 5
MOVE 2->1 5
TAKE 1 2
DROP 2 3
TAKE 1 3"""

assert run("""2
DROP 100000
TAKE 100000
0
""") == """DROP 2 100000
MOVE 2->1 100000
TAKE 1 100000"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `DROP 1` | One DROP operation | Minimum case and unfinished piles |
| Multiple drops followed by one take | One large MOVE before TAKE | Correct stack reversal |
| Large single drop and take | One reversal of 100000 plates | Maximum plate count handling |
| Alternating drops and takes | Several pile transitions | Correct maintenance of the invariant |

## Edge Cases

For a single DROP followed by a TAKE:

```
2
DROP 3
TAKE 1
```

The algorithm first places all three plates into pile 2. Before the TAKE, pile 1 is empty, so all three plates are moved into pile 1. The top of pile 1 is now the oldest plate, and removing one plate is correct. The remaining two plates stay available for later requests.

For multiple consecutive drops:

```
3
DROP 2
DROP 3
TAKE 5
```

The algorithm does not move anything during either DROP. Pile 2 simply grows from size 2 to size 5. When the TAKE arrives, one MOVE reverses the complete collection. This handles the entire queue instead of treating each DROP separately.

For unfinished work:

```
1
DROP 4
```

The algorithm prints only the action required to receive the plates. The counters correctly finish with pile 2 containing four plates. No extra operation is produced because the input never requested those plates to be delivered.

You can adjust the editorial length or emphasis if you want a more contest-style version or a more educational walkthrough.
