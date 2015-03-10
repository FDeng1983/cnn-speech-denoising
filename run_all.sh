#MAXFILES=$1
#SAMPLES=$2
#TIMESLICE=$3
#LR=$4
#GAMMA=$5
#REG=$6
#MAXITER=$7
#AUGMENT=$8
#NNARCH=$9

# network in network
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x7.16_r_c1x1.32_r_c1x1.32_r_c1x1.32_r_c7x7.16_c7x7.16_r_c7x7.1

# skinny filters
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x1.16_r_c1x7.16_r_c7x1.16_r_c1x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c1x7.16_r_c7x1.16_r_c1x7.16_r_c7x1.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

# consistent filters
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c3x3.32_r_c3x3.32_r_c3x3.32_r_c3x3.32_r_c3x3.1
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

# deep
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.8_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
