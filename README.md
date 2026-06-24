# Teacher-Tutor-Dashboard-Django

A django full-stack application for independent tutors and teachers to use with their tutees and students.

## Features

- Allows teachers to create courses/programs and related assignments
- Allows tutors to review student assignments and assignment submissions
- Allows students to sign up for courses/programs and schedule tutoring appointments
- Allows students and tutors to cancel or update appointments
- Allows teachers to review reports from appointments
- Allows teachers to review and grade assignment submissions

## Database Design/Structure

**Users**

- ID
- First Name
- Middle Name
- Last Name
- Username
- Email
- Password
- Birthdate
- Gender
- Status
- Assignment Submissions
- Tutoring Appointments

**Programs**

- ID
- Teacher ID
- Courses
- Description
- Title

**Courses**

- ID
- Program ID
- Teacher ID
- Title
- Course Prequisites
- Subject
- Assignments

**Tutoring Appointments**

- ID
- Tutor ID
- Tutee ID
- Course
- Notes
- Report
- Title

**Assignments**

- ID
- Teacher ID
- Course ID
- Title
- Description
- Submissions

**Submissions**

- ID
- Assignment ID
- Student ID
- Entry