#!/usr/bin/env python
# coding: utf-8

# In[18]:


import requests


# In[19]:


import re


# In[20]:


from bs4 import BeautifulSoup as bsup


# In[28]:


taken = requests.get('https://novelfull.com/warriors-promise.html')


# In[29]:


html = bsup(taken.text, 'html.parser')
html


# In[30]:


bottom_bar = html.find_all('a',{'data-page': re.compile('[0-8]')})
bottom_bar


# In[34]:


last_page =  int(bottom_bar[-1].get('data-page'))+1
print(f'So there are total {last_page} pages that contain chapter names')


# In[79]:


def scraping(name = 'WARRIOR’S PROMISE', start_page=1, stop_page=1):
    name = name.lower().replace(' ','-')
    ls_chapters_inpg = []
    all_span = []
    chap_content = {}
    para = {}
    html_content = {}
    print(f'book title: {name}\nfrom web_page({start_page})\nlisting all chapters name\n\n')
    
    for pg_no in range(start_page, stop_page +1):
        taken = requests.get(f'http://novelfull.com/index.html/{name}.html?page={pg_no}&per-page = 50')
        html = bsup(taken.text,'html.parser')
        html
        
        no_ul = html.find_all('ul')
        
        for ul in no_ul:
            ls_of_span = ul.find_all('span')
            all_span.extend(ls_of_span)
            
            for span in ls_of_span:
                print(span.text)
                ls_chapters_inpg.append(span.text)
                
                
                all_anchors = ul.find_all('a')
                for anchor in all_anchors:
                    if anchor.text == ls_chapters_inpg[-1]:
                        a = anchor
                
                link = 'http://novelfull.com'+ a.get('href')
                print('Link ', link)
                
                taken = requests.get(link)
                html = bsup(taken.text, 'html.parser')
                
                all_para_of_a_chap = html.find_all('p')
                
                if '\xa0' in span.text:
                    title = span.text[:-1]
                    print('yes oops')
                else:
                    title = span.text
                para[f'{title}'] = all_para_of_a_chap
                html_content[f'{title}'] = html
    
    document= {}
    for chapter, paragraph in para.items():
        txt = ''
        for each in para[chapter][:-1]:
            txt += each.get_text() + '\n\n'
        document[chapter] = txt
    ls_chapters_inpg = [key for key in document.keys()]
    
    return document, ls_chapters_inpg


# In[80]:


document,ls_chapters_inpg = scraping()


# In[58]:


print(document['chapter-30'])


# In[ ]:




