import os




bad_words_remove_line = ['Wikisource']          # remove lines containing this words and continue parsing
stop_words = ['בוויקיטקסט']                     # after these word , we stop parseing completly
for filename in os.listdir("C:/Users/jovaj/Desktop/SPL/XMLtoCSV/Israel_Law/"):
    temp= 'Israel_Law_post_parse/'+filename
    with open('Israel_Law/'+filename,encoding='utf-8') as oldfile, open(temp, 'x',encoding='utf-8') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words_remove_line):
                if any(stop_word in line for stop_word in stop_words):
                    break
                newfile.write(line)