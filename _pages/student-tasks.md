---
layout: archive
title: "Student Tasks"
permalink: /student-tasks/
author_profile: true
redirect_from:
  - /theses/
  - /topics/
---

{% include base_path %}

Below is a list of suggested topics for **bachelor's** and **master's** theses, as well as for
seminar and project assignments. The topics are grouped by the level at which they are usually
proposed, but almost every one of them can be scaled in either direction &mdash; the exact scope,
dataset and set of methods are agreed upon individually before the work starts.

If you are interested in one of the topics, or if you have an idea of your own in the areas of
robotics, artificial intelligence, network systems or operating systems, please get in touch at
[sandi.baressi.segota@unipu.hr](mailto:sandi.baressi.segota@unipu.hr).

**Before you write:** bring a short (half a page is enough) description of what you would like to do,
which tools you already know, and how much time you can realistically dedicate to the work. That is
usually enough for a first meeting.

**What is expected:** a working implementation (code in a public or shared repository), a described
and reproducible experiment, and a written thesis in which the results are compared and discussed
&mdash; not only reported. The literature listed with each topic is a starting point, not a complete
reading list.

Master's Thesis Topics
======

### 1. Reinforcement learning for collision-free motion planning of a collaborative robot

*Areas: Robotics, Artificial Intelligence*

Train a reinforcement learning agent (e.g. PPO or SAC) to move the end effector of a six-degree-of-freedom
manipulator between target poses in a cluttered workspace. The learned policy is compared against
classical sampling-based planners (RRT\*, PRM) on path length, execution time, number of collisions and
integrated joint torque. The work should also discuss the sim-to-real gap and what would be needed to
transfer the policy to a physical robot.

*Tools: CoppeliaSim / Gazebo, Python, Stable-Baselines3 or similar.*

**Suggested literature**

- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
- Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer.
- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., & Klimov, O. (2017). Proximal Policy Optimization Algorithms. *arXiv:1707.06347*.

### 2. Classification of encrypted network traffic using machine learning

*Areas: Network Systems, Artificial Intelligence*

Since payload inspection is not possible for encrypted traffic, classification has to rely on flow-level
statistics: packet size distribution, inter-arrival times, uplink/downlink ratio, burst length, flow
duration and similar. Collect your own capture and/or use a public dataset, engineer the feature set, and
compare classical models (random forest, XGBoost, SVM) with a 1D convolutional network. The influence of
individual features on the decision should be analysed with an explainability method.

*Tools: Wireshark / tshark, Python (scikit-learn, PyTorch), SHAP.*

**Suggested literature**

- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Draper-Gil, G., Lashkari, A. H., Mamun, M. S. I., & Ghorbani, A. A. (2016). Characterization of Encrypted and VPN Traffic Using Time-Related Features. *ICISSP 2016*.
- Rezaei, S., & Liu, X. (2019). Deep Learning for Encrypted Traffic Classification: An Overview. *IEEE Communications Magazine*, 57(5), 76&ndash;81.
- Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*.

### 3. Anomaly detection in operating system call traces

*Areas: Operating Systems, Artificial Intelligence*

The sequence of system calls issued by a process is a compact signature of its behaviour. Collect traces
of normal operation using `strace`, `auditd` or eBPF, model them with sequence-based methods (n-grams,
LSTM, or a small transformer), and evaluate how reliably injected anomalous behaviour is detected. An
important part of the work is measuring the runtime overhead introduced by the tracing itself.

*Tools: Linux, bpftrace / bcc, Python.*

**Suggested literature**

- Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
- Gregg, B. (2019). *BPF Performance Tools: Linux System and Application Observability*. Addison-Wesley.
- Forrest, S., Hofmeyr, S. A., Somayaji, A., & Longstaff, T. A. (1996). A Sense of Self for Unix Processes. *IEEE Symposium on Security and Privacy*.
- Creech, G., & Hu, J. (2014). A Semantic Approach to Host-Based Intrusion Detection Systems Using Contiguous and Discontiguous System Call Patterns. *IEEE Transactions on Computers*, 63(4), 807&ndash;819.

### 4. Digital twin of a robotic cell with machine learning based energy prediction

*Areas: Robotics, Artificial Intelligence*

Model an existing robotic workcell in a simulation package, log the corresponding motor power and joint
states from the real (or simulated) robot, and train a regression model that predicts the energy consumed
by a given trajectory. The model is then used as a cost function to rank alternative task sequences, and
the predicted savings are verified experimentally.

*Tools: RoboDK / CoppeliaSim, Python (scikit-learn, XGBoost).*

**Suggested literature**

- Baressi Šegota, S., Anđelić, N., Štifanić, J., & Car, Z. (2024). Regression Model for the Prediction of Total Motor Power Used by an Industrial Robot Manipulator during Operation. *Machines*, 12(4), 225.
- Kritzinger, W., Karner, M., Traar, G., Henjes, J., & Sihn, W. (2018). Digital Twin in Manufacturing: A Categorical Literature Review and Classification. *IFAC-PapersOnLine*, 51(11), 1016&ndash;1022.
- Corke, P. (2023). *Robotics, Vision and Control* (3rd ed.). Springer.
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow* (3rd ed.). O'Reilly.

### 5. Federated learning over a constrained network

*Areas: Network Systems, Artificial Intelligence, Operating Systems*

Deploy a federated learning setup across several nodes (containers, virtual machines or single-board
computers) and degrade the network between them in a controlled way using `tc`/netem &mdash; limited
bandwidth, added latency, packet loss. Compare plain FedAvg with compressed, quantised or sparsified
updates, and present the trade-off between reached accuracy, bytes transferred and wall-clock training
time.

*Tools: Docker / Linux namespaces, `tc` netem, Flower or a custom FL implementation.*

**Suggested literature**

- McMahan, H. B., Moore, E., Ramage, D., Hampson, S., & Agüera y Arcas, B. (2017). Communication-Efficient Learning of Deep Networks from Decentralized Data. *AISTATS 2017*.
- Kairouz, P., et al. (2021). Advances and Open Problems in Federated Learning. *Foundations and Trends in Machine Learning*, 14(1&ndash;2), 1&ndash;210.
- Tanenbaum, A. S., & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
- Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018). *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books.

### 6. Multimodal estimation of operator load in human-robot collaboration

*Areas: Robotics, Artificial Intelligence*

During collaborative assembly tasks, record several modalities describing the operator &mdash; for example
video, physiological signals and task performance &mdash; and train a model that estimates the level of
cognitive or physical load. Subjective NASA-TLX scores serve as a reference. The resulting model should be
interpreted, and the thesis should discuss how robot speed or task allocation could be adapted based on
the estimate.

*Tools: Python, OpenCV / MediaPipe, wearable sensors, scikit-learn.*

**Suggested literature**

- Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of Empirical and Theoretical Research. *Advances in Psychology*, 52, 139&ndash;183.
- Villani, V., Pini, F., Leali, F., & Secchi, C. (2018). Survey on Human-Robot Collaboration in Industrial Settings: Safety, Intuitive Interfaces and Applications. *Mechatronics*, 55, 248&ndash;266.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Lundberg, S. M., & Lee, S.-I. (2017). A Unified Approach to Interpreting Model Predictions. *NeurIPS 2017*.

Bachelor's Thesis Topics
======

### 1. Comparison of obstacle avoidance algorithms for a mobile robot

*Areas: Robotics*

Implement several classical obstacle avoidance approaches &mdash; for example Bug2, artificial potential
fields, the vector field histogram and the dynamic window approach &mdash; for a simulated mobile robot.
Test all of them in the same set of environments (open space, narrow corridor, local minimum trap,
dynamic obstacle) and compare success rate, path length, travel time and smoothness of motion.

*Tools: Python or ROS 2, Gazebo / CoppeliaSim.*

**Suggested literature**

- LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.
- Khatib, O. (1986). Real-Time Obstacle Avoidance for Manipulators and Mobile Robots. *The International Journal of Robotics Research*, 5(1), 90&ndash;98.
- Borenstein, J., & Koren, Y. (1991). The Vector Field Histogram &mdash; Fast Obstacle Avoidance for Mobile Robots. *IEEE Transactions on Robotics and Automation*, 7(3), 278&ndash;288.
- Fox, D., Burgard, W., & Thrun, S. (1997). The Dynamic Window Approach to Collision Avoidance. *IEEE Robotics & Automation Magazine*, 4(1), 23&ndash;33.

### 2. Web dashboard for live network traffic monitoring

*Areas: Network Systems*

Develop an application that captures traffic on a selected interface, aggregates it into flows, and
computes statistics in real time &mdash; number of packets and bytes per protocol, top talkers, average
packet size, round-trip time. The results are exposed through a small web interface with live charts and
a simple threshold-based alerting mechanism. The thesis should include a measurement of how much traffic
the tool itself can handle before it starts dropping packets.

*Tools: Python (Scapy or pyshark, FastAPI/Flask), JavaScript charting library.*

**Suggested literature**

- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
- Peterson, L. L., & Davie, B. S. (2021). *Computer Networks: A Systems Approach* (6th ed.). Morgan Kaufmann.
- Sanders, C. (2017). *Practical Packet Analysis* (3rd ed.). No Starch Press.
- *Wireshark User's Guide*. https://www.wireshark.org/docs/

### 3. Benchmarking process scheduling policies in Linux

*Areas: Operating Systems*

Prepare a set of workloads with different characteristics (CPU-bound, I/O-bound, latency-sensitive, mixed)
and run them under different scheduling policies and priorities &mdash; `SCHED_OTHER` with varying `nice`
values, `SCHED_FIFO`, `SCHED_RR` &mdash; and under different cgroup CPU limits. Measure throughput,
average and tail latency, and fairness between processes, and explain the observed behaviour using the
scheduler's design.

*Tools: Linux, `stress-ng`, `perf`, `chrt`, `cgroups`, Python for analysis and plotting.*

**Suggested literature**

- Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
- Arpaci-Dusseau, R. H., & Arpaci-Dusseau, A. C. (2018). *Operating Systems: Three Easy Pieces*. Arpaci-Dusseau Books.
- Love, R. (2010). *Linux Kernel Development* (3rd ed.). Addison-Wesley.
- Gregg, B. (2020). *Systems Performance: Enterprise and the Cloud* (2nd ed.). Addison-Wesley.

### 4. Image classification with convolutional neural networks and transfer learning

*Areas: Artificial Intelligence*

Collect or select a small image dataset from an agreed domain, and compare a convolutional network trained
from scratch with several pre-trained architectures fine-tuned on the same data. Examine the influence of
data augmentation and dataset size on the achieved performance, and evaluate the models not only by
accuracy but also by inference time and memory footprint on a constrained device.

*Tools: Python (PyTorch or TensorFlow/Keras), Raspberry Pi or similar for deployment.*

**Suggested literature**

- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. *CVPR 2016*.
- Howard, A. G., et al. (2017). MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications. *arXiv:1704.04861*.
- Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow* (3rd ed.). O'Reilly.

### 5. Comparison of application layer protocols for the Internet of Things

*Areas: Network Systems, Internet of Things*

Implement the same telemetry application &mdash; a set of sensor nodes reporting to a collector &mdash;
using MQTT, CoAP and plain HTTP. Under identical conditions, measure end-to-end latency, protocol
overhead per useful byte, number of packets, and behaviour under artificially introduced packet loss and
delay. Conclude with a recommendation on which protocol suits which class of deployment.

*Tools: Python or C, Mosquitto broker, `tc` netem, ESP32 or Raspberry Pi.*

**Suggested literature**

- OASIS (2019). *MQTT Version 5.0*. OASIS Standard.
- Shelby, Z., Hartke, K., & Bormann, C. (2014). *The Constrained Application Protocol (CoAP)*. RFC 7252.
- Naik, N. (2017). Choice of Effective Messaging Protocols for IoT Systems: MQTT, CoAP, AMQP and HTTP. *IEEE International Systems Engineering Symposium (ISSE)*.
- Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.

### 6. Gesture-based control of a robot using computer vision

*Areas: Robotics, Artificial Intelligence*

Detect the operator's hand in a camera stream, extract landmark positions, and classify a small vocabulary
of gestures which are then mapped to commands for a simulated (or, if available, real) robot. Evaluate
recognition accuracy per gesture, latency from gesture to robot reaction, and robustness to changes in
lighting and distance from the camera.

*Tools: Python, OpenCV, MediaPipe, ROS 2 or a simulator of choice.*

**Suggested literature**

- Lugaresi, C., et al. (2019). MediaPipe: A Framework for Building Perception Pipelines. *arXiv:1906.08172*.
- Quigley, M., et al. (2009). ROS: An Open-Source Robot Operating System. *ICRA Workshop on Open Source Software*.
- Corke, P. (2023). *Robotics, Vision and Control* (3rd ed.). Springer.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.

Proposing Your Own Topic
======

Topics outside this list are welcome, provided they fall within the areas above and can be evaluated
experimentally. A proposal is easiest to discuss if it states what will be built, what will be measured,
and what it will be compared against. If you already have data, a device or a company partner involved,
mention that in the first e-mail &mdash; it usually shapes the topic more than anything else.
