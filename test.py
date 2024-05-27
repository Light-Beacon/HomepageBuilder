from Core.IO.scanner import Dire,File

#print(str(File('/Users/morgan/Documents/Gits/PCL2-NewsHomepage/Pages/1.17存档.xaml')))
for f in Dire('/Users/morgan/Documents/Gits/PCL2-NewsHomepage/Libraries/Homepage').scan(r'.*\.xaml$',recur=True,min_recur_deepth=1):
    print(str(f))
