import cvxpy as cp
import pandas as pd

constraints = []
Beta = [0.2,0.5,0]
Eta = [0.2,0.6,0]
Gamma = 0.9
H = 10
g = 9.8
rho = 1000
cUTmax = 10
j=0


df = pd.DataFrame()
df = pd.read_csv('demanddata.csv')      #read demand data
df = df.multiply(100)



fT = {                                   #define decision variable (fT)
    (k,j,t): cp.Variable(
        name="x({},{},{})".format(k,j,t)
    )
    for k in range(3)
    for j in range(3)
    for t in range(24)
}

fF = {                                   #define decision variable (fF)
    (j,t): cp.Variable(
        name="x({},{})".format(j,t)
    )
    for j in range(3)
    for t in range(24)
}

fB = {                                   #define decision variable (fB)
    (j,i,t): cp.Variable(
        name="x({},{},{})".format(j,i,t)
    )
    for j in range(3)
    for i in range(3)
    for t in range(24)
}

pP = {                                   #define decision variable (pP)
    (k,j,t): cp.Variable(
        name="x({},{},{})".format(k,j,t)
    )
    for k in range(3)
    for j in range(3)
    for t in range(24)
}


vF = {                                   #define decision variable (fF)
    (k,t): cp.Variable(
        name="x({},{})".format(k,t)
    )
    for k in range(1)
    for t in range(24)
}


cUT = {                                   #define decision variable (cUT)
    (k,t): cp.Variable(
        name="x({},{})".format(k,t)
    )
    for k in range(3)
    for t in range(24)
}
cOT = {                                   #define decision variable (cOT)
    (j,t): cp.Variable(
        name="x({},{})".format(j,t)
    )
    for j in range(3)
    for t in range(24)
}

cost = 0


for t in range(24):
    cost = cost + vF[0,t]

obj = cp.Minimize(cost)


for i in range(3):                      #constraint 1
    for t in range(24):
        constraints += [
            fB[0,i,t] + fB[1,i,t] + fB[2,i,t] >= df[str(i+1)][t],
    ]

for t in range(24):                     #constraint 2
    constraints += [
      vF[0,t] >=0,
      ]

for j in range(3):
    for i in range(3):                   #constraint 3
        for t in range(24):
            constraints += [
                fB[j,i,t]  >= 0,
                fT[i,j,t]  >= 0,
                pP[j,i,t]  >= 0,
                fT[j,i,t]  >= 0,
    ]

for k in range(2):                      #constraint 4
    if k == 0:
        j = 1
    if k == 1:
        j = 2
    for t in range(24):
        constraints += [
            cUT[k,t] == cUT[k,((t-1)%24)] + Beta[k]*Eta[k]*df[str(k+1)][t] - fT[k,j,t] ,
    ]

for k in range(2):                        #constraint 5
    for t in range(24):
        constraints += [
            cUT[k,t] <= cUTmax, cUT[k,t] >=0,
            cOT[k,t] <= cUTmax, cOT[k,t] >=0,
    ]

    for t in range(24):                 #constraint 6
        k = 2
        j = 0
        constraints += [
            cUT[k,t] == cUT[k,((t-1)%24)] + vF[0,t] - fF[j,t] ,
    ]

for k in range(3):                      #constraint 7
    if k == 0:
        j = 1
    if k == 1:
        j = 2
    if k == 2:
        j = 0
    for t in range(24):
        constraints += [
            (pP[k,j,t]*Gamma)/(Beta[k]*Eta[k]*df[str(k+1)][t]*g*rho*H) <= fT[k,j,t]/1000,
    ]
for j in range(3):                            #constraint 8
    for t in range(24):
        constraints += [
            cOT[k,t] == cOT[k,((t-1)%24)] + fT[0,j,t] + fT[1,j,t] + fT[2,j,t] + fF[j,t] - fB[j,0,t]- fB[j,1,t]-fB[j,2,t],
    ]



prob=cp.Problem(obj,constraints)
prob.solve()
print("optimal value", prob.value)

#for j in range(3):
for i in range(3):
    for t in range(24):
        print(fB[0,i,t].value + fB[1,i,t].value + fB[2,i,t].value)
