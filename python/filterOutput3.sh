paste tmp0 tmp3 >tmp4
sed 's/github/api.github/g' -i tmp4 
sed 's/com/com\/repos/g' -i tmp4 
sed 's/pull/pulls/g' -i tmp4
sed 's/pull.*/compare\//g' tmp0 >tmp5
paste tmp4 tmp5 >tmp6
sed 's/ /	/g' -i tmp6
awk -F'\t' 'BEGIN {OFS="\t"} {print $1,$2,$3,$4$2"..."$3".diff"}' tmp6 > pullDiff.tsv
