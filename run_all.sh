#MAXFILES=$1
#SAMPLES=$2
#TIMESLICE=$3
#LR=$4
#GAMMA=$5
#REG=$6
#MAXITER=$7
#NNARCH=$8

bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 c5x5.1
bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 c5x5.32_r_c5x5.1
bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 c5x5.32_r_c5x5.32_r_c5x5.1
bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 c5x5.32_r_c1x1.32_r_c5x5.32_r_c5x5.1
bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 c5x5.32_r_c1x1.32_r_c5x5.32_r_c1x1.32_r_c5x5.1
