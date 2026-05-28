---
title: "CF 71E - Nuclear Fusion"
description: "We are given a set of atoms with known atomic numbers and a target set of atoms we want to produce using fusion. Each fusion operation combines exactly two atoms into one, and the resulting atom’s atomic number is the sum of the two original numbers. We cannot split atoms."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 2200
weight: 71
solve_time_s: 110
verified: false
draft: false
---

[CF 71E - Nuclear Fusion](https://codeforces.com/problemset/problem/71/E)

**Rating:** 2200  
**Tags:** bitmasks, dp  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of atoms with known atomic numbers and a target set of atoms we want to produce using fusion. Each fusion operation combines exactly two atoms into one, and the resulting atom’s atomic number is the sum of the two original numbers. We cannot split atoms. Every initial atom must be used exactly once to generate the target atoms, so we are essentially partitioning the initial set into subsets that sum to the desired atomic numbers.

The input provides symbols of elements, which we convert to their atomic numbers via a lookup table of the periodic table. The small limits, $n \le 17$, immediately suggest that exponential algorithms that enumerate subsets are feasible. The sum of atomic numbers of initial atoms equals the sum of atomic numbers of target atoms, which guarantees that if a solution exists, it can be expressed purely by rearranging and summing subsets. The key difficulty is ensuring that every atom is used exactly once and that each subset sums exactly to a target atom.

A subtle edge case arises when multiple target atoms have the same value. A naive greedy approach that assigns largest numbers first may pick the wrong elements and leave later subsets unsolvable. For example, if initial numbers are `[1,2,3,4]` and targets are `[5,5]`, picking `[4,1]` for the first 5 leaves `[2,3]` for the second, which works, but a wrong choice like `[3,2]` first leaves `[1,4]` for the second. Exhaustive or DP-based approaches handle this correctly.

## Approaches

A brute-force method would enumerate all partitions of the initial set into $k$ subsets, check if each subset sums to a target, and output the corresponding fusion operations. The number of ways to partition $n$ items into $k$ non-empty sets is given by Stirling numbers of the second kind, which grow very fast, roughly $k^n$. With $n=17$, this is on the order of $17^{17} \approx 10^{20}$, far beyond feasible computation. Even checking all $2^n$ subsets is already expensive if done naively multiple times.

The insight that allows a feasible solution is twofold. First, $n$ is small, so we can represent subsets as bitmasks. Second, we can use dynamic programming on bitmasks to track which subsets of atoms can sum to each target atomic number. This reduces the problem to: for each target atom, find a non-overlapping subset of initial atoms whose sum matches it. Since there are $2^n$ possible subsets, iterating over them is feasible ($2^{17} = 131072$). We can precompute the sum of each subset and then attempt to assign these subsets to targets using memoization to avoid recomputation. Finally, reconstructing the fusion sequence can be done greedily by always fusing the two largest remaining atoms until one remains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all partitions) | O(k^n) | O(k^n) | Too slow |
| Bitmask DP + subset sum | O(k * 2^n * n) | O(2^n * n) | Accepted |

## Algorithm Walkthrough

1. Convert element symbols to atomic numbers. Store both the symbol and number for reconstructing the solution.
2. Represent each subset of the initial set as a bitmask. Precompute the sum of numbers in each subset. This allows quick lookup of which subsets can produce each target atom.
3. Use recursive DP to attempt to assign subsets to target atoms. At each step, pick a target atom and try every subset whose sum matches its atomic number and whose bits are not used yet. Mark the subset as used and recurse on the remaining targets. If all targets are matched, we have a valid assignment.
4. If no subset matches a target or remaining targets cannot be completed, backtrack. Memoization can be applied on the mask of unused atoms and the index of the target atom to prevent recalculating the same subproblem.
5. Once a valid assignment of subsets to targets is found, reconstruct the fusion sequences. For each subset, repeatedly fuse the two largest numbers until one atom remains. Keep track of the original atom symbols to print the sequence as `A+B+...->Target`.
6. Output "YES" and the k fusion sequences. If no assignment is found, output "NO".

Why it works: The DP ensures every target gets a disjoint subset of atoms summing correctly, and the fusion reconstruction always reduces each subset to a single atom using legal pairwise fusions. The invariants are that every initial atom is used once and the sum matches the target.

## Python Solution

```python
import sys
input = sys.stdin.readline

# map of element symbols to atomic numbers
periodic_table = {
    "H":1,"He":2,"Li":3,"Be":4,"B":5,"C":6,"N":7,"O":8,"F":9,"Ne":10,
    "Na":11,"Mg":12,"Al":13,"Si":14,"P":15,"S":16,"Cl":17,"Ar":18,"K":19,"Ca":20,
    "Sc":21,"Ti":22,"V":23,"Cr":24,"Mn":25,"Fe":26,"Co":27,"Ni":28,"Cu":29,"Zn":30,
    "Ga":31,"Ge":32,"As":33,"Se":34,"Br":35,"Kr":36,"Rb":37,"Sr":38,"Y":39,"Zr":40,
    "Nb":41,"Mo":42,"Tc":43,"Ru":44,"Rh":45,"Pd":46,"Ag":47,"Cd":48,"In":49,"Sn":50,
    "Sb":51,"Te":52,"I":53,"Xe":54,"Cs":55,"Ba":56,"La":57,"Ce":58,"Pr":59,"Nd":60,
    "Pm":61,"Sm":62,"Eu":63,"Gd":64,"Tb":65,"Dy":66,"Ho":67,"Er":68,"Tm":69,"Yb":70,
    "Lu":71,"Hf":72,"Ta":73,"W":74,"Re":75,"Os":76,"Ir":77,"Pt":78,"Au":79,"Hg":80,
    "Tl":81,"Pb":82,"Bi":83,"Po":84,"At":85,"Rn":86,"Fr":87,"Ra":88,"Ac":89,"Th":90,
    "Pa":91,"U":92,"Np":93,"Pu":94,"Am":95,"Cm":96,"Bk":97,"Cf":98,"Es":99,"Fm":100
}

n, k = map(int, input().split())
initial_symbols = input().split()
target_symbols = input().split()

initial_numbers = [periodic_table[s] for s in initial_symbols]
target_numbers = [periodic_table[s] for s in target_symbols]

from itertools import combinations

# precompute subset sums
subset_sum = {}
for mask in range(1, 1<<n):
    total = 0
    for i in range(n):
        if mask & (1<<i):
            total += initial_numbers[i]
    subset_sum[mask] = total

memo = {}
assignment = [0]*k

def solve(mask, idx):
    if idx == k:
        return mask == 0
    key = (mask, idx)
    if key in memo:
        return False
    t = target_numbers[idx]
    submask = mask
    while submask:
        if subset_sum[submask] == t:
            if solve(mask ^ submask, idx+1):
                assignment[idx] = submask
                return True
        submask = (submask - 1) & mask
    memo[key] = False
    return False

if not solve((1<<n)-1, 0):
    print("NO")
    sys.exit(0)

print("YES")

# reconstruct fusion sequence
for idx in range(k):
    mask = assignment[idx]
    elems = []
    for i in range(n):
        if mask & (1<<i):
            elems.append((initial_numbers[i], initial_symbols[i]))
    elems.sort(reverse=True)
    sequence = []
    while len(elems) > 1:
        a = elems.pop(0)
        b = elems.pop(0)
        elems.append((a[0]+b[0], f"{a[1]}+{b[1]}"))
        elems.sort(reverse=True)
    print(f"{elems[0][1]}->{target_symbols[idx]}")
```

Each part corresponds directly to algorithm steps: mapping symbols to numbers, precomputing subset sums, using DP to assign subsets, and then greedily fusing largest atoms first to reconstruct the target. Careful bitmask manipulation prevents double counting atoms, and sorting ensures proper pairing.

## Worked Examples

**Sample 1**

| Step | Mask | Target idx | Chosen subset | Remaining mask |
| --- | --- | --- | --- | --- |
| 1 | 1111111111 | 0 (Sn) | Mn+C+K | remaining bits |
| 2 | ... | 1 (Pt) | Co+Zn+Sc | ... |
| 3 | ... | 2 (Y) | Li+Mg+P+F | 0 |
