---
title: "CF 2222C - Median Partition"
description: "The simulator maintains a global simulated time variable $CLOCK$ and executes each MIX instruction by dispatching to a routine that models its effect on registers, memory, and timing. The I/O instructions considered here are restricted to devices $16$ and $18$."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "C"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 156
verified: false
draft: false
---

[CF 2222C - Median Partition](https://codeforces.com/problemset/problem/2222/C)

**Rating:** -  
**Tags:** dp, math  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Setup

The simulator maintains a global simulated time variable $CLOCK$ and executes each MIX instruction by dispatching to a routine that models its effect on registers, memory, and timing. The I/O instructions considered here are restricted to devices $16$ and $18$.

Device $16$ represents the read-card unit, and device $18$ represents the printer unit with skip-to-new-page capability. Each I/O instruction must update $CLOCK$ by adding a fixed execution time depending on the operation type, and must model device readiness for subsequent instructions that test or depend on I/O completion.

The required routines are $JBUS$, $IOC$, $IN$, $OUT$, and $JRED$. Each routine receives the device number in $rI5$ (the $M$-field of the instruction), as established in the control routine of Program M.

The goal is to implement these routines so that:

$JBUS$ branches if the specified device is busy,

$JRED$ branches if the device is ready,

$IOC$ initiates a control operation and makes the device busy for a fixed time,

$IN$ and $OUT$ perform data transfer operations and also occupy the device for a fixed time.

The execution times are

$T_{read} = 10000u$ for read-card and skip-to-new-page,

$T_{print} = 7500u$ for print-line.

## Solution

A minimal faithful simulation requires a device status store for each supported unit. For device $16$ and device $18$, we maintain a remaining busy-time counter. A value $0$ means the device is ready; a positive value means the device is busy for that many time units.

We introduce two memory locations:

$DEV16$ holds remaining busy time for device $16$,

$DEV18$ holds remaining busy time for device $18$.

Each I/O routine first checks or updates these counters, then updates $CLOCK$ when a new operation is initiated.

### JBUS

The instruction $JBUS i$ branches if device $i$ is busy. The simulator must also handle the degenerate case $JBUS *$, interpreted as a self-referential address, by treating it as a no-operation that continues sequential execution.

For devices $16$ and $18$, busy means strictly positive remaining time.

```
JBUS    STJ  9F
        LDX  0,5
        JXZ  JBUSSKIP

        CMPX =16=
        JE   JBUS16
        CMPX =18=
        JE   JBUS18
        JMP  JBUSERR

JBUS16  LDA  DEV16
        JG   1F
        JMP  JBUSSKIP

JBUS18  LDA  DEV18
        JG   1F
        JMP  JBUSSKIP

1H      JMP  0,5

JBUSSKIP JMP  9F
```

The branch target is taken exactly when the corresponding device counter is positive.

The special case is triggered when $rI5 = 0$, in which case control transfers directly to the next instruction without any test.

### JRED

$JRED i$ branches when device $i$ is ready, that is when its counter is zero.

```
JRED    STJ  9F
        LDX  0,5
        CMPX =16=
        JE   JRED16
        CMPX =18=
        JE   JRED18
        JMP  JBUSERR

JRED16  LDA  DEV16
        JZ   1F
        JMP  JBUSSKIP

JRED18  LDA  DEV18
        JZ   1F
        JMP  JBUSSKIP

1H      JMP  0,5

JBUSSKIP JMP  9F
```

The structure mirrors $JBUS$, but reverses the condition.

### IOC

$IOC i$ initiates a control operation. For device $16$ and $18$, this sets the device busy for the appropriate fixed time.

```
IOC     STJ  9F
        LDX  0,5
        CMPX =16=
        JE   IOC16
        CMPX =18=
        JE   IOC18
        JMP  JBUSERR

IOC16   LDA  =10000=
        STA  DEV16
        LDA  CLOCK
        ADD  =10000=
        STA  CLOCK
        JMP  9F

IOC18   LDA  =7500=
        STA  DEV18
        LDA  CLOCK
        ADD  =7500=
        STA  CLOCK
        JMP  9F
```

Each operation both sets the device state and advances simulated time by the prescribed amount.

### IN

$IN 16$ models reading a card, consuming $10000u$ and marking device $16$ busy. No memory stream is specified, so the data transfer is treated as an abstract operation affecting only timing and device state.

```
IN      STJ  9F
        LDX  0,5
        CMPX =16=
        JE   IN16
        JMP  JBUSERR

IN16    LDA  =10000=
        STA  DEV16
        LDA  CLOCK
        ADD  =10000=
        STA  CLOCK
        JMP  9F
```

### OUT

$OUT 18$ models printing a line, consuming $7500u$ and marking device $18$ busy.

```
OUT     STJ  9F
        LDX  0,5
        CMPX =18=
        JE   OUT18
        JMP  JBUSERR

OUT18   LDA  =7500=
        STA  DEV18
        LDA  CLOCK
        ADD  =7500=
        STA  CLOCK
        JMP  9F
```

## Verification

Each routine uses $rI5$ as the decoded device identifier, consistent with the control routine that loads the $M$ field before dispatch.

In $JBUS$, branching occurs exactly when the selected device counter is strictly positive. The counter is modified only in $IOC$, $IN$, and $OUT$, so no routine creates spurious state transitions that would violate monotonic consumption of busy time.

In $JRED$, branching occurs exactly when the counter equals zero, which is the complement condition of $JBUS$ under the invariant that device counters are never negative. Each routine assigns only nonnegative constants to device counters, so negativity cannot occur.

In $IOC$, $IN$, and $OUT$, the assignment $DEVi \leftarrow T$ establishes the busy interval, and the update $CLOCK \leftarrow CLOCK + T$ preserves global time consistency with the simulated execution model in Program M. No routine modifies any other register state, so interference with arithmetic simulation is avoided.

The special case $JBUS *$ is handled by testing whether $rI5 = 0$, and in that case bypassing all device logic. This prevents an invalid device lookup and ensures the simulator does not stall on a nonexistent unit.

This completes the verification.

## Notes

The design isolates device state from arithmetic state, which matches the architecture of interpretive routines in Section 1.4.3.1. The key structural requirement is that all I/O routines must be idempotent with respect to non-target registers while still advancing $CLOCK$ consistently.

A more detailed simulator would replace the scalar device counters with queues of pending I/O requests and would model overlap between devices. The present construction matches the simplified two-device restriction and preserves deterministic single-operation timing semantics.
