import datetime
import random
import string

import mysql.connector

import models

conn = mysql.connector.connect(host='127.0.0.1',
                               user='root',
                               password='',
                               database='attendence_system')


def get_teacher(teach_id: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from teacher_table where teach_id = {teach_id}")
    for row in cursor:
        return (row)


def get_teacher_by_email(email):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from teacher_table where teach_email_id = '{email}'")
    data = cursor.fetchone()
    if data is not None:
        return data
    return False


def register_teacher(teacher: models.Teacher):
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"INSERT INTO teacher_table "
            f"VALUES ('a','{teacher.teach_name}','{teacher.teach_email_id}','{teacher.teach_phone_no}',"
            f"'{teacher.teach_password}','{teacher.teach_institution_code}')")
        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        return ex


def verify_teacher(user: models.TeacherInfo):
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT * FROM teacher_table WHERE teach_email_id = '{user.teach_email_id}' AND teach_password = '{user.teach_password}'"
    )
    data = cursor.fetchone()

    if data:

        return data
    else:
        return False


def get_student_by_email(email: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM student_table WHERE stud_email_id = '{email}'")
    data = cursor.fetchone()
    if data:
        return data

    return False


def register_student(stud: models.Student):
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO student_table (stud_id, stud_roll_no, stud_name, stud_email_id, "
                       f"stud_phone_no, stud_password, stud_institute_code) VALUES ('{stud.stud_roll_no}', '{stud.stud_roll_no}', '{stud.stud_name}', '{stud.stud_email_id}', "
                       f"'{stud.stud_phone_no}', '{stud.stud_password}', '{stud.stud_institute_code}')")
        conn.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def get_student(id: int):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * from student_table where stud_id = {id}")
    for row in cursor:
        return row
    pass


def verify_student(user: models.StudentInfo):
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM student_table WHERE stud_email_id = '{user.stud_email_id}' AND stud_password = '{user.stud_password}'"
    )
    data = cursor.fetchone()
    print(data)

    if data:

        return data
    else:
        return False


def join_student_class(data:models.EnrollInfo):
    cursor = conn.cursor()
    cursor.execute(f"Select * from class_table where class_id='{data.class_id}'")
    result = cursor.fetchone()
    if result:
        try:
            cursor.execute(f"INSERT INTO `class_enroll_table`(`enroll_id`, `class_id`, `stud_id`) VALUES ('1','{data.class_id}','{data.stud_id}')")
            conn.commit()
            return {'status':True,'detail':'join successful'}
        except Exception as e:
            return {'status':False,'detail':f'failed to join class {e}'}
    else:
        return {'status': False, 'message': 'Class id Does not Exits'}
    pass


# teacher
def get_enroll_student(class_id):
    curses = conn.cursor()
    curses.execute(
        f"SELECT stud_roll_no,stud_name,stud_email_id,stud_phone_no,stud_id from student_table WHERE stud_id in (SELECT stud_id FROM class_enroll_table WHERE class_id = '{class_id}');"
    )
    data = []
    for i in curses:
        print(i)
        data.append(i)

    return data



def get_enroll_classes(stud_id):
    curses = conn.cursor()
    curses.execute(
        f"SELECT c.class_id,c.class_name,c.class_subject,c.class_theme,t.teach_id,t.teach_name FROM class_table AS c,teacher_table as t WHERE c.class_id in (SELECT class_id from class_enroll_table WHERE stud_id = '{stud_id}') and t.teach_id = c.teach_id; "
    )
    data =[]
    for i in curses:
        data.append(i)

    return data





def verify_enroll_student_status(enrollData: models.EnrollInfo):
    cursor = conn.cursor()
    cursor.execute(
        f"select * from class_enroll_table where class_id = '{enrollData.class_id}' AND stud_id = '{enrollData.stud_id}'")
    result = cursor.fetchall()
    if (not result):
        return True
    else:
        return False



def create_class(data: models.ClassInfo):
    cursor = conn.cursor()
    print(datetime.date.today().strftime('%d-%m-%Y'))
    try:
        print(f"INSERT INTO `class_table` (`class_id`, `class_name`, `class_subject`, `class_created_date`, "
                       f"`class_theme`, `teach_id`) VALUES ('oo', '{data.class_name}', '{data.class_subject}', '{datetime.date.today().strftime('%d-%m-%Y')}', '{data.class_theme}', '{data.teach_id}');")
        cursor.execute(f"INSERT INTO `class_table` (`class_id`, `class_name`, `class_subject`, `class_created_date`, "
                       f"`class_theme`, `teach_id`) VALUES ('oo', '{data.class_name}', '{data.class_subject}', STR_TO_DATE('{datetime.date.today().strftime('%d-%m-%Y')}', '%d-%m-%Y'), '{data.class_theme}', '{data.teach_id}');")
        conn.commit()
        return {'status': True, 'messesge': 'successfull'}

    except Exception as e:
        print(e)
        return {'status': False, 'messesge': e}


def get_classes(teach_id: str):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * from class_table where teach_id = '{teach_id}'")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        pass

def get_no_of_student(class_id):
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT count(*) FROM `class_enroll_table` WHERE class_id = '{class_id}'")
        data = cursor.fetchone()
        return str(data[0])
    except Exception as e:
        pass

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def create_qr_hash(teach_id,class_id):
    cursor = conn.cursor()
    try:
        hashValue = generate_random_string(15)
        cursor.execute(f"INSERT INTO `session_table`(`session_id`, `teach_id`, `class_id`, `qr_hash`, `date`, `session_status`) VALUES "
                       f"('1','{teach_id}','{class_id}','{hashValue}',STR_TO_DATE('{datetime.date.today().strftime('%d-%m-%Y')}', '%d-%m-%Y'),'active')")
        conn.commit()
        cursor.execute(f"SELECT session_id FROM session_table WHERE teach_id = '{teach_id}' AND class_id = '{class_id}' AND qr_hash = '{hashValue}'")
        session_id = cursor.fetchone()[0]
        return session_id,hashValue

    except Exception as e:
        print(e)

def deactive_session(session_id):
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE `session_table` SET `session_status` = 'deactive' WHERE `session_table`.`session_id` = '{session_id}';")
        conn.commit()
    except Exception as e:
        print(e)


def verify_session_status(session_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `session_table` WHERE `session_id`='{session_id}' AND `session_status`='active';")
    data = cursor.fetchone()
    if(data):
        return True
    else:
        return False

def verify_attendance_status(data:models.AttendanceModel):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM `attendance_table` WHERE session_id= '{data.session_id}' AND class_id='{data.class_id}' AND stud_id='{data.stud_id}';")
    result = cursor.fetchone()
    if not result:
        return True
    else:
        return False

def marks_student_attendance(data:models.AttendanceModel):
    enrolldata = models.EnrollInfo
    enrolldata.class_id = data.class_id
    enrolldata.stud_id = data.stud_id

    result =verify_enroll_student_status(enrolldata)
    sessionStatus = verify_session_status(data.session_id)
    attenVerify = verify_attendance_status(data)
    if (not result):
        if attenVerify:

            if sessionStatus:
                cursor=conn.cursor()
                cursor.execute(f"INSERT INTO `attendance_table`(`session_id`, `class_id`, `stud_id`) VALUES ('{data.session_id}','{data.class_id}','{data.stud_id}')")
                conn.commit()
                return {'status': True, 'details': 'Attendance Mark'}
            else:
                return {'status': False, 'details': 'Session Deactivate'}
        else:
            return {'status': False, 'details': 'Attendance Already Mark'}

    else:
        return {'status':False,'details':'User Not Join the Class'}


def get_attendance_records(class_id):
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT session_id ,class_id,date FROM `session_table` WHERE class_id = '{class_id}';")
    result = cursor.fetchall()
    dataList = []
    for i in result:
        model = models.Attendance()
        model.date = str(i[2])
        model.present = str(get_present_students(i[0]))
        model.absents = str(int(get_no_of_student(i[1]))-int(get_present_students(i[0])))
        dataList.append(model)


    return dataList


def get_present_students(session_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM `attendance_table` WHERE session_id='{session_id}'")
    return cursor.fetchone()[0]


def get_student_attendance(class_id,stud_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM `attendance_table` WHERE class_id = '{class_id}' AND stud_id = '{stud_id}'")
    present = cursor.fetchone()[0]
    cursor.execute(f"SELECT count(*) FROM `session_table` WHERE class_id = '{class_id}'")
    total = cursor.fetchone()[0]

    return (present/total)*100

def get_student_attendance_detail(class_id,stud_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT count(*) FROM `attendance_table` WHERE class_id = '{class_id}' AND stud_id = '{stud_id}'")
    present = cursor.fetchone()[0]
    cursor.execute(f"SELECT count(*) FROM `session_table` WHERE class_id = '{class_id}'")
    total = cursor.fetchone()[0]

    return {"present":str(present),"absent":str(total-present),"total":str(total)}


if __name__ == '__main__':
    teacher = models.Teacher
    teacher.teach_name = 'Soham'
    teacher.teach_email_id = 'soham@gmail.com'
    teacher.teach_phone_no = '9527013655'
    teacher.teach_password = '1234'
    teacher.teach_institution_code = '123'

    student = models.Student
    student.stud_name = 'Soham'
    student.stud_email_id = "soham@gmail.com"
    student.stud_phone_no = '9527013655'
    student.stud_password = '98563'
    student.stud_institute_code = '99535'

    classes = models.ClassInfo
    classes.teach_id = 'teach_240472'
    classes.class_name = 'SE-11'
    classes.class_theme = 'ad'
    classes.class_subject = 'DBMS'

    # enrolldata = models.EnrollInfo
    # enrolldata.class_id = 'class_152601'
    # enrolldata.stud_id = 'stud_392012'

    # print()
    # print(register_teacher(teacher))
    # print(get_classes(classes.teach_id)
    # print(create_class(classes))
    # print(get_enroll_classes('stud_105891'))
    # print(join_student_class(enrolldata))
    # get_no_of_student('class_943140')

    atte = models.AttendanceModel
    atte.stud_id='stud_105891'
    atte.class_id='class_701011'
    atte.session_id='session_77308'
    # print(create_qr_hash('teach_240472','class_952351'))
    # print(marks_student_attendance(atte))
    # get_attendance_records("class_701011")
    # print(verify_enroll_student_status(enrollData=enrolldata))
    print(get_attendance_records("class_701011"))
    print(get_student_attendance("class_701011","stud_105891"))


