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

- ID (UUID)
- First Name (String)
- Middle Name (String)
- Last Name (String)
- Username (String)
- Email (String)
- Password (String)
- Birthdate (Date)
- Gender (String)
- Status (List of strings)
- Assignment Submissions (List of assignment UUIDs)
- Tutoring Appointments (List of appointment UUIDs)

**Programs**

- ID (UUID)
- Teacher ID (User UUID)
- Courses (List of course UUIDs)
- Description (Text)
- Title (String)

**Courses**

- ID (UUID)
- Program ID (UUID)
- Teacher ID (UUID)
- Title (String)
- Course Prequisites (List of course UUIDs)
- Subject (String)
- Description (Text)
- Assignments (List of assignment UUIDs)

**Tutoring Appointments**

- ID (UUID)
- Tutor ID (User UUID)
- Tutee ID (User UUID)
- Course (Course UUID)
- Notes (Text)
- Report (Text)
- Title (String)

**Assignments**

- ID (UUID)
- Teacher ID (User UUID)
- Course ID (Course UUID)
- Title (String)
- Description (Text)
- Submissions (List of submission UUIDs)

**Submissions**

- ID (UUID)
- Assignment ID (Assignment UUID)
- Student ID (User UUID)
- Entry (Text or File Upload)