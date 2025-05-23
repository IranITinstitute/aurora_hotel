function showNotification(text, options = {}) {
  // Создаем элемент уведомления
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = text;

  // Настройки по умолчанию
  const settings = {
    type: 'info',     // Тип: info/success/error
    duration: 3000,   // Время показа в миллисекундах (0 = ручное закрытие)
    position: 'top-right', // Позиция: top-right/bottom-right/top-left/bottom-left
    ...options
  };

  // Добавляем классы для стилизации
  notification.classList.add(
    `notification-${settings.type}`,
    `notification-${settings.position}`
  );

  // Кнопка закрытия
  const closeButton = document.createElement('button');
  closeButton.className = 'notification-close';
  closeButton.innerHTML = '&times;';
  closeButton.onclick = () => removeNotification(notification);
  notification.appendChild(closeButton);

  // Добавляем уведомление на страницу
  document.body.appendChild(notification);

  // Автоматическое закрытие
  if (settings.duration > 0) {
    setTimeout(() => {
      removeNotification(notification);
    }, settings.duration);
  }

  // Функция удаления с анимацией
  function removeNotification(element) {
    element.classList.add('hide');
    setTimeout(() => element.remove(), 300);
  }
}



let startDate = 1;
let endDate = 1;


if (window.location.pathname.includes('/booking')) {

    const params = new URLSearchParams(window.location.search);
    startDate = params.get('start_date');
    endDate = params.get('end_date');

    console.log(startDate, endDate);

}




document.addEventListener('DOMContentLoaded', function() {



});

const rooms = JSON.parse(document.querySelector('.block__roomlist__page').dataset.rooms);

function findRoomById(rooms, targetId) {
    return rooms.find(room => room.ID === targetId) || null;
}


// Получаем элементы DOM
const bookBtn = document.querySelector('.book-btn');
const popup = document.querySelector('.booking-popup');
const overlay = document.querySelector('.overlay');
const closeBtn = document.querySelector('.close-btn');
const bookingForm = document.querySelector('.booking-form');
const phoneInput = document.getElementById('phone');

var roomID = 1;

// Маска для телефона
phoneInput.addEventListener('input', function(e) {
    let x = e.target.value
        .replace(/\D/g, '')
        .match(/(\d{0,1})(\d{0,3})(\d{0,3})(\d{0,2})(\d{0,2})/);
    
    let mask = '+7';
    if (!x[1] && x[2]) mask = '+7' + x[2];
    if (x[2]) mask += ' (' + x[2];
    if (x[3]) mask += ') ' + x[3];
    if (x[4]) mask += '-' + x[4];
    if (x[5]) mask += '-' + x[5];
    
    e.target.value = mask;
});

// Функции для управления попапом
function openPopup(room_num) {
    roomID = room_num;
    popup.style.display = 'block';
    overlay.style.display = 'block';
}

function closePopup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';
}

// Обработчики событий

closeBtn.addEventListener('click', closePopup);
overlay.addEventListener('click', closePopup);

// Обработка отправки формы
bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value.replace(/\D/g, '');
            
    // Валидация телефона
    if (phone.length !== 11 || !phone.startsWith('7')) {
        alert('Пожалуйста, введите корректный номер телефона');
        return;
    }

    const roomData = findRoomById(rooms, roomID);

    var bookingData = {
        room: roomID,
        name: name,
        phone: parseInt(phone),
        in_date: startDate,
        out_date: endDate,
        day_price: parseInt(roomData.price)
    };

    fetch('/api/booking', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData)
    }).then();
    
    closePopup();
    bookingForm.reset();
    showNotification(`Спасибо за бронирование, ${name}, скоро мы с вами свяжемся!`, {
        type: 'success',
        duration: 5000
    });
});


// Закрытие при нажатии Esc
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closePopup();
});