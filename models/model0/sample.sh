#!/usr/bin/env bash
python patch_sampler.py dataset/mfcc/clean --normalize_spec --max_mfcc 1e5 --scale_mfcc 1e-5
