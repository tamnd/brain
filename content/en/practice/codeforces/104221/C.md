---
title: "CF 104221C - \u041a\u0443\u0437\u044f \u0438 \u0434\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f"
description: "Kuzya is preparing a birthday party, but the number of guests he can invite depends entirely on how a cake is sliced at an unknown bakery. There are several bakeries in his city, and each bakery always cuts a cake into a fixed number of slices."
date: "2026-07-01T23:45:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104221
codeforces_index: "C"
codeforces_contest_name: "\u0424\u0438\u043d\u0430\u043b \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b \u00ab\u041c\u0430\u0448\u0438\u043d\u0430 \u0422\u044c\u044e\u0440\u0438\u043d\u0433\u0430\u00bb \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104221
solve_time_s: 68
verified: true
draft: false
---

[CF 104221C - \u041a\u0443\u0437\u044f \u0438 \u0434\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/104221/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Kuzya is preparing a birthday party, but the number of guests he can invite depends entirely on how a cake is sliced at an unknown bakery. There are several bakeries in his city, and each bakery always cuts a cake into a fixed number of slices. Kuzya will not know in advance which bakery his mother chooses.

He wants to choose a number of guests so that no matter which bakery is used, the cake can be split evenly among everyone at the party, including Kuzya himself. Every person must receive exactly the same number of slices, and nothing can remain unused.

Reframing this more concretely, we are given several numbers, each describing how many equal pieces a cake could be cut into. We must choose a group size such that for every possible cake size, that cake can be partitioned evenly among the group.

The output is the maximum possible number of guests under this constraint. Since Kuzya himself is also attending, the total number of people is one more than the number we output.

The constraint of up to 100,000 bakeries with cake sizes up to 10^9 immediately rules out any solution that tries all possible group sizes and checks them individually in a naive way. A direct divisibility check for each candidate would lead to roughly 10^14 operations in the worst case, which is far beyond feasible limits.

A common subtle failure case appears when the numbers have no meaningful common structure. For example, if the bakeries produce 2, 3, and 5 slices, there is no way to choose a group size larger than zero guests, because no integer greater than 1 divides all of them. Another tricky case is when all values are identical, where the answer is simply that value minus one, since the entire cake size itself is the limiting factor.

## Approaches

The brute-force approach is to try every possible number of people in the party and verify whether that number divides all cake sizes. Concretely, we would iterate over candidate group sizes from 1 up to the minimum value in the array, and for each candidate check divisibility against all bakeries. This is correct because it directly enforces the condition that every cake can be evenly split among the chosen number of people.

However, this approach is too slow. In the worst case, we might have values up to 10^9 and 100,000 bakeries. Even restricting candidates to the minimum element, we still face up to 10^9 checks, and each check scans 100,000 elements, leading to about 10^14 operations.

The key observation is that the condition “a group size works for all bakeries” means that the number of people must divide every single a_i. That is exactly the definition of a common divisor of the entire array. Instead of testing all candidates, we only need the greatest integer that divides all elements, which is the greatest common divisor.

Once we compute the gcd of all values, any valid group size must divide this gcd, and the largest possible choice is the gcd itself. Since Kuzya includes himself in the count, the number of guests is one less than the group size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · min(a_i)) | O(1) | Too slow |
| Optimal (GCD) | O(n log A) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce the problem to finding the greatest common divisor of all cake sizes.

1. Start with the first bakery’s cake size as the initial candidate gcd value.
2. Iterate over all remaining bakery values, updating the gcd with each new number.

Each update replaces the current gcd with gcd(gcd, a_i), shrinking or keeping it unchanged.
3. After processing all values, the final gcd represents the largest number of cake slices that can be evenly distributed across all bakeries.
4. Convert this into the number of guests by subtracting one, since the gcd represents total people (guests plus Kuzya).

The reason we subtract one is structural: if the cake can be split into d equal parts, then there are exactly d people in the party, so guests are d minus one.

### Why it works

At every step, the running gcd is the largest integer that divides all processed elements so far. When we include a new element, updating with gcd preserves exactly the set of common divisors. This invariant ensures that after the final element, the result is the greatest number that divides every a_i, so no larger valid group size can exist.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd

n = int(input())
a = list(map(int, input().split()))

g = a[0]
for x in a[1:]:
    g = gcd(g, x)

print(g - 1)
```

The solution reads all bakery cake sizes and maintains a running gcd. The `math.gcd` function efficiently computes the greatest common divisor in logarithmic time per call, which is important given the large bounds.

The final subtraction by one directly reflects that the gcd counts total participants, not just guests.

A common implementation pitfall is forgetting to initialize the gcd with the first element and instead starting from zero. While mathematically gcd(0, x) = x, this is safe but less explicit; initializing with `a[0]` avoids confusion and matches the invariant description more cleanly.

## Worked Examples

### Sample 1

Input:

```
2
5 10
```

We compute the gcd progressively.

| Step | Current Value | Running GCD |
| --- | --- | --- |
| 1 | 5 | 5 |
| 2 | 10 | 5 |

The final gcd is 5, meaning the party can have 5 people total. Kuzya is one of them, so the number of guests is 4.

Output:

```
4
```

This demonstrates a case where a non-trivial shared divisor exists and remains stable across updates.

### Sample 2

Input:

```
5
2 7 8 10 5
```

| Step | Current Value | Running GCD |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 7 | 1 |
| 3 | 8 | 1 |
| 4 | 10 | 1 |
| 5 | 5 | 1 |

The gcd collapses to 1 early, meaning no group larger than one person can be formed. Therefore, there are zero guests.

Output:

```
0
```

This shows how the gcd quickly captures incompatibility among values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each gcd computation is logarithmic in the value size, applied over n elements |
| Space | O(1) | Only a single running gcd value is stored |

The constraints allow up to 100,000 values, and each value is up to 10^9, so logarithmic gcd operations comfortably fit within time limits.

## Test Cases

```python
import sys, io
from math import gcd

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    g = a[0]
    for x in a[1:]:
        g = gcd(g, x)

    return str(g - 1)

def run(inp: str) -> str:
    return solve(inp)

# provided samples
assert run("2\n5 10\n") == "4"
assert run("5\n2 7 8 10 5\n") == "0"

# custom tests
assert run("1\n7\n") == "6", "single bakery"
assert run("3\n6 12 18\n") == "5", "clear gcd structure"
assert run("4\n1 1 1 1\n") == "0", "all ones edge"
assert run("2\n1000000000 500000000\n") == "499999999", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 number | single value minus one | minimal input handling |
| 6 12 18 | 5 | multi-step gcd stability |
| all ones | 0 | smallest gcd case |
| large numbers | correct arithmetic | overflow and scale handling |

## Edge Cases

When there is only one bakery, the gcd is simply that value, so the answer becomes a_i - 1. The algorithm handles this naturally because the loop over remaining elements is skipped, leaving the initial value intact.

For an input like 7, the running gcd is 7, so the output becomes 6, meaning six guests plus Kuzya.

When all values are equal, such as 10 10 10, the gcd remains 10 throughout. This means the party can have 10 people total, so 9 guests. The algorithm preserves this because gcd(a, a) is always a.

When the array contains 1, the gcd immediately becomes 1, and no further updates can change it. This correctly forces the answer to zero guests, since no group larger than one person can be formed.
