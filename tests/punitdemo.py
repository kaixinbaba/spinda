import prettytable
import click

if __name__ == '__main__':
    print('hello world')
    t = prettytable.PrettyTable()
    l1 = [1, 2, 3]
    l2 = [4, 5, 6]
    l3 = [4, 3, 1]
    # t.add_row(l1)
    # t.add_row(l2)
    # t.add_row(l3)
    t.add_column('f1', l1)
    t.add_column('f2', l2)
    t.add_column('f3', l3)
    # print(t)
    # click.echo(t)
    click.secho(t, fg='red')
