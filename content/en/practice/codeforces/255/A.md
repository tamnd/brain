---
title: "CF 255A - Greg's Workout"
description: "Greg performs exercises in a fixed repeating order. The first exercise trains the chest, the second trains the biceps, the third trains the back, then the pattern repeats again: chest, biceps, back, and so on."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 255
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 156 (Div. 2)"
rating: 800
weight: 255
solve_time_s: 139
verified: true
draft: false
---

[CF 255A - Greg's Workout](https://codeforces.com/problemset/problem/255/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Greg performs exercises in a fixed repeating order. The first exercise trains the chest, the second trains the biceps, the third trains the back, then the pattern repeats again: chest, biceps, back, and so on.

We are given an array where the value at position `i` tells us how many repetitions Greg performs for the `i`-th exercise in this sequence. The task is to determine which muscle group receives the largest total number of repetitions after summing all exercises assigned to it.

The constraints are very small. The number of exercises is at most 20, and each repetition count is at most 25. Even a straightforward simulation is easily fast enough. There is no need for advanced data structures or optimization tricks. A simple linear scan over the array already fits comfortably within the limits.

The only subtle part is assigning each exercise to the correct muscle group. Since the pattern repeats every three exercises, the position modulo 3 determines the target muscle. A careless implementation can easily shift the mapping by one because array indices in programming are usually zero-based.

Consider this input:

```
3
10 1 20
```

The correct totals are:

- chest = 10
- biceps = 1
- back = 20

So the answer is `back`.

If someone uses `i % 3` incorrectly with one-based thinking, they might map the first exercise to biceps instead of chest and produce the wrong result.

Another easy mistake is forgetting that the sequence continues cyclically.

Example:

```
5
1 2 3 4 5
```

The assignments are:

- chest: exercises 1 and 4 → 1 + 4 = 5
- biceps: exercises 2 and 5 → 2 + 5 = 7
- back: exercise 3 → 3

The correct answer is `biceps`.

A buggy implementation that only handles the first three positions separately would fail here.

## Approaches

The brute-force idea is to explicitly simulate Greg's workout. For every exercise position, determine which muscle group it belongs to and add its repetitions to that muscle's total. After processing all exercises, compare the three totals and print the largest one.

This already works perfectly within the limits. At most we process 20 numbers, so the total work is tiny.

A more inefficient brute-force version could repeatedly build the cyclic sequence of muscle names and then count repetitions separately for each group. Even that would still pass because the input is so small, but it introduces unnecessary work and complexity.

The useful observation is that the exercise type depends entirely on the index modulo 3:

- indices 0, 3, 6, ... belong to chest
- indices 1, 4, 7, ... belong to biceps
- indices 2, 5, 8, ... belong to back

Once we recognize this repeating structure, the solution becomes a single linear pass with three accumulators.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the array of repetitions.
2. Create three variables to store the total repetitions for chest, biceps, and back.
3. Iterate through the array using zero-based indexing.
4. For each index:

- if `i % 3 == 0`, add the value to chest
- if `i % 3 == 1`, add the value to biceps
- otherwise, add the value to back

The modulo operation works because the exercise pattern repeats every three positions.
5. After processing all exercises, compare the three totals.
6. Print the muscle name with the largest total.

### Why it works

Every exercise belongs to exactly one muscle group, and the assignment follows a fixed cycle of length three. The modulo operation partitions all indices into those three groups correctly. During the scan, each repetition count is added exactly once to the correct total. After the loop finishes, the three accumulators represent the complete amount of training for each muscle group. Choosing the maximum among them gives the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

chest = 0
biceps = 0
back = 0

for i in range(n):
    if i % 3 == 0:
        chest += a[i]
    elif i % 3 == 1:
        biceps += a[i]
    else:
        back += a[i]

if chest > biceps and chest > back:
    print("chest")
elif biceps > chest and biceps > back:
    print("biceps")
else:
    print("back")
```

The program starts by reading the input array. Three accumulator variables track the total repetitions for each muscle group.

The loop processes exercises in order. Since Python uses zero-based indexing, index `0` corresponds to the first exercise, which is chest. That is why `i % 3 == 0` maps to chest rather than biceps.

The modulo pattern repeats every three indices, matching the workout cycle exactly.

At the end, the program compares the totals and prints the largest one. The problem guarantees that the answer is unique, so we do not need to handle ties.

## Worked Examples

### Example 1

Input:

```
2
2 8
```

| Index | Value | Muscle | Chest | Biceps | Back |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | chest | 2 | 0 | 0 |
| 1 | 8 | biceps | 2 | 8 | 0 |

Final totals:

- chest = 2
- biceps = 8
- back = 0

Output:

```
biceps
```

This example shows that the cycle can end before all three muscle groups appear. Back receives no exercises at all, which the algorithm handles naturally.

### Example 2

Input:

```
3
5 1 10
```

| Index | Value | Muscle | Chest | Biceps | Back |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | chest | 5 | 0 | 0 |
| 1 | 1 | biceps | 5 | 1 | 0 |
| 2 | 10 | back | 5 | 1 | 10 |

Final totals:

- chest = 5
- biceps = 1
- back = 10

Output:

```
back
```

This trace demonstrates the full three-step cycle and confirms that the modulo mapping assigns each exercise correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each exercise is processed once |
| Space | O(1) | Only three counters are stored |

With `n ≤ 20`, the running time is tiny. The solution uses constant extra memory and easily fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    chest = 0
    biceps = 0
    back = 0

    for i in range(n):
        if i % 3 == 0:
            chest += a[i]
        elif i % 3 == 1:
            biceps += a[i]
        else:
            back += a[i]

    if chest > biceps and chest > back:
        print("chest")
    elif biceps > chest and biceps > back:
        print("biceps")
    else:
        print("back")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided samples
assert run("2\n2 8\n") == "biceps", "sample 1"

# custom cases
assert run("1\n7\n") == "chest", "single exercise"
assert run("3\n1 2 10\n") == "back", "basic full cycle"
assert run("5\n1 2 3 4 5\n") == "biceps", "cycle repetition"
assert run("20\n25 1 1 25 1 1 25 1 1 25 1 1 25 1 1 25 1 1 25 1\n") == "chest", "maximum size style case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `chest` | Minimum-size input |
| `3 / 1 2 10` | `back` | Correct modulo mapping |
| `5 / 1 2 3 4 5` | `biceps` | Repeating cycle handling |
| Large 20-element case | `chest` | Larger input and repeated accumulation |

## Edge Cases

Consider the smallest possible input:

```
1
7
```

The only exercise is the first one, so it belongs to chest. During the loop:

- index 0 → `0 % 3 == 0`
- chest becomes 7

The final totals are:

- chest = 7
- biceps = 0
- back = 0

The algorithm correctly prints:

```
chest
```

Now consider a case where the cycle repeats multiple times:

```
5
1 2 3 4 5
```

Processing step by step:

- index 0 → chest += 1
- index 1 → biceps += 2
- index 2 → back += 3
- index 3 → chest += 4
- index 4 → biceps += 5

Final totals:

- chest = 5
- biceps = 7
- back = 3

The output is:

```
biceps
```

This confirms that the modulo-based assignment continues correctly beyond the first three exercises.

Finally, consider a case that exposes off-by-one mistakes:

```
3
10 1 20
```

Correct mapping:

- first exercise → chest
- second exercise → biceps
- third exercise → back

Totals become:

- chest = 10
- biceps = 1
- back = 20

The correct output is:

```
back
```

If someone accidentally treated index 0 as biceps because of one-based confusion, all totals would shift incorrectly. The presented algorithm avoids that by using consistent zero-based indexing throughout.
