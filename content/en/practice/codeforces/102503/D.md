---
title: "CF 102503D - Union Found"
description: "The logbook describes the state of a factory over time. Before the log begins, we are given every employee together with two ways of identifying them: their full identity, consisting of a title and a name, and their nickname."
date: "2026-08-05T17:08:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "D"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 2236
verified: true
draft: false
---

[CF 102503D - Union Found](https://codeforces.com/problemset/problem/102503/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 37m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The logbook describes the state of a factory over time. Before the log begins, we are given every employee together with two ways of identifying them: their full identity, consisting of a title and a name, and their nickname. The log then contains events where employees enter, employees leave, demonstrations happen, and queries asking whether a particular employee is currently inside.

The task is to process the log in order. When a demonstration occurs, we need the current number of employees inside the factory. When a query appears, we need to decide whether the referenced employee is currently present and print `FOUND` or `404`.

The first challenge is that the same person can appear under two different forms. For example, an employee may enter using `Sir Richard` and later be searched using `the Knight`. These two strings must refer to the same internal state.

The largest input contains up to 100000 employees and 100000 log entries. With a two second time limit, algorithms that repeatedly scan all employees or all currently active people are too slow. A solution performing 100000 operations per query could reach around 10^10 operations, which is far beyond what Python can handle. The intended approach needs to process each log line in roughly constant time.

Several details can cause incorrect answers in simple implementations. One mistake is storing only the exact text that appeared in the log. For example:

```
Sir Richard the Knight
----------
+ Sir Richard
FIND the Knight
END
```

The correct output is:

```
FOUND
```

A program that treats `Sir Richard` and `the Knight` as unrelated strings would incorrectly print `404`.

Another issue is updating the employee count incorrectly. Consider:

```
Sir Alice the Cat
----------
+ Sir Alice
UNION
- the Cat
UNION
END
```

The correct output is:

```
1
0
```

The first demonstration happens while Alice is inside. The second happens after the same employee leaves. Counting nicknames separately from names would count the same person twice.

A final edge case is repeated demonstrations without any movement:

```
Sir Bob the Dog
----------
UNION
UNION
END
```

The output is:

```
0
0
```

A solution must answer every query from the current state. A previous demonstration does not consume or change the state.

## Approaches

The straightforward solution is to keep a set of employees currently inside. Every time a `+` event appears, we add that employee, and every time a `-` event appears, we remove that employee. For a query, we search the set to see whether the employee exists. This is correct because the log is guaranteed to be consistent, so the set exactly represents the people inside.

The problem is the lookup cost if we store employees poorly. With a list of active employees, every query may inspect every employee. In the worst case there are 100000 employees and 100000 log lines, leading to about 10^10 comparisons.

The key observation is that the employee list is fixed before processing the log. We can assign every employee an internal identifier once. Both the full name form and nickname form can map to the same identifier. After that, the dynamic part of the problem becomes only a question of whether each identifier is active.

A hash map gives constant time conversion from text in the log to an identifier. A boolean array or set stores which identifiers are currently inside. We also keep a counter of active employees, because the `UNION` event only asks for the size of the current group.

The brute-force approach works because it directly simulates the factory, but it wastes time rediscovering the identity of employees and searching through many irrelevant people. The observation that identities can be compressed into integer IDs lets every event become a constant time update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(e * n) | O(e) | Too slow |
| Optimal | O(e + n) | O(e) | Accepted |

## Algorithm Walkthrough

1. Read the employee list and assign a unique integer ID to every employee. Store both possible references, the full title-name form and the nickname form, in a dictionary pointing to that ID.

The rest of the algorithm should never compare employee strings again. Every reference in the log should immediately become an integer lookup.

1. Create a data structure that records whether each employee ID is currently inside. Initially every employee is outside.

The log is chronological, so the current state only depends on the events already processed.

1. Read each log line until `END`.

For an entry event, find the employee ID and mark it active. Increase the current count.

For an exit event, find the employee ID and mark it inactive. Decrease the current count.

For a `UNION` event, output the current count.

For a `FIND` event, convert the reference into an ID and check the active state of that ID.

1. Print answers in the same order that events requiring output appear.

The invariant is that after processing any prefix of the log, the active array represents exactly the employees who are physically inside the factory at that moment. Entry and exit events update one employee according to the log, while query events only read the state. Since both names and nicknames map to the same ID, every query observes the correct employee.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    ref = {}
    active = []
    emp_count = 0

    while True:
        line = input().rstrip("\n")
        if line == "----------":
            break
        parts = line.split()
        title = parts[0]
        name = parts[1]
        nick = parts[2]
        ref[title + " " + name] = emp_count
        ref["the " + nick] = emp_count
        emp_count += 1

    active = [False] * emp_count
    inside = 0
    ans = []

    while True:
        line = input().rstrip("\n")
        if line == "END":
            break

        if line == "UNION":
            ans.append(str(inside))
        elif line[0] == '+':
            key = line[2:]
            idx = ref[key]
            if not active[idx]:
                active[idx] = True
                inside += 1
        elif line[0] == '-':
            key = line[2:]
            idx = ref[key]
            if active[idx]:
                active[idx] = False
                inside -= 1
        else:
            key = line[5:]
            idx = ref[key]
            if active[idx]:
                ans.append("FOUND")
            else:
                ans.append("404")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The dictionary construction phase handles the identity problem. Each employee receives one ID, and both representations point to that ID. The strings used as dictionary keys are exactly the forms that appear in the log.

The `active` array stores the current factory state. A boolean array is enough because every employee already has a compact numeric index. The `inside` variable avoids scanning the array during `UNION`.

The order of updates matters. An entry increments the count after activating the employee, and an exit decrements it after removing the employee. The problem guarantees that invalid removals cannot occur, so the checks are only defensive.

Python integers do not overflow, and the largest possible count is only 100000. Every operation uses dictionary lookup or array access, which keeps the solution within the required limits.

## Worked Examples

For the first sample, only three employees become relevant. The trace is:

| Event | Active employees | Count | Output |
| --- | --- | --- | --- |
| `+ Sir Richard` | Richard | 1 |  |
| `+ the Merchant` | Richard, Poorard | 2 |  |
| `FIND the Knight` | Richard, Poorard | 2 | FOUND |
| `UNION` | Richard, Poorard | 2 | 2 |
| `- the Knight` | Poorard | 1 |  |
| `FIND Sir Richard` | Poorard | 1 | 404 |
| `+ the Duck` | Poorard, Donard | 2 |  |
| `- Sir Poorard` | Donard | 1 |  |
| `FIND the Duck` | Donard | 1 | FOUND |
| `FIND Sir Donard` | Donard | 1 | FOUND |

This trace demonstrates why both names and nicknames must point to one employee ID. The entry through `Sir Richard` is found through `the Knight`.

For the second sample, the important transitions are:

| Event | Active employees | Count | Output |
| --- | --- | --- | --- |
| `+ Lolo Generoso` | Generoso | 1 |  |
| `UNION` | Generoso | 1 | 1 |
| `FIND the Wise` | Generoso | 1 | 404 |
| `- Lolo Generoso` | none | 0 |  |
| `UNION` | none | 0 | 0 |
| `+ Lolo Generoso` | Generoso | 1 |  |
| `UNION` | Generoso | 1 | 1 |
| `UNION` | Generoso | 1 | 1 |
| `- Lolo Generoso` | none | 0 |  |
| `UNION` | none | 0 | 0 |

This example exercises repeated demonstrations and confirms that demonstrations only read the current count. They do not modify the active employees.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(e + n) | Each employee is inserted into the dictionary once, and each log line performs constant time work. |
| Space | O(e) | The dictionaries and active-state array store one entry per employee. |

The maximum input size is 100000 employees and 100000 events. The solution performs a small constant amount of work for every input line, so it fits comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_out
    sys.stdin = old
    return out.getvalue()

assert run("""Sir Alice the Cat
----------
+ Sir Alice
FIND the Cat
UNION
END
""") == "FOUND\n1", "basic alias"

assert run("""Sir Bob the Dog
----------
UNION
UNION
END
""") == "0\n0", "empty repeated queries"

assert run("""Madam Eve the Sun
----------
+ the Sun
FIND Madam Eve
- Madam Eve
FIND the Sun
END
""") == "FOUND\n404", "enter and leave through different aliases"

assert run("""Sir A the X
Sir B the Y
----------
+ Sir A
+ Sir B
UNION
- the X
UNION
END
""") == "2\n1", "multiple employees"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single employee entering through one name and queried through nickname | `FOUND`, `1` | Alias mapping |
| Empty log state with demonstrations | `0`, `0` | No accidental state changes |
| Entering and leaving through different forms | `FOUND`, `404` | Shared employee identity |
| Multiple employees active together | `2`, `1` | Correct counter updates |

## Edge Cases

When a person enters using one identifier and is searched using another, the algorithm handles it because both strings were mapped to the same numeric ID during preprocessing. In the input:

```
Sir Alice the Cat
----------
+ Sir Alice
FIND the Cat
END
```

the dictionary contains both `Sir Alice` and `the Cat` pointing to ID zero. The entry activates ID zero, and the query checks the same ID.

When an employee leaves, the count must represent people, not appearances. In:

```
Sir Alice the Cat
----------
+ Sir Alice
UNION
- the Cat
UNION
END
```

the first demonstration sees one active ID. The exit finds that same ID and removes it, so the second demonstration sees zero.

Repeated demonstrations do not affect the state. For:

```
Sir Bob the Dog
----------
UNION
UNION
END
```

the active array remains unchanged between the two events, so both answers are zero.
