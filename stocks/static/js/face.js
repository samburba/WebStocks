'use strict';

var mouth = document.querySelector('.mouth'),
    pupils = document.querySelectorAll('.pupil');

document.addEventListener('mousemove', debounce(function (e) {
    var x = e.clientX,
        y = e.clientY,
        height = window.innerHeight,
        width = window.innerWidth;

    if (y > height / 2) {
        mouth.classList.remove('-closed');
    } else {
        mouth.classList.add('-closed');
    }

    var deltaX = (x - width / 2) / width,
        deltaY = (y - height / 2) / height;

    [].forEach.call(pupils, function (pupil) {
        pupil.style.transform = '\ntranslateX(' + deltaX * 25 + 'px)\ntranslateY(' + deltaY * 25 + 'px)';
    });
}), 100);

function debounce(func, ms) {
    var callAllowed = true;

    return function () {
        if (!callAllowed) {
            return;
        }

        func.apply(this, arguments);

        callAllowed = false;

        setTimeout(function () {
            callAllowed = true;
        }, ms);
    };
};
