f = open("D:\\androidwork\\gtgj_main\\app\\src\\main\\java\\com\\gtgj\\utility\\dfp\\DfpGenUtils.java",'r',encoding='utf-8')
rs = {}
for line in f:
    if "hashMap.put(\"" in line and "()" in line and ")))" not in line:
        s1 = line.split(",")
        name = s1[0].split("(")[1]
        name = name[1:len(name) - 1]
        key = s1[1][0:s1[1].index("(")]
        rs[key] = name
f = open("D:\\androidwork\\gtgj_main\\app\\src\\main\\java\\com\\gtgj\\utility\\dfp\\DfpGenUtils.java",'r',encoding='utf-8')
fp = open("D:\\androidwork\\gtgj_main\\app\\src\\main\\java\\com\\gtgj\\utility\\dfp\\DfpGenUtils1.java",'w')
print(rs)
for line in f:
    t = line
    for z in rs:
        t = t.replace(z,  " " +rs[z])
        print(z, rs[z])
    fp.write(t)
    
fp.close()