---
title: "CF 102191F - Sum then Multiply"
description: "We need to cut the array into consecutive subarrays. Each subarray contributes its element sum as one factor, and the objective is to maximize the product of all those factors. The output is the original array with / inserted between consecutive parts."
date: "2026-08-24T15:02:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "F"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 1481
verified: true
draft: false
---

[CF 102191F - Sum then Multiply](https://codeforces.com/problemset/problem/102191/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 24m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to cut the array into consecutive subarrays. Each subarray contributes its element sum as one factor, and the objective is to maximize the product of all those factors. The output is the original array with `/` inserted between consecutive parts.

The key difficulty is that the product can become astronomically large, so the task is not asking us to calculate the maximum product. We only need to recover one partition that achieves it. The constraints allow up to (3\cdot10^5) elements, so an (O(n)) or (O(n\log n)) solution is appropriate. Anything exponential is immediately impossible, and even an (O(n^2)) dynamic program would require around (9\cdot10^{10}) iterations in the worst case.

The fact that every array value is positive is what makes the problem collapse to a simple greedy construction. A careless implementation can fail when a part has sum (1). For example, for

```
2
3 1
```

the correct output is

```
3 1
```

because the partition `[3] / [1]` has product (3), while `[3 1]` has product (4). A strategy that cuts whenever the current sum reaches at least (2), then blindly prints the final singleton, would produce the invalidly suboptimal partition `[3] / [1]`.

Another boundary case is an array consisting entirely of ones. For

```
3
1 1 1
```

the correct output is

```
1 1 1
```

rather than `[1 1] / [1]`. The latter has product (2), while the single part has sum (3) and product (3). The final leftover one has to be merged with the previous part.

A single-element array also needs explicit consideration. For

```
1
1
```

there is no neighboring part with which the element can be merged, so the only possible answer is simply `1`.

## Approaches

A brute-force solution can enumerate every possible set of cuts. There are (n-1) gaps between adjacent elements, and every gap can either contain a cut or not, giving exactly (2^{n-1}) partitions. For each partition we can calculate all part sums and their product, then retain the best partition. Even if the product were maintained incrementally, this still requires (2^{n-1}) partition evaluations. If every partition is evaluated by scanning the whole array, the cost becomes (O(n2^n)). At (n=3\cdot10^5), even (2^{n-1}) itself is beyond any practical limit.

The observation that removes the exponential search is the inequality

[
xy \ge x+y
]

whenever (x,y\ge2). Consider two neighboring parts whose sums are (x) and (y). Keeping the cut gives product (xy), while removing the cut gives (x+y). If both sums are at least (2), keeping the cut never makes the answer worse.

This means an optimal solution should create as many parts with sum at least (2) as possible. The only dangerous part is one with sum (1). Since every array value is positive, a part with sum (1) consists of exactly one array element equal to (1). Such a part should be merged with an adjacent part whenever an adjacent part exists, because replacing a factor (1) and a factor (x) by (x+1) strictly increases the product.

The remaining question is how to maximize the number of parts whose sums are at least (2). The earliest possible place for a cut is the first position where the current part reaches sum (2). Cutting there is always safe and leaves the largest possible suffix for subsequent parts. Repeating this greedily gives the maximum possible number of complete parts. If the scan ends with one unused `1`, that final element cannot form a valid profitable part by itself, so it is merged into the preceding part.

The brute-force method works because it explicitly considers every possible placement of cuts, but fails because there are exponentially many such placements. The observation about (xy\ge x+y) changes the objective from searching over products to maximizing the number of valid parts, which can be done with one left-to-right scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Start at the first array element and maintain the start of the current part together with its running sum. The current part is not cut until its sum reaches at least (2), because a part with sum (1) is never useful when another element exists.
2. Scan the array from left to right. Whenever the running sum becomes at least (2), record a cut immediately after the current element and start a new part. Cutting at the earliest possible position maximizes the number of complete parts that can still be created later.
3. After the scan, check whether some suffix remains uncut. Because every previous cut was made as soon as its sum reached (2), an unfinished suffix can only have sum (1). Since all values are positive, that suffix is exactly one final element equal to `1`.
4. If there is such a final `1` and at least one previous part exists, remove the previous cut and extend that previous part through the final element. This eliminates the sum-(1) part, and merging it increases the product.
5. If the entire array consists of that one final element, no merge is possible. The single-element partition is the only possible partition.
6. Print every resulting subarray, placing `/` between consecutive parts.

### Why it works

Suppose two adjacent parts have sums (x,y\ge2). Their contribution when kept separate is (xy), while merging them gives (x+y). Since

[
xy-x-y=(x-1)(y-1)-1\ge0,
]

separating them never decreases the product. Thus, once every part has sum at least (2), maximizing the number of parts is sufficient.

The greedy scan always chooses the earliest possible endpoint for every part. Before a greedy endpoint is reached, the accumulated sum is below (2), so no valid part can end earlier. Consequently, the first greedy cut cannot occur later than the first cut of any partition into parts of sum at least (2). Applying the same argument to the remaining suffix proves the same property for every subsequent cut.

If the greedy scan finishes with a final `1`, that element cannot form a separate valid part. Any partition with one more part would need to leave a suffix after the corresponding previous cut, but that suffix would contain only this single `1`, which is impossible for a partition whose parts all have sum at least (2). Merging the final `1` with the previous part is thus optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    cuts = []
    start = 0
    current_sum = 0

    for i, x in enumerate(a):
        current_sum += x

        if current_sum >= 2:
            cuts.append(i)
            start = i + 1
            current_sum = 0

    # If one element remains, it must be a single 1.
    # Merge it into the previous part.
    if start < n:
        if cuts:
            cuts.pop()
            cuts.append(n - 1)
        else:
            cuts.append(n - 1)

    parts = []
    start = 0

    for end in cuts:
        parts.append(" ".join(map(str, a[start:end + 1])))
        start = end + 1

    return " / ".join(parts)

def main():
    data = sys.stdin.read()
    sys.stdout.write(solve(data) + "\n")

if __name__ == "__main__":
    main()
```

The input is read with `sys.stdin.read()` because there is only one test case and the whole input is small enough to keep in memory. This also avoids repeated parsing overhead in a problem with a (3\cdot10^5)-element array.

The `current_sum` variable represents the sum of the part currently being built. As soon as it reaches (2), the current index becomes a cut endpoint. Because all values are positive, once the sum reaches (2), extending the part further cannot help us create more parts.

The `cuts` list stores the inclusive endpoint of every completed part. If `start < n` after the scan, one element was left over. Its value must be `1`. When another part exists, the last cut is removed and replaced by `n - 1`, merging the leftover element into the previous part.

The case with no previous cut occurs only when the entire array is one final element, namely `n = 1` and `a[0] = 1`. In that case the single element is already the only possible partition.

Python integers do not overflow, although this solution never computes the product at all. That is useful here because the actual optimal product can have millions of decimal digits. The implementation only performs sums bounded by the input size and values, plus index operations.

The output is built from complete part strings and joined using `" / "`, which gives exactly one space on both sides of each slash as required.

## Worked Examples

### Sample 1

For the input

```
4
8 1 1 3
```

the scan behaves as follows.

| Index | Value | Running sum | Action | Cuts |
| --- | --- | --- | --- | --- |
| 0 | 8 | 8 | Cut after 8 | `[0]` |
| 1 | 1 | 1 | Continue | `[0]` |
| 2 | 1 | 2 | Cut after second 1 | `[0, 2]` |
| 3 | 3 | 3 | Cut after 3 | `[0, 2, 3]` |

Every produced part has sum at least (2). The resulting partition is

```
8 / 1 1 / 3
```

with factor values (8,2,3), giving product (48). The trace demonstrates the main greedy rule: cut immediately when the current sum first reaches (2).

### Sample 2

For

```
3
1 1 1
```

the scan is:

| Index | Value | Running sum | Action | Cuts |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | Continue | `[]` |
| 1 | 1 | 2 | Cut after second 1 | `[1]` |
| 2 | 1 | 1 | Leave unfinished | `[1]` |
| End |  | 1 leftover | Merge with previous part | `[2]` |

The final output is

```
1 1 1
```

The important part of this trace is the final merge. The greedy scan creates one complete part `[1,1]`, but the remaining `1` cannot be a separate useful factor. Merging it produces a single factor (3), which is better than the product (2\cdot1).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The array is scanned once, and every element is processed a constant number of times. |
| Space | (O(n)) | The array, cut positions, and output parts require linear memory. |

With (n\le3\cdot10^5), a linear scan is easily within the intended complexity. The algorithm never constructs or compares the enormous products themselves, which keeps both running time and memory practical under the 1 second and 256 MB limits.

## Test Cases

```
# helper: run solution on input string, return output string
import io

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided samples
assert run("4\n8 1 1 3\n") == "8 / 1 1 / 3", "sample 1"
assert run("3\n1 1 1\n") == "1 1 1", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "1", "single element equal to 1"

# All equal values
assert run("4\n2 2 2 2\n") == "2 / 2 / 2 / 2", "all equal values"

# Boundary case with a final singleton 1
assert run("3\n3 1 1\n") == "3 / 1 1", "trailing singleton handling"

# Maximum-size input, all ones
n = 300000
inp = str(n) + "\n" + ("1 " * (n - 1)) + "1\n"
expected = " / ".join(["1 1"] * (n // 2))
assert run(inp) == expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum-size array and the case where no merge is possible |
| `4 / 2 2 2 2` | `2 / 2 / 2 / 2` | Splitting parts with sums at least (2) never hurts |
| `3 / 3 1 1` | `3 / 1 1` | Correct handling of a final singleton and an early large value |
| `300000 / 1 1 ... 1` | 150000 parts of `1 1` | Maximum (n), linear performance, and repeated boundary decisions |

## Edge Cases

For the minimum input `1 / 1`, the scan never reaches sum (2), so there are no completed cuts. The remaining suffix is the entire array, but there is no previous part to merge it into. The algorithm consequently prints `1`, which is the only possible partition.

For `3 / 3 1`, the first element immediately forms a complete part with sum (3). The final `1` remains after the scan. Since there is a previous part, the algorithm removes the cut after `3` and merges the final element, producing `3 1`. The product is (4), which is better than the separate product (3).

For `3 / 1 1 1`, the first two ones reach sum (2), so the algorithm temporarily creates `[1,1]`. The last `1` remains as a singleton. The final merge changes the partition to `[1,1,1]`, whose factor is (3). This is optimal because the alternative product (2\cdot1) is smaller.

For an array of all values at least (2), every element can immediately form its own part. For example, `4 / 2 2 2 2` becomes `2 / 2 / 2 / 2`. Every pair of neighboring factors satisfies (xy\ge x+y), so combining any two parts cannot improve the product. The greedy partition consequently has the maximum possible number of parts and is optimal.

For the maximum-size input with (300000) ones, every pair reaches sum (2), so the scan creates 150000 parts and finishes with no leftover. The algorithm performs exactly one constant-time decision per array element and does not need any product calculation, making the large input behave the same way as the small all-ones example.
