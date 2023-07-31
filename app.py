# from crypt import methods
from secrets import choice
from flask import Flask , render_template ,request
import mysql.connector
from soupsieve import select
from tables import Description
from datetime import date


#  link to data base internal medicine
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Osamah3333#",
  database="internal_medicine"
)

app=Flask(__name__)
mycursor = mydb.cursor()





#  main window 
@app.route("/")
def Home():
    return render_template("Home.html")


           


#  signin window
    

@app.route("/signin" , methods =['POST','GET'])
def signin():
    dataConfarm=[]
    dirict =0
    dataSend=[]
    #  if clicked on submet in the signin
    if request.method =='POST':
         emailR=request.form['Email']
         passwordR=request.form['password']
         
         x="select Email , pass ,flag from account where  "
         e=" Email="+"'"+emailR+"'"
         p=" and  pass="+"'"+passwordR+"'"
         

         mycursor.execute(x+e+p)
         for x in mycursor:
             dirict =1
             dataConfarm.extend(x)
             
         if dirict == 0 :
            return render_template("signin.html")
          
         else:

          #   if admin 
          if (dataConfarm[0]==emailR and dataConfarm[1]==passwordR and dataConfarm[2]=='admin'):
              x="select AdminID , Fname ,Email ,gender,birthdate from admin where Email="
              y="'"+emailR+"'"
              mycursor.execute(x+y)
              for i in mycursor:
                dataSend.extend(i)
              return render_template ('admin.html' , dataSend=dataSend)

            # if patient
          elif (dataConfarm[0]==emailR and dataConfarm[1]==passwordR and dataConfarm[2]=='patient'):
              x="select PatID , Fname ,Email ,gender,birthdate from patient where Email="
              y="'"+emailR+"'"
              mycursor.execute(x+y)
              for i in mycursor:
                dataSend.extend(i)
              return render_template ('patient.html' , dataSend=dataSend)


               # if doctor
          elif (dataConfarm[0]==emailR and dataConfarm[1]==passwordR and dataConfarm[2]=='doctor'):
              dat=date.today()
              x="SELECT AppID, patient.Fname, patient.Lname, appointment.Description, appointment.Date FROM appointment join doctor on DocID = DocAppID join patient on PatID = PatAppID  where  appointment.Date is not NULL and appointment.Date >= "
              y="'"+str(dat)+"'" + "and doctor.email = " + "'" +emailR  + "'" 
              mycursor.execute(x + y)
              myresult = mycursor.fetchall()
              return  render_template ('doctor.html' , Appointments=myresult)
              
          else:
              return render_template ('signin.html')
    else:
        return render_template("signin.html")     

#  add docotor 
@app.route("/addDoctor", methods =['POST','GET'])
def addDoctor():
    if request.method =='POST':
      fname1=request.form['Fname']
      lname1=request.form['Lname']
      email1=request.form['Email']
      pass1=request.form['password']
      confPass1=request.form['confirmPassword']
      gender1=request.form['gender']
      brithdate1=request.form['Birthdate']
      ssn1=request.form['SSN']
    
      

      if (pass1 != confPass1):
        x="NOT MATCH PASSWORD"
        return render_template("addDoctor.html" , y=x )
      else:
            x=" "
            #  add  data of doctor's acount
            dataAcountD="insert into account (Email ,flag ,pass) values(%s ,%s,%s)"
            valuesAccountD=(email1 , 'doctor' ,pass1  )
            mycursor.execute( dataAcountD,valuesAccountD)
            mydb.commit()

            #  add data to doctor table
            dataDoctor="insert into doctor (Fname ,Lname ,gender,birthdate ,email,DSSN) values(%s ,%s,%s ,%s ,%s ,%s)"
            valuesDoctor=(fname1 ,lname1 ,gender1,brithdate1 ,email1, ssn1)
            print(valuesDoctor)
            mycursor.execute( dataDoctor,valuesDoctor)
            mydb.commit()
            return render_template("addDoctor.html" , y=x )
    else:
        return render_template("addDoctor.html")





#  view doctor 
  
@app.route("/viewDoctor" ,methods =['POST','GET'])
def viewDoctor():

    #  add from here 
    dat=date.today()
    x="SELECT AppID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname, appointment.Description, appointment.Date FROM appointment join doctor on DocID = DocAppID join patient on PatID = PatAppID  where Date >="
    y="'"+str(dat)+"'"
    mycursor.execute(x+y)
    # to here 
    myresult = mycursor.fetchall()
    return render_template("viewDoctor.html" ,dataSendViewDoctor=myresult )
   




#Approve Appointment  # Done
@app.route("/adminApproveAppointment" ,methods =['POST','GET'])
def Approve():
    if request.method =='POST':
      date=request.form['date']
      AppID=request.form['AppID']
      print(date , AppID)

      sql = "UPDATE  appointment SET Date=%s WHERE AppID = %s "
      val=(date , AppID)
      mycursor.execute(sql, val)
      mydb.commit()

      
      mycursor.execute("SELECT AppID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname, appointment.Description FROM appointment join doctor on DocID = DocAppID join patient on PatID = PatAppID  where Date IS NULL ")
      myresult = mycursor.fetchall()
      return render_template("adminApproveAppointment.html", Appointments = myresult )



    #  if not post
    else:

      mycursor.execute("SELECT AppID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname, appointment.Description FROM appointment join doctor on DocID = DocAppID join patient on PatID = PatAppID  where Date IS NULL ")
      myresult = mycursor.fetchall()
      return render_template("adminApproveAppointment.html", Appointments = myresult )



#signup window
# Done 
@app.route("/signup", methods =['POST','GET'])
def signup():
 if request.method =='POST':
      fname1=request.form['Fname']
      lname1=request.form['Lname']
      email1=request.form['Email']
      pass1=request.form['password']
      confPass1=request.form['confirmPassword']
      gender1=request.form['gender']
      brithdate1=request.form['Birthdate']
      ssn1=request.form['SSN']
    
      

      if (pass1 != confPass1):
        x="NOT MATCH PASSWORD"
        return render_template("signup.html" , messege=x )
      else:
            x=" "
            #  add  data of patient's acount
            patientAcountData="insert into account (Email ,flag ,pass) values(%s ,%s,%s)"
            patientAcounValues=(email1 , 'patient' ,pass1  )
            mycursor.execute( patientAcountData,patientAcounValues)
            mydb.commit()

            #  add data to patient table
            patientData="insert into patient (Fname ,Lname ,gender,birthdate ,email,PSSN) values(%s ,%s,%s ,%s ,%s ,%s)"
            patientValues=(fname1 ,lname1 ,gender1,brithdate1 ,email1, ssn1)
            print(patientValues)
            mycursor.execute( patientData,patientValues)
            mydb.commit()
            return render_template("signup.html" , messege=x )

 else:
       return render_template("signup.html")



#Select Appointment
#  Done
@app.route("/selectAppointment", methods =['POST','GET'])
def selectAppointment():
    mycursor.execute("SELECT DocId, Fname, Lname FROM doctor")

    myresult = mycursor.fetchall()

    if request.method =='POST':
       doctorID=request.form['selectDoctor']
       description = request.form['description']
       Email=request.form['Email']

       x = "SELECT PatID FROM patient where Email = "
       y = "'" + Email + "'"
       mycursor.execute(x+y)
       result = mycursor.fetchone()
       
      
       appointmentData = "insert into appointment (DocAppID, PatAppID, Description) values(%s, %s, %s)"
       appointmentValues = (doctorID, result[0], description) 
       mycursor.execute(appointmentData, appointmentValues)
       mydb.commit()

       return render_template("selectAppointment.html")



    else:

      return render_template("selectAppointment.html", choice = myresult)



#view appointment
# Done
@app.route("/viewAppointPatient" , methods =['POST', 'GET' ])
def viewAppointPatient():

  if request.method=='POST':
    id= request.form['ID']
    id=int(id)
    if id<=0 :
      x=" Please Enter A Valid ID"
      return render_template("viewAppointPatient.html" , ERROR= x)

    else:
      sql="SELECT AppID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname,appointment.Date FROM appointment join doctor on DocID = DocAppID join patient on PatID = PatAppID  where PatID = "  + str(id )
      print ( sql)
      
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      print(myresult)
      return render_template("vieAppointPAtient2.html" , dataS = myresult )


  else:
    x=" "
    return render_template("viewAppointPatient.html" , ERROR= x)






# Patient View Reports
# Done
@app.route("/patientViewReports", methods=['POST','GET'])
def patientViewReports():

    if request.method =='POST':

      Email = request.form['Email']
      x = "SELECT RepID, aID, doctor.Fname, doctor.Lname, Result, Tests, Medicine, DateAndTime FROM report join doctor on DocID = dID join patient on PatID = pID  where patient.email = "
      y = "'" + Email + "'"

      mycursor.execute(x + y)
      myresult = mycursor.fetchall()
      return render_template("patientViewReports.html", Reports = myresult)

    else:
      return render_template("patientViewReports.html" ) 

# Write Report

@app.route("/writeReport", methods=['POST','GET'])

def writeReport():


  if request.method =='POST':
       appID = int (request.form['AppID'])
       result = request.form['Result']
       tests = request.form['Tests']
       medicine = request.form['Medicine']


       mycursor.execute("SELECT AppID from appointment where Date is not NULL ")
       approvedApp = mycursor.fetchall()
      
       for i in approvedApp:
         for j in i:
           if j == appID:
                

             x = "SELECT PatAppID, DocAppID from appointment where AppID =  "
             y = "'" + str(appID) + "'"
             mycursor.execute(x + y)
             data = mycursor.fetchone()

             patID = data[0]
             docID = data[1]
             DateAndTime = dt.datetime.now().replace(microsecond=0)
             
             reportData = "insert into report (aID, dID, pID, Result, Tests, Medicine, DateAndTime) values(%s, %s, %s, %s, %s, %s, %s)"
             reportValues = (appID, docID, patID, result, tests, medicine, DateAndTime) 
             mycursor.execute(reportData, reportValues)
             mydb.commit()
                      

             return render_template("writeReport.html")

           else:
             message="not exsist"

       return render_template("writeReport.html", Alert=message)
            

  else:
     return render_template("writeReport.html")


# Admin View Reports

@app.route("/viewReports", methods=['POST','GET'])

def viewReports():

    if request.method =='POST':

      repID = request.form['ReportID']


      x = "SELECT RepID, aID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname, Result, Tests, Medicine, DateAndTime FROM report join doctor on DocID = dID join patient on PatID = pID  where report.RepID = "
      y = "'" + repID + "'"

      mycursor.execute(x + y)
      myresult = mycursor.fetchall()
      
      print(myresult)



      return render_template("viewReports.html", Reports = myresult)


    else:

       
      mycursor.execute("SELECT RepID, aID, patient.Fname, patient.Lname, doctor.Fname, doctor.Lname, Result, Tests, Medicine, DateAndTime FROM report join doctor on DocID = dID join patient on PatID = pID ")
      myresult = mycursor.fetchall()
    
      
      

      return render_template("viewReports.html", Reports=myresult )



if __name__=="__main__":
    app.run(debug=True ,port=4000) 







