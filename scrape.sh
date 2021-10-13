#!/bin/bash
 #curl --location --request GET 'https://github.com/search?l=&p='i'&q=label%3Asecurity+language%3AC%2B%2B&state=closed&type=Issues' --header 'Cookie: _gh_sess=RhggTLKxUeGHYvZIUNCoXKUPTKMghQJ9XqBUH57n8om9a7D1IMeys8UCoMO2BR2eoNG9HF7yNcB7MyOC47g21NURSEudUVHIW3UQ%2BFBV655kFmUB%2Ft5Ku72EJY%2F%2B5GY8e4za6k94Y1%2BI4zZg35V7N%2FknW9BD18wNUJT%2F6VPnOas4Zvv6bvW9Bhq8Df2aVHke1hPZkd8V%2FJ%2BTYzL4aNMg3TJurdzMBDgPHfuU0wkMmRdYaj%2FE%2FgH514fLV1gl5tPSu63EoTx69TE02fVn%2F%2FjEoQ%3D%3D--UsNB9gLM4zk896%2Fo--ldPYRhv%2F12iLWhd6a5%2BdgQ%3D%3D; _octo=GH1.1.410103904.1634072203; logged_in=no' | grep '<a title='| grep -o -E "href.*>" | grep pull >>op
i=1
while [ $i -le 100 ]
do
curl --location --request GET 'https://github.com/search?l=&p='$i'&q=label%3Asecurity+language%3AC%2B%2B&state=closed&type=Issues' \
--header 'Cookie: _gh_sess=CQX5mYujsnnGZ%2BIC3jZL%2Fz8yEUaQzZGvVCzcwhM%2FBW4bbwD02NyoHwb44TODkuDRqo8zeITHv8YczgNIIRNAcBXIeg49%2Br1PbLxsDjZCaaSsYZH%2Fp9n6%2FF9Sjc0WaKltm1nhdJLFGnDNBtQrGMWKYnkC%2FJcpxvdT53D%2F23t6CXMgUnnQWZzmriISAoesKzIQ5QsL%2FbY2zoVrnn6qPXwlsOuRh1MldIez2AoLe3vv%2FQ3InsPZixxLA5tg54X%2BYiyXtrM54%2FXJkwL31maZ2epJ4w%3D%3D--p%2FCtRtAvwLgXygDk--pSpPufLHiiCKiUD%2BU6MruA%3D%3D; _octo=GH1.1.410103904.1634072203; logged_in=no'|  grep -o -E "href.*>" | grep -E "pull|issues" >>op
echo 'https://github.com/search?l=&p='$i'&q=label%3Asecurity+language%3AC%2B%2B&state=closed&type=Issues'
sleep 3
((i++))
done
echo All done
