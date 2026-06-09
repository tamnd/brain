---
title: "CF 1850B - Ten Words of Wisdom"
description: "The task is to find the winning response in a short-answer game show. Each participant submits a response, which has two attributes: the number of words it contains and its quality score."
date: "2026-06-09T05:29:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 800
weight: 1850
solve_time_s: 68
verified: true
draft: false
---

[CF 1850B - Ten Words of Wisdom](https://codeforces.com/problemset/problem/1850/B)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to find the winning response in a short-answer game show. Each participant submits a response, which has two attributes: the number of words it contains and its quality score. The winner is the response that has the highest quality among all submissions that are at most ten words long. Since all quality scores are distinct, there is no ambiguity in choosing the winner.

The input provides multiple test cases. Each test case first tells us how many responses there are, followed by a list of responses with their word counts and quality scores. The output is simply the 1-based index of the winning response for each test case.

Given the constraints, there are at most 50 responses per test case, and each quality score and word count is at most 50. This implies that a brute-force scan over all responses is fast enough. Edge cases include when only one response has 10 or fewer words or when multiple responses are just at the word limit; the algorithm must correctly identify the highest-quality response among them.

A naive mistake would be to pick the first response with ≤10 words without checking all others. For instance, if the input is `3 11 5 10 6 12 7`, the correct winner is the second response (`10 6`), not the first, because it has higher quality within the word limit.

## Approaches

The simplest approach is brute force: iterate through all responses, skip those longer than 10 words, and track the highest-quality response found. This works because the number of responses is small. Each test case requires at most 50 comparisons, and there are at most 100 test cases, totaling 5000 operations-well within limits.

A more formal optimal approach does not need advanced data structures. The insight is that we only care about responses with 10 or fewer words. We can scan once, keeping track of the highest quality seen so far and the corresponding index. At the end of the scan, the index gives the winner. Sorting is unnecessary because we do not need global ordering, just a maximum among a subset.

The brute-force scan and the optimal approach are essentially the same in implementation here, because the data size is tiny. The difference is that we explicitly ignore responses that exceed the word limit during the scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Accepted |
| Optimal Scan | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the number of responses.
3. Initialize two variables: one for the current best quality found (`max_quality`) and one for the index of that response (`winner_index`). Set `max_quality` to a value lower than the minimum possible quality (e.g., `-1`).
4. Iterate through the responses with a loop variable `i` representing the 1-based index. For each response, read its word count and quality.
5. If the word count exceeds 10, skip to the next response.
6. If the word count is at most 10 and the quality is higher than `max_quality`, update `max_quality` and set `winner_index` to `i`.
7. After checking all responses, output `winner_index`.

Why it works: The invariant is that `winner_index` always holds the index of the highest-quality response among all responses examined so far that meet the word limit. Because all qualities are distinct and at least one response is short enough, the loop guarantees that the final value of `winner_index` is the correct winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    max_quality = -1
    winner_index = -1
    for i in range(1, n + 1):
        a, b = map(int, input().split())
        if a <= 10 and b > max_quality:
            max_quality = b
            winner_index = i
    print(winner_index)
```

The code reads the number of test cases and loops over each. Inside each test case, it tracks the highest quality among eligible responses. The 1-based index is preserved by iterating from `1` to `n`. The `if a <= 10` check ensures only responses within the word limit are considered. Updating `max_quality` and `winner_index` only when a higher quality is found guarantees that the winner is correct.

## Worked Examples

Sample input:

```
5
7 2
12 5
9 3
9 4
10 1
```

| i | a_i | b_i | Eligible? | max_quality | winner_index |
| --- | --- | --- | --- | --- | --- |
| 1 | 7 | 2 | yes | 2 | 1 |
| 2 | 12 | 5 | no | 2 | 1 |
| 3 | 9 | 3 | yes | 3 | 3 |
| 4 | 9 | 4 | yes | 4 | 4 |
| 5 | 10 | 1 | yes | 4 | 4 |

Output: `4`

This trace confirms that the algorithm skips ineligible responses and updates the winner correctly.

Another input:

```
3
1 2
3 4
5 6
```

| i | a_i | b_i | Eligible? | max_quality | winner_index |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | yes | 2 | 1 |
| 2 | 3 | 4 | yes | 4 | 2 |
| 3 | 5 | 6 | yes | 6 | 3 |

Output: `3`

It demonstrates that the algorithm correctly handles all eligible responses and finds the global maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single loop over responses, n ≤ 50 |
| Space | O(1) | Only two extra variables are used |

With up to 100 test cases and at most 50 responses each, the algorithm performs at most 5000 iterations, which is trivial for modern CPUs. Memory usage is minimal, well under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        max_quality = -1
        winner_index = -1
        for i in range(1, n + 1):
            a, b = map(int, input().split())
            if a <= 10 and b > max_quality:
                max_quality = b
                winner_index = i
        print(winner_index)
    return output.getvalue().strip()

# provided samples
assert run("3\n5\n7 2\n12 5\n9 3\n9 4\n10 1\n3\n1 2\n3 4\n5 6\n1\n1 43\n") == "4\n3\n1", "sample 1"

# custom cases
assert run("1\n1\n10 50\n") == "1", "single response at limit"
assert run("1\n2\n11 1\n10 2\n") == "2", "only second response eligible"
assert run("1\n3\n10 1\n10 3\n10 2\n") == "2", "highest quality in middle"
assert run("1\n4\n12 10\n9 5\n10 6\n15 7\n") == "3", "multiple eligible, middle wins"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n10 50 | 1 | Single eligible response |
| 1\n2\n11 1\n10 2 | 2 | Skips ineligible response |
| 1\n3\n10 1\n10 3\n10 2 | 2 | Correct selection among eligible responses |
| 1\n4\n12 10\n9 5\n10 6\n15 7 | 3 | Highest-quality eligible not first |

## Edge Cases

If only one response has 10 or fewer words, it must be chosen regardless of its quality relative to longer responses. For input `2\n11 10\n9 1`, the algorithm sets `max_quality` to `-1`, examines the first response (skipped), then the second response (eligible), and sets `winner_index` to `2`, which is correct.

If all responses have exactly 10 words, the algorithm still correctly selects the highest quality among them. For input `3\n10 5\n10 2\n10 7`, it tracks max_quality as 5, then 5 (unchanged for 2), then updates to 7 for the last response, outputting `3`, which confirms proper handling of boundary word counts.
