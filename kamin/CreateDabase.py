import pickle
f_1 = open('mydatabase', 'w')
DatabasetoBestored=[['Alice','01','it is alice '], \
                    ['Love ','02','it,is love 1'], \
                    ['Bob  ','03','it.is Bob   '],\
                    ['Zhang','04','ISrael      '],\
                    ['Wang ','05','United sates'],\
                    ['Zhao ','06','Ok come     '],\
                    ['Ming ','07','it is Bob   '],\
                    ['Hilel','08','yes,it is Me'],]
DatabasetoBestored=pickle.dump(DatabasetoBestored,f_1)
f_1.close()
