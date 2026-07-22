import pandas as pd

df = pd.read_csv('final_results.csv')

t = df['tournament'].unique().tolist()

for i in t:
    print(i)

print(len(t))

'''
with open('tournaments.txt', 'w') as file:
    for i in t:
        file.write(i + '\n')'''