---
title: "CF 102760H - Mock Competition Marketing"
description: "The problem models a sequence of advertisement auctions. There are only six possible advertisement types. Each type has a fixed price, and the company has a limited budget before the auctions start."
date: "2026-07-30T04:09:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "H"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 77
verified: true
draft: false
---

[CF 102760H - Mock Competition Marketing](https://codeforces.com/problemset/problem/102760/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a sequence of advertisement auctions. There are only six possible advertisement types. Each type has a fixed price, and the company has a limited budget before the auctions start. Before any auction happens, the company must decide which advertisement types it is willing to bid on.

When an auction appears, the company bids only if the auction's type was chosen beforehand and the remaining budget is enough to pay that type's price. If it bids, it wins immediately, spends the price, and gains one displayed advertisement. The goal is to choose the set of types so that the total number of successful bids is as large as possible.

The input contains the number of auctions, the initial budget, the six advertisement prices, and the type of each auction in chronological order. The output is the maximum number of advertisements that can be obtained by choosing the best possible set of advertisement types.

The number of auctions can reach 100,000, so an algorithm that repeatedly performs expensive work over the whole sequence many times is only acceptable if the number of repetitions is very small. A quadratic solution would require around 10 billion operations in the worst case, which is far beyond what is practical. The budget can be as large as 10^9, so the implementation also needs integer arithmetic that handles large remaining balances safely.

The small number of advertisement types is the key constraint. Since there are only six types, the number of possible sets of types is only 2^6 = 64. This completely changes the approach because checking every possible decision is feasible.

Several edge cases can break careless implementations. If the budget is smaller than every advertisement price, no bid can ever happen. For example:

```
1 0
5 6 7 8 9 10
1
```

The correct output is:

```
0
```

A solution that counts selected advertisement types instead of successful bids would incorrectly return a positive value.

Another edge case is when the company selects a type but can afford only some occurrences of it. For example:

```
4 5
3 4 5 6 7 8
1 1 1 1
```

The correct output is:

```
1
```

The first auction can be won because the price is 3. After spending that money, the remaining budget is 2, so every later auction of the same type must be ignored. A careless implementation might count all four occurrences.

A final case is when skipping a cheap type allows a more valuable sequence of purchases. For example:

```
5 10
2 10 1 100 100 100
1 2 1 2 1
```

The optimal output is:

```
3
```

The chosen types are 1 and 2. The company buys type 1, then type 2, then type 1 again. The ordering of auctions matters, so solutions that only look at total frequencies without simulating the sequence fail.

## Approaches

The first idea is to try every possible set of advertisement types. For each set, we simulate the auctions from left to right. During the simulation we keep the current amount of money, and whenever the current auction type belongs to the chosen set and we can afford it, we spend the money and increase the answer.

This brute-force approach is actually the optimal approach because the search space is tiny. If there were many advertisement types, checking every subset would be impossible. With six types, there are only 64 subsets. Each simulation takes O(N), so the total work is only 64 × N operations. For N = 100,000, this is about 6.4 million auction checks, which is easily manageable.

The observation that unlocks the solution is that the decision is not about choosing individual auctions. Once a type is selected, every future occurrence of that type is handled by the same rule. Since there are only six independent choices, the complete decision space fits inside a bitmask.

The brute-force approach works because the number of possible strategies is small. It would fail if the number of advertisement types grew, but the problem gives exactly the structure needed to enumerate all strategies directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all type subsets | O(2^6 × N) | O(1) | Accepted |
| Optimal subset enumeration with bitmask simulation | O(2^6 × N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Treat each possible chosen set of advertisement types as a six-bit mask. Bit i is set when advertisement type i is included in the strategy. There are only 64 masks, so we can test every possible strategy.
2. For each mask, reset the remaining budget to the initial value and start scanning the auctions from the beginning. Every mask represents a complete decision made before the auctions start, so the simulation must always begin with the original budget.
3. When processing an auction, check whether its advertisement type is enabled in the current mask. If it is not enabled, ignore the auction because the company decided before the auction sequence that it would never bid on this type.
4. If the type is enabled, compare the remaining budget with the price of that type. If the company can afford it, subtract the price and increase the number of successful bids. Otherwise, skip this auction.
5. After finishing the sequence, compare the number of successful bids from this mask with the best answer found so far. The largest value over all masks is the required result.

The reason this works is that every valid strategy corresponds to exactly one subset of the six advertisement types. The algorithm checks every possible subset, and the simulation for each subset follows the exact bidding rules of the problem. Since one of those subsets is optimal, the maximum value found must be the true answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K = map(int, input().split())
    price = list(map(int, input().split()))
    auctions = [int(x) - 1 for x in input().split()]

    ans = 0

    for mask in range(1 << 6):
        money = K
        count = 0

        for t in auctions:
            if (mask >> t) & 1 and money >= price[t]:
                money -= price[t]
                count += 1

        if count > ans:
            ans = count

    print(ans)

if __name__ == "__main__":
    solve()
```

The program represents the chosen advertisement types with an integer mask. The expression `(mask >> t) & 1` checks whether the current auction type is included in the strategy.

For every mask, the simulation variables are reset. The budget must be copied rather than reused because every strategy starts before any auction has happened.

The auction types are converted from one-based indexing to zero-based indexing immediately after reading. This avoids repeatedly subtracting one while processing the sequence.

There are no overflow concerns in Python because integers automatically grow as needed. The main implementation detail is preserving auction order. Sorting or grouping auctions would change the process because earlier purchases affect whether later bids are affordable.

## Worked Examples

For the first example:

```
6 10
1 2 3 4 5 6
6 5 4 3 2 1
```

One optimal mask selects types 1 through 4.

| Auction | Type | Remaining budget | Action | Count |
| --- | --- | --- | --- | --- |
| 1 | 6 | 10 | Skip | 0 |
| 2 | 5 | 10 | Skip | 0 |
| 3 | 4 | 10 | Buy, spend 4 | 1 |
| 4 | 3 | 6 | Buy, spend 3 | 2 |
| 5 | 2 | 3 | Buy, spend 2 | 3 |
| 6 | 1 | 1 | Cannot afford | 3 |

This trace shows why the solution must simulate the sequence. The same selected types can behave differently depending on when expensive auctions appear.

For the second example:

```
12 10
1 1 2 2 3 3
6 5 4 3 2 1 1 2 3 4 5 6
```

Choosing types 1, 2, 3, and 4 gives the following behavior.

| Auction | Type | Remaining budget | Action | Count |
| --- | --- | --- | --- | --- |
| 1 | 6 | 10 | Skip | 0 |
| 2 | 5 | 10 | Skip | 0 |
| 3 | 4 | 10 | Buy | 1 |
| 4 | 3 | 6 | Buy | 2 |
| 5 | 2 | 3 | Buy | 3 |
| 6 | 1 | 1 | Buy | 4 |
| 7 | 1 | 0 | Cannot afford | 4 |
| 8 | 2 | 0 | Cannot afford | 4 |
| 9 | 3 | 0 | Cannot afford | 4 |
| 10 | 4 | 0 | Cannot afford | 4 |
| 11 | 5 | 0 | Skip | 4 |
| 12 | 6 | 0 | Skip | 4 |

The trace demonstrates that the strategy is evaluated over the complete timeline. A type being selected does not guarantee that every occurrence will be purchased.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^6 × N) | There are 64 possible type sets, and each requires one pass through the auctions. |
| Space | O(1) | Only the current mask, budget, and counters are stored. |

With at most 100,000 auctions, the algorithm performs about 6.4 million checks. The constant factor is small because each check only involves a bit operation and a comparison.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    N, K = map(int, input().split())
    price = list(map(int, input().split()))
    auctions = [int(x) - 1 for x in input().split()]

    ans = 0
    for mask in range(64):
        money = K
        count = 0
        for t in auctions:
            if ((mask >> t) & 1) and money >= price[t]:
                money -= price[t]
                count += 1
        ans = max(ans, count)

    sys.stdin = old_stdin
    return str(ans)

assert solve_data("""6 10
1 2 3 4 5 6
6 5 4 3 2 1
""") == "4", "sample 1"

assert solve_data("""12 10
1 1 2 2 3 3
6 5 4 3 2 1 1 2 3 4 5 6
""") == "7", "sample 2"

assert solve_data("""1 0
5 6 7 8 9 10
1
""") == "0", "no budget"

assert solve_data("""4 5
3 4 5 6 7 8
1 1 1 1
""") == "1", "repeated expensive purchases"

assert solve_data("""5 10
2 10 1 100 100 100
1 2 1 2 1
""") == "3", "order dependency"

assert solve_data("""100000 1000000000
1 1 1 1 1 1
""" + "1 " * 99999 + "1\n") == "100000", "large input size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No budget with cheap-looking options | 0 | The algorithm counts only successful bids. |
| Same type appearing many times | 1 | Budget decreases after purchases and cannot be reused. |
| Mixed expensive and cheap sequence | 3 | Auction order affects the result. |
| Very large sequence | 100000 | The O(64N) approach handles maximum input size. |

## Edge Cases

When the budget is zero, every auction must be ignored because every advertisement price is positive. For the input:

```
1 0
5 6 7 8 9 10
1
```

every mask simulation keeps the budget at zero, so no purchase is possible and the answer remains zero.

When one advertisement type appears repeatedly, the algorithm correctly stops buying after the budget is exhausted. For:

```
4 5
3 4 5 6 7 8
1 1 1 1
```

the best mask includes type 1. The first auction spends 3 dollars, leaving 2 dollars. The next three auctions fail because the remaining budget is insufficient. The answer is one.

When multiple types compete for limited money, the subset enumeration checks all possible trade-offs. For:

```
5 10
2 10 1 100 100 100
1 2 1 2 1
```

the mask containing types 1 and 2 produces three successful purchases. The simulation sees the exact same budget changes that would happen in the real auction order, so it does not confuse total counts with achievable counts.
