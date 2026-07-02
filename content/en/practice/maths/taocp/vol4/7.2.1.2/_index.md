---
title: "TAOCP 7.2.1.2: Generating All Permutations"
description: "Section 7.2.1.2 exercises: 46/113 solved."
tags: ["taocp", "mathematics", "algorithms"]
categories: ["mathematics"]
section: "7.2.1.2"
section_title: "Generating All Permutations"
chapter: 7
chapter_title: "Combinatorial Searching"
volume: 4
weight: 7020102
draft: false
---

# Section 7.2.1.2. Generating All Permutations

Exercises from [TAOCP Volume 4](../) Section 7.2.1.2: 46/113 solved.

| # | Rating | Category | Status | Time |
|---|--------|----------|--------|------|
| [1](01.md) | &#9654; [*20*] | medium | solved | 4m41s |
| [2](02.md) |  [*20*] | medium | solved | 5m44s |
| [3](03.md) | &#9654; [*M21*] | math-medium | solved | 1m58s |
| [4](04.md) |  [*M23*] | math-medium | verified | 1m18s |
| [5](05.md) |  [*HM25*] | hm-medium | solved | 3m47s |
| [6](06.md) |  [*HM34*] | hm-hard | solved | 3m52s |
| [7](07.md) |  [*HM35*] | hm-hard | solved | 3m53s |
| [8](08.md) | &#9654; [*21*] | medium | solved | 6m18s |
| [9](09.md) |  [*22*] | medium | solved | 5m47s |
| [10](10.md) |  [*20*] | medium | solved | 6m06s |
| [11](11.md) |  [*M22*] | math-medium | solved | 5m40s |
| [12](12.md) | &#9654; [*M23*] | math-medium | solved | 6m38s |
| [13](13.md) |  [*M21*] | math-medium | solved | 4m54s |
| [14](14.md) |  [*M22*] | math-medium | solved | 6m16s |
| [15](15.md) |  [*M23*] | math-medium | solved | 5m27s |
| [16](16.md) |  [*21*] | medium | solved | 6m15s |
| [17](17.md) | &#9654; [*20*] | medium | solved | 6m23s |
| 18 |  [*21*] | medium | - | - |
| [19](19.md) |  [*25*] | medium | solved | 3m06s |
| 20 | &#9654; [*20*] | medium | - | - |
| [21](21.md) |  [*M21*] | math-medium | solved | 6m05s |
| [22](22.md) |  [*M15*] | math-simple | solved | 3m12s |
| 23 |  [*M20*] | math-medium | - | - |
| [24](24.md) |  [*25*] | medium | solved | 1m16s |
| 25 | &#9654; [*M21*] | math-medium | - | - |
| [26](26.md) |  [*25*] | medium | solved | 4m28s |
| [27](27.md) |  [*30*] | hard | solved | 4m06s |
| [28](28.md) |  [*M25*] | math-medium | solved | 4m27s |
| [29](29.md) | &#9654; [*M25*] | math-medium | solved | 4m16s |
| [30](30.md) |  [*25*] | medium | solved | 4m10s |
| 31 |  [*M22*] | math-medium | - | - |
| [32](32.md) |  [*M25*] | math-medium | solved | 4m11s |
| [33](33.md) |  [*25*] | medium | solved | 4m15s |
| [34](34.md) |  [*M26*] | math-hard | solved | 4m11s |
| [35](35.md) | &#9654; [*M20*] | math-medium | solved | 4m14s |
| [36](36.md) |  [*M23*] | math-medium | solved | 4m26s |
| [37](37.md) | &#9654; [*HM22*] | hm-medium | solved | 4m18s |
| [38](38.md) |  [*HM21*] | hm-medium | solved | 5m45s |
| 39 |  [*16*] | medium | - | - |
| 40 |  [*M23*] | math-medium | - | - |
| 41 | &#9654; [*M33*] | math-hard | - | - |
| 42 |  [*M20*] | math-medium | - | - |
| 43 |  [*M24*] | math-medium | - | - |
| 44 |  [*20*] | medium | - | - |
| 45 |  [*20*] | medium | - | - |
| 46 |  [*20*] | medium | - | - |
| 47 | &#9654; [*M21*] | math-medium | - | - |
| 48 | &#9654; [*M25*] | math-medium | - | - |
| 49 | &#9654; [*28*] | hard | - | - |
| 50 |  [*M15*] | math-simple | - | - |
| 51 |  [*M16*] | math-medium | - | - |
| 52 | &#9654; [*M22*] | math-medium | - | - |
| 53 | &#9654; [*M26*] | math-hard | - | - |
| 54 |  [*20*] | medium | - | - |
| 55 |  [*M27*] | math-hard | - | - |
| 56 |  [*M22*] | math-medium | - | - |
| 57 |  [*HM22*] | hm-medium | - | - |
| 58 |  [*M21*] | math-medium | - | - |
| 59 |  [*M20*] | math-medium | - | - |
| 60 | &#9654; [*21*] | medium | - | - |
| 61 |  [*21*] | medium | - | - |
| 62 | &#9654; [*M23*] | math-medium | - | - |
| 63 |  [*M25*] | math-medium | - | - |
| 64 |  [*23*] | medium | - | - |
| 65 |  [*M25*] | math-medium | - | - |
| 66 |  [*22*] | medium | - | - |
| 67 |  [*26*] | hard | - | - |
| 68 |  [*M30*] | math-hard | - | - |
| 69 | &#9654; [*28*] | hard | - | - |
| 70 | &#9654; [*M33*] | math-hard | - | - |
| 71 |  [*48*] | research | - | - |
| 72 |  [*M21*] | math-medium | - | - |
| 73 | &#9654; [*M30*] | math-hard | - | - |
| 74 |  [*M30*] | math-hard | - | - |
| 75 |  [*M26*] | math-hard | - | - |
| 76 |  [*M31*] | math-hard | - | - |
| 77 | &#9654; [*22*] | medium | - | - |
| 78 |  [*M23*] | math-medium | - | - |
| 79 |  [*20*] | medium | - | - |
| 80 |  [*21*] | medium | - | - |
| 81 | &#9654; [*22*] | medium | - | - |
| 82 |  [*M21*] | math-medium | - | - |
| 83 |  [*22*] | medium | - | - |
| 84 |  [*20*] | medium | - | - |
| 85 | &#9654; [*25*] | medium | - | - |
| 86 |  [*20*] | medium | - | - |
| 87 |  [*20*] | medium | - | - |
| 88 |  [*21*] | medium | - | - |
| 89 | &#9654; [*M30*] | math-hard | - | - |
| 90 |  [*M21*] | math-medium | - | - |
| 91 |  [*HM21*] | hm-medium | - | - |
| 92 |  [*M18*] | math-medium | - | - |
| 93 |  [*35*] | hard | - | - |
| 94 | &#9654; [*25*] | medium | - | - |
| 95 |  [*21*] | medium | - | - |
| 96 |  [*21*] | medium | - | - |
| 97 |  [*21*] | medium | - | - |
| 98 |  [*HM23*] | hm-medium | - | - |
| 99 |  [*M30*] | math-hard | - | - |
| [100](100.md) |  [*21*] | medium | solved | 6m26s |
| [101](101.md) |  [*21*] | medium | solved | 6m13s |
| [102](102.md) |  [*M30*] | math-hard | solved | 4m39s |
| [103](103.md) |  [*M32*] | math-hard | solved | 5m03s |
| [104](104.md) | &#9654; [*M22*] | math-medium | solved | 3m10s |
| [105](105.md) | &#9654; [*26*] | hard | verified | 1m15s |
| [106](106.md) |  [*M40*] | math-project | verified | 3m31s |
| [107](107.md) | &#9654; [*30*] | hard | solved | 6m49s |
| [108](108.md) |  [*M27*] | math-hard | solved | 6m07s |
| [109](109.md) |  [*M47*] | math-research | solved | 6m19s |
| [110](110.md) | &#9654; [*25*] | medium | solved | 1m48s |
| 111 | &#9654; [*M25*] | math-medium | - | - |
| [112](112.md) | &#9654; [*M30*] | math-hard | solved | 6m32s |
| [113](113.md) |  [*HM43*] | hm-project | solved | 6m14s |
