def calculate_score_golf(rolls, a=sum, b=range):
    return (lambda f:a(f[:20])+a(f[i+2]*((f[i]+f[i+1])==10)+f[i+4-(f[i+2]!=10)]*(f[i]==10)for i in b(0,20,2)))((
        lambda s:[10 if s[i]=='X'else((10-int(s[i-1]))if s[i]=='/'else int(s[i]))for i in b(24)])([c if c!='-'else 0
            for c in rolls.replace('X','X-')if c!=' ']+[0]*24))
