f = open("rd.txt", "r")
vertices=[]
surfaces=[]
for line in f:
    if line.startswith("v"):
        l = line.replace("v", "")
        l = l.strip()
        res = list(map(float, l.split(" ")))
        vertices.append(res)
    if line.startswith("f"):
        l = line.replace("f", "")
        l = l.strip()
        slash = list(map(str, l.split(" ")))
        res=[]
        for s in slash:
            r = s.split("/")
            res.append(int(r[0]))
        surfaces.append(res)

fw = open("dandn.txt", "w")

for face in surfaces:
    fw.write("f " + str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + "\n")
fw.close()

