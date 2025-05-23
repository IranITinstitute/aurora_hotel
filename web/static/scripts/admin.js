document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('p[contenteditable="true"]').forEach(element => {
    let originalValue = element.textContent.trim();
    
    // Сохраняем исходное значение при фокусе
    element.addEventListener('focus', () => {
        originalValue = element.textContent.trim();
    });

    // Обрабатываем изменения при потере фокуса
    element.addEventListener('blur', () => {
        const newValue = element.textContent.trim();
        
        if (newValue !== originalValue) {
            const row = element.closest('tr.clients_table_field');
            const userId = row.dataset.id;
            const fieldName = element.id;
            
            const data = {
                userId: userId,
                [fieldName]: newValue
            };
            
            console.log(data);
            
            fetch('/api/editClient', { 
                method: 'POST', 
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data) 
            });
        }
    });
    });
    
});



console.log(JSON.parse(document.querySelector('.block__roomlist__page__content').dataset.bookings))


function booking_cancel(bookingId) {
    console.log("отмена бронирования с id", bookingId)

    fetch(`/api/booking_cancel?booking_id=${bookingId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
    }).then();
    window.location.reload();
}

function delete_user(userId) {
    console.log(`delete user ${userId}`)
    fetch(`/api/deleteClient?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
    }).then();
    window.location.reload();
}

function addUser() {
    let userId = 0;
    fetch(`/api/addClient`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
    }).then(response => {
        if (!response.ok) throw new Error('HTTP error');
        return response.json();
    })
    .then(data => {
        userId = data.userId; // Присваивание работает здесь
        console.log('New ID:', userId); // Проверьте здесь
    })
    .catch(error => {
        console.error('Error:', error);
    });
    window.location.reload();
}


