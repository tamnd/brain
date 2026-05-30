---
title: "CF 471A - MUH and Sticks"
description: "We are given exactly six stick lengths. To build an animal, four of the sticks must be used as legs, which means those four sticks must all have the same length. After choosing the four leg sticks, two sticks remain. These determine the animal type."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 471
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 269 (Div. 2)"
rating: 1100
weight: 471
solve_time_s: 81
verified: true
draft: false
---

[CF 471A - MUH and Sticks](https://codeforces.com/problemset/problem/471/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given exactly six stick lengths. To build an animal, four of the sticks must be used as legs, which means those four sticks must all have the same length.

After choosing the four leg sticks, two sticks remain. These determine the animal type.

For an elephant, the remaining two sticks must have equal lengths, because the head and body are the same size.

For a bear, the remaining two sticks must have different lengths, because the head must be shorter than the body.

Our task is to determine whether the six sticks can form a bear, an elephant, or neither. The statement guarantees that both animals cannot be possible at the same time.

The constraints are tiny. There are only six sticks and each length is between 1 and 9. Any reasonable algorithm will run instantly. The challenge is not performance but correctly identifying which four sticks should be chosen as legs when multiple equal lengths exist.

A common mistake is to look only for a value appearing exactly four times. The legs only require four equal sticks, so a value appearing five or six times can also provide the legs.

Consider:

```
4 4 4 4 4 5
```

We can use four of the five sticks of length 4 as legs. The remaining sticks are 4 and 5, which are different, so the answer is `Bear`. A check for "exactly four occurrences" would incorrectly reject this case.

Another subtle case occurs when six sticks are identical:

```
3 3 3 3 3 3
```

Four sticks become legs, leaving two sticks of length 3 and 3. Since the remaining sticks are equal, the correct answer is `Elephant`.

A third tricky situation is when no length appears at least four times:

```
1 2 3 4 5 6
```

No four equal sticks exist, so no animal can be formed. The answer is `Alien`.

## Approaches

The brute-force idea is to try every possible choice of four sticks among the six. There are only C(6,4) = 15 possibilities. For each selection, check whether the chosen sticks have equal lengths. If they do, inspect the two remaining sticks. Equal remaining lengths mean an elephant, different remaining lengths mean a bear.

This approach is correct because it directly tests every valid way to choose the legs. With only 15 combinations, it is easily fast enough.

The problem becomes even simpler when we focus on frequencies. The only thing that matters is whether some length appears at least four times. If no such length exists, the answer is immediately `Alien`.

Once we find a length occurring at least four times, we remove exactly four copies of it. Only two sticks remain. Their relationship completely determines the answer. Equal lengths give `Elephant`, different lengths give `Bear`.

This observation removes the need to enumerate combinations and leads to a very short implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(6,4)) = O(1) | O(1) | Accepted |
| Optimal | O(6 log 6) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the six stick lengths.
2. Count how many times each length appears.
3. Find a length whose frequency is at least 4.

Such a length can provide the four required leg sticks.
4. If no length has frequency at least 4, print `Alien`.

Without four equal sticks, constructing either animal is impossible.
5. Remove exactly four occurrences of the chosen length.

We are fixing those four sticks as the legs.
6. Collect the two remaining sticks.
7. If the remaining two lengths are equal, print `Elephant`.

Equal head and body lengths match the elephant definition.
8. Otherwise print `Bear`.

Different remaining lengths match the bear definition.

### Why it works

The defining requirement for both animals is the existence of four equal-length leg sticks. Any valid construction must use four sticks of the same length, so some length must occur at least four times.

After selecting four such sticks, exactly two sticks remain. The animal type depends only on these two sticks. Equal remaining lengths satisfy the elephant condition, while different remaining lengths satisfy the bear condition. Since the statement guarantees the answer is unique, examining any length with frequency at least four yields the correct classification.

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline

sticks = list(map(int, input().split()))
cnt = Counter(sticks)

leg_length = None

for length, freq in cnt.items():
    if freq >= 4:
        leg_length = length
        break

if leg_length is None:
    print("Alien")
else:
    remaining = []
    removed = 0

    for x in sticks:
        if x == leg_length and removed < 4:
            removed += 1
        else:
            remaining.append(x)

    if remaining[0] == remaining[1]:
        print("Elephant")
    else:
        print("Bear")
```

The first part counts occurrences of each stick length. We then search for any length appearing at least four times. If none exists, we immediately know no valid set of legs can be formed.

The removal step deserves attention. We remove exactly four copies, not all copies. Cases such as `4 4 4 4 4 5` depend on keeping the fifth stick. Removing all occurrences would leave only one remaining stick and produce an incorrect result.

After removal, exactly two sticks remain. Comparing those two values directly determines the animal type.

No sorting is required, although a sorting-based solution would also be accepted.

## Worked Examples

### Sample 1

Input:

```
4 2 5 4 4 4
```

| Step | State |
| --- | --- |
| Count frequencies | {4:4, 2:1, 5:1} |
| Leg length found | 4 |
| Remove four 4's | Remaining = [2, 5] |
| Compare remaining sticks | 2 ≠ 5 |
| Output | Bear |

The four sticks of length 4 become the legs. The remaining sticks are different lengths, so they represent a bear's head and body.

### Example 2

Input:

```
3 3 3 3 5 5
```

| Step | State |
| --- | --- |
| Count frequencies | {3:4, 5:2} |
| Leg length found | 3 |
| Remove four 3's | Remaining = [5, 5] |
| Compare remaining sticks | 5 = 5 |
| Output | Elephant |

The remaining two sticks are equal, matching the elephant requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only six sticks are processed |
| Space | O(1) | Frequency table stores at most nine lengths |

The input size is fixed at six elements, so the algorithm performs only a handful of operations. It easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import Counter

def solve():
    sticks = list(map(int, input().split()))
    cnt = Counter(sticks)

    leg_length = None

    for length, freq in cnt.items():
        if freq >= 4:
            leg_length = length
            break

    if leg_length is None:
        print("Alien")
        return

    remaining = []
    removed = 0

    for x in sticks:
        if x == leg_length and removed < 4:
            removed += 1
        else:
            remaining.append(x)

    print("Elephant" if remaining[0] == remaining[1] else "Bear")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4 2 5 4 4 4\n") == "Bear", "sample 1"

# custom cases
assert run("3 3 3 3 5 5\n") == "Elephant", "equal remaining sticks"
assert run("1 2 3 4 5 6\n") == "Alien", "no four equal sticks"
assert run("4 4 4 4 4 5\n") == "Bear", "frequency greater than four"
assert run("9 9 9 9 9 9\n") == "Elephant", "all sticks equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3 3 3 5 5` | `Elephant` | Equal remaining sticks |
| `1 2 3 4 5 6` | `Alien` | No valid leg set exists |
| `4 4 4 4 4 5` | `Bear` | Must remove exactly four copies, not all |
| `9 9 9 9 9 9` | `Elephant` | All sticks identical |

## Edge Cases

Consider:

```
4 4 4 4 4 5
```

The frequency of 4 is 5, which is still sufficient for the legs. The algorithm removes exactly four copies of 4, leaving `[4, 5]`. Since the remaining sticks differ, it outputs `Bear`. Any solution requiring a frequency of exactly four would fail here.

Consider:

```
3 3 3 3 3 3
```

The algorithm chooses 3 as the leg length and removes four copies. The remaining sticks are `[3, 3]`. Because they are equal, the output is `Elephant`. This confirms correct handling when all six sticks have the same length.

Consider:

```
1 2 3 4 5 6
```

No length appears at least four times. The search for a leg length fails, so the algorithm immediately prints `Alien`. This correctly handles inputs where constructing any animal is impossible.
