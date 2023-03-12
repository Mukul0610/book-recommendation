from flask import Flask,render_template,request
import pickle as pkl
import numpy as np
import pandas as pd
popolar_book=pkl.load(open('most-popular-book.pkl','rb'))
pv=pkl.load(open('pivot-tabel.pkl','rb'))
similarity=pkl.load(open('similarity.pkl','rb'))
df=pkl.load(open('books.pkl','rb'))
def recommendation(book_name):
    index=np.where(pv.index==book_name)[0][0]
    similar_book=sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    l = []
    for i in similar_book:
        l.append(pv.index[i[0]])
    return l

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',book=list(popolar_book['Book-Title'].values),
    author=list(popolar_book['Book-Author'].values),
    img=list(popolar_book['Image-URL-M'].values),
    rating = list(popolar_book['Book-Rating_y'].values))
@app.route('/Recommended')
def book():
    return render_template('Recommended Book.html')
@app.route('/Recommended_Book',methods=['post'])
def user():
    user_input=request.form.get('user_input')
    book_list=recommendation(user_input)
    new_df = df[df['Book-Title'].isin(book_list)]
    return render_template('Recommended Book.html',book=list(new_df['Book-Title'].values),
    author=list(new_df['Book-Author'].values),
    img=list(new_df['Image-URL-M'].values),
    rating = list(new_df['Book-Rating'].values))

if __name__=='__main__':
    app.run(debug=True)