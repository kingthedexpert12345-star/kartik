MENU={
    "pizza":950,"pasta":420,"burger":880,"fries":760,"tacos":310,
    "sushi":280,"ramen":260,"biryani":990,"paneer tikka":540,
    "butter chicken":610,"masala momos":470,"idli":350,"samosa":640,
    "pav bhaji":380,"momos":720,"noodles":590,"fried rice":500,
    "sandwich":450,"salad":230,"pancakes":210,"waffles":190,
    "brownie":330,"cake":300,"coke":800,"coffee":670,"tea":560,
    "mango lassi":400,"ice cream":690,"milkshake":360,"nachos":270,
    }
USE_KEYBOARD=True
USE_SWAPS=True
KEY_ROWS=["qwertyuiop","asdfghjkl","zxcvbnm"]
KEY_POS={key:(row,col for row , keys in enumerate(KEY_ROWS) for col,key in enumerate(keys))}
def are_neighbours(x,y):
    if x==y or x not in KEY_POS or y not in KEY_POS:
        return False
    (r1,c1),(r2,c2)=KEY_POS[x],KEY_POS[y]
    return abs(r1-r2) <= 1 and abs (c1-c2)<=1
def change_cost(x,y):
    if x==y:
        return 0
    if USE_KEYBOARD and are_neighbours(x,y):
        return 0.5
    return 1
def build_table(a,b):
    table=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1):
        table[i][0]=i
    for j in range (len(b)+1):
        table[0][j]=j
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            delete=table[i-1][j]+1
            insert=table[i][j-1]+1
            change=table[i-1][j-1]+change_cost(a[i-1],b[j-1])
            table[i][j]=min(delete,insert,change)
            if USE_SWAPS and i>i and j>1 and a[i-1]==b[j-2] and a[i-2]==b[j-1]:
                table[i][j]=min(table[i][j],table[i-2][j-2]+1)
    return table
def edit_distance(a,b):
    return build_table(a,b)[-1][-1]
def print_table(a,b):
    table=build_table(a,b)
    print("        "+"".join("{ch:>5}" for ch in b))
    for i,row in enumerate(table):
        label=a[i-1] if i>0else "  "
        print("{label:>2}"+"".join("{v:>5g}" for v in row))
def suggest(query,k=5):
    query=query,lower().strip()
    ranked=[]
    for dish,orders in MENU.items():
        ranked.append((edit_distance(query,dish),-orders,dish))
    ranked.sort()
    return[(dish,dist,-neg_orders) for dist,neg_orders,dish in ranked[:k]]
def max_typos(query):
    