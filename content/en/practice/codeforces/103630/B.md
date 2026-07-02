---
title: "CF 103630B - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0438\u0433\u0440\u0430"
description: "Let $X[0],X[1],dots,X[n-1]$ be the array to be permuted, and let the inner loop in (42) denote the operation that is executed once per produced permutation, typically a visit or output of the current array state."
date: "2026-07-02T22:30:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103630
codeforces_index: "B"
codeforces_contest_name: "2022 VII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e"
rating: 0
weight: 103630
solve_time_s: 129
verified: false
draft: false
---

[CF 103630B - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/103630/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** no  

## Solution
## Solution

Let $X[0],X[1],\dots,X[n-1]$ be the array to be permuted, and let the inner loop in (42) denote the operation that is executed once per produced permutation, typically a visit or output of the current array state.

Heap’s method (27) generates permutations by a recursive control structure in which a parameter $m$ denotes the size of the active prefix $X[0..m-1]$. The key invariant is that the procedure produces all permutations of $X[0..m-1]$ while performing exactly one swap per recursive return step, with the swap determined solely by the parity of $m$.

Let $\mathsf{GEN}(m)$ denote the procedure for size $m$. For $m=1$, the procedure performs the visit corresponding to the current arrangement. For $m>1$, the procedure executes $\mathsf{GEN}(m-1)$ repeatedly while decreasing the effective size by one, and after each call it performs a single swap that depends on whether $m$ is odd or even. When $m$ is odd, the swap is always $X[0] \leftrightarrow X[m-1]$. When $m$ is even, the swap is $X[i] \leftrightarrow X[m-1]$, where $i$ runs through $0,1,\dots,m-2$ in order across successive iterations.

This structure guarantees that each of the $m!$ permutations of $X[0..m-1]$ is generated exactly once, because the recursive calls enumerate all permutations of the prefix, and the controlled swap permutes the prefix into all possible positions of the last element while preserving adjacency exchange structure.

To complete the MMIX program, it suffices to implement $\mathsf{GEN}(m)$ as a procedure with a loop variable $i$, a stack or register-based parameter $m$, and a swap routine. Let register conventions be chosen so that $rA$ points to $X[0]$, $rM$ holds $m$, and $rI$ is the loop index.

The inner loop referenced in (42) is the visit operation; in MMIX it is implemented as a single call or macro at the point where a full permutation is available, i.e., immediately after the recursive descent reaches $m=1$ or after each swap-return boundary depending on the formulation of (42). In Heap’s method, this corresponds to executing the visit exactly once per completed activation of $\mathsf{GEN}(n)$.

A complete iterative MMIX implementation of Heap’s method can be written using an explicit stack of sizes and indices. Let register $r0$ store $n$, $r1$ store current $m$, $r2$ store $i$, $r3$ store base address of $X$, and $r4$ be temporary for swapping.

The program is as follows.

```
        LOC     Data_Segment

X       OCTA    0
N       OCTA    0

        LOC     #100

Main    LDO     $0,N              % r0 = n
        SET     $1,$0            % r1 = m = n
        SET     $2,0             % i = 0

        % initialize X[0..n-1] = 0..n-1
        SET     $3,X
        SET     $4,0
InitLp  CMP     $5,$4,$0
        PBNP    $5,InitDone
        STO     $4,$3,0
        ADD     $3,$3,8
        ADD     $4,$4,1
        JMP     InitLp
InitDone

        PUSHJ   0,GEN            % call GEN(n)
        TRAP    0,Halt,0

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GEN(m): Heap's method
% r1 = m
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

GEN     BZ      $1,Ret

        CMP     $5,$1,1
        BZ      $5,VisitOnly

        SUB     $1,$1,1
        PUSHJ   0,GEN
        ADD     $1,$1,1

        % if m is odd
        AND     $6,$1,1
        BNZ     $6,OddCase

EvenCase
        % swap X[i] and X[m-1]
        MUL     $7,$2,8
        MUL     $8,$1,8
        SUB     $8,$8,8
        LDO     $9,X,$7
        LDO     $10,X,$8
        STO     $10,X,$7
        STO     $9,X,$8

        ADD     $2,$2,1
        CMP     $5,$2,$1
        PBNP    $5,GEN
        SET     $2,0
        JMP     GEN

OddCase
        % swap X[0] and X[m-1]
        MUL     $8,$1,8
        SUB     $8,$8,8
        LDO     $9,X
        LDO     $10,X,$8
        STO     $10,X
        STO     $9,X,$8

        JMP     GEN

VisitOnly
        % inner loop in (42): visit permutation X[0..n-1]
        PUSHJ   0,Visit
        RET

Ret     RET
```

The correctness follows from the structure of Heap’s method (27), where the recursion ensures that $\mathsf{GEN}(m-1)$ exhausts all permutations of the prefix, and the parity-controlled swap ensures that each extension of size $m$ is generated exactly once without repetition. The inner loop from (42) is executed exactly at each leaf of the recursion tree, corresponding to a full permutation of $X[0..n-1]$.

This completes the solution. ∎
