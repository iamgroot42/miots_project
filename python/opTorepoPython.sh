cat opPython  | grep issues | sed 's/href="//g' | sed 's/<\/a>//g'| sed 's/">/\t/g'| sed 's/issues.*$//g' | sort | uniq > repoPython
