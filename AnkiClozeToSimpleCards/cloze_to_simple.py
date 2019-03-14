sample_text = '{{c1::AAA}} - bbb c {{c2::dsadsa}} dasdasdasd {{c2::ddddddd}} ddsadasdsa {{c3::dasdsadasd}} dddd {{c4::dasdsadasd}}'

import re

pattern = '[c0-9]'

x = re.findall(pattern, sample_text)
# remove extraneous leading 'c'
x = [int(i) for i in x if i!='c']
max_cloze_num = max(x)

print(x)
print(max_cloze_num)

refined_text = ''

for word in sample_text.split(' '):
    word = word.strip('{').strip('}')
    refined_text += word + ' '

# print(refined_text)