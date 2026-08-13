---
title: "CF 102302F - Drawing cards"
description: "There are initially N cards in the box, one card for every label from 1 through N. Whenever a label is drawn for the first time, that card is placed on the desk and one fresh card is added to the box. The label of the fresh card is chosen uniformly from all N possible labels."
date: "2026-08-13T07:40:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102302
codeforces_index: "F"
codeforces_contest_name: "2019 USP-ICMC"
rating: 0
weight: 102302
solve_time_s: 132
verified: true
draft: false
---

[CF 102302F - Drawing cards](https://codeforces.com/problemset/problem/102302/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

There are initially N cards in the box, one card for every label from 1 through N. Whenever a label is drawn for the first time, that card is placed on the desk and one fresh card is added to the box. The label of the fresh card is chosen uniformly from all N possible labels. Repeated draws of a label that has already appeared do not change the collection of cards in the box.

We need the expected number of distinct labels that have appeared by the moment label 1 appears for the first time. Since the card with label 1 is placed on the desk at that moment, the answer is at least 1.

The constraint N <= 10^6 is large enough that a simulation of the random process is not a suitable solution. Even a solution taking O(N^2) operations would be far beyond the one second limit. We need to exploit a property of the random process that lets us obtain the expectation directly, ideally in constant time.

The subtle cases are surprisingly simple. For N = 1, the only card is already label 1, so the answer is exactly 1. A careless formula involving N - 1 divisions or an assumption that another label exists could mishandle this case. For N = 2, the two labels are perfectly symmetric, so either one is the first to appear. The expected number of labels on the desk is consequently 1 when 1 is first and 2 when 2 is first, giving 1.5. Any simulation-based intuition that assumes label 1 is somehow favored because it is the stopping label would be incorrect.

For example, the input `1` has answer `1.0000000000`. The input `2` has answer `1.5000000000`. The answer for `3` is `2.0000000000`, because labels 2 and 3 each have probability one half of appearing before label 1.

## Approaches

A direct approach would simulate the entire random experiment. We could store the multiplicity of every label in the box, repeatedly choose a random card, mark a label as seen when it appears for the first time, and stop when label 1 is drawn. This would correctly model the process, but it does not compute an exact expectation. A Monte Carlo simulation only estimates the answer, and the number of draws before label 1 appears is random and has no fixed worst-case bound. In particular, there is always a positive probability of avoiding label 1 for arbitrarily many draws, so there is no finite worst-case operation count that makes simulation a valid exact algorithm.

The key observation is that we do not need to understand the complicated evolution of the box at all. Consider any label i different from 1. We only care whether i has appeared before 1. The entire random process treats labels symmetrically. Swapping the names 1 and i does not change any rule or probability: every initial label occurs once, and every newly created card chooses its label uniformly from 1 through N.

Consequently, labels 1 and i have exactly the same distribution with respect to which one appears first. One of them must appear first, so each has probability exactly 1/2 of being first. Thus the probability that i appears before 1 is also exactly 1/2.

Now introduce an indicator X_i for every i from 2 through N. Let X_i be 1 if label i has appeared before the first appearance of label 1, and 0 otherwise. When label 1 finally appears, the number of cards on the desk is

1 + X_2 + X_3 + ... + X_N.

Taking expectations and using linearity of expectation gives

E = 1 + sum E[X_i].

Each X_i has expectation 1/2, so

E = 1 + (N - 1) / 2 = (N + 1) / 2.

The important part is that the X_i do not need to be independent. Linearity of expectation works regardless of their dependencies. This completely removes the need to model how many duplicate cards are created or how long the process runs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded random runtime | O(N) | Too slow and only estimates |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read N, the number of possible labels.
2. Consider one arbitrary label i with 2 <= i <= N. The process is symmetric under exchanging labels 1 and i, because both initially have one card and every newly generated label is selected uniformly.
3. Since either 1 or i must be the first of these two labels to appear, symmetry gives P(i appears before 1) = 1/2.
4. Define one indicator for every label i from 2 through N. Its value is 1 exactly when that label is already on the desk when label 1 is drawn for the first time. Its expected value is therefore 1/2.
5. The final number of cards on the desk equals 1 plus the sum of these indicators. The extra 1 corresponds to label 1 itself.
6. Apply linearity of expectation. The expected desk size is 1 + (N - 1) / 2, which simplifies to (N + 1) / 2.
7. Print the result as a floating-point number. No simulation, arrays, random numbers, or iterative process are needed.

### Why it works

The invariant behind the argument is label symmetry. At every stage, replacing every occurrence of label 1 by label i and every occurrence of label i by label 1 produces a process with exactly the same probability distribution. Thus neither label can have an advantage in being the first one encountered. For every i != 1, the event that i appears before 1 has probability 1/2.

The final desk count can be expressed as a sum of independent-looking indicator contributions, but independence is not required. Linearity of expectation says that the expected sum is the sum of the individual expectations. Each of the N - 1 labels other than 1 contributes 1/2 in expectation, while label 1 contributes exactly 1. Hence the formula `(N + 1) / 2` is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
answer = (n + 1) / 2.0
print(f"{answer:.10f}")
```

The input contains only one integer, so a single call to `input()` is sufficient. The expression `(n + 1) / 2.0` performs floating-point division and directly evaluates the derived expectation.

There is no need to construct the box or track which labels have appeared. Doing so would solve a much more complicated problem than the one actually asked. The symmetry argument has already accounted for every possible sequence of random card creations.

Using `.10f` gives ten digits after the decimal point, comfortably more precision than the required error tolerance. Python integers can represent N exactly, and the intermediate value N + 1 is tiny compared with Python's integer range, so overflow is not a concern.

## Worked Examples

### Example 1: N = 2

For two labels, label 2 has probability one half of appearing before label 1. The final desk contains label 1 in every outcome, and contains label 2 exactly when label 2 appeared first.

| N | Label considered | P(label before 1) | Expected contribution | Expected total |
| --- | --- | --- | --- | --- |
| 2 | 2 | 1/2 | 1/2 | 1 + 1/2 = 1.5 |

The answer is `1.5000000000`, matching the sample. This trace demonstrates the symmetry argument in its smallest nontrivial case.

### Example 2: N = 3

Labels 2 and 3 are both symmetric with label 1. Each has probability one half of appearing before 1, regardless of the complicated duplicate-card behavior that may happen beforehand.

| N | Label considered | P(label before 1) | Expected contribution | Running expected total |
| --- | --- | --- | --- | --- |
| 3 | 2 | 1/2 | 1/2 | 1.5 |
| 3 | 3 | 1/2 | 1/2 | 2.0 |

The answer is `2.0000000000`. This demonstrates that the individual events for labels 2 and 3 do not need to be independent. We only add their expectations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only one arithmetic expression is evaluated after reading N. |
| Space | O(1) | No data structure grows with N. |

The maximum N is 10^6, but the solution performs the same constant amount of work for every input size. It is comfortably within both the one second time limit and the 256 MB memory limit.

## Test Cases

The exact floating-point result should be compared with a tolerance in a robust test harness. The following tests use the same solution logic and validate the important boundaries and several larger values.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)
    try:
        input = sys.stdin.readline
        n = int(input())
        answer = (n + 1) / 2.0
        return f"{answer:.10f}"
    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve(inp)

# provided sample
assert run("2\n") == "1.5000000000", "sample 1"

# minimum-size input
assert run("1\n") == "1.0000000000", "N = 1"

# first odd value where the answer is an integer
assert run("3\n") == "2.0000000000", "N = 3"

# larger even boundary case
assert run("1000000\n") == "500000.5000000000", "maximum N"

# another odd value, checking the half-integer result
assert run("999999\n") == "500000.0000000000", "large odd N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1.0000000000` | Minimum N and the case with no other labels |
| `2` | `1.5000000000` | Provided sample and first nontrivial symmetry case |
| `3` | `2.0000000000` | Small odd N and integer expectation |
| `999999` | `500000.0000000000` | Large odd N and half-integer arithmetic |
| `1000000` | `500000.5000000000` | Maximum N and large even N |

## Edge Cases

For N = 1, the input is `1`. There are no labels other than 1, so the first card drawn must be label 1. The desk contains exactly one card at that moment. The formula gives `(1 + 1) / 2 = 1`, so the algorithm prints `1.0000000000`.

For N = 2, the input is `2`. Labels 1 and 2 start with one card each, and every generated card chooses between them with equal probability. More generally, the complete process remains unchanged if their names are exchanged. Thus either label is equally likely to be encountered first. If 1 comes first, one card is on the desk. If 2 comes first, both labels are eventually represented when 1 is drawn, so two cards are on the desk. The expectation is `(1 + 2) / 2 = 1.5`.

For N = 3, the input is `3`. Label 2 has a 1/2 chance of preceding 1, and label 3 independently has a 1/2 marginal probability of preceding 1. We do not need to determine whether both can occur together with a particular probability. Their expected contributions are each 1/2, giving `1 + 1/2 + 1/2 = 2`.

For the maximum input `1000000`, the formula gives `1000001 / 2 = 500000.5`. The algorithm reaches this result with exactly the same amount of work as for N = 1. This is also why tracking the dynamically growing box would be unnecessary overhead: the number of possible cards can become large, while the expected value is determined entirely by symmetry.
