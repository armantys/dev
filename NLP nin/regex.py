import re

#define a simple pattern

pattern = r'\b\d\d[A-Z]\b'# on recherche 
pattern2 = r'\d+[A-Z]'#example : matches one or more digits
regex_object = re.compile(pattern2)


#simple text
text = 'This is my adress : Angle street no 564B and my parents adress is Bananas street 11C'

#Using re.searching() with the pre-compiled regex object
match = regex_object.search(text)
match2 = regex_object.findall(text)
if match:
    print('pattern found', match2)
else:
    print('pattern not found')


#simple text


pattern3 = r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}'#example : matches one or more digits
regex_object = re.compile(pattern3)

text2 = 'This is my personal email@google.com and this is my office email alice22@abc.com'

#Using re.searching() with the pre-compiled regex object

match3 = regex_object.findall(text2)

if match3:
    print('pattern found', match3)
else:
    print('pattern not found')


pattern4 = r'\+[0-9\s\-]+.'#example : matches one or more digits
regex_object = re.compile(pattern4)

text3 = 'the following are the phone numbers of 3 students in a class, Michael : +234-123-456-7890, James : +234 100 000 1000, Sarah : +2349999999999'

#Using re.searching() with the pre-compiled regex object

match4 = regex_object.findall(text3)

if match3:
    print('pattern found', match4)
else:
    print('pattern not found')