
mottos = open("motto.txt")

new_motto = open("new-motto.txt", 'w')

f = open('new-motto.txt', 'r')
result = list()
for line in mottos:
    line = mottos.readline()
    result.append(line)
f.close()

print(result)

for mo in result:
    new_motto.writelines('"' + mo + '",')