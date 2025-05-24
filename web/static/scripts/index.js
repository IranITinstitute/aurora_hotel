function openComplaintModal() {
    document.getElementById('complaint-modal__overlay').style.display = 'block';
}

function closeComplaintModal() {
    document.getElementById('complaint-modal__overlay').style.display = 'none';
}

// Закрытие по клику вне области
document.getElementById('complaint-modal__overlay').addEventListener('click', function(e) {
    if(e.target === this) closeComplaintModal();
});



// Закрытие по ESC
document.addEventListener('keydown', function(e) {
    if(e.key === 'Escape') closeComplaintModal();
});




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

document.getElementById('passport').addEventListener('input', function(e) {
    // Получаем значение и удаляем все нецифровые символы
    let value = e.target.value.replace(/\D/g, '');
    
    // Форматируем с пробелами
    let formatted = '';
    for (let i = 0; i < value.length; i++) {
        if (i === 2 || i === 4) formatted += ' ';
        formatted += value[i];
    }
    
    // Обрезаем до 10 цифр (2+2+6) + 2 пробела = 12 символов
    e.target.value = formatted.substring(0, 12);
});

// Дополнительная валидация при потере фокуса
document.getElementById('passport').addEventListener('blur', function(e) {
    const isValid = /^\d{2} \d{2} \d{6}$/.test(e.target.value);
});


document.getElementById('promo').addEventListener('input', function(e) {
    let value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
    let newValue = '';
    
    // Форматируем по шаблону
    for (let i = 0; i < value.length; i++) {
        if (i === 0 && /[A-Z]/.test(value[i])) { // Первый символ - буква
            newValue += value[i];
        } 
        else if ((i === 1 || i === 2) && /\d/.test(value[i])) { // 2 и 3 символы - цифры
            newValue += value[i];
        }
        else if ((i === 3 || i === 4) && /[A-Z]/.test(value[i])) { // 4 и 5 символы - буквы
            newValue += value[i];
        }
    }
    
    e.target.value = newValue;
});

// Проверка при потере фокуса
document.getElementById('promo').addEventListener('blur', function(e) {
    const isValid = /^[A-Z]\d{2}[A-Z]{2}$/.test(e.target.value);
    if (!isValid) {
        alert('Неверный формат промокода! Пример: Z00YH');
    }
});


var discount = 0;

function promoCheck() {
  var promo = document.querySelector('#promo').value
  console.log(promo)

  fetch(`/api/checkPromo?promo_name=${promo}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
    }).then(response => {
        if (!response.ok) throw new Error('HTTP error');
        return response.json();
    })
    .then(data => {
        console.log(data); // Проверьте здесь
        if (discount == 0) {
            if (data.discount && data.discount !== "NotFound") {
                console.log("Скидка активна:", data.discount + "%");
                discount = data.discount;
                // Здесь можно выполнить действия для действующей скидки
                const oldPrice = parseInt(document.querySelector('#allSummBooking').innerHTML);
                document.querySelector('#allSummBooking').innerHTML = oldPrice - Math.floor(oldPrice * discount / 100);


                const summDiv = document.querySelector('.summ');
                const newElement = document.createElement('h3');
                newElement.textContent = `${oldPrice} ₽`; // Замените на нужный текст
                // Вставка после первого элемента
                summDiv.children[0].after(newElement);


            } else {
                console.log("Скидка не найдена или недействительна");
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



let services = null;
let services_list = null;

const select = document.getElementById('serviceSelect');
const selectedServices = document.getElementById('selectedServices');
let selected = [];


fetch('/api/getAvailableServices')
  .then(response => response.json())
  .then(data => {
    services_list = data;
    services = data.map(service => 
      `${service.name} - ${service.price}p.`
    );
    // Заполняем select опциями
    services.forEach(service => {
        const option = document.createElement('option');
        option.value = service;
        option.textContent = service;
        select.appendChild(option);
    });
  })
  .catch(error => console.error('Error:', error));



var servicesList = null;
var countedPrice = null;

// Обработчик выбора услуги
select.addEventListener('change', function(e) {
    if(this.value && !selected.includes(this.value)) {
        selected.push(this.value);
        updateSelectedServices();
        updateSelectOptions();
        this.value = ''; // Сбрасываем выбор
    }
    let data = parseServices(selected);
    let servicesPrice = 0;
    for (let i = 0; i < data.services.length; i++) {
      servicesPrice += data.services[i].price;
    }
    
    servicesList = data;

    try{
      let i = selected.length - 1   
      const oldPrice = parseInt(document.querySelector('#allSummBooking').innerHTML);


        document.querySelector('#allSummBooking').innerHTML = oldPrice + parseServices([selected[i]]).services[0].price;
        countedPrice = document.querySelector('#allSummBooking').innerHTML;
      
    } catch {

    }
    
});


function removeElementService(service) {
  selected = selected.filter(s => s !== service);
  updateSelectOptions();
  updateSelectedServices();
}
// Удаление услуги
function removeService(service) {
    selected = selected.filter(s => s !== service);
    
    let data = parseServices([service]);
    let servicesPrice = 0;
    for (let i = 0; i < data.services.length; i++) {
      servicesPrice += data.services[i].price;
    }
    

    try{
      const oldPrice = parseInt(document.querySelector('#allSummBooking').innerHTML);
      let newPrice = oldPrice - data.services[0].price
      document.querySelector('#allSummBooking').innerHTML = 0;
      document.querySelector('#allSummBooking').innerHTML = newPrice;
    } catch {

    }

    
    updateSelectOptions();
    updateSelectedServices();
}

function parseServices(inputArray) {
    return {
        services: inputArray.map(item => {
            // Разделяем строку на название и цену
            const [name, pricePart] = item.split(' - ');
            
            // Извлекаем числовое значение цены
            const price = parseInt(pricePart.replace('p.', '').trim(), 10);
            
            return {
                name: name.trim(),
                price: price
            };
        })
    };
}


// Обновление отображения выбранных услуг
function updateSelectedServices() {
    
    selectedServices.innerHTML = selected.map(service => `
        <div class="service-tag">
            ${service}
            <button onclick="removeService('${service}')">×</button>
        </div>
    `).join('');

    //let data = parseServices([selected]);
}



// Обновление доступных опций в select
function updateSelectOptions() {
    const options = select.querySelectorAll('option');
    options.forEach(option => {
        if(option.value) {
            option.disabled = selected.includes(option.value);
        }
    });
}

// Инициализация
updateSelectOptions();









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

var booking_price = null;

// Функции для управления попапом
function openPopup(room_num, onePrice) {
  var diffDays = 0;

  // Функция для преобразования даты из формата DD.MM.YYYY
  function parseDate(dateString) {
    const [day, month, year] = dateString.split('.');
    return new Date(year, month - 1, day); // Месяцы в JS начинаются с 0
  }

  try {

    const timeDiff = parseDate(endDate) - parseDate(startDate);
    diffDays = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
  } catch (error) {
  }


    roomID = room_num;
    popup.style.display = 'flex';
    overlay.style.display = 'block';
    
    let booking_info = {
      "room_id": room_num,
      "booking_price": onePrice * diffDays
    }

    booking_price = onePrice * diffDays;

    document.querySelector('#allSummBooking').innerHTML = onePrice * diffDays;

    console.log(booking_info)
}

function closePopup() {
    popup.style.display = 'none';
    overlay.style.display = 'none';

    document.querySelectorAll('.service-tag').forEach(div => {
        const text = div.childNodes[0].textContent.trim();
        removeElementService(text)
        div.remove(); // если нужно удалить весь элемент
    });
    
    
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

    var servicesIds = null;

    try {
        servicesIds = servicesList.services.map(selected => {
        const service = services_list.find(item => 
            item.name === selected.name && 
            item.price === selected.price
        );
            return service ? service.id : null;
        }).filter(id => id !== null);
    } catch {
        countedPrice = booking_price;
    }
    

    

    var bookingData = {
        room: roomID,
        name: name,
        mail: document.querySelector('#email').value,
        bornDate: document.querySelector('#borndate').value.replace(/(\d{4})-(\d{2})-(\d{2})/, '$3.$2.$1') || '',
        passNum: document.querySelector('#passport').value,
        services: servicesIds,
        paymentType: document.querySelector('#payment_type').value,
        phone: parseInt(phone),
        in_date: startDate,
        out_date: endDate,
        day_price: parseInt(roomData.price),
        countedPrice: parseInt(countedPrice)
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