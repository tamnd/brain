---
title: "CF 120A - Elevator"
description: "We are given two pieces of information about a person riding an elevator. The first input tells us which door the person used to enter, either the front door or the back door. The second input tells us which rail the person was holding, rail 1 or rail 2."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 120
codeforces_index: "A"
codeforces_contest_name: "School Regional Team Contest, Saratov, 2011"
rating: 1000
weight: 120
solve_time_s: 86
verified: true
draft: false
---

[CF 120A - Elevator](https://codeforces.com/problemset/problem/120/A)

**Rating:** 1000  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two pieces of information about a person riding an elevator.

The first input tells us which door the person used to enter, either the front door or the back door. The second input tells us which rail the person was holding, rail 1 or rail 2.

The elevator is symmetric, but the meaning of "left" and "right" changes depending on which side a person enters from. Rail 1 is on the left side when entering through the front door, but on the right side when entering through the back door. Since people hold the rail with their stronger hand, we must determine whether the VIP is left-handed or right-handed.

The constraints are extremely small. There are only four possible input combinations:

- front + rail 1
- front + rail 2
- back + rail 1
- back + rail 2

Any constant-time solution is more than fast enough. Even a brute-force lookup over all possibilities easily fits within the limits.

The main difficulty is not performance, but avoiding confusion about the orientation of the elevator. A careless implementation may assume that rail numbers always correspond to the same physical side, which is false because the perspective changes when entering from the opposite door.

One easy mistake happens with this input:

```
back
1
```

The correct answer is:

```
R
```

Someone entering through the back sees rail 1 on their right side, not their left. A solution that always maps rail 1 to the left hand would incorrectly print `L`.

Another tricky case is:

```
front
2
```

The correct answer is:

```
R
```

From the front entrance, rail 2 is on the rider's right side. Forgetting to switch between left and right based on the rail number would produce the wrong result.

## Approaches

The brute-force approach is to manually encode every possible configuration. Since there are only four cases, we can directly write conditional statements for each one.

For example:

- `front + 1 -> L`
- `front + 2 -> R`
- `back + 1 -> R`
- `back + 2 -> L`

This works because the input space is tiny. The time complexity is constant because we only evaluate a few comparisons.

Even though the brute-force solution is already accepted, we can simplify the logic further by observing the pattern behind the cases.

When entering from the front, the rail number directly matches the side:

- rail 1 means left hand
- rail 2 means right hand

When entering from the back, the orientation reverses:

- rail 1 becomes right hand
- rail 2 becomes left hand

The key observation is that the answer depends on whether the rail appears on the rider's left or right from their current perspective. The entrance direction completely determines whether the mapping is normal or reversed.

That lets us reduce the problem to one simple conditional structure instead of treating all four combinations independently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the entrance door as a string.

The value is either `"front"` or `"back"`.
2. Read the rail number.

The value is either `1` or `2`.
3. If the person entered through the front door, interpret the rails normally.

Rail 1 is on the left side, so print `L`.

Rail 2 is on the right side, so print `R`.
4. If the person entered through the back door, reverse the interpretation.

Rail 1 is now on the right side, so print `R`.

Rail 2 is now on the left side, so print `L`.

### Why it works

The elevator geometry is fixed, but the rider's perspective changes depending on which entrance they use. Entering from opposite sides swaps the meaning of left and right.

The algorithm correctly models this perspective change. For the front entrance, rail numbering matches the natural left-to-right order. For the back entrance, the order reverses. Since the rider always holds the rail with the stronger hand, identifying the side of the rail directly identifies whether the rider is left-handed or right-handed.

## Python Solution

```python
import sys
input = sys.stdin.readline

door = input().strip()
rail = int(input())

if door == "front":
    if rail == 1:
        print("L")
    else:
        print("R")
else:
    if rail == 1:
        print("R")
    else:
        print("L")
```

The program starts by reading the entrance direction and rail number.

The first conditional separates the two possible perspectives of the rider. Inside each branch, the rail number determines whether the rail is on the rider's left or right side.

The implementation stays explicit instead of compressing everything into a single expression. For a small implementation problem like this, clarity is more valuable than cleverness.

The `.strip()` call is important because the input line contains a trailing newline character. Without removing it, comparisons such as `door == "front"` would fail.

There are no boundary issues or overflow concerns because the input domain is extremely small.

## Worked Examples

### Example 1

Input:

```
front
1
```

| Step | door | rail | Interpretation | Output |
| --- | --- | --- | --- | --- |
| Read input | front | 1 | Front entrance keeps orientation |  |
| Determine side | front | 1 | Rail 1 is left side | L |

Final output:

```
L
```

This example demonstrates the normal orientation case. Entering from the front means rail numbering follows the natural left-to-right layout.

### Example 2

Input:

```
back
1
```

| Step | door | rail | Interpretation | Output |
| --- | --- | --- | --- | --- |
| Read input | back | 1 | Back entrance reverses orientation |  |
| Determine side | back | 1 | Rail 1 becomes right side | R |

Final output:

```
R
```

This example demonstrates the critical perspective reversal. The same rail number corresponds to the opposite hand because the rider entered from the opposite side.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few comparisons are performed |
| Space | O(1) | No additional data structures are used |

The solution easily fits within the limits because it performs constant work regardless of input. Memory usage is also constant since only two variables are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    door = input().strip()
    rail = int(input())

    if door == "front":
        if rail == 1:
            print("L")
        else:
            print("R")
    else:
        if rail == 1:
            print("R")
        else:
            print("L")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("front\n1\n") == "L\n", "sample 1"

# custom cases
assert run("front\n2\n") == "R\n", "front entrance, right rail"
assert run("back\n1\n") == "R\n", "back entrance reverses orientation"
assert run("back\n2\n") == "L\n", "back entrance with second rail"
assert run("front\n1\n") == "L\n", "minimum valid configuration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `front 2` | `R` | Correct mapping for front entrance |
| `back 1` | `R` | Perspective reversal handling |
| `back 2` | `L` | Reverse orientation for second rail |
| `front 1` | `L` | Basic left-side mapping |

## Edge Cases

Consider this input:

```
back
1
```

The algorithm enters the `"back"` branch. Inside that branch, rail 1 maps to the right side because the rider is facing the opposite direction compared to the front entrance.

Execution trace:

- `door = "back"`
- `rail = 1`
- enter back-door logic
- rail 1 corresponds to right hand
- print `R`

The output is:

```
R
```

This case catches solutions that forget to reverse orientation for the back entrance.

Now consider:

```
front
2
```

Execution trace:

- `door = "front"`
- `rail = 2`
- enter front-door logic
- rail 2 corresponds to right hand
- print `R`

The output is:

```
R
```

This case verifies that the normal orientation mapping is handled correctly.

Finally, consider:

```
back
2
```

Execution trace:

- `door = "back"`
- `rail = 2`
- enter back-door logic
- rail 2 corresponds to left hand
- print `L`

The output is:

```
L
```

This confirms that both the entrance direction and rail number are handled together correctly, rather than independently.
