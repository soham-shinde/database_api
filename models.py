from pydantic import BaseModel


class TeacherInfo(BaseModel):
    teach_email_id: str
    teach_password: str


class Teacher(TeacherInfo):
    teach_id: str
    teach_name: str
    teach_phone_no: str
    teach_institution_code: str

    class Config:
        orm_mode = True


class StudentInfo(BaseModel):
    stud_email_id: str
    stud_password: str


class Student(StudentInfo):
    stud_id: str
    stud_roll_no: str
    stud_name: str
    stud_phone_no: str
    stud_institute_code: str

    class Config:
        orm_mode = True


class ClassInfo(BaseModel):
    teach_id: str
    class_name: str
    class_subject: str
    class_theme: str

    class Config:
        orm_mode = True


class Classes:

    def __init__(self):
        print("sd")


class Students:

    def __init__(self):
        print("sa")


class ClassEnroll(BaseModel):
    enroll_id: str
    class_name: str
    class_subject: str
    class_theme: str
    class_teacher: str


class EnrollInfo(BaseModel):
    class_id: str
    stud_id: str

class AttendanceModel(BaseModel):
    session_id:str
    class_id:str
    stud_id:str

    class Config:
        orm_mode = True


class Attendance:
    def __init__(self):
        pass


