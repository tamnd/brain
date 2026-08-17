---
title: "CF 102215H - Missing Number"
description: "We have an array of length n. Its elements are distinct integers from 0 through n, so exactly one value from that range does not occur. The array itself is hidden. We cannot read its values directly."
date: "2026-08-17T23:48:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "H"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 552
verified: false
draft: false
---

[CF 102215H - Missing Number](https://codeforces.com/problemset/problem/102215/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of length n. Its elements are distinct integers from 0 through n, so exactly one value from that range does not occur. The array itself is hidden. We cannot read its values directly. Instead, for any array position i and bit position b, we may ask the interactor for the b-th bit of a i ​.

The task is to determine the missing value while using at most 2n+19 bit queries. The official statement confirms that the interaction begins with n, each query returns one bit, and the final answer must be printed as `! x`.

The bound n≤1000 is small enough that ordinary computation over all values 0,…,n is cheap. The difficult constraint is the query limit. Reading every bit of every array element would use roughly nlog 2 ​ n queries, which is around 10000 queries when n=1000, far above the allowed 2019. The algorithm must reduce the number of questions, not merely optimize local computation.

There are two edge cases that commonly cause mistakes. First, the missing value can be 0. For example, with n=1, the only possible array is `[1]`, so the answer is `0`. A solution that initializes the answer to a nonzero value or treats zero as a special failure case can get this wrong.

Second, the missing value can be n, including when n itself is a power of two. For example, with n=4 and array `[0,1,2,3]`, the answer is `4`. Bit position 2 is needed because 4 is `100` in binary. A careless loop using only `range(int(log2(n)))` would stop before querying that bit and could never distinguish 4 from the smaller values.

The array is guaranteed to contain distinct values. Consequently, an input such as `n=3` with `[1,1,2]` is not a valid test case. In particular, an "all equal" array is outside the problem's domain, so it cannot meaningfully be used as a correctness test for the submitted interactive solution.

## Approaches

A direct solution would reconstruct every array element completely. Since every value is between 0 and n, each value needs at most ⌊log 2 ​ n⌋+1 bits. For n=1000, that is 10 bits, so reconstructing all 1000 elements requires 10000 queries in the worst case. Once the values are known, finding the missing number is trivial, but the query budget has already been exceeded.

The useful observation is that we do not need to know any complete array value. We only need to know the bits of the one value that is missing.

Suppose we already know several low bits of the missing number. Consider all values from 0 through n that have exactly those bits. Call them the possible values. Among the actual array elements, there is exactly one fewer element in the group containing the missing value, while every other group has exactly the expected number of elements.

Now query the next bit, but only for array positions whose already-known bits match the missing prefix. We obtain two groups, one with bit 0 and one with bit 1. We also know how many values from 0 through n should belong to each group. The group whose observed size is smaller than its expected size must contain the missing value.

The reason this saves queries is that after fixing b low bits, the possible numbers have the same remainder modulo 2 b. Their next bit splits them almost evenly. Thus the candidate array positions shrink by roughly a factor of two at every iteration. We never query positions that have already been eliminated.

The brute force works because every queried bit gives enough information to reconstruct an element, but it fails because it spends Θ(nlogn) queries reconstructing information we do not need. The observation that only the group containing the missing value matters lets us follow one path through this implicit binary partition, reducing the total number of queries to O(n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nlogn) queries | O(n) | Too many queries |
| Optimal | O(nlogn) local computation, O(n) queries | O(n) | Accepted |

## Algorithm Walkthrough

1. Start with every value from 0 through n as a possible missing value, and every array index as a candidate position.

At this point we know nothing about the missing number, so every value and every array element is relevant.
2. Process bit positions from the least significant bit upward through `n.bit_length() - 1`.

These are exactly the bits that can occur in a number from 0 through n. Processing low bits first is convenient because values with the same processed bits form a nearly even arithmetic progression, which gives the required shrinking property.
3. Split the current possible values into `possible_zero` and `possible_one` according to the current bit.

These lists tell us how many values should have bit 0 and bit 1 if none were missing.
4. For every current candidate array index, ask the interactor for this bit and split the indices into `candidate_zero` and `candidate_one`.

We only ask about candidates whose previously discovered bits agree with the missing number. Every other array element has already been ruled out as a source of the missing value.
5. Compare the observed group sizes with the expected group sizes.

If `len(candidate_zero) < len(possible_zero)`, the missing value has bit 0. Otherwise it has bit (1`, because exactly one value is absent from the group containing the missing number.
6. Keep only the corresponding value group and candidate index group.

The invariant is now preserved: `possible_values` contains exactly the values consistent with all discovered bits of the missing number, while `candidates` contains exactly the array positions whose values have those same bits.
7. Set the corresponding bit of the answer whenever the chosen group is the bit-1 group.

After processing every relevant bit, only one possible value remains. Print it with the interactive answer format.

### Why it works

At the beginning of every iteration, the candidate array positions represent all present values having the same processed bits as the missing value. The corresponding `possible_values` contain all values from 0 through n with that same bit pattern. Since exactly one value is missing, the actual array has one fewer element than expected precisely in the group containing the missing value. Comparing the observed and expected group sizes identifies the missing bit uniquely. Filtering both groups then preserves the invariant for the next bit. After all bits have been processed, two different values cannot share every relevant bit, so the remaining possible value is exactly the missing number.

## Python Solution

The actual Codeforces problem is interactive, so the program below must be submitted as an interactive solution. The empty lines shown in the statement's sample are only presentation formatting, and the real interaction requires flushing after every query and after the final answer.

```python
Pythonimport sysinput = sys.stdin.readline

def main():    n = int(input())
    possible_values = list(range(n + 1))    candidates = list(range(n))
    answer = 0
    for bit in range(n.bit_length()):        possible_zero = []        possible_one = []
        for value in possible_values:            if (value >> bit) & 1:                possible_one.append(value)            else:                possible_zero.append(value)
        candidate_zero = []        candidate_one = []
        for idx in candidates:            print("?", idx + 1, bit, flush=True)            response = int(input())
            if response == -1:                sys.exit(0)
            if response == 0:                candidate_zero.append(idx)            else:                candidate_one.append(idx)
        if len(candidate_zero) < len(possible_zero):            possible_values = possible_zero            candidates = candidate_zero        else:            possible_values = possible_one            candidates = candidate_one            answer |= 1 << bit
    print("!", answer, flush=True)

if __name__ == "__main__":    main()
```

The program first initializes `possible_values` with all n+1 values because any of them could initially be missing. `candidates` contains every array index because no position has yet been ruled out.

For each bit, the possible values are partitioned before asking questions. This gives the exact expected population of each bit group. The array positions are then queried one by one, and the responses form the corresponding observed groups.

The comparison `len(candidate_zero) < len(possible_zero)` is the central decision. There cannot be two missing values, so if the zero group is smaller than expected, its missing member must be the answer. If it is not smaller, the one group must be missing a member.

The answer bit is set only when the one group is selected. There is no need to explicitly construct the answer from `possible_values`, although after the final iteration that list contains exactly one number.

`idx + 1` is necessary because Python stores array indices from zero while the interactor numbers positions from one. The bit itself is not shifted or adjusted because the statement numbers bits starting from zero.

The loop uses `n.bit_length()` rather than `int(log2(n))`. For n=4, `n.bit_length()` is 3, so bits 0,1,2 are processed and value 4=100 2 ​ is handled correctly. Python integers do not overflow, so no special integer type is required.

The `flush=True` on every query is mandatory in an interactive problem. Without it, Python may keep the query in its output buffer while the program waits for the interactor's response, causing a deadlock. The statement explicitly requires every interaction message to be flushed.

## Worked Examples

The provided sample is an interaction transcript rather than a conventional array input. Its responses are consistent, for example, with the hidden array `[0, 3, 1]`, whose missing value is `2`. The sample asks three questions and receives the answers `0`, `1`, and `0`, eventually producing `2`.

| Bit | Possible values before | Queried candidate positions | Response groups | Chosen bit | Possible values after |
| --- | --- | --- | --- | --- | --- |
| 0 | 0, 1, 2, 3 | 1, 2, 3 | zero: 1, 3; one: 2 | 0 | 0, 2 |
| 1 | 0, 2 | 1, 3 | zero: 1, 3; one: none | 1 | 2 |

This table illustrates the general mechanism, although the exact sample transcript asks its questions in a different order. At bit 0, values `0` and `2` belong to the zero group, while values `1` and `3` belong to the one group. The observed array contains only one member of the one group, so the missing value has bit 0. At bit 1, among the remaining possibilities `0` and `2`, the missing value must have bit 1, leaving `2`.

For a second example, take n=4 and hidden array `[0, 1, 2, 3]`. The missing value is `4`.

| Bit | Possible values before | Zero group size | One group size | Observed zero | Observed one | Chosen bit |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0, 1, 2, 3, 4 | 3 | 2 | 2 | 2 | 0 |
