import stm
import utime

''' 
FSMC EXTERNAL MEMORY CLASS: 16bit SRAM
This class is designed for the IS61WV102416. Producer: ISSI
Tested on STM32F439ZIT6

Copyleft, Roberto Marino 2017 - formica@member.fsf.org

'''


class fsmc_sram_buffer(object):
	def __init__(self, size, bank_addr, start_addr, end_addr, addr_inc):
		self.size = size 	## expressed in word
		self.baddr = bank_addr
		self.saddr = start_addr
		self.eaddr = end_addr
		self.addri = addr_inc
		self.memory_init()
		self.iterator = 0
		self.t16 = 0
		self.t1 = 0
		self.t2 = 0
		self.wtime = 0

	def memory_init(self):
		### RCC_CLOCK INIT #####
		stm.mem32[stm.RCC + stm.RCC_AHB1ENR]  |= 0x00000078
		stm.mem32[stm.RCC + stm.RCC_AHB3ENR] |= 0x00000001
		stm.mem32[stm.RCC + stm.RCC_AHB3RSTR]  |= 0x00000000
		### GPIOx_AFRL INIT - Offset: 0x20 #####
		stm.mem32[stm.GPIOD + 0x20] |= 0x00CC00CC ## or 0x00320022
		stm.mem32[stm.GPIOE + 0x20] |= 0xC000C0C0
		stm.mem32[stm.GPIOF + 0x20] |= 0x00CCCCCC
		stm.mem32[stm.GPIOG + 0x20] |= 0x00CCCCCC
		### GPIOx_AFRH INIT - Offset: 0x24 #####
		stm.mem32[stm.GPIOD + 0x24] |= 0xCCCCCCCC
		stm.mem32[stm.GPIOE + 0x24] |= 0xCCCCCCCC
		stm.mem32[stm.GPIOF + 0x24] |= 0xCCCC0000
		stm.mem32[stm.GPIOG + 0x24] |= 0x000000C0 ## or 0x00000030
		### GPIOx_MODER INIT - Offset: 0x00 ####
		stm.mem32[stm.GPIOD + 0x00] |= 0xAAAA0A0A
		stm.mem32[stm.GPIOE + 0x00] |= 0xAAAA808A
		stm.mem32[stm.GPIOF + 0x00] |= 0xAA000AAA
		stm.mem32[stm.GPIOG + 0x00] |= 0x00080AAA
		### GPIOx_OTYPER INIT - Offset: 0x04 ###
		stm.mem32[stm.GPIOD + 0x04] |= 0x00000000
		stm.mem32[stm.GPIOE + 0x04] |= 0x00000000
		stm.mem32[stm.GPIOF + 0x04] |= 0x00000000
		stm.mem32[stm.GPIOG + 0x04] |= 0x00000000
		### GPIOx_PUPDR INIT - Offset: 0x0C ####
		stm.mem32[stm.GPIOD + 0x0C] |= 0x00000000
		stm.mem32[stm.GPIOE + 0x0C] |= 0x00000000
		stm.mem32[stm.GPIOF + 0x0C] |= 0x00000000
		stm.mem32[stm.GPIOG + 0x0C] |= 0x00000000
		### GPIOx_OSPEEDR INIT - Offset: 0x08 ##
		stm.mem32[stm.GPIOD + 0x08] |= 0xFFFF0F0F
		stm.mem32[stm.GPIOE + 0x08] |= 0xFFFFC0CF
		stm.mem32[stm.GPIOF + 0x08] |= 0xFF000FFF
		stm.mem32[stm.GPIOG + 0x08] |= 0x000C0FFF
		#### FMC INIT ###########################
		stm.mem32[0xA0000000 + 0x00000008] |= 0x00001011      ## write on FSMC_BCR2
		stm.mem32[0xA0000004 + 0x00000008] |= 0x00110212      ## write on FSMC_BTR2
		stm.mem32[0xA0000104 + 0x00000008] |= 0x00110212      ## write on FSMC_BWTR2

	def fsmc_register_dump(self):
		#### RCC REGS #######################
		RCC_AHB1ENR = stm.mem32[stm.RCC + stm.RCC_AHB1ENR]
		RCC_AHB3ENR = stm.mem32[stm.RCC + stm.RCC_AHB3ENR]
		RCC_AHB3RSTR = stm.mem32[stm.RCC + stm.RCC_AHB3RSTR]
		### GPIOx_MODER INIT - Offset: 0x00 ####
		GPIOD_MODER = stm.mem32[stm.GPIOD + 0x00]
		GPIOE_MODER = stm.mem32[stm.GPIOE + 0x00]
		GPIOF_MODER = stm.mem32[stm.GPIOF + 0x00]
		GPIOG_MODER = stm.mem32[stm.GPIOG + 0x00]
		### GPIOx_AFRL INIT - Offset: 0x20 #####
		GPIOD_AFRL = stm.mem32[stm.GPIOD + 0x20] 
		GPIOE_AFRL = stm.mem32[stm.GPIOE + 0x20]
		GPIOF_AFRL = stm.mem32[stm.GPIOF + 0x20]
		GPIOG_AFRL = stm.mem32[stm.GPIOG + 0x20]
		### GPIOx_AFRH INIT - Offset: 0x24 #####
		GPIOD_AFRH = stm.mem32[stm.GPIOD + 0x24]
		GPIOE_AFRH = stm.mem32[stm.GPIOE + 0x24]
		GPIOF_AFRH = stm.mem32[stm.GPIOF + 0x24]
		GPIOG_AFRH = stm.mem32[stm.GPIOG + 0x24]
		### GPIOx_OTYPER INIT - Offset: 0x04 ###
		GPIOD_OTYPER = stm.mem32[stm.GPIOD + 0x04]
		GPIOE_OTYPER = stm.mem32[stm.GPIOE + 0x04]
		GPIOF_OTYPER = stm.mem32[stm.GPIOF + 0x04]
		GPIOG_OTYPER = stm.mem32[stm.GPIOG + 0x04]
		### GPIOx_PUPDR INIT - Offset: 0x0C ####
		GPIOD_PUPDR = stm.mem32[stm.GPIOD + 0x0C]
		GPIOE_PUPDR = stm.mem32[stm.GPIOE + 0x0C]
		GPIOF_PUPDR = stm.mem32[stm.GPIOF + 0x0C] 
		GPIOG_PUPDR = stm.mem32[stm.GPIOG + 0x0C]
		### GPIOx_OSPEEDR INIT - Offset: 0x08 ##
		GPIOD_OSPEEDR = stm.mem32[stm.GPIOD + 0x08]
		GPIOE_OSPEEDR = stm.mem32[stm.GPIOE + 0x08]
		GPIOF_OSPEEDR = stm.mem32[stm.GPIOF + 0x08]
		GPIOG_OSPEEDR = stm.mem32[stm.GPIOG + 0x08]
		FSMC_BCR2 = stm.mem32[0xA0000000 + 0x00000008]
		FSMC_BTR2 = stm.mem32[0xA0000004 + 0x00000008]	 
		FSMC_BWTR2 = stm.mem32[0xA0000104 + 0x00000008]
		print("-- REGISTER DUMP --")
		print("RCC_AHB1ENR: ", hex(RCC_AHB1ENR))
		print("RCC_AHB3ENR: ", hex(RCC_AHB3ENR))
		print("RCC_AHB3RSTR: ", hex(RCC_AHB3RSTR))
		print("GPIOD_MODER: ", hex(GPIOD_MODER))
		print("GPIOE_MODER: ", hex(GPIOE_MODER))
		print("GPIOF_MODER: ", hex(GPIOF_MODER))
		print("GPIOG_MODER: ", hex(GPIOG_MODER))
		print("GPIOD_AFRL: ", hex(GPIOD_AFRL))
		print("GPIOE_AFRL: ", hex(GPIOE_AFRL))
		print("GPIOF_AFRL: ", hex(GPIOF_AFRL))
		print("GPIOG_AFRL: ", hex(GPIOG_AFRL))
		print("GPIOD_AFRH: ", hex(GPIOD_AFRH))
		print("GPIOE_AFRH: ", hex(GPIOE_AFRH))
		print("GPIOF_AFRH: ", hex(GPIOF_AFRH))
		print("GPIOG_AFRH: ", hex(GPIOG_AFRH))
		print("GPIOD_OTYPER: ", hex(GPIOD_OTYPER))
		print("GPIOE_OTYPER: ", hex(GPIOE_OTYPER))
		print("GPIOF_OTYPER: ", hex(GPIOF_OTYPER))
		print("GPIOG_OTYPER: ", hex(GPIOG_OTYPER))
		print("GPIOD_PUPDR: ", hex(GPIOD_PUPDR))
		print("GPIOE_PUPDR: ", hex(GPIOE_PUPDR))
		print("GPIOF_PUPDR: ", hex(GPIOF_PUPDR))
		print("GPIOG_PUPDR: ", hex(GPIOG_PUPDR))
		print("GPIOD_OSPEEDR: ", hex(GPIOD_OSPEEDR))
		print("GPIOE_OSPEEDR: ", hex(GPIOE_OSPEEDR))
		print("GPIOF_OSPEEDR: ", hex(GPIOF_OSPEEDR))
		print("GPIOG_OSPEEDR: ", hex(GPIOG_OSPEEDR))
		print("FSMC_BCR2: ", hex(FSMC_BCR2))
		print("FSMC_BTR2: ", hex(FSMC_BTR2))
		print("FSMC_BWTR2: ", hex(FSMC_BWTR2))


	def write(self,data):
		if (self.iterator >= self.size):
			self.iterator = 0
		stm.mem16[self.baddr + self.addri*self.iterator] = data
		#print("Wrote ",data," on ", self.baddr+self.addri*self.iterator)
		self.iterator += 1
	
	def read_i(self, it):
		ret = stm.mem16[self.baddr + self.addri*it]
		#print("Read ", ret, " on ", self.baddr + self.addri*it)
		return ret
	
	def read_a(self, oaddr):
		ret = stm.mem16[self.baddr + oaddr] #oaddr is an offset
		return ret

	def flush_on_file(self,fd):
		self.t1 = utime.ticks_ms()
		for i in range(0,self.size):
			self.t16 = stm.mem16[self.baddr + self.addri*i]
			fd.write('{:X} '.format(self.t16))
		self.t2 = utime.ticks_ms()
		self.wtime = utime.ticks_diff(self.t2,self.t1)
		self.iterator = 0
	
	def fill_with_number(self):
		for i in range(self.size):
			if(self.iterator >= self.size):
				self.iterator = 0
			stm.mem16[self.baddr + self.addri*self.iterator] = 0
			self.iterator +=1
		self.iterator = 0

	 		 
