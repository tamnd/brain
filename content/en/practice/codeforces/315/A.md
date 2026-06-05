---
title: "CF 315A - Sereja and Bottles"
description: "Each bottle has two properties. The value a[i] is the bottle's own brand. The value b[i] is the brand of bottles that this bottle can open. A bottle can be opened if there exists some other bottle whose opening capability matches its brand."
date: "2026-06-06T01:20:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 315
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 187 (Div. 2)"
rating: 1400
weight: 315
solve_time_s: 114
verified: true
draft: false
---

[CF 315A - Sereja and Bottles](https://codeforces.com/problemset/problem/315/A)

**Rating:** 1400  
**Tags:** brute force  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

Each bottle has two properties.

The value `a[i]` is the bottle's own brand. The value `b[i]` is the brand of bottles that this bottle can open.

A bottle can be opened if there exists some other bottle whose opening capability matches its brand. Since bottles may be used whether they are already open or still closed, we only care about the static relationships between brands. There is no sequence of actions to simulate.

For a bottle with brand `a[i]`, we need to check whether there exists another bottle `j` such that `b[j] = a[i]`. If such a bottle exists, bottle `i` can be opened. Otherwise, it can never be opened.

The task is to count how many bottles cannot be opened by any other bottle.

The constraints are very small. There are at most 100 bottles. Even an algorithm that compares every pair of bottles performs only `100 × 100 = 10,000` checks, which is trivial within the time limit. There is no need for complicated data structures or optimization.

A subtle detail is that a bottle cannot open itself. When checking whether bottle `i` can be opened, we must only consider bottles with a different index.

Consider this example:

```
2
1 1
2 2
```

Bottle 1 can open brand 1, but that capability belongs to the same bottle. Bottle 2 behaves similarly. Neither bottle can be opened by another bottle, so the answer is:

```
2
```

A careless implementation that allows self-matching would incorrectly output `0`.

Another important case is when multiple bottles share the same brand.

```
3
1 5
1 7
2 1
```

Bottle 3 can open brand 1, so both bottles with brand 1 are openable. Bottle 3 itself has brand 2, and no bottle can open brand 2. The correct answer is:

```
1
```

An implementation that only checks for unique brands instead of individual bottles could miscount.

A third case is when several bottles can open the same brand.

```
3
4 4
5 4
4 1
```

Both the first and second bottles can open brand 4. The third bottle has brand 4, and the first bottle can open it. Every bottle with brand 4 should be considered openable independently.

## Approaches

The most direct approach is to examine each bottle separately. For bottle `i`, we scan all other bottles and check whether any bottle `j` has `b[j] = a[i]`. If we find such a bottle, bottle `i` is openable. Otherwise, it contributes to the answer.

This approach is correct because the definition of openability depends only on the existence of another bottle whose opening brand matches the bottle's own brand. By checking every possible bottle `j`, we test exactly the condition required by the problem.

For larger constraints, comparing every pair might become expensive. With `n = 100`, however, the worst case is only 10,000 comparisons, which is tiny.

One could also build a set containing all opening brands `b[i]` and check membership. The only complication is the prohibition against self-opening. Since the constraints are so small, the pairwise solution is simpler and avoids special handling.

The key observation is that a bottle's status depends only on whether its brand appears among the opening capabilities of some other bottle. This naturally leads to checking all pairs of bottles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Checking | O(n²) | O(1) | Accepted |
| Brand Tracking Structures | O(n²) or O(n) | O(n) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Read `n` and store all pairs `(a[i], b[i])`.
2. Initialize `answer = 0`.
3. For each bottle `i`, assume initially that it cannot be opened.
4. Scan all bottles `j`.
5. Skip the case `i == j`, because a bottle cannot be used to open itself.
6. If `b[j] == a[i]`, then bottle `i` can be opened by bottle `j`. Mark it as openable and stop checking further bottles.
7. After examining all possible bottles, if bottle `i` is still not openable, increment `answer`.
8. After processing every bottle, print `answer`.

### Why it works

For a bottle `i`, the problem asks whether there exists another bottle whose opening capability equals `a[i]`. The algorithm checks every possible bottle `j ≠ i`. If such a bottle exists, it is found during the scan and bottle `i` is marked openable. If the scan finishes without finding one, then no such bottle exists anywhere in the input, so bottle `i` is impossible to open.

Since this reasoning is applied independently to every bottle, the final count is exactly the number of bottles that cannot be opened.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
bottles = [tuple(map(int, input().split())) for _ in range(n)]

answer = 0

for i in range(n):
    brand = bottles[i][0]
    openable = False

    for j in range(n):
        if i == j:
            continue

        if bottles[j][1] == brand:
            openable = True
            break

    if not openable:
        answer += 1

print(answer)
```

The program first stores all bottle descriptions. For each bottle, it extracts its brand `a[i]` and searches for another bottle whose opening brand equals that value.

The `i == j` check is the most important implementation detail. Without it, a bottle whose own `b[i]` equals `a[i]` would incorrectly be considered openable by itself.

The inner loop stops immediately after finding a valid opener. This does not change correctness, but avoids unnecessary comparisons.

No special handling is needed for duplicate brands or duplicate opening capabilities because every bottle is checked individually.

## Worked Examples

### Example 1

Input:

```
4
1 1
2 2
3 3
4 4
```

| Bottle i | Brand a[i] | Matching opener found? | Unopenable count |
| --- | --- | --- | --- |
| 1 | 1 | No | 1 |
| 2 | 2 | No | 2 |
| 3 | 3 | No | 3 |
| 4 | 4 | No | 4 |

Output:

```
4
```

Each bottle only matches its own opening capability. Since self-opening is not allowed, none of them can be opened.

### Example 2

Input:

```
3
1 2
2 3
3 1
```

| Bottle i | Brand a[i] | Bottle that opens it | Unopenable count |
| --- | --- | --- | --- |
| 1 | 1 | Bottle 3 | 0 |
| 2 | 2 | Bottle 1 | 0 |
| 3 | 3 | Bottle 2 | 0 |

Output:

```
0
```

The bottles form a cycle. Every bottle's brand appears as another bottle's opening capability, so all bottles are openable.

This example demonstrates that the bottles do not need to be opened in any particular order. The problem only asks whether an opener exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | For each bottle, we may scan all other bottles |
| Space | O(1) extra | Only a few variables beyond the input storage |

With `n ≤ 100`, the algorithm performs at most 10,000 pair comparisons. This is far below the limits, making the straightforward quadratic solution more than sufficient.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    bottles = [tuple(map(int, input().split())) for _ in range(n)]

    answer = 0

    for i in range(n):
        brand = bottles[i][0]
        openable = False

        for j in range(n):
            if i == j:
                continue

            if bottles[j][1] == brand:
                openable = True
                break

        if not openable:
            answer += 1

    return str(answer)

# provided sample
assert run("4\n1 1\n2 2\n3 3\n4 4\n") == "4", "sample 1"

# minimum size
assert run("1\n42 42\n") == "1", "single bottle cannot open itself"

# cyclic opening
assert run("3\n1 2\n2 3\n3 1\n") == "0", "all bottles openable"

# duplicate brands
assert run("3\n1 5\n1 7\n2 1\n") == "1", "two bottles opened by same opener"

# all bottles open same brand
assert run("4\n1 5\n2 5\n3 5\n4 5\n") == "4", "no bottle brand appears among opening capabilities"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42 42` | `1` | Self-opening is not allowed |
| Cycle of three bottles | `0` | Every bottle can be opened |
| Duplicate brand example | `1` | Multiple bottles may share a brand |
| All opening capabilities equal 5 | `4` | No matching opener exists for any bottle |

## Edge Cases

Consider the smallest possible input:

```
1
42 42
```

The algorithm checks the only bottle. The inner loop skips the self-comparison because `i == j`. No valid opener is found, so the answer becomes `1`. This matches the rule that a bottle cannot open itself.

Consider a case with duplicate brands:

```
3
1 5
1 7
2 1
```

For the first bottle, the algorithm finds that bottle 3 has `b = 1`, so it is openable. The same reasoning applies to the second bottle because it has the same brand. The third bottle has brand `2`, and no bottle has opening capability `2`, so only that bottle is counted. The answer is `1`.

Consider a cycle:

```
3
1 2
2 3
3 1
```

Bottle 1 is opened by bottle 3, bottle 2 by bottle 1, and bottle 3 by bottle 2. Every search finds a matching opener, so the count remains `0`. The algorithm correctly handles chains and cycles because it only checks existence, not an opening sequence.
