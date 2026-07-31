---
title: "CF 102591A - 3435"
description: "We need count the integers inside an interval [l, r] that are equal to the sum of a special value assigned to each of their digits. For a digit x, its contribution is x^x, so a number is valid when adding the contributions of all its digits reconstructs the original number."
date: "2026-07-31T15:53:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102591
codeforces_index: "A"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043f\u0440\u0435\u0434\u043c\u0435\u0442\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041c\u0423\u0418\u0422 \u043f\u043e \u0441\u043f\u043e\u0440\u0442\u0438\u0432\u043d\u043e\u043c\u0443 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2020. \u0424\u0438\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u0442\u0443\u0440."
rating: 0
weight: 102591
solve_time_s: 427
verified: true
draft: false
---

[CF 102591A - 3435](https://codeforces.com/problemset/problem/102591/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We need count the integers inside an interval `[l, r]` that are equal to the sum of a special value assigned to each of their digits. For a digit `x`, its contribution is `x^x`, so a number is valid when adding the contributions of all its digits reconstructs the original number.

For example, the number `3435` is valid because its digits contribute `3^3 + 4^4 + 3^3 + 5^5`, which equals `3435`.

The interval endpoints can be as large as `10^9`. A direct scan of every number would require checking up to one billion candidates, and even a very fast digit check would not be enough. The useful property is that the number of digits is small. Every candidate has at most ten digits, so instead of searching through numbers, we can search through digit combinations.

The edge cases mostly come from treating the number as an ordinary integer instead of as a sequence of digits. The digit `0` is possible inside a number, and its contribution is `0^0` in the usual definition used by this problem, which must be handled as `1` because the contribution of digit `0` is defined as `0^0` in the digit formula. A careless implementation using a normal power function can produce different results for this case. For example, the interval `1 1` contains the valid number `1`, so the correct output is `1`. An implementation that ignores the single digit case could incorrectly return `0`.

Another edge case is the upper boundary. The number `438579088` is valid and is below `10^9`, so the input `438579088 438579088` must return `1`. A solution that only precomputes values below a smaller limit or accidentally uses a strict upper bound would miss it.

The interval may also contain no valid values. For example, `2 10` has no valid numbers, so the answer is `0`. A brute force implementation that only checks digit sums for numbers with multiple digits might incorrectly count or skip small values.

## Approaches

The straightforward approach is to iterate through every number from `l` to `r`, compute the sum of digit contributions, and compare it with the original number. This is correct because it directly follows the definition of a valid number. However, the largest interval can contain about one billion numbers. Each check examines up to ten digits, giving roughly `10^10` digit operations in the worst case, which is far beyond what is practical.

The important observation is that there are very few possible answers. A number with at most ten digits can only be formed from ten choices for each digit, and the number of valid combinations is tiny. We can reverse the search direction. Instead of asking whether every number is valid, we generate all possible sums of digit contributions and reconstruct the corresponding number.

During a digit search, we choose each digit position. The contribution sum is accumulated at the same time as the actual numeric value. After all positions are chosen, if the constructed number equals the accumulated contribution sum, we have found a valid number.

There are only eleven possible lengths to consider if we include the range up to `10^9`, and the pruning is strong because the contribution of a digit is fixed. The search visits far fewer states than scanning the interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l+1) * 10) | O(1) | Too slow |
| Optimal | O(10 * 10^10) in the loose upper bound, much smaller with pruning | O(10) | Accepted |

## Algorithm Walkthrough

1. Precompute the contribution of every digit from `0` to `9`. The value depends only on the digit, so calculating it once avoids repeated work during the search.
2. Generate every possible number with up to ten digits using depth first search. While building a number, keep two values: the number represented by the chosen digits and the sum of digit contributions.
3. Skip numbers with leading zeroes by only starting lengths from one digit and allowing zeroes only after the first chosen digit. This prevents generating the same number multiple times with different lengths.
4. When a complete digit sequence is created, compare the constructed number with the accumulated contribution sum. If they are equal and the number lies inside `[l, r]`, add it to the answer.
5. Sort or store the generated valid numbers and count how many fall into the requested interval.

The reason this works is that every possible number in the allowed range has exactly one digit representation without leading zeroes. The search enumerates every such representation, calculates the exact value required by the definition, and accepts only representations where the two values match. Since no valid representation is skipped and no invalid representation is accepted, the final count is correct.

## Python Solution

```
Python
```

The array `pow_digit` stores the only information needed from each digit. Handling digit zero explicitly avoids relying on a language-specific interpretation of `0 ** 0`.

The recursive function keeps `value`, the actual number currently being constructed, and `total`, the sum of digit contributions. Once all positions are filled, equality between these two variables is exactly the condition from the problem.

The search considers lengths from one to ten because `10^9` has ten digits. Leading zeroes are rejected at the first position, which avoids duplicate representations. The upper bound check allows branches larger than `r` to stop immediately.

Python integers do not overflow, so the implementation does not need special handling for large intermediate values. The final range check is inclusive on both sides, matching the definition of the interval.

## Worked Examples

For the sample input:

```

```

the search generates the valid numbers below `10^9`, then checks which ones belong to the interval.

| Length | Candidate | Digit contribution sum | Valid | Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Yes, outside range | 0 |
| 4 | 3435 | 3435 | Yes, inside range | 1 |
| 9 | 438579088 | 438579088 | Yes, outside range | 1 |

The trace shows that the algorithm does not need to inspect every number between `2020` and `4040`. It finds the small set of valid numbers and performs a range check afterward.

A second example is:

```

```

| Length | Candidate | Digit contribution sum | Valid | Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | Yes, inside range | 1 |
| 2 | none | none | none | 1 |

This confirms that single digit values are included and that the interval boundaries are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10 * generated_states) | The recursion explores digit assignments, but the actual number of completed candidates is very small because only ten digit positions exist. |
| Space | O(10) | The recursion depth is at most ten, and the stored answer list contains only a few numbers. |

The maximum input size prevents scanning the whole interval. The digit generation approach depends only on the number of digits, which remains small for the given limit.

## Test Cases

```
Python
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Handles the smallest possible interval and single digit answers |
| `2 10` | `0` | Handles intervals with no valid values |
| `3435 3435` | `1` | Checks inclusive lower and upper boundaries |
| `438579088 1000000000` | `1` | Checks the maximum side of the input range |

## Edge Cases

For the interval `1 1`, the algorithm starts a one-digit search, chooses digit `1`, and calculates both the constructed value and contribution sum as `1`. They match, so the answer becomes `1`. This prevents losing valid one-digit numbers.

For the interval `438579088 438579088`, the DFS reaches the nine-digit representation `438579088`. The accumulated contribution sum is also `438579088`, so the value is counted. This confirms that the upper part of the allowed range is included.

For the interval `2 10`, the only valid number in that region would be `1`, but it lies outside the interval. The generated list is checked against both bounds, leaving the count at `0`. This handles empty result ranges correctly.
