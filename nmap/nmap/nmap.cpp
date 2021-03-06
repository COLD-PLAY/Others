// nmap.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#pragma warning(disable:4996)
uint16_t sequence = 0;
time_t start = 0, end = 0;
uint32_t ip_num = 0;
char *ip_char = NULL;
struct icmppk* send_data;
uint8_t* rcv_data;
SOCKET sockfd = INVALID_SOCKET;
struct sockaddr_in local;

static struct icmppk*
request_echo_icmp(/*const char* */);

static void
dispose_resources();

static void
rcv_parse_reply_echo_icmp();

int
ipstr_to_numeric(const char*, int*);

static void
usage_disp() {
	println("Usage: ping <ip_address>");
}

static struct icmppk*
request_echo_icmp() {
	uint16_t ip_numeric = 0;
	struct icmppk* hd = NULL;

	hd = create_icmppk(8, 0, ++sequence);
	return hd;
}

static void
rcv_parse_reply_echo_icmp() {
	int rcv_len = 0;
	int frm_len = ICMPPK_SIZE;
	while (1) {
		rcv_len = recvfrom(sockfd, (char*)rcv_data, 0x100, 0,
			(struct sockaddr*)&local, &frm_len);
		if (rcv_len > 0) {
			struct icmppk* ptr = (struct icmppk*)(((uint8_t*)rcv_data) + IPHD_SIZE);
			if (((struct iphd*)rcv_data)->m_uiSourIp == ip_num &&
				((struct iphd*)rcv_data)->m_cTypeOfProtocol == IPPROTO_ICMP) {
				end = time(NULL);
				printf("Reply from %s: bytes = %d, time = %f nm, req = %d, TTL = %d\n",
					ip_char,
					DEF_DATA_LEN,
					difftime(end, start),
					ntohs(ptr->hd.seqnum),
					((struct iphd*)rcv_data)->m_cTTL);
				start = end = 0;
#ifdef _MSC_VER
				Sleep(1000);
#elif __GNUC__
				sleep(1);
#endif
				break;
			}
			else { continue; }
		}
		else { continue; }
	}
}

static void
display_frame(struct icmppk* _pk, int _len) {
	int i = 0;
	for (; i < _len; i++) { printf("0x%02x ", ((uint8_t*)_pk)[i]); }
}

int
ipstr_to_numeric(const char* _str, int* _addr) {
	const char* index;
	unsigned char* addr = (unsigned char*)_addr;
	int isnumeric = 1;
	int i = 3;
	*_addr = 0;

	index = _str;
	while ((*index) && (isnumeric)) {
		if (isdigit((unsigned char)*index)) addr[i] = addr[i] * 10 + (*index - '0');
		else if (*index == '.') {
			i--;
			if (i == -1) isnumeric = 0;
		}
		else isnumeric = 0;
		index++;
	}
	
	if (isnumeric && i) return -1; //error
	if (isnumeric) return 0;	// successful
}

int
main(int argc, char *argv[])
{
	WSADATA wsaData;
	struct sockaddr_in hints;
	int remte_addr = 0;
	int timeout = 1000;
	int res;

	//if (argc < 2) {
	//	usage_disp();
	//	return 0;
	//}
	
	res = WSAStartup(MAKEWORD(2, 2), &wsaData);

	if (res != 0) {
		printf("WSAStartup fault, error: %d\n", res);
		return 1;
	}

	rcv_data = (uint8_t*) malloc (0x100);

	memset(&hints, 0, sizeof(struct sockaddr_in));
	memset(&local, 0, sizeof(struct sockaddr_in));
	hints.sin_family = AF_INET;
	//hints.sin_addr.s_addr = ip_num
	//	= inet_addr(ip_char = argv[ADDR_OFFSET]);
	hints.sin_addr.s_addr = ip_num
		= inet_addr(ip_char = "220.181.57.216");
	local.sin_family = AF_INET;
	local.sin_addr.s_addr = inet_addr("127.0.0.1");

	sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);

	if (sockfd == INVALID_SOCKET) {
		printf("Socket fault, error: %ld\n", WSAGetLastError());
		WSACleanup();
		dispose_resources();
		return 1;
	}

	printf("Ping host %s\n", ip_char);

	while (1) {
		send_data = request_echo_icmp();
		start = time(NULL);
		// send data to server
		//res = sendto(sockfd, (const char*)send_data, ICMPPK_SIZE, 0,
		//	(struct sockaddr*)&hints, sizeof(hints));
		res = sendto(sockfd, (const char*)send_data, ICMPPK_SIZE, 0,
			(struct sockaddr*)&hints, sizeof(hints));
		if (res == SOCKET_ERROR) {
			printf("Send Error: %d\n", WSAGetLastError());
			closesocket(sockfd);
			WSACleanup();
			dispose_resources();
			return 1;
		}

		// receive from remote
		rcv_parse_reply_echo_icmp();
	}
	
	// shutdown(sockfd, SD_BOTH);
	closesocket(sockfd);
	WSACleanup();
	dispose_resources();

    return 0;
}

static void
dispose_resources() {
	rcv_data && (free(rcv_data), (rcv_data = NULL));
	send_data && (free(send_data), (send_data = NULL));
}