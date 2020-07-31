import glob
from bs4 import BeautifulSoup
import multiprocessing
from time import perf_counter
import pyzipper


def main():
    t1_start = perf_counter()

    htGlob = glob.glob('./output*.html', recursive=True)

    print(htGlob)
    p = multiprocessing.Pool()
    for f in htGlob:
        p.apply_async(process, [f])
    p.close()
    p.join()

    # p.close()
    # p.join()
    #for ht in htGlob:
        #process(ht)
    
    with pyzipper.AESZipFile('backup.zip',
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(b'testpassword')

        for fi in htGlob:
            print(fi[2:])
            zf.writestr(fi[2:], open(fi, 'rb').read())

    
    t1_end = perf_counter()
    print(f'Time elapsed: {t1_end - t1_start}')


def process(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, features='lxml')

    anchors = soup.findAll('a')

    with open(str(filename).split('.html')[0] + '.txt', 'w') as o:

        for a in anchors:
            
            href = a.get('href')
            st = f'"{a.text}" : "{href}",'
            o.write(st)


if __name__ == '__main__':
    main()
    