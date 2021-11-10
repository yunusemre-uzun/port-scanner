This project aims to apply nmap port scanner with a web UI.

How to run:

    1. Dependencies: Docker, docker-compose, Kafka
    2. Steps:
    
      * Clone the project
      * Run 'docker-compose up kafka elasticsearch'
      * Wait for kafka and elastic seatch to settle
      * Run '/scripts/kafka_partition.sh' to create kafka partitions. You may need to specify kafka binary in your system
      * Run 'docker-compuse up elk scanner web-server
      * Open localhost:8085 on your browser
    3. Run:
      * Type for host eg(192.168.1.1) or net mask (192.168.1.0/24)
      * Select single port, port range or all ports
      * Type arguments(If OS detection is choosen arguments will be inefective)
      * Enable/Disable OSDetection
