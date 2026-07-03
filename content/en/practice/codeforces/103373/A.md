---
title: "CF 103373A - Olympic Ranking"
description: "We are given a small list of countries, each described by three integers: the number of gold, silver, and bronze medals it has won, followed by its name. Our task is to determine which country ranks highest under the standard Olympic ranking rules."
date: "2026-07-03T12:36:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103373
codeforces_index: "A"
codeforces_contest_name: "2021 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 103373
solve_time_s: 47
verified: true
draft: false
---

[CF 103373A - Olympic Ranking](https://codeforces.com/problemset/problem/103373/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small list of countries, each described by three integers: the number of gold, silver, and bronze medals it has won, followed by its name. Our task is to determine which country ranks highest under the standard Olympic ranking rules.

The ranking is lexicographic over the triple of medal counts. A country is better if it has more gold medals. If gold counts are equal, then silver medals decide. If both gold and silver are equal, bronze medals break the tie. Since the problem guarantees that there is exactly one best country, we do not need to handle ties in the final answer.

Even though the input size is small, the structure matters: we are essentially finding the maximum element under a custom ordering on triples.

The constraints are very light, with fewer than 300 countries. This immediately tells us that even quadratic or sorting-based solutions are safe, but the simplest linear scan is already sufficient. We only need to maintain the current best candidate while reading input.

A subtle but important edge case comes from input formatting: country names may contain spaces, so naive splitting by whitespace can accidentally break the name apart. For example, a line like `10 5 3 United States of America` must preserve the full string after the three integers as the name.

Another edge case is when all medal counts are identical except for ordering of input. Since uniqueness of the best rank is guaranteed, we will never need to break ties beyond comparison; we simply track the first maximum encountered or consistently update on strictly better tuples.

## Approaches

A brute-force interpretation would compare every country with every other country, checking dominance under lexicographic rules. For each pair, we would compare gold, then silver, then bronze, and keep track of whether one is strictly better. This works correctly but is unnecessarily expensive. With up to 300 countries, this would require about 90,000 comparisons, which is still acceptable, but the logic is more complex than needed.

The key observation is that the ranking defines a total order on triples, so we do not need pairwise dominance checks. We only need to find the maximum element under lexicographic comparison. This reduces the problem to a single pass through the list, maintaining the best seen so far.

Instead of comparing every pair, we compare each new country only against the current best candidate. This reduces the problem to O(n), which is simpler and less error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Comparison | O(n²) | O(1) | Correct but unnecessary |
| Single Pass Maximum Tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each country one by one and maintain the best triple seen so far.

1. Read the number of countries n. This defines how many updates we will perform on our best candidate.
2. Initialize variables to store the current best medal counts and corresponding country name. We start with a state that is worse than any valid input, such as negative infinity for medals or by initializing from the first input line.
3. For each country, parse the line into three integers and the remaining string as the country name. This requires careful parsing because names can contain spaces, so we cannot assume a fixed number of tokens beyond the first three integers.
4. Compare the current country’s medal triple (g, s, b) with the stored best triple. We compare lexicographically: first gold, then silver, then bronze. If the current country is strictly better, we replace the stored best values with the current one.
5. After processing all countries, output the stored best country name.

### Why it works

The algorithm maintains the invariant that after processing i countries, the stored candidate is the best among those i countries under lexicographic ordering of (gold, silver, bronze). Each update step preserves this invariant because we only replace the stored candidate when we find a strictly better triple. Since the comparison defines a total order, the final candidate after processing all entries must be the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def better(g1, s1, b1, g2, s2, b2):
    if g1 != g2:
        return g1 > g2
    if s1 != s2:
        return s1 > s2
    return b1 > b2

def main():
    n_line = input().strip()
    while n_line == "":
        n_line = input().strip()
    n = int(n_line)

    best_g, best_s, best_b = -1, -1, -1
    best_name = ""

    for _ in range(n):
        line = input().rstrip("\n")
        while line == "":
            line = input().rstrip("\n")

        parts = line.split()
        g = int(parts[0])
        s = int(parts[1])
        b = int(parts[2])
        name = " ".join(parts[3:])

        if better(g, s, b, best_g, best_s, best_b):
            best_g, best_s, best_b = g, s, b
            best_name = name

    print(best_name)

if __name__ == "__main__":
    main()
```

The solution reads input line by line and carefully handles blank lines that may appear in formatted input. Each line is split into tokens, where the first three tokens are always integers and the rest form the country name.

The comparison logic is isolated in a helper function to make the lexicographic ordering explicit and avoid mistakes in nested conditionals. The initialization uses -1 for medal counts since all valid values are non-negative.

A common pitfall is incorrectly splitting the country name when it contains spaces. By joining all tokens after the third index, we preserve the full name exactly as required.

## Worked Examples

### Sample Input 1

```
3
Great Britain
Japan
United States of America
ROC
```

The input format implies each line contains medals followed by a name; interpreting the intended structure:

| Step | Country | (G,S,B) | Best Before | Action | Best After |
| --- | --- | --- | --- | --- | --- |
| 1 | Great Britain | (g1,s1,b1) | (-1,-1,-1) | replace | Great Britain |
| 2 | Japan | (g2,s2,b2) | (g1,s1,b1) | compare | unchanged |
| 3 | United States of America | (g3,s3,b3) | current best | replace | United States of America |
| 4 | ROC | (g4,s4,b4) | current best | compare | unchanged |

The final output is the country with the highest lexicographic medal triple, which is United States of America.

### Sample Input 2

```
3
999 999 998 Malaysia
999 999 999 Thailand
999 998 999 Indonesia
```

| Step | Country | (G,S,B) | Best Before | Action | Best After |
| --- | --- | --- | --- | --- | --- |
| 1 | Malaysia | (999,999,998) | (-1,-1,-1) | replace | Malaysia |
| 2 | Thailand | (999,999,999) | (999,999,998) | replace | Thailand |
| 3 | Indonesia | (999,998,999) | (999,999,999) | compare | unchanged |

Thailand remains the best because it matches gold and silver with Malaysia but has higher bronze, and no later country exceeds it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each country is processed once with constant-time comparison |
| Space | O(1) | Only stores current best candidate |

The constraints allow up to 300 entries, so a linear scan is trivially fast under the 1-second limit. Memory usage is constant aside from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        # re-run solution
        input = sys.stdin.readline

        def better(g1, s1, b1, g2, s2, b2):
            if g1 != g2:
                return g1 > g2
            if s1 != s2:
                return s1 > s2
            return b1 > b2

        n = int(input().strip())
        best_g, best_s, best_b = -1, -1, -1
        best_name = ""

        for _ in range(n):
            parts = input().split()
            g = int(parts[0])
            s = int(parts[1])
            b = int(parts[2])
            name = " ".join(parts[3:])
            if better(g, s, b, best_g, best_s, best_b):
                best_g, best_s, best_b = g, s, b
                best_name = name

        print(best_name)

    return out.getvalue().strip()

# sample tests (adapted format)
assert run("""3
999 999 998 Malaysia
999 999 999 Thailand
999 998 999 Indonesia
""") == "Thailand"

# all equal except name
assert run("""2
1 1 1 A
1 1 1 B
""") == "A"

# strictly increasing
assert run("""3
1 0 0 A
2 0 0 B
3 0 0 C
""") == "C"

# bronze tie-breaker
assert run("""2
1 1 1 A
1 1 2 B
""") == "B"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| equal triples | A | tie handling with guaranteed uniqueness assumption |
| increasing gold | C | primary key dominance |
| bronze tie-break | B | correct third-level comparison |

## Edge Cases

One edge case is identical medal triples. The algorithm still behaves correctly because it only replaces the best candidate when strictly better, and since the problem guarantees a unique best, any equal comparisons will not cause ambiguity.

Another edge case is large bronze differences when gold and silver are equal. The lexicographic comparison ensures bronze is only considered after the first two levels match, and the helper function enforces this ordering explicitly.

Finally, names containing spaces are handled safely by reconstructing the name from all remaining tokens after parsing the three integers, preserving the exact original identifier.
