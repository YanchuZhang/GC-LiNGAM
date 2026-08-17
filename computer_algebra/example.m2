load("methods.m2");

-- Testing model equivalence of two graphs
n = 3;

edg1 = {(1,2),(2,3)};
b1 = {(2,3)};

-- equivalent models
edg2 = {(1,2),(1,3),(2,3)};
b2 = {(2,3)};

checkEquivalence(n, edg1, edg2, b1, b2)

-- non-equivalent models
edg3 = {(1,2),(3,2)};
b3 = {(2,3)};

checkEquivalence(n, edg1, edg3, b1, b3)



-- Equivalence class of the following ADMG
n = 3;
edg1 = {(1,2),(2,3)};
b1 = {(2,3)};
eqclass = findEqGraphs(n,edg1,b1);

for e in eqclass do(
     print(e);
     );


-- Equivalence class of the following DMG (cyclic)
n = 3;
edg1 = {(1,2),(2,3)};
b1 = {(2,3)};
eqclass = findEqGraphsCyc(n,edg1,b1);

for e in eqclass do(
     print(e);
     );
