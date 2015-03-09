grep -b1 "Optimization Done" *.log | grep -v Optimization | grep -v "\-\-" | gawk '{print $1" "$(NF-1)}' | perl -ne 's/\.caffe\.log\S+/ /; print' | sort -nr -k2
