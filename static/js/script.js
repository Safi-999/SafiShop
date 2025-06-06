// Script for navigation bar

const bar = document.getElementById('bar')
const fermer = document.getElementById('fermer')
const nav = document.getElementById('navbar')

if (bar){
    bar.addEventListener('click', () => {
        nav.classList.add('active');
    })
}

if (fermer){
    fermer.addEventListener('click', () => {
        nav.classList.remove('active');
    })
}
