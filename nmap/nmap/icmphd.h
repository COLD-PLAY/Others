#pragma once
#ifndef _ICMPHD_H_
# define _ICMPHD_H_

#include <stdint.h>

# define DEF_DATA_LEN 0x10

#pragma pack (1)

// the struct of ip protocol's header
struct iphd {
	uint8_t m_cVersionAndHeaderLen;
	uint8_t m_cTypeOfService;
	uint16_t m_sTotalLenOfPacket;
	uint16_t m_sSliceinfo;
	uint8_t m_cTTL;
	uint8_t m_cTypeOfProtocol;
	uint16_t m_sCheckSum;
	uint32_t m_uiSourIp;
	uint32_t m_uiDestIp;
};

struct icmphd {
	uint8_t type;
	uint8_t code;
	uint16_t chksum;
	uint16_t identifier;
	uint16_t seqnum;
};

struct icmppk {
	struct icmphd hd;
	uint8_t data[DEF_DATA_LEN];
};

#pragma pack ()  

#   define ICMPHD_SIZE     (sizeof (struct icmphd))  
#   define ICMPPK_SIZE     (sizeof (struct icmppk))  
#   define IPHD_SIZE        (sizeof (struct iphd))  

extern struct icmppk*
create_icmppk(uint8_t, uint8_t, uint16_t);

#endif