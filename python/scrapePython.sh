#!/bin/bash
i=1
while [ $i -le 100 ]
do
curl --location --request GET 'https://github.com/search?l=&o=desc&p='$i'&q=language%3APython+state%3Aclosed&s=comments&type=Issues'  \
--header 'Cookie: _gh_sess=CQX5mYujsnnGZ%2BIC3jZL%2Fz8yEUaQzZGvVCzcwhM%2FBW4bbwD02NyoHwb44TODkuDRqo8zeITHv8YczgNIIRNAcBXIeg49%2Br1PbLxsDjZCaaSsYZH%2Fp9n6%2FF9Sjc0WaKltm1nhdJLFGnDNBtQrGMWKYnkC%2FJcpxvdT53D%2F23t6CXMgUnnQWZzmriISAoesKzIQ5QsL%2FbY2zoVrnn6qPXwlsOuRh1MldIez2AoLe3vv%2FQ3InsPZixxLA5tg54X%2BYiyXtrM54%2FXJkwL31maZ2epJ4w%3D%3D--p%2FCtRtAvwLgXygDk--pSpPufLHiiCKiUD%2BU6MruA%3D%3D; _octo=GH1.1.410103904.1634072203; logged_in=no'|  grep -o -E "href.*>" | grep -E "pull|issues" >>opPython
echo 'https://github.com/search?l=&p='$i'&q=label%3Asecurity+language%3AC%2B%2B&state=closed&type=Issues'
sleep 3
((i++))
done
echo All done


