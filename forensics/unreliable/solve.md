tcpflow -X /dev/null -r unreliable.pcap
for i in {1..64}; do cut -b $i *.08888| sort -u; done | tr -d '\n'; echo
