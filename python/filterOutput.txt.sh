sed 's/a href="//g' -i output.txt
sed 's/"$//g' -i output.txt
rm tmp
cat output.txt | xargs -I'{}' curl 'https://github.com/{}' -H 'cookie: _octo=GH1.1.251309622.1630158620;  user_session=Oe5o8S2w85Udl8xu-jIsXzXqKDtPr9J92hSy73Jnf3lfeYlU; __Host-user_session_same_site=Oe5o8S2w85Udl8xu-jIsXzXqKDtPr9J92hSy73Jnf3lfeYlU; logged_in=yes; dotcom_user=noble-8; has_recent_activity=1; _gh_sess=y4N%2FlCcjUzBmGwuIiSoU0JVLqLO1I5hzn%2FjNc1SAZKq7zphmWi9zRUMqswLOaJbMaA8LMJUJWj45djhmEpBHASTl%2BPWopq%2Fc%2BnqwLVozETQY9Rp7dRFYdzYCVyYNFUF6lzuq32E58CAVi8OuMuWkDPX1t01f3uVLbAaKdlB3KMZ6Ilafmr%2Fj2gD535KPb%2BwMZAwOg2RFD2OxQfvL5vRVqsRGFti2n37qK5a9pxeCULWxR5ebsc8upqqv0EJzFIvN4aOFQDohyzBTMouBnFbSa5VbJ6Q3Rdu%2Fu6XrbbvKLNje3Tey%2FYeJILsUNQDXW1B5%2Fdc%2FPCpMgGdo7vIudHpqx9PafXstu1JbHsG0ba%2BJ%2BPuFYwn7Infu4IJyfe2BIA7re57iaZL6tsygWrLEv9l7Diipb%2FObSGmD9wGdA2BJYIxU9u5bbcZVG3Tks1D3y0sVdeKJiBoxWFJGOSxoqVFqyDgGCAtgVAihnfGPhQ6hbWvrUuJ8Jkfh%2FT6pVQ9Rc4fyNf90hYnRrsmUf3atRTz9pM6FmHBoBTcGd9CENjZdRo2NoVn%2B5VaA8bMIvUgIDwQfsM%2FGg%2FRFcOCqWEgtaGod05Ho0No3hfBGP%2FMJCelW%2BdQ%3D--bVkt16yGZ%2Br%2Fypk2--JrTuqI1%2FpxGlnzZsl5dm7w%3D%3D' --compressed > tmp
sed 's/<\/html>/\n/g' -i tmp 
sed 's/<html><body>You are being <a href="//g' -i tmp
sed 's/">redirected.*$//g' -i tmp
cat tmp | grep -E "^https" > tmp0
