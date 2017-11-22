#!/bin/bash
dirn=$(ls -t reports | head -1)
fn=$(ls -S reports/$dirn/run_1/provenance_data/*.txt | head -1)
filen=$fn
echo $filen
outdir='data'
cat $filen |grep "calcium" | awk '{print $10}' > $outdir/ca.txt
cat $filen |grep "Neuron" -A 8  | paste - - - - - - - - - -  | awk '{print $56, $51}' > $outdir/wgt.txt


