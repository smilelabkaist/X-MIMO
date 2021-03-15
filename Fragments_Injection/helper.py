#
#=====================================================================================
#       Filename:  helper.py
# 
#    Description:  generate the correct payloads for embedding ZigBee signal (emulation) in the WiFi fragments.
#        Version:  1.0
#
#         Author:  Shuai Wang
#         Email :  <shine.hitcs@gmail.com>
#   Organization:  Smart and Mobile Systems (Smile) Lab @ KAIST 
#				   https://sites.google.com/view/smilelab/
#
#   Copyright (c)  Smart and Mobile Systems (Smile) Lab @ KAIST 
# =====================================================================================
#

import copy



# Even though the scrambler seed changes for each WiFi packet (fragment), the first WiFi fragment always emulates the ZigBee signal successfully.  
# There are two parameters you need to specify in this program:
# 1: scrambler seed, which is shown in the "injector" program. You need to set this parameter on line 16.
# 2: The MAC address of the WiFi receiver (X-MIMO). You need to set this parameter on line 167.


# The AR9334 WNIC on TP-link WDR 4300 wireless router always uses seed 71 as the initial seed.
# Put the scrambler seed (decimal) you see on the injector program here.

scrambler_seed=71



# generate all 127 seeds in a list :
seed_list=[]

state=[0,0,0,0,0,0,0]

for i in range(1,128):
	state=[0,0,0,0,0,0,0]
	ss=bin(i)[2:]

	ss_start_index=len(state)-len(ss)
	for j in range(len(ss)):
		state[ss_start_index+j]=int(ss[j])

	state.reverse()
	seed_list.append(state)


start_index=  (72- scrambler_seed-1)%127


# generate the right seed scquence for all the following packets:

rightseed=[]

for seq_index in range(127):
	ss=seed_list[(start_index+seq_index)%127]

	rightseed.append(ss)




# because each wifi packet contains two fragments and the scrambler seed is different for each fragment, 
# we repeate 63 times to generate 63 WiFi packets for transmitting 126 fragments. 

for seq_index in range(63):


	sourceFile = open('./encoded_bits/gen_bits_'+str(0)+'.txt', "r")
	
	# read the encoded bits
	SourceBits = []
	for line in sourceFile.readlines():
		strline = line.split(',')
		for i in range(len(strline)):
			SourceBits.append(int(strline[i]))
	sourceFile.close()

	# the first WiFi symbol contains scrambler seed, packet type, transmitter's and receiver's MAC address.
	# so, we should process the first symbol differently and start emulating ZigBee after this

	# skip the first 16 bits (which represents scrambler seed) in the payload.
	M=16
	ss_bits = [0 for i in range(M)]



	state=copy.deepcopy(rightseed[seq_index*2])
	
	out_bits = [0 for i in range(M)]
	for i in range(M):
		feedback = state[3] ^ state[6]
		out_bits[i] = ss_bits[i] ^ feedback
		state[1:7] = state[0:6]
		state[0] = feedback


	first_symbol_input=copy.deepcopy(out_bits)

	for i in range(52*4*1/2-M):
		first_symbol_input.append(0)


	# M becomes the size (bits) of one WiFi SymBol. For example,  we apply QAM 16 with encoding rate of 1/2 to emulate ZigBee signals in the first fragment. Then M = 4 * 1/2 * 52, where 52 represents the number of data subcarriers in one 802.11n symbol.
	M=52*4*1/2

	
	first_symbol_output=[]
	state=copy.deepcopy(rightseed[seq_index*2])

	out_bits = [0 for i in range(M)]
	for i in range(M):
		feedback = state[3] ^ state[6]
		first_symbol_output.append( first_symbol_input[i] ^ feedback )
		state[1:7] = state[0:6]
		state[0] = feedback


	first_symbol_pkt_input=first_symbol_output[16:]

	first_symbol_matlab_input=first_symbol_output

	# the first symbol is done. Now proceed with the rest symbols (ZigBee emulaton)
	other_symbol_input= [0 for i in range(len(SourceBits))]
	for i in range(len(SourceBits)):
		feedback = state[3] ^ state[6]
		other_symbol_input[i] = SourceBits[i] ^ feedback
		state[1:7] = state[0:6]
		state[0] = feedback



	all_bits=copy.deepcopy(first_symbol_pkt_input)+other_symbol_input

	for i in range(len(first_symbol_pkt_input)-10):
		all_bits[i]=first_symbol_pkt_input[i]


	# sometimes the length of the encoded bits is not the multiplier of one byte. Then, we just append 0s.

	compensation_len=len(all_bits)/8
	compensation_len=len(all_bits)-compensation_len*8


	for i in range(compensation_len):
		all_bits.append(0)

	# "packets" stores the payload in Bytes.
	packets=[]
	for i in range(len(all_bits)/8):


		temp=all_bits[i*8:(i+1)*8]
		###    Bit Numbering
		temp.reverse()
		temp_str=""
		for j in range(8):
			temp_str+=str(temp[j])

		packets.append(int(temp_str,2))


	# The first 4 elements specifies the type of the packet (e.g. Beacon). 
	# The subsequent 6 elements represent the MAC address of the receiver (X-MIMO).
	# For example, the following MAC address is A0:F3:B1:FF:42:59. 
	# You should change the MAC address to the receiver's address. No matter the receivr is a Openwrt router or an Atheros WiFi NIC.
	packets[:10]=[128,0,0,0,160,243,193,255,50,89]

	wifiFiles = open('./gen_frag_packet/gen_pkt_'+str(seq_index)+'.txt', "w")

	for i in range(len(packets)-1):
		wifiFiles.write(str(packets[i])+'\n')
	wifiFiles.write(str(packets[i+1]))
	wifiFiles.close()
