#define _WINSOCK_DEPRECATED_NO_WARNINGS 
#include <stdio.h>
#include <stdlib.h>
#include<iostream>
#include<string>
#include<cstring>
#include<WS2tcpip.h>
#include <WinSock2.h>
#include<Windows.h>
#pragma comment(lib, "ws2_32.lib")  //���� ws2_32.dll
using namespace std;

int main()
{
	cout << "-----------�ͻ���-----------" << endl;

	//	1	��ʼ��
	WSADATA wsadata;
	WSAStartup(MAKEWORD(2, 2), &wsadata);


	//	2	�����׽���
	SOCKET clientSocket = {};
	clientSocket = socket(PF_INET, SOCK_STREAM, 0);
	if (SOCKET_ERROR == clientSocket) {
		cout << "�׽��ִ�����ʧ��!" << endl;
	}
	else {
		cout << "�׽��ִ����ɹ�!" << endl;
	}


	//	3	���׽���	ָ���󶨵�IP��ַ�Ͷ˿ں�
	sockaddr_in socketAddr;
	socketAddr.sin_family = PF_INET;
	socketAddr.sin_addr.S_un.S_addr = inet_addr("192.168.199.221");
	socketAddr.sin_port = htons(8081);
	int cRes = connect(clientSocket, (SOCKADDR*)&socketAddr, sizeof(SOCKADDR));
	if (SOCKET_ERROR == cRes) {
		cout << "�ͻ���:\t\t�����������ʧ��....." << endl;
	}
	else {
		cout << "�ͻ���:\t\t����������ӳɹ�....." << endl;
	}


	while (true)
	{
		/*
		string s;
		cout << "���뷢������:\t";
		getline(cin, s);									//������ո�,Ĭ���Ի��з���������,
		send(clientSocket, (char*)s.c_str(), (int)s.length(), 0);

		//��Ϊrecv���ܺ�������������,�������Ǽ����ж�
		//������ȷ�ҲŽ�������,����Ӱ���Ҽ�������
		if (0 == strcmp("��ȡ�汾��Ϣ", s.c_str())) {
			char recvBuf[4024] = {};
			int reLen = recv(clientSocket, recvBuf, 4024, 0);//��������,�ȴ���������
			cout << endl << recvBuf << endl << endl;
		}
		*/


		//	5	��������
		int abc = 0;
		DWORD efg = 0;
		char recvBuf[1024] = {};
		recv(clientSocket, recvBuf, 1024, 0);
		cout << "�ͻ��˽�������	:	" << recvBuf << endl << endl;


		if (0 == strcmp(recvBuf, "2000")) {
			//efg = (DWORD)recvBuf;
			//abc = (int)efg;
			//abc = strtol(recvBuf, NULL, 16); //16����ת������
			//abc = strtoul(recvBuf, NULL, 16); //�޷��ų�����
			abc = static_cast<int>(atof(recvBuf));
			cout << abc << endl << endl;
			Sleep(abc);
			//Sleep(2000);
			//	4	��������
			char sendBuf[1024] = "T";
			send(clientSocket, sendBuf, strlen(sendBuf), 0);

			cout << "�ͻ����˳�" << endl;
			cin.get();
			return 0;
		}
		
	}

	//	6	�ر�socket
	//closesocket(clientSocket);


	//	7	��ֹ
	//WSACleanup();
}


