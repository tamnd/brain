---
title: "CF 102897I - BM \u65c5\u6e38"
description: "We are given four large integers. Each integer is not directly the object of interest. Instead, each one encodes whether a particular sightseeing location has been visited."
date: "2026-07-04T08:48:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102897
codeforces_index: "I"
codeforces_contest_name: "The 3rd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102897
solve_time_s: 34
verified: true
draft: false
---

[CF 102897I - BM \u65c5\u6e38](https://codeforces.com/problemset/problem/102897/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four large integers. Each integer is not directly the object of interest. Instead, each one encodes whether a particular sightseeing location has been visited.

For each of the four values A, B, C, and D, we compute a simple digit property: we sum all decimal digits of the number. If this digit sum is at least 16, or exactly equal to 6, then we consider the corresponding viewpoint as visited. Otherwise, it is not visited.

After evaluating the four viewpoints independently, we count how many of them are marked as visited. Based on this count, we output one of five fixed strings.

The constraints allow each number to be as large as 10^18, so each digit sum computation involves at most 19 digits. This makes a direct digit-by-digit scan trivial in terms of complexity. Even in the worst case, we perform only a constant amount of work per number, so the entire solution is effectively constant time.

A subtle edge condition comes from the dual condition “sum ≥ 16 or sum = 6”. The equality condition is redundant for values already ≥ 16, but it matters for distinguishing small digit sums. A naive implementation that only checks “sum ≥ 16” would misclassify numbers with digit sum exactly 6.

For example, consider input `111`. The digit sum is 3, so it is not visited. If a buggy implementation incorrectly used a different threshold rule or forgot edge conditions, it might miscount visited viewpoints, changing the final output category.

Another edge case arises when all four values are identical or all zeros. For `0 0 0 0`, each digit sum is 0, so no viewpoints are visited, producing the lowest-category output.

## Approaches

A brute-force interpretation would literally simulate the rule for each number: compute digit sums, check the condition, and count how many pass. This already sounds optimal, but it helps to formalize why there is no hidden combinatorial structure.

For each of the four numbers, computing digit sum takes O(d) where d is the number of digits, at most 19. Doing this four times gives at most about 76 digit operations. Even if repeated over many test cases, this remains linear in input size with a tiny constant factor.

The only “naive” alternative would be to attempt something more complex like precomputing or transforming numbers, but there is no interaction between A, B, C, and D. Each decision is independent, so no optimization beyond direct evaluation is meaningful.

The key observation is that the problem is purely local per number, and the final result depends only on a small integer count in [0,4]. Once this is seen, the solution reduces to simple classification.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (digit check per number) | O(4 * digits) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read four integers A, B, C, D. These are treated independently, so no combined preprocessing is needed.
2. For each number, compute the sum of its decimal digits by repeatedly taking modulo 10 and dividing by 10. This directly reconstructs the required feature from the encoding.
3. Check whether the digit sum satisfies the condition: it must be at least 16 or exactly equal to 6. If it does, mark this viewpoint as visited. This step encodes the problem’s definition into a boolean decision.
4. Maintain a counter of how many of the four viewpoints are marked visited. This counter can only range from 0 to 4, which later determines the output category.
5. Map the final count to the required string output according to the problem specification.

### Why it works

Each viewpoint decision depends only on a single number and is fully determined by its digit sum. The digit sum computation is exact and lossless with respect to the rule, so each classification is correct in isolation. Since the final answer depends only on the number of true classifications, aggregating them with a counter preserves correctness without requiring any additional structure or ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_sum(x: int) -> int:
    s = 0
    while x > 0:
        s += x % 10
        x //= 10
    return s

A, B, C, D = map(int, input().split())

vals = [A, B, C, D]
cnt = 0

for x in vals:
    s = digit_sum(x)
    if s >= 16 or s == 6:
        cnt += 1

if cnt == 0:
    print("Bao Bao is so Zhai......")
elif cnt == 1:
    print("Oh dear!!")
elif cnt == 2:
    print("BaoBao is good!!")
elif cnt == 3:
    print("Bao Bao is a SupEr man///!")
else:
    print("Oh my God!!!!!!!!!!!!!!!!!!!!!")
```

The digit sum function uses a standard base-10 decomposition loop. This avoids string conversion overhead but either approach would be valid given the tiny input size. The conditional structure at the end directly encodes the five output categories.

The mapping must be implemented carefully since the strings are exact and sensitive to punctuation and capitalization. Any deviation, including extra spaces, would cause a wrong answer.

## Worked Examples

### Example 1

Input:

```
1 2 3 4
```

| Number | Digit sum | Condition satisfied | Visited |
| --- | --- | --- | --- |
| 1 | 1 | No | 0 |
| 2 | 2 | No | 0 |
| 3 | 3 | No | 0 |
| 4 | 4 | No | 0 |

Count is 0, so output is:

```
Bao Bao is so Zhai......
```

This confirms the base case where no number satisfies the condition.

### Example 2

Input:

```
69 777 88 9999
```

| Number | Digit sum | Condition satisfied | Visited |
| --- | --- | --- | --- |
| 69 | 15 | No | 0 |
| 777 | 21 | Yes | 1 |
| 88 | 16 | Yes | 1 |
| 9999 | 36 | Yes | 1 |

Count is 3, so output is:

```
Bao Bao is a SupEr man///!
```

This example demonstrates mixed cases where both the ≥16 rule and the exact equality behavior matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Four numbers, each with at most 19 digit operations |
| Space | O(1) | Only a constant number of variables used |

The runtime is effectively constant regardless of input magnitude because digit length is bounded by the fixed 64-bit constraint. This guarantees immediate execution within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def digit_sum(x: int) -> int:
        s = 0
        while x > 0:
            s += x % 10
            x //= 10
        return s

    A, B, C, D = map(int, input().split())
    vals = [A, B, C, D]
    cnt = 0

    for x in vals:
        s = digit_sum(x)
        if s >= 16 or s == 6:
            cnt += 1

    if cnt == 0:
        return "Bao Bao is so Zhai......"
    elif cnt == 1:
        return "Oh dear!!"
    elif cnt == 2:
        return "BaoBao is good!!"
    elif cnt == 3:
        return "Bao Bao is a SupEr man///!"
    else:
        return "Oh my God!!!!!!!!!!!!!!!!!!!!!"

# provided sample
assert run("1 2 3 4") == "Bao Bao is so Zhai......"

# all zero
assert run("0 0 0 0") == "Bao Bao is so Zhai......"

# one valid
assert run("999999999999999999 1 1 1") == "Oh dear!!"

# two valid
assert run("999999999999999999 888888888888888888 1 1") == "BaoBao is good!!"

# three valid
assert run("999999999999999999 888888888888888888 777777777777777777 1") == "Bao Bao is a SupEr man///!"

# all valid
assert run("999999999999999999 888888888888888888 777777777777777777 666666666666666666") == "Oh my God!!!!!!!!!!!!!!!!!!!!!"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | Zhai output | all zeros edge case |
| all 9s-heavy mix | SupEr man case | multiple thresholds |
| single large + rest small | Oh dear case | single valid count |
| two large numbers | good case | mid-range aggregation |
| four large numbers | final case | maximum count edge |

## Edge Cases

For the input `0 0 0 0`, each digit sum is computed as 0. The condition requires either at least 16 or exactly 6, so none qualify. The counter remains 0 and the algorithm selects the “none visited” string. The digit sum loop terminates immediately for each value since the number is zero.

For the input `6 0 0 0`, the first number has digit sum 6, which satisfies the equality condition even though it is below 16. The counter becomes 1, and the output falls into the single-visited category. This case specifically validates that equality checking is not accidentally replaced by a pure threshold check.
