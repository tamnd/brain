---
title: "CF 102785A - A lazy controller"
description: "Each weighing records two integers. The first is the number of identical parts placed on the scale, and the second is the measured total weight of those parts. If every part in the batch has the same integer weight x, then every record must satisfy wi = ai × x."
date: "2026-07-28T15:47:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102785
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 18)"
rating: 0
weight: 102785
solve_time_s: 59
verified: true
draft: false
---

[CF 102785A - A lazy controller](https://codeforces.com/problemset/problem/102785/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

Each weighing records two integers. The first is the number of identical parts placed on the scale, and the second is the measured total weight of those parts.

If every part in the batch has the same integer weight `x`, then every record must satisfy

`wi = ai × x`.

The controller does not know the correct weight in advance. He only checks whether there exists some integer weight that explains every recorded measurement. If at least one such integer exists, there is no evidence of defects and the batch is accepted. If no integer weight is consistent with all measurements, the batch is definitely defective.

The number of measurements is at most 1000. Every value involved is also small enough that simple integer arithmetic is sufficient. There is no need for any advanced optimization because even an algorithm that processes every record once easily fits within the limits.

The only real difficulty is correctly interpreting what "defect" means. We are not trying to determine the true weight of the parts. We only need to determine whether some integer weight could explain every measurement simultaneously.

A common mistake is checking only that every individual measurement has an integer weight. Consider

```
2
2 6
3 12
```

The first weighing suggests a weight of `3`, while the second suggests a weight of `4`. Both are integers, but they disagree, so the correct output is

```
DEFECT
```

Another easy mistake is choosing the weight from the first measurement and ignoring whether it is an integer.

```
2
2 5
4 10
```

The first record would imply a weight of `2.5`, which is impossible because the weight must be an integer. Although both measurements are consistent with the same fractional value, the correct answer is

```
DEFECT
```

A final edge case is having only one measurement.

```
1
7 35
```

The only implied weight is `5`, which is an integer, so the correct output is

```
QUALITY
```

One consistent measurement is enough because the controller only rejects the batch when the records contradict every possible integer weight.

## Approaches

The most direct approach is to try every possible integer weight and check whether all measurements satisfy `wi = ai × weight`. This is correct because the batch is acceptable exactly when at least one candidate weight matches every record.

The weakness is deciding how many candidate weights must be tested. The statement does not provide an explicit upper bound on the true weight. Even if we derive one from the input by considering every possible value up to the largest observed weight, the algorithm would perform up to nearly one million checks for each of the thousand measurements, resulting in roughly one billion comparisons in the worst case.

The key observation is that every measurement directly determines the only possible weight it could represent. Rearranging the equation gives

`weight = wi / ai`.

For a measurement to be valid, the division must be exact because the weight is an integer. Every valid measurement also has to produce exactly the same value. Instead of searching through possible weights, we simply compute the implied weight from the first record and verify that every remaining record implies the same integer.

This reduces the problem to a single linear scan through the measurements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k × W), where W is the searched weight range | O(1) | Too slow |
| Optimal | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of measurements.
2. Read the first measurement. If its total weight is not divisible by its number of parts, immediately print `DEFECT`, because no integer weight can explain even this single record.
3. Otherwise, compute the candidate weight as `w1 // a1`. Every valid measurement must produce exactly this value.
4. Process each remaining measurement one by one.
5. For each measurement, first check whether `wi` is divisible by `ai`. If it is not, print `DEFECT` and terminate because the implied weight is not an integer.
6. Compute the implied weight `wi // ai`. If it differs from the candidate weight, print `DEFECT` and terminate because different measurements require different part weights.
7. If every measurement passes both checks, print `QUALITY`.

### Why it works

The algorithm maintains one invariant throughout the scan. The candidate weight is the only integer weight consistent with every processed measurement.

The first valid measurement uniquely determines the candidate. Every later measurement either agrees with it or proves that no common integer weight exists. Since every possible valid solution must satisfy every measurement, accepting only when all implied weights are identical is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())

a, w = map(int, input().split())

if w % a != 0:
    print("DEFECT")
    sys.exit()

weight = w // a

for _ in range(k - 1):
    a, w = map(int, input().split())
    if w % a != 0 or w // a != weight:
        print("DEFECT")
        sys.exit()

print("QUALITY")
```

The first measurement establishes the only possible integer weight. Before storing it, the code verifies that the division is exact. This prevents fractional weights from being accepted.

Each later measurement performs the same divisibility check before comparing the implied weight with the stored candidate. Using integer division only after confirming divisibility avoids incorrect truncation.

The program exits immediately after detecting any contradiction. Since one inconsistent measurement is enough to reject the batch, there is no reason to process the remaining input.

## Worked Examples

### Sample 1

Input:

```
3
10 30
5 15
2 6
```

| Measurement | a | w | Divisible | Implied Weight | Candidate | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | 30 | Yes | 3 | 3 | Continue |
| 2 | 5 | 15 | Yes | 3 | 3 | Continue |
| 3 | 2 | 6 | Yes | 3 | 3 | Continue |

Every measurement implies the same integer weight, so the output is

```
QUALITY
```

This trace confirms the invariant that the candidate weight remains consistent throughout the scan.

### Sample 2

Input:

```
2
2 5
4 10
```

| Measurement | a | w | Divisible | Implied Weight | Candidate | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 5 | No | Invalid | None | Reject |

The algorithm stops immediately because the very first measurement cannot correspond to an integer part weight.

The output is

```
DEFECT
```

This demonstrates that a common fractional weight is not acceptable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each measurement is processed exactly once. |
| Space | O(1) | Only a few integer variables are stored. |

Since `k` is at most 1000, a single linear pass is easily fast enough and uses negligible memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    k = int(input())
    a, w = map(int, input().split())

    if w % a != 0:
        print("DEFECT")
        return

    weight = w // a

    for _ in range(k - 1):
        a, w = map(int, input().split())
        if w % a != 0 or w // a != weight:
            print("DEFECT")
            return

    print("QUALITY")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided samples
assert run("3\n10 30\n5 15\n2 6\n") == "QUALITY", "sample 1"
assert run("2\n2 5\n4 10\n") == "DEFECT", "sample 2"

# custom cases
assert run("1\n7 35\n") == "QUALITY", "single valid measurement"
assert run("2\n2 6\n3 12\n") == "DEFECT", "different integer weights"
assert run("4\n1 9\n2 18\n3 27\n4 36\n") == "QUALITY", "all equal weight"
assert run("2\n1000 999000\n1 999\n") == "QUALITY", "boundary values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One valid measurement | QUALITY | Minimum input size |
| Two different implied integer weights | DEFECT | Detects inconsistent measurements |
| Four consistent measurements | QUALITY | Multiple matching records |
| Large `a` with matching ratio | QUALITY | Boundary arithmetic |

## Edge Cases

Consider the case where every measurement individually gives an integer weight, but the weights differ.

```
2
2 6
3 12
```

The algorithm stores the candidate weight `3` from the first measurement. The second measurement implies `4`, which does not match the candidate, so it prints `DEFECT`. This catches contradictions that a simple divisibility check would miss.

Now consider a fractional implied weight.

```
2
2 5
4 10
```

The first measurement fails the divisibility check because `5 % 2 != 0`. The algorithm immediately prints `DEFECT` without examining later records. This correctly rejects batches that can only be explained by a non-integer weight.

Finally, consider the smallest valid input.

```
1
7 35
```

The measurement implies the integer weight `5`. No other records exist to contradict it, so the algorithm finishes the scan and prints `QUALITY`. This matches the requirement that the controller only rejects the batch when the collected evidence is inconsistent with every possible integer weight.
