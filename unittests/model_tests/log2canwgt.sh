#!/bin/bash
dirn=$(ls -t reports | head -1)
fn=$(ls -S reports/$dirn/run_1/provenance_data/*.txt | head -1)
filen=$fn
#echo $filen
outdir='data'
cat $filen |python log_ca.py > $outdir/ca.txt
cat $filen |python log_wgt.py > $outdir/wgt.txt


