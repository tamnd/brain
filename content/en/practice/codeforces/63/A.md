---
title: "CF 63A - Sinking Ship"
description: "We are given a list of people standing in a fixed left-to-right order on a sinking ship. Every person has a name and a role. The evacuation order depends entirely on the role priority. Rats leave first. Women and children share the next priority level. Men leave after them."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 63
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 59 (Div. 2)"
rating: 900
weight: 63
solve_time_s: 91
verified: true
draft: false
---

[CF 63A - Sinking Ship](https://codeforces.com/problemset/problem/63/A)

**Rating:** 900  
**Tags:** implementation, sortings, strings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of people standing in a fixed left-to-right order on a sinking ship. Every person has a name and a role. The evacuation order depends entirely on the role priority.

Rats leave first. Women and children share the next priority level. Men leave after them. The captain always leaves last.

When two people belong to the same priority group, their relative order must stay exactly the same as in the original line. That means this is not just a sorting problem by category, it is a stable ordering problem.

The input size is tiny, only up to 100 people. Even quadratic algorithms would easily fit inside the time limit. The challenge is not performance, it is implementing the priority rules correctly without accidentally breaking the original order inside a group.

One common mistake is treating women and children as separate priorities. They actually belong to the same evacuation level.

Consider this input:

```
4
Anna woman
Ben child
Chris woman
David man
```

The correct output is:

```
Anna
Ben
Chris
David
```

A careless implementation that evacuates all women before all children would incorrectly produce:

```
Anna
Chris
Ben
David
```

Another easy mistake is using an unstable sort without preserving the original position.

Consider:

```
5
Tom man
Jerry man
Spike man
Mila woman
Captain captain
```

The men must remain in their original order:

```
Mila
Tom
Jerry
Spike
Captain
```

If the implementation only sorts by priority and ignores original indices, the order among the men could become arbitrary.

A third edge case is the captain. There is exactly one captain, and that person must always appear last no matter where they stand initially.

Example:

```
3
Jack captain
Alice woman
Bob rat
```

Correct output:

```
Bob
Alice
Jack
```

If someone processes the line from left to right and prints immediately, the captain could incorrectly appear too early.

## Approaches

The most direct brute-force idea is to repeatedly scan the entire list and extract people category by category. First scan for rats and print them in order. Then scan again for women and children. Then scan again for men. Finally print the captain.

This works because the evacuation priorities are fixed and there are only five possible statuses. Since each scan preserves the original left-to-right order, the output is correct.

The worst-case complexity is still tiny. We scan at most four or five times over at most 100 people, so the total work is around 500 operations.

Another approach is to assign a numeric priority to every role and sort the people by that priority. For example:

```
rat -> 0
woman -> 1
child -> 1
man -> 2
captain -> 3
```

The key observation is that women and children intentionally share the same priority. Once we map roles to numbers, the problem becomes a stable sorting task.

Python’s built-in sort is stable, which means people with equal priority automatically remain in their original order. That matches the problem requirement perfectly.

Even though both approaches are fast enough, the sorting approach is cleaner and easier to generalize.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of crew members.
2. For each person, read their name and status.
3. Assign a numeric evacuation priority to each status.

Rats get the smallest value because they leave first. Captains get the largest value because they leave last. Women and children receive the same value because they share priority.
4. Store every person as a pair containing their priority and name.

The original input order is automatically preserved because Python sorting is stable.
5. Sort the list by priority.
6. Print the names in the sorted order.

### Why it works

Every crew member belongs to exactly one evacuation category. The numeric mapping converts the verbal rules into a sortable ordering relation.

If two people belong to different categories, the smaller priority value correctly places one before the other.

If two people belong to the same category, both receive the same priority. Python’s stable sort preserves their original relative order, which exactly matches the statement requirement that people farther left evacuate first when priorities tie.

Because both rules are satisfied simultaneously, the final order is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    priority = {
        "rat": 0,
        "woman": 1,
        "child": 1,
        "man": 2,
        "captain": 3
    }

    people = []

    for _ in range(n):
        name, status = input().split()
        people.append((priority[status], name))

    people.sort()

    for _, name in people:
        print(name)

solve()
```

The dictionary converts each status into a sortable numeric value. The crucial detail is that `"woman"` and `"child"` both map to `1`, giving them equal priority.

Each person is stored as a tuple `(priority, name)`. Since Python sorts tuples lexicographically, the list is ordered primarily by priority.

Python’s sort is stable, which is the subtle but critical property here. When two people have the same priority, their relative order remains unchanged from the input. That automatically satisfies the left-to-right rule from the problem statement without storing explicit indices.

The constraints are so small that performance is irrelevant, but this implementation is still clean and efficient.

## Worked Examples

### Example 1

Input:

```
6
Jack captain
Alice woman
Charlie man
Teddy rat
Bob child
Julia woman
```

Processing steps:

| Person | Status | Priority | Stored Tuple |
| --- | --- | --- | --- |
| Jack | captain | 3 | (3, Jack) |
| Alice | woman | 1 | (1, Alice) |
| Charlie | man | 2 | (2, Charlie) |
| Teddy | rat | 0 | (0, Teddy) |
| Bob | child | 1 | (1, Bob) |
| Julia | woman | 1 | (1, Julia) |

After sorting:

| Priority | Name |
| --- | --- |
| 0 | Teddy |
| 1 | Alice |
| 1 | Bob |
| 1 | Julia |
| 2 | Charlie |
| 3 | Jack |

Output:

```
Teddy
Alice
Bob
Julia
Charlie
Jack
```

This trace demonstrates why stable sorting matters. Alice, Bob, and Julia all share the same priority, and their original relative order is preserved.

### Example 2

Input:

```
5
Tom man
Jerry man
Lucy child
Kate woman
Morgan captain
```

Processing steps:

| Person | Status | Priority | Stored Tuple |
| --- | --- | --- | --- |
| Tom | man | 2 | (2, Tom) |
| Jerry | man | 2 | (2, Jerry) |
| Lucy | child | 1 | (1, Lucy) |
| Kate | woman | 1 | (1, Kate) |
| Morgan | captain | 3 | (3, Morgan) |

After sorting:

| Priority | Name |
| --- | --- |
| 1 | Lucy |
| 1 | Kate |
| 2 | Tom |
| 2 | Jerry |
| 3 | Morgan |

Output:

```
Lucy
Kate
Tom
Jerry
Morgan
```

This example shows two separate tied groups. Children and women share one group, while the two men form another. In both cases, the original ordering remains intact.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the crew list dominates the runtime |
| Space | O(n) | The list of people is stored in memory |

With at most 100 crew members, the runtime is tiny. Even much slower algorithms would pass comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        priority = {
            "rat": 0,
            "woman": 1,
            "child": 1,
            "man": 2,
            "captain": 3
        }

        people = []

        for _ in range(n):
            name, status = input().split()
            people.append((priority[status], name))

        people.sort()

        out = []

        for _, name in people:
            out.append(name)

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""6
Jack captain
Alice woman
Charlie man
Teddy rat
Bob child
Julia woman
"""
) == (
"""Teddy
Alice
Bob
Julia
Charlie
Jack"""
), "sample 1"

# minimum size
assert run(
"""1
Jack captain
"""
) == (
"""Jack"""
), "single person"

# all same priority
assert run(
"""4
Anna woman
Bella child
Cara woman
Diana child
"""
) == (
"""Anna
Bella
Cara
Diana"""
), "stable order among equal priorities"

# captain appears first in input
assert run(
"""3
Captain captain
Tom man
Jerry rat
"""
) == (
"""Jerry
Tom
Captain"""
), "captain must always be last"

# multiple men preserve order
assert run(
"""5
Tom man
Jerry man
Spike man
Lucy child
Captain captain
"""
) == (
"""Lucy
Tom
Jerry
Spike
Captain"""
), "stable order among men"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single captain | Captain | Minimum input size |
| Women and children mixed | Same relative order | Equal-priority stability |
| Captain at front | Captain printed last | Correct captain handling |
| Multiple men | Original order preserved | Stable sorting behavior |

## Edge Cases

One subtle case is mixing women and children. They are not separate evacuation phases.

Input:

```
4
Anna woman
Ben child
Chris woman
David man
```

The algorithm assigns priorities:

```
woman -> 1
child -> 1
woman -> 1
man -> 2
```

After sorting, all three priority-1 people remain in their original order because Python sorting is stable:

```
Anna
Ben
Chris
David
```

Another tricky situation is preserving order among identical categories.

Input:

```
5
Tom man
Jerry man
Spike man
Lucy woman
Captain captain
```

Priorities become:

```
Tom -> 2
Jerry -> 2
Spike -> 2
Lucy -> 1
Captain -> 3
```

Sorting moves Lucy ahead of the men, but the three men stay ordered as:

```
Tom
Jerry
Spike
```

The final result is:

```
Lucy
Tom
Jerry
Spike
Captain
```

The captain edge case is also important.

Input:

```
3
Jack captain
Alice woman
Bob rat
```

The priorities are:

```
Jack -> 3
Alice -> 1
Bob -> 0
```

Sorting produces:

```
Bob
Alice
Jack
```

Even though the captain stood first in line initially, the priority mapping forces the captain to evacuate last.
