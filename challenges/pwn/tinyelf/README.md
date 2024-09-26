---
title: 我再也不要出有附件的题目了
author: 13m0n4de
difficulty: Easy
category: Pwn
image: ghcr.io/svuctf/svuctf-autumn-2024/tinyelf:latest
port: 70
writeup_author:
tags:
  - Ret2Shellcode
  - TinyELF
reference:
---

# 我再也不要出有附件的题目了

## 题目描述

想象一下，出题人如西西弗一般，日复一日地推动着题目附件这块沉重的巨石。他们编译、打包、上传，眼看着附件目录如山间碎石般杂乱无章。每一次整理都是徒劳，因为新的附件如潮水般涌来，将文件夹再度吞没。

然而，我们应当设想，这位出题人是幸福的。

幸福个头，我再也不要出有附件的题目了，而且根本没人做 PWN 题，人人都爱 Misc，如果放段 Base64 所有 Misc 手都会来做的吧。

```
f0VMRgEBAQAAAAAAAAAAAAIAAwABAAAATIAECCwAAAAAAAAAAAAAADQAIAABAAAAAAAAAACABAgAgAQIewAAAHsAAAAFAAAAABAAAIPsIGoEWDHbQ2hwgAQIWWoLWs2AagNYS4nhaiBazYCDxBj/5HNvIHRpbnkuLi4K
```

## 题目解析

<analysis>
