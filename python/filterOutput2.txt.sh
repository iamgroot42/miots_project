sed 's/<\/html>/\n/g' -i tmp 
sed 's/<html><body>You are being <a href="//g' -i tmp 
sed 's/">redirected.*$//g' -i tmp 
cat tmp | grep -E '^https://github.com' > tmp2
sed 's/github/api\.github/g' -i tmp2
sed 's/com/com\/repos/g'  -i tmp2
sed 's/pull/pulls/g' -i tmp2
rm tmp3
cat tmp2| xargs -I'{}' curl -H 'Authorization:token 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' {} | jq '[.base.sha , .merge_commit_sha] | join("\t")'  > tmp3
