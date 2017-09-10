from http.server import HTTPServer, SimpleHTTPRequestHandler, test as test_orig
import threading
import time
import sys
import os
import xlrd
import simplejson as json


class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers(self):
        print(self)
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


def test(*args):
    test_orig(*args, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
    print("server running properly")


def con():
    # Open the workbook and select the first worksheet
    wb = xlrd.open_workbook('./puthere/myfile.xlsx')
    sh = wb.sheet_by_index(0)



    # List to hold dictionaries
    output = {}
    # Iterate through each row in worksheet and fetch values into dict
    for rownum in range(1, sh.nrows):
        row = sh.row_values(rownum)
        col = sh.row_values(0)
        for i, x in enumerate(row):
            try:
                row[i] = int(x)
            except ValueError:
                pass

        if (row[0] != ""):
          boss = row[0]
          output.update(
            {row[0]: {row[1]: dict(zip(col[2:], row[2:]))}})
        else:
          output[boss].update({row[1]: dict(zip(col[2:], row[2:]))})

    # Serialize the list of dicts to JSON
    j = json.dumps(output)

    # Write to file
    with open('data.json', 'w') as f:
        f.write(j)


class mythread1(threading.Thread):
    def run(self):
        print("thread one called")
        test(CORSRequestHandler, HTTPServer)


class mythread2(threading.Thread):
    def run(self):
        con()
        print("file changer  is running")
        i = os.path.getmtime('./puthere/myfile.xlsx')
        while(True):
            if i != os.path.getmtime('./puthere/myfile.xlsx'):
                con()
                i = os.path.getmtime('./puthere/myfile.xlsx')
                print("the file has changed")
            time.sleep(1)


if __name__ == '__main__':
    d = mythread1()
    e = mythread2()
    d.start()
    e.start()

