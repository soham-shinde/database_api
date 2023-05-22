from typing import Optional, List

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette import status

import curd
import models

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'successfully'}


@app.post('/api/teacher/register', status_code=status.HTTP_201_CREATED)
def register_teacher(teacher: Optional[models.Teacher] = None):
    print(curd.get_teacher_by_email(teacher.teach_email_id))
    if curd.get_teacher_by_email(teacher.teach_email_id):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Already Register")
    elif curd.register_teacher(teacher):
        return {"message": "user created"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error while to creating the user')


@app.post("/api/teacher/authorise", status_code=status.HTTP_200_OK)
def authorise_teacher(teacher: Optional[models.TeacherInfo] = None):
    data = curd.verify_teacher(teacher)
    if data:
        return {
            "teach_id": data[0],
            "teach_name": data[1],
            "teach_email_id": data[2],
            "teach_phone_no": data[3],
            "teach_password": data[4],
            "teach_institution_code": data[5]
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error user Not found')


@app.post("/api/teacher/classes/create")
def create_class(classesdata: models.ClassInfo):
    data = curd.create_class(classesdata)
    if data['status']:
        return {'message': "Class Create Successfully"}

    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=data)
    pass


@app.get("/api/teacher/classes/{teach_id}")
async def get_classes(teach_id):
    print(teach_id)
    a = curd.get_classes(teach_id)
    my_list = []
    for i in a:
        row = models.Classes()
        row.class_id = i[0]
        row.class_name = i[1]
        row.class_subject = i[2]
        row.class_created_date = i[3]
        row.class_theme = i[4]
        row.class_no_of_student = str(curd.get_no_of_student(i[0]))
        row.teach_id = i[5]
        my_list.append(row)

    return my_list


@app.get('/api/teacher/classes/student/{class_id}')
def get_classes_student(class_id):
    data = curd.get_enroll_student(class_id)
    dataList = []
    for i in data:
        studData = models.Students()
        studData.stud_roll_no = i[0]
        studData.stud_name = i[1]
        studData.stud_email_id = i[2]
        studData.stud_phone_no = i[3]
        studData.stud_id = i[4]
        studData.stud_attendance = str(curd.get_student_attendance(class_id,i[4]))
        dataList.append(studData)

    return dataList


@app.post('/api/student/register', status_code=status.HTTP_201_CREATED)
def register_student(student: Optional[models.Student] = None):
    if curd.get_student_by_email(student.stud_email_id):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email Already Register")
    elif curd.register_student(student):
        return {"message": "user created"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error while to creating the user')


@app.post("/api/student/authorise", status_code=status.HTTP_200_OK)
def authorise_student(student: Optional[models.StudentInfo] = None):
    print(student)
    data = curd.verify_student(student)
    if data:
        return {
            "stud_id": data[0],
            "stud_roll_no": data[1],
            "stud_name": data[2],
            "stud_email_id": data[3],
            "stud_phone_no": data[4],
            "stud_password": data[5],
            "stud_institution_code": data[6]
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error user Not found')


@app.post("/api/student/classes/join")
async def join_class(classesdata: models.EnrollInfo):
    result = curd.verify_enroll_student_status(classesdata)
    if result:
        data = curd.join_student_class(classesdata)

        if data['status']:
            return data
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=data)
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="already enroll")
    pass


@app.get("/api/student/classes/{stud_id}")
def get_student_class(stud_id):
    data = curd.get_enroll_classes(stud_id)
    dataList = []
    for i in data:
        classData = models.Classes()
        classData.class_id = i[0]
        classData.class_name = i[1]
        classData.class_subject = i[2]
        classData.class_theme = i[3]
        classData.teach_id = i[4]
        classData.teach_name = i[5]
        classData.attendance = str(curd.get_student_attendance(i[0],stud_id))
        dataList.append(classData)

    return dataList

@app.get("/api/student/classes/attent/{class_id}/{stud_id}")
def get_student_class(class_id,stud_id):
    data = curd.get_student_attendance_detail(class_id,stud_id)
    print(data)
    return data

@app.get("/api/teacher/class/{teach_id}/session/{class_id}")
def create_session(teach_id, class_id):
    session_id, hashValue = curd.create_qr_hash(teach_id, class_id)
    return {'teach_id': teach_id, 'class_id': class_id, 'session_id': session_id, 'qr_hash': hashValue}


@app.get("/api/teacher/class/session/{session_id}")
def deactivate_session(session_id):
    curd.deactive_session(session_id)
    return {'message': 'successful'}


@app.get("/api/teacher/class/attendance/{class_id}")
def get_attendance_class(class_id):
    data = curd.get_attendance_records(class_id)
    return data


@app.post("/api/teacher/class/session/attendance")
def mark_attendance(data: models.AttendanceModel):
    result = curd.marks_student_attendance(data)
    if result['status']:
        return {'message': 'successful'}
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=result['details'])


if __name__ == '__main__':
    # pass
    uvicorn.run("main:app", host='0.0.0.0', port=3000, reload=True)  #
