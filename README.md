# AI-based ICS Incident Investigation System
This project was built and completed during the GCC 2025 in Taiwan by **Group 8**, It called "AI-based ICS Incident Investigation System"
## Requirements

- Analyse malicious or abnormal traffic in ICS environment or traffic recording pcap
- Import AI module to support multiple ICS protocol for different environments
- Fine tune AI module for traffic analysing
- Able to display network topology, infected devices and indicate malicious actions
- Bonus: use AI to automate attacks on ICS


## ICS System Architecture

![image](https://github.com/user-attachments/assets/0cc7972e-cb54-41ac-9b88-ca994ab2d2dd)

## Data Flow 

![image](https://github.com/user-attachments/assets/f1461b2d-4c9e-4306-8f81-94cac135162b)

## Data Collection
### Anomaly Detection Dataset for Industrial Control Systems
- **Input**: .pcap files
- ICS-Flow from kaggle (https://www.kaggle.com/datasets/alirezadehlaghi/icssim/data)
- Capture from simulation system
- **Output**: malicious “network flow”
### Attack type: 
Normal, ddos, ip-scan, mitm, port-scan, replay, command-injection

## Generate Flow
- Multiple packets → One network flow
- Group by (protocol, source, destination)
- Preprocess data
- Handle sequential data
- Capture common characteristic

## AI Training 
### Training AI Model with ICS Dataset
![image](https://github.com/user-attachments/assets/5b63a873-c6ea-4407-857a-4c8cbaa87ce5)

## Model-AI

### XGBoost

- Multi-class classification and NaN
- Fast training
- Great performance

![image](https://github.com/user-attachments/assets/6252d5e3-2d38-4eb0-8b24-a1b5f538d644)


## Result
### Result-Training

![image](https://github.com/user-attachments/assets/c4f71fce-a6d4-4817-94bf-892982c8aa34)

### Result-Validation

![image](https://github.com/user-attachments/assets/0ef1ee30-f312-4277-bdab-137ca7fab3ba)

## Tool Architecture

###  Use AI Model and Visualize the Network Topology

![image](https://github.com/user-attachments/assets/4daf0c52-372b-479e-b005-ee5dd2c8d615)
