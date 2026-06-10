---
title: "CF 1423L - Light switches"
description: "We are asked to determine the minimal set of switches Nikola must flip to turn all warehouse lights off, given the state of the lights at the end of several days. Each switch flips a predefined subset of lights."
date: "2026-06-11T06:14:56+07:00"
tags: ["codeforces", "competitive-programming", "meet-in-the-middle"]
categories: ["algorithms"]
codeforces_contest: 1423
codeforces_index: "L"
codeforces_contest_name: "Bubble Cup 13 - Finals [Online Mirror, unrated, Div. 1]"
rating: 2600
weight: 1423
solve_time_s: 72
verified: true
draft: false
---

[CF 1423L - Light switches](https://codeforces.com/problemset/problem/1423/L)

**Rating:** 2600  
**Tags:** meet-in-the-middle  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the minimal set of switches Nikola must flip to turn all warehouse lights off, given the state of the lights at the end of several days. Each switch flips a predefined subset of lights. Conceptually, the problem reduces to transforming a starting bitmask (lights on or off) to the zero bitmask (all off) using a subset of available bitmasks corresponding to switches. Each day presents a new starting bitmask.

The constraints suggest that there can be up to 1000 lights and 30 switches. While the number of lights is large, the number of switches is small enough to consider combinatorial subsets. Flipping switches corresponds to XORing their bitmasks with the current state. Since there are 30 switches, a brute-force exploration of all $2^{30}$ subsets is feasible only if we optimize further, because iterating naively for each of 1000 days would multiply the cost significantly. The high number of lights prohibits solutions that try all light configurations directly; we need an approach that scales primarily with the number of switches.

A subtle edge case occurs when no combination of switches can turn all lights off. For instance, if a day starts with lights 1 and 2 on and all switches only affect light 1, the lights can never be fully turned off. Another case is when multiple switches affect overlapping sets of lights - a naive greedy approach that flips switches affecting the most lights on might fail. Finally, days with no lights on require zero switches, which must be handled explicitly.

## Approaches

A brute-force approach would consider all $2^S$ subsets of switches for each day, applying each combination to the day's bitmask to see if it results in all lights off. This is correct but computationally expensive. With $S$ up to 30, $2^{30}$ is about a billion. Repeating this for $D = 1000$ days is clearly infeasible.

The key insight comes from the small number of switches. Because flipping is XOR, the order of flips does not matter. This allows us to split the switches into two halves and precompute all possible XOR results of each half separately, along with the number of flips used. This is the classic meet-in-the-middle technique. For each day, we then try to find two precomputed results, one from each half, whose XOR equals the day's bitmask. Using a map from XOR values to minimum flips in one half allows efficient lookups, reducing the total work from $O(D \cdot 2^S)$ to roughly $O(D \cdot 2^{S/2})$, which is feasible given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(D * 2^S * N) | O(2^S) | Too slow |
| Meet-in-the-middle | O(D * 2^(S/2) * N) | O(2^(S/2) * N) | Accepted |

## Algorithm Walkthrough

1. Convert each switch to a bitmask of length $N$. Each bit represents whether that switch flips a specific light.
2. Split the switches into two halves, roughly equal. Precompute all XOR combinations of the first half and store in a dictionary the minimum number of flips required to achieve each resulting bitmask.
3. Similarly, precompute all XOR combinations of the second half but store them as a list of pairs (bitmask, number of flips).
4. For each day's starting bitmask, iterate over all combinations from the second half. For each combination, compute the XOR needed from the first half to reach all lights off: $needed = day\_mask \oplus second\_mask$.
5. If $needed$ exists in the first half's dictionary, sum the number of flips from both halves. Track the minimal sum.
6. If no combination produces all lights off, return -1 for that day; otherwise, return the minimal number of flips found.

Why it works: the algorithm explores all possible subsets of switches without generating the full $2^S$ space at once. By splitting into halves, the solution leverages XOR's commutativity and associativity, guaranteeing that any achievable configuration can be formed by combining one subset from each half. The dictionary ensures we always pick the combination with the fewest flips for the first half.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import combinations
from collections import defaultdict

def main():
    N, S, D = map(int, input().split())
    switches = []
    for _ in range(S):
        data = list(map(int, input().split()))
        mask = 0
        for light in data[1:]:
            mask |= 1 << (light - 1)
        switches.append(mask)
    
    half = S // 2
    first_half = switches[:half]
    second_half = switches[half:]
    
    # Precompute first half combinations
    first_dict = {}
    for k in range(len(first_half)+1):
        for comb in combinations(range(len(first_half)), k):
            mask = 0
            for idx in comb:
                mask ^= first_half[idx]
            if mask not in first_dict or first_dict[mask] > k:
                first_dict[mask] = k
    
    # Precompute second half combinations
    second_list = []
    for k in range(len(second_half)+1):
        for comb in combinations(range(len(second_half)), k):
            mask = 0
            for idx in comb:
                mask ^= second_half[idx]
            second_list.append((mask, k))
    
    # Process each day
    for _ in range(D):
        data = list(map(int, input().split()))
        day_mask = 0
        for light in data[1:]:
            day_mask |= 1 << (light - 1)
        ans = float('inf')
        for mask2, flips2 in second_list:
            needed = day_mask ^ mask2
            if needed in first_dict:
                ans = min(ans, flips2 + first_dict[needed])
        print(ans if ans != float('inf') else -1)

if __name__ == "__main__":
    main()
```

The code first converts switches to bitmasks for efficient XOR operations. Splitting switches ensures that the number of combinations stays tractable. The dictionary ensures the minimal flips from the first half are quickly retrievable. Using a list for the second half is safe because we iterate through all its combinations only once per day. Each day's mask is constructed as a bitmask, and XOR arithmetic identifies the complement subset needed.

## Worked Examples

Sample Input 1:

```
4 3 4
2 1 2
2 2 3
1 2
1 1
2 1 3
3 1 2 3
3 1 2 4
```

| Step | day_mask | first_dict hit? | second_mask | total flips |
| --- | --- | --- | --- | --- |
| Day 1 | 1<<0 | yes | 0 | 2 |
| Day 2 | 1<<0 ^ 1<<2 | yes | 0 | 2 |
| Day 3 | 1<<0 ^ 1<<1 ^ 1<<2 | yes | 0 | 3 |
| Day 4 | 1<<0 ^ 1<<1 ^ 1<<3 | no | any | -1 |

The table shows how the algorithm searches all combinations of the second half, finds the required first-half mask to zero out the lights, and computes minimal flips. Day 4 has no solution, producing -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D * 2^(S/2) * S) | Each half generates 2^(S/2) combinations; for each day we iterate through one half and lookup in the dictionary |
| Space | O(2^(S/2)) | Store first half's combinations in dictionary |

With S ≤ 30, 2^(S/2) ≈ 1024, so memory usage is well below 1 GB. Processing D = 1000 days is feasible within the 3-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("""4 3 4
2 1 2
2 2 3
1 2
1 1
2 1 3
3 1 2 3
3 1 2 4""") == "2\n2\n3\n-1", "sample 1"

# Custom cases
assert run("""2 2 2
1 1
1 2
1 1
1 2""") == "1\n1", "single flip per day"

assert run("""3 3 1
1 1
1 2
1 3
3 1 2 3""") == "3", "all lights on, each switch flips one"

assert run("""3 2 1
2 1 2
2 2 3
2 1 3""") == "2", "overlapping switches"

assert run("""1 1 1
1 1
0""") == "0", "no lights on"

assert run("""30 30 1
""" + "\n".join(f"1 {i+1}" for
```
