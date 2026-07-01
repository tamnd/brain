---
title: "CF 104344D - Prova"
description: "Each student’s result comes from a very small fixed universe: there are exactly three independent problems, worth 1, 2, and 4 points."
date: "2026-07-01T18:28:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104344
codeforces_index: "D"
codeforces_contest_name: "Maratona dos Bixes 2023 - UNICAMP"
rating: 0
weight: 104344
solve_time_s: 81
verified: false
draft: false
---

[CF 104344D - Prova](https://codeforces.com/problemset/problem/104344/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

Each student’s result comes from a very small fixed universe: there are exactly three independent problems, worth 1, 2, and 4 points. Any student’s score is just the sum of the values of the problems they solved, so every score between 0 and 7 corresponds to a unique subset of these three problems.

We are given the scores of two students, Lucca and Yvens. From these scores we can infer exactly which subsets of problems each of them solved, because there is no ambiguity in representing numbers from 0 to 7 using these three weights.

Passinho’s behavior is defined in a very specific way. He solves every problem that was solved by at least one of Lucca or Yvens, and he solves none of the problems that neither of them solved. This means Passinho’s solved set is exactly the union of the two students’ solved sets.

The task is therefore to compute the union of the two subsets represented implicitly by their scores, then convert that union back into a score.

The constraint that both scores lie between 0 and 7 implies that each score corresponds to a 3-bit mask. This eliminates any need for combinatorics or search. The entire problem collapses into bitwise reconstruction over three bits.

A subtle failure case appears when reasoning directly on scores instead of subsets. For example, 3 can be either {1,2} and 5 can be {1,4}. A naive attempt might try to combine numbers arithmetically and incorrectly assume independence of digits in decimal representation. The correct representation is binary over weights 1, 2, and 4, not base-10 digits.

## Approaches

The brute-force way is to try all subsets of the three problems for Lucca and Yvens, compute which subsets match their scores, and then explicitly union every compatible pair and recompute the resulting score. Since there are only 2³ subsets per person, this is constant work, but the method is conceptually heavy and obscures the structure.

The key observation is that each score is already a direct encoding of a subset of three elements. Writing the scores in binary aligns perfectly with the problem weights: bit 0 represents problem 1, bit 1 represents problem 2, and bit 2 represents problem 4. Thus, the score itself is a bitmask.

Once this is seen, Passinho’s score is simply the bitwise OR of the two scores. The OR operation captures exactly the union of solved problems, since a bit is set if at least one of the two students has it set.

This reduces the problem to a single operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of subsets | O(1) | O(1) | Accepted |
| Bitwise OR interpretation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers L and Y from input. These represent two bitmasks over three bits.
2. Interpret each number as a subset of {1, 2, 4} where each bit indicates whether a problem was solved.
3. Compute the union of solved problems by applying bitwise OR between L and Y. This works because OR preserves a bit if it is present in either operand.
4. Output the resulting integer, which directly corresponds to Passinho’s score.

### Why it works

Each problem contributes independently to the final score, and there are no interactions between problems. This independence guarantees that the score representation is linear in terms of bit presence. Because every valid score from 0 to 7 is a unique 3-bit vector, the union of solved sets corresponds exactly to bitwise OR. No alternative representation exists, so the result is uniquely determined.

## Python Solution

```python
import sys
input = sys.stdin.readline

L, Y = map(int, input().split())
print(L | Y)
```

The solution relies on reading two integers and applying a single bitwise OR operation. The key implementation detail is that no conversion or decoding is needed; the input values already represent bitmasks in disguise.

A common mistake is attempting to decompose the numbers into decimal digits or to reconstruct subsets manually. That is unnecessary because the encoding already matches binary structure.

## Worked Examples

### Example 1

Input:

```
0 0
```

| L | Y | L OR Y | Result |
| --- | --- | --- | --- |
| 000 | 000 | 000 | 0 |

Both students solved nothing, so the union is empty and Passinho also solves nothing.

### Example 2

Input:

```
1 2
```

| L | Y | L OR Y | Result |
| --- | --- | --- | --- |
| 001 | 010 | 011 | 3 |

Lucca solved only the 1-point problem, Yvens solved only the 2-point problem. Passinho solves both, giving total 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single bitwise operation and input parsing |
| Space | O(1) | Constant storage for two integers |

The constraints restrict values to at most 7, so even a more expensive method would be trivial. The bitwise solution fits comfortably within limits and is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    L, Y = map(int, input().split())
    return str(L | Y)

# provided samples
assert run("0 0\n") == "0", "sample 1"
assert run("1 2\n") == "3", "sample 2"
assert run("5 3\n") == "7", "sample 3"

# custom cases
assert run("7 0\n") == "7", "all bits already set"
assert run("4 2\n") == "6", "disjoint higher bits"
assert run("1 4\n") == "5", "non-adjacent bits"
assert run("6 3\n") == "7", "completing missing bit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 0 | 7 | identity behavior of OR |
| 4 2 | 6 | combining non-overlapping higher bits |
| 1 4 | 5 | non-adjacent bit merging |
| 6 3 | 7 | full coverage completion |

## Edge Cases

One edge case is when both inputs are identical, such as 3 and 3. In that case, both students solved exactly the same problems, so Passinho should solve the same set as well. The computation L OR Y = 3 OR 3 = 3 preserves the original value correctly.

Another edge case is when one input is 0. For example, L = 0 and Y = 5. The union should simply reproduce Y. The OR operation gives 0 OR 5 = 5, which matches the interpretation that Passinho solves exactly what Yvens solved.

A final case is when both inputs are disjoint, such as 1 and 2 or 1 and 4 and 2. The OR operation correctly accumulates all bits without interference, producing the full union up to 7 when all bits are covered.
