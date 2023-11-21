import re, sys

corpus_content = open(sys.argv[1], 'r', encoding='utf-8').readlines()
dic = open('subst.dic', 'r', encoding='utf-16-le').readlines()
dic_enrichi = open("subst_corpus.dic", 'w', encoding='utf-16-le')
dic_enrichi.write('\ufeff \n')
temp = [] ##cette liste vas contenir les elements sur le corpus
print("Medicaments apres enrichissement sont : \n")
for i in corpus_content:
    x = re.search(r"^-? ?(\w+) :? ?(\d+|,)+ (mg|ml).+", i, re.I)
    if x:
        dic_enrichi.write(str(x.group(1)) + ",.N+subst \n")
        print(str(x.group(1).lower()) + ",.N+subst ")

        t = str(x.group(1)).lower()
        ## match inside the subst dic the current element
        y = re.search(t, str(dic), re.I)
        if y == None:
            if t != "puis" and not t.startswith("ø") and t != "intraveineuse":
                temp.append(t)

        if t != "puis" and not t.startswith("ø") and t != "intraveineuse":
            dic.append(t + ",.N+subst\n")
dic_enrichi.close()

## elimination des doublons avec le dict
list_trie = dict.fromkeys(sorted(dic))

## generation du fichier infos3
Min = ord('A')
Max = ord('Z')

infos3 = open("infos3.txt", 'w', encoding='utf-8')
sum = 0
for i in range(Min, Max + 1):
    current_char = chr(i)
    cpt_char = 0
    for c in temp:
        if (c[0].lower() == current_char.lower()):
            cpt_char = cpt_char + 1
    infos3.write("le nombre de medicaments issus de l'enrichissement commencant par la lettre " + current_char +
                " est : " + str(cpt_char) + "\n")
    sum = sum + cpt_char
infos3.write("le nombre total de medicaments issus de l'enrichissement est : " + str(sum) + "\n")
infos3.close()

w = open("subst.dic", "w", encoding="utf-16-le")
w.write('\ufeff \n')

list_trie = list(dict.fromkeys(sorted(list_trie)))

w.write(list_trie[-1])
## on trie le 'é' manuellment et on le met apres le 'e'
for i in list_trie:
    if i[0] <= 'e':
        w.write(i)

for i in list_trie:
    if i[0] == 'é':
        w.write(i)

for i in list_trie:
    if i[0] > 'e' and i[0] <= 'z':
        w.write(i)
w.close()

## generation de fichier infos2
test = open("infos2.txt", "w")
fichier = open("subst_corpus.dic", "r",
               encoding="utf-16-le").read().lower().split()
list_enrich = list(dict.fromkeys(sorted(fichier[1:-1])))
first_car = list_enrich[0][0].lower()

cpt = 0
for token in list_enrich:
    if token.lower().startswith(first_car) and token.lower(
    ) != "puis" and token.lower() != "intraveineuse " and first_car != "ø":
        cpt += 1
    else:
        if token != "puis" and not token.startswith(
                "ø") and token != "intraveineuse":
            #Si notre script rencontre un mot qui ne commence pas par le terme courant , alors il affiche le nombre de medicament commencant par la dite lettre
            test.write(
                "Le nombre de médicaments issus du corpus qui commencent par la lettre "
                + first_car + " sont: " + str(cpt) + "\n")
            first_car = token[0]
            cpt = 1
test.write(
    "Le nombre de médicaments issus du corpus qui commencent par la lettre "
    + first_car + " sont: " + str(cpt) + "\n")
test.write(
    "Le nombre total de médicament issus du corpus est: " +
    str(len(list_enrich)) + " \n")
test.close()