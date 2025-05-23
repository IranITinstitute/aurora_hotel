document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('p[contenteditable="true"]').forEach(element => {
        let originalValue = element.textContent.trim();
        
        // Сохраняем исходное значение при фокусе
        element.addEventListener('focus', () => {
            originalValue = element.textContent.trim();
        });

        if (window.location.pathname.includes('/promo')) {
                    // Обрабатываем изменения при потере фокуса
            element.addEventListener('blur', () => {
                const newValue = element.textContent.trim();
                
                if (newValue !== originalValue) {
                    const row = element.closest('tr.clients_table_field');
                    const promoId = row.dataset.id;
                    const fieldName = element.id;
                    
                    const data = {
                        promoId: promoId,
                        [fieldName]: newValue
                    };
                    
                    console.log(data);
                    
                    fetch('/api/editPromo', { 
                        method: 'POST', 
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data) 
                    });
                }
            });
        } else if (window.location.pathname.includes('/clients')) {
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

        }

    });
    
});






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

function delete_promo(promoId) {
    console.log(`delete user ${promoId}`)
    fetch(`/api/deletePromo?promo_id=${promoId}`, {
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

function addPromo() {
    fetch(`/api/addPromo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
    }).then(response => {
        if (!response.ok) throw new Error('HTTP error');
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
    });
    window.location.reload();
}


