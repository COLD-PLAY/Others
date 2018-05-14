from scapy.all import *
import os, struct
import socket, scapy
import array, platform

class Nmap(object):
		def __init__(self, timeout=3):
				self.timout=timeout
				self.__id = os.getpid()
				self.__data = struct.pack('h', 1)
				self.__srcmac = '80:A5:89:29:B3:91'
				self.__dstmac = 'f4:83:cd:fc:e0:16' # netgate mac
				self.__srcip = '192.168.1.120'
				self.__dstip = '192.168.1.1'		# netgate ip
				self.__system = platform.system()

		def __doCksum(self,packet):#校验和运算
				words = array.array('h',packet)#将包分割成2个字节为一组的网络序列
				sum = 0
				for word in words:
					sum += (word & 0xffff)#每2个字节相加
				sum = (sum >> 16) + (sum & 0xffff)#因为sum有可能溢出16位所以将最高位和低位sum相加重复二遍
				sum += (sum >> 16) # 为什么这里的sum不需要再 & 0xffff 因为这里的sum已经是16位的不会溢出,可以手动测试超过65535的十进制数字就溢出了
				return (~sum) & 0xffff #最后取反返回完成校验

		def __getMac(self, mac):
				return binascii.a2b_hex(mac.replace(':', ''))

		def __getIp(self, ip):
				i = list(map(int,ip.strip('.')))
				ipi = i[0]*256*256*256+i[1]*256*256+i[2]*256+i[3]
				iph = hex(ipi)
				return binascii.a2b_hex(iph[2:])

		@property
		def __icmpPacket(self):
				header = struct.pack('bbHHh',8,0,0,self.__id,0)
				packet = header + self.__data
				cksum = self.__doCksum(packet)
				header = struct.pack('bbHHh',8,0,cksum,self.__id,0)#将校验带入原有包,这里才组成头部,数据部分只是用来做校验所以返回的时候需要返回头部和数据相加
				return header + self.__data

		@property
		def __icmpSocket(self):
				icmp = socket.getprotobyname('icmp')
				sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
				return sock

		@property
		def __arpPacket(self, others=None):
				if others is not None:
						sha = self.__getMac(others[0])
						spa = self.__getIp(others[1])
						tha = self.__getMac(others[2])
						tpa = self.__getIp(others[3])
				else:
						sha = self.__getMac(self.__srcmac)
						spa = self.__getIp(self.__srcip)
						tha = self.__getMac(self.__dstmac)
						tpa = self.__getIp(self.__dstip)
						
				# ethernet header
				arp = struct.pack('H', 0x0806)
				header = tha + sha + arp
				
				# arp packet
				hrd = struct.pack('h', 0x0001)
				pro = struct.pack('h', 0x0801)
				hln = struct.pack('b', 0x06)
				pln = struct.pack('b', 0x04)
				op = struct.pack('h', 0x0001)
				# sha = sha
				# spa = spa
				# tha = tha
				# tpa = tpa
				arpPkt = hrd+pro+hln+pln+op+sha+spa+tha+tpa

				return header + arpPkt
			
		@property
		def __arpSocket(self):
				arp = socket.htons(0x0806)
				sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, arp)
				sock.bind(('eth0', socket.htons(0x0800)))
				return sock

def main():
		nmap = Nmap()

if __name__ == '__main__':
		main()
	