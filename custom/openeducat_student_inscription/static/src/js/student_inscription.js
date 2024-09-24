odoo.define('student_inscription', function (require) {
    "use strict";

    const core = require('web.core');
    const rpc = require('web.rpc');
    const _t = core._t

    const $from = document.getElementById("studentinscription")
    //submit del form
    $from.addEventListener('submit', function (e) {
        //prevenimos el submit para poder ejecutar nuestra logica
        e.preventDefault()

        //nos traemos nuestra tabla y seleccionamos el body de nuestra tabla por cada fila
        const coursesTable = document.getElementById('courses');
        const rows = coursesTable.querySelectorAll('tbody tr');

        /*recorremos cada fila que es nuestra materios y verificamos si se selecciono una session
        para esta materia en el caso de hacerlo se agrega en un array, en caso contrario no se hace nada */
        const sessionData = [];
        rows.forEach(row => {
            const session = row.querySelector('td:nth-child(3) select').value;
            if (session != "") {
                sessionData.push({
                    session,
                });
            }
        });

        //formateamos mejor nuestro array para poder leerlo de mejor forma
        const formatSession = sessionData.map((session) => ({
            id: session.session,
        }))

        //falta comentar
        formatSession.forEach((session, index) => {
            const $inputSession = document.createElement('input');

            const sess = `id-${index + 1}`;

            $inputSession.name = sess;
            $inputSession.id = sess;
            $inputSession.style.visibility = "hidden";
            $inputSession.value = session.id;
            $from.appendChild($inputSession)
        })
        //falta comentar
        const $inputLen = document.createElement('input')
        const len = 'Len'
        $inputLen.name = "len";
        $inputLen.id = "len";
        $inputLen.style.visibility = "hidden";
        $inputLen.value = formatSession.length;
        $from.appendChild($inputLen);

        $from.submit()
    })



    $from.addEventListener('click', async function (e) {
        //nos traemos nuestra tabla y seleccionamos el body de nuestra tabla por cada fila
        const coursesTable = document.getElementById('courses');
        const rows = coursesTable.querySelectorAll('tbody tr');
        //nos traemos todas las sessiones en un arreglo
        const sessions = await rpc.query({
            'model': 'op.session',
            'method': 'search_read',
            'arg': [],
            "fields": ["classroom_id", "headquarters", "start_datetime", "faculty_id", "end_datetime", "type"] // type es el dia de se la session, dia de clase
        })
        //por cada linea hacemos una busqueda por el id seleccionado para que muestre informacion
        rows.forEach(row => {
            const $currentRow = row.querySelector('td:nth-child(3) select').value;
            if ($currentRow != '') {
                // se cambia el valor del id de string a int
                const id = parseInt($currentRow)
                //se realiza la busqueda para la session seleccionada
                const class_s = sessions.find(e => e.id == id)
                //Formateo la hora
                const start_split = class_s.start_datetime.split(' ')[1].split(':')
                const start_hour = `${start_split[0]}:${start_split[1]}`
                const end_split = class_s.end_datetime.split(' ')[1].split(':')
                const end_hour = `${end_split[0]}:${end_split[1]}`
                //obtengo la fila donde estoy parado y asigno los valores a cada columna
                row.querySelector('td:nth-child(4) span').innerText = `${class_s.faculty_id[1]}`
                row.querySelector('td:nth-child(5) span').innerText = `${class_s.headquarters}`
                row.querySelector('td:nth-child(6) span').innerText = `${start_hour}`
                row.querySelector('td:nth-child(7) span').innerText = `${end_hour}`
                row.querySelector('td:nth-child(8) span').innerText = `${class_s.classroom_id[1]}`
                row.querySelector('td:nth-child(9) span').innerText = `${class_s.type}`

            } else {
                /*obtengo la fila donde estoy parado y asigno los valores a cada columna ya que
                no se selecciono niguna*/
                const $currentRow = e.target.closest('tr')
                row.querySelector('td:nth-child(4) span').innerText = ``
                row.querySelector('td:nth-child(5) span').innerText = ``
                row.querySelector('td:nth-child(6) span').innerText = ``
                row.querySelector('td:nth-child(7) span').innerText = ``
                row.querySelector('td:nth-child(8) span').innerText = ``
                row.querySelector('td:nth-child(9) span').innerText = ``
            }
        })
    })
});
