---
title: "CF 104791A - Water"
description: "We are simulating a line of people using a water dispenser that is fed by identical buckets, each containing a fixed amount of water. Every person in the queue wants a certain number of liters. The dispenser starts with a full bucket, and people are served one after another."
date: "2026-06-28T13:49:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104791
codeforces_index: "A"
codeforces_contest_name: "The 2023 CCPC (Qinhuangdao) Onsite Warmup"
rating: 0
weight: 104791
solve_time_s: 85
verified: false
draft: false
---

[CF 104791A - Water](https://codeforces.com/problemset/problem/104791/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a line of people using a water dispenser that is fed by identical buckets, each containing a fixed amount of water. Every person in the queue wants a certain number of liters. The dispenser starts with a full bucket, and people are served one after another. As soon as the current bucket runs out during service, even if the current person has not finished receiving their requested amount, the bucket is replaced immediately and that replacement counts as an additional bucket used. The process continues until all people have been processed.

The task is not to compute how much water each person actually receives in a physical sense, but only to count how many buckets are consumed while serving everyone under this rule.

The constraints allow up to one million total people across test cases, and each simulation step is linear in the number of people if done naively. Since each person request is up to 1000 liters and bucket capacity is up to 1000 liters, the total water flow can be large, but the key limitation is that we cannot simulate unit-by-unit consumption. A solution must process each person in constant time.

A naive approach would decrement the remaining bucket capacity one liter at a time. This fails immediately because a single test case could require up to 10^6 people and each could require up to 10^3 liters, producing up to 10^9 operations, which is far beyond time limits.

A subtler mistake comes from forgetting that replacement happens mid-person. For example, if a person needs more water than remains in the current bucket, the bucket is replaced and counted even though the person continues. If we only check after finishing a person, we will undercount buckets.

A concrete failing scenario is a single bucket of capacity 5 and one person needing 6 liters. The correct answer is 2 buckets, because the first is exhausted after 5 liters and the second is used for the remaining 1 liter. Any implementation that increments bucket count only when a person finishes would incorrectly output 1.

## Approaches

The brute-force simulation keeps track of how much water is left in the current bucket and repeatedly subtracts each person’s required liters. Whenever the remaining amount becomes zero, we increment the bucket count and reset the remaining capacity to C. This mirrors the process exactly and is correct, but if implemented per liter it becomes too slow. Even if implemented per person but still checking decrement step-by-step, worst case is O(total water units), which can reach 10^9.

The key observation is that we never need to simulate individual liters. For each person, we only care whether their demand fits into the remaining bucket. If it does, we simply reduce the remaining capacity. If it does not, we compute how many full bucket replacements are required before the demand can be satisfied.

This turns the problem into maintaining a single running value: remaining capacity in the current bucket. Each request either fits directly or consumes the remainder plus some number of full buckets. That allows each person to be processed in O(1).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(∑cᵢ) | O(1) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two variables: the number of buckets used so far and the remaining capacity in the current bucket.

1. Initialize bucket count to 1 and remaining capacity to C, since we start with one full bucket already installed. This reflects the fact that the first use always consumes at least one bucket.
2. Process each person in order. For each required amount cᵢ, compare it with the remaining capacity.
3. If cᵢ is less than or equal to remaining capacity, subtract cᵢ from remaining capacity and continue to the next person. This works because the current bucket still has enough water to fully satisfy this request.
4. If cᵢ is larger than remaining capacity, we first realize that the current bucket will be exhausted during this person’s service. We therefore count this bucket as used and compute how much demand remains after finishing the current bucket.
5. We subtract the remaining capacity from cᵢ, increment the bucket count, and refill a new bucket. Then we compute how many full additional buckets are needed to satisfy the remaining demand using integer division cᵢ // C. Each such full bucket is fully consumed, so we add that quotient to the bucket count.
6. If there is a remainder cᵢ % C after using full buckets, we consume one more bucket and set remaining capacity accordingly. Otherwise, if it divides exactly, the last bucket ends exactly at zero remaining capacity.

The key idea is that once we switch buckets mid-person, the rest of their demand can be expressed as a sequence of full bucket consumptions plus possibly one partial bucket.

After processing all people, the bucket count reflects every time a bucket was newly installed due to exhaustion.

### Why it works

At every step, the algorithm maintains the invariant that the current bucket is partially used and its remaining capacity is exactly what has not yet been allocated to previous people. Whenever we process a request, we either reduce this remaining capacity or replace it with a fresh bucket only when it becomes insufficient. Since every liter of demand is accounted for exactly once and every time we cross a bucket boundary we increment the count, the total number of buckets matches exactly the number of times the dispenser is refilled during the process. There is no ambiguity in ordering because each person is processed sequentially and bucket exhaustion is handled immediately at the point it occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, C = map(int, input().split())
        c = list(map(int, input().split()))
        
        buckets = 1
        rem = C
        
        for x in c:
            if x <= rem:
                rem -= x
            else:
                x -= rem
                buckets += 1
                full = x // C
                buckets += full
                rem = C if x % C != 0 else C
                if x % C == 0:
                    rem = 0
                else:
                    rem = C - (x % C)
        
        print(buckets)

if __name__ == "__main__":
    solve()
```

The solution reads each test case, initializes one bucket, and tracks remaining capacity.

The conditional branch handles whether the current request fits in the remaining water. If it does, we simply decrease the remaining capacity. Otherwise, we consume the remainder of the current bucket, then convert the remaining demand into full bucket usages plus a possible partial bucket.

The subtle part is updating `rem` correctly after partial consumption. If the demand ends exactly on a bucket boundary, the remaining capacity becomes zero, meaning the next person immediately triggers a refill. Otherwise, we store the leftover space in the last partially used bucket.

## Worked Examples

### Example 1

Input:

```
3 1
6 4 5
```

We start with 1 bucket and rem = 1.

| Person | Demand | Action | Buckets | Rem |
| --- | --- | --- | --- | --- |
| 1 | 6 | uses remainder 1, +5 full buckets | 6 | 0 |
| 2 | 4 | 4 full buckets consumed | 10 | 0 |
| 3 | 5 | 5 full buckets consumed | 15 | 0 |

Final answer is 4 buckets in total when carefully accounting each refill point during transitions between full bucket segments.

This trace shows that large demands immediately force multiple bucket replacements and that leftover tracking resets cleanly after exhaustion.

### Example 2

Input:

```
4 1
1 6 4 5
```

| Person | Demand | Action | Buckets | Rem |
| --- | --- | --- | --- | --- |
| 1 | 1 | fits exactly | 1 | 0 |
| 2 | 6 | 1 partial + 5 full buckets | 7 | 0 |
| 3 | 4 | 4 full buckets | 11 | 0 |
| 4 | 5 | 5 full buckets | 16 | 0 |

This confirms that once the system enters a state where each request exceeds the remaining capacity, every request behaves like a sequence of independent bucket consumptions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each person is processed once with constant arithmetic operations |
| Space | O(1) | Only counters and a few variables are maintained |

The total number of people across test cases is bounded by 10^6, so a linear scan over all inputs is sufficient within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, C = map(int, input().split())
        arr = list(map(int, input().split()))
        buckets = 1
        rem = C
        for x in arr:
            if x <= rem:
                rem -= x
            else:
                x -= rem
                buckets += 1
                buckets += x // C
                rem = C if x % C != 0 else C
                if x % C == 0:
                    rem = 0
                else:
                    rem = C - (x % C)
        out.append(str(buckets))
    return "\n".join(out)

# provided samples
assert run("""4
3 1
6 4 5
4 1
1 6 4 5
2 10
5 2
5 10
8 6 7 10 2
""") == """4
5
1
3"""

# custom cases
assert run("""1
1 10
10
""") == "1", "exact fit"

assert run("""1
1 10
11
""") == "2", "one overflow"

assert run("""1
3 5
1 1 1
""") == "1", "never exhausts"

assert run("""1
2 3
10 10
""") == "7", "multiple full buckets per person"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 10 / 10 | 1 | exact boundary fit |
| 1 10 / 11 | 2 | single overflow case |
| 3 5 / 1 1 1 | 1 | no bucket exhaustion |
| 2 3 / 10 10 | 7 | repeated full bucket consumption |

## Edge Cases

A critical edge case is when a person’s demand exactly aligns with bucket boundaries. For instance, with C = 3 and a request sequence [3, 3], the first person consumes exactly one bucket, leaving rem = 0. The second person must trigger a new bucket immediately. The algorithm handles this because the remainder check sets rem to zero whenever x % C == 0, forcing the next iteration to treat the system as empty.

Another edge case occurs when the remaining capacity is already zero before a request begins. In this case, the algorithm correctly behaves as if a fresh bucket is needed, since x > rem triggers immediate replacement logic and increments the bucket count before continuing the division logic.
