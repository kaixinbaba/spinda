import ast

if __name__ == '__main__':
    m = open('/Users/junjiexun/PycharmProjects/spinda/spinda/spinda.py').read()

    p = ast.parse(m)
    print(dir(p))
    for b in p.body:
        # print(dir(b))
        # print(b)
        # print(type(b))
        if isinstance(b, ast.ClassDef) and b.name == 'SourceObjectSummary':
        # if isinstance(b, ast.ClassDef) and b.name == 'Summary':
            print(b.__dict__)
            print(b.name)
            for base in b.bases:
                print(type(base))
                print(base.__dict__)
                print(base.id)
            # if hasattr(b, 'names'):
            #     print(b.names)
            # if hasattr(b, 'name'):
            #     print(b.name)
            # if hasattr(b, 'keywords'):
            #     print(b.keywords)
