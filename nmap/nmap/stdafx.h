// stdafx.h : 标准系统包含文件的包含文件，
// 或是经常使用但不常更改的
// 特定于项目的包含文件
//

#pragma once

#include "targetver.h"

#include <stdio.h>
#include <tchar.h>



// TODO: 在此处引用程序需要的其他头文件
#include "icmphd.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <WinSock2.h>
#include <time.h>
#include <Ws2tcpip.h>

#if defined _WIN32 || defined _WIN64
#include <Windows.h>
#endif

#if !defined MAKEWORD  
#define MAKEWORD(low,high) ((WORD)(((BYTE)(low)) | ((WORD)((BYTE)(high))) << 8))  
#endif  

#pragma comment(lib, "ws2_32.lib")

#define ADDR_OFFSET 1
#define println(___STR) printf ("%s\n", ___STR)