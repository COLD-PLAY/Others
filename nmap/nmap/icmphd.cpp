#include "stdafx.h"

static uint16_t
icmp_cal_cksum(uint8_t*, int);

struct icmppk*
create_icmppk(uint8_t _type, uint8_t _code, uint16_t _seq) {
	struct icmppk* pk = (struct icmppk*) malloc (ICMPPK_SIZE);
	if (pk != NULL) {
		int i = 0;
		memset(pk, 0, ICMPPK_SIZE);
		pk->hd.type = _type;
		pk->hd.code = _code;
		pk->hd.identifier = 1;
		//
		((uint8_t*)(&(pk->hd.seqnum)))[0] = (uint8_t)((_seq & 0xff00) >> 8);
		((uint8_t*)(&(pk->hd.seqnum)))[1] = _seq & 0x00ff;
		for (; i < DEF_DATA_LEN; i++)
			pk->data[i] = i + '0';
		pk->hd.chksum = icmp_cal_cksum((uint8_t*)pk, ICMPPK_SIZE);
	}
	return pk;
}

static uint16_t
icmp_cal_cksum(uint8_t* _data, int _data_len) {
	int sum = 0;
	int odd = _data_len & 0x01;
	uint16_t* value = (uint16_t*)_data;
	while (_data_len & 0xfffe) {
		sum += *(uint16_t*)_data;
		_data += 2;
		_data_len -= 2;
	}
	if (odd) {
		uint16_t tmp = ((*_data) << 8) & 0xff00;
		sum += tmp;
	}
	sum = (sum >> 16) + (sum & 0xffff);
	sum += (sum >> 16);
	return ~sum;
}