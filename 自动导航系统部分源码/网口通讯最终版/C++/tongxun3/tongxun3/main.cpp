#define _WINSOCK_DEPRECATED_NO_WARNINGS 
#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include<string>
#include<cstring>
#include<WS2tcpip.h>
#include <WinSock2.h>
#include<Windows.h>
#pragma comment(lib, "ws2_32.lib")  //加载 ws2_32.dll
using namespace std;

int main()
{
	cout << "-----------客户端-----------" << endl;

	//	1	初始化
	WSADATA wsadata;
	WSAStartup(MAKEWORD(2, 2), &wsadata);


	//	2	创建套接字
	SOCKET clientSocket = {};
	clientSocket = socket(PF_INET, SOCK_STREAM, 0);
	if (SOCKET_ERROR == clientSocket) {
		cout << "套接字闯创建失败!" << endl;
	}
	else {
		cout << "套接字创建成功!" << endl;
	}


	//	3	绑定套接字	指定绑定的IP地址和端口号
	sockaddr_in socketAddr;
	socketAddr.sin_family = PF_INET;
	socketAddr.sin_addr.S_un.S_addr = inet_addr("192.168.199.221");
	socketAddr.sin_port = htons(8081);
	int cRes = connect(clientSocket, (SOCKADDR*)&socketAddr, sizeof(SOCKADDR));
	if (SOCKET_ERROR == cRes) {
		cout << "客户端:\t\t与服务器连接失败....." << endl;
	}
	else {
		cout << "客户端:\t\t与服务器连接成功....." << endl;
	}


	while (true)
	{
		/*
		string s;
		cout << "输入发送数据:\t";
		getline(cin, s);									//可输入空格,默认以换行符结束输入,
		send(clientSocket, (char*)s.c_str(), (int)s.length(), 0);

		//因为recv接受函数是阻塞函数,所以我们加以判断
		//请求正确我才接收数据,否则不影响我继续请求
		if (0 == strcmp("获取版本信息", s.c_str())) {
			char recvBuf[4024] = {};
			int reLen = recv(clientSocket, recvBuf, 4024, 0);//阻塞函数,等待接受数据
			cout << endl << recvBuf << endl << endl;
		}
		*/


		//	5	接受数据
		int abc = 0;
		DWORD efg = 0;
		char recvBuf[1024] = {};
		recv(clientSocket, recvBuf, 1024, 0);
		cout << "客户端接收数据	:	" << recvBuf << endl << endl;


		if (0 == strcmp(recvBuf, "2000")) {
			//efg = (DWORD)recvBuf;
			//abc = (int)efg;
			//abc = strtol(recvBuf, NULL, 16); //16进制转整型数
			//abc = strtoul(recvBuf, NULL, 16); //无符号长整数
			abc = static_cast<int>(atof(recvBuf));
			cout << abc << endl << endl;
			Sleep(abc);
			//Sleep(2000);
			//	4	发送请求
			char sendBuf[1024] = "T";
			send(clientSocket, sendBuf, strlen(sendBuf), 0);

			cout << "客户端退出" << endl;
			cin.get();
			return 0;
		}
		
	}

	//	6	关闭socket
	//closesocket(clientSocket);


	//	7	终止
	//WSACleanup();
}


