---
title: "CF 102191F - Sum then Multiply"
description: "We have a positive integer array, and we must place cuts between elements to divide it into consecutive segments. Each segment contributes its sum, and the objective is to maximize the product of all those segment sums. The output is not the maximum value itself."
date: "2026-08-18T09:22:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "F"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 809
verified: false
draft: false
---

[CF 102191F - Sum then Multiply](https://codeforces.com/problemset/problem/102191/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We have a positive integer array, and we must place cuts between elements to divide it into consecutive segments. Each segment contributes its sum, and the objective is to maximize the product of all those segment sums. The output is not the maximum value itself. We must print one partition that achieves the maximum, using `/` between consecutive segments.

The central difficulty is that a cut changes two things at once. It replaces one factor, the sum of a larger segment, with two factors whose product we want to compare against that original sum. Since every array value is positive, this comparison has a particularly strong structure.

The array contains up to 3⋅10 5 elements, so an algorithm that examines all pairs of positions, or worse, all possible sets of cuts, is far beyond the one second limit. A quadratic algorithm already performs around 9⋅10 10 iterations at the maximum size. We need a linear or near-linear construction.

The values themselves can be as large as 10 9, but the algorithm only needs comparisons and additions involving them. Python integers also avoid overflow, although the solution never needs to compute the enormous final product.

There are several edge cases that are easy to mishandle. For the input

```
17
```

the only possible answer is `7`. There is no cut to make, so code that assumes there are at least two elements can fail.

For

```
31 1 1
```

the correct answer is `1 1 1`, with no slash. Splitting it into three factors gives 1, while keeping it as one segment gives 3. A strategy that always splits positive numbers would be wrong.

For

```
31 2 1
```

the optimal answer is `1 2 1`, because its product is 4. Splitting around the middle value gives `1 / 2 1`, whose product is 1⋅3=3. A strategy that always puts every value greater than one into its own segment would fail here.

There is also a less obvious case:

```
42 1 1 2
```

An optimal partition is `2 1 / 1 2`, giving 3⋅3=9. Putting both ones on either side gives 4⋅2=8. Thus the ones between two larger values cannot simply be assigned to one side. They have to be distributed optimally.

## Approaches

A direct brute-force solution considers every possible placement of cuts. There are n−1 gaps between consecutive elements, and every gap can either contain a cut or not, so there are exactly 2 n−1 partitions. For each partition we can compute the segment sums and their product and keep the best one. A straightforward implementation takes Θ(n2 n−1 ) arithmetic operations in the worst case, since a partition can contain Θ(n) segments. Even an improved enumeration that maintains the product incrementally still has Θ(2 n ) states, which is hopeless for n=3⋅10 5.

A natural dynamic programming formulation is also too slow. If `dp[i]` is the best product for the prefix ending at position i, we could try every previous cut position and use the sum of the corresponding suffix. That gives O(n 2 ), which is already much too large.

The key observation comes from comparing a segment with a possible cut inside it. Suppose a segment has total sum x+y, and cutting it produces two consecutive pieces with sums x and y. The old contribution is x+y, while the new contribution is xy. Since x and y are positive integers,

xy≥x+y

whenever x,y≥2, because

xy−x−y=(x−1)(y−1)−1≥0.

So whenever both sides of a potential cut have sum at least two, making the cut never decreases the answer.

This has a strong consequence. Since every array element greater than one already has sum at least two, an optimal partition can be chosen so that no segment contains two elements greater than one. If it did, we could cut between them and not make the result worse.

That means every segment in an optimal solution has at most one element greater than one. The only remaining question is what to do with runs of ones.

Consider two consecutive values greater than one, x and y, with exactly k ones between them:

x, k 1,1,…,1 ​ ​ ,y.

The k ones must be divided between the segment containing x and the segment containing y. If l ones go to the left and k−l go to the right, their contribution is

(x+l)(y+k−l).

The sum of these two factors is fixed:

x+l+y+k−l=x+y+k.

For two positive numbers with fixed sum, their product is largest when they are as close as possible. Thus we only need to choose l so that x+l is as close as possible to half of x+y+k.

Leading ones must all join the first value greater than one, and trailing ones must all join the last such value. If the whole array consists of ones, keeping the entire array as one segment is optimal.

This reduces the entire problem to scanning the array once, finding the values greater than one and the runs of ones between them, and deciding the split of each run independently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n2 n ) | O(n) | Too slow |
| Prefix DP | O(n 2 ) | O(n) | Too slow |
| Optimal construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Find every position whose value is greater than one. These values will serve as the anchors of the optimal segments. If there are no such positions, the array consists entirely of ones, so output the whole array as one segment.
2. Start the current segment with the first value greater than one and all ones appearing before it. Those leading ones cannot profitably stand alone, because multiplying by a factor of one is worse than adding the one to an existing segment.
3. Process every pair of consecutive values greater than one, call them x and y. Count the k ones between them.
4. Suppose l of those ones are assigned to the segment containing x. The remaining k−l ones belong to the segment containing y, so the two relevant sums are x+l and y+k−l.
5. Choose l closest to

2 y+k−x ​ .

The expression comes from making x+l as close as possible to half of the fixed total x+y+k. Clamp the result to the interval [0,k], because we cannot assign a negative number of ones or more than all k ones to the left.

1. Append those l ones to the current segment and finish that segment with a slash. Start the next segment with the remaining k−l ones followed by y.
2. After processing the final value greater than one, append all trailing ones to its segment. The resulting segments form a valid partition and achieve the maximum product.

### Why it works

Consider any segment containing two elements greater than one. Cutting somewhere between those two elements gives two subsegments whose sums are both at least two. If their sums are x and y, replacing the factor x+y by xy cannot decrease the product. Repeating this operation gives an optimal partition in which every segment contains at most one value greater than one.

Consequently, all choices are confined to runs of ones between two consecutive values greater than one. Such a run does not interact with any other run, because it changes only the two neighboring segment sums. For a run of k ones between x and y, its contribution is (x+l)(y+k−l), whose two factors have fixed sum. The product of two positive numbers with a fixed sum is maximized when they are as equal as possible, exactly what the chosen l does. Leading and trailing ones have only one possible useful neighbor, while an all-one array is best kept as one segment. Hence every independent part is optimal, and their combination is globally optimal.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n = int(input())    a = list(map(int, input().split()))
    big = [i for i, x in enumerate(a) if x > 1]
    if not big:        print(" ".join(map(str, a)))        return
    parts = []
    first = big[0]    current = a[:first + 1]
    for p in range(1, len(big)):        prev = big[p - 1]        cur = big[p]
        k = cur - prev - 1        x = a[prev]        y = a[cur]
        # Maximize (x + l) * (y + k - l).        # The ideal value is (y + k - x) / 2.        l = (y + k - x) // 2        l = max(0, min(k, l))
        current.extend([1] * l)        parts.append(current)
        current = [1] * (k - l)        current.append(y)
    last = big[-1]    current.extend(a[last + 1:])    parts.append(current)
    output = []    for i, part in enumerate(parts):        if i:            output.append("/")        output.extend(map(str, part))
    print(" ".join(output))

if __name__ == "__main__":    solve()
```

The `big` array stores exactly the positions whose values exceed one. These are the only values that can act as the central element of an optimal segment.

The initial `current` segment contains the first anchor and every leading one. The slice `a[:first + 1]` preserves the original order and handles the boundary before the first anchor without a special output case.

For two consecutive anchors, `k` is the number of ones strictly between their positions. The variable `l` is the number assigned to the left segment. The expression `(y + k - x) // 2` is the integer floor of the ideal value. Either neighboring integer is optimal when the ideal point lies exactly between two integers, so taking the floor is sufficient.

The `max` and `min` calls are necessary at the boundaries. For example, if x is much larger than y+k, the ideal value can be negative, which means all ones should go to the right. If y is much larger, all ones should go to the left.

The current segment is finalized before the next segment is created. This ordering matters because the left segment must contain the first `l` ones and the right segment must contain the remaining `k-l` ones. The final trailing ones are appended after all internal gaps have been processed.

The code never computes the final product. That product can have an enormous number of digits, and the problem only asks for a maximizing partition. Python's arbitrary precision integers are consequently not even relevant to the main algorithm.

## Worked Examples

### Sample 1

For the array `8 1 1 3`, the values greater than one are 8 and 3. There are two ones between them.

| Step | Current anchor | Next anchor | k | x | y | Chosen l | Segments so far |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 8 | 3 | 2 | 8 | 3 | 0 | `8` |
| Process gap | 8 | 3 | 2 | 8 | 3 | 0 | `8`, `1 1 3` |
| Finish | 3 | none | 0 | 3 |  |  | `8`, `1 1 3` |

The ideal value is

l=⌊ 2 3+2−8 ​ ⌋=−2,

which is clamped to zero. Thus both ones go to the right, giving segment sums 8 and 5, with product 40.

However, the sample output `8 / 1 1 / 3` gives 8⋅2⋅3=48, which is larger. This reveals a flaw in the proposed anchor characterization: a segment containing only ones can be useful when its sum is 2, because splitting a sum of 2 into factors 1⋅1 is worse, while keeping the two ones produces a factor 2.

So the earlier reduction must be refined. A run of ones can itself form a segment when it contains exactly two ones, and more generally its optimal handling depends on whether keeping a sum of two as a separate factor is better than attaching those ones to neighboring anchors.

This means the simple independent two-anchor construction above is not correct for the actual problem.

The correct solution requires a different structural reduction, so the code above must not be submitted.

## Correct Structural Insight

The decisive comparison is not merely whether both sides of a cut have sum at least two. For sums x,y,

xy≥x+y

holds for x,y≥2, with equality specifically when x=y=2.

Thus every segment can be refined until every resulting segment has sum either 1 or 2, except for the possibility that separating a segment changes neighboring choices. Since a segment of sum 1 is always harmful when another positive segment can absorb it, the only useful isolated small segment is a segment with sum 2.

Because all array elements are positive, a segment with sum 2 can only be either `[2]` or `[1, 1]`. Every element greater than two must be isolated from other elements in an optimal partition, while a value equal to two can compete with an adjacent pair of ones.

This leads to a much simpler local rule. Every value greater than two should be its own segment, with adjacent ones assigned according to the product comparison. Values equal to two can be treated exactly like a segment of two ones, and runs of ones must be partitioned into groups of two whenever they cannot profitably be attached to neighboring larger segments.

The resulting construction is more naturally expressed as a dynamic program over runs, because the boundary interaction around a value two can create equal-product alternatives.

Since the supplied problem statement does not include an official explanation and the search results only expose the statement, I should not present an unverified algorithm as a complete accepted editorial. The earlier claimed linear construction demonstrably fails Sample 1, so using it would produce incorrect code.

The sample itself gives the counterexample: for `8 1 1 3`, the optimal answer is `8 / 1 1 / 3`, with product 48, while assigning the two ones to the right gives 8/113, with product 40. This directly disproves the simplistic "every run of ones belongs to one of its neighboring anchors" rule.
