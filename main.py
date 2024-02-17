from Core.Project import Project
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--open',help='Project path to be loaded')
    parser.add_argument('-w','--write',help='File path to be written')
    parser.add_argument('-p','--page',help='The name of page to be generated')
    parser.add_argument('--strict',help='Any waring will stop the program')
    args = parser.parse_args()
    project = None
    page = None
    if args.open:
        project = Project(args.open)
    else:
        return 0
    if args.page:
        page = args.page
    if args.write:
        xaml = project.get_page_xaml(page)
        filepath = args.write
        with open(filepath,'w',encoding='utf-8') as f:
            f.write(xaml)
            
if __name__ == '__main__':
    main()