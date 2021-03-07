import docx2txt
from concurrent.futures import ThreadPoolExecutor
import time
import os
import traceback
import textract




dest_PATH= './Bill_document_txt./'
src_PATH= './Bill_document/'
#print(os.listdir(src_PATH))
list= os.scandir(src_PATH)
#full_path= src_PATH+"bill_doc_101290.docx"
#my_text= textract.process(full_path)
#my_text = text.decode("utf-8")


for file in list :
    try:
        file=file.name
        if(file[-4] == ".zip"):
            continue
        #my_text = docx2txt.process(src_PATH+file)
        my_text = textract.process(src_PATH+file)
        my_text = my_text.decode("utf-8")
        my_text= my_text.replace('\n',' ')
        newfile=file[0:5]+ file[9:-5]+".txt"
        #txt = f.readlines()
        #txt = [x.strip() for x in txt]
        #txt = ' '.join(txt)
        f = open(dest_PATH+newfile, "w", encoding='utf-8')

        f.write(my_text)
        f.close()
    except Exception:
        traceback.print_exc()
        #print("this is expection")
        #continue


print("done")