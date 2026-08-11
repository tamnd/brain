---
title: "CF 102409K - Lending Woes"
description: "The original loans do not matter individually once we know each person's net position. For every loan a b c, person a has given away c, while person b has received c."
date: "2026-08-12T00:09:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "K"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 273
verified: true
draft: false
---

[CF 102409K - Lending Woes](https://codeforces.com/problemset/problem/102409/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The original loans do not matter individually once we know each person's net position. For every loan `a b c`, person `a` has given away `c`, while person `b` has received `c`. When all loans are combined, define the balance of a person as money they should receive minus money they should pay. A positive balance means that the person must receive that amount, a negative balance means that the person must pay its absolute value, and a zero balance means that the person is already settled.

For example, if `0` lent `1` five units and `1` later lent `2` five units, the balances are `0 = +5`, `1 = 0`, and `2 = -5`. The original middle transaction disappears from the problem, because person `0` can simply receive five units directly from person `2`.

The output is any collection of payments that brings every balance to zero. The first objective is to minimize the total amount transferred. Once that is optimal, the second objective is to minimize the number of payments. The required output format is the number of payments followed by their payer, receiver, and amount. The problem statement confirms that the original loan graph can be replaced by the resulting net balances.

The first objective has a simple characterization. Let the positive balances sum to `P`. Every positive-balance person must receive exactly their balance, so every valid settlement transfers at least `P` units. We can achieve exactly `P` by allowing only negative-balance people to pay positive-balance people. Thus the minimum total amount is fixed before we even start optimizing the number of payments.

The difficult part is the second objective. There are at most 18 people, which is the key constraint. A polynomial algorithm would be pleasant, but this problem contains a subset-sum-like choice: a group of people can be settled independently precisely when their balances sum to zero. Finding the best collection of such groups is exponential in general, so `N <= 18` is what makes a bitmask dynamic program practical. The number of loans can be as large as `100000`, but those loans only have to be accumulated into `N` balances, so their contribution is linear in `K`.

There are several edge cases that a direct implementation can mishandle.

Consider two people with opposite balances.

```
2 1
1 0 1
```

Person `0` has balance `-1` and person `1` has balance `+1`, so the only payment is `0 1 1`. A careless implementation that keeps the original loan direction would output the opposite direction and fail to settle the balances.

Now consider a person who ends up with balance zero even though they appeared in many loans.

```
3 2
0 1 5
1 0 5
```

Every balance is zero, so the correct output is simply

```
0
```

Keeping zero-balance people in the exponential DP does not change correctness, but it unnecessarily doubles the state space for every extra person. Removing them before the DP is a significant optimization when many loans cancel.

The more subtle case is when several independent zero-sum groups exist. For example,

```
4 2
0 2 2
1 3 2
```

gives balances `+2, +2, -2, -2`. Two payments are enough, one inside each pair. A greedy procedure that repeatedly picks an arbitrary debtor and creditor can still settle the money, but it can miss the fact that the participants split into independent components. The second objective is exactly about finding as many such independent components as possible.

Finally, the same pair can occur many times. The input

```
2 100000
0 1 1
0 1 1
...
0 1 1
```

with the line repeated `100000` times produces balances `-100000` and `+100000`. The original `100000` loans are irrelevant after aggregation, and only one settlement payment is needed. Using a per-loan state instead of a net balance would completely miss the structure that makes the problem small.

## Approaches

A brute-force solution can enumerate every possible partition of the non-zero people into groups. For each partition, check whether every group has balance sum zero. If it does, a group containing `s` people can be settled using `s-1` payments, so the total number of payments is minimized by the partition having the largest number of groups. This is correct because every connected component of a settlement must have total balance zero, and a zero-sum group of `s` people can always be settled with `s-1` payments.

The problem is the number of partitions. The number of set partitions of 18 labeled elements is the 18th Bell number, `682076806159`, roughly `6.82 * 10^11`. Even checking a constant amount of information for every partition is far beyond a one-second time limit.

The brute force works because it explicitly searches for the independent zero-sum groups. It fails because it searches for complete partitions when most of that information is redundant. The useful observation is that the only property of a group that matters is whether its balance sum is zero. That lets us represent every collection of people by a bitmask and reuse results for all smaller masks.

For a mask `S`, let `sum[S]` be the sum of its balances. Define `dp[S]` as the maximum number of pairwise disjoint zero-sum subsets that can be found inside `S`. This is a maximum zero-sum subpartition, not necessarily a partition of all of `S`.

Choose any person `x` in `S`. If `S` does not sum to zero, an optimal collection of zero-sum groups cannot contain every person in `S`, because those groups together would also have sum zero. At least one person can be removed without reducing the optimum. Thus we can take the best `dp[S without x]` over all choices of `x`.

If `S` itself sums to zero, an optimal zero-sum partition of `S` contains some group containing `x`. Removing `x` destroys exactly that group, while the remaining groups form a zero-sum subpartition of `S without x`. Consequently, the optimum is one larger than the best result for a mask obtained by removing one element.

This gives the recurrence

```
dp[S] = max dp[S without x]                         if sum[S] != 0
dp[S] = 1 + max dp[S without x]                    if sum[S] == 0
```

over all `x` in `S`. This recurrence is a standard `O(n 2^n)` dynamic programming formulation of maximum zero-sum partitioning.

The full set of non-zero balances has sum zero, so `dp[full]` is exactly the maximum number of independent zero-sum groups. If there are `m` non-zero people and `g` groups, each group of size `s` needs `s-1` payments. Summing over the groups gives

```
(s1 - 1) + (s2 - 1) + ... + (sg - 1)
= m - g
```

so maximizing `g` is exactly the same as minimizing the number of payments.

The DP only gives the optimal number of groups. To recover the actual groups, we backtrack. Pick one remaining person `x` and enumerate submasks containing `x` until finding a zero-sum subset `G` satisfying

```
dp[remaining without G] + 1 = dp[remaining]
```

Such a subset must exist by the definition of the DP. Once `G` is found, remove it and repeat.

After the groups are known, each group can be settled independently. Inside one group, repeatedly select one debtor and one creditor and transfer the smaller remaining amount. At least one of them becomes zero after every payment. Since the group starts with `s` non-zero balances and ends with all balances zero, exactly `s-1` payments are produced.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(B_n * n)` | `O(n)` | Too slow |
| Optimal | `O(K + n 2^n)` | `O(2^n)` | Accepted |

Here `B_n` is the nth Bell number, while the optimal method uses only `2^n` masks and examines at most `n` transitions per mask.

## Algorithm Walkthrough

1. Read every loan and accumulate net balances. For a loan `a b c`, add `c` to `balance[a]` and subtract `c` from `balance[b]`, because `a` is entitled to receive the money back while `b` owes it.
2. Remove every person whose final balance is zero. Such a person participates in no required settlement, and excluding them reduces the bitmask dimension without changing the answer.
3. Store the remaining balances in an array of length `m`. Since every original loan moves money from one person to another, the sum of all balances is zero.
4. Compute `sum[mask]` for every subset. Remove the lowest set bit from `mask`, reuse the already computed sum of the smaller mask, and add the corresponding balance. This computes all subset sums in `O(2^m)` time.
5. Initialize `dp[0] = 0`. For every non-empty mask, remove each possible set bit and inherit the best result from the smaller mask. If the current mask has sum zero, add one to the candidate because the current mask itself can form one zero-sum group.
6. Read `dp[full]` as the maximum possible number of independent zero-sum groups. Since a group with `s` people needs exactly `s-1` payments, the minimum number of payments is `m - dp[full]`.
7. Reconstruct the groups. Take the lowest set bit `x` of the current mask and enumerate its submasks. Find a submask `G` containing `x` whose sum is zero and for which `dp[current without G] + 1` equals `dp[current]`. This identifies one group used by an optimal partition.
8. Remove `G` from the current mask and continue until no people remain. The reconstruction considers at most `m` groups, and each reconstruction phase examines at most `2^m` submasks, which is still small for `m <= 18`.
9. For each recovered group, split its members into debtors with negative balances and creditors with positive balances. Match one debtor with one creditor and transfer the smaller absolute balance.
10. Update both remaining balances after every payment. If the debtor reaches zero, advance to the next debtor. If the creditor reaches zero, advance to the next creditor. At least one pointer advances every iteration, so a group of size `s` generates exactly `s-1` payments.

### Why it works

The key invariant is that `dp[mask]` equals the maximum number of disjoint zero-sum groups that can be selected from `mask`. If `mask` is not zero-sum, every zero-sum subpartition leaves at least one person unused, so removing a suitable person preserves the optimum. If `mask` is zero-sum, take the group containing any chosen person. Removing that person leaves all other groups intact, so the optimum for `mask` is exactly one more than the optimum for the corresponding smaller mask. This proves the recurrence by induction on the mask size.

For the full set, all non-zero people themselves sum to zero, so an optimal subpartition is actually a partition of everyone. If it contains `g` groups and `m` people, those groups require `m-g` payments. Maximizing `g` consequently minimizes the number of payments.

The final greedy settlement is correct inside each selected group because every payment transfers money only from a debtor to a creditor, so the total transferred amount is exactly the sum of positive balances. That is the minimum possible total transfer. Each payment makes at least one remaining balance zero, and the final payment makes the last two balances zero, giving exactly `s-1` payments for a group of `s` people.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(map(int, data.split()))
    try:
        n = next(it)
        k = next(it)
    except StopIteration:
        return ""

    balance = [0] * n

    for _ in range(k):
        a = next(it)
        b = next(it)
        c = next(it)

        balance[a] += c
        balance[b] -= c

    people = []
    vals = []

    for person, value in enumerate(balance):
        if value != 0:
            people.append(person)
            vals.append(value)

    m = len(vals)

    if m == 0:
        return "0\n"

    size = 1 << m

    subset_sum = [0] * size

    for mask in range(1, size):
        bit = mask & -mask
        idx = bit.bit_length() - 1
        subset_sum[mask] = subset_sum[mask ^ bit] + vals[idx]

    dp = [0] * size

    for mask in range(1, size):
        best = 0
        bits = mask

        if subset_sum[mask] == 0:
            while bits:
                bit = bits & -bits
                candidate = dp[mask ^ bit] + 1
                if candidate > best:
                    best = candidate
                bits ^= bit
        else:
            while bits:
                bit = bits & -bits
                candidate = dp[mask ^ bit]
                if candidate > best:
                    best = candidate
                bits ^= bit

        dp[mask] = best

    groups = []
    mask = size - 1

    while mask:
        first = mask & -mask
        sub = mask

        while sub:
            if (sub & first) and subset_sum[sub] == 0:
                rest = mask ^ sub
                if dp[rest] + 1 == dp[mask]:
                    groups.append(sub)
                    mask = rest
                    break
            sub = (sub - 1) & mask

    answer = []

    for group in groups:
        debtors = []
        creditors = []

        bits = group
        while bits:
            bit = bits & -bits
            idx = bit.bit_length() - 1

            if vals[idx] < 0:
                debtors.append([idx, -vals[idx]])
            else:
                creditors.append([idx, vals[idx]])

            bits ^= bit

        i = 0
        j = 0

        while i < len(debtors) and j < len(creditors):
            debtor, owe = debtors[i]
            creditor, receive = creditors[j]

            amount = min(owe, receive)

            answer.append((people[debtor], people[creditor], amount))

            owe -= amount
            receive -= amount

            debtors[i][1] = owe
            creditors[j][1] = receive

            if owe == 0:
                i += 1
            if receive == 0:
                j += 1

    out = [str(len(answer))]
    out.extend(f"{a} {b} {c}" for a, b, c in answer)
    return "\n".join(out) + "\n"

def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The input section uses `sys.stdin.buffer.read()` instead of repeatedly calling `input()`. With up to `100000` loans, reading the entire input at once is simple and fast, while the actual algorithm still has only `O(N)` financial state.

The balance update uses `balance[a] += c` and `balance[b] -= c`. Reversing these signs is a common source of wrong answers because the input describes the historical loan direction, while the output describes the direction of the eventual repayment.

The zero-balance people are filtered before constructing masks. Consequently, `m` can be smaller than `N`, and every mask bit corresponds to an actual non-zero balance. When all balances are zero, the function returns immediately and never creates a zero-sized DP array with special reconstruction logic.

The subset-sum array uses the lowest set bit. If `bit` is that bit, then `mask ^ bit` contains every other person, so `subset_sum[mask]` can be calculated from one previously computed entry. The values can reach about `10^8`, so Python integers comfortably handle them without overflow.

The DP transition deliberately considers every set bit instead of choosing only one fixed bit. The proof guarantees that at least one choice preserves an optimal subpartition, and considering all choices lets the recurrence discover that choice.

The reconstruction is separate from the DP because the recurrence stores only the optimal count, not the identity of every zero-sum group. Enumerating submasks during reconstruction is affordable because there are at most 18 non-zero people. It is also safer than trying to infer a group from the bit removed by the DP transition, since that bit does not by itself identify the corresponding zero-sum component.

The final settlement does not alter the original `vals` array. It works on small mutable `[person, amount]` pairs inside each group. This is useful because the DP describes the optimal partition, while the settlement phase only needs to construct one valid payment sequence for that partition.

## Worked Examples

### Sample 1

The input is

```
2 1
1 0 1
```

The loan makes person `1` a creditor and person `0` a debtor.

| State | Value |
| --- | --- |
| `balance[0]` | `-1` |
| `balance[1]` | `+1` |
| non-zero balances | `[-1, +1]` |
| `sum[01]` | `0` |
| `dp[01]` | `1` |
| recovered group | `{0, 1}` |

The recovered group contains one debtor and one creditor. Person `0` pays person `1` one unit.

```
1
0 1 1
```

The total transferred amount is one, which is unavoidable because person `1` must receive one unit. The group contains two people, so one payment is also the minimum possible count.

### Sample 2

The input is

```
3 4
2 0 2
1 0 1
1 0 1
2 0 1
```

The four loans give the following net balances.

| Person | Balance |
| --- | --- |
| `0` | `-5` |
| `1` | `+2` |
| `2` | `+3` |

There are three non-zero people, so the mask space has only eight states.

| Mask | People | Sum | `dp` |
| --- | --- | --- | --- |
| `001` | `0` | `-5` | `0` |
| `010` | `1` | `+2` | `0` |
| `100` | `2` | `+3` | `0` |
| `011` | `0,1` | `-3` | `0` |
| `101` | `0,2` | `-2` | `0` |
| `110` | `1,2` | `+5` | `0` |
| `111` | `0,1,2` | `0` | `1` |

There is no proper zero-sum subset, so all three people form one group. The settlement phase matches debtor `0` with creditor `1` for two units, then with creditor `2` for three units.

```
2
0 1 2
0 2 3
```

The sample uses the same two payments in the opposite creditor order, which is equally optimal.

The trace demonstrates why the DP must distinguish between a zero-sum group and an arbitrary collection of people. The full set is zero-sum, so it contributes one independent component, while no proper subset can be settled independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(K + m 2^m)` | `O(K)` to compute balances, `O(2^m)` for subset sums, `O(m 2^m)` for DP, and `O(m 2^m)` in the worst case for reconstruction |
| Space | `O(2^m + N)` | Subset sums and DP each contain `2^m` entries, while the balance arrays contain `O(N)` entries |

Since `m <= N <= 18`, there are at most `262144` masks. The main DP performs fewer than roughly `18 * 262144`, or `4.7 million`, bit transitions. The reconstruction has the same exponential scale and remains practical at this bound. The `100000` input loans add only a linear preprocessing pass, so the solution fits comfortably within the intended small-`N`, large-`K` structure of the problem.

## Test Cases

The tests below use the same `solve` function as the submitted solution. Since the problem accepts any optimal payment sequence, comparing the deterministic output of this implementation is sufficient for these fixed tests.

```python
import io
import sys

def solve(data: str) -> str:
    it = iter(map(int, data.split()))

    n = next(it)
    k = next(it)

    balance = [0] * n

    for _ in range(k):
        a = next(it)
        b = next(it)
        c = next(it)
        balance[a] += c
        balance[b] -= c

    people = []
    vals = []

    for person, value in enumerate(balance):
        if value:
            people.append(person)
            vals.append(value)

    m = len(vals)

    if m == 0:
        return "0\n"

    size = 1 << m
    subset_sum = [0] * size

    for mask in range(1, size):
        bit = mask & -mask
        idx = bit.bit_length() - 1
        subset_sum[mask] = subset_sum[mask ^ bit] + vals[idx]

    dp = [0] * size

    for mask in range(1, size):
        best = 0
        bits = mask

        while bits:
            bit = bits & -bits
            candidate = dp[mask ^ bit]

            if subset_sum[mask] == 0:
                candidate += 1

            if candidate > best:
                best = candidate

            bits ^= bit

        dp[mask] = best

    groups = []
    mask = size - 1

    while mask:
        first = mask & -mask
        sub = mask

        while sub:
            if (sub & first) and subset_sum[sub] == 0:
                rest = mask ^ sub
                if dp[rest] + 1 == dp[mask]:
                    groups.append(sub)
                    mask = rest
                    break
            sub = (sub - 1) & mask

    answer = []

    for group in groups:
        debtors = []
        creditors = []

        bits = group
        while bits:
            bit = bits & -bits
            idx = bit.bit_length() - 1

            if vals[idx] < 0:
                debtors.append([idx, -vals[idx]])
            else:
                creditors.append([idx, vals[idx]])

            bits ^= bit

        i = 0
        j = 0

        while i < len(debtors) and j < len(creditors):
            debtor, owe = debtors[i]
            creditor, receive = creditors[j]

            amount = min(owe, receive)

            answer.append(
                (people[debtor], people[creditor], amount)
            )

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] == 0:
                i += 1
            if creditors[j][1] == 0:
                j += 1

    out = [str(len(answer))]
    out.extend(f"{a} {b} {c}" for a, b, c in answer)
    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    return solve(inp)

assert run(
    """2 1
1 0 1
"""
) == """1
0 1 1
""", "sample 1"

assert run(
    """3 4
2 0 2
1 0 1
1 0 1
2 0 1
"""
) == """2
0 1 2
0 2 3
""", "sample 2"

assert run(
    """1 0
"""
) == """0
""", "minimum size with no loans"

assert run(
    """4 2
0 2 2
1 3 2
"""
) == """2
3 0 2
2 1 2
""", "two independent equal groups"

assert run(
    """3 1
0 1 1
"""
) == """1
1 0 1
""", "zero-balance participant"

large_input = "2 100000\n" + ("0 1 1\n" * 100000)

assert run(large_input) == """1
0 1 100000
""", "maximum K and large aggregated balance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 0 1` | `1 / 0 1 1` | Direct debtor-creditor direction |
| `3 4 / sample 2` | `2 / 0 1 2 / 0 2 3` | A single three-person zero-sum component |
| `1 0` | `0` | Empty settlement and smallest possible `N` |
| `4 2 / 0 2 2 / 1 3 2` | `2 / 3 0 2 / 2 1 2` | Multiple independent zero-sum groups |
| `3 1 / 0 1 1` | `1 / 1 0 1` | A person with zero final balance is removed |
| `2 100000` with repeated `0 1 1` | `1 / 0 1 100000` | Large `K`, aggregation of repeated loans, and large balance |

## Edge Cases

A direct opposite pair is the simplest zero-sum group. For

```
2 1
1 0 1
```

the balances after aggregation are `[-1, +1]`. The full mask has sum zero, so `dp[full] = 1`. Reconstruction selects both people as one group. The settlement phase finds debtor `0` and creditor `1`, transfers one unit, and both balances become zero. The output is

```
1
0 1 1
```

A person with zero balance must not create a fake transaction. For

```
3 2
0 1 5
1 0 5
```

the two loans cancel exactly, leaving balances `[0, 0, 0]`. The filtering step removes every person, so `m = 0` and the algorithm immediately outputs

```
0
```

This is also why the DP should be built from non-zero balances rather than from all `N` people.

Independent zero-sum components are the central case that defeats arbitrary greedy matching. For

```
4 2
0 2 2
1 3 2
```

the balances are `[+2, +2, -2, -2]`. The optimal partition has two groups, `{0,3}` and `{1,2}`. Each group needs one payment, so the final answer has two transactions:

```
2
3 0 2
2 1 2
```

The total transferred amount is four, equal to the sum of positive balances, and two payments is optimal because each independent pair already needs one.

Repeated loans exercise the distinction between input size and state size. With `100000` copies of `0 1 1`, the balances become `[-100000, +100000]`. The DP still contains only four masks because there are only two non-zero people. Reconstruction produces one group, and the settlement phase makes one payment of `100000`:

```
1
0 1 100000
```

The original `100000` loans are processed once each, but none of them creates a separate DP state.

A final boundary case is a single non-zero pair hidden among zero-balance people. For

```
3 1
0 1 1
```

the balances are `[+1, -1, 0]`. Person `2` is discarded, leaving the two-element DP state `[+1, -1]`. The resulting payment is

```
1
1 0 1
```

The zero-balance participant has no role in the settlement, and the bitmask indices refer only to the two remaining people, so the original person IDs must be preserved separately during reconstruction.
