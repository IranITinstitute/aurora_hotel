document.addEventListener('DOMContentLoaded', function() {
        flatpickr("#start-date", {
            locale: "ru", // Русский язык
            dateFormat: "d.m.Y", // Формат даты
            minDate: "today", // Минимальная дата — сегодня
            onChange: function(selectedDates, dateStr) {
                endPicker.set("minDate", dateStr); // Устанавливаем мин. дату для выезда
            }
        });

        const endPicker = flatpickr("#end-date", {
            locale: "ru",
            dateFormat: "d.m.Y",
            minDate: new Date().fp_incr(1) // Завтрашняя дата
        });

        // Обработка кнопки
        document.querySelector('#check_booking').addEventListener('click', function() {
            const startDate = document.getElementById('start-date').value;
            const endDate = document.getElementById('end-date').value;
            
            if (!startDate || !endDate) {
                alert('Пожалуйста, выберите обе даты!');
                return;
            }
            
            
            console.log(`${startDate} --- ${endDate}`);
            
            window.location.href = `/booking?start_date=${startDate}&end_date=${endDate}`;
        });

        if (window.location.pathname.includes('/booking')) {

            const params = new URLSearchParams(window.location.search);
            const startDate = params.get('start_date');
            const endDate = params.get('end_date');

            if (startDate) document.getElementById('start-date').value = startDate;
            if (endDate) document.getElementById('end-date').value = endDate;
        }

    });