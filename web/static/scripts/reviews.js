document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const gradeInput = document.getElementById('grade');

    if (!gradeInput) {
        console.error('Element with id "grade" not found!');
        return;
    }

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = parseInt(this.dataset.value);
            console.log(value)
            gradeInput.value = value.toString(); // Убедитесь, что значение строка
            
            stars.forEach(s => {
                const starValue = parseInt(s.dataset.value);
                s.classList.toggle('active', starValue <= value);
            });
        });

        star.addEventListener('mouseover', function() {
            const value = parseInt(this.dataset.value);
            stars.forEach(s => {
            s.style.color = parseInt(s.dataset.value) <= value ? '#ffd700' : '#ddd';
            });
        });

        star.addEventListener('mouseout', function() {
            stars.forEach(s => {
            s.style.color = '#ddd';
            if(gradeInput.value > 0) {
                s.style.color = parseInt(s.dataset.value) <= gradeInput.value ? '#ffd700' : '#ddd';
            }
            });
        });
    });
});


