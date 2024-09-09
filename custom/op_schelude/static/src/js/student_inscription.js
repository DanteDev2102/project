odoo.define('my_module', function (require) {
    'use strict';

    var rpc = require('web.rpc');

    const $form = document.getElementById("studentinscription");

    // document.getElementById('enroll').addEventListener('click', function (e) {
    //     e.preventDefault()


    //     // Access form elements
    //     const studentElement = document.getElementById('student');
    //     const pnfElement = document.getElementById('pnf');
    //     const academicYearElement = document.getElementById('academic_year');
    //     const academicTermElement = document.getElementById('academic_erm');

    //     // Extract data
    //     const studentName = studentElement.textContent;
    //     const pnf = pnfElement.textContent;
    //     const academicYear = academicYearElement.textContent;
    //     const academicTerm = academicTermElement.textContent;

    //     // Do something with the extracted data
    //     // console.log('Student:', studentName);
    //     // console.log('PNF:', pnf);
    //     // console.log('Academic Year:', academicYear);
    //     // console.log('Academic Term:', academicTerm);

    //     const coursesTable = document.getElementById('courses');
    //     const rows = coursesTable.querySelectorAll('tbody tr');

    //     const courseData = [];

    //     rows.forEach(row => {
    //         const courseName = row.querySelector('td:nth-child(1) input').value;
    //         const batchId = row.querySelector('td:nth-child(2) select').value;
    //         const teacherId = row.querySelector('td:nth-child(3) select').value;
    //         if (batchId != "" && teacherId != "") {
    //             courseData.push({
    //                 courseName,
    //                 batchId,
    //                 teacherId
    //             });
    //         }
    //     });

    //     // console.log('Course Data:', courseData);
    //     const data = {
    //         student_name: studentName,
    //         pnf: pnf,
    //         academic_year: academicYear,
    //         academic_term: academicTerm,
    //         courses: courseData
    //     };
    //     // console.log(rpcData)
    //     // fetch('/student-register/', {
    //     //     method: 'POST',
    //     //     headers: {
    //     //         'Content-Type': 'application/json'
    //     //     },
    //     //     body: JSON.stringify(rpcData)
    //     // })

    // });


    $form.addEventListener('submit', function (e) {
        e.preventDefault()

        const coursesTable = document.getElementById('courses');
        const rows = coursesTable.querySelectorAll('tbody tr');

        const courseData = [];

        rows.forEach(row => {
            const courseName = row.querySelector('td:nth-child(1) input').value;
            const batchId = row.querySelector('td:nth-child(2) select').value;
            const teacherId = row.querySelector('td:nth-child(3) select').value;
            if (batchId != "" && teacherId != "") {
                courseData.push({
                    courseName,
                    batchId,
                    teacherId
                });
            }
        });

        const formatCourses = courseData.map((course) => ({
            name: course.courseName,
            batchId: +course.batchId,
            teacherId: +course.teacherId
        }))

        formatCourses.forEach((course, index) => {
            const $inputName = document.createElement('input')
            const $inputBatch = document.createElement('input')
            const $inputTeacher = document.createElement('input')

            const name = `name-${index + 1}`;
            const batch = `batch-${index + 1}`;
            const teacher = `teacher-${index + 1}`;

            $inputName.name = name;
            $inputName.id = name;
            $inputName.style.visibility = "hidden";
            $inputName.value = course.name;
            $form.appendChild($inputName)

            $inputBatch.name = batch;
            $inputBatch.id = batch;
            $inputBatch.style.visibility = "hidden";
            $inputBatch.value = course.batchId;
            $form.appendChild($inputBatch)

            $inputTeacher.name = teacher;
            $inputTeacher.id = teacher;
            $inputTeacher.style.visibility = "hidden";
            $inputTeacher.value = course.teacherId;
            $form.appendChild($inputTeacher)


        })

        const $inputLen = document.createElement('input')
        const len = 'Len'
        $inputLen.name = "len";
        $inputLen.id = "len";
        $inputLen.style.visibility = "hidden";
        $inputLen.value = formatCourses.length;
        $form.appendChild($inputLen)

        $form.submit()
    })
});