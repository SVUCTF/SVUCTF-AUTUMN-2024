# SVUCTF-AUTUMN-2024

## 题目

### Crypto

|                       题目描述与题解                       |   难度   |                       附件                        |                     源代码                      | 镜像  |              标签               | 出题人  |
| :-------------------------------------------------: | :----: | :---------------------------------------------: | :------------------------------------------: | :-: | :---------------------------: | :--: |
| [张学长的神秘字符串](challenges/crypto/ascii_sum/README.md)  |  Easy  |  [附件](challenges/crypto/ascii_sum/attachments)  |                      -                       |  -  |             ASCII             | Only |
| [月黑风高✌](challenges/crypto/affine_cipher/README.md)  | Normal |                        -                        | [源代码](challenges/crypto/affine_cipher/build) |  -  | Affine Cipher, Custom Charset | Only |
| [LAST-RSA](challenges/crypto/rsa_small_n/README.md) | Medium | [附件](challenges/crypto/rsa_small_n/attachments) |                      -                       |  -  |       RSA, Brute Force        | Only |

### Misc

|                        题目描述与题解                         |   难度   |                        附件                         |                     源代码                      | 镜像  |                       标签                        | 出题人  |
| :----------------------------------------------------: | :----: | :-----------------------------------------------: | :------------------------------------------: | :-: | :---------------------------------------------: | :--: |
|  [给flag小姐的一封情书](challenges/misc/null_byte/README.md)   |  Easy  |    [附件](challenges/misc/null_byte/attachments)    |                      -                       |  -  |            Steganography, Null Bytes            | ksks |
|  [给不来方夕莉小姐的照片](challenges/misc/rar_passwd/README.md)   | Normal |   [附件](challenges/misc/rar_passwd/attachments)    |                      -                       |  -  | RAR Password Crack, Base64, Reverse Image Bytes | ksks |
| [写给猫娘的一封情书](challenges/misc/russian_usb_hid/README.md) | Medium | [附件](challenges/misc/russian_usb_hid/attachments) | [源代码](challenges/misc/russian_usb_hid/build) |  -  |         Russian Encode, USB HID Packet          | ksks |

### Pwn

|                      题目描述与题解                      |   难度   |                    附件                    |                 源代码                 |                                                      镜像                                                      |            标签             |   出题人    |
| :-----------------------------------------------: | :----: | :--------------------------------------: | :---------------------------------: | :----------------------------------------------------------------------------------------------------------: | :-----------------------: | :------: |
| [我再也不要出有附件的题目了](challenges/pwn/tinyelf/README.md) |  Easy  | [附件](challenges/pwn/tinyelf/attachments) | [源代码](challenges/pwn/tinyelf/build) | [ghcr.io/svuctf/svuctf-autumn-2024/tinyelf:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/tinyelf:latest) |  Ret2Shellcode, TinyELF   | 13m0n4de |
|     [Canary](challenges/pwn/canary/README.md)     | Normal | [附件](challenges/pwn/canary/attachments)  | [源代码](challenges/pwn/canary/build)  |  [ghcr.io/svuctf/svuctf-autumn-2024/canary:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/canary:latest)  |     Leak Canary, ROP      | 13m0n4de |
|       [Note](challenges/pwn/note/README.md)       | Medium |  [附件](challenges/pwn/note/attachments)   |  [源代码](challenges/pwn/note/build)   |    [ghcr.io/svuctf/svuctf-autumn-2024/note:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/note:latest)    | UAF, Double Free, Fastbin | 13m0n4de |

### Reverse

|                      题目描述与题解                       |   难度   |                       附件                       |                    源代码                    | 镜像  |     标签     |   出题人    |
| :------------------------------------------------: | :----: | :--------------------------------------------: | :---------------------------------------: | :-: | :--------: | :------: |
|     [简单混个淆](challenges/reverse/smc/README.md)      |  Easy  |    [附件](challenges/reverse/smc/attachments)    |    [源代码](challenges/reverse/smc/build)    |  -  |    SMC     | 13m0n4de |
|   [奇怪的电路](challenges/reverse/pyc_tea/README.md)    | Normal |  [附件](challenges/reverse/pyc_tea/attachments)  |  [源代码](challenges/reverse/pyc_tea/build)  |  -  |  PYC, TEA  | 13m0n4de |
| [SimpleVM](challenges/reverse/simple_vm/README.md) | Medium | [附件](challenges/reverse/simple_vm/attachments) | [源代码](challenges/reverse/simple_vm/build) |  -  | VM, OpCode | 13m0n4de |

### Web

|                             题目描述与题解                              |   难度   |                             附件                              |                          源代码                           |                                                                         镜像                                                                         |                       标签                        |   出题人    |
| :--------------------------------------------------------------: | :----: | :---------------------------------------------------------: | :----------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------: | :------: |
|        [又是文件上传](challenges/web/imagecreatefrom/README.md)        |  Easy  |                              -                              |      [源代码](challenges/web/imagecreatefrom/build)       |            [ghcr.io/svuctf/svuctf-autumn-2024/imagecreatefrom:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/imagecreatefrom:latest)            | PHP, File Upload, Image Rerendering, GD Library |   Only   |
|              [gRPC](challenges/web/grpc/README.md)               | Normal |                              -                              |            [源代码](challenges/web/grpc/build)            |                       [ghcr.io/svuctf/svuctf-autumn-2024/grpc:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/grpc:latest)                       | gRPC, Service Discovery, API Version Downgrade  | 13m0n4de |
| [拼尽全力也无法越权](challenges/web/python_prototype_pollution/README.md) | Medium | [附件](challenges/web/python_prototype_pollution/attachments) | [源代码](challenges/web/python_prototype_pollution/build) | [ghcr.io/svuctf/svuctf-autumn-2024/python_prototype_pollution:latest](https://ghcr.io/svuctf/svuctf-autumn-2024/python_prototype_pollution:latest) |        Python, Prototype Pollution, JWT         | 13m0n4de |
