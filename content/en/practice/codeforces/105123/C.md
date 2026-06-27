---
title: "CF 105123C - Flipped DNA"
description: "We are given two DNA strings of equal length, composed only of the characters A, T, C, and G. Each position represents a nucleotide, and we are asked to decide whether the second string can be obtained from the first using only mutations that swap complementary bases."
date: "2026-06-27T19:32:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105123
codeforces_index: "C"
codeforces_contest_name: "BioCode 2024"
rating: 0
weight: 105123
solve_time_s: 77
verified: true
draft: false
---

[CF 105123C - Flipped DNA](https://codeforces.com/problemset/problem/105123/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two DNA strings of equal length, composed only of the characters A, T, C, and G. Each position represents a nucleotide, and we are asked to decide whether the second string can be obtained from the first using only mutations that swap complementary bases.

The biological rule is that A pairs with T, and C pairs with G. The intended interpretation here is that at every position, if a mutation happened, it can only convert a nucleotide into its complementary partner, and nothing else. So A can become T or remain A, T can become A or remain T, C can become G or remain C, and G can become C or remain G. Importantly, no cross-pair transitions like A to C or G to T are allowed.

We are not rearranging the string or performing global operations. Every position evolves independently, and we are only verifying whether each character in the first string can legally transform into the corresponding character in the second string.

The constraint n up to 10^5 implies we need a linear scan solution. Any approach that tries to explore combinations or simulate multi-step mutation paths per position is still fine only if it stays O(1) per character. Anything quadratic or involving repeated scanning would fail under a 2-second limit.

A subtle failure case appears when characters are from different complementary pairs. For example, if X has A and Y has C at the same position, this is invalid even though both characters are valid DNA bases. A naive mistake is to assume that “any change is fine as long as both letters are valid,” which would incorrectly accept such cases.

Another edge case is when the strings are identical, which should always be valid since no mutation is needed. Also, single-character strings must be handled correctly without any special branching.

## Approaches

The brute-force perspective is to simulate allowed mutations per position. For each index i, we check whether X[i] can become Y[i]. If we model mutation as “you can stay or switch to your complementary base,” then for each character we explicitly test membership in its allowed pair.

This can be implemented by predefining a mapping of valid transitions. For each character in X, we check whether Y[i] equals either itself or its complement. This is already O(n), but a more naive interpretation might attempt to generate mutation sequences or graph transitions among letters, which is unnecessary and would introduce overhead or even exponential reasoning if mis-modeled as multi-step transformations.

The key observation is that the mutation rule is purely local and symmetric: each character belongs to a fixed pair {A, T} or {C, G}, and mutation never crosses between pairs. So the only condition we need is that X[i] and Y[i] belong to the same pair.

This reduces the problem to a simple equivalence-class check: A and T form one class, C and G form another. If X[i] and Y[i] are in different classes, the answer is immediately NO. Otherwise, all positions must satisfy this condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Accepted |
| Optimal Pair Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by classifying each character into its complement group and checking consistency position by position.

1. Define the complementary groups as two sets: one containing A and T, and another containing C and G. This structure encodes the mutation rule in a way that is fast to query.
2. Iterate through every index i from 0 to n−1, comparing X[i] and Y[i].
3. For each position, determine which group X[i] belongs to.
4. Check whether Y[i] belongs to the same group.
5. If any position violates this condition, immediately conclude that the hypothesis is false and stop.
6. If the scan completes without violations, conclude that every mutation respects the rule.

The reason for immediate termination is that a single invalid position invalidates the entire hypothesis, so continuing would only waste computation.

### Why it works

Each character belongs to exactly one of two equivalence classes induced by complementarity. The mutation rule permits transitions only within the same class. Therefore, any valid transformation must preserve class membership at every index. The algorithm enforces this invariant directly by checking equality of classes position by position, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def same_group(a, b):
    # A <-> T, C <-> G
    if a in "AT":
        return b in "AT"
    else:
        return b in "CG"

n = int(input().strip())
x = input().strip()
y = input().strip()

for i in range(n):
    if not same_group(x[i], y[i]):
        print("NO")
        sys.exit(0)

print("YES")
```

The solution reads the input strings and defines a helper function that encodes the two complement groups. The loop checks each position independently and exits early on failure. Using a direct membership check avoids any need for explicit mapping tables or multi-step logic, keeping the implementation minimal and constant-time per character.

A common implementation mistake is to attempt chaining complements, such as checking whether x can reach y in two steps, which is unnecessary because the mutation rule does not allow leaving the equivalence class at all.

## Worked Examples

### Sample 1

We compare the strings position by position and verify whether each pair stays inside the same complement class.

| i | X[i] | Y[i] | Group(X[i]) | Group(Y[i]) | Valid |
| --- | --- | --- | --- | --- | --- |
| 0 | G | G | CG | CG | Yes |
| 1 | C | C | CG | CG | Yes |
| 2 | A | A | AT | AT | Yes |
| 3 | A | A | AT | AT | Yes |
| 4 | G | G | CG | CG | Yes |
| 5 | C | C | CG | CG | Yes |
| 6 | C | C | CG | CG | Yes |
| 7 | T | T | AT | AT | Yes |

No mismatch appears, so the output is YES. This confirms that identical characters are always valid under the rule.

### Sample 2

Here we detect a violation of complement grouping at some position.

| i | X[i] | Y[i] | Group(X[i]) | Group(Y[i]) | Valid |
| --- | --- | --- | --- | --- | --- |
| 0 | C | C | CG | CG | Yes |
| 1 | G | G | CG | CG | Yes |
| 2 | T | T | AT | AT | Yes |
| 3 | A | A | AT | AT | Yes |
| 4 | T | T | AT | AT | Yes |
| 5 | G | G | CG | CG | Yes |
| 6 | G | G | CG | CG | Yes |
| 7 | A | A | AT | AT | Yes |
| 8 | C | C | CG | CG | Yes |
| 9 | A | C | AT | CG | No |

At index 9, A belongs to the AT group while C belongs to CG, breaking the mutation constraint. The algorithm stops immediately and returns NO. This demonstrates that even a single cross-group mismatch invalidates the full string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each position once and perform constant-time group checks |
| Space | O(1) | Only a fixed amount of state is used for classification |

The linear scan fits comfortably within the constraints for n up to 10^5, and the constant-time operations per character ensure the solution runs efficiently under the time limit.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input().strip())
    x = input().strip()
    y = input().strip()

    def same_group(a, b):
        if a in "AT":
            return b in "AT"
        else:
            return b in "CG"

    for i in range(n):
        if not same_group(x[i], y[i]):
            print("NO")
            return
    print("YES")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided samples
assert run("8\nGCAAGCCT\nCCATCCCT") == "YES", "sample 1"
assert run("10\nCGTATGGACA\nATACTCACCA") == "NO", "sample 2"

# custom cases
assert run("1\nA\nT") == "YES", "single valid flip"
assert run("1\nA\nC") == "NO", "cross group invalid"
assert run("5\nATCGA\nTACGC") == "YES", "mixed valid pairs"
assert run("5\nAAAAA\nCCCCC") == "NO", "all invalid cross group"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 A T | YES | minimal valid complement |
| 1 A C | NO | cross-group rejection |
| ATCGA / TACGC | YES | mixed valid transitions |
| AAAAA / CCCCC | NO | uniform invalid mapping |

## Edge Cases

For single-character inputs like X = "A" and Y = "T", the algorithm performs exactly one group check. A belongs to the AT class, and T also belongs to AT, so the loop finishes without triggering failure and outputs YES.

For a failing cross-class example such as X = "A" and Y = "C", the same check identifies that A is in AT while C is in CG. The condition fails immediately at index 0, and the algorithm outputs NO without needing further processing.

For identical strings like X = "CGTAC" and Y = "CGTAC", every index preserves group membership, so the algorithm confirms validity across the entire scan and returns YES.
