import mysql.connector
import datetime
from decimal import Decimal


class EnrollDB:
    """Application for an enrollment database on MySQL"""

    def connect(self):
        """Makes a connection to the database and returns connection to caller"""
        try:
            # TODO: Fill in your connection information
            print("Connecting to database.")
            self.cnx = mysql.connector.connect(
                user="testuser",
                password="304testpw",
                host="localhost",
                database="testuser",
            )
            return self.cnx
        except mysql.connector.Error as err:
            print(err)

    def init(self):
        """Creates and initializes the database"""
        fileName = "university.ddl"
        print("Loading data")

        try:
            cursor = self.cnx.cursor()
            with open(fileName, "r") as infile:
                st = infile.read()
                commands = st.split(";")
                for line in commands:
                    # print(line.strip("\n"))
                    line = line.strip()
                    if line == "":  # Skip blank lines
                        continue

                    cursor.execute(line)

            cursor.close()
            self.cnx.commit()
            print("Database load complete")
        except mysql.connector.Error as err:
            print(err)
            self.cnx.rollback()

    def close(self):
        try:
            print("Closing database connection.")
            self.cnx.close()
        except mysql.connector.Error as err:
            print(err)

    def listAllStudents(self):
        print("Executing list all students.")

        cursor = self.cnx.cursor()
        cursor.execute("SELECT * FROM student")
        result = cursor.fetchall()

        for row in result:
            r0, r1, r2, r3, r4 = row
            if r3 is not None:
                r3 = r3.strftime("%Y-%m-%d")
            else:
                r3 = "N/A"
            r4 = float(r4) if r4 is not None else 0.00
            print(f"{r0}, {r1}, {r3}, {r4:.2f}")
        cursor.close()
        return " "

    def listDeptProfessors(self, deptName):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT pname, dname FROM prof")
        result = cursor.fetchall()

        for row in result:
            r0, r1 = row
            if deptName == r1:
                print(f"{r0}, {r1}")
        cursor.close()
        return " "

    def listCourseStudents(self, courseNum):
        cursor = self.cnx.cursor()
        cursor.execute(
            "SELECT S.sid, S.sname, E.cnum, E.secnum \
                       FROM student S \
                       JOIN enroll E ON S.sid = E.sid \
                       JOIN section SEC ON E.cnum = SEC.cnum AND E.secnum = SEC.secnum;"
        )
        result = cursor.fetchall()

        for row in result:
            r0, r1, r2, r3 = row
            if courseNum == r2:
                print(f"{r0}, {r1}, {r2}, {r3}")
        cursor.close()
        return " "

    def computeGPA(self, studentId):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT gpa FROM student WHERE sid = %s"
            cursor.execute(query, (studentId,))
            result = cursor.fetchone()

            if result:
                gpa = result[0]
                print(f"GPA: {gpa}")
            else:
                print(f"No GPA found!")
            return cursor

        except mysql.connector.Error as err:
            print(err)
            return None

    def addStudent(self, studentId, studentName, sex, birthDate):
        try:
            cursor = self.cnx.cursor()
            query = "INSERT INTO student (sid, sname, sex, birthdate) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (studentId, studentName, sex, birthDate))
            self.cnx.commit()
            print(f"Student {studentId} added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def deleteStudent(self, studentId):
        try:
            cursor = self.cnx.cursor()

            check_query = "SELECT sid FROM student WHERE sid = %s"
            cursor.execute(check_query, (studentId,))
            student = cursor.fetchone()

            if student:
                delete_query = "DELETE FROM student WHERE sid = %s"
                cursor.execute(delete_query, (studentId,))
                self.cnx.commit()
                print(f"Student {studentId} removed successfully!")
            else:
                print(f"Student {studentId} does not exist.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def updateStudent(self, studentId, studentName, sex, birthDate, gpa):
        try:
            cursor = self.cnx.cursor()
            query = "UPDATE student SET sname = %s, sex = %s, birthDate = %s, gpa = %s WHERE sid = %s"
            cursor.execute(query, (studentName, sex, birthDate, gpa, studentId))
            self.cnx.commit()
            print(f"Student {studentId} updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def newEnroll(self, studentId, courseNum, sectionNum, grade):
        """Creates a new enrollment in a course section."""

        try:
            cursor = self.cnx.cursor()
            query = "INSERT INTO enroll (sid, cnum, secnum, grade) VALUES (%s,%s,%s,%s)"
            cursor.execute(query, (studentId, courseNum, sectionNum, grade))
            print(f"Student {studentId} has been Enrolled in {courseNum}!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def updateStudentGPA(self, studentId):
        """Updates a student's GPA based on courses taken."""
        try:
            cursor = self.cnx.cursor()
            query = """
        UPDATE student
        SET gpa = (
            SELECT AVG(grade)
            FROM enroll
            WHERE sid = %s
        )
        WHERE sid = %s
        """
            cursor.execute(query, (studentId, studentId))
            self.cnx.commit()
            print(f"Student {studentId}'s GPA has been updated!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def removeStudentFromSection(self, studentId, courseNum, sectionNum):
        """Removes a student friom a course and updates their GPA."""

        # TODO: Execute statement. Make sure to commit
        return

    def updateStudentMark(self, studentId, courseNum, sectionNum, grade):
        """Updates a student's mark in an enrolled course section and updates their grade."""

        # TODO: Execute statement. Make sure to commit
        return

    def query1(self):
        """Return the list of students (id and name) that have not registered in any course section. Hint: Left join can be used instead of a subquery."""

        # TODO: Execute the query and return a cursor
        return None

    def query2(self):
        """For each student return their id and name, number of course sections registered in (called numcourses), and gpa (average of grades).
        Return only students born after March 15, 1992. A student is also only in the result if their gpa is above 3.1 or registered in 0 courses.
        Order by GPA descending then student name ascending and show only the top 5."""

        # TODO: Execute the query and return a cursor
        return None

    def query3(self):
        """For each course, return the number of sections (numsections), total number of students enrolled (numstudents), average grade (avggrade), and number of distinct professors who taught the course (numprofs).
        Only show courses in Chemistry or Computer Science department. Make sure to show courses even if they have no students. Do not show a course if there are no professors teaching that course.
        Format:
        cnum, numsections, numstudents, avggrade, numprof"""

        # TODO: Execute the query and return a cursor
        return None

    def query4(self):
        """Return the students who received a higher grade than their course section average in at least two courses. Order by number of courses higher than the average and only show top 5.
        Format:
        EmployeeId, EmployeeName, orderCount"""

        # TODO: Execute the query and return a cursor
        return None

    # Do NOT change anything below here
    def resultSetToString(self, cursor, maxrows):
        output = ""
        cols = cursor.column_names
        output += "Total columns: " + str(len(cols)) + "\n"
        output += str(cols[0])
        for i in range(1, len(cols)):
            output += ", " + str(cols[i])
        for row in cursor:
            output += "\n" + str(row[0])
            for i in range(1, len(cols)):
                output += ", " + str(row[i])
        output += "\nTotal results: " + str(cursor.rowcount)
        return output


# Main execution for testing
enrollDB = EnrollDB()
enrollDB.connect()
enrollDB.init()

print(enrollDB.listAllStudents())

print("Executing list professors in a department: Computer Science")
print(enrollDB.listDeptProfessors("Computer Science"))
print("Executing list professors in a department: none")
print(enrollDB.listDeptProfessors("none"))

print("Executing list students in course: COSC 304")
enrollDB.listCourseStudents("COSC 304")
print()
print("Executing list students in course: DATA 301")
enrollDB.listCourseStudents("DATA 301")
print()

print("Executing compute GPA for student: 45671234")
enrollDB.resultSetToString(enrollDB.computeGPA("45671234"), 10)
print("Executing compute GPA for student: 00000000")
enrollDB.resultSetToString(enrollDB.computeGPA("00000000"), 10)
print()

print("Adding student 55555555:")
enrollDB.addStudent("55555555", "Stacy Smith", "F", "1998-01-01")
print("Adding student 11223344:")
enrollDB.addStudent("11223344", "Jim Jones", "M", "1997-12-31")
print(enrollDB.listAllStudents())
print()

print("Test delete student:")
print("Deleting student 99999999:")
enrollDB.deleteStudent("99999999")
# Non-existing student
print("Deleting student 00000000:")
enrollDB.deleteStudent("00000000")
print(enrollDB.listAllStudents())

print("Updating student 99999999:")
enrollDB.updateStudent("99999999", "Wang Wong", "F", "1995-11-08", 3.23)
print("Updating student 00567454:")
enrollDB.updateStudent("00567454", "Scott Brown", "M", None, 4.00)
print(enrollDB.listAllStudents())

print("Test new enrollment in COSC 304 for 98123434:")
enrollDB.newEnroll("98123434", "COSC 304", "001", 2.51)
print()

enrollDB.init()
print("Test update student GPA for student:")
enrollDB.newEnroll("98123434", "COSC 304", "001", 3.97)
enrollDB.updateStudentGPA("98123434")

print("Test update student mark for student 98123434 to 3.55:")
enrollDB.updateStudentMark("98123434", "COSC 304", "001", 3.55)

enrollDB.init()

enrollDB.removeStudentFromSection("00546343", "CHEM 113", "002")

# Queries
# Re-initialize all data
enrollDB.init()
print(enrollDB.resultSetToString(enrollDB.query1(), 100))
print(enrollDB.resultSetToString(enrollDB.query2(), 100))
print(enrollDB.resultSetToString(enrollDB.query3(), 100))
print(enrollDB.resultSetToString(enrollDB.query4(), 100))

enrollDB.close()
