#MAXFILES=$1
#SAMPLES=$2
#TIMESLICE=$3
#LR=$4
#GAMMA=$5
#REG=$6
#MAXITER=$7
#AUGMENT=$8
#NNARCH=$9

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.32_r_c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.32_r_c1x1.32_r_c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.32_r_c1x1.32_r_c5x5.32_r_c1x1.32_r_c5x5.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.64_r_c1x1.64_r_c5x5.64_r_c1x1.64_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.64_r_c1x1.128_r_c5x5.128_r_c1x1.128_r_c5x5.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c1x1.32_r_c1x1.32_r_c3x3.32_r_c3x3.32_r_c3x3.32_r_c1x1.128_r_c1x1.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c1x1.32_r_c1x1.32_r_c1x1.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c3x3.32_r_c3x3.32_r_c3x3.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c9x9.16_r_c9x9.16_r_c9x9.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c7x7.16_r_c7x7.16_r_c7x7.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c5x5.16_r_c5x5.16_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 1 c3x3.16_r_c3x3.16_r_c3x3.1


# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.32_r_c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.32_r_c1x1.32_r_c5x5.32_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.32_r_c1x1.32_r_c5x5.32_r_c1x1.32_r_c5x5.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.64_r_c1x1.64_r_c5x5.64_r_c1x1.64_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.64_r_c1x1.128_r_c5x5.128_r_c1x1.128_r_c5x5.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c1x1.32_r_c1x1.32_r_c3x3.32_r_c3x3.32_r_c3x3.32_r_c1x1.128_r_c1x1.1

# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c1x1.32_r_c1x1.32_r_c1x1.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c3x3.32_r_c3x3.32_r_c3x3.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c9x9.16_r_c9x9.16_r_c9x9.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c7x7.16_r_c7x7.16_r_c7x7.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c5x5.16_r_c5x5.16_r_c5x5.1
# bash run_autoenc.sh 100 5 20 .0001 .9 0 1000 0 c3x3.16_r_c3x3.16_r_c3x3.1

########################

#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c9x9.16_r_c9x9.16_r_c9x9.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x7.16_r_c7x7.16_r_c7x7.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c5x5.16_r_c5x5.16_r_c5x5.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c1x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
#bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x1.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x1.16_r_c1x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c1x7.16_r_c7x1.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x1.16_r_c1x7.16_r_c7x1.16_r_c1x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c1x7.16_r_c7x1.16_r_c1x7.16_r_c7x1.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c7x1.32_r_c1x7.32_r_c7x7.32_r_c7x7.32_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0 1000 0 c1x7.32_r_c7x1.32_r_c7x7.32_r_c7x7.32_r_c7x7.1

bash run_autoenc.sh 100 5 100 .0001 .9 0.000001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0.000001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0.00001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1

bash run_autoenc.sh 100 5 100 .0001 .9 0.0001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1
bash run_autoenc.sh 100 5 100 .0001 .9 0.0001 1000 0 c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.16_r_c7x7.1


