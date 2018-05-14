import os
import socket
import struct
import array
import sys

class Pinger(object):
    def __init__(self,timeout=3):
        self.timeout = timeout
        self.__id = os.getpid()
        self.__data = struct.pack('h',1)#h代表2个字节与头部8个字节组成偶数可进行最短校验

    @property
    def __icmpSocket(self):#返回一个可以利用的icmp原对象,当做属性使用
        icmp = socket.getprotobyname("icmp")#指定服务
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)#socket.SOCK_RAW原生包
        return sock


    def __doCksum(self,packet):#校验和运算
        words = array.array('h',packet)#将包分割成2个字节为一组的网络序列
        sum = 0
        for word in words:
            sum += (word & 0xffff)#每2个字节相加
        sum = (sum >> 16) + (sum & 0xffff)#因为sum有可能溢出16位所以将最高位和低位sum相加重复二遍
        sum += (sum >> 16) # 为什么这里的sum不需要再 & 0xffff 因为这里的sum已经是16位的不会溢出,可以手动测试超过65535的十进制数字就溢出了
        return (~sum) & 0xffff #最后取反返回完成校验

    @property
    def __icmpPacket(self):#icmp包的构造
        header = struct.pack('bbHHh',8,0,0,self.__id,0)
        packet = header + self.__data
        cksum = self.__doCksum(packet)
        header = struct.pack('bbHHh',8,0,cksum,self.__id,0)#将校验带入原有包,这里才组成头部,数据部分只是用来做校验所以返回的时候需要返回头部和数据相加
        return header + self.__data

    def usage(self):
    	print('use python3 ping.py hostname')

    def ping(self,target_host):
        try:
            socket.gethostbyname(target_host)

            sock = self.__icmpSocket
            sock.settimeout(self.timeout)

            packet = self.__icmpPacket

            sock.sendto(packet,(target_host,1))#发送icmp包

            ac_ip = sock.recvfrom(1024)[1][0]
            print('[+] %s active'%(ac_ip))
        except Exception as e:
            sock.close()

def main():
	# s = Pinger()
	# if len(sys.argv) != 2:
	# 	s.usage()
	# 	exit(1)
	# s.ping(sys.argv[1])
    # arp = socket.htons(0x0806)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, arp)
    # sock.bind(('eth0', socket.htons(0x0800)))

if __name__ == '__main__':
	main()