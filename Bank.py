import streamlit as st
import mysql.connector as msql

mydb=msql.connect(
    host='localhost',
    user='admin',
    password='admin',
    database='project'
)
# if mydb.is_connected(): #to check connected or not 
#     print('s')
# else:
#     print('nnnnnnnnnn')
# a=mydb.cursor()

st.header('WELCOME TO THE OLDMAN BANK')
menu=['select the option','Add New customer','Withdraw money','Deposit','Change Name','Change Password','Check Balance']
op=st.selectbox('Optins',menu)

def add_customer(name,phon,passw,balance):
    a=mydb.cursor()
    query = "INSERT INTO customer (cname, phon, passw, bal) VALUES (%s, %s, %s, %s)"
    values = (name, int(phon), passw, balance)
    a.execute(query,values)
    mydb.commit()
    st.success('customer added successfully')
    a.execute('select cid,cname,phon,passw,bal from customer where phon=%s and cname=%s', (phon,name))
    d=a.fetchall()
    st.write(f"""customer id :{d[0][0]} \t
                customer name:{d[0][1]}\t
                customer phon:{d[0][2]}\t
                customer passw:{d[0][3]}\t
                customer balance:{d[0][4]}""")
    
###################################################################################################################
if op=='Add New customer':
    name=st.text_input('Name :')
    phon = st.text_input('Phone', max_chars=10)
    password=st.text_input('password',type='password')
    balance=st.number_input('Balance',min_value=1000)

    # Ensure the phone number is exactly 10 digits
    if phon and len(phon) == 10 and phon.isdigit():
        st.success(f'Phone number is valid: {phon}')
    else:
        if phon:
            st.error('Phone number must be exactly 10 digits')
    if st.button('create'):
        add_customer(name,phon,password,balance)

elif op=='Withdraw money':
    cid=st.number_input('cid',min_value=0,format='%d')
    password=st.text_input('password',type='password')
    amount=st.number_input('enter amount',min_value=0,format='%d')
    if st.button('withdraw'):
        a=mydb.cursor()
        try:
            a.execute(f'select passw,bal from customer where cid={cid};')
            b=a.fetchall()
            if password==b[0][0]:
                if amount<=b[0][1]:
                    a.execute(f'update customer set bal=bal-{amount} where cid={cid}')
                    mydb.commit()
                    st.success('withdraw successfully')
                else:
                    st.error('insufficient balance.......')
        except:
            st.error('incorrect customer id.......')
elif op=='Deposit':
    cid=st.number_input('cid',min_value=0,format='%d')
    password=st.text_input('password',type='password')
    amount=st.number_input('enter amount',min_value=0,format='%d')
    if st.button('Deposit'):
        try:
            a=mydb.cursor()
            a.execute(f'select passw from customer where cid={cid} ')
            b=a.fetchall()
            if password==b[0][0]:
                a.execute(f'update customer set bal=bal+{amount} where cid={cid}')
                mydb.commit()
                st.success('withdraw successfully')
            else:
                st.error('incorrect password.......')
        except:
            st.error('incorrect customer id.......')


elif op=='Check Balance':
    cid=st.number_input('cid',min_value=0,format='%d')
    password=st.text_input('password',type='password')
    if st.button('check'):
        try:
            a=mydb.cursor()
            a.execute(f'select passw from customer where cid={cid} ')
            b=a.fetchall()
            if password==b[0][0]:
                a.execute(f'select bal from customer where cid={cid}')
                d=a.fetchall()
                st.success(f'your balance is {d[0][0]}')
            else:
                st.error('incorrect password......')
        except:
            st.error('incorrect customer id.......')

elif op=='Change Name':
    cid=st.number_input('cid',min_value=0,format='%d')
    password=st.text_input('password',type='password')
    name=st.text_input('enter new name : ')
    if st.button('change'):
        try:
            a=mydb.cursor()
            a.execute(f'select passw from customer where cid={cid}')
            b=a.fetchall()
            if password==b[0][0]:
                a.execute(f'update customer set cname= {name} where cid={cid}')
                mydb.commit()
                st.success('name changed successfully')
            else:
                st.error('incorrect password.............')
        except:
            st.error('incorrect cid ...........')


elif op=='Change Password':
    cid=st.number_input('cid',min_value=0,format='%d')
    password=st.text_input('old password',type='password')
    npassw=st.text_input('New password',type='password')
    if st.button('change..'):
        try:
            a=mydb.cursor()
            a.execute(f'select passw from customer where cid={cid}')
            b=a.fetchall()
            if password==b[0][0]:
                a.execute(f'update customer set passw= {npassw} where cid={cid}')
                mydb.commit()
                st.success('password changed successfully')
            else:
                st.error('incorrect password.............')
        except:
            st.error('incorrect cid ...........')