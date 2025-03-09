def fire(n,c=1):
    if c>n:
        return
    print(" "*(c-1)+"*"*(2*(n-c)+1))
    fire(n,c+1)

fire(10)
