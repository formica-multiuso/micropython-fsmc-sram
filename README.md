# micropython-fsmc-sram
## Micropython FSMC Driver for External SRAM on STM32F439

The class is designed for IS61WV102416 1M x 16bit SRAM from ISSI, but is easily modifiable.
Read [STM43F4xx Reference Manual](https://goo.gl/bq5Bsw) (RM0090, page 1540)

#### Simple Read/Write
```
>>> from fsmc import fsmc_sram_buffer
>>> sram_b = fsmc_sram_buffer(50000,0x64000000,0x64000000,0x64000000+0xc350,0x02) ## 50000 16bit locations = 100KB

>>> sram_b.write(0x5555) ## Push the 16bit value 0x5555 (int:21845) in memory
>>> it = 0
>>> sram.read_i(it) ## Read from the memory using an iterator
21845 
>>> sram.read_a(0x64000000) ## Read from the memory using a memory address
0
```
#### Fill with zeros and Flush on file
```
>>> from fsmc import fsmc_sram_buffer
>>> sram_b = fsmc_sram_buffer(50000,0x64000000,0x64000000,0x64000000+0xc350,0x02) ## 50000 16bit locations = 100KB
>>> sram_b.fill_with_number() ## fill with zeros
>>> fd = open("file.dat",'w')
>>> sram_b.flush_on_file(fd) ## flush on file
>>> fd.close()
```

