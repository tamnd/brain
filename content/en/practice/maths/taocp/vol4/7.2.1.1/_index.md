---
title: "TAOCP 7.2.1.1: Generating All n-Tuples"
description: "Section 7.2.1.1 exercises: 19/112 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.2.1.1"
section_title: "Generating All n-Tuples"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7020101
draft: false
---

# Section 7.2.1.1. Generating All n-Tuples

Exercises from [TAOCP Volume 4](../) Section 7.2.1.1: 19/112 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) |  [*10*] | simple | verified | 1m05s |
| [2](02.md) |  [*15*] | simple | solved | 1m29s |
| [3](03.md) | &#9654; [*M20*] | math-medium | solved | 3m52s |
| [4](04.md) | &#9654; [*18*] | medium | solved | 1m50s |
| [5](05.md) | &#9654; [*22*] | medium | solved | 1m09s |
| [6](06.md) |  [*M17*] | math-medium | verified | 1m05s |
| [7](07.md) |  [*20*] | medium | solved | 3m10s |
| [8](08.md) |  [*15*] | simple | verified | 1m15s |
| [9](09.md) |  [*16*] | medium | solved | 4m08s |
| [10](10.md) | &#9654; [*M21*] | math-medium | solved | 4m09s |
| 11 |  [*M22*] | math-medium | - | - |
| 12 | &#9654; [*25*] | medium | - | - |
| 13 |  [*21*] | medium | - | - |
| 14 |  [*20*] | medium | - | - |
| 15 | &#9654; [*25*] | medium | - | - |
| 16 |  [*23*] | medium | - | - |
| 17 |  [*20*] | medium | - | - |
| 18 | &#9654; [*20*] | medium | - | - |
| 19 |  [*23*] | medium | - | - |
| 20 |  [*M36*] | math-project | - | - |
| 21 |  [*M30*] | math-hard | - | - |
| 22 | &#9654; [*22*] | medium | - | - |
| 23 |  [*20*] | medium | - | - |
| 24 |  [*M21*] | math-medium | - | - |
| 25 | &#9654; [*M25*] | math-medium | - | - |
| 26 |  [*25*] | medium | - | - |
| 27 | &#9654; [*20*] | medium | - | - |
| 28 |  [*M27*] | math-hard | - | - |
| 29 |  [*M24*] | math-medium | - | - |
| 30 | &#9654; [*M27*] | math-hard | - | - |
| 31 |  [*HM35*] | hm-hard | - | - |
| 32 |  [*M20*] | math-medium | - | - |
| 33 | &#9654; [*M20*] | math-medium | - | - |
| 34 |  [*M21*] | math-medium | - | - |
| 35 |  [*HM23*] | hm-medium | - | - |
| 36 |  [*21*] | medium | - | - |
| 37 |  [*HM23*] | hm-medium | - | - |
| 38 | &#9654; [*M25*] | math-medium | - | - |
| 39 | &#9654; [*HM30*] | hm-hard | - | - |
| 40 | &#9654; [*21*] | medium | - | - |
| 41 |  [*25*] | medium | - | - |
| 42 |  [*35*] | hard | - | - |
| 43 |  [*41*] | project | - | - |
| 44 |  [*M20*] | math-medium | - | - |
| 45 |  [*M40*] | math-project | - | - |
| 46 |  [*M23*] | math-medium | - | - |
| 47 |  [*HM24*] | hm-medium | - | - |
| 48 |  [*HM48*] | hm-research | - | - |
| 49 |  [*20*] | medium | - | - |
| 50 | &#9654; [*21*] | medium | - | - |
| 51 |  [*M24*] | math-medium | - | - |
| 52 |  [*M20*] | math-medium | - | - |
| 53 |  [*M46*] | math-research | - | - |
| 54 |  [*M20*] | math-medium | - | - |
| 55 | &#9654; [*35*] | hard | - | - |
| 56 |  [*M30*] | math-hard | - | - |
| 57 |  [*32*] | hard | - | - |
| 58 | &#9654; [*21*] | medium | - | - |
| 59 |  [*22*] | medium | - | - |
| 60 |  [*20*] | medium | - | - |
| 61 |  [*M30*] | math-hard | - | - |
| 62 |  [*46*] | research | - | - |
| 63 |  [*30*] | hard | - | - |
| 64 | &#9654; [*HM35*] | hm-hard | - | - |
| 65 |  [*30*] | hard | - | - |
| 66 |  [*40*] | project | - | - |
| 67 |  [*20*] | medium | - | - |
| 68 |  [*21*] | medium | - | - |
| 69 | &#9654; [*M25*] | math-medium | - | - |
| 70 |  [*21*] | medium | - | - |
| 71 |  [*M22*] | math-medium | - | - |
| 72 |  [*20*] | medium | - | - |
| 73 | &#9654; [*32*] | hard | - | - |
| 74 |  [*HM25*] | hm-medium | - | - |
| 75 |  [*32*] | hard | - | - |
| 76 |  [*M25*] | math-medium | - | - |
| 77 |  [*21*] | medium | - | - |
| 78 |  [*M26*] | math-hard | - | - |
| 79 | &#9654; [*M22*] | math-medium | - | - |
| 80 |  [*M20*] | math-medium | - | - |
| 81 |  [*M21*] | math-medium | - | - |
| 82 | &#9654; [*M25*] | math-medium | - | - |
| 83 |  [*41*] | project | - | - |
| 84 | &#9654; [*25*] | medium | - | - |
| 85 | &#9654; [*M25*] | math-medium | - | - |
| 86 | &#9654; [*26*] | hard | - | - |
| 87 |  [*27*] | hard | - | - |
| 88 | &#9654; [*25*] | medium | - | - |
| 89 | &#9654; [*25*] | medium | - | - |
| 90 |  [*26*] | hard | - | - |
| 91 | &#9654; [*34*] | hard | - | - |
| 92 |  [*M30*] | math-hard | - | - |
| 93 | &#9654; [*M28*] | math-hard | - | - |
| 94 |  [*22*] | medium | - | - |
| 95 | &#9654; [*M24*] | math-medium | - | - |
| 96 | &#9654; [*M28*] | math-hard | - | - |
| 97 |  [*M29*] | math-hard | - | - |
| 98 |  [*M34*] | math-hard | - | - |
| 99 | &#9654; [*M23*] | math-medium | - | - |
| [100](100.md) |  [*40*] | project | verified | 1m29s |
| [101](101.md) | &#9654; [*M30*] | math-hard | solved | 3m06s |
| [102](102.md) |  [*HM28*] | hm-hard | verified | 1m15s |
| [103](103.md) |  [*M20*] | math-medium | solved | 3m21s |
| [104](104.md) |  [*17*] | medium | solved | 4m01s |
| [105](105.md) |  [*M31*] | math-hard | solved | 5m54s |
| [106](106.md) | &#9654; [*M30*] | math-hard | solved | 5m41s |
| [107](107.md) |  [*HM30*] | hm-hard | solved | 5m47s |
| [108](108.md) |  [*M35*] | math-hard | solved | 4m38s |
| 109 |  [*M22*] | math-medium | - | - |
| 110 |  [*M25*] | math-medium | - | - |
| 111 |  [*20*] | medium | - | - |
| 112 | &#9654; [*25*] | medium | - | - |
