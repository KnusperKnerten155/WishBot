
#lvl1 = "perms", "lvl1"
lvl1 = "mystic", "valor", "instinct" #


def get (memb):
    lvl = [0]
    for r in memb.roles:
        
        if r.name in lvl1:
            lvl.append(1)
            
    print(lvl, max(lvl))
    return max(lvl)
    

def check(memb, lvl):
    return get(memb) <= lvl
